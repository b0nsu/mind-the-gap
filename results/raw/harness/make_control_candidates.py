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

for tag, text in {"v131": BODY, "t4-minimal": MINIMAL}.items():
    d = OUT / tag / "skill"
    if d.exists():
        shutil.rmtree(d)
    for rel in FILES:
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_text(show(rel))
    (d / "SKILL.md").write_text(text)
    body_words = len(text[end:].split())
    print(f"{tag:11} {len(text.split())} words with frontmatter, {body_words} body words -> {d}")
