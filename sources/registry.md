# Source registry — India's Aadhaar and data-protection law

Live URL ⇄ local copy ⇄ retrieval date. **Trust order is the `authority_tier` column** in the three manifests — [`../corpus-acts/MANIFEST.tsv`](../corpus-acts/MANIFEST.tsv), [`../corpus-delegated/MANIFEST.tsv`](../corpus-delegated/MANIFEST.tsv), [`../corpus-judgments/MANIFEST.tsv`](../corpus-judgments/MANIFEST.tsv) — which are the authoritative record. This file is the readable index and the place for the things a manifest has no column for.

Everything was retrieved **2026-09-16**. Per-item SHA-256, byte counts and retrieval dates are in the manifests.

## 1. The three sources

| Source | What it gave | How |
|---|---|---|
| `indiacode.gov.in` | every Act, at section granularity; every delegated instrument, as a PDF and the publisher's own text of it | DSpace 7 REST API, unauthenticated, `discover/search/objects` keyed on `act_id` |
| `api.sci.gov.in` | the Puttaswamy judgments | a deterministic PDF path, unauthenticated |
| `cdnbbsr.s3waas.gov.in` | the official Supreme Court Reports text of the 2018 judgment | direct PDF |
| `uidai.gov.in` | **no corpus text.** Its consolidated Act PDF is used as an oracle (§4) and its site is evidence in two findings | plain GET |

**India Code moved hosts between July and September 2026** — `indiacode.nic.in` now serves a migration stub and 404s everything under it, and the July reconnaissance in this repo recorded those 404s as a fact about India. They were a fact about a hostname. The lesson is in `tools/indiacode.py`'s docstring and in `method.md` §4's terms: *a 404 that reproduces is a question too*, and fetching the host root is the cheapest positive control there is.

## 2. Redistribution basis, in the source's own words

**Copyright Act, 1957, s. 52(1)(q)**, split three ways by layer, with the Act layer's exemption conditional on publishing commentary alongside. The full reasoning, with the text quoted from `corpus-acts/COPYRIGHT-1957-s52`, is [`../findings/indian-statutes-are-copyright-works-and-section-52-splits-three-ways.md`](../findings/indian-statutes-are-copyright-works-and-section-52-splits-three-ways.md).

**GODL-India is not the basis** and has been dropped from the README. It is a licence a data publisher offers over NDSAP datasets; statutes are not datasets, and India Code marks nothing GODL.

## 3. Two grains, declared

The Act layer is **one corpus item per section**, because India Code publishes it that way (`this.i` @4sxgog). The delegated layer is **one item per instrument**, because India Code gives those items no text field at all — only a PDF. Every finding says which grain it is quoting.

**The cost of instrument grain is live in this corpus and is not hypothetical.** The 2021 Regulations carry their superseded wordings in footnotes: "Regulation 12(1), before substitution, stood as under:" and then the old text in quotation marks. The item is honestly `in-force`, the banner says so, and the superseded words are inside it where item-level validity cannot see them. On the Act layer that hazard is structurally absent, because the publisher puts current text and amendment history in different fields and this repo stores only the first (`this.i` @gogceltr).

## 4. Sources used as oracles rather than corpus

**UIDAI's consolidated edition, `Aadhaar_Act_2016_as_amended.pdf`**, SHA-256 `75b5627b0c47ca88…`, retrieved 2026-09-16 from `https://uidai.gov.in/images/Aadhaar_Act_2016_as_amended.pdf`. All 69 sections India Code publishes as items are present in it as headings; a mismatch aborts the harvest. It is **not stored as corpus text**, deliberately: a second, instrument-grained copy of the Aadhaar Act would give a quotation a retrieval path that bypasses per-section validity.

**India Code's own ACT-level PDF of the DPDP Act** plays the same role for that Act's 44 sections. It is the same publisher as the section items, so it is a weaker control and is declared as one in `candidates.py`.

**`dc.identifier.next_section`** is India Code's own linked list of sections, and a fourth free shape oracle beside Japan's `<TOC><ArticleRange>`, Korea's gapless numbering and Indonesia's `status_hukum`. It walks 59 of the Aadhaar Act's 69 sections **cleanly**, and it is never a warning: every one of the ten lettered insertions — 3A, 8A, 23A, 33A–33F, 50A — has a null pointer and is never pointed at, and §3 points straight at §4. For the DPDP Act the chain does not exist at all: it reaches 1 of 44. So it is used for what it proves, paired with `order_number` and a declared count, and the harvest prints both numbers (`this.i` @6v3ks6eo).

