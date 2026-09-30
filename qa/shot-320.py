"""Screenshot a page at a true 320px layout.

Headless Chrome on Windows clamps --window-size to a 500px minimum, so a direct
--window-size=320 screenshot is a 500px layout cropped to 320px and tells you
nothing. This renders the page inside a same-origin 320px iframe (a real
layout box) and screenshots the iframe element by its clip rect.

Run from the project root:  python qa/shot-320.py <path> <out.png>
"""
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

page = sys.argv[1] if len(sys.argv) > 1 else "index.html"
out = sys.argv[2] if len(sys.argv) > 2 else "qa/shots/narrow-320.png"
height = int(sys.argv[3]) if len(sys.argv) > 3 else 900

probe = pathlib.Path("site", "__shot320.html")
probe.write_text(
    f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;padding:0;background:#fff}}#f{{border:0;display:block;width:320px;height:{height}px}}</style>
</head><body><iframe id="f" src="http://127.0.0.1:8811/{page}"></iframe></body></html>""",
    encoding="utf-8",
)

out_path = pathlib.Path(out).resolve()
out_path.parent.mkdir(parents=True, exist_ok=True)

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run(
    [chrome, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
     "--force-device-scale-factor=2",
     "--virtual-time-budget=9000",
     f"--screenshot={out_path}",
     "--window-size=340,960",
     "http://127.0.0.1:8811/__shot320.html"],
    capture_output=True, timeout=90,
)
probe.unlink(missing_ok=True)
print(f"{out_path}  ({out_path.stat().st_size if out_path.exists() else 0} bytes)")
