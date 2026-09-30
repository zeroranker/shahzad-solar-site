"""Full integrity sweep across the site.

Catches the specific failure modes this project has hit before:
  - U+FFFD replacement characters (the PowerShell Get-Content corruption)
  - literal UTF-8 punctuation typed into markup where an entity belongs
  - markdown ** left in HTML
  - stray English words inside Urdu prose
  - unbalanced or duplicated HTML ids

Run from the project root:  python qa/sweep.py
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path("site")
issues = 0

URDU_PAGES = sorted((ROOT / "ur").rglob("*.html"))

# --- 1. replacement characters -----------------------------------------
for p in sorted(ROOT.rglob("*.html")) + sorted(ROOT.rglob("*.css")) \
        + [ROOT / "assets/js/site.js", ROOT / "sitemap.xml",
           ROOT / "robots.txt", ROOT / "manifest.webmanifest"]:
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8")
    n = t.count("\ufffd")
    if n:
        issues += n
        print(f"  U+FFFD x{n}  {p.as_posix()}")
print(f"[1] replacement characters: {'clean' if not issues else 'FOUND'}")

# --- 2. literal punctuation in VISIBLE markup --------------------------
# Inside <script type="application/ld+json"> a literal UTF-8 character is not
# only acceptable but required: script content is raw text, so an HTML entity
# there would arrive at the parser as the six characters "&#8212;" inside the
# answer string. The JSON-LD sync script writes literal characters on purpose.
lit = 0
for p in sorted(ROOT.rglob("*.html")):
    t = p.read_text(encoding="utf-8")
    jsonld = [(m.start(), m.end()) for m in re.finditer(
        r'<script type="application/ld\+json">.*?</script>', t, re.S)]
    for i, line in enumerate(t.split("\n"), 1):
        hits = [name for ch, name in
                [("\u2014", "em-dash"), ("\u2013", "en-dash"),
                 ("\u00d7", "multiply"), ("\u00b7", "middot"),
                 ("\u00a9", "copyright"), ("\u00a0", "nbsp")]
                if ch in line]
        if not hits:
            continue
        offset = sum(len(l) + 1 for l in t.split("\n")[: i - 1])
        if any(s <= offset + 5 < e for s, e in jsonld):
            continue  # inside JSON-LD: correct as-is
        lit += len(hits)
        print(f"  literal {', '.join(hits)}  {p.as_posix()}:{i}")
print(f"[2] literal punctuation in visible markup: "
      f"{'clean' if not lit else str(lit) + ' FOUND'}")

# --- 3. markdown left in HTML ------------------------------------------
md = 0
for p in sorted(ROOT.rglob("*.html")):
    t = p.read_text(encoding="utf-8")
    n = len(re.findall(r"\*\*[^*<]{1,40}\*\*", t))
    if n:
        md += n
        print(f"  markdown bold x{n}  {p.as_posix()}")
print(f"[3] markdown in HTML: {'clean' if not md else str(md) + ' FOUND'}")

# --- 4. duplicate ids --------------------------------------------------
dups = 0
for p in sorted(ROOT.rglob("*.html")):
    t = p.read_text(encoding="utf-8")
    ids = re.findall(r'\sid="([^"]+)"', t)
    seen, d = set(), []
    for i in ids:
        (d if i in seen else seen).append(i) if i in seen else seen.add(i)
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        dups += len(dupes)
        print(f"  duplicate id {sorted(dupes)}  {p.as_posix()}")
print(f"[4] duplicate ids: {'clean' if not dups else str(dups) + ' FOUND'}")

# --- 5. unclosed tags (crude but catches gross damage) -----------------
open_p = close_p = 0
for p in sorted(ROOT.rglob("*.html")):
    t = p.read_text(encoding="utf-8")
    o = len(re.findall(r"<p[ >]", t))
    c = len(re.findall(r"</p>", t))
    if o != c:
        open_p += 1
        print(f"  <p> {o} open / {c} close  {p.as_posix()}")
print(f"[5] <p> balance: {'clean' if not open_p else str(open_p) + ' IMBALANCED'}")

# --- 6. hreflang symmetry ----------------------------------------------
bad = 0
for p in sorted(ROOT.rglob("*.html")):
    t = p.read_text(encoding="utf-8")
    if 'hreflang="en"' not in t and 'hreflang="ur"' not in t:
        print(f"  no hreflang at all  {p.as_posix()}")
        bad += 1
print(f"[6] hreflang: {'clean' if not bad else str(bad) + ' FOUND'}")

# --- 6b. no leftover probe or scratch files in the shipped site ---------
# robots.txt and sitemap.xml are legitimate site-root files, not scratch.
ALLOWED_ROOT_FILES = {"robots.txt", "sitemap.xml", "manifest.webmanifest"}
stray = [
    p.as_posix() for p in ROOT.rglob("*")
    if p.is_file()
    and p.name not in ALLOWED_ROOT_FILES
    and (p.name.startswith(("__", "tmp", "probe")) or p.suffix in (".py", ".bak"))
]
if stray:
    print("  stray files in site/:")
    for s in stray:
        print(f"    {s}")
print(f"[6b] no scratch files in site/: "
      f"{'clean' if not stray else str(len(stray)) + ' FOUND'}")
bad += len(stray)

# --- 7. Urdu pages: lang and dir ---------------------------------------
urdu = 0
for p in URDU_PAGES:
    t = p.read_text(encoding="utf-8")
    if 'lang="ur"' not in t:
        urdu += 1
        print(f"  Urdu page without lang=\"ur\"  {p.as_posix()}")
    if 'dir="rtl"' not in t:
        urdu += 1
        print(f"  Urdu page without dir=\"rtl\"  {p.as_posix()}")
print(f"[7] Urdu lang/dir: {'clean' if not urdu else str(urdu) + ' FOUND'}")

print()
total = issues + lit + md + dups + open_p + bad + urdu
print("SWEEP CLEAN" if total == 0 else f"SWEEP FOUND {total} ISSUE(S)")
sys.exit(0 if total == 0 else 1)
