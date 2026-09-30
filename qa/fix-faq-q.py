"""One-off: make .faq__q real.

The FAQ styling was written against `.faq summary`, an element selector, so the
`.faq__q` class that appears on the Urdu <summary> elements matched nothing.
Worse, the two English <summary> elements that lack the class were styled only
by virtue of being a <summary>, so markup and styling disagreed about which
part was load-bearing.

This adds the class to the English summaries so both languages carry the same
markup, and points the CSS at the class rather than the tag.

Run from the project root:  python qa/fix-faq-q.py
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

# 1. CSS: target the class, with the tag selector kept as the fallback
css_path = pathlib.Path("site/assets/css/site.css")
css = css_path.read_text(encoding="utf-8")
before = css
css = css.replace(
    ".faq summary {", ".faq summary, .faq__q {", 1
)
css = css.replace(
    ".faq summary::-webkit-details-marker",
    ".faq summary::-webkit-details-marker, .faq__q::-webkit-details-marker", 1
)
css = css.replace(
    ".faq summary::after {", ".faq summary::after, .faq__q::after {", 1
)
css = css.replace(
    ".faq details[open] summary::after {",
    ".faq details[open] summary::after, .faq details[open] .faq__q::after {", 1
)
css = css.replace(
    ".faq summary:hover {", ".faq summary:hover, .faq__q:hover {", 1
)
if css != before:
    css_path.write_text(css, encoding="utf-8")
    print("site.css: .faq__q added to the five summary rules")

# 2. English summaries: add the class where it is missing
for rel in ("site/faq/index.html", "site/ur/faq/index.html"):
    p = pathlib.Path(rel)
    t = p.read_text(encoding="utf-8")
    n = len(re.findall(r"<summary(?![^>]*class=)", t))
    if n == 0:
        print(f"{rel}: every <summary> already carries a class")
        continue
    t = re.sub(r"<summary(?![^>]*class=)", '<summary class="faq__q"', t)
    p.write_text(t, encoding="utf-8")
    print(f"{rel}: added class to {n} <summary> element(s)")

# 3. verify
for rel in ("site/faq/index.html", "site/ur/faq/index.html"):
    t = pathlib.Path(rel).read_text(encoding="utf-8")
    total = len(re.findall(r"<summary", t))
    classed = len(re.findall(r'<summary class="faq__q"', t))
    print(f"  {rel}: {classed}/{total} summaries carry .faq__q")
