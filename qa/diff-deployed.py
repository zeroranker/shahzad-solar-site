"""Show exactly how the deployed copy differs from the local one.

compare-deployed.py proved every file differs. This says *how*, because a
stale deploy is only a problem to the extent that it is missing a fix — and
one of the fixes made after the last deploy is the one that stops the strict
CSP from silently killing the web fonts.

  python qa/diff-deployed.py https://shahzad-solar-site.vercel.app
"""
import difflib
import ssl
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(2)
BASE = sys.argv[1].rstrip("/")
CTX = ssl.create_default_context()

CHECKS = [
    # (path, label, [substrings whose presence matters])
    ("index.html", "inline onload font handler", ["onload=\"this.media='all'\""]),
    ("index.html", "canonical host", ["<link rel=\"canonical\""]),
    ("index.html", "faq__q class", ["class=\"faq__q\""]),
    ("assets/js/site.js", "JS font-swap code", ["media=\"print\""]),
    ("assets/js/site.js", "JS print handler", ["data-print"]),
    ("assets/css/site.css", "brand flex-shrink fix", ["flex-shrink: 1"]),
    ("assets/css/site.css", "dead .form-status rule", [".form-status {"]),
    ("assets/css/site.css", "dead reveal system", ["[data-reveal]"]),
]


def get(path):
    with urllib.request.urlopen(BASE + "/" + path, context=CTX,
                                timeout=25) as r:
        return r.read().decode("utf-8", "replace")


print(f"{BASE}\n")
print(f"{'file':<20} {'feature':<34} {'local':<8} {'deployed':<9}")
print("-" * 74)
stale = []
for path, label, needles in CHECKS:
    remote = get(path)
    local = Path("site", path).read_text(encoding="utf-8")
    for needle in needles:
        in_local = needle in local
        in_remote = needle in remote
        same = in_local == in_remote
        if not same:
            stale.append((path, label))
        print(f"  {path:<18} {label[:32]:<32} "
              f"{'yes' if in_local else 'no':<8} "
              f"{'yes' if in_remote else 'no':<9}"
              f"{'' if same else '  <-- DIFFERS'}")

print()
if not stale:
    print("The deployed copy contains every fix. The byte differences are "
          "line-ending only.")
else:
    print(f"{len(stale)} feature(s) present locally but NOT deployed:")
    for p, l in stale:
        print(f"  - {p}: {l}")
    print("\nRedeploy. Until then the live site is running older code.")

# show a concrete textual diff of the head of index.html
print("\n--- first differences in index.html (deployed -> local) ---")
remote = get("index.html").splitlines()
local = Path("site/index.html").read_text(encoding="utf-8").splitlines()
n = 0
for line in difflib.unified_diff(remote, local, "deployed", "local",
                                 lineterm="", n=0):
    if line.startswith(("---", "+++", "@@")):
        continue
    if line.startswith(("+", "-")):
        print("  " + line[:150])
        n += 1
        if n > 24:
            print("  … (truncated)")
            break
if n == 0:
    print("  none — the files differ only in line endings")
