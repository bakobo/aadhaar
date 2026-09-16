#!/usr/bin/env python3
"""Verify that every quotation in `findings/` is retrievable from this repo's corpus.

`method.md` §1: a claim is admissible only with a citation *and* a verbatim quotation retrievable
from the corpus. That rule is worth having only if something enforces it, because the failure it
guards against — a fluent, confident, fabricated quotation — is invisible on reading. A reviewer
checking by eye is checking the thing they are least able to check.

So this takes every markdown blockquote line in `findings/`, strips the emphasis a finding adds for
the reader, splits on the ellipsis a finding uses to elide, and requires each remaining fragment to
appear in one of the three corpora. A fragment that does not is printed with its file and line, and
the run fails. Descended from `indonesia-id/tools/check-quotes.py`, with two Indian differences.

**The amendment bracket.** India Code marks a span some amending Act inserted or substituted with a
superscript marker and square brackets, which `indiacode.render` keeps as a bare digit: section 33
reads `an order of a court not inferior to that of a 1[Judge of a High Court]`. That is the text, and
a finding quoting the provision as a reader would write it must still match, so both sides are folded
through `unmark` — which deletes `1[` and `]` — before comparison. The marks are kept in the corpus
rather than stripped at harvest, because they are how every printed consolidated edition of an Indian
Act renders the same fact, and because deleting them would make an inserted clause indistinguishable
from original enacted text.

**No space-stripped retry.** Indonesia has one, because OCR there ate word boundaries and a correct
quotation of `Penyelenggara Sertifikasi Elektronik asing` could not match any other way. Nothing in
this corpus needs it: the Act layer is JSON metadata rather than OCR, and the one instrument whose
extraction eats spaces — the 2013 foreign-CA Regulation — is refused rather than stored, so a
fallback that reached it would be reaching into a document this repo has decided is unquotable.

    python3 tools/check-quotes.py
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lawcorpus.normalise import normalise_text  # noqa: E402
from lawcorpus.store import CorpusStore  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CORPORA = ("corpus-acts", "corpus-delegated", "corpus-judgments")
# Long enough that matching it proves something. An English elision leaves fragments like `of the`,
# which occur everywhere.
MIN_FRAGMENT = 14

_EMPHASIS = re.compile(r"\*\*|\*|`")
# `…` and `...` are how a finding elides. `[…]` is how it marks a correction it is making visible,
# and the corrected characters are not in the corpus, so a bracketed span is dropped rather than
# searched. The lookbehind is what keeps that from eating India Code's amendment brackets, which
# are always preceded by their marker digit: without it, a quotation of section 28 containing
# `1[sixty years]` was split at the bracket and the fragment ending `shall subsist until 1` matched
# nothing, because `unmark` had already removed that digit from the corpus side.
_ELISION = re.compile(r"…|\.\.\.|(?<!\d)\[[^\]]{0,80}\]")
# India Code's amendment marks: a superscript number rendered as a digit, immediately before the
# bracket that opens the amended span, and the bracket that closes it.
_MARK = re.compile(r"\d{1,2}\[|\]")


def unmark(text: str) -> str:
    return _MARK.sub("", text)


def key(text: str) -> str:
    """Fold a string the way the corpus was folded, collapse whitespace, drop amendment marks."""
    return " ".join(unmark(normalise_text(text)).split())


def fragments(quote: str):
    for part in _ELISION.split(_EMPHASIS.sub("", quote)):
        part = part.strip()
        if len(part) >= MIN_FRAGMENT:
            yield part


def corpus_texts() -> dict:
    texts = {}
    for name in CORPORA:
        store = CorpusStore(ROOT / name)
        for item_id in store.item_ids():
            texts[f"{name}/{item_id}"] = key(store.read(item_id))
    return texts


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("paths", nargs="*", help="finding files (default: findings/*.md)")
    args = parser.parse_args(argv)

    paths = [Path(p) for p in args.paths] or sorted((ROOT / "findings").glob("*.md"))
    texts = corpus_texts()
    if not texts:
        print("No corpus text found. Run tools/harvest.py first.", file=sys.stderr)
        return 2

    checked = missing = 0
    for path in paths:
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), start=1):
            if not line.startswith("> "):
                continue
            for fragment in fragments(line[2:]):
                checked += 1
                needle = key(fragment)
                if any(needle in folded for folded in texts.values()):
                    continue
                missing += 1
                print(f"{path}:{number}  NOT IN CORPUS: {fragment[:90]}")

    print(f"\n{checked} quoted fragment(s) checked across {len(paths)} finding(s); {missing} not found.")
    if missing:
        print(
            "A quotation that cannot be reproduced from the corpus is deleted, not softened "
            "(method.md §1). Before concluding the source does not say it, check the extraction: "
            "on India Code a zero is an extraction artefact at least as often as it is a fact "
            "about the law."
        )
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
