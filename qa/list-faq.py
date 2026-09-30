"""List the FAQ items in both languages, with a count.

The FAQ sync script reported "found 14 items, expected 8", which is worth
checking directly rather than trusting: the report and the README both claim a
different number, so one of them is wrong.

Run from the project root:  python qa/list-faq.py
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ITEM = re.compile(
    r'<details class="faq__item"[^>]*>\s*<summary class="faq__q"[^>]*>(.*?)</summary>',
    re.S,
)

for rel in ("site/faq/index.html", "site/ur/faq/index.html"):
    text = pathlib.Path(rel).read_text(encoding="utf-8")
    items = ITEM.findall(text)
    # a second count, ignoring the class, to be sure the regex is not undercounting
    raw = len(re.findall(r"<summary", text))
    print(f"\n{rel}")
    print(f"  faq__item blocks : {len(items)}")
    print(f"  all <summary>    : {raw}")
    for i, q in enumerate(items, 1):
        clean = re.sub(r"<[^>]+>", "", q).strip()
        print(f"   {i:2}. {clean[:76]}")
