# Shahzad Solar — website handoff

A static, bilingual (English / Urdu) website for **Shahzad Solar (Private) Limited**, Faisalabad.

Everything here is plain files. There is no build step, no framework, no package manager, no
server-side code and no database.

---

## 1. What this is

| | |
|---|---|
| Pages | 19 static HTML files — 9 English, 9 Urdu, 1 bilingual 404 |
| Stylesheet | one file, `assets/css/site.css` |
| Script | one file, `assets/js/site.js`, vanilla, no dependencies |
| Images | 6 project photos, 5 PWA/app icons, 1 social card — all local |
| Third-party JavaScript | **none** (the only external request is the Google Fonts stylesheet, loaded non-blocking) |
| Total size | **1.52 MB across 37 files** |
| Build step | **none** |
| Runtime cost | **none** — any static host serves it |

The full project write-up — market intelligence, verification record, design
rationale and the red-team review — is in **[REPORT.md](REPORT.md)**.

## 2. Running it locally

```powershell
cd site
python -m http.server 8811 --bind 127.0.0.1
```

Then open <http://127.0.0.1:8811/>.

It must be **served over HTTP**, not opened as `file://`. The pages use absolute paths
(`/net-billing/`), which `file://` cannot resolve.

To check it also serves correctly for Urdu, visit <http://127.0.0.1:8811/ur/>.

### Validating after any change

```powershell
python qa\check-site.py       # links, assets, titles, canonical, hreflang, headings, tag balance
python qa\sweep.py            # encoding, entity discipline, duplicate ids, stray files
python qa\verify-jsonld.py    # structured data parses AND matches the visible text
python qa\check-contrast.py   # WCAG AA, computed from the real token values
```

Run all four from the project root. Current state: **19 pages, 302 internal links/assets, no
problems · sweep clean · JSON-LD in sync · 15/15 contrast pairs pass.** A fifth check,
`qa\check-solar-day.py`, drives the "Your solar day" model in a real headless browser and
asserts that 5 kW over 30 days still yields 630 units in both languages.

`sweep.py` is the one that matters most if you edit by hand. It detects U+FFFD replacement
characters, which is the signature of the PowerShell encoding trap described in section 6.

---

## 3. File layout

```
site/
  index.html                  English home
  net-billing/index.html      the February 2026 rule change
  before-you-buy/index.html   the 12-check buyer-protection checklist
  systems/index.html          system sizes, 1.0x vs 1.5x, process
  projects/index.html         five projects, each with footage links
  agriculture/index.html      tubewells, diesel maths, the closed subsidy
  about/index.html            the AEDB register entry, verbatim
  faq/index.html              14 questions + what we cannot answer
  contact/index.html          address, phones, form, WhatsApp
  404.html                    bilingual, links to all 18 pages
  ur/                         the same nine pages, dir="rtl" lang="ur"
  robots.txt
  sitemap.xml                 18 URLs, 54 hreflang alternates
  manifest.webmanifest        192/512 "any" + "maskable" icons
  assets/
    css/site.css
    js/site.js
    img/projects/*.jpg        6 photographs, 960x540
    img/icon-*.png            PWA and Apple touch icons
    img/og-card.png           1200x630 social card
    img/favicon.svg
```

---

## 4. Deploying

### Any static host (Netlify, Vercel, GitHub Pages, Cloudflare Pages, Hostinger, cPanel)

1. Upload the **contents of `site/`** — not the `site/` folder itself.
2. That is the whole process. There is nothing to compile.

### Apache / cPanel — required for clean URLs

The pages use extensionless paths (`/net-billing/`). Without a rewrite rule those 404.
Add to `.htaccess` in the site root:

```apache
DirectoryIndex index.html
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.+)/$ $1/index.html [L]
```

### Nginx

```nginx
location / {
  try_files $uri $uri/ $uri/index.html =404;
}
error_page 404 /404.html;
```

### Before going live — change these

- [ ] `sitemap.xml` — replace the placeholder domain with the real one
- [ ] Every page's `rel="canonical"` and `og:url` — same replacement
- [ ] `hreflang` `href` values — same replacement
- [ ] `robots.txt` — set the `Sitemap:` line to the real URL
- [ ] `manifest.webmanifest` — the `start_url`

Search every file for the placeholder before deploying:

```powershell
Select-String -Path site\**\*.html,site\*.txt,site\*.xml -Pattern 'example\.com'
```

---

## 5. Editing guide

### The one rule

**Never open a file under `site/` with PowerShell `Get-Content` / `Set-Content` / `Out-File`.**
Windows PowerShell 5.1 reads UTF-8 without a BOM as ANSI and writes it back mangled, which
destroys the Urdu text irrecoverably. Use a proper editor, or the `Write`/`Edit` tools.

If you have already done it, the file is corrupted. It cannot be repaired by re-saving.

### Typography

