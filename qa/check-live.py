"""Verify a DEPLOYED site, not the local files.

Everything else in qa/ checks the source. This checks what a visitor actually
gets, because the failures that matter here only happen after deployment:

  - a page 404s on the host that works locally (directory-style URLs need
    cleanUrls off and trailingSlash on, which is easy to get wrong)
  - the Content-Security-Policy header is silently dropped, and the font link
    goes back to media="print" — a failure with no error message anywhere
  - canonical tags still point at the old domain, which tells search engines
    the real page lives somewhere unreachable
  - the stylesheet or script 404s

  python qa/check-live.py https://<deployment>.vercel.app

Exits non-zero if anything fails, so it can gate a deploy.
"""
import re
import ssl
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(2)
BASE = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].rstrip("/")
CTX = ssl.create_default_context()

PAGES = [
    "/", "/net-billing/", "/before-you-buy/", "/systems/",
    "/agriculture/", "/projects/", "/faq/", "/about/", "/contact/",
    "/ur/", "/ur/net-billing/", "/ur/before-you-buy/", "/ur/systems/",
    "/ur/agriculture/", "/ur/projects/", "/ur/faq/", "/ur/about/",
    "/ur/contact/", "/404.html",
]
ASSETS = ["/assets/css/site.css", "/assets/js/site.js",
          "/assets/img/og-card.png", "/sitemap.xml", "/robots.txt",
          "/manifest.webmanifest"]

problems = []
warnings = []


def get(path, method="GET"):
    req = urllib.request.Request(BASE + path, method=method,
                                 headers={"User-Agent": "shahzad-qa/1.0"})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=25) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()
    except Exception as e:                                   # noqa: BLE001
        return 0, {}, str(e).encode()


print(f"checking {BASE}\n")

# --- 1. every page must be reachable --------------------------------------
print("pages")
first_headers = None
for p in PAGES:
    st, hd, body = get(p)
    if st != 200:
        problems.append(f"{p} -> HTTP {st}")
        print(f"  {p:<26} {st}  FAIL")
    else:
        if first_headers is None:
            first_headers = hd
        print(f"  {p:<26} {st}  ok   {len(body):>7,} B")
print()

# --- 2. assets ------------------------------------------------------------
print("assets")
for a in ASSETS:
    st, hd, body = get(a)
    if st != 200:
        problems.append(f"{a} -> HTTP {st}")
    print(f"  {a:<34} {st}  {len(body):>7,} B")
print()

# --- 3. a nonsense URL must 404, not 200 ----------------------------------
st, _, _ = get("/this-page-does-not-exist-qa-check/")
if st != 404:
    problems.append(f"unknown URL returned {st}, expected 404")
print(f"unknown URL returns {st} (want 404)  "
      f"{'ok' if st == 404 else 'FAIL'}")
print()

# --- 4. the security headers ---------------------------------------------
print("headers (from the first page fetched)")
want = {
    "Content-Security-Policy": "script-src",
    "X-Content-Type-Options": "nosniff",
}
for h, needle in want.items():
    val = (first_headers or {}).get(h)
    if not val:
        problems.append(f"header {h} is not being sent")
        print(f"  {h:<28} MISSING  FAIL")
    else:
        ok = needle in val
        if not ok:
            problems.append(f"{h} does not contain {needle!r}")
        print(f"  {h:<28} present  {'ok' if ok else 'unexpected value'}")

csp = (first_headers or {}).get("Content-Security-Policy", "")
if csp:
    if "unsafe-inline" in csp.split("script-src")[1].split(";")[0]:
        problems.append("script-src allows unsafe-inline")
    m = re.search(r"script-src[^;]*'sha256-([^']+)'", csp)
    print(f"  script-src hash       {m.group(1)[:24] + '…' if m else 'NONE'}")
print()

# --- 5. canonicals must match the deployment host ------------------------
print("canonicals")
st, _, body = get("/")
home = body.decode("utf-8", "replace")
canon = re.search(r'<link rel="canonical" href="([^"]+)"', home)
if not canon:
    problems.append("home page has no canonical")
    print("  home page has no canonical  FAIL")
else:
    href = canon.group(1)
    host_ok = href.startswith(BASE)
    if not host_ok:
        problems.append(f"canonical points at {href}, not {BASE}")
    print(f"  {href}")
    print(f"  {'matches the deployment host' if host_ok else 'DOES NOT MATCH'}"
          f"  {'ok' if host_ok else 'FAIL'}")

st, _, body = get("/net-billing/")
nb = body.decode("utf-8", "replace")
canon2 = re.search(r'<link rel="canonical" href="([^"]+)"', nb)
if canon2 and not canon2.group(1).startswith(BASE):
    problems.append(f"net-billing canonical -> {canon2.group(1)}")
    print(f"  /net-billing/ canonical: {canon2.group(1)}  FAIL")
print()

# --- 6. the font link must be able to become media=all -------------------
# A blocked onload handler leaves media="print" and the fonts never load.
# The attribute in the source should be "print" — the swap is done by
# site.js — but the page must also load site.js, or nothing flips it.
if 'src="/assets/js/site.js"' in home:
    st, _, _ = get("/assets/js/site.js")
    if st != 200:
        problems.append("site.js did not load — the font swap would never run")
    print(f"site.js reachable ({st}) — font swap will run")
else:
    problems.append("site.js is not referenced on the home page")
    print("site.js NOT referenced  FAIL")
print()

# --- 7. no stray placeholder domain --------------------------------------
stray = 0
for p in ["/", "/ur/", "/sitemap.xml"]:
    _, _, b = get(p)
    stray += b.decode("utf-8", "replace").count("shahzadsolar.pk")
if stray:
    problems.append(f"{stray} reference(s) to the non-resolving shahzadsolar.pk")
print(f"references to the non-resolving shahzadsolar.pk: {stray}  "
      f"{'ok' if stray == 0 else 'FAIL — run qa/set-domain.py'}")
print()

print("=" * 62)
if problems:
    print(f"{len(problems)} PROBLEM(S):")
    for p in problems:
        print(f"  - {p}")
    sys.exit(1)
print("DEPLOYMENT OK — pages, assets, headers and canonicals all correct")
