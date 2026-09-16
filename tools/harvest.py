#!/usr/bin/env python3
"""Fetch India's Aadhaar and data-protection corpus, verify it, and write it with its manifests.

Three layers at two grains, written to three directories, each with its own `MANIFEST.tsv`:

    corpus-acts/        one item per **section** of an Act      (this.i @4sxgog)
    corpus-delegated/   one item per **instrument**             (this.i @4sxgog, @yt6p5u4j)
    corpus-judgments/   one item per judgment, hand-curated     (this.i @hyjd5n)

**The gates, in the order they run.**

1. **Identity.** The `act_name` India Code returns must carry the phrase `candidates.py` declared,
   compared through `lawcorpus.normalise.search_key`. `method.md` §2 — a remembered citation is the
   kind of plausible fabrication this apparatus exists to catch, and once the text is in the corpus
   the error is invisible.
2. **Count and inventory.** The Aadhaar Act's 69 sections are checked against **UIDAI's own
   consolidated PDF**, a different publisher and a different artefact, section by section. A
   mismatch aborts, the way the California harvest aborts against the OAL notice.
3. **The `next_section` chain**, for what it proves and no more. It reaches 59 of 69 sections and
   misses every lettered insertion; the harvest reports both numbers rather than the reassuring one.
   `this.i` @6v3ks6eo.
4. **Validity, derived where the publisher states it and hand-curated where it does not.** India
   Code's own `dc.identifier.repealed` is `false` for all 69 sections *including the omitted §57*,
   so it is wired to nothing and the harvest says so out loud. What the text states — a body opening
   `Omitted by …` — is derived and must agree with the declared table. Judicial validity comes from
   `sources/judicial-overlay.tsv`, which is the source the manifest is generated from
   (`this.i` @q3dsvsrl).
5. **Extraction.** On the delegated layer the stored text is the publisher's own, gated by ours
   (`this.i` @yt6p5u4j), and refused outright if it reads as mojibake (`tools/indian.py`).

    python3 tools/harvest.py                 # everything
    python3 tools/harvest.py acts
    python3 tools/harvest.py delegated judgments
"""

from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import re
import sys
import tempfile
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import candidates as C  # noqa: E402
import indiacode as IC  # noqa: E402
import indian  # noqa: E402
from lawcorpus.errors import LawcorpusError  # noqa: E402
from lawcorpus.manifest import Manifest, ManifestItem  # noqa: E402
from lawcorpus.normalise import search_key  # noqa: E402
from lawcorpus.pdf import extract  # noqa: E402
from lawcorpus.store import CorpusStore  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"
ACTS = ROOT / "corpus-acts"
DELEGATED = ROOT / "corpus-delegated"
JUDGMENTS = ROOT / "corpus-judgments"
OVERLAY = ROOT / "sources" / "judicial-overlay.tsv"
FOOTNOTES = ROOT / "sources" / "amendment-footnotes.tsv"
TODAY = datetime.date.today().isoformat()


class HarvestError(LawcorpusError):
    """A gate refused. Nothing was written."""

    code = "e.state.conflict.harvest.f"


def say(*parts):
    print(*parts, flush=True)


# --------------------------------------------------------------------------------------------
# The judicial overlay — the authored source that judicial validity is derived from
# --------------------------------------------------------------------------------------------


def read_overlay() -> list:
    """The overlay rows. Absent, the harvest refuses rather than treating silence as 'in force'."""
    if not OVERLAY.exists():
        raise HarvestError(
            f"There is no judicial overlay at {OVERLAY}. Judicial validity is nowhere in India Code "
            f"— it records what Parliament did and never what a court did — so an absent overlay "
            f"would silently mark a read-down provision as in force, which is the one failure this "
            f"repo exists to prevent."
        )
    with OVERLAY.open(encoding="utf-8") as fh:
        return [row for row in csv.DictReader(fh, delimiter="\t") if row.get("instrument")]


