# 05 — Primary-source verification: certificates, gazettes, and what they actually say

**Compiled 30 September 2026.**
This file exists because two claims central to the website had to move from "reported" to
"verified against the primary document", and because one finding changed the site's central
argument. Evidence grade is stated per claim. Nothing here is inferred where a document could
be read.

---

## A. The finding that changed the brief

### A.1 What was found

FESCO publishes, on its own public site, the **official list of certified solar installers** under
NEPRA's AEDB (Certification) Regulations, 2021, split into three categories:

| List | Category | Published | Pages | PDF |
|---|---|---|---|---|
| C-1 | up to and above **500 kW** | 15-04-2026 | 50 | `FESCO_1776660301_...C-1 (15-04-2026).pdf` |
| C-2 | up to **500 kW** | 01-04-2026 | — | `FESCO_1776660385_...C-2 (01-04-2026).pdf` |
| C-3 | up to **250 kW** | 08-04-2026 | 50 | `FESCO_1776660420_...C-3 (08-04-2026).pdf` |

All three were downloaded from `fesco.com.pk/net_metering` and parsed. Text extraction succeeded on
all three (`research/raw/aedb-c*.pdf.txt`).

**Shahzad Solar appears in exactly one of the three lists.**

Verbatim, from `aedb-c3-2026-04-08.pdf.txt` lines 205–214:

```
16. Shahzad Solar (Private) Limited
    CR/24/027/C-3 (Rev-1)  08-06-2025  Solar ICT & Punjab
    160-A, Sheikh Colony, Jhang Road, Faisalabad.
    Cell: 0332-7619344
    Email: shahzadsolar.director@gmail.com
```

A programmatic search of the C-1 and C-2 lists for `shahzad` returned **no match**.

**Evidence grade: ✅ VERIFIED against a government-published primary source.**

### A.2 What this proves — and it is genuinely strong

1. **The company is a registered private limited company, not a trading name.** "Shahzad Solar
   (Private) Limited" with a Companies Registration Commission reference embedded in the
   certificate number (`CR/24/…`).
2. **It has held a formal NEPRA/AEDB installer certification.** Not a membership, not a
   self-assertion — a certificate issued under the AEDB (Certification) Regulations, 2021, published
   by the distribution company.
3. **The certificate was issued in 2024** (`CR/24/027/C-3`) and was current into June 2025.
4. **The registered address is 160-A Sheikh Colony, Jhang Road, Faisalabad** — an exact match for
   the premises of Shahzad Pumps & Electric Works, which independently confirms the group-entity
   relationship inferred in the dossier.
5. **There is a working, officially-published email address:**
   `shahzadsolar.director@gmail.com`. This is *not* the dead `info@shahzadsolar.com`.
6. **A third telephone number exists** — 0332-7619344 — distinct from the 0347/0337 numbers on
   their public posters.

None of this was available from any social-media or directory source. It came from a file the
utility publishes for the convenience of its own customers.

### A.3 What it raises — and this must go on the website

**Finding A.3.1 — The certificate's stated validity date has passed.**

The list records validity `08-06-2025`. It is unambiguous that the list itself was published
**08-04-2026**, roughly ten months *after* that date. The list is therefore **not filtered by
validity**, and reading it as "currently certified" is an error.

An independent structural check on the same dataset supports this: across the C-1 list, a large
majority of entries carry validity dates that have already passed (109 entries share an identical
`30-06-2026` date; further blocks expire in 2025, 2024 and 2023). An official list containing
largely lapsed entries cannot be read as a live register.

> **Therefore: as at 30 September 2026, Shahzad Solar's current certification status is UNKNOWN.**
> It was certified; the certificate on file expired 8 June 2025; it may since have been renewed,
> which we have not been able to confirm from any public source.

**Finding A.3.2 — The certification category does not cover the largest advertised project.**

Category C-3 covers facilities **up to 250 kW**. The largest project in Shahzad Solar's own
published video record is a **1 MW** plant — four times that ceiling.

The C-1 list (≥500 kW) does not contain Shahzad Solar. So on the public record, the firm's
certified scope does not extend to the capacity of its largest self-published project.

