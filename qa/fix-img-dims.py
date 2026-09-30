"""One-off: correct the width/height attributes on every project image.

The six JPEGs are 16:9. Several pages declared 1200x800 (1.500) or 480x360
(1.333), which reserves the wrong box and caused a measured CLS of 0.28 on
/ur/projects/. They are now 960x540 after qa/re-encode-images.py.

Run from the project root:  python qa/fix-img-dims.py
"""
import pathlib
import re

ROOT = pathlib.Path("site")

REPLACEMENTS = [
    (re.compile(r'width="1200" height="800"'), 'width="960" height="540"'),
    (re.compile(r'width="480" height="360"'), 'width="960" height="540"'),
    (re.compile(r'width="1280" height="720"'), 'width="960" height="540"'),
]

changed = []
for p in sorted(ROOT.rglob("*.html")):
    original = p.read_text(encoding="utf-8")
    text = original
    for pattern, repl in REPLACEMENTS:
        text = pattern.sub(repl, text)
    if text != original:
        p.write_text(text, encoding="utf-8")
        changed.append(p.as_posix())

print("files changed:", len(changed))
for c in changed:
    print("  ", c)

# report anything still wrong
leftovers = []
for p in sorted(ROOT.rglob("*.html")):
    for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        m = re.search(r'<img[^>]*width="(\d+)"\s+height="(\d+)"', line)
        if m and (m.group(1), m.group(2)) != ("960", "540"):
            leftovers.append(f"{p.as_posix()}:{i} {m.group(1)}x{m.group(2)}")
print("remaining non-960x540 declarations:", len(leftovers))
for l in leftovers:
    print("  ", l)
