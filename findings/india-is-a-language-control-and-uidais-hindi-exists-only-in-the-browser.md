# English is the authoritative text by constitutional command, and UIDAI's Hindi has no artefact to store

**Question:** does this programme's translation machinery apply to India?
**Corpus:** `corpus-acts/`, `corpus-delegated/` at 2026-09-16.
**Answer, short:** no, for the corpus. Article 348(1)(b) of the Constitution makes English the authoritative text of every central Act *and* of every rule and regulation made under one, so India is a **language control** alongside Singapore rather than a translation problem. It is not a monolingual jurisdiction — s. 5(1) of the Official Languages Act, 1963 makes a Presidentially-authorised Hindi translation authoritative *in Hindi* — which is why the Hindi PDFs sitting beside the English ones on India Code are out of scope rather than filed as authoritative. And UIDAI's Hindi pages, which the spike identified as this vocabulary's first real `machine` case, turn out not to be storable at all, for a reason worth recording.

## 1. The constitutional provision, and it reaches the delegated layer too

`corpus-delegated/CONSTITUTION-2026`:

> 348. Language to be used in the Supreme Court and in the High Courts and for Acts, Bills, etc.—(1) Notwithstanding anything in the foregoing provisions of this Part, until Parliament by law otherwise provides— (a) all proceedings in the Supreme Court and in every High Court; (b) the authoritative texts— … (ii) of all Acts passed by Parliament or the Legislature of a State and of all Ordinances promulgated by the President or the Governor … of a State; and (iii) of all orders, rules, regulations and bye-laws issued under this Constitution or under any law made by Parliament or the Legislature of a State, shall be in the English language.

*(The ellipsis after "Governor" stands for `1***`, India Code's own mark for the words "or Rajpramukh", omitted by the Constitution (Seventh Amendment) Act, 1956. It is in the stored text because it is in the Constitution as India Code publishes it.)*

Sub-clause (iii) is the part that matters here and the part a summary would drop. Article 348 is usually cited for Acts; it says the same thing about **orders, rules, regulations and bye-laws**. So the 2021 Regulations and the 2020 SWIK Rules are authoritative in English, which is why every item in `corpus-delegated/` is filed `translation_status: authoritative` and carries no translation banner. Every quotation in every finding in this repo is of an authentic text.

## 2. Hindi is not a translation here either, which is why the Hindi PDFs are out of scope

`corpus-acts/OFFLANG-1963-s5`:

> (1) A translation in Hindi published under the authority of the President in the Official Gazette on and after the appointed day,— (a) of any Central Act or of any Ordinance promulgated by the President, or (b) of any order, rule, regulation or bye-law issued under the Constitution or under any Central Act, shall be deemed to be the authoritative text thereof in Hindi.

India is therefore a **two-authentic-texts** jurisdiction of the European kind, not a jurisdiction with an original and a rendering. That sharpens the reason `hindiaadhaar.pdf` and `aov_hin.pdf` are excluded rather than carried: those files might be the Presidentially-authorised texts, in which case `authoritative` is right; or they might be departmental translations, in which case it is badly wrong. What decides it is publication under the President's authority in the Gazette, and sitting next to the English file in a repository is not evidence of that. Recording `authoritative` on the strength of adjacency is the exact default the `translation_status` field exists to refuse.

## 3. The Bhashini case: a machine translation with nothing to store

UIDAI says in its own site footer, served identically on the English and the Hindi paths:

*"UIDAl website translation is done by Bhashini Machine Translation. This is done on experimental basis and will be improved over a period of time. Kindly ignore the errors if any."*

*(That sentence is from a web page and not from the corpus, so it is not offered as a corpus quotation. The `UIDAl` with a lower-case L is UIDAI's own typo, preserved.)*

The programme wanted this as the first real instance of `translation_status: machine` — a stored item that the chokepoints refuse to treat as evidence. **It cannot be that, and the reason is more useful than the demonstration would have been.** Fetched today from this box, `https://uidai.gov.in/en/ovse` and `https://uidai.gov.in/hi/ovse` both return 200 and both return the *same English body*: 305,971 and 305,942 characters, each containing eighteen Devanagari characters. The Hindi is produced by a Bhashini widget in the reader's browser, after the response has been served.

So there is no Hindi artefact. A machine translation that exists only at render time cannot be harvested, cannot be hashed, and cannot be quoted by anybody — including by somebody who wanted to quote it wrongly. The `machine` token is for text that has been *written down*: a stored file somebody could cite. This is a step beyond that, and the honest entry in the registry is that India did not supply the `machine` case after all, because the thing that would have been machine-translated is never serialised.

Two consequences worth carrying. **A claim sourced to "UIDAI's Hindi page" is unverifiable by construction** — two readers can see different text at the same URL on the same day, and neither can produce the bytes. And for this programme's purposes the case still teaches something the vocabulary did not anticipate: between "an official translation" and "a machine translation" there is a third thing, **a translation with no artefact**, and the right handling for it is exclusion rather than a status.

## What this finding does not establish

- Whether India Code's Hindi PDFs are Presidentially-authorised texts under s. 5(1). Establishing it means finding the Gazette notification that authorised each one, which no finding here needs.
- What the Bhashini widget actually renders. Driving a browser at it would produce bytes, but they would be *our* bytes and not a published artefact, which is the whole point above.