## 5. The publisher field that is wired to nothing

**`dc.identifier.repealed` is `false` for all 69 sections of the Aadhaar Act, including the omitted §57.** It is not connected to `validity` and it never will be. This is recorded here because the field is the obvious thing to reach for, it is right there in the metadata, and a harvester that trusted it would mark the one provision this repo exists for as in force.

What *is* derived from the publisher is the text: exactly one of 69 section bodies opens with an amendment note, and the harvest checks that against the declared table — a disagreement aborts.

## 6. The judicial overlay

[`judicial-overlay.tsv`](judicial-overlay.tsv) is the single authored record of what the Supreme Court did to provisions in this corpus, and the manifests are **generated from it** (`this.i` @q3dsvsrl). `tools/verify.py` re-checks the derivation and checks every quotation in it back against the judgment it is attributed to, so a hand-edited manifest row fails rather than wins.

Eight rows, four of them live:

| Live | Instrument and provision | Status |
|---|---|---|
| ✅ | Aadhaar Act s. 2(d) | `read-down` — an authentication record excludes metadata |
| ✅ | Aadhaar Act s. 7 | `read-down` — "benefit" read *ejusdem generis* with "subsidies" |
| ✅ | PMLA (Maintenance of Records) Rules 2005, r. 9(a)(17) | `struck-down`; **not in this corpus** |
| ✅ | DoT circular of 23 March 2017 | `struck-down`; **not in this corpus** |
| — | Aadhaar Act s. 33(1) and (2) | spent: the read-down is now statutory, the struck sub-section was re-enacted in amended form and has never been tested |
| — | Aadhaar Act s. 47 | spent: the Court recommended an amendment and Parliament made it |
| — | Aadhaar Act s. 57 | spent: Parliament omitted the whole section |
| — | Aadhaar (Authentication) Regulations 2016, regs. 26 and 27(1) | spent: those Regulations are repealed |

**Why the overlay is four rows and not four hundred.** The 2019 Amendment Act legislated most of the 2018 judgment. That is the substantive finding behind the sizing, and it is why the July plan's provision-level overlay was not the right shape: what survives is a short file about court decisions rather than a shadow copy of the statute book.

The two rows with no `item_id` are the reason the overlay could not simply be folded into the manifests. They are about instruments this corpus does not hold, and a manifest has no row for a document it does not have.

## 7. What was refused, and why

**The Information Technology (Recognition of Foreign Certifying Authorities operating under a Regulatory Authority) Regulation, 2013** — handle `123456789/507084`, fetched on every run and stored on none.

It matters: it is the implementing instrument for IT Act s. 19, the only statutory route by which a foreign certifying authority is recognised in India, and therefore the one document that would settle whether a foreign issuer may issue to Indian residents. Its India Code copy is a bilingual Gazette scan whose **English** is corrupt at the character level. Its out-of-vocabulary rate against this corpus's own words is 0.62 where every sound instrument runs 0.15–0.40, and a reader finds `Recognized Foreign Certifling Authority`, `shall not issue ceftificates in India`, `Notwithstanding anything contained ln these regulations`, `regularity and extent ofaudit`.

**The automatic guards passed it.** Letter substitutions that keep the vowels, the case and the word count are invisible to every statistic tried here, and the sentence a reader would most want to quote is intact while its neighbours are not — quotable-looking, with no way to know which characters are the Gazette's. So it is refused **by hand**, in `candidates.py`, where the reason is written down (`this.i` @nppnqlxn). Obtaining a clean copy — OCR, or the Gazette's own PDF from a reachable host — is the single highest-value addition to this corpus.

## 8. Extraction flags — three failures in one corpus, all non-empty and plausible

**(a) The India Code watermark, which *reorders*.** Every PDF India Code serves carries a diagonal "India Code" stamp whose glyphs `pdftotext` emits as fragments. In `-layout` mode — `lawcorpus.pdf.extract`'s default — they displace body text: in the 2021 Regulations the words "Official Gazette" are emitted *above* the sentence that ends in them, so `publication in the Official Gazette` greps to zero in a document that says it. In `layout=False` the order survives and the glyphs sit on lines of their own: 140 such lines in one 32-page instrument, with tokens `e`, `od`, `aC`, `di`, `In` — none removable by a blind filter, since `In` opens a sentence in this corpus. **The remedy is to dodge it**: the stored text is the publisher's own `TEXT` bundle, which is watermark-free, with our extraction as the control (`this.i` @yt6p5u4j).

