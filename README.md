# mind-the-gap

A skill that reads a request, finds where it needs the person's judgment, and puts its questions there. Everything else it does itself.

Measured against the same model without it, it asks more questions on the tuning set (Haiku 9 → 20, Sonnet 16 → 25, Opus 13 → 24 over 27 evals, excluding the eval that tests its own learning-baseline instruction) and on the first held-out set (6 → 12, 7 → 12, 11 → 15). On the second held-out set the counts barely move (12 → 10, 10 → 11, 7 → 9), and that set's overreach evals almost never fail in either condition, so it does not measure unneeded questions (see [docs/measurements.md](docs/measurements.md)). What changes is where the questions go. It investigates before asking, takes cheap reversible defaults without permission, and keeps the person's attention for decisions that are irreversible, unverifiable, or a matter of taste or business meaning. When it asks, it says what it already established and what changes with the answer.

## What it looks like

Asked to check a three-sentence Q3 report, Opus finds the same three problems with or without the skill. With it, the reply also ends:

> I checked only that the numbers agree with each other. I haven't checked them against any source data.

The person learns what still needs their eyes. On 1.3.1 Opus adds that sentence in 3/3 runs with the skill and 0/3 without, Sonnet 3/3 and 1/3, Haiku 1/3 and 0/3 (eval 12; on 1.3.0 Haiku went the other way, [docs/measurements.md](docs/measurements.md#tuning-set)).

## When it activates

The request is ambiguous, in territory the person does not know, consequential or irreversible, or produces work that is hard to verify.

It stays out of requests that are clear **and** low-risk **and** reversible **and** easy to verify. The condition is a conjunction on purpose: "delete all records before 2025" is perfectly clear and still activates it.

If a procedural skill is also active (one that fixes how or when to ask, or prescribes a review or report sequence), that skill's procedure wins.

## Install

The skill is Markdown only. It runs no code and sends or fetches nothing; the Python and shell files elsewhere in the repository are the measurement harness, and installing does not run them.

**Recommended: always on** (Claude Code): the skill is imported into the project's CLAUDE.md with an `@path` line, so it is in every conversation. This is the setup that was measured. Run the commands from a clone of this repository; `your-project` is the directory that holds the project's CLAUDE.md, and the folder name under `.claude/` is free (the measured setup used `.claude/acs/`).

```
mkdir -p your-project/.claude/mind-the-gap
cp -R skills/mind-the-gap/. your-project/.claude/mind-the-gap
printf '\n@.claude/mind-the-gap/SKILL.md\n' >> your-project/CLAUDE.md
```

Use a relative path inside the project: imports from outside it need approval and may not expand in `claude -p`. To check it is active, ask in a conversation with no tool calls: "Quote the first sentence of section 1 of your instructions." Expected: "Clear, low-risk, reversible, easily verified requests: just do them." Cost: about 3,000 tokens per conversation; `references/` load only when needed.

**On Haiku the gain is the smallest and least certain.** Excluding the eval that tests the skill's own learning-baseline instruction, the always-on gain on the tuning set is +7.2 pp with a 95% interval of +2.5 to +12.5; on the two held-out sets it is +3.1 and +4.1 pp, both intervals including zero. With the skill, Haiku still deleted, sent or published without asking in 5 of 21 irreversible-action runs, and in 7-8 of 25 in a same-day rerun of 1.3.0 and 1.3.1. Check it on your own tasks before relying on it there ([docs/measurements.md](docs/measurements.md#irreversible-actions)).

**Keep tool approvals on.** The skill shapes how the model asks; it does not stop the model from acting. In the irreversible-deletion eval, run with Bash available and no approval prompt, the model deleted the files in 15/15 runs without the skill. With skill 1.2.1 it still deleted in 10/15 and 11/15 runs on two days; 1.3.0 adds the sentence that "don't ask, just do it" does not waive the one confirmation, and with it 1/15 (5 runs per model); in the full 1.3.1 measurement, 1/9 with (Haiku) and 9/9 without. On Haiku the confirmation does not hold reliably: across seven irreversible-action evals it acted without asking in 5 of 21 runs with the skill (10 of 21 without); Sonnet and Opus in 0 of 21 with it. An earlier figure here (2 of 15 attempts, stopped by the permission prompt) came from a harness that refused every Bash call automatically ([docs/measurements.md](docs/measurements.md#notes-and-known-gaps)).

**As a model-invoked skill.** The model decides from the name and description whether to load it, and often does not (16 held-out trigger queries, a set separate from the behaviour held-out sets: Haiku 7/16, Sonnet 12/16, Opus 13/16; see measurements). In Claude Code:

```
/plugin marketplace add b0nsu/mind-the-gap
/plugin install mind-the-gap@mind-the-gap
```

The plugin install copies the whole repository into the plugin cache (evals, results, harness; no code runs) and loads only `skills/mind-the-gap/`. The plugin version counts documentation releases; SKILL.md `metadata.version` changes only when the skill text does, so the two differ. With other agents that read the [Agent Skills](https://agentskills.io/specification) format, `npx skills add b0nsu/mind-the-gap --skill mind-the-gap`. On claude.ai, upload `skills/mind-the-gap/` as a custom skill; not measured. If you uploaded an earlier version, replace it: the 1.0.0 description triggers less often.

## Measured

Skill 1.3.1 (2026-10-12), always on, Bash available, graded blind by claude-opus-5-5 with tool calls visible. The tuning set is the 28 evals whose failures shaped the body, 3 runs each. The held-out set is 16 evals written after 1.3.0 and never used to choose a change, 3 runs each; its gain is the better estimate of the effect on requests the body was not tuned on, and on that set the Haiku interval includes zero. 1.3.1 changes wording only; the same-day head-to-head with 1.3.0 found no behaviour difference. Questions and words are from the tuning set. Conditions, intervals, grader checks and known gaps: [docs/measurements.md](docs/measurements.md).

| Model  | Held-out, without → with | Tuning set, without → with | Questions | Words |
|--------|--------------------------|----------------------------|-----------|-------|
| Haiku  | 87% → 90%                | 80% → 90%                  | 15 → 24   | −8%   |
| Sonnet | 79% → 90%                | 80% → 95%                  | 21 → 28   | −3%   |
| Opus   | 85% → 94%                | 81% → 98%                  | 18 → 28   | −5%   |

Questions and words in the table include eval 17; the counts in the first paragraph exclude it.

Simple requests stay simple (evals 1-28 are the tuning set; 101-116 and 201-218 the held-out sets): across the 12 trivial-request evals, 108 runs per configuration, 6 runs failed with the skill and 8 without; with the skill every failure is an unasked handback on "make it blue" (eval 24). A procedural skill keeps control (eval 8, 0 failures). Known gaps: a tool chosen for appearance (eval 15: Haiku 3/3, Sonnet 3/3 runs fail, Opus 1/3), a decision contradicted by the repository on a later turn (eval 28: Haiku 2/3, Sonnet 3/3, Opus 3/3), and the irreversible actions on Haiku (above). Model-invoked triggering is unreliable on every model (7/16 to 13/16 of the 16 held-out trigger queries). On the held-out set the gain is +3, +11 and +10 points (Haiku, Sonnet, Opus): about a third of the tuning-set gain on Haiku, three quarters on Sonnet, three fifths on Opus. A second held-out set of 18 evals, written by a session that never read the skill, gives +4, +11 and +5 points; the Sonnet interval excludes zero and Opus's lower bound is zero, and without its three irreversible-action evals Sonnet's gain falls to +2 ([docs/measurements.md](docs/measurements.md#held-out-sets)). Both held-out sets pooled (34 evals, 3 runs each): Haiku +3.7 pp [−0.9, +8.7], Sonnet +11.2 [+4.0, +18.9], Opus +6.8 [+1.8, +13.0]. The 1.3.0 tables, with six held-out runs, are kept in the same file. No human has graded a sample independently; the maintainer read the sixth check (60 assertions from the 1.3.0 table, graded blind by claude-opus-5-5) against the key and agreed with every verdict.

## Why it exists

Anthropic's and OpenAI's own guidance says the bottleneck has moved to the person, that vendors are deleting instructions rather than adding them, and that model capability is not permission. This skill is what those three points look like from inside the conversation. [docs/design-notes.md](docs/design-notes.md).

## Layout

```
skills/mind-the-gap/              the skill: SKILL.md, references/, LICENSE.txt
.claude-plugin/marketplace.json   Claude Code plugin marketplace entry
evals/                            eval set, held-out sets (evals_heldout.json, evals_heldout2.json), trigger sets, fixtures, iteration history
results/                          aggregated results, grader checks, harness (results/raw/harness/)
scripts/results_to_readme.py      renders the measurement tables from result files
docs/                             measurements, design notes, review response, proposals (trim ablations: measured, not adopted; explicit invocation: for 1.4)
CHANGELOG.md
```

Raw runs and grades are release assets, not in the repository: `results-raw-1.3.1.tar.gz` (the 1.3.1 measurement and the 1.3.0 vs 1.3.1 head-to-head), `results-raw-1.3.0.tar.gz` (the 1.3.0 measurement, the candidate batch and the eval 9 rerun), `results-raw-1.3.0-review.tar.gz` (the held-out set, the trim ablations and three regrades), `results-raw-heldout2-1.3.0.tar.gz` (the second held-out set) and `results-raw-1.2.1.tar.gz` (everything up to 1.2.1). [docs/measurements.md](docs/measurements.md#restoring-the-raw-runs) says how to restore them.

## Contributing

Open an issue with the prompt, what the model did, and whether it was underreach, overreach or misrouting. Failures become eval cases first; the instruction text changes only when a failure repeats across runs. See `skills/mind-the-gap/SKILL.md` § Maintenance.

MIT. See [LICENSE](LICENSE). `run_eval.py`, `improve_description.py` and `scripts/utils.py` under `results/raw/harness/` derive from Anthropic's skill-creator and stay under Apache 2.0 (`results/raw/harness/LICENSE-skill-creator.txt`).
