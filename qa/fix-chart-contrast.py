"""One-off: raise the contrast of every colour in the "Your solar day" chart.

The chart is drawn as inline SVG, so it could not be fixed by a CSS token
change alone. Measured against the paper background:
  --sun   2.361:1  stroke  -> unreadable at 2.5px
  --rule  1.108:1  gridlines -> invisible, and invisible gridlines read as
                            "no data" rather than as a quiet frame
  --text-3 4.202:1 tick labels -> below the 4.5:1 body-text floor

Each is repointed at a token that already passes. Run from the project root.
"""
import pathlib

JS = pathlib.Path("site/assets/js/site.js")
text = JS.read_text(encoding="utf-8")

# The load curve: --sun is a fill colour, so it is darkened to --sun-deep.
# The gridlines and the axis rule: --rule -> a dedicated --rule-chart.
# The tick labels: --text-3 -> --text-2.
pairs = [
    ('" stroke="var(--rule)" stroke-width="1"/>',
     '" stroke="var(--rule-chart)" stroke-width="1"/>'),
    ('" fill="none" stroke="var(--sun)" stroke-width="2.5" stroke-linejoin="round"/>',
     '" fill="none" stroke="var(--sun-deep)" stroke-width="2.5" stroke-linejoin="round"/>'),
    ('\'font-size="11" fill="var(--text-3)" font-family="var(--mono)">\'',
     '\'font-size="11" fill="var(--text-2)" font-family="var(--mono)">\''),
]

for old, new in pairs:
    n = text.count(old)
    if n == 0:
        print("  NOT FOUND:", old[:60])
    else:
        text = text.replace(old, new)
        print(f"  replaced {n}x: {old[:52]}")

JS.write_text(text, encoding="utf-8")

CSS = pathlib.Path("site/assets/css/site.css")
css = CSS.read_text(encoding="utf-8")
if "--rule-chart" not in css:
    anchor = "  --rule-strong: #8E897E;"
    css = css.replace(
        anchor,
        anchor
        + "\n  /* Chart gridlines and axis rule only. --rule is too faint at 1.11:1 to"
        + "\n     read as a frame; this is the same hairline, at 3:1. */"
        + "\n  --rule-chart: #969186;",
        1,
    )
    CSS.write_text(css, encoding="utf-8")
    print("  added --rule-chart: #969186 to site.css")
else:
    print("  --rule-chart already defined")
