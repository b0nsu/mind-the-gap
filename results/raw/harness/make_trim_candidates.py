#!/usr/bin/env python3
"""Build the always-on candidates for docs/proposed-trim-ablations.md.

Each tag differs from the 1.2.1 body (git tag v1.2.1) by exactly one change, so a difference in
an eval can be attributed to that change. Writes $EVAL_SCRATCH/evalskills/<tag>/skill/
(SKILL.md, references/, LICENSE.txt), the layout run_behaviour3.py reads for always_on.
No plugin/ wrapper is built, so these tags cannot run the with_skill config.
references/ and LICENSE.txt are copied from the working tree; only SKILL.md changed between 1.2.1 and 1.3.0.

Usage: make_trim_candidates.py
"""
import os, shutil, subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / "skills/mind-the-gap"
OUT = Path(os.environ.get("EVAL_SCRATCH", "/tmp/mind-the-gap-eval")) / "evalskills"
BODY = subprocess.run(["git", "-C", str(REPO), "show", "v1.2.1:skills/mind-the-gap/SKILL.md"],
                      check=True, capture_output=True, text=True).stdout


def cut_from(text, marker):
    i = text.index(marker)
    assert text.count(marker) == 1, marker
    return text[:i].rstrip("\n") + "\n"


def replace_once(text, old, new):
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


S5_PLACEMENT = """
  The consequence lives in exactly one place: the sentence that states what
  the action does. Do not also give it as the reason you are asking ("because
  this can't be undone") and do not repeat it in the confirmation line. The
  confirmation line is bare — "Proceed?" or "Confirm and I'll run it." — and
  the whole exchange, including any plan, stays short enough that the
  consequence is the only thing the user has to weigh.

  When you ask to confirm an irreversible action you cannot perform
  yourself, say so plainly before the consequence, and make the
  confirmation about what you will actually do ("Confirm and I'll give you
  the commands."), not about an action you cannot take.
"""

S7_OLD = """For substantial work, the final response makes clear, in proportion to the
task:"""
S7_NEW = """Skip this for trivial work (a one-line edit, a lookup, a conversion): the
result is the whole reply. For substantial work, the final response makes clear, in
proportion to the task:"""

CANDIDATES = {
    # Baseline: the shipped 1.2.1 body, rerun on eval set 1.5.0.
    "v121": BODY,
    # t1: Maintenance is maintainer text; move it to docs/ if adopted.
    "t1-maint": cut_from(BODY, "## Maintenance"),
    # t2: the trivial-work exemption first, with examples, instead of last.
    "t2-s7": replace_once(
        replace_once(BODY, S7_OLD, S7_NEW),
        "when verification was not possible, say so rather than leaving it implicit.\nNothing of this for trivial work.\n",
        "when verification was not possible, say so rather than leaving it implicit.\n"),
    # t3: the two placement paragraphs under irreversible-action confirmation.
    "t3-s5conf": replace_once(BODY, S5_PLACEMENT, ""),
}

base_words = len(BODY.split())
for tag, text in CANDIDATES.items():
    d = OUT / tag / "skill"
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(SRC, d)
    (d / "SKILL.md").write_text(text)
    w = len(text.split())
    print(f"{tag:10s} {w:5d} words ({w - base_words:+d})  {d}")
