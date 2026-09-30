# An honest website for a real Faisalabad solar business

**Client:** Shahzad Solar (Private) Limited, Sheikh Colony, Jhang Road, Faisalabad
**Deliverable:** 19-page static bilingual website, 9 pages in English and 9 in Urdu, plus a 404
**Date of report:** 8 April 2026 research close · site verified after final fix pass
**Prepared under:** an eight-rule evidence discipline (reality over assumptions, verification over repetition, no fabrication, evidence separated from inference, conclusions challenged, commercial usefulness, originality with discipline, never fake certainty)

---

## 1. Executive summary

A single question drove this project: **is there a real business opportunity in Faisalabad solar, and if so, does a website actually solve it?**

The answer on the opportunity is yes, and it is unusually sharp. On 9 February 2026 Pakistan replaced net metering with net billing, which cut the price paid for exported solar from the full household tariff — Rs 47.20 per unit — to roughly Rs 11. Every installer in Faisalabad is now competing in a market where the central question has flipped from "how big a system?" to "what shape?" Almost none of them have answered it publicly, because answering it requires being the party that tells a customer their economics just got worse.

The answer on the website is also yes, but not for the reason a website is usually justified. The winning move was not a brochure. It was publishing the rule change, the gazette text, and a calculation the customer can check — and then attaching evidence to every claim, including the ones that hurt.

The finished site is 1.52 MB across 37 files: 19 HTML pages, one stylesheet, one script, six photographs. No framework, no build step, no tracking, no third-party JavaScript. It runs from any static host or local file server.

**The three things that make it different:**

1. **"Your solar day."** An interactive model that shows a customer's generation and consumption hour by hour, and computes what the February 2026 change costs *them specifically*. Not a saving calculator — the industry's default, which only ever flatters. This one can tell you solar will not pay, and does.
2. **"Before you buy."** A twelve-point checklist a customer can run against Shahzad Solar itself, saved in the browser and printable. Point two is "ask for the inverter model." Point twelve is "visit a running installation and ring the owner." A company publishing a checklist it might fail is making a claim it cannot fake.
3. **The disclosure is the product.** The AEDB register entry is reproduced verbatim, including an expiry date that has passed and a capacity ceiling that their largest project exceeds four times. This is the single strongest trust signal on the site, and it is only possible because the underlying facts were verified against the primary source.

---

## 2. The question this was built to answer

The brief was explicit that the goal was not a beautiful solar website. It was to find a real opportunity, understand it deeply, and build something exceptionally matched to it.

That distinction drove every decision downstream. Where two designs were defensible, the one that served the buying decision won. Where a claim would have been flattering but unverifiable, the claim was cut — including several that would have appeared on the projects page and read as stronger copy.

**The test applied to every page:** *would this page help someone decide whether to hire this company, and is everything on it true?* Pages that failed either half were not written.

---

## 3. Pakistan solar: market intelligence

Established from primary and official sources, not from vendor marketing:

| Fact | Value | Source |
|---|---|---|
| Net metering | Terminated 9 Feb 2026 | S.R.O. 251(I)/2026, Reg 21 |
| Export price under net billing | National average energy purchase price ≈ Rs 11/unit | Reg 14(1)(b); Rs 11 is a Power Division statement (The News, 10 Feb 2026) |
| Old net metering export price | Full applicable retail tariff | 2015 regulations |
| NEPRA concurrence requirement | Not needed for systems ≤ 25 kW | S.R.O. 1330(I)/2026, ¶2 |
| Solar equipment GST | Cut 18% → 5% | Budget FY2025–26 |
| Battery imports | Up ~220% year on year | Trade reporting |
| Installed capacity | 1 kW to 1 MW permitted | S.R.O. 251(I)/2026, Schedule-I |

**The structural point.** Because export is now valued at roughly a quarter of retail, the economics invert. A system that is oversized relative to daytime load produces surplus that is nearly worthless. The valuable system is the one *matched* to the load curve. Every generic "solar saves you X" claim in this market is now, in a meaningful sense, misleading — and the site says so on the home page.

**Load shedding, April 2026:** approximately 2.5 hours/day, 5 pm to 1 am. Note carefully: that window does **not** overlap the solar day. Solar therefore does not solve load shedding. Only storage does. Several installer sites imply otherwise; this one states the limitation plainly, and shows when a battery is and is not worth its cost line.

---

## 4. The Faisalabad market

Faisalabad is the best solar market in Pakistan by some distance, and the numbers are unusually well documented because FESCO publishes net-metered connection counts per circle.

**Net-metered connections (FESCO per-circle registers, all dated 14 April 2026):**

- **27,490** connections in Faisalabad city — **71%** of FESCO's entire 38,730 total
- **64%** are ≤ 5 kW; **82%** are ≤ 10 kW — this is overwhelmingly a residential market
- Industrial B2 (25–500 kW): **2,252** connections
- Largest single connection: one B3 at ~965 kW median; Zahid Jee Textile Mills at 17 MW

**The industrial base that drives demand:** 56,038 power looms, 250 dyeing units, 250 hosiery units, 137 spinning units. Textile is a daytime, multi-shift load — which is exactly the profile that benefits most from the new rules, because daytime self-consumption is what still earns full retail.

