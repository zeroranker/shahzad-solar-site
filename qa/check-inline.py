"""Confirm the print button still works after moving it out of an inline handler.

Removing onclick="window.print()" is only safe if the replacement actually
fires. This drives the real button in a headless browser and checks that
window.print() was invoked, by installing a stub before the click.

Run from the project root:  python qa/check-inline.py
"""
import json
import pathlib
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")

PROBE = """<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<iframe id="f" src="http://127.0.0.1:8811/before-you-buy/" style="width:1100px;height:900px;border:0"></iframe>
<script>
window.addEventListener('load', function () {
  var w = document.getElementById('f').contentWindow;
  var d = w.document;
  setTimeout(function () {
    var b = d.querySelector('[data-print]');
    if (!b) { document.title = 'RES' + 'ULT:' + JSON.stringify({found: false}); return; }
    var called = 0;
    w.print = function () { called++; };
    b.click();
    var inline = d.querySelectorAll('[onclick]').length;
    document.title = 'RES' + 'ULT:' + JSON.stringify({
      found: true, label: b.textContent.trim(), printCalls: called,
      inlineHandlersOnPage: inline
    });
  }, 1400);
});
</script></body></html>"""

with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                 dir="site", encoding="utf-8") as f:
    f.write(PROBE)
    probe = pathlib.Path(f.name).name

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
try:
    proc = subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=11000", "--dump-dom",
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
    print("no result — probe did not complete")
    sys.exit(1)

d = json.loads(title)
print(f"  button found        : {d.get('found')}")
print(f"  label               : {d.get('label')!r}")
print(f"  window.print calls  : {d.get('printCalls')}")
print(f"  inline handlers left: {d.get('inlineHandlersOnPage')}")
ok = d.get("found") and d.get("printCalls") == 1 and d.get("inlineHandlersOnPage") == 0
print("\nPASS" if ok else "\nFAIL")
sys.exit(0 if ok else 1)
