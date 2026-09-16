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

        Corrected 2026-09-16, reasoning intact and example replaced. The consolidated PDF UIDAI
        serves is right: its §57 reads "[Omitted.]", and quote-or-drop over it cannot manufacture the
        claim. The danger is Aadhaar_Act_2016_English.pdf, the annotated edition UIDAI's rebuilt
        legal page now links, whose body marks §57 repealed and whose footnote then reproduces the
        omitted text in full inside quotation marks. That is worse than the stale file this node
        assumed: it is a drafting convention rather than an oversight, so it recurs across the class,
        it survives quote-or-drop intact, and item-level validity cannot see it because the item is
        honestly marked. The rest of the reasoning is unaffected, and the case for case law as corpus
        is stronger than when it was written — the 2019 Amendment Act legislated most of the 2018
        judgment, so the judgments now also say which of their own dispositions are spent.

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

        Re-grounded 2026-09-16: the conclusion stands and every premise has changed. India Code's
        machine interfaces are not disabled — the host moved to indiacode.gov.in and both are live
        (@4sxgog), and India Code never carried judgments anyway. main.sci.gov.in and
        digiscr.sci.gov.in no longer resolve at all. What now argues against a scraper is better
        than cost: the two search surfaces that would make one worthwhile, scr.sci.gov.in and
        judgments.ecourts.gov.in, are captcha-gated, and lawcorpus.fetch.browser refuses a challenge
        rather than defeating it. So hand-curation is principled here and not merely economical.
        Retrieval, by contrast, is now deterministic: api.sci.gov.in serves a judgment at
        /supremecourt/&lt;year&gt;/&lt;diary&gt;/&lt;diary&gt;_&lt;year&gt;_Judgement_&lt;date&gt;.pdf, unauthenticated, and it
        extracts clean. The hand work is selection — one diary number and date per judgment — after
        which the URL is refetchable, which is what a manifest needs.

    Validity is recorded per provision, not per instrument = decision:
      id: 4sxgog
      why: >
        The id-law-kit manifest carries validity per corpus item, which is the right granularity
        for an instrument that is wholly in force or wholly repealed. The Aadhaar Act is neither:
        one section was struck down, others were read down, and the 2019 Amendment Act rewrote
        parts in response. Recording validity for the Act as a whole would be useless — it would
        read "amended" and hide the thing that matters.

        Recorded 2026-07-31, with no corpus and no sight of the publisher's record format: chose a
        provision-level validity overlay in this repo, keyed to the item, rather than pushing the
        complexity into the shared schema for four repos that do not need it. Tradeoff named at the
        time: an overlay is a second place that can drift from the manifest, and cite.py must
        consult both to print an honest banner.

        Revised 2026-09-16, on evidence the original could not have had. taxonomy.md §3 offers two
        ways to get the grain right and prefers the first — make the provision the item — and the
        July decision took the second only because the first looked expensive. It is not:
        indiacode.gov.in publishes each section as its own DSpace item, with the current as-amended
        text in dc.identifier.section_page_note and the amendment provenance in a separate
        dc.identifier.section_footnote. 69 items for the Aadhaar Act, 44 plus a schedule for DPDP,
        one query per act_id, no splitting step and therefore no splitting bug. So the preferred
        option is taken on the Act layer, and the overlay shrinks rather than disappears.

        Three costs of the revision, recorded rather than engineered away. (1) The delegated layer
        gets no such split — RULE, REGULATION and NOTIFICATION items carry no text field at all,
        only a PDF bitstream — so validity there stays per instrument and the grain is mixed and
        declared rather than uniform. (2) dc.identifier.repealed is false for all 69 sections
        including the omitted §57, so the publisher's own validity flag is unusable and is wired to
        nothing; the registry says so, because a reader who finds the field will otherwise assume we
        missed it. (3) Judicial validity is nowhere in India Code, which records what Parliament did
        and never what a court did — so the overlay survives, for the four live rows the 2019
        Amendment Act did not legislate away (§2(d), §7, PMLA Rule 9(a)(17), the DoT circular of
        23-3-2017), two of which are instruments this corpus does not hold.

        Rejected: keeping the overlay at provision scale anyway, for uniformity with the delegated
        layer. Uniformity is not the thing being bought — a second copy of the statute book is, and
        the publisher already maintains one.
      children:
        The overlay is the source of judicial validity, and the manifest is derived from it = decision:
          id: q3dsvsrl
          why: >
            @4sxgog's named cost is drift: two places recording validity, disagreeing silently. With
            the provision as the item both places can now express the same fact — a section item's
            validity column can hold read-down directly — which makes the drift concrete rather than
            theoretical. Chose to make sources/judicial-overlay.tsv the single authored record, and
            to have tools/harvest.py derive the manifest's validity and validity_note from it, so
            the manifest is output and cannot disagree with its input. tools/verify.py re-checks the
            derivation, so a hand-edited manifest fails rather than wins.
            Rejected: authoring validity in the manifest and treating the overlay as commentary.
            That is the shape that drifts, and it cannot say anything at all about the two struck
            instruments this corpus does not hold. Tradeoff: a section's judicial status is no
            longer editable in the place a reader will first look for it.

        India Code's amendment footnotes are provenance, never corpus text = decision:
          id: gogceltr
          why: >
            The publisher separates current text (section_page_note) from amendment provenance
            (section_footnote), and that separation is the strongest single argument for the
            revision above — it is what makes a section item structurally immune to the footnote
            hazard that UIDAI's own annotated edition carries, where the omitted §57 is reproduced
            verbatim in quotation marks four lines below a heading bearing its number, retrievable
            by quote-or-drop and invisible to item-level validity. Concatenating the two fields into
            one stored item would import that hazard by hand in a milder form, since footnotes here
            quote the superseded words. So the footnote field is read — it is what names the amending
            instrument in every validity_note — and written to sources/amendment-footnotes.tsv as
            provenance, and never to corpus-acts/.
            Rejected: storing footnotes as separate corpus items, which would make superseded
            wordings quotable behind their own banner. That is defensible, and is what
            ccpa/corpus-regs does for 30 superseded wordings; it is refused here because this repo
            exists for one case where a retrievable superseded wording produced a confidently false
            statement of Indian law.

    The delegated layer's text is the publisher's own extraction, gated by ours = decision:
      id: yt6p5u4j
      why: >
        Every India Code PDF is stamped with a diagonal "India Code" watermark whose glyphs
        pdftotext emits as separate fragments — and in layout mode, which is lawcorpus.pdf's
        default, they do not merely pollute the text, they reorder it: in the 2021 Regulations the
        words "Official Gazette" are emitted before the sentence that ends in them, so the phrase is
        not contiguous and greps to zero. Non-empty, plausible, and wrong, which is the dangerous
        shape. Each India Code item also carries a TEXT bundle — the publisher's own pdfbox
        extraction — which is watermark-free: 0 glyph-only lines against 140 in our own raw-mode
        extraction and 27 reordered lines in layout mode. Chose the publisher's text as the stored
        corpus text, with our own layout=False extraction run as an independent control: the two
        must agree on the provision inventory before anything is stored, and a disagreement aborts.
        Rejected: stripping the watermark from our own extraction. The glyph tokens are e, od, aC,
        di and In, none safely removable by a blind filter — In opens a sentence in this very
        corpus. Rejected also: trusting the publisher's text alone, which leaves one source
        vouching for itself. Tradeoff: the stored text is a derivative we did not produce, so a
        publisher-side extraction bug is ours too, which is what the control is for.
      children:
        The publisher's text is preferred and does not win = decision:
          id: ah7ssl3s
          why: >
            The control found a publisher-side bug on its first run, which is the case @yt6p5u4j
            named and did not say what to do about. India Code's TEXT bundle for the Digital
            Personal Data Protection Rules, 2025 stops at exactly 100,000 characters, mid-sentence,
            with no marker; our own extraction of the same PDF runs to 119,414 and ends with the
            printer's colophon. Every other document here has a publisher text 1.01–1.27 times the
            length of ours, because ours loses lines to the watermark, so a publisher text shorter
            than ours is the signature of a truncated tail. Chose to fall back to our own extraction
            for that instrument, stored with a quotation_qualifier saying so, rather than refusing an
            instrument we can read or storing a truncated one. In layout=False the watermark sits on
            lines of its own instead of displacing the body, so the fallback copy is polluted and not
            disordered, which is the difference that makes it quotable at all.
            Rejected: refusing the document. The DPDP Rules are the operative instrument for the
            whole DPDP layer and nothing else carries their text. Rejected also: a length check
            alone — an inventory comparison was written first, and it cannot see this failure,
            because a schedule at the end of an instrument restarts its numbering and contributes no
            heading the body has not already used.

        Soundness is measured in windows, and where the measurement runs out, a person reads = decision:
          id: nppnqlxn
          why: >
            The mojibake guard was first written over whole-document rates, and it refused S.O.
            2927(E) — a commencement notification whose English is perfect. Its Hindi is set in a
            legacy non-Unicode Devanagari font, so it extracts as Latin rubbish and drags the
            document's averages to exactly where a genuinely corrupt document sits. A gate that
            refuses good documents is a gate somebody turns off, which `method.md` §6 already
            records from thai.py. So the measurement is windowed: a document passes if 70% of its
            60-token windows read as English, and a document below that is stored only if every
            phrase it was declared for sits inside a window that does read. Clean documents run
            0.73–1.00; the damaged ones run 0.29, 0.32 and 0.50.
            And then the limit, which is the part worth recording: the 2013 foreign-CA Regulation
            passes that test and is still not quotable. Its damage is letter substitution that keeps
            the vowels, the case and the word count — "Certifling", "ceftificates", "ln these
            regulations", "ofaudit" — so the sentence we want is intact and its neighbours are
            wrong in ways no statistic tried here can see. An out-of-vocabulary rate against the
            corpus's own words separates it whole-document (0.62 against 0.15–0.40) and collapses
            around the passage that matters (0.195 against a sound document's 0.200). Chose to keep
            that number as a reported diagnostic and to refuse the document **by hand**, in
            candidates.py, with the reason written where the refusal is. Rejected: tuning a
            threshold until it excluded this one document, which would produce a gate that passes
            everything it has not already seen.

    The next_section chain is a shape oracle, and it is blind where it matters most = decision:
      id: 6v3ks6eo
      why: >
        India Code authors a per-section next_section pointer. It is a publisher-authored linked
        list and therefore independent evidence of completeness — the Indian analogue of Japan's
        TOC/ArticleRange, and a fourth free shape oracle for the kit's collection. Walking it from
        §1 reaches §59 in 59 steps with no broken link, which reads as a clean bill of health. It is
        not one: all ten lettered insertions have a null next_section and none is ever pointed at.
        3A, 8A, 23A, 33A–33F and 50A are simply off the chain, and §3 points straight at §4. A
        harvester validating on the walk alone would be missing the ten sections the 2019 Amendment
        Act inserted — which include the whole adjudication and appeal machinery — and would see
        nothing wrong. Chose to use the chain for what it proves, that the base-numbered spine is
        gapless and in order, and to pair it with order_number and a declared count, so that an
        insertion is caught by an oracle that can see one.
        Rejected: discarding the chain as unreliable. It is not unreliable, it is partial, and an
        oracle whose blind spot is known and written down is worth more than no oracle.

    Redistribution rests on Copyright Act §52(1)(q), split three ways, and not on GODL = decision:
      id: 5lrzngtg
      why: >
        The README named GODL-India and Copyright Act §52(1)(q) as the two candidate bases. GODL is
        irrelevant: its own scope clause covers "shareable non-sensitive data … generated using
        public funds", which is NDSAP datasets, and India Code marks nothing GODL. And §52(1)(q)
        does not do what the US "edicts of government" doctrine does, which is what a single-basis
        framing silently assumes: §2(k) and §28 make an Act of Parliament a Government work in
        copyright until 2076, and §52(1)(q) then frees it only conditionally. Chose to state the
        basis per layer — judgments free under (q)(iv), Gazette rules and notifications free under
        (q)(i), Acts free under (q)(ii) only "together with any commentary thereon or any other
        original matter" — and to say plainly in the README that a bare corpus of Act text arguably
        does not satisfy that condition, rather than resolve it by optimism. The repo is private, so
        nothing turns on it today; a decision to publish has a real question to answer.
        Rejected: asserting the condition is met because findings/ exists. It probably is met, and
        "probably" is not a licence.
