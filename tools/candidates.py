#!/usr/bin/env python3
"""The work-list: what this corpus contains, and what it deliberately does not.

`method.md` §8 — *scope is a file, not a vibe*. Everything here is declared before it is fetched, so
that "out of scope" is a decision somebody made rather than something nobody thought of, and so that
`method.md` §2's identity check has something to compare the retrieved title against.

**The corpus is in three parts, at two grains, and the difference is real rather than a compromise.**
India Code publishes each section of each Act as its own item, so the Act layer is stored at
provision grain (`this.i` @4sxgog). It publishes delegated legislation as a PDF with no text field at
all, so that layer is stored at instrument grain. Judgments are hand-curated, five of them
(`this.i` @hyjd5n). A finding says which grain it is quoting, because a section item and a whole
regulation carry their validity banners at different resolutions.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# --------------------------------------------------------------------------------------------
# The Act layer — provision as item
# --------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class ActLayer:
    """One Act, harvested as one corpus item per section."""

    key: str  # index into indiacode.ACT_IDS
    prefix: str  # item_id prefix, e.g. AADHAAR-2016 -> AADHAAR-2016-s7
    citation: str  # citation template, `{s}` for the section number
    title: str  # the Act's own title, as India Code states it
    expect_title: str  # the phrase the retrieved item's act_name must carry (method.md §2)
    sections: tuple = ()  # (), meaning every section India Code files under this act_id
    expect_count: int = 0  # 0 means "no declared count"; otherwise a hard oracle
    oracle_pdf: str = ""  # an independent publisher's consolidated text, for the section list
    oracle_note: str = ""


AADHAAR = ActLayer(
    key="aadhaar-2016",
    prefix="AADHAAR-2016",
    citation="Aadhaar (Targeted Delivery of Financial and Other Subsidies, Benefits and Services) "
    "Act, 2016 (Act 18 of 2016), s. {s}",
    title="The Aadhaar (Targeted Delivery of Financial and Other Subsidies, Benefits and Services) "
    "Act, 2016",
    expect_title="Aadhaar (Targeted Delivery of Financial and Other Subsidies",
    expect_count=69,
    # UIDAI's own consolidated edition, a different publisher and a different artefact, checked
    # against India Code's section items section by section. This is the California/OAL pattern of
    # `method.md` §2: where an independent authority states what the corpus should contain, make it
    # a hard oracle. It is fetched for the oracle only and is **not** stored as corpus text — see
    # `sources/registry.md`, "Sources used as oracles rather than corpus".
    oracle_pdf="https://uidai.gov.in/images/Aadhaar_Act_2016_as_amended.pdf",
    oracle_note="UIDAI consolidated edition, Aadhaar_Act_2016_as_amended.pdf",
)

DPDP = ActLayer(
    key="dpdp-2023",
    prefix="DPDP-2023",
    citation="Digital Personal Data Protection Act, 2023 (Act 22 of 2023), s. {s}",
    title="The Digital Personal Data Protection Act, 2023",
    expect_title="Digital Personal Data Protection Act, 2023",
    expect_count=44,
    oracle_note="India Code's own ACT-level PDF of the same Act — the same publisher, a different "
    "artefact, so this is a weaker control than the Aadhaar Act's and is declared as one",
)

# The supporting Acts. Only the provisions the findings actually rest on: this repo is about Aadhaar
# and the DPDP Act, and harvesting the whole Copyright Act to quote three sections of it would put
# 80 items in the corpus that no finding will ever cite. Each is named individually so that the
# choice is visible and a later reader can add one.
COPYRIGHT = ActLayer(
    key="copyright-1957",
    prefix="COPYRIGHT-1957",
    citation="Copyright Act, 1957 (Act 14 of 1957), s. {s}",
    title="The Copyright Act, 1957",
    expect_title="Copyright Act, 1957",
    sections=("2", "17", "28", "52"),
)

IT_ACT = ActLayer(
    key="it-2000",
    prefix="IT-2000",
    citation="Information Technology Act, 2000 (Act 21 of 2000), s. {s}",
    title="The Information Technology Act, 2000",
    expect_title="Information Technology Act, 2000",
    sections=("2", "19", "43A"),
)

OFFICIAL_LANGUAGES = ActLayer(
    key="official-languages-1963",
    prefix="OFFLANG-1963",
    citation="Official Languages Act, 1963 (Act 19 of 1963), s. {s}",
    title="The Official Languages Act, 1963",
    expect_title="Official Languages Act, 1963",
    sections=("5",),
)

ACT_LAYERS = (AADHAAR, DPDP, COPYRIGHT, IT_ACT, OFFICIAL_LANGUAGES)


# --------------------------------------------------------------------------------------------
# Validity on the Act layer
# --------------------------------------------------------------------------------------------

# **The Aadhaar Act.** Every section is in force as it now stands — the 2019 Amendment Act's changes
# are *in* the text India Code serves, so `amended` would be wrong for them: that token means "this
# copy is a superseded version", and these are the current ones. What is not in force is recorded
# here, and the judicial rows come from `sources/judicial-overlay.tsv` rather than from this table
# (`this.i` @q3dsvsrl), so the two cannot disagree.
AADHAAR_VALIDITY = {
    "57": (
        "repealed",
        "Omitted by the Aadhaar and Other Laws (Amendment) Act, 2019 (Act 14 of 2019), s. 25 "
        "(w.e.f. 25-7-2019). The part of it that enabled a body corporate or person to seek "
        "authentication had already been held unconstitutional in K.S. Puttaswamy v. Union of "
        "India (26 Sep 2018), and Parliament then omitted the section entire.",
    ),
}
# Sections 2, 7, 33 and 47 are deliberately absent from this table. Everything a court did to them
# lives in `sources/judicial-overlay.tsv`, which is the single authored record of judicial validity
# and the thing the manifest is generated from — `this.i` @q3dsvsrl. §57 is here because Parliament
# omitted it, which is a statutory fact; the 2018 disposition on §57 is in the overlay, marked spent.

# **The DPDP Act.** Most of it is not in force. The instrument that says so is G.S.R. 843(E), the
# Ministry of Electronics and Information Technology notification of 13 November 2025, which appoints
# three commencement dates under s. 1(2). It is harvested as `DPDP-COMMENCEMENT-2025` and the table
# below is read off it; `tools/harvest.py` re-derives the table from the stored notification text and
# aborts on a disagreement, so this is a transcription that is checked rather than trusted.
#
# Verbatim, from the notification: "(a) the date of publication of this notification in the Official
# Gazette as the date on which the provisions of sub-section (2) of section 1, section 2, sections 18
# to 26 sections 35, 38, 39, 40, 41, 42, 43, and sub-sections (1) and (3) of section 44 of the said
# Act shall come into force; (b) one year from the date of publication of this gazette on which the
# provisions of sub-section (9) of section 6 and clause (d) of sub-section (1) of section 27 of the
# said Act shall come into force. (c) eighteen months from the date of publication of this gazette,
# on which the provision of sections 3 to 5, sub-sections (1) to (8) and (10) of section 6,sections 7
# to 10, sections 11 to 17, section 27 except clause (d) of sub-section (1) of the said section,
# sections 28 to 34, 36, 37 and sub-section (2) of section 44 of the said Act shall come into force."
DPDP_COMMENCED = ("2",) + tuple(str(n) for n in range(18, 27)) + ("35", "38", "39", "40", "41", "42", "43")
DPDP_PART_COMMENCED = {
    # A section some of which is in force and some of which is not. Marked not-yet-applicable, which
    # fails closed: a reader quoting the part that *is* in force gets a banner telling them to check,
    # where the other choice would let them quote the part that is not as current law.
    "6": "Sub-section (9) comes into force 13-11-2026 and sub-sections (1) to (8) and (10) on "
    "13-5-2027, per G.S.R. 843(E) of 13-11-2025. No part of this section is in force today.",
    "27": "Clause (d) of sub-section (1) comes into force 13-11-2026 and the rest of the section on "
    "13-5-2027, per G.S.R. 843(E) of 13-11-2025. No part of this section is in force today.",
    "44": "Sub-sections (1) and (3) are in force from 13-11-2025; sub-section (2), which amends "
    "section 8(1)(j) of the Right to Information Act, 2005, comes into force 13-5-2027. Per "
    "G.S.R. 843(E) of 13-11-2025.",
}
DPDP_DEFERRED_NOTE = (
    "Not yet in force. G.S.R. 843(E) of 13-11-2025 appoints 13-5-2027 as the commencement date for "
    "this section, under s. 1(2) of the Act."
)
DPDP_SECTION_1_NOTE = (
    "Section 1 carries the short title and the commencement power; G.S.R. 843(E) of 13-11-2025 "
    "expressly appoints sub-section (2) as in force from that date."
)


# --------------------------------------------------------------------------------------------
# The delegated layer — instrument as item
# --------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Delegated:
    """One delegated instrument, or one constitutional or Gazette document, stored whole."""

    item_id: str
    handle: str
    citation: str
    expect_title: str
    authority_tier: str = "delegated"
    validity: str = "in-force"
    validity_note: str = ""
    bitstream: str = ""  # which ORIGINAL bitstream, when an item carries several (En + Hi)
    version_id: str = ""
    expect_phrase: tuple = ()  # phrases the stored text must carry, checked before it is stored
    unquotable: str = ""  # a hand refusal: why a person read this document and would not store it
    note: str = ""


DELEGATED = (
    Delegated(
        item_id="AOV-REGS-2021",
        handle="123456789/507089",
        citation="Aadhaar (Authentication and Offline Verification) Regulations, 2021, as amended to "
        "9-12-2025",
        expect_title="Aadhaar (Authentication and Offline Verification) Regulations, 2021",
        bitstream="aov_eng.pdf",
        version_id="[Updated as on 09.12.2025]",
        expect_phrase=(
            "Aadhaar Verifiable Credential",
            "Registration of OVSE",
            "publication in the Official Gazette",
        ),
        note="The operative instrument for the whole credential stack. Its Reg. 2(be), 3A and 13A "
        "were inserted or substituted by the amendment notified on 9 December 2025.",
    ),
    Delegated(
        item_id="SWIK-RULES-2020",
        handle="123456789/510201",
        citation="Aadhaar Authentication for Good Governance (Social Welfare, Innovation, Knowledge) "
        "Rules, 2020, as amended to 31-1-2025",
        expect_title="Aadhaar Authentication for Good Governance",
        bitstream="swik_rules_-english_version.pdf",
        version_id="[Updated as on 1.4.2025]",
        expect_phrase=("in the interest of State",),
        note="India Code titles the item '…Rules, 2021'; the instrument's own heading says 2020, and "
        "the citation follows the instrument. This is the route by which a non-statutory entity "
        "reaches Aadhaar authentication, and it begins at a Ministry.",
    ),
    Delegated(
        item_id="ENROLMENT-REGS-2016",
        handle="123456789/507087",
        citation="Aadhaar (Enrolment and Update) Regulations, 2016",
        expect_title="Aadhaar (Enrolment and Update) Regulations, 2016",
    ),
    Delegated(
        item_id="DATA-SECURITY-REGS-2016",
        handle="123456789/507088",
        citation="Aadhaar (Data Security) Regulations, 2016",
        expect_title="Aadhaar (Data Security) Regulations, 2016",
    ),
    Delegated(
        item_id="SHARING-REGS-2016",
        handle="123456789/507092",
        citation="Aadhaar (Sharing of Information) Regulations, 2016",
        expect_title="Aadhaar (Sharing of Information) Regulations, 2016",
    ),
    Delegated(
        item_id="DPDP-RULES-2025",
        handle="123456789/510190",
        citation="Digital Personal Data Protection Rules, 2025 (G.S.R. 843(E) series, 13-11-2025)",
        expect_title="Digital Personal Data Protection",
        validity="not-yet-applicable",
        validity_note="Phased commencement by their own rule 1: rules 1, 2 and 17 to 21 from "
        "13-11-2025, rule 4 from 13-11-2026, and rules 3, 5 to 16, 22 and 23 from 13-5-2027. The "
        "instrument is stored whole, so most of what it contains is not yet in application.",
        expect_phrase=("Digital Personal Data Protection Rules, 2025",),
    ),
    Delegated(
        item_id="AADHAAR-COMMENCEMENT-1-10-24-47",
        handle="123456789/504689",
        citation="S.O. 2927(E), 12-9-2016 — commencement of ss. 1 to 10 and 24 to 47 of the Aadhaar "
        "Act, 2016",
        expect_title="Enforcement of provisions of sections 1 to 10 and 24 to 47",
        expect_phrase=("shall come into force",),
        note="The S.O. number is read off the notification's own English text. An earlier draft of "
        "this file carried 'S.O. 2914(E)', which is not a number anybody published — it was "
        "remembered rather than retrieved, which is the failure `method.md` §2 is about, committed "
        "inside the tool that exists to catch it.",
    ),
    Delegated(
        item_id="AADHAAR-COMMENCEMENT-11-20-22-23-48-59",
        handle="123456789/504683",
        citation="S.O. 2357(E), 12-7-2016 — commencement of ss. 11 to 20, 22 to 23 and 48 to 59 of "
        "the Aadhaar Act, 2016",
        expect_title="Enforcement of provisions of sections 11 to 20",
        expect_phrase=("shall come into force",),
    ),
    Delegated(
        item_id="DPDP-COMMENCEMENT-2025",
        handle="123456789/504682",
        citation="G.S.R. 843(E), 13-11-2025 — commencement of the Digital Personal Data Protection "
        "Act, 2023",
        expect_title="Enforcement Timeline for the DPDP Act",
        expect_phrase=("sub-section (2) of section 1", "eighteen months"),
        note="The instrument that decides the validity of all 44 DPDP sections. Bilingual Gazette "
        "page: the Hindi half extracts as mojibake and the English half is clean.",
    ),
    Delegated(
        item_id="CONSTITUTION-2026",
        handle="123456789/618394",
        citation="Constitution of India (English, as published by India Code, 2026)",
        expect_title="Constitution of India",
        authority_tier="constitutional",
        expect_phrase=("shall be in the English language",),
        note="Carried for Article 348(1)(b), which makes English the authoritative text of every "
        "central Act and of the whole delegated layer, and therefore decides that India is a "
        "language control rather than a translation problem.",
    ),
)

# The instrument the spike found and could not read: the Information Technology (Recognition of
# Foreign Certifying Authorities operating under a Regulatory Authority) Regulation, 2013, handle
# 123456789/507084. It is still fetched and still measured on every run, so that the refusal is
# current rather than remembered, and it is **not** stored. See `sources/registry.md`, "What was
# refused and why".
FOREIGN_CA_REGULATION = Delegated(
    item_id="FOREIGN-CA-REG-2013",
    handle="123456789/507084",
    citation="Information Technology (Recognition of Foreign Certifying Authorities operating under "
    "a Regulatory Authority) Regulation, 2013",
    expect_title="Recognition of Foreign Certifying Authorities",
    expect_phrase=("shall not issue digital signature certificates to Indian nationals",),
    unquotable="Refused by hand on 2026-09-16, after the automatic guards let it through. Its "
    "out-of-vocabulary rate against the Act layer's own words is 0.62, against 0.15–0.40 for every "
    "sound instrument here — but that spread also covers two notifications whose English is perfect, "
    "and the windowed soundness test passes the passage that matters, so a "
    "person reading that passage finds 'Recognized Foreign Certifling Authority', 'shall not issue "
    "ceftificates in India', 'Notwithstanding anything contained ln these regulations', "
    "'regularity and extent ofaudit'. Letter substitutions that keep the vowels, the case and the "
    "word count are invisible to every statistical test tried here and obvious to a reader. The "
    "sentence we would want to quote is intact and its neighbours are not, which is the worst "
    "possible shape: quotable-looking, and no way to be sure which characters are the Gazette's.",
    note="The implementing instrument for IT Act s. 19 — the only statutory route by which a foreign "
    "certifying authority is recognised in India, and therefore the one document that would settle "
    "whether a foreign issuer may issue to Indian residents. What it says matters and our copy of it "
    "cannot be quoted, which is the state of that question rather than an answer to it.",
)


# --------------------------------------------------------------------------------------------
# The judicial layer — five documents, hand-curated
# --------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Judgment:
    item_id: str
    url: str
    citation: str
    title: str
    expect_phrase: tuple
    validity: str = "in-force"
    validity_note: str = ""
    note: str = ""


JUDGMENTS = (
    Judgment(
        item_id="PUTTASWAMY-2017",
        url="https://api.sci.gov.in/supremecourt/2012/35071/35071_2012_Judgement_24-Aug-2017.pdf",
        citation="K.S. Puttaswamy (Retd.) v. Union of India, W.P. (C) No. 494 of 2012, Supreme Court "
        "of India, 24 August 2017, (2017) 10 SCC 1",
        title="Justice K.S. Puttaswamy (Retd.) and another v. Union of India and others (privacy)",
        expect_phrase=("IN THE SUPREME COURT OF INDIA",),
        note="Nine judges. The frame everything about Aadhaar is read against.",
    ),
    Judgment(
        item_id="PUTTASWAMY-2018",
        url="https://api.sci.gov.in/supremecourt/2012/35071/35071_2012_Judgement_26-Sep-2018.pdf",
        citation="K.S. Puttaswamy (Retd.) v. Union of India, W.P. (C) No. 494 of 2012, Supreme Court "
        "of India, 26 September 2018, (2019) 1 SCC 1",
        title="Justice K.S. Puttaswamy (Retd.) and another v. Union of India and others (Aadhaar)",
        expect_phrase=("IN THE SUPREME COURT OF INDIA",),
        note="Five judges, 567 pages. Every row of the judicial overlay comes from this judgment.",
    ),
    Judgment(
        item_id="PUTTASWAMY-2018-SCR",
        url="https://cdnbbsr.s3waas.gov.in/s3ec0490f1f4972d133619a60c30f3559e/documents/"
        "aor_notice_circular/48.pdf",
        citation="Justice K.S. Puttaswamy (Retd.) v. Union of India, [2018] 8 S.C.R. — Supreme Court "
        "Reports, the official law report",
        title="Justice K.S. Puttaswamy (Retd.) v. Union of India [2018] 8 S.C.R. (official report)",
        expect_phrase=("S.C.R.",),
        note="Preferred for quotation over the raw judgment PDF: it is the official law report, it "
        "carries the headnote, and its enumerated answer to Issue 4 states the operative "
        "dispositions in one place, which is what the overlay is built from.",
    ),
)


# --------------------------------------------------------------------------------------------
# What is deliberately not here
# --------------------------------------------------------------------------------------------

OUT_OF_SCOPE = """
Recorded 2026-09-16, with the reason, so that a later reader can add one deliberately rather than
discovering the gap. `method.md` §8: scope is a file, not a vibe.

