"""One-off: raise the contrast of the inline footer address colour.

#5D6874 on the --ink background measured 3.311:1. The footer address is the
one place a visitor is told where to physically go, so it needs to be readable,
not decorative. #737E8A clears 4.5:1 on the same background.

Run from the project root:  python qa/fix-footer-contrast.py
"""
import pathlib
import re

OLD = "#5D6874"
NEW = "#737E8A"

changed = 0
for p in sorted(pathlib.Path("site").rglob("*.html")):
    t = p.read_text(encoding="utf-8")
    if OLD not in t:
        continue
    p.write_text(t.replace(OLD, NEW), encoding="utf-8")
    changed += 1
    print("  ", p.as_posix())

print("files changed:", changed)

left = []
for p in sorted(pathlib.Path("site").rglob("*.html")):
    if OLD in p.read_text(encoding="utf-8"):
        left.append(p.as_posix())
print("remaining:", left or "none")