**Three innocent explanations exist, and we cannot choose between them from public data:**
- the 1 MW plant was executed with a C-1 partner firm subcontracting the DC/AC scope;
- the certificate has since been upgraded, consistent with A.3.1 being an unconfirmed renewal;
- the project capacity as stated in the video title is not accurate.

**Finding A.3.3 — The category that *is* on file is the one that matters commercially.**

C-3 (≤250 kW) is the category that covers Faisalabad's **volume** segment. Per FESCO's own
net-metering register, 64% of Faisalabad's net-metered connections are ≤5 kW residential and 82%
are ≤10 kW; 2,252 connections sit in industrial B2 at 25–500 kW. Shahzad Solar's certified scope
covers the 5–250 kW band, which is where the overwhelming majority of Faisalabad's *new*
connections will be formed after 9 February 2026.

### A.4 The decision this forces

Three options were considered:

| Option | Why rejected / chosen |
|---|---|
| Say nothing about certification | **Rejected.** Withholding a known, checkable fact is the exact behaviour this site exists to criticise. A buyer who finds the AEDB list and sees no mention will conclude the worst. |
| Claim "AEDB certified" on the About page | **Rejected — would be false.** It would be true for a period ending 8 June 2025 and unverifiable today. This is the single most tempting lie in the entire project and it is not available. |
| **Publish the certificate number, the category, the validity date, and the limits of all three** | **Chosen.** It is the one move a competitor cannot cheaply copy, and it is the argument of the whole site made concrete. |

A market in which 80 companies were named in a fraud inquiry, fake firms were used to launder
Rs 110 billion, and B-grade panels are sold as "Tier-1" is a market where **disclosure is the
product**. An installer that publishes its own certificate expiry date is doing something no
competitor is doing, and it cannot be undercut on trust because there is no lower number to
compete with.

**This is now the site's spine, not a footnote.**

---

## B. Regulatory claims — moved from press to gazette

Earlier drafts of the net-billing page rested on news reporting. All of it has now been checked
against the instruments themselves, downloaded from FESCO and NEPRA.

- `sro-251-2026-02-09.pdf` — 17 pages, full text layer, 35,032 characters extracted.
- `sro-1330-2026-08-06.pdf` — 1 page, 1,457 characters, downloaded from `nepra.org.pk`.
- `sro-547-2026-04-02.pdf` — **1 page, 0 characters. Image-only scan, no text layer. Unreadable.**

| # | Claim as published | Instrument | Citation | Grade |
|---|---|---|---|---|
| B.1 | Export is bought at the national average energy purchase price | SRO 251(I)/2026 | Reg. 14(1)(b), line 206: *"the kWh supplied by prosumer to the licensee, shall be billed in accordance with the national average energy purchase price."* | ✅ verbatim |
| B.2 | Import is billed at the applicable tariff | SRO 251(I)/2026 | Reg. 14(1)(a), line 204 | ✅ verbatim |
| B.3 | The Authority may revise that rate during the agreement | SRO 251(I)/2026 | Reg. 14(3), lines 215–216: *"shall be deemed incorporated in the agreement"* | ✅ verbatim |
| B.4 | Facility capacity may not exceed sanctioned load | SRO 251(I)/2026 | Reg. 3(2), line 62 | ✅ verbatim |
| B.5 | ≥250 kW requires a load-flow study via the licensee or a PEC-registered consultant | SRO 251(I)/2026 | Reg. 3(3), lines 66–68 | ✅ verbatim |
| B.6 | No application if DG on a transformer reaches 80% of rated capacity | SRO 251(I)/2026 | Reg. 3(5), lines 74–75 | ✅ verbatim |
| B.7 | Agreement term is five years | SRO 251(I)/2026 | line 141 and line 368 | ✅ verbatim |
| B.8 | One-time concurrence fee of Rs 1,000/kW | SRO 251(I)/2026 | line 496 | ✅ verbatim |
| B.9 | **The 1 MW ceiling** | SRO 251(I)/2026 | Schedule-I, line 276: *"capacity equal or greater than 1 kW but no more"* [than 1 MW]; and line 266, *"Distributed Generation Interconnection Agreement (1 kW to 1MW)"* | ✅ primary — **previously secondary only** |
| B.10 | The 2015 Net Metering Regulations are repealed, with savings for pre-existing agreements | SRO 251(I)/2026 | Reg. 21(1) line 245, Reg. 21(2) lines 247–251, Reg. 21(3) line 255 | ✅ verbatim |
| B.11 | ≤25 kW needs no NEPRA concurrence; the licensee approves instead | **SRO 1330(I)/2026**, 6 Aug | Para. 2: *"a prosumer having distributed generation facility of 25 kW or below capacity shall not be required to seek concurrence from the Authority and the concerned licensee shall accord its approval."* | ✅ verbatim, from NEPRA directly |
| B.12 | The 2 April 2026 amendment concerns grandfathering | SRO 547(I)/2026 | Two independent secondary sources state it **amends Regulation 21**, the savings/repeal clause. The gazette itself is an unreadable scan. | 🟡 corroborated, not verified |
| B.13 | Export is worth ≈ Rs 11 | Power Division statement, The News 10-02-2026 | The gazette fixes no number; it specifies the *formula*. | 🟡 corroborated |

