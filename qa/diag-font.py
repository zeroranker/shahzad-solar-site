"""Is site.js actually running, and what is the font link's media attribute?

check-csp-live.py reported fontLinkMedia = None after the swap was moved into
the deferred site script. That has two possible causes — the script not
running at all, or the selector not matching — and they need to be told apart
before anything else is changed.

Run from the project root:  python qa/diag-font.py
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

PORT = 8826
ROOT = pathlib.Path("site").resolve()

PROBE = """<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<iframe id="f" src="http://127.0.0.1:%d/index.html" style="width:420px;height:800px;border:0"></iframe>
<script>
window.addEventListener('load', function () {
  var w = document.getElementById('f').contentWindow;
  var d = w.document;
  setTimeout(function () {
    var links = d.querySelectorAll('link[rel=stylesheet]');
    var found = [];
    for (var i = 0; i < links.length; i++) {
      found.push({
        href: String(links[i].getAttribute('href')).slice(0, 46),
        mediaAttr: links[i].getAttribute('media'),
        mediaProp: String(links[i].media)
      });
    }
    // did site.js run at all? it registers the nav, and the Solar Day tool
    // writes to [data-out] — check for a rendered number instead.
    var out = d.querySelector('[data-out="gen"]');
    var jsRunning = !!(out && out.textContent.trim() && out.textContent.trim() !== '0');
    document.title = 'RES' + 'ULT:' + JSON.stringify({
      siteJsRan: jsRunning,
      genOutput: out ? out.textContent.trim() : null,
      stylesheetLinks: found
    });
  }, 2500);
});
</script></body></html>""" % PORT


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", PORT), H)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
time.sleep(0.5)

probe = ROOT / "__fontdiag.html"
probe.write_text(PROBE, encoding="utf-8")

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
proc = subprocess.run(
    [chrome, "--headless", "--disable-gpu", "--no-sandbox",
     "--virtual-time-budget=14000", "--dump-dom",
     f"http://127.0.0.1:{PORT}/__fontdiag.html"],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
    timeout=90,
)
probe.unlink(missing_ok=True)
httpd.shutdown()

res = {}
for line in (proc.stdout or "").splitlines():
    if "RESULT:" in line:
        res = json.loads(line.split("RESULT:", 1)[1].split("</")[0].strip())

if not res:
    print("no result")
    sys.exit(1)

print(f"site.js ran (Solar Day produced a number): {res['siteJsRan']}")
print(f"  [data-out=gen] = {res['genOutput']!r}\n")
print("stylesheet links as the browser sees them:")
for s in res["stylesheetLinks"]:
    print(f"  media attribute = {s['mediaAttr']!r}   media property = {s['mediaProp']!r}")
    print(f"    {s['href']}…")
