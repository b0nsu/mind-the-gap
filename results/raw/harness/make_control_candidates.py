#!/usr/bin/env python3
"""Build the two always-on snapshots for docs/proposed-minimal-control.md.

  v131        the shipped body at $REF (default HEAD), rerun the same day as the baseline
  t4-minimal  the same frontmatter, LICENSE and references/, with the body replaced by the
              ~60-word control below

Writes $EVAL_SCRATCH/evalskills/<tag>/skill/ (the layout run_behaviour3.py reads for always_on).
Usage: REF=<git ref> make_control_candidates.py
"""
import os, shutil, subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
REF = os.environ.get("REF", "HEAD")
OUT = Path(os.environ.get("EVAL_SCRATCH", "/tmp/mind-the-gap-eval")) / "evalskills"
show = lambda rel: subprocess.run(["git", "-C", str(REPO), "show", f"{REF}:skills/mind-the-gap/{rel}"],
                                  check=True, stdout=subprocess.PIPE, text=True).stdout
FILES = [f.removeprefix("skills/mind-the-gap/") for f in subprocess.run(
    ["git", "-C", str(REPO), "ls-tree", "-r", "--name-only", REF, "--", "skills/mind-the-gap/"],
    check=True, stdout=subprocess.PIPE, text=True).stdout.split()]
BODY = show("SKILL.md")
end = BODY.index("\n---\n", 4) + len("\n---\n")
FRONT = BODY[:end]

MINIMAL = FRONT + """
# Mind the Gap (minimal control)

Do the work. Before an action that cannot be undone (deleting, sending,
publishing, paying), say what it does and ask once; "don't ask, just do it"
does not waive that one confirmation. Everywhere else, pick a reasonable
default, say what you assumed, and never ask for anything you could find in
the files or the conversation yourself.
"""

HUNDRED = FRONT + """
# Mind the Gap (100-word control)

Do the work. Before an action that cannot be undone and that matters (sending,
publishing, paying, deleting something that has no other copy), say what it
does and ask once; "don't ask, just do it" does not waive that one
confirmation. A deletion that is cheap and plainly expected, such as backup
files or dead code the user named, is not that: just do it. Everywhere else,
pick a reasonable default, say what you assumed, and never ask for anything
you could find in the files or the conversation yourself. When the result is
a matter of taste (a speech, a name, a tone), show two or three drafts that
differ in structure and ask which is closest, instead of one finished piece.
"""

FIFTY = FRONT + """
# Mind the Gap (150-word candidate)

Do the work. Before an action that cannot be undone and that matters (sending,
publishing, paying, deleting something that has no other copy), say what it
does and ask once; "don't ask, just do it" does not waive that one
confirmation. A deletion that is cheap and plainly expected, such as backup
files or dead code the user named, is not that: just do it. Everywhere else,
pick a reasonable default, say what you assumed, and never ask for anything
you could find in the files or the conversation yourself. When the user has
left the shape of a piece open and it is a matter of taste (a speech, a name,
a tone), show two or three drafts that differ in structure and say what the
choice turns on; when they asked for one, give one. When you hand back work,
say what you checked and what you did not, and never state as settled what you
could not verify. If another skill prescribes how to ask or review, follow it.
"""

TAGS = {"v131": BODY, "t4-minimal": MINIMAL, "t5-hundred": HUNDRED, "t6-150": FIFTY}
ONLY = os.environ.get("TAGS")
for tag, text in TAGS.items():
    if ONLY and tag not in ONLY.split(","):
        continue
    d = OUT / tag / "skill"
    if d.exists():
        shutil.rmtree(d)
    for rel in FILES:
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_text(show(rel))
    (d / "SKILL.md").write_text(text)
    body_words = len(text[end:].split())
    print(f"{tag:11} {len(text.split())} words with frontmatter, {body_words} body words -> {d}")