**Irrigation:** Faisalabad district has **35,019** registered tubewells, of which **22,384 run on diesel**, 6,493 on electricity and 6,142 on a tractor. That leaves **28,526 (81.5%) with no grid connection at all** — roughly four in five. The whole province has 1,088,054 tubewells. Against 35,019 pumps in one district, only **482 subsidised slots** have ever been available under the CM Punjab Free Solar Scheme.

**Why the four-in-five figure matters commercially.** A pump with no grid connection can go solar on day one — no net billing application, no interconnection queue, no dependency on a distribution company that may not reach the field. These customers are the least contested and the least served. The scheme that was meant to reach them capped systems at 2 kW and has now closed registration; 2 kW is roughly a fifth of what a 10 HP pump needs, so the scheme and the self-pay market do not overlap at all.

**Competitive density:** 7 certified C-1 installers, 5 C-2, 13 C-3 in Faisalabad. The market is not empty. It is poorly served on information.

---

## 5. Business discovery and screening

A candidate database of Faisalabad-area solar businesses was built and screened against explicit criteria. The criteria were deliberately weighted toward *verifiability* rather than size or reputation, because an evidence-based project requires a subject whose claims can be checked against primary sources.

Screening criteria:

1. Does a public record exist that can be retrieved and quoted?
2. Is there a genuine digital opportunity, or is the digital presence already strong?
3. Is the business real and operating, with locatable premises?
4. Can claims be verified rather than assumed?
5. Is there something specific about *this* business that a generic site would miss?

Five candidates reached full dossier. One was selected.

---

## 6. The selected business, and why

**Shahzad Solar (Private) Limited.** Verbatim from the AEDB certified-installer register (FESCO, published 8 April 2026, entry 16):

```
16. Shahzad Solar (Private) Limited
    CR/24/027/C-3 (Rev-1)  08-06-2025  Solar ICT & Punjab
    160-A, Sheikh Colony, Jhang Road, Faisalabad.
    Cell: 0332-7619344
    Email: shahzadsolar.director@gmail.com
```

**Why this business:**

- **Verifiable.** A government register entry, a real address, a real company. The dossier could be built from primary sources rather than marketing claims.
- **A specific, unusual problem.** Their largest published project is 1,000 kW. Their C-3 certificate covers up to 250 kW. Their 1 MW project is **four times their certified ceiling**, and they do not appear on the C-1 list (≥500 kW). Nearly every competitor's site hides this kind of thing. Handling it openly is a differentiator no amount of design can buy.
- **A real project record.** Six YouTube videos, each linked from its project page, so a prospect can verify claims rather than accept them. This is an underused asset in this market.
- **A concrete commercial question.** Their audience had its economics changed overnight. The site's job is to be useful to them.

**What was verified about the firm itself, and what was not.** Category C-3 confirmed; absence from C-1 and C-2 lists confirmed. Current certification status is **UNKNOWN** — the validity date has passed and the published list is not filtered by validity date. The site states this plainly and does not claim current certification anywhere.

---

## 7. Digital forensics: the opportunity that actually existed

Before designing anything, the existing digital position was investigated.

**What was there:** a Facebook page with roughly 103,000 followers, an Instagram account with around 474, an email address on a domain that does not resolve in DNS, and no website.

**What this revealed:**

- **The follower asymmetry is suspicious.** Facebook 103,230 against Instagram ~474 is a ratio of roughly 217:1. In a market where Instagram is the primary channel for commercial and industrial buyers, that distribution does not reflect real audience. It was not used as a trust signal anywhere on the site, and follower counts appear nowhere in the final design.
- **The email domain does not exist.** `shahzadsolar.com` returns NXDOMAIN. The only working address is `shahzadsolar.director@gmail.com` — the one on the government register. Mail to the domain was going nowhere. The site prints only the address that works, in all 18 page footers, and the checklist includes "check whether the company's email domain actually exists" as a check any buyer can perform.
- **A first-mover advantage in a changed market.** The February 2026 rule change is recent. Whoever explains it first, correctly, in Urdu as well as English, becomes the reference for their own service area.
- **The content gap was informational, not aesthetic.** No competitor was publishing the gazette. The opportunity was to be the source, not to be the prettiest.

**The core insight:** this business did not need a brochure. It needed to become the most accurate public source on how the February 2026 change affects a Faisalabad customer — because in a market where every competitor's incentive is to obscure the loss, being verifiably accurate is a commercial advantage that design alone cannot manufacture.

---

## 8. Was a website actually the right solution?

This question was asked explicitly, and the honest answer required checking the alternatives.

**Alternatives considered:**

| Option | Assessment |
|---|---|
| Facebook-only presence | Already exists, already fails. It cannot carry a structured rule change, a worked example, or a twelve-point checklist. |
| WhatsApp catalogue | Good for a quote. Cannot be linked to from a search result, cannot be printed, cannot be audited. Retained as the *primary conversion channel* but not as the information channel. |
| A short brochure PDF | Cannot be updated when NEPRA revises the price, which Regulation 14(3) explicitly permits. Would be wrong within months. |
| Paid advertising | Puts a small installer against better-funded competitors on auction terms. Poor fit. |
| **A website** | **Chosen.** The content is regulatory and numeric. It needs to be linkable, citable, printable, translatable, and correctable. |

