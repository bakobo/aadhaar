#!/usr/bin/env python3
"""Check that this repo holds together — after a harvest, and before believing any finding.

`tools/harvest.py` refuses before it writes. This refuses after, and it exists because the two are
different questions: the harvest asks whether each document is what it claims, and this asks whether
the three layers still agree with each other and with the files they were written from.

Five checks, and each of them has a failure it was written for:

1. **Every stored text still hashes to its manifest row.** A corpus whose files have drifted from
   their digests cannot support quote-or-drop at all.
2. **Every corpus file has a manifest row, and every row a file.** An item in one and not the other
   is a retrieval that half-succeeded.
3. **The judicial overlay is what the manifest says.** `this.i` @q3dsvsrl makes the overlay the
   source and the manifest the output; this is what makes that true rather than intended, because a
   hand-edited manifest row is otherwise indistinguishable from a generated one.
4. **Every quotation the overlay attributes to a judgment is retrievable from that judgment.** The
   overlay is where this repo says what a court did; quote-or-drop applies to it exactly as it
   applies to a finding.
5. **The DPDP commencement table is a faithful transcription.** `candidates.py` decides the validity
   of all 44 DPDP sections from three clauses of G.S.R. 843(E). Those clauses are quoted in the
   file's comments, and the notification is in the corpus, so the quotation is checkable.

    python3 tools/verify.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import candidates as C  # noqa: E402
import harvest as H  # noqa: E402
from lawcorpus.manifest import Manifest  # noqa: E402
from lawcorpus.normalise import search_key  # noqa: E402
from lawcorpus.store import CorpusStore  # noqa: E402

CORPORA = (H.ACTS, H.DELEGATED, H.JUDGMENTS)

# The three clauses of G.S.R. 843(E) that `candidates.py` reads the DPDP commencement table off,
# verbatim from the notification. Transcribed once, checked on every run.
COMMENCEMENT_CLAUSES = (
    # Clause (a) is checked in two pieces because the Gazette breaks "sub-sections" across a line
    # with a hyphen, and `search_key` folds line wrapping but does not rejoin a hyphenated word.
    "sub-section (2) of section 1, section 2, sections 18 to 26 sections 35, 38, 39, 40, 41, 42, 43",
    "sections (1) and (3) of section 44 of the said Act shall come into force",
    "one year from the date of publication of this gazette on which the provisions of sub-section "
    "(9) of section 6 and clause (d) of sub-section (1) of section 27",
    "eighteen months from the date of publication of this gazette",
)


def check_digests(problems: list) -> None:
    for root in CORPORA:
        manifest = Manifest.read(root / "MANIFEST.tsv")
        store = CorpusStore(root)
        stored = set(store.item_ids())
        listed = {item.item_id for item in manifest}
        for missing in sorted(listed - stored):
            problems.append(f"{root.name}: {missing} is in the manifest and not on disk")
        for orphan in sorted(stored - listed):
            problems.append(f"{root.name}: {orphan} is on disk and not in the manifest")
        for item in manifest:
            if item.item_id in stored and not store.verify(item.item_id, item.sha256):
                problems.append(
                    f"{root.name}: {item.item_id} no longer hashes to its manifest digest"
                )
        print(f"  {root.name}: {len(listed)} items, digests checked")


def check_overlay(problems: list) -> None:
    rows = H.read_overlay()
    acts = Manifest.read(H.ACTS / "MANIFEST.tsv")
    judgments = CorpusStore(H.JUDGMENTS)
    live = [r for r in rows if r["disposition"] == "live"]
    for row in rows:
        if row["item_id"] and row["validity"]:
            item = acts[row["item_id"]]
            if item.validity.value != row["validity"]:
                problems.append(
                    f"overlay: {row['item_id']} is '{row['validity']}' in the overlay and "
                    f"'{item.validity.value}' in the manifest. The overlay is the source "
                    f"(this.i @q3dsvsrl) — re-run the harvest rather than editing the manifest."
                )
            if item.validity_note != row["validity_note"]:
                problems.append(f"overlay: {row['item_id']}'s validity_note has drifted")
        quote = row["judgment_quote"]
        if not quote:
            continue
        text = search_key(judgments.read(row["judgment"]))
        for fragment in (f.strip() for f in quote.split("…")):
            if len(fragment) >= 20 and search_key(fragment) not in text:
                problems.append(
                    f"overlay: the quotation attributed to {row['judgment']} for "
                    f"{row['instrument']} {row['provision']} is not retrievable from it: "
                    f"{fragment[:70]!r}"
                )
    print(f"  overlay: {len(rows)} rows, {len(live)} live, quotations checked against the judgments")


def check_commencement(problems: list) -> None:
    text = search_key(CorpusStore(H.DELEGATED).read("DPDP-COMMENCEMENT-2025"))
    for clause in COMMENCEMENT_CLAUSES:
        if search_key(clause) not in text:
            problems.append(
                f"commencement: G.S.R. 843(E) as stored does not contain the clause "
                f"candidates.py reads the DPDP validity table off: {clause[:70]!r}"
            )
    manifest = Manifest.read(H.ACTS / "MANIFEST.tsv")
    in_force = sorted(
        item.item_id.rsplit("-s", 1)[1]
        for item in manifest
        if item.item_id.startswith("DPDP-2023-") and item.validity.value == "in-force"
    )
    expected = sorted(set(C.DPDP_COMMENCED) | {"1"})
    if in_force != expected:
        problems.append(
            f"commencement: the manifest marks DPDP sections {in_force} in force and the "
            f"notification appoints {expected}"
        )
    print(f"  commencement: G.S.R. 843(E) quoted faithfully; {len(in_force)} of 44 DPDP sections in force")


def main() -> int:
    problems: list = []
    check_digests(problems)
    check_overlay(problems)
    check_commencement(problems)
    if problems:
        print("\n" + "\n".join(f"  FAIL {p}" for p in problems))
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
