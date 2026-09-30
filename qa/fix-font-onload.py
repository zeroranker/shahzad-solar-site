"""One-off: move the non-blocking font swap out of an inline event handler.

The trick was:

    <link rel="stylesheet" href="...google fonts..."
          media="print" onload="this.media='all'">

`onload="..."` is an inline event handler. It is covered by script-src, so a
strict Content-Security-Policy blocks it — and a blocked handler does not
error visibly: the link simply stays media="print", the web fonts never
fetch, and the site loses its entire typographic identity in production while
looking perfect on a dev server that sends no policy at all. That was caught
by qa/check-csp-live.py, not by reading the code.

Hashing the handler would have required adding 'unsafe-hashes', which
re-permits any event handler matching a known hash. Moving the swap into the
deferred site script is both simpler and strictly tighter: after this runs the
site has zero inline event handlers, so the policy needs one hash, not two.

The <noscript> block already carries a plain stylesheet link, so a
JavaScript-disabled reader still gets the fonts.

Run from the project root:  python qa/fix-font-onload.py
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

changed = []
for p in sorted(pathlib.Path("site").rglob("*.html")):
    text = p.read_text(encoding="utf-8")
    # the attribute sits on a link tag that may span a line break in 404.html
    new = re.sub(r'\s+onload="this\.media=\'all\'"', "", text)
    if new != text:
        p.write_text(new, encoding="utf-8")
        changed.append(p.as_posix())

print(f"removed the inline handler from {len(changed)} page(s)")
for c in changed:
    print(f"  {c}")

# verify nothing is left anywhere
left = 0
for p in sorted(pathlib.Path("site").rglob("*.html")):
    text = p.read_text(encoding="utf-8")
    for m in re.findall(r'\son[a-z]+="[^"]*"', text):
        left += 1
        print(f"  STILL PRESENT in {p.as_posix()}: {m}")
print(f"\ninline event-handler attributes remaining in site/: {left}")

# the font link must still be there, just without the handler
sample = pathlib.Path("site/index.html").read_text(encoding="utf-8")
m = re.search(r'<link rel="stylesheet"[^>]*fonts\.googleapis[^>]*>', sample)
print("\nfont link on index.html now reads:")
print("  " + (m.group(0) if m else "NOT FOUND"))
