#!/usr/bin/env python3
"""Rewrite a raw-run release tarball with local identifiers replaced, then list every
email address left in it so the packer can check them before uploading.
Usage: SCRUB_EMAILS=a@x,b@y scrub_asset.py <in.tar.gz> <out.tar.gz>
  SCRUB_EMAILS  addresses to replace with USER@example.com. `claude -p` hands the model the
                account email, and models write it into answers (held-out 106, 216), so pass
                the account email of whoever ran the harness.
Paths: /Users/<name> -> ~, /private/tmp/claude-<uid>/ and /var/folders/../T/ -> $TMP/.
Member order, names, modes and mtimes are kept; only file contents change."""
import io, os, re, sys, tarfile

SRC, DST = sys.argv[1], sys.argv[2]
EMAILS = [e.strip() for e in os.environ.get("SCRUB_EMAILS", "").split(",") if e.strip()]
SUBS = [(re.compile(re.escape(e).encode(), re.I), b"USER@example.com") for e in EMAILS] + [
    (re.compile(rb"/private/tmp/claude-\d+/"), b"$TMP/"),
    (re.compile(rb"/var/folders/[\w]+/[\w]+/T/"), b"$TMP/"),
    (re.compile(rb"/Users/[^/\s\"'\\]+"), b"~"),
]
EMAIL = re.compile(rb"[\w.%+-]+@[\w-]+(?:\.[\w-]+)+")

changed, left = 0, {}
with tarfile.open(SRC) as tin, tarfile.open(DST, "w:gz") as tout:
    for m in tin:
        if not m.isfile():
            tout.addfile(m)
            continue
        b = tin.extractfile(m).read()
        nb = b
        for pat, rep in SUBS:
            nb = pat.sub(rep, nb)
        if nb != b:
            changed += 1
        for e in EMAIL.findall(nb):
            left[e] = left.get(e, 0) + 1
        m.size = len(nb)
        tout.addfile(m, io.BytesIO(nb))

print(f"{changed} files changed")
print("emails left (check each is public or synthetic):")
for e, n in sorted(left.items(), key=lambda x: -x[1]):
    print(f"  {n:5d}  {e.decode(errors='replace')}")
