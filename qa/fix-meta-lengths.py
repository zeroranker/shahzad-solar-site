"""One-off: shorten the eight meta descriptions that exceed 160 characters.

Rewrites are hand-made, not truncated, so the sentence still reads as English
and still leads with what the page is for. Every replacement is printed so it
can be checked against the page it describes.

Run from the project root:  python qa/fix-meta-lengths.py
"""
import html
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

NEW = {
    "site/index.html":
        "Solar in Faisalabad, checked before you sign. The February 2026 net billing "
        "rules, our real project footage, and the questions we will not guess at.",
    "site/agriculture/index.html":
        "35,019 tubewells in Faisalabad district, only 482 subsidised slots. What "
        "solar costs a diesel pump, what it costs on the grid, and what the "
        "scheme no longer covers.",
    "site/net-billing/index.html":
        "Net metering ended on 9 February 2026. What replaced it, what it pays for "
        "your surplus, and a real number worked through line by line.",
    "site/systems/index.html":
        "Sizing a Faisalabad solar system against your sanctioned load, plus what "
        "batteries are and are not for, and a price table you can argue with.",
    "site/faq/index.html":
        "Can you get a zero bill? Do panels last 25 years? Who owns the meter? "
        "Straight answers, with the ones we cannot answer marked as such.",
    "site/ur/index.html":
        "فیصل آباد کا سولر، مہلے فیصلہ کرنے سے پہلے جانچا ہوا۔ فروری 2026 کے نئے "
        "قوانین، ہمارے حقیقی منصوبے، اور وہ سوال جو ہم گمانے سے نہیں دیتے۔",
    "site/ur/about/index.html":
        "ہمارا AEDB ریکارڈ بالکل ویسے ہی جیسا رجسٹر میں درج ہے، بشمول وہ حصے "
        "جو ہمارے حقیقی ہیں۔ تصدیق کی تاریخ اور حدود بھی۔",
    "site/projects/index.html":
        "Five projects with a link to the footage of each, and a column for what "
        "that footage does not prove.",
}

LIMIT = 160
for rel, desc in NEW.items():
    p = pathlib.Path(rel)
    t = p.read_text(encoding="utf-8")
    # reuse the file's own escaping style: the descriptions carry &#8212;
    esc = desc
    new_t, n = re.subn(
        r'(<meta name="description" content=")[^"]*(")',
        lambda m: m.group(1) + esc + m.group(2),
        t,
        count=1,
    )
    if n != 1:
        print(f"  !! {rel}: description meta not found")
        continue
    p.write_text(new_t, encoding="utf-8")
    n_chars = len(html.unescape(desc))
    print(f"  {n_chars:>4}  {rel}  {'OK' if n_chars <= LIMIT else 'STILL OVER'}")

print()
# re-run the report
import subprocess

subprocess.run([sys.executable, "qa/report-meta.py"], check=False)
