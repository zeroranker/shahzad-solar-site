import sys, io, re
from pypdf import PdfReader

src = r"E:\harness\New folder\solar-mission\research\raw"

for name in ["aedb-c3-2026-04-08.pdf", "sro-547-2026-04-02.pdf", "sro-251-2026-02-09.pdf"]:
    path = f"{src}\\{name}"
    try:
        r = PdfReader(path)
    except Exception as e:
        print(f"=== {name}: READ ERROR {e}"); continue
    txt = []
    for p in r.pages:
        try: txt.append(p.extract_text() or "")
        except Exception as e: txt.append(f"[page err {e}]")
    full = "\n".join(txt)
    out = f"{src}\\{name}.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(full)
    print(f"=== {name}: {len(r.pages)} pages, {len(full)} chars extracted")
    if not full.strip():
        print("    !! NO TEXT LAYER - image-only scan")
    else:
        hits = [l for l in full.splitlines() if re.search(r"(?i)shahzad", l)]
        for h in hits:
            print("    SHAHZAD:", h.strip())