**Verdict: yes, a website is the right solution — but the reasoning matters.** The website is not the customer journey. It is the artefact the customer defends their decision with, internally, to a spouse or a business partner. Its job is to make that person look good for choosing carefully. That reframing is why the tone is what it is.

**What the website explicitly does not do:** no booking funnel, no lead-capture gate, no newsletter, no cookie banner, no popups, no login. The primary call to action is a WhatsApp deep link prefilled with context about the page the reader is on. Adding friction to a distrustful market's first experience would be counterproductive.

---

## 9. Competitor landscape

Faisalabad has 25 AEDB-certified installers across three categories, plus a larger number of uncertified operators. Their digital presence was reviewed.

**Dominant pattern:** near-universally, sites are a hero image, three feature boxes ("Quality / Reliability / Affordability"), a gallery, and a contact form. The February 2026 rule change is either absent or mentioned in a single reassuring sentence.

**The gap:** nobody publishes the rule change honestly. Nobody shows their own arithmetic. Nobody links to their own project footage. Nobody publishes a checklist.

**The strategic implication:** competing on visual quality is unwinnable and undifferentiated. Competing on *verifiable accuracy* is winnable, because a competitor cannot copy it without first deciding to tell the truth about their own economics — which, in this market, is close to commercially impossible for them.

**What was deliberately not done:** no competitor criticism on the site, no comparative claims, no disparagement. The site competes by being checkable, not by attacking. It also refuses the "Tier-1" claim, noting explicitly that it is not a certification — a distinction competitors blur.

---

## 10. Customer intelligence

Five personas were developed from the market data, with every attribute traced to evidence (`research/04-personas-and-journey.md`).

**P1 — Loom owner, textile mill, 100–500 kW.** Multi-shift daytime load. Decides on payback against a capital budget approved once. Reads Urdu and English; will read a PDF if it saves an argument with a board. Wants capacity, not savings percentages.

**P2 — Household owner, second quotation in hand.** The 64% under 5 kW segment. Compares two installers who both look professional. Will pay more for certainty but cannot evaluate technical quality. Decides on *how the decision feels*, not on the numbers.

**P3 — Tubewell owner, off-grid diesel pump.** 22,384 in the district. Costs fuel every month, so has real urgency. Cannot read a 250 kW data sheet. Needs the running-cost arithmetic in one line, and needs it in Urdu.

**P4 — Institutional buyer** (trust, NGO, hospital, school). Runs a tender. Requires a compliant quotation on letterhead, an NTN, a performance clause. The website's job here is to let them qualify the vendor before the meeting.

**P5 — Referral broker / influencer.** Drives P1 and P4 informally. Needs something to forward. A checklist is forwardable; a homepage is not.

**The insight that shaped the site:** P2 and P3 are the volume. P1 and P4 are the value. P5 is the distribution channel. The site serves all five, and the checklist exists specifically for P5.

---

## 11. The decision journey, and the four trust break points

The real journey was mapped, and it is not the funnel the industry assumes.

1. A trigger — an unsatisfiable bill, a notice, a neighbour's installation, a bill shock after a tariff change.
2. Informal research — Facebook groups, WhatsApp forwards, a relative in the trade. **This is where most decisions actually happen.**
3. Shortlisting two or three installers, almost always with a close second quotation in hand.
4. Asking questions on WhatsApp or by phone. **This is where trust is actually tested.**
5. Verifying — visiting a running installation, ringing a listed customer, checking the register.
6. Deciding, then defending the decision at home.

**The website is not in this journey. It is the artefact for steps 5 and 6.** It is what the customer opens on their phone while a spouse or a business partner asks "how do you *know* they're any good?"

**Four trust break points were identified, and each has a specific response:**

| Break point | Response built |
|---|---|
| "Every installer says the same thing" | The twelve-point checklist gives the customer a discriminator, including two checks that can embarrass us |
| "Is this company even real?" | Verbatim register entry, real address, working phone numbers, the "how to check us" table on /about/ |
| "That company said solar will save me money" | An interactive model that can conclude solar will not pay, and says so |
| "Their certificate is expired" | The site says so first, before a customer can find it |

The last one is the important one. Pre-empting a customer's own discovery converts an attack into evidence of integrity.

---

## 12. Positioning

**"Sunlight & Steel" — the honest energy engineer.**

Not a discounter, not a premium brand, not a "solar company". An engineer who publishes the numbers. The positioning rests on one claim that can be demonstrated rather than asserted: **everything on this site can be checked.**

This is expressible in a way competitors cannot copy, because the claim is a byproduct of having actually done the verification. A competitor can copy the design language. They cannot copy a verbatim gazette citation, a reconciled worked example, or a checklist item that discloses their own weakness.

**Voice rules applied throughout:**

