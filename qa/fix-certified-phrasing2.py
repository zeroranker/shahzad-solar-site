"""One-off, part 2: the remaining present-tense "certified range" phrasings.

Same rationale as part 1 - these sit in about/, projects/, systems/ and the
Urdu projects page. Every one points at a document whose validity date has
passed, and the list it comes from is not filtered by validity, so the
present tense overstates what we actually know.

Run from the project root:  python qa/fix-certified-phrasing2.py
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")

REPLACEMENTS = {
    "site/about/index.html": [
        ("Our largest published project is four times our certified range",
         "Our largest published project is four times the range on our C-3 certificate"),
    ],
    "site/projects/index.html": [
        ("<span class=\"tag tag--signal\">4&#215; our certified range</span>",
         "<span class=\"tag tag--signal\">4&#215; the range on our C-3 certificate</span>"),
        ("<span class=\"tag tag--good\">Within our certified range</span>",
         "<span class=\"tag tag--good\">Within our C-3 certificate range</span>"),
        ("<td>That this is within our AEDB C-3 certified range of up to 250 kW</td>",
         "<td>That this is within the 250 kW range on our AEDB C-3 certificate</td>"),
        ("Top of our certified range", "Top of our C-3 range"),
        ("A ground-mounted industrial array at exactly the top of our AEDB C-3 certified range of",
         "A ground-mounted industrial array at exactly the top of the 250 kW range on our AEDB C-3 certificate:"),
    ],
    "site/systems/index.html": [
        ("This is the top of our AEDB C-3 certified range.",
         "This is the top of the 250 kW range on our AEDB C-3 certificate."),
    ],
    "site/ur/projects/index.html": [
        ("<td>250 kW ہماری تصدیق کی C-3 حد کے بالکل برابر ہے</td>",
         "<td>250 kW ہماری C-3 سرٹیفکیٹ پر درج حد کے بالکل برابر ہے</td>"),
    ],
}

for rel, pairs in REPLACEMENTS.items():
    p = pathlib.Path(rel)
    t = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old not in t:
            print(f"  --  {rel}: not found -> {old[:62]!r}")
            continue
        n = t.count(old)
        t = t.replace(old, new)
        print(f"  ok  {rel}: {n}x  {old[:56]!r}")
    p.write_text(t, encoding="utf-8")

print()
left = []
for p in sorted(pathlib.Path("site").rglob("*.html")):
    t = p.read_text(encoding="utf-8")
    for bad in ("certified range", "تصدیق کی C-3 حد"):
        if bad in t:
            left.append(f"{p.as_posix()}: {bad!r}")
print("remaining:", left or "none")
