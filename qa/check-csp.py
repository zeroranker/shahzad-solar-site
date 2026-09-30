"""Compute the SHA-256 hash of every inline script body AND every inline event
handler, for a strict CSP.

The site has exactly one inline script — the 45-byte snippet that sets the
`js` class on <html> so the CSS can reveal the mobile nav — and one inline
event handler, `onload="this.media='all'"` on the non-blocking Google Fonts
link, on 19 pages. Static hosts cannot inject a nonce, but a hash is just as
strong for a body that never changes, and it lets the site ship a
Content-Security-Policy with no 'unsafe-inline' for scripts at all.

The second hash matters more than it looks. Without it the fonts link stays
media="print", the web fonts never load, and the site loses its whole
typographic identity in production while still looking fine in a dev server
that sends no policy. qa/check-csp-live.py is what caught that.

For event handlers the hashed value is the ATTRIBUTE VALUE, not the whole tag.

Run from the project root:  python qa/check-csp.py
"""
import base64
import hashlib
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

HANDLER = re.compile(
    r'\son(click|load|error|change|input|focus|blur|submit|keydown|keyup)'
    r'="([^"]*)"',
    re.I,
)


def b64(s: str) -> str:
    return base64.b64encode(hashlib.sha256(s.encode("utf-8")).digest()).decode()


script_bodies = {}
handler_values = {}

for p in sorted(pathlib.Path("site").rglob("*.html")):
    text = p.read_text(encoding="utf-8")
    for body in re.findall(
        r"<script(?![^>]*\bsrc=)(?![^>]*type=)[^>]*>(.*?)</script>", text, re.S
    ):
        if body.strip():
            script_bodies.setdefault(body, []).append(p.as_posix())
    for _, value in HANDLER.findall(text):
        if value.strip():
            handler_values.setdefault(value, []).append(p.as_posix())

if not script_bodies and not handler_values:
    print("no inline scripts or handlers — script-src needs no hashes")
    sys.exit(0)

hashes = []
print(f"{len(script_bodies)} distinct inline <script> body/bodies\n")
for body, files in script_bodies.items():
    d = b64(body)
    hashes.append(d)
    print(f"  {len(files):>2} page(s)  {len(body.encode('utf-8')):>4} bytes")
    print(f"       body   : {body.strip()[:74]}")
    print(f"       sha256 : {d}")

if handler_values:
    print(f"\n{len(handler_values)} distinct inline event-handler value(s)\n")
    for value, files in handler_values.items():
        d = b64(value)
        hashes.append(d)
        print(f"  {len(files):>2} page(s)")
        print(f"       handler: {value[:74]}")
        print(f"       sha256 : {d}")
        print(f"       on     : {', '.join(f.replace('site/', '') for f in files[:3])}"
              f"{' …' if len(files) > 3 else ''}")

quoted = " ".join(f"'{h}'" for h in hashes)
print("\nPaste into script-src:")
print(f"  script-src 'self' {quoted}")
print("\nStyle is separate: style-src still needs 'unsafe-inline' because the")
print("markup carries inline style attributes. Inline *style* is a much")
print("smaller risk than inline *script* and is accepted practice.")
