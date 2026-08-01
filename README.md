# aadhaar — India's identity and data-protection regime

> **Status: scaffolded, not yet harvested.** This repo holds its intent and its plan. There is no
> corpus in it yet. Nothing here should be cited for anything.

Part of a family of repos that harvest primary legal sources so they can be analysed later —
by a person or by an AI — without repeating the online research, and without trusting anyone's
memory of what the law says. Shared method and tooling:
**[`id-law-kit`](https://github.com/bakobo/id-law-kit)**.

| Repo | Regime | Corpus |
|---|---|---|
| [`utah-id-law`](https://github.com/bakobo/utah-id-law) | Utah identity-verification law | ✅ |
| [`eu-data-law`](https://github.com/bakobo/eu-data-law) | GDPR + EU data-locality stack | ✅ |
| [`eidas-eudi`](https://github.com/bakobo/eidas-eudi) | eIDAS 2, EUDI wallet, ARF | ✅ |
| [`ccpa`](https://github.com/bakobo/ccpa) | California CCPA/CPRA | ✅ |
| **`aadhaar`** | Aadhaar Act, UIDAI regulations, DPDP Act | ⬜ this repo |

## Why this one is different, and last

The other four repos can answer most questions from statutory and regulatory text. **This one
cannot**, and that is the reason it is sequenced last rather than merely the reason it is hard.

Section 57 of the Aadhaar Act 2016 was **struck down** by the Supreme Court of India in 2018. The
Act PDF that UIDAI publishes today still contains it. An agent applying this programme's central
rule — *quote-or-drop*, admit a claim only with a verbatim quotation retrievable from the corpus —
over that PDF produces a confidently false statement of Indian law, by obeying the rule.

That single case is why `id-law-kit`'s manifest schema carries a required `validity` field with no
default, and why `lawcite` prints a validity banner above every quote it emits. Those defences were
built for this repo before this repo had a corpus.

## Planned scope

| Layer | Source | Difficulty |
|---|---|---|
| Aadhaar Act 2016, as amended | `uidai.gov.in` — direct PDFs | Easy; PDF extraction |
| Aadhaar (Amendment) Act 2019 | `uidai.gov.in` | Easy |
| UIDAI regulations, rules, notifications | `uidai.gov.in` subpages | Moderate; scraping |
| DPDP Act 2023 + DPDP Rules | `indiacode.nic.in` | Moderate |
| **The judgments** | see below | Hard, and mandatory |

The load-bearing judgments are *K.S. Puttaswamy v. Union of India* (2017, privacy as a fundamental
right) and the 2018 Aadhaar judgment that struck down §57 and read down others.

## What the reconnaissance found

Done 2026-07-31, so the next person does not repeat it:

- **`indiacode.nic.in` is an older DSpace with its machine interfaces disabled.** `/oai/request` and
  the DSpace REST endpoints both return **404**. Browsing works (`/handle/123456789/<id>/browse?type=actno`),
  so enumeration means scraping browse pages.
- **UIDAI publishes the primary instruments as direct PDFs** from
  `uidai.gov.in/en/about-uidai/legal-framework.html` — `Aadhaar_Act_2016_as_amended.pdf`,
  `Aadhaar_Act_2016_English.pdf`, `news/Amendment_Act_2019.pdf`, plus regulations/rules/notification
  subpages. Small, stable, and now extractable: `lawcorpus/pdf.py` exists.
- **The judgments have no clean bulk source.** `main.sci.gov.in` is scrape-hostile and Indian Kanoon
  is metered. For five to ten documents that will not change, **hand-curation with full manifest
  entries beats building a scraper** — a scraper's cost is justified by breadth, and there is none
  here. Recorded as `this.i` @hyjd5n.

## Design decisions already recorded

See [`this.i`](this.i). In short: case law is a **mandatory corpus layer** here rather than an
acknowledged gap (@meihbh); judgments are **hand-curated**, not scraped (@hyjd5n); and validity is
recorded **per provision**, not per instrument, because "the Aadhaar Act is amended" would hide
exactly the thing that matters (@4sxgog).

## Licence

The **original work** in this repo is **[CC BY 4.0](LICENSE)**. Attribution: Bakobo, *aadhaar*.

Any corpus added later will **not** be covered by that licence and is not ours to license. Indian
government works sit under GODL-India and section 52(1)(q) of the Copyright Act, 1957 — a different
basis from the US "edicts of government" reasoning used by `utah-id-law` and from the EU's
Decision 2011/833/EU. State the basis in this README when the corpus lands; do not copy another
repo's.

**Not legal advice.** Textual research by non-lawyers, with substantial AI assistance.
