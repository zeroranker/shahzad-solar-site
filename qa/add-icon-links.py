"""Add the apple-touch-icon link to every page.

Without it iOS screenshots the top of the page and renders its own white
background behind the icon, so a share sheet or a home-screen bookmark shows a
half-bleed page instead of the mark. One link, no layout cost.

Run from the project root:  python qa/add-icon-links.py
"""
import pathlib

LINE = '<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">\n'
ANCHOR = '<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">\n'

changed = 0
for p in sorted(pathlib.Path("site").rglob("*.html")):
    t = p.read_text(encoding="utf-8")
    if "apple-touch-icon" in t:
        continue
    if ANCHOR not in t:
        print(f"  !! {p.as_posix()}: favicon link not found")
        continue
    p.write_text(t.replace(ANCHOR, ANCHOR + LINE, 1), encoding="utf-8")
    changed += 1

print("pages updated:", changed)

missing = [
    p.as_posix()
    for p in sorted(pathlib.Path("site").rglob("*.html"))
    if "apple-touch-icon" not in p.read_text(encoding="utf-8")
]
print("missing:", missing or "none")
