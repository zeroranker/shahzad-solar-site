"""Show where a literal em-dash or multiply sign sits, and whether it is
inside a JSON-LD <script> block (where a literal character is correct and an
HTML entity would be wrong, because script content is raw text) or in visible
markup (where this project uses numeric entities throughout).

Run from the project root:  python qa/where-punct.py
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

PUNCT = {"—": "em-dash", "–": "en-dash", "×": "multiply",
         "·": "middot", "©": "copyright", " ": "nbsp"}

for p in sorted(pathlib.Path("site").rglob("*.html")):
    text = p.read_text(encoding="utf-8")

    # mark the byte ranges occupied by JSON-LD script blocks
    jsonld = [(m.start(), m.end())
              for m in re.finditer(
                  r'<script type="application/ld\+json">.*?</script>',
                  text, re.S)]

    for i, line in enumerate(text.split("\n"), 1):
        hits = [name for ch, name in PUNCT.items() if ch in line]
        if not hits:
            continue
        pos = text.index(line) if False else None
        # locate this line within the document
        offset = sum(len(l) + 1 for l in text.split("\n")[: i - 1])
        inside = any(s <= offset + 5 < e for s, e in jsonld)
        where = "JSON-LD (literal is CORRECT here)" if inside else "VISIBLE MARKUP"
        print(f"{p.as_posix()}:{i}  {', '.join(hits)}  -> {where}")
        print(f"    {line.strip()[:120]}")
