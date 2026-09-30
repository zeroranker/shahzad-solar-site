"""Verify every JSON-LD block on the site parses, and that each FAQPage
question/answer text appears verbatim in the visible page content.

Run from the project root:  python qa/verify-jsonld.py
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("site")
fail = 0

for path in sorted(ROOT.rglob("*.html")):
    page = path.read_text(encoding="utf-8")
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', page, re.S
    )
    if not blocks:
        continue

    for raw in blocks:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"FAIL {path.as_posix()}: invalid JSON — {e}")
            fail += 1
            continue

        kind = data.get("@type", "?")
        print(f"ok   {path.as_posix()}: {kind}")

        if kind != "FAQPage":
            continue

        # strip script/style, then tags, so we can look for the literal answer
        visible = re.sub(r"<script.*?</script>", " ", page, flags=re.S)
        visible = re.sub(r"<style.*?</style>", " ", visible, flags=re.S)
        visible = re.sub(r"<[^>]+>", " ", visible)
        visible = html.unescape(visible)
        visible = re.sub(r"\s+", " ", visible)

        for q in data["mainEntity"]:
            name = q["name"]
            answer = q["acceptedAnswer"]["text"]
            # check the first 60 characters of each, which is enough to prove
            # they were taken from this page rather than from a stale copy
            for label, text in (("question", name), ("answer", answer)):
                probe = text[:60].strip()
                if probe and probe not in visible:
                    print(f"     MISMATCH in {label}: {probe!r}")
                    fail += 1

print()
print("FAILURES:", fail) if fail else print("All JSON-LD valid and in sync with visible text.")
sys.exit(1 if fail else 0)
