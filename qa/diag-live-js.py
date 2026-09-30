"""Probe the LIVE deployment in a real browser.

The HTTP layer is fine — every page 200s, the CSS and JS are served, the CSP
header arrives. So whatever the user is seeing has to be a script that is not
executing. This loads the deployed URL in headless Chrome and reports what
actually happened, plus any console errors and any CSP violations.

  python qa/diag-live-js.py https://shahzad-solar-site.vercel.app
"""
import json
import subprocess
import sys
import tempfile
import pathlib

sys.stdout.reconfigure(encoding="utf-8")

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(2)
URL = sys.argv[1].rstrip("/")

PROBE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{{margin:0}}#f{{border:0;display:block;width:1024px;height:900px}}</style>
</head><body>
<iframe id="f" src="{url}/"></iframe>
<script>
window.addEventListener('load', function () {{
  var w = document.getElementById('f').contentWindow;
  var d = w.document;
  setTimeout(function () {{
    var out = {{}};
    try {{
      out.htmlClass = d.documentElement.className;
      var outGen = d.querySelector('[data-out="gen"]');
      out.genText = outGen ? outGen.textContent.trim() : '(no element)';
      // the tool is live if genText is a real number, not the 0 placeholder
      out.solarDayLive = /^\\d/.test(out.genText);

      // the profile buttons: do they carry a handler? clicking one should
      // change which button is pressed
      var btns = d.querySelectorAll('[data-profile], .seg__btn, [data-seg]');
      out.profileBtnCount = btns.length;
      out.profileBtnAttrs = [];
      for (var i = 0; i < btns.length && i < 4; i++) {{
        out.profileBtnAttrs.push(btns[i].tagName + ' ' + btns[i].className
          + ' | ' + Array.prototype.map.call(btns[i].attributes,
            function (a) {{ return a.name + '=' + a.value; }}).join(' ').slice(0, 90));
      }}
      out.btnClassList = [];
      for (i = 0; i < btns.length && i < 4; i++) btnClassList.push(btns[i].className);
      out.scriptTagCount = d.querySelectorAll('script[src]').length;
      out.hasSiteJs = !!w.SolarDay || typeof w.print === 'function';
      out.bodyHeight = d.body.scrollHeight;
      out.docScrollW = d.documentElement.scrollWidth;
      out.docClientW = d.documentElement.clientWidth;
    }} catch (e) {{
      out.error = String(e);
    }}
    document.title = 'RES' + 'ULT:' + JSON.stringify(out);
  }}, 3000);
}});
</script></body></html>"""

tmp = pathlib.Path(tempfile.gettempdir(), "livejs.html")
tmp.write_text(PROBE.format(url=URL), encoding="utf-8")

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
proc = subprocess.run(
    [chrome, "--headless", "--disable-gpu", "--no-sandbox",
     "--enable-logging=stderr", "--v=0",
     "--virtual-time-budget=20000", "--dump-dom",
     tmp.as_uri()],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
    timeout=120,
)
tmp.unlink(missing_ok=True)

res = {}
for line in (proc.stdout or "").splitlines():
    if "RESULT:" in line:
        res = json.loads(line.split("RESULT:", 1)[1].split("</")[0].strip())

print(f"probing {URL}\n")
if not res:
    print("no result — the probe could not reach the page")
    print("stderr tail:")
    print("\n".join((proc.stderr or "").splitlines()[-10:]))
    sys.exit(1)

for k, v in res.items():
    if k == "profileBtnAttrs":
        print(f"  {k}:")
        for b in v:
            print(f"      {b}")
    else:
        print(f"  {k:<18} {v}")

print("\nconsole / CSP lines:")
noise = [l for l in (proc.stderr or "").splitlines()
         if "CONSOLE" in l or "Content Security" in l or "Refused" in l]
if not noise:
    print("  (none)")
for l in noise[:12]:
    print("  " + l.split("CONSOLE:")[-1][:160] if "CONSOLE:" in l else "  " + l[:160])
