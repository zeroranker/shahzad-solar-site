"""Print the visible FAQ questions on both language versions, side by side.

Run from the project root:  python qa/faq-questions.py
"""
import html
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

for rel in ("faq/index.html", "ur/faq/index.html"):
    page = pathlib.Path("site") / rel
    print(f"\n=== {rel} ===")
    for i, block in enumerate(
        re.findall(r'<details class="faq__item"[^>]*>(.*?)</details>', page.read_text(encoding="utf-8"), re.S),
        1,
    ):
        q = re.search(r"<summary[^>]*>(.*?)</summary>", block, re.S)
        if q:
            text = html.unescape(re.sub(r"<[^>]+>", "", q.group(1)))
            print(f"  {i}. {re.sub(r'[[:space:]]+', ' ', text).strip()}")
