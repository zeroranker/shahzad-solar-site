"""Headless check that the "Your solar day" model is still self-consistent.

Loads the real page in Chrome, drives the real controls through JS, and reads
the real rendered output — it does not re-derive the arithmetic in Python, so
this catches a regression in site.js rather than restating it.

The invariant the page itself claims: 5 kW x 30 days = 630 units, and the
verdict text must state that number.

Run from the project root:  python qa/check-solar-day.py
"""
import json
import pathlib
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")

PROBE = """<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<iframe id="f" src="http://127.0.0.1:8811/{page}" style="width:1280px;height:900px;border:0"></iframe>
<script>
window.addEventListener('load', function () {{
  var w = document.getElementById('f').contentWindow;
  var d = w.document;
  setTimeout(function () {{
    var kw  = d.querySelector('[data-ctl="kw"]');
    var gen = d.querySelector('[data-out="gen"]');
    var slf = d.querySelector('[data-out="self"]');
    var exp = d.querySelector('[data-out="export"]');
    var ver = d.querySelector('[data-out="verdict"]');
    if (!kw) {{ document.title = 'NO-KW-CONTROL'; return; }}
    kw.value = '5';
    kw.dispatchEvent(new w.Event('input', {{bubbles: true}}));
    kw.dispatchEvent(new w.Event('change', {{bubbles: true}}));
    setTimeout(function () {{
      document.title = 'RES' + 'ULT:' + JSON.stringify({{
        gen: gen ? gen.textContent.trim() : null,
        self: slf ? slf.textContent.trim() : null,
        export: exp ? exp.textContent.trim() : null,
        verdict: ver ? ver.textContent.replace(/\\s+/g,' ').trim().slice(0,300) : null
      }});
    }}, 500);
  }}, 1500);
}});
</script></body></html>"""

for page in ("index.html", "ur/index.html"):
    with tempfile.NamedTemporaryFile(
        "w", suffix=".html", delete=False, dir="site",
        encoding="utf-8",
    ) as f:
        f.write(PROBE.format(page=page))
        probe_path = pathlib.Path(f.name).name

    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    proc = subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=12000", "--dump-dom",
         f"http://127.0.0.1:8811/{probe_path}"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=90,
    )
    pathlib.Path("site", probe_path).unlink(missing_ok=True)

    title = ""
    for line in (proc.stdout or "").splitlines():
        if "RESULT:" in line:
            title = line.split("RESULT:", 1)[1].split("</")[0].strip()
    if not title:
        print(f"{page}: could not read a result (no RESULT marker in output)")
        continue
    try:
        data = json.loads(title)
    except json.JSONDecodeError:
        print(f"{page}: malformed result -> {title[:200]!r}")
        continue
    verdict = data.get("verdict") or ""
    gen, slf, exp = data.get("gen"), data.get("self"), data.get("export")
    print(f"{page}")
    print(f"   gen/self/export : {gen} / {slf} / {exp}")
    print(f"   verdict         : {verdict[:200]}")
    # the model says 5 kW x 30 days must reconcile to 630 units
    ok = "630" in verdict
    print(f"   630 in verdict  : {'YES' if ok else 'NO'}")
    if not ok:
        print("   -> FAIL: expected 630 units for 5 kW over 30 days")
