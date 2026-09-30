"""Add og:image / twitter:image to every indexable page.

Every page already declared twitter:card=summary_large_image but supplied no
image, which is an invalid large-image card and degrades in every share
surface. This points all 18 at the one rendered card, and also adds the two
dimensions + alt text that Facebook and LinkedIn expect.

Run from the project root:  python qa/add-og-image.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path("site")
SITE = "https://shahzadsolar.pk"
IMAGE = f"{SITE}/assets/img/og-card.png"

TAGS = (
    f'<meta property="og:image" content="{IMAGE}">\n'
    f'<meta property="og:image:width" content="1200">\n'
    f'<meta property="og:image:height" content="630">\n'
    f'<meta property="og:image:alt" content="Shahzad Solar, Faisalabad &#8212; '
    f'look at the work before you decide.">\n'
    f'<meta name="twitter:image" content="{IMAGE}">\n'
    f'<meta name="twitter:image:alt" content="Shahzad Solar, Faisalabad &#8212; '
    f'look at the work before you decide.">'
)

# og:image must appear after og:url for most scrapers; twitter:* after that.
changed, skipped = [], []

for p in sorted(ROOT.rglob("*.html")):
    page = p.read_text(encoding="utf-8")

    if p.name == "404.html":
        skipped.append(p.as_posix())  # noindex, nothing to share
        continue
    if 'property="og:image"' in page:
        skipped.append(p.as_posix() + "  (already present)")
        continue

    m = re.search(r'^\s*<meta name="twitter:card"[^>]*>\s*$', page, re.M)
    if not m:
        skipped.append(p.as_posix() + "  (no twitter:card line)")
        continue

    new = page[: m.end()] + "\n" + TAGS + page[m.end():]
    p.write_text(new, encoding="utf-8")
    changed.append(p.as_posix())

print(f"updated {len(changed)} pages")
for c in changed:
    print("  ", c)
if skipped:
    print(f"skipped {len(skipped)}:")
    for s in skipped:
        print("  ", s)

# verify every indexable page now has the image
missing = []
for p in sorted(ROOT.rglob("*.html")):
    if p.name == "404.html":
        continue
    t = p.read_text(encoding="utf-8")
    if 'property="og:image"' not in t or 'name="twitter:image"' not in t:
        missing.append(p.as_posix())
print("missing og:image after run:", missing or "none")
sys.exit(1 if missing else 0)