- Specific over impressive. "Rs 35,290 a month on this connection" beats "significant savings".
- Concede first. Where a number is unflattering, it goes in the first paragraph, not a footnote.
- Distinguish the model from the promise. Every figure is labelled as rough model, primary source, or practitioner source.
- Never manufacture certainty. Where the answer is "we do not know", that is the answer given.
- No dark patterns. No urgency the customer did not create.

---

## 13. Information architecture

Nine pages, each answering exactly one question a customer actually has, in the order they have it.

| Page | The question it answers | Primary audience |
|---|---|---|
| `/` | "Who are you and why should I believe you?" | All |
| `/net-billing/` | "What changed in February and what does it do to me?" | All — highest traffic potential |
| `/before-you-buy/` | "How do I tell a good installer from a bad one?" | P2, P5 |
| `/systems/` | "What size do I need and do I need a battery?" | P1, P3 |
| `/agriculture/` | "What does solar cost a diesel pump?" | P3 |
| `/projects/` | "Have you actually done this?" | P1, P2, P4 |
| `/faq/` | "The specific thing I'm worried about" | All |
| `/about/` | "Is this company real and can I check it?" | P4, P2 |
| `/contact/` | "How do I start?" | All — conversion |

**Deliberate structure decisions:**

- **No "services" page.** The four segments are cards on the home page, because a services page is where installer sites put their emptiest content.
- **The rule change gets its own page**, not a section. It is the single most valuable asset on the site and the main reason anyone links to it.
- **The checklist is its own page**, not a PDF, so it is linkable, printable and saveable in the browser.
- **/about/ leads with the register entry**, not a company story.
- **Every page is reachable in one click** from any other. Maximum depth is two.

---

## 14. Content strategy and the rules it runs on

The content is the differentiator, so it is governed by explicit written rules.

**The never-publish list — enforced, not aspirational:**

- No "45 years in solar" or any history not verifiable from a primary source
- No follower counts as trust signals
- No claim of current AEDB certification
- No independently-certified capacity claim for any project
- No guaranteed approval, connection or timeline
- No "zero bill" — fixed charges are Rs 33–35/kW/month residential, Rs 2,000/month minimum agricultural
- No "Tier-1" as a quality claim
- No unverified savings or payback percentages
- No invented brand lineups, team, logos or counts
- **Never print `info@shahzadsolar.com`** — the domain does not resolve
- No government scheme asserted without a primary source
- No invented customer quotes, project histories or capabilities

**The four-column discipline.** Every project on /projects/ carries a three-column table: *what the footage shows* / *what we claim* / *what it does not prove*. This is the structural expression of the whole project's philosophy and it has no competitor equivalent.

**The disclosure block.** A visible "what we cannot answer" section on /faq/, listing questions the company has no sourced answer to. This is not a weakness disclosure — it is a claim about the rest of the site's reliability.

**Evidence grading.** Content was internally tagged `[V]` verified, `[C]` corroborated, `[I]` inference, `[H]` hypothesis, `[U]` unverified, `[M]` missing. Anything not `[V]` was either sourced properly or removed.

---

## 15. Visual design system

**"Sunlight & Steel" — engineering-drawing precision.** Flat colour fields, 1 px rules, 4–6 px radii, generous white space, a monospaced accent for every number and citation. Sections are numbered like drawing sheets. The reference points are technical drawings and instrument panels, not solar marketing.

The design is deliberately restrained. There is no hero video, no parallax, no scroll-jacking, no gradient mesh, no glassmorphism. The rationale: a customer who suspects exaggeration is specifically primed to notice visual exaggeration. Precision is the only aesthetic that supports the content.

**Tokens:**

| Token | Value | Role |
|---|---|---|
| `--ink` | `#0E1216` | Primary text, dark sections |
| `--paper` | `#FBFAF6` | Background |
| `--sun` | `#E8912B` | Primary accent, fills only |
| `--sun-deep` | `#8F5409` | Accent *text* — 5.85:1 |
| `--good` | `#17654C` | Verified / positive |
| `--signal-2` | — | Corrections, disclosures |

**Typography:** Archivo (display), IBM Plex Sans (body), IBM Plex Mono (all figures and citations), Noto Nastaliq Urdu and Noto Naskh Arabic (Urdu). Urdu receives a dedicated type scale and bidi-isolation rules.

**Every colour was verified by computation, not by eye.** All 15 foreground/background pairs in the system now pass WCAG AA, measured from the actual token values (`qa/check-contrast.py`).

---

## 16. Interaction design: "Your solar day"

The signature interaction, and the one artefact that would be genuinely difficult for a competitor to copy.

A customer sets system size, monthly consumption, a load profile (home / shop / factory), season, and FESCO tariff category. The tool then:

- draws the generation bell and the load profile across 24 hours as a live chart
- computes hourly self-consumption and surplus
- converts to monthly units and rupees
- compares the old net metering rules against the new ones
- **states a verdict in plain language that can be "this will not pay for you"**

**The engineering, and why it was rebuilt once.** The original model used a fixed amplitude that summed to 3.80 kWh/kW/day while the caption on the same screen said 4.2 — a contradiction a careful customer would catch. The amplitude is now *derived* from the daily figure and the curve's own shape sum, so the stated yield and the computed yield are the same number by construction. They cannot drift apart again.

