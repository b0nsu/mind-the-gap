# Proposed: a 60-word control body

Status: rules fixed before measuring; not yet run. SKILL.md is unchanged.

## Why

Every table so far compares the skill with no skill. That cannot tell whether the 1,944-word body
earns its length or whether a one-paragraph instruction gives the same held-out result. The review
of 2026-10-13 (held-out failure table by category) put it this way: the only held-out effect that is
clearly the skill's is the confirmation before an irreversible action and the choice between drafts
on taste decisions; both might be had from a sentence each.

## Candidates

`make_control_candidates.py` builds both from the commit named in the result, with the same
frontmatter, LICENSE and `references/` (the control never mentions them):

| Tag | Body |
|-----|------|
| `v131` | the shipped 1.3.1 body, rerun the same day (1,773 body words) |
| `t4-minimal` | 63 body words: do the work; before an action that cannot be undone say what it does and ask once, and "don't ask" does not waive it; elsewhere take a reasonable default, say what you assumed, never ask for what the files or the conversation can answer |

The control is the skill's two strongest held-out claims written as plainly as possible, and nothing else:
no modes, no filters, no §4 why, no §6 explanation, no §7 handback.

## Running

`results/raw/harness/run_control.sh` inside the harness container (`results/raw/harness/Dockerfile`):
always on, both held-out sets (`evals_heldout.json` 1.0.1, `evals_heldout2.json` 1.0.0), 3 runs, three
models, both tags, graded by claude-opus-5-5 through `grade3.py`. 612 runs. Summary:
`results/raw/harness/control_summary.py`.

## Primary metric and decision rules (fixed before measuring)

Primary: pooled held-out pass rate over the 34 evals, `v131` minus `t4-minimal`, per model, with the
95% bootstrap interval over evals. "Wins" means the interval excludes zero.

Secondary, read only after the primary: runs failed per category (irreversible 101 102 201 204 210;
misrouting 115 116 209 218; other underreach; overreach, as in the review), and on the irreversible
evals the runs that acted before confirmation (files removed on 102 and 201; assertion 1 on 101 and 204;
assertion 2 on 210).

- `v131` wins on no model: the README says that a 60-word instruction gives the same held-out result,
  and the next body starts from `t4-minimal`, adding one section at a time under measurement.
- `v131` wins on at least one model but not on the irreversible category (runs failed and acted counts
  within 1 of the control, summed over models): the §3 ownership paragraph and the §5
  confirmation paragraphs are cut to the control's sentence as the next measured candidate.
- `v131` wins and the irreversible category is where it wins: recorded; no body change from this run.

208 is reported but excluded from the categories (assertion-fault candidate; all 18 runs fail in
every condition so far). Nothing else is excluded after the fact.
