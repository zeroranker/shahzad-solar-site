"""Re-encode the project photographs to the size they are actually displayed at.

The six JPEGs are 1280x720 and total ~980 KB, which was 94% of the weight of
/projects/. The largest one is ever rendered at about 580 CSS px wide inside a
two-column grid, so the browser was decoding roughly 2.2x more pixels than it
ever painted, and paying to download the difference on a 3G connection.

960x540 keeps the same 16:9 aspect ratio (so the corrected width/height
attributes stay accurate) and is still comfortably above the rendered size on
every breakpoint.

Run from the project root:  python qa/re-encode-images.py [--restore]
"""
import pathlib
import shutil
import sys
from PIL import Image

SRC = pathlib.Path("site/assets/img/projects")
BACKUP = pathlib.Path("qa/img-originals")
TARGET = (960, 540)
QUALITY = 78

sys.stdout.reconfigure(encoding="utf-8")

if "--restore" in sys.argv:
    for orig in sorted(BACKUP.glob("*.jpg")):
        shutil.copy2(orig, SRC / orig.name)
    print(f"restored {len(list(BACKUP.glob('*.jpg')))} originals")
    raise SystemExit(0)

BACKUP.mkdir(parents=True, exist_ok=True)

before = after = 0
for p in sorted(SRC.glob("*.jpg")):
    (BACKUP / p.name).write_bytes(p.read_bytes())  # one-time safety copy
    with Image.open(p) as im:
        w, h = im.size
        if (w, h) == TARGET:
            continue
        # thumbnail preserves aspect ratio and never upscales
        resized = im.copy()
        resized.thumbnail(TARGET, Image.LANCZOS)
        if resized.size != TARGET:
            print(f"  {p.name}: {w}x{h} -> {resized.size[0]}x{resized.size[1]} "
                  f"(source is not 16:9, left aspect intact)")
    before += p.stat().st_size
    with Image.open(p) as im:
        im.convert("RGB").save(p, "JPEG", quality=QUALITY, optimize=True,
                               progressive=True)
    after += p.stat().st_size
    print(f"  {p.name}: {w}x{h} -> {p.stat().st_size:,} B")

print(f"\ntotal {before:,} B -> {after:,} B  "
      f"({(1 - after / before) * 100:.0f}% smaller)")
print(f"originals kept in {BACKUP.as_posix()} — rerun with --restore to undo")