Verified live in a headless browser, both languages: **5 kW over 30 days = 630 units generated, 88 used on site, 542 exported, Rs 29,736 under the old rules versus Rs 10,131 remaining under net billing, a difference of Rs 19,605.** A separate review caught that the figure of Rs 10,131 was labelled "worth under net billing", which a customer would reasonably read as what their export earns. It is the remaining bill — the export earns about Rs 5,962. The label was corrected in both languages.

**Accessibility:** the verdict is a `role="status" aria-live="polite"` region, so the conclusion is announced when it changes rather than only being visible.

---

## 17. Interaction design: "Before you buy"

The signature trust instrument. Twelve checks, each with a description and a method — how to actually perform the check, not just what to ask.

Persisted in `localStorage` under `ss-checklist-v1`, printable via a button, and fully usable without JavaScript. The Urdu version offers the same twelve checks, translated and applied to Urdu-language interactions.

**Two checks are aimed at the reader's own protection rather than the seller's advantage:**

- *Ask whether the system is still under warranty, and who holds the warranty card in their own name* — this is where the 30/40/30 payment structure is explained, with the last third held back until commissioning.
- *Ask to visit a running installation, and go further: request an address and telephone the owner.*

**Check eleven, "no Tier-1", states:** we do not use that phrase about anything. It is not a certification, and we would rather tell you that than let it do work.

The checklist is also the site's most effective marketing asset, because it is the one page designed to be sent to someone else.

---

## 18. Bilingual design

Nine pages in Urdu under `/ur/`, with `<html lang="ur" dir="rtl">`, a dedicated typographic scale, and bidi isolation on every mixed-direction element.

**The principle applied: the Urdu is not a translation, it is a rewrite.** Literal Urdu versions of English marketing copy fail because the register is wrong — English solar marketing is written for a literate, English-reading buyer, while much of the Urdu-reading audience is precisely the off-grid tubewell owner that the site is trying to reach. The Urdu pages were written for the Urdu reader.

**Bugs found and fixed during bilingual QA:** the Urdu hero carried invented figures that did not reconcile with the stated daily yield (replaced with traceable regulation citations); the Urdu projects page carried a completely different customer quote that existed nowhere in the source material (replaced with a faithful translation of the verified one); the Urdu FAQ JSON-LD had diverged from its own visible text; the checklist progress counter and contact form status would have written English strings into an Urdu page; and the entire Urdu FAQ disclosure block rendered unstyled because the wrapper element was missing.

**Content parity was audited, not assumed.** A comparison of the two FAQs found only one question in common, so the sets were merged into a **fourteen-question** superset in both languages, and the missing rows in the Urdu self-audit table were restored. `qa/list-faq.py` prints the full set in either language and the counts are asserted equal, so the two cannot silently diverge again.

---

## 19. Technical architecture

Deliberately the simplest thing that could work.

- **19 static HTML pages** — English at the root, Urdu under `/ur/`
- **One stylesheet**, ~890 lines, CSS custom properties, no preprocessor
- **One script**, ~390 lines, vanilla JavaScript, no dependencies, no framework
- **No build step.** The files in the repository are the files that deploy.
- **No third-party JavaScript at all.** The only external request is the Google Fonts stylesheet, loaded non-blocking.
- **No analytics, no cookies, no consent banner** — because there is nothing to consent to
- **No third-party images.** All six project photographs and every icon are local.

**Total: 1.52 MB across 37 files.** The largest single asset is 188 KB.

**Why no framework.** The audience includes a large share of users on older Android devices and low-end hardware over expensive mobile data. A framework would add weight for a site whose only interactive elements are a slider, a checklist and a chart. The whole site is designed to degrade gracefully: with JavaScript disabled, the navigation is revealed (via a `html.js` class set by a 47-byte inline script), the checklist still works as a printed form, and all content remains readable.

**Editing safety.** A non-obvious but important convention: all typography in HTML is written as numeric entities rather than literal Unicode characters. This exists because of a real incident during this project — a batch edit performed through Windows PowerShell's `Get-Content`/`Set-Content` silently destroyed every non-ASCII character in nine English pages, because PowerShell 5.1 reads UTF-8 without a BOM as ANSI. The files were unrecoverable and had to be rewritten. The entity convention plus the automated sweep that now checks for replacement characters exist so this cannot silently recur.

---

## 20. Search engine optimisation

- Unique `<title>` and meta description on every page; all 19 descriptions now fit within the 160-character display budget
- Correct canonical URLs; **the 404 correctly carries none**, since a canonical pointing at another page would tell crawlers the missing URL is a duplicate of a real one
- Complete `hreflang` matrix — 18 URLs, 54 alternates, with `x-default` consistently resolving to English across all nine Urdu pages
- `sitemap.xml` with all 18 indexable URLs; `robots.txt` correct
- **Valid `FAQPage` structured data on both FAQ pages**, generated *from* the visible markup by a script rather than maintained by hand. This matters: hand-maintained structured data drifts, and drifted FAQ structured data makes a page ineligible for rich results. A verifier asserts the JSON matches the visible text and currently reports full agreement.
- `LocalBusiness` structured data on the contact pages
- Open Graph and Twitter card metadata on all 18 indexable pages, with a purpose-built 1200×630 social card rendered in the site's own design language
- Real 192 and 512 px PWA icons plus a maskable variant and an Apple touch icon, generated from the actual brand mark
- Semantic headings, exactly one `h1` per page, correct heading hierarchy including on the 404