- **The Hindi texts.** `hindiaadhaar.pdf` and `aov_hin.pdf` sit beside the English ones on India
  Code, and s. 5(1) of the Official Languages Act, 1963 makes a Hindi translation published under
  the President's authority in the Gazette the authoritative Hindi text. Whether *these* files are
  those texts is not evidenced by their sitting next to the English ones, and nothing in this
  corpus's findings turns on the Hindi. Carrying them as `authoritative` on an assumption is the
  error this programme's translation vocabulary exists to prevent.
- **The remaining ~26 notifications under the Aadhaar Act**, which are deadline extensions for
  producing an Aadhaar number under specific welfare schemes. The two commencement notifications
  are carried because they decide when the Act's own sections began; the rest decide dates for
  programmes this repo says nothing about.
- **The UIDAI (Adjudication of Penalties) Rules 2021, the Returns and Annual Report Rules 2018,
  the Unique Health Identifier Rules 2021 and UIDAI's service-conditions rules.** Machinery about
  UIDAI as an employer and adjudicator, not about the credential or about who may verify it.
- **The Aadhaar (Payment of Fees for Performance of Authentication) Regulations, 2023.** Pricing,
  and reachable in a later pass if a finding ever needs it.
- **Two judgments named in the spike's work-list and not retrieved**: Binoy Viswam v. Union of
  India (2017) on s. 139AA of the Income Tax Act, Beghar Foundation (2021) dismissing the review
  petitions, and Rojer Mathew (2019) referring the Money Bill question onward. Each needs its diary
  number looked up by hand on a captcha-gated search surface before the deterministic PDF URL can
  be built, and none of them changes a disposition this corpus records. Their absence is why no
  finding here asserts that the 2018 holding is final.
- **Everything on `backend.uidai.gov.in` and `ovse.uidai.gov.in`** — the OVSE Handbook, the list of
  registered OVSEs, the registration portal, most UIDAI circulars. Those hosts are a TCP blackhole
  from this egress, which is itself recorded as a finding rather than worked around.
"""