Every page uses typographic characters written as **numeric HTML entities**, so they survive
any editor round-trip:

| Character | Entity |
|---|---|
| em dash — | `&#8212;` |
| en dash – | `&#8211;` |
| multiplication × | `&#215;` |
| middot · | `&#183;` |
| copyright © | `&#169;` |
| right-to-left mark | `&#x200F;` |

**One deliberate exception:** inside `<script type="application/ld+json">` blocks the
characters are written literally, because script content is raw text — an entity there would
arrive at the parser as the six literal characters `&#8212;` inside the answer string.
`qa/sweep.py` knows this difference and will not flag either form.

### Adding a page

1. Copy the closest existing page as a starting point.
2. Give it a unique `<title>`, meta description and canonical.
3. Add `hreflang` alternates pointing at the English and Urdu equivalents.
4. Add the page to `sitemap.xml` with all three alternates.
5. Add it to the nav in **every** page of both languages.
6. Add it to the 404 page's link lists.
7. Run `python qa\check-site.py`.

### Changing the Solar Day model

All assumptions are named constants near the top of `site.js`:

| Constant | Meaning |
|---|---|
| `KWH_PER_KW_DAY` | daily yield per kW. **The bell's amplitude is derived from this**, so the number shown on screen and the number the model computes cannot drift apart. Changing this changes both. |
| `EXPORT_RATE` | Rs per exported unit. A Power Division estimate, not a gazette figure. |
| `RATES` | FESCO column D rates by category |
| `LOADS` | the three load shapes, normalised to their own peak |
| `SEASONS` | the summer/winter multiplier |

---

## 6. The editing rules this site runs on

These are not style preferences. The site's entire value proposition is that it publishes only
what it can substantiate, so breaking them destroys the reason it exists.

**Never publish:**

- "AEDB certified" or "مندرجہ مستند" as a current claim. The company appears in the register at
  **Category C-3 only** (≤250 kW), certificate date **08-06-2025**, and the published list is not
  filtered by validity, so the current status is **unknown**. The About page says this.
- `info@shahzadsolar.com` — that domain does not resolve. Use
  `shahzadsolar.director@gmail.com`.
- "Zero bill" anywhere. There are fixed charges (about Rs 33–35/kW/month; Rs 2,000/month minimum
  on an agricultural connection).
- Guaranteed approval, connection or timeline.
- Independently-certified capacity for any project. Project sizes are the company's own figures.
- Social follower counts as trust signals.
- Any year-count, anniversary or "since" claim.
- A diesel price. It changes every fortnight; a stale figure is worse than no figure.
- "Our certified range" in the present tense. The certificate date has passed, so the phrasing
  is "the range on our C-3 certificate". This distinction was applied across 9 places in both
  languages.
- Any figure attributed to a source that does not show it. In particular, the 22,384 tubewell
  figure comes from the Punjab Agriculture Department, **not** from FESCO's circle registers.

**Always carry the caveat with the Rs 11 figure.** It is a Power Division statement reported in
the press, not a number in the gazette. The gazette sets a *formula* and lets NEPRA revise it.

**When correcting something publicly**, correct it in public. The projects page already does this
for a residential rooftop that was previously described as a weaving factory.

---

## 7. Known open items

These are unresolved and are recorded so they are not mistaken for oversights.

| Item | Why it matters |
|---|---|
| Has `CR/24/027/C-3` been renewed since 08-06-2025? | Determines whether the company may describe itself as certified at all. The single highest-value unknown. |
| SRO 547(I)/2026 text | Retrieved as an image-only scan; never readable. It governs protection of existing connections. |
| NEPRA's actual NAEPP determination | Sets the real export rate in place of the Rs 11 estimate. |
| FESCO Category D agricultural tariff | Rs 28.90 is a practitioner source, not from FESCO's published schedule. The page says so and tells readers to use their own bill. |
| Punjab Solar Tubewell Scheme 2026 | No published status found, so the site says nothing about it. |
| SECP company record | Not retrieved. |
| FESCO head-office address | Unconfirmed. Not published. |
| The footer address form | The register says "160-A, Sheikh Colony, Jhang Road, Faisalabad." The footers also print "Afghanabad Road", "near Rescue 1122" and "37450" as local landmarks. The claim that this is taken from the register was removed because those parts are not register text — but the company should confirm this is the form it wants customers to follow. |
| No screen-reader pass | All ARIA was derived from computed DOM attributes and measured styles, not from an actual assistive-technology run. |
| Image contents | Alt text was written and reviewed; the pixels were never inspected. |
| Project capacities | Nothing independently confirms the 1 MW figure. The project tables state this. |

---

## 8. Browser support

Modern evergreen browsers. The site uses CSS custom properties, `grid`, `clamp()`, logical
properties, `<details>`, and `IntersectionObserver` with a graceful no-JS fallback.

No polyfills, no transpilation, no bundler.