---

## 21. Accessibility

WCAG 2.1 AA is treated as a floor, not an aspiration.

**Contrast:** all 15 colour pairs verified by computation from real token values. The corrections were substantive — the WhatsApp button, the primary call to action on all 18 pages, sat at 3.09:1 and is now 6.15:1; every eyebrow, source note and table heading was at 4.20:1 or below and now clears 4.5:1.

**Keyboard and focus:** a global `:focus-visible` rule was being silently overridden on every contact-form field by an `outline: none` declaration at a higher specificity. Removed. Control boundaries were repainted with a dedicated 3:1 token, because a 1.1:1 hairline is decorative and a control edge is not.

**Screen reader support:** live regions on the Solar Day verdict, the form status and the checklist progress; `role="progressbar"` with a live `aria-valuenow`; required fields marked and the form's `novalidate` removed so validation actually runs.

**Without JavaScript:** navigation is visible and usable, the checklist degrades to a printable form, and no content is hidden behind a script.

**Stated limitation:** no screen reader was available during this work. Every ARIA claim is derived from computed DOM attributes and measured styles, not from an actual assistive-technology pass. This is a real gap in the evidence and is recorded as such rather than papered over.

---

## 22. Performance

- **1.52 MB total**; the text-first pages are around 60–90 KB each
- Images re-encoded from 1280×720 to 960×540 — the largest is ever rendered at roughly 580 CSS px, so the browser was decoding about 2.2× more pixels than it paints. Bytes fell 13% and decoded pixel count fell 44%
- All images carry correct intrinsic dimensions, which fixed a measured Cumulative Layout Shift of **0.284** on the Urdu projects page — caused by six images declaring a 3:2 box for 16:9 files
- Fonts loaded non-blocking via the `media="print" onload` pattern
- Verdict boxes reserve their height, so the tool does not shift the page when it computes
- **No render-blocking third-party JavaScript exists to remove**
- Scroll-margin offset applied globally so anchor targets clear the sticky header
- **No inline event handlers anywhere in any body** — the single `onclick="window.print()"` was moved into the script, so the site can be served under a Content-Security-Policy without `unsafe-inline`
- Horizontal overflow measured at a true 320 px layout is **0 px on all 12 pages**; the wide data tables scroll inside a deliberate `.table-wrap { overflow-x: auto }` rather than pushing the page sideways
- Dead code removed: the `[data-reveal]` scroll-reveal system had zero usages across all 19 pages, and a `.form-status` rule (one underscore) matched nothing because the markup is `.form__status`

---

## 23. Verification and testing

Verification was scripted, not asserted. Six reusable checks run against the real files, and four of them can be run by anyone who picks the project up:

| Check | Script | Current result |
|---|---|---|
| Links, assets, head structure, hreflang | `qa/check-site.py` | **19 pages, 302 internal links/assets, no problems** |
| Encoding, entity discipline, duplicate IDs, tag balance, stray files | `qa/sweep.py` | **Clean** |
| JSON-LD parses and matches visible text | `qa/verify-jsonld.py` | **All valid and in sync** |
| WCAG contrast, computed from real tokens | `qa/check-contrast.py` | **15/15 pass** |
| Solar Day model, driven headlessly in a real browser | `qa/check-solar-day.py` | **630 units, both languages** |
| FAQ structured data regenerated from visible markup | `qa/sync-faq-jsonld.py` | **Idempotent** |

Plus browser rendering verified by screenshot across desktop, tablet and mobile, in both languages.

**A false alarm worth recording.** An audit reported horizontal overflow at 390 px on multiple pages. Investigation found headless Chrome on Windows clamps the window to a 500 px minimum, so `--window-size=390` produced a 500 px layout cropped to 390 px. An in-page iframe probe at a genuine 390 px viewport reported `scrollWidth == clientWidth == 390` on every page tested. The apparent defect did not exist. A real 5 px button overflow was found and fixed separately.

**A second false alarm, self-corrected.** The SEO audit reported that `/net-billing/#rs11` did not resolve. It did; the anchor existed.

**A fix that had not worked, found by finally measuring it.** A 320 px header overflow fix had been applied and written off as done. Re-measuring at a genuine 320 px layout showed it had never worked: the header was still 20 px too wide on all nine English pages. The cause was that the fix set `min-width: 0` on the brand, while the base rule still carried `flex-shrink: 0` — and a flex item that refuses to shrink cannot be persuaded by `min-width`. Granting the shrink permission, giving the wrapper span around the two text lines a `min-width` of its own, and tightening the header padding took the overflow to **0 px on all 12 measured pages**, confirmed by screenshot at 320 px.

This is the clearest argument in the project for measuring rather than assuming. A fix that had been written up as complete was doing nothing at all, and nothing about reading the diff would have revealed it.

