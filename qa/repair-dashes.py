"""Repair the typographic characters destroyed by the bad PowerShell re-encode.

Two distinct losses:
  1. em-dash U+2014  ->  two spaces
  2. en-dash U+2013  ->  deleted outright (numeric/时间 ranges)
  3. times sign U+00D7 -> deleted outright (1.5x sanctioned load)

Known en-dash/times cases are fixed explicitly first, then every remaining
double-space inside a TEXT NODE becomes an em-dash. Attributes and the
JSON-LD blocks are handled separately so we never touch code.
"""
import glob, os, re

ROOT = r"E:\harness\New folder\solar-mission\site"
DASH, NDASH, TIMES, DOT = "\u2014", "\u2013", "\u00d7", "\u00b7"

# --- 1. explicit restorations (do these first) --------------------------
EXACT = [
    # ranges that lost their en-dash with no surrounding spaces
    ("301400 units", "301" + NDASH + "400 units"),
    ("001100 units", "001" + NDASH + "100 units"),
    ("0200 units",  "0" + NDASH + "200 units"),
    ("25500 kW",    "25" + NDASH + "500 kW"),
    ("325 kW",      "3" + NDASH + "25 kW"),
    ("5070%",       "50" + NDASH + "70%"),
    # the multiplication sign
    ("1.5 sanctioned", "1.5" + TIMES + " sanctioned"),
    ("1.0 sanctioned", "1.0" + TIMES + " sanctioned"),
    ("2.0 sanctioned", "2.0" + TIMES + " sanctioned"),
    # ranges that lost a spaced en-dash -> now read as a double space
    ("3 kW  25 kW",        "3" + NDASH + "25 kW"),
    ("10 kW  100 kW",      "10" + NDASH + "100 kW"),
    ("100 kW  250 kW",     "100" + NDASH + "250 kW"),
    ("Rs 42  47 per watt", "Rs 42" + NDASH + "47 per watt"),
    ("9am  7pm",           "9am" + NDASH + "7pm"),
    ("Monday  Saturday",   "Monday" + NDASH + "Saturday"),
    ("Rs 750,000  900,000",        "Rs 750,000" + NDASH + "900,000"),
    ("Rs 1,300,000  1,600,000",    "Rs 1,300,000" + NDASH + "1,600,000"),
    ("Rs 2,000,000  2,400,000",    "Rs 2,000,000" + NDASH + "2,400,000"),
    ("Rs 750,000  Rs 2,400,000",   "Rs 750,000" + NDASH + "Rs 2,400,000"),
    # middle dot that lost its neighbour
    ("&nbsp;  &nbsp;", "&nbsp;" + DOT + "&nbsp;"),
]

# --- 2. blanket em-dash inside text nodes only --------------------------
TEXTNODE = re.compile(r">([^<>]*)<")
DASHABLE = re.compile(r"[^\s]\s{2,}[^\s]")

def fix_text(s: str) -> str:
    return DASHABLE.sub(f" {DASH} ", s)

total_exact = total_dash = 0
for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)):
    src = open(path, encoding="utf-8").read()
    before = src

    n = 0
    for old, new in EXACT:
        c = src.count(old)
        if c:
            src = src.replace(old, new)
            n += c
    total_exact += n

    # only inside >text< runs, so attributes/JS/JSON are never touched
    src = TEXTNODE.sub(lambda m: ">" + fix_text(m.group(1)) + "<", src)
    d = DASHABLE.sub(" " + DASH + " ", before) != DASHABLE.sub(" " + DASH + " ", src)
    total_dash += len(DASHABLE.findall(before)) - len(DASHABLE.findall(src))

    if src != before:
        open(path, "w", encoding="utf-8", newline="").write(src)
        print(f"  {os.path.relpath(path, ROOT):26} exact={n:2}  em-dash={len(DASHABLE.findall(before)) - len(DASHABLE.findall(src)):2}")

print(f"\nexact restorations: {total_exact}   em-dashes restored: {total_dash}")

# --- 3. verify nothing was left behind ----------------------------------
left = 0
for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)):
    src = open(path, encoding="utf-8").read()
    for m in re.finditer(r">([^<>]{2,})<", src):
        t = m.group(1)
        for mm in re.finditer(r"\S(  +)\S", t):
            print(f"  LEFTOVER {os.path.relpath(path, ROOT)}: {t[max(0,mm.start()-30):mm.end()+30]!r}")
            left += 1
print(f"leftover double-spaces in text: {left}")
