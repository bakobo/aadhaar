# Who may verify an Aadhaar credential is decided by administrative discretion with unpublished criteria

**Questions:** Q11 — what would a foreign verifier have to do to be admitted? Q12 — does data-protection law bar the transaction anyway?
**Language of analysis:** English, which Article 348(1)(b) of the Constitution makes the authoritative text of the Act and of every regulation under it. **Corpus:** `corpus-acts/` (121 provisions), `corpus-delegated/` (10 instruments), at 2026-09-16.
**Answer, short:** there are two gates, and neither is a licence anyone can apply for on published criteria. Online authentication needs an Act of Parliament naming you or an Indian ministry sponsoring you. Offline verification needs registration with UIDAI "on such terms and conditions as may be specified by the Authority" — published nowhere. The one published Indian-incorporation rule binds the network intermediary rather than the verifier, and the schedule that once set criteria for verifiers was deleted from the regulation in February 2023. Cross-border transfer is not the obstacle, and is less of one than it looks, because the section that would restrict it is not in force.

Every quotation below is verbatim from the corpus and reproducible with `tools/check-quotes.py`.

## 1. Online authentication: s. 4(4), and both of its routes begin in India

`corpus-acts/AADHAAR-2016-s4`, in force. Sub-sections (3) to (7) were substituted by the Aadhaar and Other Laws (Amendment) Act, 2019, which is why the stored text carries the amendment mark `1[`.

> (4) An entity may be allowed to perform authentication, if the Authority is satisfied that the requesting entity is--
> (a) compliant with such standards of privacy and security as may be specified by regulations; and
> (b) (i) permitted to offer authentication services under the provisions of any other law made by Parliament; or
> (ii) seeking authentication for such purpose, as the Central Government in consultation with the Authority, and in the interest of State, may prescribe.

Route (b)(i) is an Act of the Indian Parliament naming you. Route (b)(ii) is the Aadhaar Authentication for Good Governance (Social Welfare, Innovation, Knowledge) Rules, 2020, and rule 4 routes every applicant through a Ministry. `corpus-delegated/SWIK-RULES-2020`:

> (2) Any entity other than the Ministry or Department referred to in sub-rule (1), which is desirous of utilising Aadhaar authentication, shall prepare a proposal with justification in regard to the authentication sought being for a purpose specified in rule 3 and in the interest of State, and submit the same to the concerned Ministry or Department of the appropriate Government.

So there is **no route to Aadhaar authentication that does not begin with an Indian statute or an Indian ministry.** It is not a licence you apply for; it is a sponsorship you obtain, ending in a notification in the Gazette. Whether the applicant is foreign is not what the provision turns on — it turns on finding an Indian ministry willing to say the purpose is "in the interest of State", which is a different and harder thing.

## 2. Offline verification: registration exists, and its criteria do not

The 2021 Regulations were amended on 9 December 2025 to insert Reg. 13A. `corpus-delegated/AOV-REGS-2021`:

> 13A. Registration of OVSE.- (1) An entity desirous of undertaking Aadhaar Paperless Offline e-KYC verification or Aadhaar Verifiable Credential verification through Aadhaar Application shall apply to the Authority for registration, in such form as the Authority may provide upon request made to it by such entity and **on such terms and conditions as may be specified by the Authority from time to time**

and the decision:

> (4) The Authority may, if it is satisfied that the entity is eligible as per the terms and conditions specified by the Authority, may approve the application and register the entity as OVSE.

There is a procedure — a fifteen-day deadline for communicating a rejection with grounds, a right to seek reconsideration — and there are no criteria. The regulation does not state them, the Act does not state them, and they are whatever UIDAI's terms and conditions say on the day. **That is an administrative gate whose contents are not law and are not published.**

What the registration requires *technically* is published, on UIDAI's OVSE page, and it inverts the usual direction of trust: the verifier hands UIDAI a public certificate and registers a domain and a callback URL to which UIDAI posts the result. That is a claim about a web page rather than about an instrument, so it is not quoted here; see `sources/registry.md`, "Sources this repo could not reach".

## 3. There *is* an Indian-incorporation requirement, it binds a different role, and the one that used to bind the verifier was deleted

A phrase-family sweep over both corpora with `lawcite --grep` — `incorporat`, `registered in India`, `Companies Act`, `body corporate`, `resident in India`, `established in India`, `domicile` — returns exactly one incorporation rule about an entity in the Aadhaar stack, and it is not where the question expected it. Schedule A of the 2021 Regulations, `corpus-delegated/AOV-REGS-2021`:

