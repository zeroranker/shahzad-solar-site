"""Site-wide contrast audit on what the browser actually paints.

qa/check-contrast.py reads the stylesheet and compares token against token. It
passed 15/15 while the Urdu hero's secondary call to action sat at 1.07:1 —
invisible — because the fault was never in a single colour value. It was a
light-theme component (.btn--ghost) placed on a dark section (.section--ink).
No amount of reading the token table sees that pairing; you have to render it.

So this renders every page and measures every visible text element against
the background actually painted beneath it, walking up the tree until an
opaque background is found. It catches the whole class of bug.

  python qa/check-painted-contrast.py [base-url]
"""
import json
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8811"

PAGES = [
    "/", "/net-billing/", "/before-you-buy/", "/systems/", "/agriculture/",
    "/projects/", "/faq/", "/about/", "/contact/", "/ur/", "/ur/net-billing/",
    "/ur/before-you-buy/", "/ur/systems/", "/ur/agriculture/", "/ur/projects/",
    "/ur/faq/", "/ur/about/", "/ur/contact/",
]

PROBE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{{margin:0}}</style></head><body>
<script>
function lum(c) {{
  var m = c.match(/[\\d.]+/g);
  if (!m || m.length < 3) return null;
  var a = parseFloat(m[3] === undefined ? 1 : m[3]);
  if (a === 0) return null;
  var f = m.slice(0, 3).map(function (v) {{
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  }});
  return 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2];
}}
function ratio(a, b) {{
  var l1 = lum(a), l2 = lum(b);
  if (l1 === null || l2 === null) return null;
  return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
}}
function parse(c) {{
  var m = c.match(/[\\d.]+/g);
  if (!m || m.length < 3) return null;
  return {{ r: +m[0], g: +m[1], b: +m[2],
            a: m.length > 3 ? parseFloat(m[3]) : 1 }};
}}
function over(fg, bg) {{
  // composite a possibly-translucent colour onto an opaque one
  var a = fg.a;
  return 'rgb(' + Math.round(fg.r * a + bg.r * (1 - a)) + ', ' +
                  Math.round(fg.g * a + bg.g * (1 - a)) + ', ' +
                  Math.round(fg.b * a + bg.b * (1 - a)) + ')';
}}
function bgOf(el) {{
  /* The sticky header and the mobile bottom bar are translucent. Reading
     their rgba() as if it were opaque made near-white look like a tinted
     wash and produced dozens of false failures — dark header text scoring
     1.19:1 against what is really near-white. So: collect every background
     from the element upwards, then composite the stack from the bottom up
     until it is opaque, exactly as the browser paints it. */
  var layers = [], n = el;
  while (n && n !== document.documentElement) {{
    var p = parse(getComputedStyle(n).backgroundColor);
    if (p && p.a > 0) {{
      layers.push(p);
      if (p.a >= 1) break;
    }}
    n = n.parentElement;
  }}
  if (!layers.length || layers[layers.length - 1].a < 1) {{
    layers.push({{ r: 255, g: 255, b: 255, a: 1 }});
  }}
  // layers[0] is nearest the text; the last one is opaque. Fold upward.
  var base = layers[layers.length - 1];
  for (var i = layers.length - 2; i >= 0; i--) {{
    base = over(layers[i], base);
  }}
  return 'rgb(' + base.r + ', ' + base.g + ', ' + base.b + ')';
}}
function scan(d) {{
  var out = [], seen = {{}};
  d.querySelectorAll('body *').forEach(function (el) {{
    // only elements that directly contain visible text
    var txt = '';
    for (var i = 0; i < el.childNodes.length; i++) {{
      var n = el.childNodes[i];
      if (n.nodeType === 3) txt += n.nodeValue;
    }}
    txt = txt.replace(/\\s+/g, ' ').trim();
    if (txt.length < 2) return;
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    if (parseFloat(cs.opacity) < 0.6) return;
    var r = ratio(cs.color, bgOf(el));
    if (r === null) return;
    var px = parseFloat(cs.fontSize);
    var bold = parseInt(cs.fontWeight, 10) >= 700;
    var large = px >= 24 || (px >= 18.66 && bold);
    var need = large ? 3.0 : 4.5;
    var key = cs.color + '|' + bgOf(el) + '|' + el.className;
    if (seen[key]) return;
    seen[key] = 1;
    if (r >= need) return;
    out.push({{
      sel: el.tagName.toLowerCase() +
           (el.className && typeof el.className === 'string'
             ? '.' + el.className.trim().split(/\\s+/).join('.') : ''),
      text: txt.slice(0, 38), color: cs.color, bg: bgOf(el),
      size: px, ratio: Math.round(r * 100) / 100, need: need
    }});
  }});
  return out;
}}
var pages = {pages};
var results = {{}}, done = 0, total = 0, fails = 0;
function finish() {{
  document.title = 'RES' + 'ULT:' + JSON.stringify({{
    total: total, fails: fails, results: results
  }});
}}
pages.forEach(function (p) {{
  var f = document.createElement('iframe');
  f.style.cssText = 'width:1280px;height:900px;border:0;position:absolute;left:-9999px';
  f.src = p;
  f.onload = function () {{
    setTimeout(function () {{
      try {{
        var bad = scan(f.contentDocument);
        results[p] = bad;
        total += 1;
        fails += bad.length;
      }} catch (e) {{
        results[p] = [{{ sel: 'ERROR', text: String(e).slice(0, 60),
                        ratio: 0, need: 4.5 }}];
      }}
      if (++done === pages.length) finish();
    }}, 900);
  }};
  document.body.appendChild(f);
}});
</script></body></html>"""

tmp = pathlib.Path("site", "__painted.html")
tmp.write_text(PROBE.format(pages=json.dumps(PAGES)), encoding="utf-8")

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
try:
    proc = subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=120000", "--dump-dom",
         f"{BASE}/__painted.html"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=300,
    )
finally:
    tmp.unlink(missing_ok=True)

res = {}
for line in (proc.stdout or "").splitlines():
    if "RESULT:" in line:
        res = json.loads(line.split("RESULT:", 1)[1].split("</")[0].strip())

if not res:
    print("no result — the scan did not complete")
    sys.exit(2)

print(f"painted contrast across {len(PAGES)} pages of {BASE}\n")
for page, bad in res["results"].items():
    if bad:
        print(f"  {page}")
        for b in bad:
            print(f"    {b['ratio']:>6}:1  need {b['need']}  {b['size']}px  {b['sel'][:54]}")
            print(f"            {b['text']!r}  {b['color']} on {b['bg']}")
        print()

print("=" * 62)
if res["fails"]:
    print(f"{res['fails']} text style(s) below WCAG AA as actually painted.")
    sys.exit(1)
print(f"Clean. Every text style on all {len(PAGES)} pages meets AA "
      f"against the background it is really drawn on.")
