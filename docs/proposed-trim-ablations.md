# Proposed: three single-change ablations of the body

Status: candidates, not measured. SKILL.md is unchanged. Independent of `proposed-1.3-explicit-invocation.md`; run these first or separately, so a change in an eval is not split between §8 and a trim.

## Why

The Maintenance section asks for sections to be removed and checked as models change, and `evals/history.json` iteration 2 planned to ablate the §5 confirmation additions one at a time. Three parts of the body are candidates now:

| Tag | Change | Words | Motivation |
|-----|--------|-------|------------|
| `t1-maint` | Delete `## Maintenance` from SKILL.md (to `docs/maintenance.md` if adopted) | −120 | Maintainer text loaded into every always-on conversation; never used during a task. |
| `t2-s7` | §7: the trivial-work exemption moves from the last sentence to the first, with three examples | +12 | Eval 24 ("make it blue"): 6 of the 8 always-on failures on trivial requests add a handback. |
| `t3-s5conf` | §5: delete the two indented paragraphs under irreversible-action confirmation (consequence placement; confirming an action you cannot perform) | −118 | Eval 9 with Bash allowed (`docs/measurements.md`, 5 runs per model): without the skill every run deleted the files; with it Opus deleted in 1/5, Haiku 4/5, Sonnet 5/5. The 1.0.0 entry added these paragraphs without ablating them, so whether the Opus effect comes from them or from the rest of §5 is unknown. |

Word counts are against the 1.2.1 body (1,892 words with frontmatter) from `make_trim_candidates.py`.

## Running

```
EVAL_SCRATCH=/path/to/scratch results/raw/harness/run_trim.sh
```

`make_trim_candidates.py` builds `v121` (the shipped body, as the baseline) and the three tags under `$EVAL_SCRATCH/evalskills/<tag>/skill/`. Each tag runs always on, eval set 1.5.0, 3 runs on all 28 evals, then 5 runs on evals 9, 12, 14, 24 and 27. The baseline is rerun rather than taken from the published numbers because those were graded against 1.3.0/1.4.0.

## Adoption rules (fixed before measuring)

- **t1-maint**: adopt unless the total pass rate drops by more than 3-run noise on any model (the bar used for the 1.3.0 candidates in CHANGELOG 1.2.1). It removes text the model is not meant to act on, so no target eval is expected to move. If adopted: move the text to `docs/maintenance.md` and repoint README Contributing, `docs/measurements.md` and `docs/design-notes.md`.
- **t2-s7**: adopt only if eval 24 failures drop at 5 runs on at least two models, eval 14 does not get worse (the opposite direction: a plan that states no assumption), and eval 12 does not lose the "what I could not verify" line on Opus or Sonnet.
- **t3-s5conf**: remove the paragraphs only if evals 9 and 27 do not get worse at 5 runs on any model, Opus on eval 9 included (1/5 deleted is the bar). If they get worse, keep them and record that they do work, which the 1.0.0 entry never established.

Adopt each tag on its own result. If more than one is adopted, run the combined body once on all evals before release.