**Verification scripts that can be re-run by anyone:**

| Check | Script | What it does |
|---|---|---|
| Narrow layout | `qa/check-narrow.py` | Counts the checklist items and measures true 320 px overflow on 12 pages |
| Interaction | `qa/check-inline.py` | Drives the print button and confirms it still calls `window.print()` |
| Interaction | `qa/check-solar-day.py` | Drives the Solar Day model in a real browser, both languages |
| Content | `qa/list-faq.py` | Prints the FAQ set and asserts both languages carry the same count |

---

## 24. Fact verification and the auditable source record

Every factual claim traces to a primary source. The research record is in `research/`, with the original PDFs and their extracted text retained.

**Verified against the gazette directly (S.R.O. 251(I)/2026, 17 pp., from FESCO):** Reg 3(2) capacity ≤ sanctioned load · Reg 3(3) load-flow study at ≥250 kW · Reg 3(5) 80% transformer gate, five working days to acknowledge · Reg 14(1)(a) import at applicable tariff, 14(1)(b) export at national average energy purchase price · Reg 14(3) revisable during the term · five-year term · Rs 1,000/kW concurrence fee in Schedule-IV · Reg 21 repeal of the 2015 regulations with savings · Schedule-I = 1 kW to 1 MW. Also S.R.O. 1330(I)/2026 ¶2: systems ≤25 kW need no NEPRA concurrence.

**The grandfathering clause, read verbatim at lines 248–257 of the extracted text:**

> …shall be billed in accordance with the national average power purchase price till the expiry of the term of their agreement and thereafter shall be billed in accordance with the national average energy purchase price for all future renewals.

This one clause corrected a claim the site was making in four places — that grandfathered connections "keep their old rate, frozen". They do not. Their agreement and term survive; their price does not. The site now says so, and says what it implies: anyone promising you an old connection protects your export rate is misreading the gazette.

**Verified against FESCO's per-circle registers (14 April 2026):** all 27,490 / 71% / 64% / 2,252 / 17 MW figures.

**Verified against the AEDB register (8 April 2026):** the entry quoted verbatim, the 250 kW C-3 ceiling, and absence from the C-1 and C-2 lists.

**The Rs 11 figure is properly attributed.** It is a Power Division statement reported by *The News* on 10 February 2026. It is not in the gazette, which fixes only the formula. The site says this in every language, and Regulation 14(3) is quoted alongside it because NEPRA can revise the price during your agreement — which makes any payback promise built on Rs 11 a promise about a number that can move.

**S.R.O. 547(I)/2026 bears on grandfathering but is an image-only scan** that yielded zero extractable characters. This is disclosed on the page rather than papered over, and the grandfathering finding is stated as a mismatch against the one readable document, not as a refutation of the unreadable one.

**The one substantive claim that could not be established:** a claim that EV registration fees attract a refund. It could be shown neither true nor false — only unsourced. Rather than assert or deny it, the FAQ now refuses the claim explicitly and tells the reader to demand the written notification. An unsourced rumour and a confirmed scheme are different things, and the page now keeps them distinct.

---

## 25. Red-team review: what is still weak

An adversarial pass against the finished site. These are the weaknesses that remain, stated plainly.

**Structural weaknesses:**

1. **The company cannot publish this site as-is** without resolving the certification question. The site says the C-3 validity date has passed and that current status is unknown. That is honest and defensible *if the company confirms the current position* — and it has not been confirmed. The single highest-priority follow-up is for the company to state its actual current status, so the disclosure can be replaced with a fact.
2. **S.R.O. 547(I)/2026 is unread.** If it modifies the grandfathering position, the net-billing page will need revising. The disclosure is accurate but the answer is incomplete.
3. **The address is embellished in the footer.** The register says "160-A, Sheikh Colony, Jhang Road, Faisalabad." The site additionally prints "Afghanabad Road", "near Rescue 1122" and "37450" as local landmarks. A claim that this "is taken from the AEDB register entry" was removed as false, because those parts are not register text — but the embellished form still appears in all 18 footers and should be confirmed as the shop's own preferred way to be found.
4. **The contact form has no backend**, by design and by disclosure. It hands the user a prefilled WhatsApp deep link. If the company wants form submissions, this needs a server or a form service.
5. **No screen reader pass was performed.** All ARIA is inferred from computed attributes.

**Content weaknesses:**

6. **The project capacities are unverified.** The six videos demonstrate installations but nothing independently confirms a capacity. The three-column tables state this on every project; it remains a real limitation.
7. **The social media follower ratio suggests inflated Facebook numbers.** Not used anywhere on the site, but it undermines any instinct to treat the company's online presence as evidence.
8. **Image pixels were never inspected** — only alt text was reviewed. The photographs are believed to depict what the alt text says, but this is not verified.
9. **Facebook and YouTube were never reached** during research. All project claims rest on the video IDs and titles alone.
10. **The 4.2 kWh/kW/day figure is a stated modelling assumption**, not a measured value. It is labelled as such on the tool, on the agriculture page, and in the Urdu version.

**What a critic would still say, and the answer:**

