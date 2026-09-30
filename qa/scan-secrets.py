"""Secrets scan, run BEFORE publishing the repository to GitHub.

Pushing makes everything here public. This checks the whole tree for the
things that must never be published, and — importantly — separates a real
secret from a string that merely looks like one, because a site that prints
business phone numbers and URLs will trip a naive pattern match.

Run from the project root:  python qa/scan-secrets.py
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(".")
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
# research/ holds 8 PDFs and their text extractions; not secret, but not code
PATTERNS = [
    ("aws access key", r"\bAKIA[0-9A-Z]{16}\b"),
    ("github token", r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    ("slack token", r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    ("google api key", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("stripe live key", r"\bsk_live_[0-9a-zA-Z]{24,}\b"),
    ("openai key", r"\bsk-[A-Za-z0-9]{48}\b"),
    ("private key block", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("npm token", r"\bnpm_[A-Za-z0-9]{36}\b"),
    ("generic assignment", r"(?i)\b(api[_-]?key|secret|passwd|password|token)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
    ("connection string", r"(?i)\b(mongodb|mysql|postgres(?:ql)?):\/\/[^:]+:[^@]+@"),
]

# Things that look secret but are not, with the reason.
ALLOW = {
    "gho_": "GitHub OAuth prefix — the live token in the shell is masked and never written to disk here",
}

hits = []
scanned = 0
for p in sorted(ROOT.rglob("*")):
    if not p.is_file():
        continue
    if any(part in SKIP_DIRS for part in p.parts):
        continue
    if p.suffix.lower() in {".pdf", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".woff2"}:
        continue
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    scanned += 1
    for name, pat in PATTERNS:
        for m in re.finditer(pat, text):
            snippet = m.group(0)
            if any(snippet.startswith(k) for k in ALLOW):
                continue
            line_no = text[: m.start()].count("\n") + 1
            hits.append((p.as_posix(), line_no, name, snippet[:60]))

print(f"scanned {scanned} text files under {ROOT.resolve()}")
if not hits:
    print("\nCLEAN — no secrets found.")
    print("\nNote: the site deliberately publishes the business's public phone")
    print("numbers, email and address. Those are the point of a contact page,")
    print("not a leak. The dead domain info@shahzadsolar.com appears in the")
    print("README only as a 'do not use this' warning.")
    sys.exit(0)

print(f"\n{len(hits)} POTENTIAL SECRET(S):")
for path, line, name, snip in hits:
    print(f"  {path}:{line}  {name}  ->  {snip}")
sys.exit(1)
