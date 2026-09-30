"""One-off: stop the project pages implying a currently-valid certificate.

The AEDB register entry reads "CR/24/027/C-3 (Rev-1) 08-06-2025". That date
has passed, the list was published 08-04-2026, and it is not validity-filtered
- so today's status is genuinely UNKNOWN. The site says so at length on /about/
and in the FAQ, but the project pages, cards and tables kept saying "our AEDB
C-3 certified range" in the present tense, which reads as a live credential.

These rewordings point at the document rather than asserting live status. The
factual content is unchanged: 250 kW, C-3, same category, same project.

Run from the project root:  python qa/fix-certified-phrasing.py
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")

REPLACEMENTS = {
    "site/index.html": [
        ("4&#215; our certified range",
         "4&#215; the range on our C-3 certificate"),
        ("Our largest published project is four times our certified range",
         "Our largest published project is four times the range on our C-3 certificate"),
        ("Within our certified range",
         "Within our C-3 certificate range"),
        ("That this is within our AEDB C-3 certified range of up to 250 kW",
         "That this is within the 250 kW range on our AEDB C-3 certificate"),
        ("Top of our certified range",
         "Top of our C-3 range"),
        ("A ground-mounted industrial array at exactly the top of our AEDB C-3 certified range of",
         "A ground-mounted industrial array at exactly the top of the 250 kW range on our AEDB C-3 certificate:"),
        ("A ground-mounted industrial array at the top of our certified range.",
         "A ground-mounted industrial array at the top of the range on our C-3 certificate."),
        ("times the top of our certified range, and we say so on the project page.",
         "times the top of the range on our C-3 certificate, and we say so on the project page."),
        ("This is the top of our AEDB C-3 certified range.",
         "This is the top of the 250 kW range on our AEDB C-3 certificate."),
    ],
    "site/ur/index.html": [
        ("ہماری AEDB تصدیق کیٹیگری C-3 کی ہے، جس کی حد <b>250 kW</b> ہے۔",
         "کیٹیگری C-3 کی ہماری سرٹیفکیٹ پر درج حد <b>250 kW</b> ہے۔"),
        ("<td>250 kW ہماری تصدیق کی C-3 حد کے بالکل برابر ہے</td>",
         "<td>250 kW ہماری C-3 سرٹیفکیٹ پر درج حد کے بالکل برابر ہے</td>"),
        ("کیٹیگری C-3 کی حد <b>250 kW</b> تک ہے۔",
         "کیٹیگری C-3 کی حد <b>250 kW</b> تک ہے۔"),
    ],
}

for rel, pairs in REPLACEMENTS.items():
    p = pathlib.Path(rel)
    t = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old not in t:
            print(f"  --  {rel}: not found -> {old[:60]!r}")
            continue
        n = t.count(old)
        t = t.replace(old, new)
        print(f"  ok  {rel}: {n}x  {old[:58]!r}")
    p.write_text(t, encoding="utf-8")

print()
left = []
for p in sorted(pathlib.Path("site").rglob("*.html")):
    t = p.read_text(encoding="utf-8")
    for bad in ("certified range", "تصدیق کی C-3 حد", "ہماری تصدیق کیٹیگری C-3"):
        if bad in t:
            left.append(f"{p.as_posix()}: {bad!r}")
print("remaining present-tense 'certified range' phrasing:", left or "none")
