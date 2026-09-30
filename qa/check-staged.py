"""Verify the staged (index) content matches the working tree byte-for-byte
in terms of text content.

Git's eol=lf normalisation rewrites line endings in the index. That is
desirable, but this project has been destroyed once already by an encoding
round-trip, and a `.gitattributes` rule is exactly the kind of thing that
silently rewrites files. So this reads the staged blobs back out of the index
and compares them to the working files, ignoring only CR characters.

Any difference beyond CR would mean the commit is not what is on disk.

Run from the project root:  python qa/check-staged.py
"""
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

TEXT = (".html", ".css", ".js", ".md", ".py", ".txt", ".xml",
        ".webmanifest", ".svg", ".gitignore", ".gitattributes")

names = subprocess.run(
    ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
).stdout.split()

problems = 0
checked = 0
for name in names:
    if not name.lower().endswith(TEXT):
        continue
    blob = subprocess.run(
        ["git", "show", f":{name}"],
        capture_output=True,
    ).stdout
    try:
        staged = blob.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"  NOT UTF-8 IN INDEX: {name}  ({exc})")
        problems += 1
        continue
    try:
        ondisk = open(name, "rb").read().decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"  NOT UTF-8 ON DISK : {name}  ({exc})")
        problems += 1
        continue

    checked += 1
    if staged.replace("\r\n", "\n") != ondisk.replace("\r\n", "\n"):
        problems += 1
        print(f"  CONTENT DIFFERS  : {name}")
        if "�" in staged:
            print("      replacement character present in the staged blob")

print(f"compared {checked} text files, {problems} problem(s)")
if problems == 0:
    # spot-check that Urdu survived, using a known string
    out = subprocess.run(
        ["git", "show", ":site/ur/index.html"],
        capture_output=True,
    ).stdout.decode("utf-8", errors="replace")
    ok = "منظور شدہ لوڈ" in out and "�" not in out
    print(f"Urdu integrity in staged ur/index.html: "
          f"{'OK' if ok else 'FAILED'}")
    if not ok:
        problems += 1

print("\nSTAGED CONTENT MATCHES DISK" if problems == 0
      else f"\n{problems} PROBLEM(S)")
sys.exit(0 if problems == 0 else 1)
