#!/usr/bin/env python3
"""A client for `indiacode.gov.in`, the Government of India's legislative repository.

**Read `../README.md` first if you are new here; read this docstring before changing the client.**

India Code migrated from `indiacode.nic.in` to `indiacode.gov.in` some time between 2026-07-31 and
2026-09-16, and the new site is a different machine: a DSpace 7 Angular instance with an open REST
API, where the old one was a JSPUI whose machine interfaces answered 404. The repo's July
reconnaissance recorded those 404s, and **they still reproduce today against the old host**, which
is the trap this module exists on the far side of. `method.md` §4 says a zero is a question; a 404
that reproduces is a question too, and "has this host moved" is the cheapest positive control there
is. See `../README.md`, "What the reconnaissance found".

Three properties of the API shape everything below:

- **`discover/search/objects` is public and unauthenticated**; `core/items` is not (401, which is
  ordinary DSpace 7). So enumeration goes through search, and the free-text query is the `act_id`.
  Search is a *free-text* index, so it returns items belonging to other Acts that happen to match;
  every result is filtered on an exact `dc.identifier.act_id` before it is believed.
- **Each section of each Act is its own item**, carrying the current as-amended text in
  `dc.identifier.section_page_note` and the amendment provenance in a separate
  `dc.identifier.section_footnote`. That separation is why this repo stores provisions rather than
  instruments on the Act layer — `this.i` @4sxgog — and why `render()` below never joins the two.
- **Delegated instruments carry no text field at all**, only PDF bitstreams. Those PDFs are
  watermarked and the watermark defeats our own extraction (`this.i` @yt6p5u4j), so the text comes
  from the item's `TEXT` bundle, which is the publisher's own extraction, with ours as the control.

Politeness: one request at a time, a delay between them, and a cache under `.cache/`. This is
somebody else's host and there is no rate limit to hide behind.
"""

from __future__ import annotations

import hashlib
import html as html_module
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from lawcorpus.errors import LawcorpusError

BASE = "https://indiacode.gov.in/server/api"
SITE = "https://indiacode.gov.in"
UA = "bakobo-id-law-kit/0.1 (corpus harvest; +https://github.com/bakobo/aadhaar)"
DELAY = 1.0
PAGE_SIZE = 100

# The act_id is India Code's own internal key for an instrument and everything hangs off it. These
# were resolved by search and pinned here, because a free-text search for "Copyright Act 1957"
# returns state Acts of the same name and the wrong one would be invisible afterwards: real law,
# correctly manifested, under the wrong title (`method.md` §2).
ACT_IDS = {
    "aadhaar-2016": "AC_CEN_37_85_00001_201618_1517807328460",
    "dpdp-2023": "AC_CEN_45_0_00003_2023-22_1763464807080",
    "copyright-1957": "AC_CEN_9_30_00006_195714_1517807321712",
    "it-2000": "AC_CEN_45_76_00001_200021_1517807324077",
    "official-languages-1963": "AC_CEN_5_39_00001_196319_1517807319151",
}


class IndiaCodeError(LawcorpusError):
    """India Code answered, and what it said cannot be used."""

    code = "e.source.unusable.indiacode.f"


class IdentityError(IndiaCodeError):
    """The item returned is not the item the work-list named. `method.md` §2."""

    code = "e.state.conflict.identity.f"


def meta(item: dict, key: str, default=None):
    """One metadata value. DSpace returns a list of dicts per key; only `linked_id` repeats."""
    values = item.get("metadata", {}).get(key)
    return values[0]["value"] if values else default


def metas(item: dict, key: str) -> list:
    return [v["value"] for v in item.get("metadata", {}).get(key, [])]


# --------------------------------------------------------------------------------------------
# Rendering India Code's HTML fields to text
# --------------------------------------------------------------------------------------------

