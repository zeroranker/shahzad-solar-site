"""Count the checklist items, and measure real horizontal overflow.

Two things the report asserts that were never actually measured:

  1. The "Before you buy" checklist is described as twelve checks. Count it.
  2. A 320 px header fix was applied but never re-measured. Headless Chrome
     on Windows clamps its window to a 500 px minimum, so --window-size=320
     produces a 500 px layout cropped to 320 px — which is what produced a
     false alarm earlier in this project.

     The fix here is the same one used before: load the target inside a
     same-origin full-width iframe, then set that iframe's *layout* width to
     the width under test and measure inside the child frame. The child
     viewport is genuinely 320 px because the iframe is a real layout box.

Run from the project root:  python qa/check-narrow.py
"""
import json
import pathlib
import re
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")

PAGES = [
    "index.html", "net-billing/index.html", "before-you-buy/index.html",
    "systems/index.html", "agriculture/index.html", "projects/index.html",
    "faq/index.html", "about/index.html", "contact/index.html",
    "ur/index.html", "ur/faq/index.html", "ur/before-you-buy/index.html",
]

# ---------------------------------------------------------------- checklist
print("=== checklist item count ===")
for rel in ("site/before-you-buy/index.html", "site/ur/before-you-buy/index.html"):
    text = pathlib.Path(rel).read_text(encoding="utf-8")
    ticks = re.findall(r'<input[^>]*id="(?:c|cb)-\d+"', text)
    labels = re.findall(r'<span class="check__t">\s*(\d+)\.', text)
    print(f"  {rel}")
    print(f"    checkboxes : {len(ticks)}")
    print(f"    numbered labels found: "
          f"{', '.join(labels) if labels else 'none (checkboxes are unnumbered here)'}")

# ------------------------------------------------------------ 320 px test
PROBE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;padding:0}}#f{{border:0;display:block}}</style></head><body>
<iframe id="f" src="http://127.0.0.1:8811/{page}" style="width:320px;height:900px"></iframe>
<script>
window.addEventListener('load', function () {{
  var f = document.getElementById('f');
  var w = f.contentWindow, d = w.document;
  setTimeout(function () {{
    var de = d.documentElement, deH = d.querySelector('.site-header__in');
    var r = function (el) {{ return el ? Math.round(el.getBoundingClientRect().right) : null; }};
    var over = [];
    var all = d.querySelectorAll('body *');
    for (var i = 0; i < all.length && i < 3000; i++) {{
      var b = all[i].getBoundingClientRect();
      if (b.width > 0 && b.right > 321) {{
        var tag = all[i].tagName.toLowerCase();
        var cls = (all[i].className && all[i].className.baseVal !== undefined)
          ? all[i].className.baseVal : (all[i].className || '');
        over.push(tag + '.' + String(cls).split(' ')[0] + ' right=' + Math.round(b.right));
      }}
    }}
    document.title = 'RES' + 'ULT:' + JSON.stringify({{
      scrollW: de.scrollWidth, clientW: de.clientWidth,
      headerRight: r(deH),
      overflowing: over.slice(0, 6)
    }});
  }}, 1200);
}});
</script></body></html>"""

print("\n=== 320px horizontal overflow (true 320px layout) ===")
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
worst = 0
for page in PAGES:
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                     dir="site", encoding="utf-8") as f:
        f.write(PROBE.format(page=page))
        probe = pathlib.Path(f.name).name
    try:
        proc = subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-sandbox",
             "--virtual-time-budget=10000", "--dump-dom",
             f"http://127.0.0.1:8811/{probe}"],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=90,
        )
    finally:
        pathlib.Path("site", probe).unlink(missing_ok=True)

    title = ""
    for line in (proc.stdout or "").splitlines():
        if "RESULT:" in line:
            title = line.split("RESULT:", 1)[1].split("</")[0].strip()
    if not title:
        print(f"  {page:34} NO RESULT")
        continue
    d = json.loads(title)
    bad = d["scrollW"] > d["clientW"] + 1
    worst = max(worst, d["scrollW"] - d["clientW"])
    flag = "OVERFLOW" if bad else "ok"
    print(f"  {page:34} scrollW={d['scrollW']:>4} clientW={d['clientW']:>4}  {flag}")
    if d["overflowing"]:
        print(f"      first offenders: {', '.join(d['overflowing'][:4])}")

print(f"\nlargest horizontal overflow across {len(PAGES)} pages: {worst}px")