> ELIGIBILITY CRITERIA OF AUTHENTICATION SERVICE AGENCIES
> [See regulation 12(2A)]
> 1. Entities seeking appointment as ASA are categorised as follows:
> … Category 4 A company registered in India under the Companies Act, 2013 (18 of 2013)

with, for that category:

> Annual turnover of at least ₹100 crore … A Telecom Service Provider … having a minimum of 100 Multiprotocol Label Switching (MPLS) Points of Presence (PoP) in India

An **Authentication Service Agency is the network intermediary** that carries a request to the CIDR, not the party asking the question. So the published incorporation rule binds the pipe, and a foreign verifier would in any case be reaching the CIDR through somebody else's pipe.

For the **requesting entity** — the verifier — Reg. 12 sets no eligibility criterion at all:

> (1) An agency or other person seeking appointment as a requesting entity for use of an Authentication facility shall apply to the Authority for appointment, in such form as the Authority may provide upon request made to it by such agency or person

followed by:

> (1A) Requesting entity and ASA shall meet technical and security criteria as specified by the Authority from time to time.

**And criteria for requesting entities were once in this instrument and were taken out.** The regulation's own footnote records it:

> “Schedule A” omitted vide notification No. HQ-13011/240/2021-AUTH-II (No. 01 of 2023) dated 24.2.2023 … “Schedule B” was substituted by “Schedule A”

So in February 2023 the schedule of eligibility criteria was deleted and the ASA schedule renamed into its place.

*(That quotation is of the instrument's own amendment-history footnote, which records what changed. It is not a superseded wording. The delegated layer does carry superseded wordings in its footnotes — Reg. 12(1) of this same instrument is followed by "Regulation 12(1), before substitution, stood as under:" and then the old text in quotation marks — and because this layer is stored at instrument grain, item-level validity reads `in-force` over the lot. That is the declared cost of the mixed grain; see the README.)* That is the finding in §2 arriving from a second direction and with a date on it: **eligibility for the party that asks moved out of published delegated legislation and into "criteria as specified by the Authority from time to time", while eligibility for the party that carries stayed published.** Reg. 13A of December 2025 then created the OVSE gate in the same unpublished shape.

This is a claim about instruments, not about practice. The OVSE Handbook and the application form are the two documents most likely to carry a rule, they are linked from UIDAI's own page, and they sit on a host that does not answer this egress at all (`sources/registry.md`). The honest statement is that the gate may well live in the form — which is exactly what a deleted schedule and an "as specified by the Authority" clause would predict.

## 4. Section 8A is the sharp constraint on an offline verifier, and it is in the Act

`corpus-acts/AADHAAR-2016-s8A`, inserted by Act 14 of 2019 and in force:

> (4) No offline verification-seeking entity shall---
> (a) subject an Aadhaar number holder to authentication;
> (b) collect, use, or store an Aadhaar number or biometric information of any individual for any purpose;
> (c) take any action contrary to any obligation on it as may be specified by regulations.

Holding the number at all is prohibited. For a verifier building on the Secure QR this is not a burden — the QR carries only the last four digits — but it forecloses the obvious architecture in which a relying party keeps the Aadhaar number as a key.

## 5. Cross-border transfer is not the gate, and the section that would be is not in force

`corpus-acts/DPDP-2023-s16` is **not yet applicable**: G.S.R. 843(E) of 13 November 2025 appoints 13 May 2027 as its commencement date. The banner `lawcite` prints above it says so. What it will say then:

> (1) The Central Government may, by notification, restrict the transfer of personal data by a Data Fiduciary for processing to such country or territory outside India as may be so notified.

That is a **blacklist**, the inverse of GDPR Chapter V: transfer is permitted by default and restricted only to countries the Central Government notifies. No country has been notified. Sub-section (2) preserves stricter sectoral rules, which is where the real constraint lives for payments data.

So on this corpus's evidence, for the question "may a foreign verifier receive Indian personal data", Indian law today says less than it will in 2027 and less than Korea's PIPA says now. **The obstacle is admission, not data-protection law** — and this is the cleanest instance of that pattern in the programme, because here the two come apart completely: nothing in the cryptography and nothing in the transfer rules stands in the way, and s. 4(4) and Reg. 13A do.

## What this finding does not establish

- Whether a non-Indian entity has ever been registered as an OVSE, or ever applied. Nothing in this corpus speaks to practice.
- What UIDAI's terms and conditions under Reg. 13A(1) actually require. They are not published where this corpus could reach them, and they are the operative rule.
- Whether the AUA/KUA eligibility criteria contain an incorporation requirement. UIDAI's own eligibility PDF 404s with positive controls firing on the same path prefix, so its absence is real and its contents are unknown.