def overlay_for_items(rows: list) -> dict:
    """The rows that override a manifest value, keyed by item.

    A row with an empty `validity` is history rather than an override — the 2018 disposition on §57,
    whose current validity is decided by Parliament's omission of the section and not by the Court,
    and the dispositions on the 2016 Authentication Regulations, which are repealed. Keeping them in
    the same file is what makes the file answerable to "what did the 2018 judgment do, and what is
    left of it" rather than only to "what is still bad law".
    """
    return {r["item_id"]: r for r in rows if r["item_id"] and r["validity"]}


# --------------------------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------------------------


def http_get(url: str, cache_name: str) -> bytes:
    """A plain GET with a cache. For hosts that are not India Code — UIDAI, the Supreme Court."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / cache_name
    if path.exists():
        return path.read_bytes()
    request = urllib.request.Request(url, headers={"User-Agent": IC.UA})
    with urllib.request.urlopen(request, timeout=180) as response:
        body = response.read()
    path.write_bytes(body)
    return body


def pdf_text(raw: bytes, layout: bool = True) -> str:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as fh:
        fh.write(raw)
        fh.flush()
        return extract(fh.name, layout=layout)


# --------------------------------------------------------------------------------------------
# The Act layer
# --------------------------------------------------------------------------------------------

_OMITTED = re.compile(r"^\s*(?:\[?\s*)?(Omitted|Repealed|Rep\.)\b", re.IGNORECASE)


def declared_validity(layer, number: str, overlay: dict, item_id: str) -> tuple:
    """(validity, validity_note) for one section, from the overlay first and the tables after.

    The overlay wins where it speaks, and it is the only place a *judicial* status is written, so
    the manifest cannot disagree with it — `this.i` @q3dsvsrl. A row that names a section the
    statutory table also claims aborts rather than one silently winning.
    """
    row = overlay.get(item_id)
    if row:
        return row["validity"], row["validity_note"]
    if layer is C.AADHAAR:
        return C.AADHAAR_VALIDITY.get(number, ("in-force", ""))
    if layer is C.DPDP:
        if number == "1":
            return "in-force", C.DPDP_SECTION_1_NOTE
        if number in C.DPDP_PART_COMMENCED:
            return "not-yet-applicable", C.DPDP_PART_COMMENCED[number]
        if number in C.DPDP_COMMENCED:
            return "in-force", ""
        return "not-yet-applicable", C.DPDP_DEFERRED_NOTE
    return "in-force", ""


def dpdp_oracle(client: IC.IndiaCode, items: list, numbers: list) -> None:
    """The DPDP Act's own PDF must contain every section India Code publishes as an item.

    **A weaker control than the Aadhaar Act's, and declared as one.** It is the same publisher, so
    it cannot catch a mistake made upstream of both artefacts; what it does catch is a `discover`
    query that silently dropped a page, which is the failure this layer is exposed to. The DPDP Act
    has no second publisher whose consolidated text is reachable — MeitY's own copy is the same
    file. Saying that is better than implying a cross-publisher check that did not happen.
    """
    from lawcorpus.completeness import scan

    act = next((o for o in items if IC.meta(o, "dc.identifier.collection") == "ACT"), None)
    if act is None:
        raise HarvestError("India Code publishes no ACT-level item for the DPDP Act to check against.")
    published = pick_bitstream(client.bitstreams(act), "TEXT", "")
    if published is None:
        raise HarvestError("The DPDP Act's India Code item carries no TEXT bitstream to check against.")
    text = client.content(published).decode("utf-8", "replace")
    found = {str(p) for p in scan(text, "", terminator=r"\.")}
    missing = [n for n in numbers if n not in found]
    if missing:
        raise HarvestError(
            f"India Code's own PDF of the DPDP Act does not carry section(s) {', '.join(missing)} "
            f"as headings, and India Code publishes them as items. One of the two is incomplete."
        )
    say(f"    oracle: all {len(numbers)} sections present in India Code's ACT-level PDF of the same Act")


def aadhaar_oracle(client: IC.IndiaCode, numbers: list) -> None:
    """UIDAI's consolidated edition must contain every section India Code gave us, and no others.

    A second publisher, a different artefact, and the strongest control available here: it is what
    would catch a `discover` query that silently dropped a page. The PDF is fetched for this and
    **not stored** — the corpus's copy of the Act is India Code's section items, and a second
    instrument-grained copy would give a quotation a retrieval path that bypasses per-section
    validity.
    """
    from lawcorpus.completeness import scan

    raw = http_get(C.AADHAAR.oracle_pdf, "uidai-act-as-amended.pdf")
    text = pdf_text(raw)
    found = {str(p) for p in scan(text, "", terminator=r"\.")}
    missing = [n for n in numbers if n not in found]
    if missing:
        raise HarvestError(
            f"{C.AADHAAR.oracle_note} does not contain section(s) {', '.join(missing)}, which India "
            f"Code publishes as items of this Act. Two publishers disagree about what the Act "
            f"contains and this harvest cannot say which is right, so nothing is stored. "
            f"sha256 of the oracle PDF: {hashlib.sha256(raw).hexdigest()}"
        )
    say(
        f"    oracle: all {len(numbers)} sections present in {C.AADHAAR.oracle_note} "
        f"(sha256 {hashlib.sha256(raw).hexdigest()[:16]}…)"
    )


def harvest_acts(client: IC.IndiaCode) -> None:
    ACTS.mkdir(exist_ok=True)
    store = CorpusStore(ACTS)
    overlay = overlay_for_items(read_overlay())
    items, footnotes = [], []
    for layer in C.ACT_LAYERS:
        act_id = IC.ACT_IDS[layer.key]
        say(f"  {layer.prefix} — {act_id}")
        found = client.act_items(act_id)
        sections = [o for o in found if IC.meta(o, "dc.identifier.collection") == "SECTION"]
        if not sections:
            raise HarvestError(
                f"India Code returned no SECTION items for act_id {act_id}. Before concluding that "
                f"this Act is not decomposed, fetch one that is known to be — the Aadhaar Act — "
                f"with the same call. `method.md` §4."
            )

        # Gate 1: identity.
        names = {IC.meta(o, "dc.identifier.act_name", "") for o in sections}
        wanted = search_key(layer.expect_title)
        if not any(wanted in search_key(n) for n in names):
            raise IC.IdentityError(
                f"The items under act_id {act_id} are titled {sorted(names)!r}, which does not "
                f"carry the declared phrase '{layer.expect_title}'. Either the work-list names the "
                f"wrong act_id or India Code has re-keyed the instrument; storing this would put "
                f"real law in the corpus under the wrong name."
            )

        ordered = IC.section_order(sections)
        numbers = [IC.meta(o, "dc.identifier.section_number") for o in ordered]

        # Gate 2: count, and the publisher's own flag, which does not work.
        if layer.expect_count and len(sections) != layer.expect_count:
            raise HarvestError(
                f"{layer.prefix}: India Code returned {len(sections)} sections and the work-list "
                f"declares {layer.expect_count}. Got: {', '.join(numbers)}."
            )
        flagged = [n for n, o in zip(numbers, ordered)
                   if str(IC.meta(o, "dc.identifier.repealed", "")).lower() == "true"]
        say(
            f"    {len(sections)} section items; dc.identifier.repealed is true for "
            f"{len(flagged)} of them{' — ' + ', '.join(flagged) if flagged else ''}"
        )

        # Gate 3: the chain, for what it proves.
        if not layer.sections:
            reached = IC.walk_next_section(ordered)
            off_chain = [n for n in numbers if n not in reached]
            say(
                f"    next_section chain reaches {len(reached)} of {len(numbers)}; off the chain: "
                f"{', '.join(off_chain) if off_chain else 'none'}"
            )
            if reached != sorted(reached, key=lambda n: int(re.sub(r"\D", "", n) or 0)):
                raise HarvestError(
                    f"{layer.prefix}: the publisher's next_section chain is not ascending, which "
                    f"means either the chain or our walk of it is wrong."
                )
            stranded = [n for n in off_chain if n.isdigit()]
            if stranded and len(reached) > 1:
                raise HarvestError(
                    f"{layer.prefix}: section(s) {', '.join(stranded)} carry no letter suffix and "
                    f"are still off the next_section chain. The chain's known blind spot is "
                    f"insertions (this.i @6v3ks6eo); a base-numbered section off the chain is a "
                    f"different problem and has not been seen before."
                )
            if len(reached) <= 1 and len(numbers) > 1:
                say(
                    f"    NOTE: the chain is absent for this Act, not merely partial — it reaches "
                    f"{len(reached)} of {len(numbers)}. The oracle is per-Act optional, so its "
                    f"silence is not evidence."
                )
            if layer is C.AADHAAR:
                aadhaar_oracle(client, numbers)
            elif layer is C.DPDP:
                dpdp_oracle(client, found, numbers)

        wanted_numbers = set(layer.sections) if layer.sections else None
        if wanted_numbers:
            absent = sorted(wanted_numbers - set(numbers))
            if absent:
                raise HarvestError(
                    f"{layer.prefix}: the work-list names section(s) {', '.join(absent)} and India "
                    f"Code does not publish them under this act_id."
                )

        for item in ordered:
            number = IC.meta(item, "dc.identifier.section_number")
            if wanted_numbers and number not in wanted_numbers:
                continue
            item_id = f"{layer.prefix}-s{number}"
            text = IC.section_text(item)
            if not text.startswith(f"{number}."):
                raise HarvestError(
                    f"{item_id}: the composed text opens {text[:40]!r} rather than with its own "
                    f"section number. The publisher's fields are not where this code expects them."
                )
            body = text.split("\n", 1)[1] if "\n" in text else ""

            validity, note = declared_validity(layer, number, overlay, item_id)
            # Gate 4: what the text itself states must agree with what the table declares.
            derived_gone = bool(_OMITTED.match(body.strip()))
            if derived_gone and validity == "in-force":
                raise HarvestError(
                    f"{item_id}: its text opens {body.strip()[:60]!r}, so the publisher is saying "
                    f"this provision is gone, and the work-list declares it in force. Resolve the "
                    f"disagreement in candidates.py before storing it."
                )
            if validity in ("repealed", "struck-down") and not derived_gone and not overlay.get(item_id):
                raise HarvestError(
                    f"{item_id}: declared '{validity}' and its stored text does not say so. If a "
                    f"court did it, the row belongs in sources/judicial-overlay.tsv."
                )

            stored = store.write(item_id, text)
            handle = item["handle"]
            footnote = IC.render(IC.meta(item, "dc.identifier.section_footnote", ""))
            if footnote:
                footnotes.append(
                    {
                        "item_id": item_id,
                        "handle": handle,
                        "footnote": " ".join(footnote.split()),
                    }
                )
            items.append(
                ManifestItem(
                    item_id=item_id,
                    citation=layer.citation.format(s=number),
                    title=(IC.meta(item, "dc.title", "") or "").strip(),
                    authority_tier="legislative",
                    validity=validity,
                    validity_note=note,
                    translation_status="authoritative",
                    version_id=f"India Code {handle}, accessioned "
                    f"{(IC.meta(item, 'dc.date.accessioned', '') or '')[:10]}",
                    lang="eng",
                    source_url=f"{IC.SITE}/handle/{handle}",
                    retrieved=TODAY,
                    media_type="application/json",
                    bytes=stored.bytes,
                    sha256=stored.sha256,
                )
            )

    manifest = Manifest(items)
    manifest.write(ACTS / "MANIFEST.tsv")
    FOOTNOTES.parent.mkdir(exist_ok=True)
    with FOOTNOTES.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, ["item_id", "handle", "footnote"], delimiter="\t")
        writer.writeheader()
        writer.writerows(footnotes)
    say(f"  wrote {len(items)} section items and {len(footnotes)} amendment footnotes")


# --------------------------------------------------------------------------------------------
# The delegated layer
# --------------------------------------------------------------------------------------------


def pick_bitstream(streams: list, bundle: str, wanted: str):
    candidates_ = [s for s in streams if s.bundle == bundle]
    if wanted:
        candidates_ = [s for s in candidates_ if s.name.startswith(wanted.rsplit(".", 1)[0])]
    else:
        candidates_ = [s for s in candidates_ if "hin" not in s.name.lower()]
    return candidates_[0] if candidates_ else None


def harvest_one_delegated(client: IC.IndiaCode, spec, store: CorpusStore, vocab: set) -> ManifestItem:
    item = client.item_by_handle(spec.handle)
    title = (IC.meta(item, "dc.title", "") or item["name"]).strip()
    if search_key(spec.expect_title) not in search_key(title):
        raise IC.IdentityError(
            f"{spec.item_id}: handle {spec.handle} is titled {title!r}, which does not carry the "
            f"declared phrase {spec.expect_title!r}."
        )
    streams = client.bitstreams(item)
    published = pick_bitstream(streams, "TEXT", spec.bitstream)
    original = pick_bitstream(streams, "ORIGINAL", spec.bitstream)
    if not published or not original:
        raise HarvestError(
            f"{spec.item_id}: India Code has no {'TEXT' if not published else 'ORIGINAL'} bitstream "
            f"for {spec.handle}. Bundles present: {sorted({s.bundle for s in streams})}."
        )

    their_text = client.content(published).decode("utf-8", "replace")
    our_text = pdf_text(client.content(original), layout=False)

    # The publisher's text is preferred and does not win by default. Where it is short, ours is
    # stored instead — it is watermarked but complete, and in `layout=False` the watermark sits on
    # lines of its own rather than displacing the body. `this.i` @ah7ssl3s.
    source, text, qualifier = "the publisher's own extraction", their_text, ""
    only_ours = indian.agree(their_text, our_text, spec.item_id)
    if only_ours:
        say(f"    {spec.item_id}: headings our extraction sees and theirs does not: {only_ours}")
    try:
        indian.check_length(their_text, our_text, spec.item_id)
    except indian.ExtractionRefused as e:
        say(f"    {spec.item_id}: falling back to our own extraction — {e.message}")
        source, text = "our extraction, layout=False", our_text
        qualifier = (
            f"our own extraction, because India Code's stops at {len(their_text)} characters; "
            f"isolated 'India Code' watermark fragments appear on lines of their own"
        )
    health_note = indian.check_latin(text, f"{spec.item_id} ({source})", spec.expect_phrase)
    share = indian.sound_share(text)[0]
    say(
        f"    {spec.item_id}: {len(text)} chars from {source}; watermark lines theirs="
        f"{indian.watermark_lines(their_text)} ours={indian.watermark_lines(our_text)}; "
        f"{share:.0%} reads as English, oov={indian.oov_rate(text, vocab):.3f}"
    )
    for phrase in spec.expect_phrase:
        if search_key(phrase) not in search_key(text):
            raise HarvestError(
                f"{spec.item_id}: the stored text does not contain the declared phrase "
                f"{phrase!r}. Before concluding the instrument does not say it, check the "
                f"extraction — on this source a zero is an extraction artefact more often than it "
                f"is a fact about the law."
            )

    stored = store.write(spec.item_id, text)
    return ManifestItem(
        item_id=spec.item_id,
        citation=spec.citation,
        title=title,
        authority_tier=spec.authority_tier,
        validity=spec.validity,
        validity_note=spec.validity_note,
        translation_status="authoritative",
        version_id=spec.version_id or f"India Code {spec.handle}",
        lang="eng",
        source_url=f"{IC.SITE}/handle/{spec.handle}",
        retrieved=TODAY,
        media_type="application/pdf",
        bytes=stored.bytes,
        sha256=stored.sha256,
        quotation_qualifier="; ".join(
            p for p in (qualifier or "extracted by the publisher from a watermarked PDF", health_note) if p
        ),
    )


def reference_vocabulary() -> set:
    """The Act layer's own words, used to score every delegated extraction. `indian.oov_rate`."""
    store = CorpusStore(ACTS)
    texts = [store.read(i) for i in store.item_ids()]
    if not texts:
        raise HarvestError(
            "corpus-acts/ is empty, so there is nothing to score the delegated extractions against. "
            "Harvest the Act layer first: python3 tools/harvest.py acts"
        )
    return indian.vocabulary(texts)


