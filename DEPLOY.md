# Deploying to Vercel

Everything is prepared. The only step that needs you is the Vercel login,
because it is an interactive browser flow tied to your account — I cannot
complete it on your behalf.

---

## 1. Log in (one command, browser opens)

```powershell
vercel login
```

Verify it took:

```powershell
vercel whoami
```

You should see your account name, not `Logged out.`

---

## 2. Point the site at the URL it will actually be served from

This step is not optional and not cosmetic.

The site currently self-references `https://shahzadsolar.pk` in 127 places —
every canonical tag, every `hreflang` alternate, `og:url`, and the whole
sitemap. **That domain does not resolve.** I checked: NXDOMAIN on the apex and
on `www`, against a control lookup of `fesco.com.pk` that resolves normally.

Shipping it that way would tell every search engine "the real version of this
page is at a URL that does not exist" — which is worse than having no
canonical at all.

So decide the domain first:

| Option | What to run |
|---|---|
| **Ship on the Vercel URL** (fastest, fine for a start) | `python qa\set-domain.py https://<your-project>.vercel.app` |
| **The company buys `shahzadsolar.pk`** and points it at Vercel | `python qa\set-domain.py https://shahzadsolar.pk` after the domain resolves |

Preview first, apply after — `--check` changes nothing:

```powershell
python qa\set-domain.py https://shahzad-solar-site.vercel.app --check
python qa\set-domain.py https://shahzad-solar-site.vercel.app
python qa\check-site.py
```

---

## 3. Deploy

```powershell
vercel --prod
```

Or connect the GitHub repo and let every push deploy — recommended, since it
means a fix is one `git push` away from being live:

```powershell
vercel link
vercel --prod
```

Then in the Vercel dashboard, **Settings → Git → connect `zeroranker/shahzad-solar-site`**.

---

## 4. Verify the deployment — do not skip this

```powershell
python qa\check-live.py https://<your-deployment>.vercel.app
```

This fetches the real deployed pages and checks the things that only break in
production:

- every page returns 200, and a nonsense URL returns 404 (not 200)
- the `Content-Security-Policy` header is actually being sent
- the canonical URL on each page matches the deployment host
- the Solar Day page's script and stylesheet return 200
- the Urdu pages and the sitemap are reachable

The CSP header is the one most likely to be silently dropped, and the font
link is the thing most likely to be silently broken by it. That combination
produces a site that looks fine in every screenshot and has lost its fonts for
every real visitor.

---

## What is already configured

`vercel.json` sets the output directory to `site/`, keeps directory-style URLs
(`/net-billing/`) working, serves `404.html` for unknown paths, caches
`/assets/*` for a year, and sends:

- `Content-Security-Policy` — `script-src 'self'` plus one SHA-256 hash for
  the single 45-byte inline script. No `unsafe-inline` for scripts.
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy` denying geolocation, microphone and camera

The policy is not decorative. `qa/check-csp-live.py` serves the real policy
locally and asserts the site still works under it, because the failure mode is
silent: a blocked inline handler leaves the font link at `media="print"`, the
web fonts never load, and nothing anywhere reports an error. That exact bug
was in this site until the test caught it.

---

## Troubleshooting

**"No Output Directory named `site`"** — you are in the wrong folder. Run from
`E:\harness\New folder\solar-mission`, the folder containing `vercel.json`.

**Deployment succeeds but styles are missing** — check the CSP header actually
arrived. If the host is not Vercel, this header comes from that host's config
instead; `vercel.json` is Vercel-specific.

**Fonts look like a fallback stack** — run `qa\check-csp-live.py` locally. If
it passes locally but not in production, the production host is dropping or
altering the `Content-Security-Policy` header.

**`shahzadsolar.pk` still appears in the canonical** — `qa\set-domain.py`
reports how many references remain. It must be 0.
