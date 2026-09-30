"""Regenerate the FAQPage JSON-LD from the visible <details> content.

Google requires that a FAQPage's Question/acceptedAnswer text match what is
actually on the page. Maintaining two copies by hand let them drift, so this
script reads the visible markup and rewrites the block from it. Running it is
always safe: if nothing drifted, it is a no-op.

It also inserts an equivalent block into the Urdu FAQ page, which had none.

Run from the project root:  python qa/sync-faq-jsonld.py
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("site")
SCRIPT = "assets/js/site.js"


def strip_tags(fragment: str) -> str:
    """Visible text of a block of HTML, with entity and whitespace cleanup."""
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract(page: str):
    """Return [(question, answer)] from the page's <details class="faq__item">."""
    items = []
    for block in re.findall(
        r'<details class="faq__item"[^>]*>(.*?)</details>', page, re.S
    ):
        q = re.search(r"<summary[^>]*>(.*?)</summary>", block, re.S)
        a = re.search(r'<div class="faq__a">(.*)$', block, re.S)
        if not q or not a:
            continue
        # The whole answer body, not just its <p> elements: an answer that
        # contains a <ul> must carry those list items into the structured
        # data too, or the JSON-LD is not what the page says.
        answer = strip_tags(a.group(1))
        if answer:
            items.append((strip_tags(q.group(1)), answer))
    return items


def build_block(items) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in items
        ],
    }
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, indent=2, ensure_ascii=False)
        + "\n</script>"
    )


def main() -> int:
    changed = []

    # No hardcoded expected count. An earlier version pinned it at 8, which
    # silently skipped the sync twice as the FAQ grew to 14 — the guard was
    # protecting the script from working. The real invariants are checked by
    # qa/verify-jsonld.py, which fails if the JSON and the visible text
    # disagree. Here we only require the two languages to carry the same
    # number of questions, and that it is not zero.
    counts = {}
    for rel in ("faq/index.html", "ur/faq/index.html"):
        path = ROOT / rel
        page = path.read_text(encoding="utf-8")
        items = extract(page)
        counts[rel] = len(items)
        if not items:
            print(f"  !! {rel}: no .faq__item blocks found — nothing to sync")
            return 1

        if len(set(counts.values())) > 1:
            print(f"  !! FAQ item counts differ between languages: {counts}")
            return 1

        block = build_block(items)
        if re.search(r'<script type="application/ld\+json">.*?</script>', page, re.S):
            new = re.sub(
                r'<script type="application/ld\+json">.*?</script>',
                lambda m: block,
                page,
                count=1,
                flags=re.S,
            )
        else:
            # insert immediately after the <script> that sets the js class
            anchor = "<script>document.documentElement.classList.add('js');</script>"
            new = page.replace(anchor, anchor + "\n\n" + block, 1)

        if new != page:
            path.write_text(new, encoding="utf-8")
            changed.append(f"{rel} ({len(items)} questions)")

    n = next(iter(counts.values()))
    print(f"FAQ items per language: {n}")
    print("updated:", ", ".join(changed) if changed else "nothing (already in sync)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
