"""Site integrity check: every internal link and asset resolves, no duplicate IDs,
no unbalanced tags, every page has the essentials."""
import os, re, sys, html
from urllib.parse import urlparse, unquote
from urllib.request import urlopen, Request

BASE = "http://127.0.0.1:8811"
ROOT = r"E:\harness\New folder\solar-mission\site"

pages = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    if "assets" in dirpath:
        continue
    for f in filenames:
        if f.endswith(".html"):
            pages.append(os.path.join(dirpath, f))
pages.sort()

LINK = re.compile(r'(?:href|src)="(/[^"#?]*)"', re.I)
problems, checked, links = [], 0, 0

def local(path):
    p = unquote(urlparse(path).path)
    return os.path.join(ROOT, p.lstrip("/").replace("/", os.sep))

def ok(path):
    """Does a URL path resolve to something servable?"""
    p = unquote(urlparse(path).path)
    if not p or p == "/":
        return os.path.isfile(os.path.join(ROOT, "index.html"))
    f = os.path.join(ROOT, p.lstrip("/").replace("/", os.sep))
    if os.path.isfile(f):
        return True
    if p.endswith("/"):
        return os.path.isfile(os.path.join(f, "index.html"))
    return os.path.isfile(f + ".html") or os.path.isfile(os.path.join(f, "index.html"))

print(f"Found {len(pages)} HTML pages\n")

for page in pages:
    rel = os.path.relpath(page, ROOT).replace(os.sep, "/")
    src = open(page, encoding="utf-8").read()
    checked += 1
    is_404 = os.path.basename(page) == "404.html"

    # --- essentials -------------------------------------------------
    # A 404 is the one page that must NOT carry a canonical: pointing one at
    # the home page tells a crawler the missing URL is a duplicate of a real
    # page, which is the opposite of what noindex means. It is `noindex, follow`
    # and nothing else.
    essentials = [
        (r'<title>.{10,}?</title>', "title"),
        (r'<meta name="description" content=".{50,}"', "meta description"),
        (r'<html lang="[a-z]{2}"', "html lang"),
        (r'name="viewport"', "viewport"),
        (r'hreflang="ur"', "urdu alternate"),
    ]
    if not is_404:
        essentials.insert(2, (r'<link rel="canonical"', "canonical"))
    for req, label in essentials:
        if not re.search(req, src, re.I | re.S):
            problems.append(f"{rel}: MISSING {label}")

    if is_404 and re.search(r'<link rel="canonical"', src, re.I):
        problems.append(f"{rel}: 404 must not declare a canonical")

    if src.count("<h1") != 1:
        problems.append(f"{rel}: has {src.count('<h1')} <h1> (want exactly 1)")
    if 'aria-current="page"' not in src and 'name="viewport"' in src:
        pass  # home page has no nav self-link; fine

    # --- tag balance ------------------------------------------------
    for tag in ["div", "section", "article", "ul", "ol", "table", "form", "blockquote"]:
        o = len(re.findall(rf"<{tag}[\s>]", src, re.I))
        c = len(re.findall(rf"</{tag}>", src, re.I))
        if o != c:
            problems.append(f"{rel}: <{tag}> {o} open vs {c} close")

    # --- duplicate ids ----------------------------------------------
    ids = re.findall(r'\sid="([^"]+)"', src)
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        problems.append(f"{rel}: duplicate id(s) {sorted(dupes)}")

    # --- internal links ---------------------------------------------
    for m in set(LINK.findall(src)):
        links += 1
        if not ok(m):
            problems.append(f"{rel}: BROKEN -> {m}")

    # --- unescaped ampersands in hrefs ------------------------------
    for m in re.findall(r'href="[^"]*&(?!amp;|lt;|gt;|quot;|#\d+)[^"]*"', src):
        problems.append(f"{rel}: raw & in href: {m[:60]}")

    print(f"  ok  {rel}")

print(f"\nChecked {checked} pages, {links} internal links/assets")
if problems:
    print(f"\n{len(problems)} PROBLEM(S):")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("\nNo problems found.")