### B.1 — Correction carried into the site

The widely repeated claim that **"tariffs jumped in February 2026" is not supported.** Checked
directly against FESCO's own two tariff schedules: variable rates were flat-to-falling — industrial
B2 *fell* 21.4%. What changed was the fixed-charge architecture. **The site does not repeat this
myth.** It is listed here so the claim is not silently reintroduced during a later edit.

### B.2 — The "about 26 working days" figure

Reg. 3 sets a statutory clock: acknowledge in 5 working days (line 70), complete or reject within
3 (line 72), initial review within 15 (line 79), reject within 3 of review (line 81), NEPRA
concurrence and connection letter in 7 each. **These are minimums for the licensee, not a typical
elapsed time, and a refusal resets the clock.** The site states the range and the failure modes,
not a single number.

---

## C. Still open — carried forward, not resolved

| # | Item | Status | Why it matters |
|---|---|---|---|
| C.1 | **SRO 547(I)/2026 full text** | ⬜ Unreadable | Image-only scan, no OCR available in this environment. It is the *grandfathering* instrument — the one that decides whether a 2 April 2026 applicant keeps old rates. Material. |
| C.2 | **Whether CR/24/027/C-3 was renewed** | ⬜ Not found | No public register of live certificates was located. FESCO's list is dated April 2026 and is not validity-filtered. **This is the single most important open item on the website and is presented as an open question, not resolved.** |
| C.3 | NEPRA's actual NAEPP determination | ⬜ Not found | The gazette names the price but no published determination was located. The Rs 11 figure is a ministry statement. |
| C.4 | SECP record for Shahzad Solar (Private) Limited | ⬜ Not attempted | Would confirm incorporation date, directors, filing status. Requires a paid search; the AEDB certificate is the public proxy. |
| C.5 | FESCO Category D agricultural tariff | ⬜ Not found | Needed for the tubewell page. The Rs 28.90 figure used on the site is from a practitioner source, not the schedule. |
| C.6 | Punjab diesel price, September 2026 | ⬜ Not found | "Over Rs 300/litre" is directional only. **The site does not state a specific diesel price.** |
| C.7 | Punjab Solar Tubewell Scheme 2026 status | 🟡 Corroborated | Only SEO sources. Flagged on the site as unconfirmed, with the official portal linked. |
| C.8 | Structural survey of Shahzad Solar's own site | ⬜ Does not exist | No published qualification claims are made anywhere on the website. |

---

## D. What the website is therefore obliged to do

1. **Not print `info@shahzadsolar.com`.** The domain is NXDOMAIN. Print
   `shahzadsolar.director@gmail.com` instead, because FESCO publishes it.
2. **Print the certificate number, category, validity date and status — including the lapse.**
3. **State that the 1 MW project exceeds the certified scope**, and state that we do not know why.
4. **Attribute the Rs 11 export figure to the Power Division, not to the gazette.**
5. **Publish the gazette citations** so a reader can check the site the way the site asks them to
   check a seller. The site must be auditable by the same standard it demands of others.