# `section_page_note` is HTML: indentation spans, `<br/>` plus a borderless `<hr/>` as a paragraph
# break, `<i>` on cross-reference numerals, and `<sup>n</sup>` immediately before the `[` that opens
# a span some amending Act inserted or substituted.
_SUP = re.compile(r"<sup>\s*(\d+)\s*</sup>")
_BREAK = re.compile(r"<br\s*/?>", re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")
_SPACES = re.compile(r"[ \t]+")
_BLANKS = re.compile(r"\n{3,}")


def render(fragment) -> str:
    """India Code's HTML as plain text, with the amendment marks kept.

    The superscript marker is kept as a bare digit — `1[Judge of a High Court]` — because that is
    how the printed consolidated editions render it, including UIDAI's own, so a passage stored here
    and the same passage extracted from a PDF can be compared. `tools/check-quotes.py` folds the
    marks out of both sides before matching, so a finding may quote the sentence as a reader would
    write it.
    """
    if not fragment:
        return ""
    text = _SUP.sub(r"\1", fragment)
    text = _BREAK.sub("\n", text)
    text = _TAG.sub("", text)
    text = html_module.unescape(text)
    text = text.replace(" ", " ")
    lines = [_SPACES.sub(" ", line).strip() for line in text.split("\n")]
    return _BLANKS.sub("\n\n", "\n".join(lines)).strip()


def section_text(item: dict) -> str:
    """The stored text of a section item: its number, its title, and its current text.

    Three publisher fields joined in the publisher's own order, and nothing else. In particular
    **not** `section_footnote`, which reproduces the superseded words in quotation marks and is
    written to `sources/amendment-footnotes.tsv` as provenance instead — `this.i` @gogceltr.
    """
    number = meta(item, "dc.identifier.section_number", "")
    title = (meta(item, "dc.title", "") or "").strip()
    body = render(meta(item, "dc.identifier.section_page_note", ""))
    heading = f"{number}. {title}".strip()
    return f"{heading}\n{body}\n" if body else f"{heading}\n"


# --------------------------------------------------------------------------------------------
# The client
# --------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Bitstream:
    bundle: str
    name: str
    size: int
    url: str


class IndiaCode:
    """A polite, cached client. One connection, one request at a time, a delay between them."""

    def __init__(self, cache: Path, delay: float = DELAY, transport=None):
        self.cache = Path(cache)
        self.cache.mkdir(parents=True, exist_ok=True)
        self.delay = delay
        self._transport = transport or self._urlopen
        self._last = 0.0

    def _urlopen(self, url: str, accept: str) -> bytes:
        wait = self.delay - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                body = response.read()
        except urllib.error.HTTPError as e:
            raise IndiaCodeError(
                f"India Code answered {e.code} for {url}. Before concluding anything about Indian "
                f"law from that, fetch {SITE} itself: this host has moved once already, and a 404 "
                f"that reproduces is a question, not an answer."
            ) from e
        except urllib.error.URLError as e:
            raise IndiaCodeError(
                f"India Code could not be reached at {url}: {e.reason}. Transient or a network "
                f"path problem; retrying later may help."
            ) from e
        finally:
            self._last = time.monotonic()
        return body

    def fetch(self, url: str, accept: str = "application/json", binary: bool = False) -> bytes:
        name = hashlib.sha256(url.encode()).hexdigest()[:24] + (".bin" if binary else ".json")
        path = self.cache / name
        if path.exists():
            return path.read_bytes()
        body = self._transport(url, accept)
        path.write_bytes(body)
        return body

    def api(self, path: str, **params) -> dict:
        url = f"{BASE}/{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        return json.loads(self.fetch(url))

    def search(self, query: str, size: int = PAGE_SIZE, page: int = 0) -> dict:
        return self.api("discover/search/objects", query=query, size=size, page=page)

    def search_all(self, query: str) -> list:
        """Every hit for a free-text query, paged. Unfiltered — the caller must filter."""
        items, page = [], 0
        while True:
            result = self.search(query, page=page)["_embedded"]["searchResult"]
            items += [o["_embedded"]["indexableObject"] for o in result["_embedded"]["objects"]]
            if page + 1 >= result["page"]["totalPages"]:
                return items
            page += 1

    def act_items(self, act_id: str) -> list:
        """Every item India Code files under one `act_id`, in document order where it says one.

        Filtered on an exact `act_id` match, because the query is free text: a search for the
        Aadhaar Act's id returns six items belonging to State Acts that merely score against it.
        """
        return [o for o in self.search_all(act_id) if meta(o, "dc.identifier.act_id") == act_id]

    def item_by_handle(self, handle: str) -> dict:
        """One item, by its DSpace handle. Search by the numeric part, then match exactly."""
        for candidate in self.search_all(handle.rsplit("/", 1)[-1]):
            if candidate["handle"] == handle:
                return candidate
        raise IndiaCodeError(
            f"No item on India Code has the handle '{handle}'. Handles are stable, so this is "
            f"either a typo in the work-list or an item the publisher has withdrawn."
        )

    def bitstreams(self, item: dict) -> list:
        out = []
        for bundle in self.api(f"core/items/{item['id']}/bundles")["_embedded"]["bundles"]:
            listing = self.api(f"core/bundles/{bundle['uuid']}/bitstreams")
            for stream in listing["_embedded"]["bitstreams"]:
                out.append(
                    Bitstream(
                        bundle=bundle["name"],
                        name=stream["name"],
                        size=stream["sizeBytes"],
                        url=stream["_links"]["content"]["href"],
                    )
                )
        return out

    def content(self, stream: Bitstream) -> bytes:
        return self.fetch(stream.url, accept="*/*", binary=True)


# --------------------------------------------------------------------------------------------
# The shape oracles
# --------------------------------------------------------------------------------------------


def section_order(items: list) -> list:
    """The section items of one Act, in the publisher's declared document order."""
    return sorted(items, key=lambda o: int(meta(o, "dc.identifier.order_number", "0")))


def walk_next_section(items: list) -> list:
    """Follow `dc.identifier.next_section` from the first section, and report what it reaches.

    India Code authors this pointer, so it is independent evidence of completeness in the way
    Japan's `<TOC><ArticleRange>` is — the fourth free shape oracle in this programme. **It is
    partial, and its blind spot is the one that matters**: every lettered insertion (3A, 8A, 23A,
    33A–33F, 50A in the Aadhaar Act) carries a null pointer and is never pointed at, so a walk that
    reaches the last section cleanly can still be missing every provision an amending Act inserted.
    Pair it with `section_order` and a declared count. `this.i` @6v3ks6eo.
    """
    by_number = {meta(o, "dc.identifier.section_number"): o for o in items}
    first = section_order(items)[0] if items else None
    reached, current = [], meta(first, "dc.identifier.section_number") if first else None
    while current and current in by_number and current not in reached:
        reached.append(current)
        pointer = meta(by_number[current], "dc.identifier.next_section")
        current = pointer.split(".", 1)[0].strip() if pointer else None
    return reached