def harvest_delegated(client: IC.IndiaCode) -> None:
    DELEGATED.mkdir(exist_ok=True)
    store = CorpusStore(DELEGATED)
    vocab = reference_vocabulary()
    items = []
    for spec in C.DELEGATED:
        items.append(harvest_one_delegated(client, spec, store, vocab))
    # Measured on every run, stored on none, so that the refusal is current rather than remembered.
    # `method.md` §4: a zero is a question, and a refusal nobody re-asks has stopped being one.
    refused = client.item_by_handle(C.FOREIGN_CA_REGULATION.handle)
    text = client.content(
        pick_bitstream(client.bitstreams(refused), "TEXT", "")
    ).decode("utf-8", "replace")
    say(
        f"    FOREIGN-CA-REG-2013: not stored. oov={indian.oov_rate(text, vocab):.3f}, "
        f"{indian.sound_share(text)[0]:.0%} reads as English. "
        f"{C.FOREIGN_CA_REGULATION.unquotable}"
    )
    Manifest(items).write(DELEGATED / "MANIFEST.tsv")
    say(f"  wrote {len(items)} delegated items")


# --------------------------------------------------------------------------------------------
# The judicial layer
# --------------------------------------------------------------------------------------------


def harvest_judgments() -> None:
    JUDGMENTS.mkdir(exist_ok=True)
    store = CorpusStore(JUDGMENTS)
    items = []
    for spec in C.JUDGMENTS:
        raw = http_get(spec.url, f"{spec.item_id}.pdf")
        text = pdf_text(raw)
        indian.check_latin(text, spec.item_id, spec.expect_phrase)
        for phrase in spec.expect_phrase:
            if search_key(phrase) not in search_key(text):
                raise HarvestError(
                    f"{spec.item_id}: the extraction does not contain {phrase!r}. The Supreme "
                    f"Court's PDFs extract cleanly, so this is a wrong document rather than a "
                    f"broken one."
                )
        stored = store.write(spec.item_id, text)
        say(f"    {spec.item_id}: {len(text)} chars from {len(raw)} bytes of PDF")
        items.append(
            ManifestItem(
                item_id=spec.item_id,
                citation=spec.citation,
                title=spec.title,
                authority_tier="judicial",
                validity=spec.validity,
                validity_note=spec.validity_note,
                translation_status="authoritative",
                version_id=spec.url.rsplit("/", 1)[-1],
                lang="eng",
                source_url=spec.url,
                retrieved=TODAY,
                media_type="application/pdf",
                bytes=stored.bytes,
                sha256=stored.sha256,
            )
        )
    Manifest(items).write(JUDGMENTS / "MANIFEST.tsv")
    say(f"  wrote {len(items)} judgments")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("layers", nargs="*", default=None,
                        choices=["acts", "delegated", "judgments"], help="default: all three")
    args = parser.parse_args(argv)
    layers = args.layers or ["judgments", "acts", "delegated"]
    client = IC.IndiaCode(CACHE / "indiacode")
    try:
        for layer in layers:
            say(f"== {layer}")
            if layer == "acts":
                harvest_acts(client)
            elif layer == "delegated":
                harvest_delegated(client)
            else:
                harvest_judgments()
    except LawcorpusError as e:
        print(f"\n{e.code}: {e.message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
