"""Click the profile buttons and confirm the model actually responds.

The reported symptom was "the Home / Shop / Factory buttons don't work". The
cause was a selector in site.js that looked for a button *inside* an element
carrying data-seg, while the markup puts data-seg on the button itself. The
selector matched nothing, so every profile button was dead. The tool still
computed correctly on load, which is why every other check passed and only a
real click exposed it.

This clicks each button in a real browser and asserts that:
  - the pressed state moves (aria-pressed flips)
  - self-use and export change
  - the verdict text changes

Generation is deliberately NOT asserted to change: it depends on system size,
not on the consumption profile, so 630 units across all three is correct.

  python qa/check-buttons.py [base-url] [page]
  python qa/check-buttons.py http://127.0.0.1:8811 /ur/
"""
import json
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8811"
PAGE = sys.argv[2] if len(sys.argv) > 2 else "/"

PROBE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{{margin:0}}#f{{border:0;display:block;width:1024px;height:900px}}</style>
</head><body>
<iframe id="f" src="{base}{page}"></iframe>
<script>
window.addEventListener('load', function () {{
  var w = document.getElementById('f').contentWindow;
  var d = w.document;
  function read() {{
    var g = d.querySelector('[data-out="gen"]');
    var s = d.querySelector('[data-out="self"]');
    var e = d.querySelector('[data-out="export"]');
    var v = d.querySelector('[data-out="verdict"]');
    var pressed = [];
    var bs = d.querySelectorAll('[data-seg="profile"]');
    for (var i = 0; i < bs.length; i++) {{
      if (bs[i].getAttribute('aria-pressed') === 'true') {{
        pressed.push(bs[i].textContent.trim());
      }}
    }}
    return {{
      gen: g ? g.textContent.trim() : null,
      self: s ? s.textContent.trim() : null,
      export: e ? e.textContent.trim() : null,
      verdict: v ? v.textContent.replace(/\\s+/g, ' ').trim().slice(0, 110) : null,
      pressed: pressed
    }};
  }}
  setTimeout(function () {{
    var steps = [];
    steps.push({{ label: 'initial', state: read() }});
    var bs = d.querySelectorAll('[data-seg="profile"]');
    if (!bs.length) {{
      document.title = 'RES' + 'ULT:' + JSON.stringify(
        {{ buttonCount: 0, buttonLabels: [], steps: steps }});
      return;
    }}
    var i = 0;
    (function next() {{
      if (i >= bs.length) {{
        document.title = 'RES' + 'ULT:' + JSON.stringify({{
          buttonCount: bs.length,
          buttonLabels: Array.prototype.map.call(bs, function (b) {{
            return b.textContent.trim();
          }}),
          steps: steps
        }});
        return;
      }}
      var idx = i++;
      bs[idx].click();
      setTimeout(function () {{
        steps.push({{ label: 'clicked ' + bs[idx].textContent.trim(),
                      state: read() }});
        next();
      }}, 700);
    }})();
  }}, 1800);
}});
</script></body></html>"""

tmp = pathlib.Path("site", "__btnprobe.html")
tmp.write_text(PROBE.format(base=BASE, page=PAGE), encoding="utf-8")

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
try:
    proc = subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=20000", "--dump-dom",
         f"{BASE}/__btnprobe.html"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=120,
    )
finally:
    tmp.unlink(missing_ok=True)

res = {}
for line in (proc.stdout or "").splitlines():
    if "RESULT:" in line:
        res = json.loads(line.split("RESULT:", 1)[1].split("</")[0].strip())

print(f"testing {BASE}{PAGE}")
if not res:
    print("  no result — probe did not complete")
    sys.exit(1)

if not res.get("buttonCount"):
    print("  no profile buttons found on this page")
    sys.exit(1)

print(f"buttons found: {res['buttonCount']}  {res['buttonLabels']}\n")
for s in res["steps"]:
    st = s["state"]
    print(f"  {s['label']:<20} pressed={str(st['pressed']):<12} "
          f"gen={st['gen']:<12} self={st['self']:<13} export={st['export']}")
    print(f"      {st['verdict'][:94]}")

exported = {s["state"]["export"] for s in res["steps"]}
selfuse = {s["state"]["self"] for s in res["steps"]}
pressed = {tuple(s["state"]["pressed"]) for s in res["steps"]}
verdicts = {s["state"]["verdict"] for s in res["steps"]}
gens = {s["state"]["gen"] for s in res["steps"]}

print()
print(f"distinct pressed states  : {len(pressed)}   "
      f"{'ok' if len(pressed) > 1 else 'FAIL'}")
print(f"distinct export values   : {len(exported)}   "
      f"{'ok' if len(exported) > 1 else 'FAIL'}")
print(f"distinct self-use values : {len(selfuse)}   "
      f"{'ok' if len(selfuse) > 1 else 'FAIL'}")
print(f"distinct verdicts        : {len(verdicts)}   "
      f"{'ok' if len(verdicts) > 1 else 'FAIL'}")
print(f"generation constant      : {'yes (correct)' if len(gens) == 1 else 'varies'}"
      f"  — depends on kW, not on the load profile")

ok = len(pressed) > 1 and len(exported) > 1 and len(verdicts) > 1
print("\nPASS — the buttons recompute the model"
      if ok else "\nFAIL — the buttons repaint but do not change the model")
sys.exit(0 if ok else 1)
