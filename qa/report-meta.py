"""Report meta description lengths against the 160-character display budget.

Google truncates a description around 155-160 characters depending on device.
Anything longer is spending words that are never shown.

Run from the project root:  python qa/report-meta.py
"""
import html
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
LIMIT = 160

rows = []
for p in sorted(pathlib.Path("site").rglob("*.html")):
    t = p.read_text(encoding="utf-8")
    m = re.search(r'<meta name="description" content="([^"]*)"', t)
    if not m:
        continue
    d = html.unescape(m.group(1))
    rows.append((len(d), p.as_posix(), d))

for n, path, d in sorted(rows, reverse=True):
    flag = "OVER" if n > LIMIT else "ok  "
    print(f"{flag} {n:>4}  {path}")

over = [r for r in rows if r[0] > LIMIT]
print(f"\n{len(over)} of {len(rows)} descriptions exceed {LIMIT} characters.")
