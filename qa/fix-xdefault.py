"""One-off: point x-default at the English URL on every Urdu page.

The nine Urdu pages declared x-default -> the Urdu URL, while sitemap.xml
declared x-default -> the English URL for all eighteen. Google expects one
consistent target. English is the right choice: it is the language a search
engine should fall back to for a user whose language it cannot identify.

Run from the project root:  python qa/fix-xdefault.py
"""
import pathlib
import re

ROOT = pathlib.Path("site")
PATTERN = re.compile(
    r'(<link rel="alternate" hreflang="x-default" href="https://shahzadsolar\.pk)'
    r'(/ur(?:/[a-z-]+)?/)?"'
)

changed = []
for p in sorted(ROOT.rglob("*.html")):
    original = p.read_text(encoding="utf-8")
    match = PATTERN.search(original)
    if not match:
        continue
    ur_path = match.group(2)
    if not ur_path:
        continue  # already pointing somewhere without /ur
    en_path = ur_path.replace("/ur/", "/", 1)
    text = original.replace(match.group(0), f'{match.group(1)}"{en_path}"')
    p.write_text(text, encoding="utf-8")
    changed.append(f"{p.as_posix()}  x-default -> {en_path}")

print("files changed:", len(changed))
for c in changed:
    print("  ", c)
