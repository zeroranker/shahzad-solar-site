"""Load the LIVE page directly in Chrome and read the resulting DOM.

Framing is not an option — the deployed CSP sets frame-ancestors 'self',
which correctly blocks an iframe from another origin (and is exactly what
stopped the previous probe; that was the site behaving properly, not a
fault). So this navigates straight to the deployed URL and inspects the DOM
as it stands after the scripts have run.

The Solar Day outputs are the tell. In the source markup they read "0". If
site.js executed, they read real numbers. If it did not, they still read "0".

  python qa/diag-live-dom.py https://shahzad-solar-site.vercel.app
"""
import re
import subprocess
import sys
import tempfile
import pathlib

sys.stdout.reconfigure(encoding="utf-8")

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(2)
URL = sys.argv[1].rstrip("/")

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
proc = subprocess.run(
    [chrome, "--headless", "--disable-gpu", "--no-sandbox",
     "--enable-logging=stderr", "--v=0",
     "--virtual-time-budget=18000", "--dump-dom", URL + "/"],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
    timeout=120,
)

dom = proc.stdout or ""
print(f"probing {URL}/")
print(f"DOM returned: {len(dom):,} chars\n")

# --- did site.js run? ---------------------------------------------------
print("Solar Day outputs (source markup says 0; live values mean JS ran)")
for attr in ("gen", "self", "export", "old", "new", "delta"):
    m = re.search(rf'data-out="{attr}"[^>]*>([^<]*)<', dom)
    print(f"  data-out={attr:<7} {m.group(1).strip() if m else '(not found)'}")

verdict = re.search(r'data-out="verdict"[^>]*>(.*?)</div>', dom, re.S)
if verdict:
    txt = re.sub(r"<[^>]+>", "", verdict.group(1))
    print(f"\n  verdict: {' '.join(txt.split())[:150]}")

js_ran = bool(verdict and len(" ".join(txt.split())) > 40)
print(f"\n  site.js executed: {js_ran}")

# --- the profile buttons ------------------------------------------------
print("\nprofile buttons")
btns = re.findall(r'<button[^>]*data-profile[^>]*>', dom)
if not btns:
    btns = re.findall(r'<button[^>]*class="[^"]*seg[^"]*"[^>]*>', dom)
print(f"  found {len(btns)}")
for b in btns[:5]:
    print(f"    {' '.join(b.split())[:110]}")

# --- anything the console complained about -------------------------------
print("\nconsole / CSP")
noise = [l for l in (proc.stderr or "").splitlines()
         if "CONSOLE" in l or "Refused" in l]
if not noise:
    print("  (none)")
for l in noise[:10]:
    body = l.split("CONSOLE:")[-1] if "CONSOLE:" in l else l
    print("  " + body.strip()[:165])
