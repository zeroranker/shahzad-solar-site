"""Diagnose what the CSP test found: which stylesheets, and which inline
handler is still being executed.

check-csp-live.py reported sheetRules = 0 and a violation reading "Executing
inline event handler". Two separate things, both need identifying precisely
rather than guessing — so this enumerates every stylesheet and every
event-handler-ish attribute on the page, from the live DOM under the policy.

Run from the project root:  python qa/diag-csp.py
"""

import http.server
import json
import pathlib
import socketserver
import subprocess
import sys
import threading
import time

sys.stdout.reconfigure(encoding="utf-8")

PORT = 8825
ROOT = pathlib.Path("site").resolve()
CFG = json.loads(pathlib.Path("vercel.json").read_text(encoding="utf-8"))
POLICY = next(
    h["value"] for h in CFG["headers"][0]["headers"]
    if h["key"] == "Content-Security-Policy"
)

HANDLER_ATTRS = [
    "onclick", "onload", "onerror", "onchange", "oninput",
    "onmouseover", "onfocus", "onblur", "onsubmit", "onkeydown",
]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def end_headers(self):
        if not self.path.endswith("__diagprobe.html"):
            self.send_header("Content-Security-Policy", POLICY)
        super().end_headers()

    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
time.sleep(0.5)

PROBE = """<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<iframe id="f" src="http://127.0.0.1:%d/index.html" style="width:420px;height:800px;border:0"></iframe>
<script>
window.addEventListener('load', function () {
  var w = document.getElementById('f').contentWindow;
  var d = w.document;
  setTimeout(function () {
    var sheets = [];
    var i;
    for (i = 0; i < d.styleSheets.length; i++) {
      var s = d.styleSheets[i];
      var n = null;
      try { n = s.cssRules.length; } catch (e) { n = 'BLOCKED'; }
      sheets.push({
        href: s.href ? s.href.replace(/^https?:\\/\\/[^/]+/, '') : '(inline <style>)',
        rules: n,
        disabled: s.disabled
      });
    }
    var handlers = [];
    var all = d.querySelectorAll('body *');
    for (i = 0; i < all.length; i++) {
      for (var h = 0; h < HANDLERS.length; h++) {
        if (all[i].hasAttribute && all[i].hasAttribute(HANDLERS[h])) {
          handlers.push(all[i].tagName.toLowerCase() + '[' + HANDLERS[h] + '="'
            + String(all[i].getAttribute(HANDLERS[h])).slice(0, 40) + '"]');
        }
      }
    }
    var links = [];
    var ls = d.querySelectorAll('link[rel=stylesheet]');
    for (i = 0; i < ls.length; i++) {
      links.push(ls[i].getAttribute('href'));
    }
    document.title = 'RES' + 'ULT:' + JSON.stringify({
      sheets: sheets, linkHrefs: links, handlers: handlers
    });
  }, 2500);
});
</script></body></html>""" % PORT

probe = ROOT / "__diagprobe.html"
probe.write_text(PROBE, encoding="utf-8")
# inject the handler list into the probe's own scope
probe.write_text(
    PROBE.replace(
        "var all = d.querySelectorAll('body *');",
        "var HANDLERS = " + json.dumps(HANDLER_ATTRS) + ";\n"
        "    var all = d.querySelectorAll('body *');"
    ),
    encoding="utf-8",
)

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
proc = subprocess.run(
    [chrome, "--headless", "--disable-gpu", "--no-sandbox",
     "--virtual-time-budget=14000", "--dump-dom",
     f"http://127.0.0.1:{PORT}/__diagprobe.html"],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
    timeout=90,
)
probe.unlink(missing_ok=True)
httpd.shutdown()

result = {}
for line in (proc.stdout or "").splitlines():
    if "RESULT:" in line:
        result = json.loads(line.split("RESULT:", 1)[1].split("</")[0].strip())

if not result:
    print("no result")
    sys.exit(1)

print("stylesheets as the browser sees them:")
for s in result["sheets"]:
    print(f"  rules={str(s['rules']):>8}  disabled={s['disabled']}  {s['href']}")
print("\n<link rel=stylesheet> hrefs in the markup:")
for h in result["linkHrefs"]:
    print(f"  {h}")
print(f"\ninline event-handler attributes still present: {len(result['handlers'])}")
for h in result["handlers"]:
    print(f"  {h}")