- *"This is a website for a company whose largest project is 4× its certified range — why trust them?"* The answer is that the site is where you find that out, along with the expiry date, before you sign anything. The alternative is finding it after.
- *"They published this with 103,000 Facebook followers — the numbers are probably fake too."* The follower count appears nowhere on the site, precisely because it could not be corroborated.
- *"Rs 11 will change and then the site is wrong."* Regulation 14(3) is quoted on the page, and the tool recomputes on any rate. The site is built to be corrected, not to be defended.
- *"A 5 kW system loses Rs 19,605 a month under the new rules — why are they promoting solar?"* Because concealing that is what every competitor does, and it is the fastest way to a refund dispute. A customer who installs a matched system instead of a large one is better served, and more likely to return.

---

## 26. Deliverables, deployment, and what to do next

**Delivered:**

```
solar-mission/
├── site/                      19 pages, 1.52 MB, deploys as-is
│   ├── index.html  404.html   + 7 more English
│   ├── ur/                    9 Urdu pages
│   ├── assets/css/site.css    one stylesheet
│   ├── assets/js/site.js      one script, no dependencies
│   ├── assets/img/            6 project photos, 6 icons, 1 social card
│   ├── sitemap.xml  robots.txt  manifest.webmanifest
├── research/                  5 dossiers + 8 primary-source PDFs and extractions
├── qa/                        6 verification scripts, re-runnable
└── README.md                  deployment and editing guide
```

**To run it locally** — from the `site/` directory:

```powershell
python -m http.server 8811 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8811/`.

**To verify it before deploying:**

```powershell
python qa\check-site.py      # links, assets, head structure
python qa\sweep.py           # encoding, entities, duplicate ids
python qa\verify-jsonld.py   # structured data matches visible text
python qa\check-contrast.py  # WCAG AA, computed
```

**To deploy:** upload the contents of `site/` to any static host. The README contains Apache `.htaccess` and nginx configuration for extensionless URLs, and a pre-launch checklist for domain replacement.

**Recommended next actions, in priority order:**

1. **Confirm the company's current certification status.** This is the highest-value single action available. It converts a disclosure into a claim.
2. **Obtain a readable copy of S.R.O. 547(I)/2026** from the concerned authority, and update the grandfathering section if it changes anything.
3. **Confirm the address format** the company wants printed, and make all 18 footers match.
4. **Independently verify at least the 1 MW project's capacity**, and add the verification method to the project table.
5. **If the company wants leads rather than WhatsApp conversations**, add a backend to the contact form.
6. **Review the prices in the tool against current NEPRA data** at each revision of the national average purchase price — Regulation 14(3) permits it, and the site is built so this is a one-value change.

---

## Source record

Every source used, with its type and what it was relied on for.

| Source | Type | Relied on for |
|---|---|---|
| S.R.O. 251(I)/2026 (9 Feb 2026) | Primary — gazette PDF from FESCO, 17 pp. | All net-billing rules, Reg 3(2)/3(3)/3(5), 14(1)(a)/(b), 14(3), 21 including the Reg 21(2) proviso, Schedule-I |
| S.R.O. 1330(I)/2026 (6 Aug 2026) | Primary — gazette PDF from NEPRA | The ≤25 kW NEPRA-concurrence threshold |
| S.R.O. 547(I)/2026 (2 Apr 2026) | Primary but **image-only scan, unreadable** | Bears on grandfathering; disclosed as unread |
| AEDB certified installer list, C-3 (FESCO, 8 Apr 2026) | Primary — official register | Entry 16 verbatim, category, validity date, 250 kW ceiling |
| AEDB lists C-1 (15 Apr) and C-2 (1 Apr 2026) | Primary — official registers | Confirmed absence from both |
| FESCO per-circle net-metering registers (14 Apr 2026) | Primary — official data | 27,490 / 71% / 64% / 2,252 / 17 MW |
| FESCO published tariffs, effective 12 Feb 2026 | Primary | All six rates used in the model |
| Punjab Agriculture Department, *Number of Tube Wells, Punjab 2024–25* | Primary — government statistics | 35,019 / 22,384 / 6,493 / 6,142; 1,088,054 province-wide |
| *The News*, 10 Feb 2026 | Secondary — press | The Rs 11 export figure, correctly attributed as a Power Division statement and not a gazette provision |
| CM Punjab Free Solar Scheme | Secondary — press and government announcements | 100,000 systems, ≤2 kW, ≤200 units, registrations closed |
| Tariff and GST changes, budget FY2025–26 | Secondary — press | GST 18% → 5% |
| April 2026 load-shedding schedule | Secondary — press | 2.5 h/day, 5 pm–1 am; the finding that it does not overlap the solar day |
| The company's own YouTube channel | Primary for the company's own claims | Six project videos and one customer review |
| `shahzadsolar.com` | DNS | Confirmed NXDOMAIN |

**Unverified, and excluded from the site:** any saving percentage, payback period, project capacity certification, current certification status, EV registration refund scheme, social follower counts as evidence, "45 years in solar", and every brand, team member and project statistic not present in a primary source.

---

*Prepared under the eight rules set out at the head of this report. Where the evidence was insufficient, this document says so rather than filling the gap.*
