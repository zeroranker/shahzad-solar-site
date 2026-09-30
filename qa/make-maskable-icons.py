"""Render the PWA icon sizes from the real brand geometry in favicon.svg.

A manifest with only an SVG icon installs on Android but gets no home-screen
icon on iOS, and "any maskable" on a single vector entry is treated by Chrome
as a claim rather than a measurement. Chrome wants real 192 and 512 PNGs.

This is the favicon's own artwork, traced into PIL: a 40x40 viewBox, dark
rounded square, orange sun at (20,15) r=6 with eight rays, and a white
saw-tooth roofline from x7 to x33. The 512 render is drawn with proportional
fractions and a 10% safe-zone inset for maskable cropping, so the rays are
never clipped when Android crops to a circle or a squircle.

Run from the project root:  python qa/make-maskable-icons.py
"""
import pathlib
from PIL import Image, ImageDraw

OUT = pathlib.Path("site/assets/img")
INK = (14, 18, 22, 255)
SUN = (232, 145, 43, 255)
PAPER = (251, 250, 246, 255)
SS = 4  # supersample factor, downscaled with LANCZOS


def draw_icon(size: int, rounded: bool) -> Image.Image:
    """size = output px. rounded=True for the app icon, False for maskable."""
    s = size * SS
    im = Image.new("RGBA", (s, s), INK if rounded else (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    if rounded:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=s * 0.225, fill=INK)

    # Work in the favicon's own 40-unit space, inset for the maskable safe zone.
    inset = 0 if not rounded else 0
    m = 0.10 if not rounded else 0.02
    u = s * (1 - 2 * m) / 40          # units -> px
    ox = oy = s * m

    def P(x, y):
        return (ox + x * u, oy + y * u)

    def S(v):
        return v * u

    # sun
    sx, sy = P(20, 15)
    r = S(6)
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SUN)

    # eight rays, transcribed from favicon.svg's <path d="...">
    RAYS = [
        (20, 4, 20, 6.4), (20, 23.6, 20, 26),      # vertical
        (9.6, 15, 12, 15), (28, 15, 30.4, 15),      # horizontal
        (12.7, 7.7, 14.4, 9.4), (25.6, 20.6, 27.3, 22.3),   # down-right
        (27.3, 7.7, 25.6, 9.4), (14.4, 20.6, 12.7, 22.3),   # down-left
    ]
    lw = max(2, int(round(S(2))))
    for x0, y0, x1, y1 in RAYS:
        d.line([P(x0, y0), P(x1, y1)], fill=SUN, width=lw)

    # roofline, the favicon's saw-tooth silhouette
    roof = [(7, 34), (14.5, 22.5), (18, 28), (22, 20.5), (33, 34)]
    d.polygon([P(x, y) for x, y in roof], fill=PAPER)

    return im.resize((size, size), Image.LANCZOS)


JOBS = [
    (192, "icon-192.png", True),
    (512, "icon-512.png", True),
    (192, "icon-maskable-192.png", False),
    (512, "icon-maskable-512.png", False),
    (180, "apple-touch-icon.png", True),
]

for size, name, rounded in JOBS:
    path = OUT / name
    draw_icon(size, rounded).save(path, "PNG", optimize=True)
    print(f"  {name:<28} {size}x{size}  {path.stat().st_size:,} B")
