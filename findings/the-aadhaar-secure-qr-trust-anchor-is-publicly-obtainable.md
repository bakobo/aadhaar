# A foreign verifier can obtain and validate UIDAI's trust anchor, because the credential lives inside India's general PKI

**Question:** Q10 — can a verifier outside the issuing jurisdiction obtain the trust anchor for a state-issued credential?
**Corpus:** `corpus-acts/`, `corpus-delegated/` at 2026-09-16, plus certificates fetched and parsed on this box the same day.
**Answer, short:** **yes, and it is the first yes in this programme.** UIDAI's current Aadhaar Secure QR signing certificate validates to `CN=CCA India 2022`, the root the Controller of Certifying Authorities publishes on a public web page, using only material fetched from Oregon today. The structural reason matters more than the fact, and it generalises: **ask which PKI a signature lives in before asking whether its anchor is published.** Two gaps are real and are recorded — UIDAI no longer publishes the leaf, and no rotation policy exists anywhere.

The legal half of this finding is quote-or-drop over the corpus. The cryptographic half is an **artefact oracle**: not a document saying the chain validates, but the chain validating, here, today.

## 1. Why the anchor cannot be private: the regulation defines the signature by reference to the IT Act

`corpus-delegated/AOV-REGS-2021`:

> (ib) “Digital signature” means digital signature as defined in clause (p) of sub-section (1) of Section 2 of the Information Technology Act, 2000 (21 of 2000);

and `corpus-acts/IT-2000-s2`:

> (p) "digital signature" means authentication of any electronic record by a subscriber by means of an electronic method or procedure in accordance with the provisions of section 3;

That one cross-reference decides the whole question. The signature on an Aadhaar Secure QR is not a UIDAI-defined artefact in a UIDAI-defined trust scheme; it is an **Information Technology Act signature**, which means it is made by a subscriber of a Certifying Authority licensed by the Controller under that Act, and it is validated the way every electronic signature in Indian law is validated. **A state that puts its identity credential inside its general electronic-signature PKI cannot keep the anchor private without breaking the PKI**, because the whole of Indian e-commerce depends on those roots being fetchable.

So the question "will UIDAI let a foreigner have the trust anchor" is the wrong question. Nobody had to decide it. The anchor is the Root Certifying Authority of India's, and it is published for reasons that have nothing to do with Aadhaar.

## 2. The chain, built from material fetched today

`openssl verify -CAfile CCAIndia2022.cer -untrusted <(CA + sub-CA) <leaf>`:

```
uidai_offline_publickey_2026.cer: OK
```

| Depth | Subject CN | Issuer CN | Key | Validity | Serial |
|---|---|---|---|---|---|
| 3 root | `CCA India 2022` (O=India PKI) | self | RSA 4096 | 2022-02-02 → **2042-02-02** | 762433EB…FE117 |
| 2 CA | `(n)Code Solutions CA 2022` (O=GNFC Ltd) | CCA India 2022 | RSA 2048 | 2022-03-16 → 2032-03-16 | 51D38C2A…03798 |
| 1 sub-CA | `(n)Code Solutions Sub-CA for DSC 2022` | (n)Code Solutions CA 2022 | RSA 2048 | 2022-04-01 → 2032-03-14 | 6214B505 |
| 0 leaf | `DS Unique Identification Authority of India 06` (O=UNIQUE IDENTIFICATION AUTHORITY OF INDIA) | (n)Code Solutions Sub-CA for DSC 2022 | RSA 2048 | 2026-02-03 → 2029-02-03 | 624C4F50 |

Every certificate is RSA with `sha256WithRSAEncryption`; there is no ECDSA anywhere in the chain. The leaf's KeyUsage is Digital Signature and Non-Repudiation, both critical, and its SHA-256 fingerprint is `E0:30:4B:9E:61:EE:36:40:EC:DD:AE:2D:B4:B6:17:F2:E2:67:8F:57:DB:C2:82:6C:2F:86:AC:5C:04:F2:77:DF`, identical in two independent third-party repositories.

**UIDAI signs with an ordinary commercial document-signer certificate.** (n)Code Solutions is a CA run by Gujarat Narmada Valley Fertilizers and Chemicals Limited. This is not a bespoke sovereign trust list and not a closed scheme; it is the same PKI a company uses to sign an invoice.

## 3. The gap: UIDAI no longer publishes the leaf, and the absence is real

The QR payload carries a raw signature and not the signer's certificate, so a verifier must obtain the leaf out of band. UIDAI used to publish it and does not now:

```
https://uidai.gov.in/images/uidai_offline_publickey_26022021.cer   404   (153 bytes of HTML)
https://uidai.gov.in/images/authDoc/uidai_auth_prod.cer            404
positive control, same host and path prefix:
https://uidai.gov.in/images/Aadhaar_Act_2016_as_amended.pdf        200   560,458 bytes
```

The control fires, so this is a real absence rather than a blanket 404 on legacy paths — `method.md` §4 applied to a certificate instead of a search result. The leaf used above came from a third-party verifier's repository, pinned to a commit. **So the anchor is public and the leaf is vendored**, which is a strange posture: the hardest part of the trust story is solved by the Controller of Certifying Authorities and the easiest part is left to whoever wrote the open-source reader you happen to be using.

One incidental finding, worth a line because it is funny and because it bites: the sub-CA had to be fetched over **http**, because `https://www.ncodesolutions.com` fails with `unable to get local issuer certificate`. The web TLS certificate of the CA that signs UIDAI's signing certificate does not itself chain on this box.

## 4. Revocation: CRL yes, OCSP no

```
http://www.ncodesolutions.com/repository/ncodeca22subca1.crl   200   176,776 bytes  application/x-pkcs7-crl
http://ocsp.ncode.in/nCodeSolutionsSubCAforDSC2022             TCP connect timeout (103.20.105.158)
```

The CRL serves. The OCSP responder resolves in DNS and does not answer this box; whether it is down or filtered from this egress is unestablished. A verifier outside India should plan on CRL.

## 5. Rotation: there is no policy, and there is an observable habit

Searched for and not found: on UIDAI's live site (both candidate pages 404), and in the 2021 Regulations, where `certificate` occurs **zero** times against controls of `shall` at 154 and `Authority` at 234. So the instrument that constitutes the credential says nothing about the lifetime of the key that signs it.

What four recovered UIDAI document signers *show*:

| CN | Issuing CA | Validity |
|---|---|---|
| `DS … INDIA 4` | e-Mudhra Sub CA Class 3 for Document Signer 2014 | 2017-06-08 → 2020-06-07 |
| `DS … INDIA 05` | (n)Code Solutions CA 2014 | 2021-02-26 → 2024-02-27 |
| `DS … India 05` | (n)Code Solutions Sub-CA for DSC 2022 | 2024-02-21 → 2026-02-16 |
| `DS … India 06` | (n)Code Solutions Sub-CA for DSC 2022 | 2026-02-03 → 2029-02-03 |

A roughly three-year lifetime, a CA migration from e-Mudhra to (n)Code Solutions, and a successor issued **before** the incumbent expires — 6 days of overlap at the 2024 handover, 13 days at the 2026 one. **That is a convention, not a policy**, and the difference is operational: a verifier that hard-codes one certificate breaks silently about every three years with under two weeks' notice, and has nothing to read that would have warned it.

Two traps in that table. The CN index went **4 → 05 → 05 → 06**, reusing `05` across the CA migration, so **the common name does not identify a signer** — a verifier must key on serial or fingerprint. And there is a 264-day gap between the 2020 expiry and the 2021 issue that no recovered certificate covers; whether one exists is unestablished.

## What this finding does not establish

- **That certificate `…06` is the key currently signing Secure QR payloads.** The cryptography proves it is a genuine India-PKI document-signer certificate with a UIDAI subject. Confirming it signs today's QRs needs a real QR sample run through a verifier, which nobody here has. This is the single most load-bearing gap in the finding and it is one sample wide.
- The QR's byte layout or signature padding. Third-party readers agree; no primary source was reachable; nothing here rests on it.
- Anything about the Paperless Offline e-KYC XML's signature, which third-party accounts put at RSA-SHA1 and no retrievable UIDAI document confirms.

## Why this is the programme's headline

Across six Phase 0 spikes, no jurisdiction answered Q10 yes. India does, and not because India is more generous — because of where it put the signature. `asia-id-strategy.md` §8.1's headline, *the obstacle is admission and not cryptography*, survives and India is its cleanest instance: the cryptography is genuinely open, the admission gate is genuinely closed (see the finding beside this one), and for once the two come apart cleanly enough to see both.

The transferable move is the heuristic at the top. Every one of these questions was asked as "does the issuer publish its trust anchor", which is a question about an organisation's disposition. **"Which PKI does this signature live in" is a question about architecture, and it has an answer you can look up.**
