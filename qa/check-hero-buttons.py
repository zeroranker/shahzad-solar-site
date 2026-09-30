"""Measure the real painted colour of the hero buttons, both languages.

The English hero sits on paper and the Urdu hero sits on ink, so the same
button classes sit on very different backgrounds. A contrast audit that reads
only the stylesheet can miss that pairing; this asks the browser what it
actually painted, walking up from the element until it finds a non-transparent
background and computing WCAG from the result.

The probe is served from the same origin and drives a same-origin iframe —
framing is permitted locally, and the deployed CSP's frame-ancestors 'self'
means this must stay same-origin to be meaningful.

  python qa/check-hero-buttons.py [base-url]
"""
import json
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8811"
PAGES = ["/", "/ur/"]

PROBE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{{margin:0}}</style></head><body>
<script>
function lum(c) {{
  var m = c.match(/[\\d.]+/g).map(Number);
  var f = m.slice(0, 3).map(function (v) {{
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  }});
  return 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2];
}}
function ratio(a, b) {{
  var l1 = lum(a), l2 = lum(b);
  return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
}}
function bgOf(el) {{
  var n = el;
  while (n) {{
    var b = getComputedStyle(n).backgroundColor;
    if (b && b !== 'rgba(0, 0, 0, 0)' && b !== 'transparent') return b;
    n = n.parentElement;
  }}
  return 'rgb(255, 255, 255)';
}}
function measure(d) {{
  var out = [];
  d.querySelectorAll('.hero__cta a, .hero__cta button').forEach(function (el) {{
    var cs = getComputedStyle(el);
    var col = cs.color, bg = bgOf(el);
    var px = parseFloat(cs.fontSize);
    var bold = parseInt(cs.fontWeight, 10) >= 700;
    var large = px >= 24 || (px >= 18.66 && bold);
    var r = ratio(col, bg);
    out.push({{
      text: el.textContent.replace(/\\s+/g, ' ').trim().slice(0, 30),
      color: col, bg: bg, size: px, weight: cs.fontWeight,
      ratio: Math.round(r * 100) / 100,
      need: large ? 3.0 : 4.5,
      pass: r >= (large ? 3.0 : 4.5)
    }});
  }});
  return out;
}}
var pages = {pages};
var results = {{}}, done = 0;
pages.forEach(function (p, i) {{
  var f = document.createElement('iframe');
  f.style.cssText = 'width:1200px;height:900px;border:0';
  f.src = p;
  f.onload = function () {{
    setTimeout(function () {{
      try {{ results[p] = measure(f.contentDocument); }}
      catch (e) {{ results[p] = [{{ text: 'ERROR ' + e, pass: false,
                                  ratio: 0, need: 4.5 }}]; }}
      if (++done === pages.length) {{
        document.title = 'RES' + 'ULT:' + JSON.stringify(results);
      }}
    }}, 1200);
  }};
  document.body.appendChild(f);
}});
</script></body></html>"""

tmp = pathlib.Path("site", "__heroprobe.html")
tmp.write_text(PROBE.format(pages=json.dumps(PAGES)), encoding="utf-8")

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
try:
    proc = subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=20000", "--dump-dom",
         f"{BASE}/__heroprobe.html"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=120,
    )
finally:
    tmp.unlink(missing_ok=True)

res = {}
for line in (proc.stdout or "").splitlines():
    if "RESULT:" in line:
        res = json.loads(line.split("RESULT:", 1)[1].split("</")[0].strip())

print(f"measuring hero buttons on {BASE}\n")
if not res:
    print("no result — probe did not complete")
    sys.exit(1)

fails = 0
total = 0
for page, rows in res.items():
    print(f"  {page}")
    if not rows:
        print("      no hero buttons found")
        continue
    for r in rows:
        total += 1
        flag = "ok" if r["pass"] else "FAIL"
        if not r["pass"]:
            fails += 1
        print(f"    {r['text']:<30} {r['size']}px/{r['weight']:<4} "
              f"{r['ratio']:>6}:1  need {r['need']}  {flag}")
        print(f"        {r['color']} on {r['bg']}")
    print()

print(f"{total} button(s) measured, {fails} below WCAG AA")
sys.exit(1 if fails else 0)