**(b) The publisher's own extraction is silently truncated, once.** India Code's `TEXT` bundle for the **Digital Personal Data Protection Rules, 2025** stops at **exactly 100,000 characters**, mid-sentence, with no marker, where our extraction of the same PDF runs to 119,414 and ends with the printer's colophon. Every other document here has a publisher text 1.01–1.27× the length of ours. That instrument is therefore stored from **our own extraction**, with a `quotation_qualifier` saying so (`this.i` @ah7ssl3s). An inventory comparison cannot see this failure, because a schedule at the end of an instrument restarts its numbering and contributes no heading the body has not already used.

**(c) Legacy-font Hindi, which is not mojibake but scores as it.** A 2016 Gazette page sets its Hindi in a non-Unicode Devanagari font, so the Hindi extracts as Latin rubbish — `jftLVªh laö Mhö ,yö&33004@99`, `dk-vk- 2927¼v½` — beside English that is *perfect*. Judged whole-document, S.O. 2927(E) scores exactly where the genuinely corrupt 2013 Regulation scores. Both commencement notifications are stored, because the measurement is windowed and the passages they are carried for are sound; their manifest rows carry a qualifier saying only 29% and 50% of the document reads as English and that the Devanagari is not quotable at all (`this.i` @nppnqlxn).

## 9. Hosts that cannot be reached from this box

Egress is OVH, Hillsboro, Oregon, US.

| Host | Result | What is lost |
|---|---|---|
| `backend.uidai.gov.in` | TCP timeout | the OVSE Handbook, the list of registered OVSEs, most UIDAI circulars |
| `ovse.uidai.gov.in` | TCP timeout | the OVSE registration portal — and therefore whatever eligibility rules the application form states |
| `ocsp.ncode.in` | TCP timeout | OCSP for UIDAI's signing certificate. The CRL serves (200, 176,776 bytes) |
| `cf-media.api-setu.in` | 403 from CloudFront, with `apisetu.gov.in/digilocker` serving 200 as a control | the DigiLocker Issuer and Requester specifications, and `DigiLocker_International_SOP_09062026.pdf` |
| `main.sci.gov.in`, `digiscr.sci.gov.in` | NXDOMAIN | nothing — `api.sci.gov.in` serves the judgments |

It is per-host and not per-subnet: `uidai.gov.in` at `103.57.226.101` answers and `backend.uidai.gov.in` at `103.57.226.31` does not. Whether that is geo-blocking, a WAF, or an origin not meant to be public cannot be told from here. **A document CDN that 403s a foreign request is itself a partial answer about foreign participation**, which is why it is recorded as evidence rather than only as an obstacle.

Two UIDAI paths that 404 with positive controls firing on the same prefix, so their absence is real: `images/uidai_offline_publickey_26022021.cer` and `images/resource/eligibility_criteria_for_aua_kua_17122016.pdf`.

## 10. The `machine` translation case that could not be stored

UIDAI's site footer says its translation is Bhashini Machine Translation. Both `uidai.gov.in/en/ovse` and `uidai.gov.in/hi/ovse` return **the same English body** — 305,971 and 305,942 characters, eighteen Devanagari characters each — because the Hindi is rendered in the reader's browser. So there is no artefact to store, hash, or quote. India was expected to supply this programme's first real `translation_status: machine` item and supplies instead a category the vocabulary does not have: **a translation with no artefact**, whose right handling is exclusion. See [`../findings/india-is-a-language-control-and-uidais-hindi-exists-only-in-the-browser.md`](../findings/india-is-a-language-control-and-uidais-hindi-exists-only-in-the-browser.md).

## 11. Amendment footnotes

[`amendment-footnotes.tsv`](amendment-footnotes.tsv) holds India Code's `dc.identifier.section_footnote` for the 37 sections that have one — which instrument amended the provision, and when. It is **provenance and not corpus**: it is what every `validity_note` naming an amending Act is built from, and it is kept out of `corpus-acts/` because footnotes quote the superseded words and a corpus item is a thing quote-or-drop will retrieve (`this.i` @gogceltr).

## 12. Not in this corpus

The full scope decision, with reasons, is `OUT_OF_SCOPE` at the foot of [`../tools/candidates.py`](../tools/candidates.py). In short: the Hindi texts (provenance unestablished), 26 deadline-extension notifications, UIDAI's employment and adjudication machinery, and three of the five judgments the spike named — Binoy Viswam (2017), Beghar Foundation (2021) and Rojer Mathew (2019). Each of those three needs a diary number looked up by hand on a captcha-gated search surface, and **no finding here asserts that the 2018 holding is final**, which is the claim their absence would otherwise have licensed.
