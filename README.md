# aadhaar — India's identity and data-protection regime

> **Status: harvested 2026-09-16.** 134 corpus items across three layers, five findings, and a
> four-row judicial overlay. Every claim in `findings/` is a verbatim quotation retrievable from
> `corpus-*/` and checked by `tools/check-quotes.py`. This repo is **private** and nothing in it is
> legal advice.

Part of a family of repos that harvest primary legal sources so they can be analysed later — by a
person or by an AI — without repeating the online research, and without trusting anyone's memory of
what the law says. Shared method and tooling:
**[`id-law-kit`](https://github.com/bakobo/id-law-kit)**.

| Repo | Regime | Corpus |
|---|---|---|
| [`utah-id-law`](https://github.com/bakobo/utah-id-law) | Utah identity-verification law | ✅ |
| [`eu-data-law`](https://github.com/bakobo/eu-data-law) | GDPR + EU data-locality stack | ✅ |
| [`eidas-eudi`](https://github.com/bakobo/eidas-eudi) | eIDAS 2, EUDI wallet, ARF | ✅ |
| [`ccpa`](https://github.com/bakobo/ccpa) | California CCPA/CPRA | ✅ |
| **`aadhaar`** | Aadhaar Act, UIDAI regulations, DPDP Act, the judgments | ✅ this repo |

## Why this one is different

The other four repos can answer most questions from statutory and regulatory text. This one cannot.

Section 57 of the Aadhaar Act 2016 was held partly unconstitutional by the Supreme Court in 2018 and
then omitted outright by Parliament in 2019. An agent applying this programme's central rule —
*quote-or-drop*, admit a claim only with a verbatim quotation retrievable from the corpus — over the
wrong edition of the Act produces a confidently false statement of Indian law, **by obeying the
rule**. That single case is why `id-law-kit`'s manifest carries a required `validity` field with no
default and why `lawcite` prints a validity banner above every quote. Those defences were built for
this repo before this repo had a corpus.

**The trap turns out not to be where the July plan expected it.** UIDAI's consolidated PDF is
correct: its §57 reads `[Omitted.]`, and quote-or-drop over that document cannot manufacture the
claim. The danger is `Aadhaar_Act_2016_English.pdf`, the annotated edition UIDAI's rebuilt legal page
now links, whose body marks §57 repealed and whose **footnote then reproduces the omitted text in
full, inside quotation marks, four lines below a heading bearing the same number.** That survives
quote-or-drop intact and is invisible to item-level validity, because the item is honestly marked.
It is an Indian drafting convention rather than a stale file, so it recurs across the class — the
same PDF does it for §2(a), §33(1) and §33(2).

**India Code's section items are structurally immune**, because the publisher puts current text and
amendment history in separate fields. That is the strongest argument for how this corpus is built.

## What is in here

| Layer | Grain | Items | Source |
|---|---|---|---|
| `corpus-acts/` | **one item per section** | 121 | India Code's `SECTION` items |
| `corpus-delegated/` | one item per instrument | 10 | India Code PDFs and the publisher's text of them |
| `corpus-judgments/` | one item per judgment | 3 | `api.sci.gov.in` and the official Supreme Court Reports |

The Act layer is the Aadhaar Act 2016 (69 sections), the DPDP Act 2023 (44), and the provisions of
the Copyright Act 1957, the IT Act 2000 and the Official Languages Act 1963 that the findings rest
on. The delegated layer is the 2021 Authentication and Offline Verification Regulations as amended
to 9 December 2025, the SWIK Rules, three 2016 regulation sets, the DPDP Rules 2025, three
commencement notifications, and the Constitution. The judgments are *K.S. Puttaswamy* 2017 and 2018,
the latter in both the raw and the official-report versions.

**The two grains are a real difference, not a compromise.** India Code publishes each section of each
Act as its own item, with the current as-amended text in one field and the amendment provenance in
another; it publishes delegated legislation as a PDF with no text field at all. So validity is per
section on the Act layer and per instrument below it, and every finding says which it is quoting.
The cost of instrument grain is live here and is written down in `sources/registry.md` §3.

## How to use it

```bash
python3 -m venv .venv && .venv/bin/pip install -e ../id-law-kit
.venv/bin/lawcite --corpus corpus-acts 'AADHAAR-2016-s57'          # quote one provision
.venv/bin/lawcite --corpus corpus-acts --grep 'offline verification'
.venv/bin/lawcite --corpus corpus-delegated --grep 'Verifiable Credential'
.venv/bin/python tools/verify.py                                    # the repo holds together
.venv/bin/python tools/check-quotes.py                              # every finding quote is real
.venv/bin/python tools/harvest.py                                   # refetch everything
```

`lawcite` prints a validity banner above every quotation. Read it. `AADHAAR-2016-s57` prints
`[REPEALED: this text is NOT current law …]`; `DPDP-2023-s16`, the cross-border transfer provision,
prints `[NOT YET APPLICABLE …]` and will until 13 May 2027.

## The findings

- **[The trust anchor is publicly obtainable](findings/the-aadhaar-secure-qr-trust-anchor-is-publicly-obtainable.md)** — Q10, and the first yes in the programme. UIDAI's Secure QR signing certificate validates to `CN=CCA India 2022` from Oregon, because Reg. 2(ib) defines the signature by reference to IT Act s. 2(1)(p) and so puts the credential inside India's general PKI. The heuristic: *ask which PKI a signature lives in before asking whether its anchor is published.*
- **[Who may verify is administrative discretion](findings/who-may-verify-an-aadhaar-credential-is-decided-by-administrative-discretion.md)** — Q11 and Q12. Online authentication needs an Act of Parliament or a ministry's sponsorship; offline verification needs registration on terms UIDAI does not publish, and the schedule that once set criteria for verifiers was deleted from the regulation in February 2023.
- **[The stack is eight layers and one is offline-verifiable](findings/the-aadhaar-stack-is-eight-layers-and-one-of-them-is-offline-verifiable.md)** — Q9 and Q14, including the "Aadhaar Verifiable Credential" that became a defined term in Indian delegated legislation on 9 December 2025, shareable "in full or part".
- **[Statutes are copyright works and s. 52(1)(q) splits three ways](findings/indian-statutes-are-copyright-works-and-section-52-splits-three-ways.md)** — the redistribution basis.
- **[India is a language control](findings/india-is-a-language-control-and-uidais-hindi-exists-only-in-the-browser.md)** — Article 348(1)(b), and why UIDAI's machine-translated Hindi could not be stored at all.

## Design decisions

See [`this.i`](this.i). The July decisions survive with their reasoning intact and two of their
premises corrected: case law is a **mandatory corpus layer** (@meihbh), judgments are
**hand-curated** (@hyjd5n), and validity is recorded **per provision** (@4sxgog) — which since
2026-09-16 means *the provision is the item*, because India Code publishes it that way, with the
overlay shrunk to the judicial residue. Then: the overlay is the **source** the manifests are
generated from (@q3dsvsrl), amendment footnotes are provenance and never corpus (@gogceltr), the
delegated layer's text is the publisher's own with ours as the control (@yt6p5u4j) except where the
publisher's stops early (@ah7ssl3s), the `next_section` chain is a shape oracle with a known blind
spot (@6v3ks6eo), soundness is measured in windows and a person reads where that runs out
(@nppnqlxn), and redistribution rests on Copyright Act §52(1)(q) split by layer (@5lrzngtg).

## Redistribution — read this before publishing anything from here

**Indian statutes are copyright works of the Government until the end of 2076.** There is no Indian
analogue of the US "edicts of government" doctrine, and GODL-India — named in this README's first
version — governs NDSAP datasets and not legislation. The basis is **Copyright Act, 1957, s.
52(1)(q)**, and it does three different things:

- **judgments**, under (q)(iv): free to reproduce, absent a prohibition by the court. Neither
  Puttaswamy judgment carries one.
- **rules, regulations and notifications**, under (q)(i): free to reproduce as Gazette matter.
- **Acts**, under (q)(ii): free **only** "together with any commentary thereon or any other original
  matter".

That last condition is on the act of publication rather than on the text, so the same 121 section
files are freely reproducible in one arrangement and arguably not in another. A repository that is
only a corpus does not obviously satisfy it; this repository, whose `findings/` analyse the
provisions they quote, does. **The repo is private, so nothing turns on it today.** A decision to
publish has a real question to answer, and it should be answered deliberately rather than by
optimism. The full reasoning is in the finding linked above, and it is the kind of inference that
wants a lawyer's eye first.

## Known gaps, as of 2026-09-16

- **Three of the five load-bearing judgments are absent** — Binoy Viswam (2017), Beghar Foundation
  (2021), Rojer Mathew (2019). Each needs a diary number looked up by hand on a captcha-gated search
  surface. Consequently **no finding here asserts that the 2018 holding is final**, which is exactly
  the claim their absence would otherwise have licensed.
- **The 2013 foreign-CA Regulation is refused, not stored.** Its India Code copy's English is
  corrupt at the character level and the automatic guards passed it; it is excluded by hand. It is
  the only statutory route by which a foreign issuer is recognised in India, so obtaining a clean
  copy is the highest-value single addition to this corpus. `sources/registry.md` §7.
- **UIDAI's own document host does not answer this egress**, so the OVSE Handbook, the registered-OVSE
  list and most circulars are unread — and they are the documents most likely to carry the
  eligibility criteria Reg. 13A leaves unwritten.
- **No Secure QR specification could be retrieved**, so every claim about the Indian wire format
  remains third-party. The trust-anchor half does not depend on it.
- **The Hindi texts are out of scope**, because whether they are the Presidentially-authorised texts
  under s. 5(1) of the Official Languages Act is not evidenced by their sitting beside the English.
- The DPDP Rules 2025 are stored from our own extraction and carry isolated watermark fragments on
  lines of their own. The manifest row says so.

## Licence

The **original work** in this repo is **[CC BY 4.0](LICENSE)**. Attribution: Bakobo, *aadhaar*.

The corpus is **not** covered by that licence and is not ours to license; see Redistribution above.

**Not legal advice.** Textual research by non-lawyers, with substantial AI assistance.
