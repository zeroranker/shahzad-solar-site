"""Rewrite every absolute URL in the site to a real domain.

The site currently carries https://shahzadsolar.pk/ in 127 places — canonical
links, hreflang alternates, og:url, the sitemap and robots.txt. That domain
does not resolve (verified: NXDOMAIN on both apex and www, against a control
lookup of fesco.com.pk that resolves normally).

Shipping it as-is would be an active SEO liability, not a neutral placeholder:
a canonical tag tells a search engine "the real version of this page is over
there", and "over there" does not exist. Search engines would then either
ignore the canonical or consolidate the pages onto an unreachable host.

So the domain has to be the one the site is actually served from.

  python qa/set-domain.py https://shahzad-solar-site.vercel.app
  python qa/set-domain.py https://www.example.com --check

Rewrites, in both languages and the sitemap/robots:
  canonical, og:url, twitter:url, hreflang alternates, sitemap <loc>, sitemap
  alternates, and any absolute internal link.

It refuses to guess: the replacement must be an https URL, and --check reports
what would change without writing.
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

CURRENT = "https://shahzadsolar.pk"

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(2)

new = sys.argv[1].rstrip("/")
check_only = "--check" in sys.argv

if not new.startswith("https://") and not new.startswith("http://localhost"):
    print(f"refusing: '{new}' is not an http(s) URL")
    sys.exit(2)

targets = sorted(
    [p for p in pathlib.Path("site").rglob("*.html")]
    + [pathlib.Path("site/sitemap.xml"), pathlib.Path("site/robots.txt")]
)

total = 0
touched = []
for p in targets:
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8")
    n = text.count(CURRENT)
    if n:
        total += n
        touched.append((p.as_posix(), n))
        if not check_only:
            p.write_text(text.replace(CURRENT, new), encoding="utf-8")

print(f"{'would rewrite' if check_only else 'rewrote'} {total} reference(s) "
      f"across {len(touched)} file(s)")
print(f"  {CURRENT}  ->  {new}\n")
for path, n in touched[:12]:
    print(f"  {n:>3}  {path}")
if len(touched) > 12:
    print(f"  ... and {len(touched) - 12} more files")

# confirm nothing is left behind
left = sum(
    p.read_text(encoding="utf-8").count(CURRENT)
    for p in targets if p.exists()
)
print(f"\nreferences to the old domain remaining: {left}")
if left:
    print("  (this is expected in --check mode; run without --check to apply)")
else:
    print("  the site now self-references its real host.")
