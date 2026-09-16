# Indian statutes are copyright works until 2076, and s. 52(1)(q) frees them three different ways

**Question:** on what basis, if any, could this corpus be redistributed?
**Corpus:** `corpus-acts/` at 2026-09-16 — the Copyright Act, 1957 ss. 2, 17, 28 and 52, harvested as provisions.
**Answer, short:** there is no Indian analogue of the US "edicts of government" doctrine. An Act of the Indian Parliament is a copyright work of the Government until the end of 2076. Section 52(1)(q) then exempts reproduction, and it does so in **three different ways for three different layers** — judgments freely, Gazette rules and notifications freely, and Acts only on a condition that a bare corpus may not meet. The repo is private, so nothing turns on this today; a decision to publish has a real question to answer, and the README states it rather than resolving it.

Every quotation below is verbatim from the corpus and reproducible with `tools/check-quotes.py`.

## 1. A statute is a Government work, and Government works carry copyright

`corpus-acts/COPYRIGHT-1957-s2`, in force:

> (k) Government work means a work which is made or published by or under the direction or control of-- (i) the Government or any department of the Government; (ii) any Legislature in India; (iii) any court, tribunal or other judicial authority in India;

`corpus-acts/COPYRIGHT-1957-s28`, in force:

> 28. Term of copyright Government works.
> In the case of Government work, where Government is the first owner of the copyright therein, copyright shall subsist until 1[sixty years] from the beginning of the calendar year next following the year in which the work is first published.

So the Aadhaar Act, published in 2016, is in copyright until the end of **2076**, and the Supreme Court's judgments are Government works too. `utah-id-law` rests on the proposition that an edict of government carries no copyright at all; **that proposition is not Indian law**, and copying its reasoning into this repo would have been the error `method.md` §8 warns about in so many words.

Everything therefore depends on the exception.

## 2. Section 52(1)(q), whole, because the answer is in its last clause

`corpus-acts/COPYRIGHT-1957-s52`, in force:

> (q) the reproduction or publication of-- (i) any matter which has been published in any Official Gazette except an Act of a Legislature; (ii) any Act of a Legislature subject to the condition that such Act is reproduced or published together with any commentary thereon or any other original matter; (iii) the report of any committee, commission, council, board or other like body appointed by the Government if such report has been laid on the Table of the Legislature, unless the reproduction or publication of such report is prohibited by the Government; (iv) any judgment or order of a court, tribunal or other judicial authority, unless the reproduction or publication of such judgment or order is prohibited by the court, the tribunal or other judicial authority, as the case may be;

Read it against this repo's three layers and it says three different things.

| Layer in this repo | Clause | What it permits |
|---|---|---|
| `corpus-judgments/` — the Puttaswamy judgments | (q)(iv) | Reproduction, unconditionally, unless the Court prohibits it. Neither judgment carries a prohibition. |
| `corpus-delegated/` — regulations, rules, commencement notifications | (q)(i) | Reproduction, unconditionally. These are Gazette matter, and the carve-out in (q)(i) is for "an Act of a Legislature", which they are not. |
| `corpus-acts/` — 121 sections of five Acts | (q)(ii) | Reproduction **only** "together with any commentary thereon or any other original matter". |

Three observations follow, and the third is the one a single-basis framing cannot express.

**(q)(i) does real work for the layer that is largest by volume.** Every instrument in `corpus-delegated/` is Gazette matter, so the whole delegated layer is free of the condition that binds the Act layer. That is the opposite of the intuition that delegated legislation is somehow more encumbered than primary legislation.

**(q)(iv) is why case law is cheap to carry and expensive to obtain.** This repo treats judgments as corpus rather than commentary (`this.i` @meihbh), and the copyright position is the least of the difficulties in doing so.

**(q)(ii) is a condition on the act of publication, not a property of the text.** The same 121 section files are freely reproducible in one arrangement and arguably not in another. A repository of Act text with a manifest is a reproduction of Acts of a Legislature and nothing else; the same repository with `findings/` in it is a reproduction "together with … commentary thereon". **This repo is plainly in the second case** — five findings that analyse the provisions they quote is original matter about those Acts, not decoration — but the point is that it is so *because of a choice*, and a future strip-down to "just the corpus" would change the answer without changing a single file of Act text.

That is an unusual constraint and it is stated rather than resolved. It is also, read charitably, a coherent policy: the drafters made the Gazette free and made the statute book free to anyone adding something to it, which is a different bargain from the American one and not obviously a worse one.

## 3. GODL-India is not the basis, and naming it was a category error

The README named the Government Open Data Licence – India alongside s. 52(1)(q). GODL is a MeitY instrument offered by a data publisher over data it publishes under the National Data Sharing and Accessibility Policy, and its own scope clause reaches "shareable non-sensitive **data** … generated using public funds". Statutes are not NDSAP datasets, and India Code marks nothing on its site GODL. It is not that GODL says something unhelpful about legislation; it does not address legislation at all.

*(GODL's text is not in this corpus — it is a Gazette notification of 10 February 2017 that no finding here quotes — so the sentence above is a characterisation and not a quotation, and it is the reason this repo now names one basis instead of two.)*

The instructive part is not that the README was half wrong. It is that **naming the right instrument was not enough.** Section 52(1)(q) is the right instrument, and stopping at "s. 52(1)(q) covers government material" would have produced a confident and wrong licence statement, because the clause splits three ways and one of the three carries a condition. `asia-id-strategy.md`'s lesson — read the licence, do not name it from memory — has a corollary: reading it means reading to the end of the clause.

## What this finding does not establish

- Whether a court would agree that `findings/` satisfies (q)(ii). It is an inference from the words, it is the kind of inference that wants a lawyer, and it is load-bearing only if this repo is published.
- Anything about s. 52(1)(r), which separately frees translation of an Act into an Indian language on conditions. It would matter if the Hindi texts were ever carried, and they are not.
- Whether the Supreme Court has ever prohibited reproduction of a judgment under (q)(iv). The clause contemplates it; nothing in this corpus says it has happened here.
