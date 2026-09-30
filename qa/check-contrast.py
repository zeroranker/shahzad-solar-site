"""Compute WCAG contrast ratios for the site's actual colour pairs.

Nothing here is copied from an audit report. The foreground/background pairs
are the ones the stylesheet and the inline page markup actually use, and each
ratio is computed from the WCAG 2.x relative-luminance formula so the pass or
fail is a measurement, not an assertion.

Run from the project root:  python qa/check-contrast.py
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")


def srgb(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lum(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b)


def ratio(fg: str, bg: str) -> float:
    a, b = lum(fg), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


# resolved from site/assets/css/site.css
css = pathlib.Path("site/assets/css/site.css").read_text(encoding="utf-8")
TOKENS = dict(
    re.findall(r"(--[a-z0-9-]+):\s*(#[0-9A-Fa-f]{6})", css)
)
PAPER = TOKENS.get("--paper", "#FBFAF6")
INK = TOKENS.get("--ink", "#0E1216")

PAIRS = [
    # (label, foreground, background, minimum)
    ("body text", TOKENS["--text"], PAPER, 4.5),
    ("secondary text", TOKENS["--text-2"], PAPER, 4.5),
    ("tertiary text / source notes", TOKENS["--text-3"], PAPER, 4.5),
    ("accent text on paper", TOKENS["--sun-deep"], PAPER, 4.5),
    ("success text", TOKENS["--good"], PAPER, 4.5),
    ("primary button label", "#2A1A05", TOKENS["--sun"], 4.5),
    ("primary button hover label", "#FFF6E6", "#A05F0E", 4.5),
    ("WhatsApp button label", "#FFFFFF", "#15703C", 4.5),
    ("WhatsApp hover label", "#FFFFFF", "#0E5C2E", 4.5),
    ("footer body text", "#737E8A", INK, 4.5),
    ("footer heading", TOKENS["--on-ink"], INK, 4.5),
    ("chart load curve", TOKENS["--sun-deep"], PAPER, 3.0),
    ("chart gridlines", TOKENS["--rule-chart"], PAPER, 3.0),
    ("chart tick labels", TOKENS["--text-2"], PAPER, 4.5),
    ("control border", TOKENS["--rule-strong"], PAPER, 3.0),
]

print(f"tokens resolved: {len(TOKENS)}   paper={PAPER}  ink={INK}\n")
fails = 0
for label, fg, bg, minimum in PAIRS:
    r = ratio(fg, bg)
    ok = r >= minimum
    fails += 0 if ok else 1
    print(f"{'PASS' if ok else 'FAIL'}  {r:5.2f}:1  (min {minimum})  {label}"
          f"   {fg} on {bg}")

# and the one that used to fail, restated for the record
print()
print("previously failing values, for comparison:")
for label, fg, bg in [
    ("WhatsApp brand green", "#FFFFFF", "#1FA855"),
    ("--text-3 original", "#6E7A85", PAPER),
    ("--sun-deep original", "#B96D12", PAPER),
    ("footer original", "#5D6874", INK),
    ("chart --sun original", "#B96D12", PAPER),
    ("--rule original", "#DCD7CC", PAPER),
]:
    print(f"          {ratio(fg, bg):5.2f}:1  {label}   {fg} on {bg}")

print(f"\n{len(PAIRS) - fails}/{len(PAIRS)} pairs pass. FAILURES: {fails}")
sys.exit(1 if fails else 0)
