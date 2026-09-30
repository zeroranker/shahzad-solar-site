"""Prove the Content-Security-Policy in vercel.json does not break the site.

A wrong script hash does not throw an error — it silently blocks the one
inline script, which is the 45-byte snippet that sets the `js` class on <html>.
That class is what reveals the mobile navigation, so a bad hash would ship a
site whose menu cannot be opened on a phone, with nothing in the build to say
so.

This serves the real site with the real header and asks the browser what
actually happened:

  - did the inline script run?   (html.js must be present)
  - was anything blocked?        (console must be free of CSP violations)
  - does the stylesheet load?

Run from the project root:  python qa/check-csp-live.py
"""

import http.server
import json
import os
import pathlib
import re
import socketserver
import subprocess
import sys
import threading
import time

sys.stdout.reconfigure(encoding="utf-8")

PORT = 8823
PROBE_PORT = 8824
ROOT = pathlib.Path("site").resolve()

# take the policy straight out of vercel.json so this cannot drift from it
CFG = json.loads(pathlib.Path("vercel.json").read_text(encoding="utf-8"))
POLICY = next(
    h["value"] for h in CFG["headers"][0]["headers"]
    if h["key"] == "Content-Security-Policy"
)
print("policy under test:")
print("  " + POLICY[:150] + "…\n")


class Handler(http.server.SimpleHTTPRequestHandler):
    """Serves the site WITH the policy, and the probe page without it.

    The probe must be same-origin with the site or the iframe's DOM is
    inaccessible, and it must be policy-free or its own inline script is
    blocked. Exempting the single probe path satisfies both. Every other
    request — every real page and asset — is served under the policy.
    """

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def end_headers(self):
        if not self.path.endswith("__cspprobe.html"):
            self.send_header("Content-Security-Policy", POLICY)
            self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
time.sleep(0.6)

PROBE = """<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<iframe id="f" src="http://127.0.0.1:%d/index.html" style="width:420px;height:800px;border:0"></iframe>
<script>
var violations = [];
window.addEventListener('load', function () {
  var w = document.getElementById('f').contentWindow;
  var d = w.document;
  setTimeout(function () {
    var html = d.documentElement;
    // did the hashed inline script actually execute?
    var jsClass = html.classList.contains('js');
    // Is the site's own stylesheet applied? Read it by href, not by index:
    // styleSheets[0] is the cross-origin Google Fonts sheet, whose cssRules
    // throws by design, which previously made this test report a false
    // failure against a site that was loading its CSS perfectly.
    var sheetRules = -1, fontMedia = null, fontTagMedia = null;
    for (var i = 0; i < d.styleSheets.length; i++) {
      var s = d.styleSheets[i];
      if (s.href && s.href.indexOf('/assets/css/site.css') !== -1) {
        try { sheetRules = s.cssRules.length; } catch (e) { sheetRules = -2; }
      }
    }
    // Read the font link by iterating the stylesheet links. A
    // querySelector('[href*=...]') on this page returned null even though the
    // element was present and correct, so the check now walks the collection
    // the same way diag-font.py does, which is known to work.
    var fontTagMedia = null;
    var links = d.querySelectorAll('link[rel=stylesheet]');
    for (var j = 0; j < links.length; j++) {
      if (String(links[j].getAttribute('href')).indexOf('fonts.googleapis') !== -1) {
        fontTagMedia = links[j].getAttribute('media');
      }
    }
    // is the mobile nav actually reachable?
    var toggle = d.querySelector('.nav-toggle');
    var nav = d.querySelector('.nav');
    var bodyFont = w.getComputedStyle(d.body).fontFamily;
    document.title = 'RES' + 'ULT:' + JSON.stringify({
      jsClass: jsClass,
      htmlClass: html.className,
      siteCssRules: sheetRules,
      fontLinkMedia: fontTagMedia,
      navToggleFound: !!toggle,
      navVisibleWhenClosed: !!(nav && w.getComputedStyle(nav).visibility !== 'hidden'),
      bodyFont: String(bodyFont).slice(0, 70)
    });
  }, 2500);
});
</script></body></html>"""

probe_path = ROOT / "__cspprobe.html"
probe_path.write_text(PROBE % PORT, encoding="utf-8")

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
proc = subprocess.run(
    [chrome, "--headless", "--disable-gpu", "--no-sandbox",
     "--enable-logging=stderr", "--v=0",
     "--virtual-time-budget=12000", "--dump-dom",
     f"http://127.0.0.1:{PORT}/__cspprobe.html"],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
    timeout=90,
)
probe_path.unlink(missing_ok=True)
httpd.shutdown()

result = {}
for line in (proc.stdout or "").splitlines():
    if "RESULT:" in line:
        result = json.loads(line.split("RESULT:", 1)[1].split("</")[0].strip())

csp_errors = [
    l for l in ((proc.stderr or "").splitlines())
    if "Content Security Policy" in l or "Refused to" in l
]

if not result:
    print("no result — probe did not complete")
    sys.exit(1)

print("under a 420px viewport, with the policy enforced:")
for k, v in result.items():
    print(f"  {k:<18} {v}")

print(f"\nCSP violations in console: {len(csp_errors)}")
for e in csp_errors[:5]:
    print("  " + e[:150])

ok = (result.get("jsClass") is True
      and result.get("siteCssRules", -1) > 50
      and result.get("fontLinkMedia") == "all"
      and not csp_errors)

print()
if result.get("fontLinkMedia") != "all":
    print("!! the font link is still media=print — the web fonts would NOT")
    print("   load in production, silently, with no error anywhere.")
if csp_errors:
    print("!! CSP violations in console: " + "; ".join(
        e.split("violates")[-1].strip()[:70] for e in csp_errors[:3]))

print("\nPASS — the policy does not block anything the site needs"
      if ok else "\nFAIL — the policy would break the deployed site")
sys.exit(0 if ok else 1)
