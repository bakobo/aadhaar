# aadhaar — Intent Tree (this.i)

A checkable corpus of India's Aadhaar and data-protection regime = goal:
  id: pwt4yj
  why: >
    Harvest the Aadhaar Act 2016 as amended, the UIDAI regulations, the DPDP Act 2023 and its
    rules, and the constitutional judgments that govern how the Act is read — so that later
    analysis of the world's largest identity system can quote sources rather than recall them.
    Driving constraint that separates this repo from the other four: the statutory text alone is
    actively misleading here, so the corpus is not complete without case law. Tradeoff accepted:
    this is the most expensive of the five to harvest — PDF sources, a document repository with its
    machine interfaces disabled, and judgments with no clean bulk feed — and is therefore
    deliberately sequenced last, after the tooling has matured on easier regimes.
  children:
    Case law is a mandatory corpus layer, not an acknowledged gap = decision:
      id: meihbh
      why: >
        utah-id-law excludes judicial decisions and says so in Known Gaps; that exclusion is
        defensible in Utah, where statutory text usually carries the answer. It is indefensible
        here. Section 57 of the Aadhaar Act was struck down by the Supreme Court in 2018, and
        Puttaswamy (2017) set the privacy frame the Act is read against — yet the Act PDF published
        on uidai.gov.in still carries the struck text. A quote-or-drop rule applied to that PDF
        would manufacture a confidently false claim, which is the exact failure the rule exists to
        prevent. Rejected treating the judgments as commentary to be cited loosely. Tradeoff: the
        judgments are long, discursive, and plurality-split, so mapping "which provision did this
        judgment do what to" is hand work that cannot be mechanized.

    Judgments are hand-curated rather than scraped = decision:
      id: hyjd5n
      why: >
        indiacode.nic.in is an older DSpace whose OAI-PMH and REST interfaces both return 404, so
        enumeration means scraping browse pages; the Supreme Court's own site and Indian Kanoon are
        the alternatives, one scrape-hostile and one metered. Chose to hand-curate the five to ten
        judgments that are actually load-bearing, with full manifest entries, over building a
        scraper. A scraper's cost is justified by breadth, and here the breadth is a handful of
        documents that will not change. Tradeoff: the corpus cannot answer questions about the
        wider case law, and adding a judgment later is manual work rather than a refetch.

    Validity is recorded per provision, not per instrument = decision:
      id: 4sxgog
      why: >
        The id-law-kit manifest carries validity per corpus item, which is the right granularity
        for an instrument that is wholly in force or wholly repealed. The Aadhaar Act is neither:
        one section was struck down, others were read down, and the 2019 Amendment Act rewrote
        parts in response. Recording validity for the Act as a whole would be useless — it would
        read "amended" and hide the thing that matters. Chose to carry a provision-level validity
        overlay in this repo, keyed to the item, rather than pushing the complexity into the shared
        schema for four repos that do not need it. Tradeoff: an overlay is a second place that can
        drift from the manifest, and cite.py must consult both to print an honest banner.
