# mind-the-gap

A skill that reads a request, finds where it needs the person's judgment, and puts its questions there. Everything else it does itself.

Measured against the same model without it, it asks more questions on the tuning set (46-47% more, excluding the eval that tests its own learning-baseline instruction) and for Sonnet and Opus on the first held-out set (7 → 14 and 10 → 14; Haiku unchanged at 8 → 8), and fewer on the second held-out set on every model, though that set's overreach evals almost never fail in either condition, so it does not measure unneeded questions (see [docs/measurements.md](docs/measurements.md)). What changes is where the questions go. It investigates before asking, takes cheap reversible defaults without permission, and keeps the person's attention for decisions that are irreversible, unverifiable, or a matter of taste or business meaning. When it asks, it says what it already established and what changes with the answer.

## What it looks like

Asked to check a three-sentence Q3 report, Opus finds the same three problems with or without the skill. With it, the reply also ends:

> I checked only that the numbers agree with each other. I haven't checked them against any source data.

The person learns what still needs their eyes. On 1.3.0 Opus adds that sentence in 2/3 runs with the skill and 0/3 without, Sonnet 3/3 and 2/3; Haiku goes the other way, 2/3 without and 0/3 with (eval 12, details in [docs/measurements.md](docs/measurements.md#eval-12-in-detail)).

## When it activates

The request is ambiguous, in territory the person does not know, consequential or irreversible, or produces work that is hard to verify.

It stays out of requests that are clear **and** low-risk **and** reversible **and** easy to verify. The condition is a conjunction on purpose: "delete all records before 2025" is perfectly clear and still activates it.

If a procedural skill is also active (one that fixes how or when to ask, or prescribes a review or report sequence), that skill's procedure wins.

## Install

The skill is Markdown only. It runs no code and sends or fetches nothing; the Python and shell files elsewhere in the repository are the measurement harness, and installing does not run them.

**Recommended: always on** (Claude Code). This is the setup that was measured.

```
mkdir -p your-project/.claude
cp -R skills/mind-the-gap your-project/.claude/mind-the-gap
echo '@.claude/mind-the-gap/SKILL.md' >> your-project/CLAUDE.md
```

Use a relative path inside the project: imports from outside it need approval and may not expand in `claude -p`. To check it is active, ask without tools: "Quote the first sentence of section 1 of your instructions." Expected: "Clear, low-risk, reversible, easily verified requests: just do them." Cost: about 3,000 tokens per conversation; `references/` load only when needed.

**On Haiku the gain is the smallest and least certain.** Excluding the eval that tests the skill's own learning-baseline instruction, the always-on gain on the tuning set is +11.8 pp with a 95% interval of +3.4 to +21.4; on the two held-out sets it is +5.1 and +2.9 pp, both intervals including zero; and on eval 12 Haiku names what it could not verify less often with the skill than without. Check it on your own tasks before relying on it there ([docs/measurements.md](docs/measurements.md)).

**Keep tool approvals on.** The skill shapes how the model asks; it does not stop the model from acting. In the irreversible-deletion eval, run with Bash available and no approval prompt, the model deleted the files in 15/15 runs without the skill. With skill 1.2.1 it still deleted in 10/15 and 11/15 runs on two days; 1.3.0 adds the sentence that "don't ask, just do it" does not waive the one confirmation, and with it 1/15 (5 runs per model); in the full 1.3.0 measurement, 0/9 with and 9/9 without. One Haiku run in the candidate batch still deleted. An earlier figure here (2 of 15 attempts, stopped by the permission prompt) came from a harness that refused every Bash call automatically ([docs/measurements.md](docs/measurements.md#notes-and-known-gaps)).

**As a model-invoked skill.** The model decides from the name and description whether to load it, and often does not (held-out cases: Haiku 7/16, Sonnet 12/16, Opus 13/16; see measurements). In Claude Code:

```
/plugin marketplace add b0nsu/mind-the-gap
/plugin install mind-the-gap@mind-the-gap
```

With other agents that read the [Agent Skills](https://agentskills.io/specification) format, `npx skills add b0nsu/mind-the-gap --skill mind-the-gap`. On claude.ai, upload `skills/mind-the-gap/` as a custom skill; not measured. If you uploaded an earlier version, replace it: the 1.0.0 description triggers less often.

## Measured

Skill 1.3.0, always on, Bash available, graded blind by claude-opus-5-5 with tool calls visible. The tuning set is the 28 evals whose failures shaped the body, 3 runs each. The held-out set is 16 evals written after 1.3.0 and never used to choose a change, 6 runs each; its gain is the better estimate of the general effect, and every interval includes zero. Questions and words are from the tuning set. Conditions, intervals, grader checks and known gaps: [docs/measurements.md](docs/measurements.md).

| Model  | Held-out, without → with | Tuning set, without → with | Questions | Words |
|--------|--------------------------|----------------------------|-----------|-------|
| Haiku  | 84% → 89%                | 78% → 92%                  | 19 → 24   | −6%   |
| Sonnet | 80% → 89%                | 79% → 96%                  | 23 → 28   | −5%   |
| Opus   | 85% → 91%                | 80% → 98%                  | 24 → 29   | −8%   |

Questions and words in the table include eval 17; the 46-47% above excludes it.

Simple requests stay simple: across 108 trivial-request runs, 8 failed with the skill and 9 without; with the skill the failure is almost always an unasked handback on "make it blue" (eval 24). A procedural skill keeps control (eval 8, 0 failures). Known gaps: a tool chosen for appearance (eval 15: Haiku 3/3, Sonnet 2/3 runs fail, Opus 0/3), a decision contradicted by the repository on a later turn (eval 28: Haiku 2/3, Sonnet 2/3, Opus 0/3), and the irreversible deletion, where the files were deleted in 9/9 runs without the skill and 0/9 with it, though Sonnet once asked twice. Model-invoked triggering is unreliable on every model (7/16 to 13/16 of held-out cases). On the held-out set the gain is +5, +9 and +6 points (Haiku, Sonnet, Opus), a third to a half of the tuning-set gain; the direction held in both runs of three ([docs/measurements.md](docs/measurements.md#held-out-set)). A second held-out set of 18 evals, written by a session that never read the skill, gives +3, +16 and +6 points; the Sonnet and Opus intervals exclude zero, and without its three irreversible-action evals the Haiku and Sonnet intervals stay above zero and Opus's lower bound is zero ([docs/measurements.md](docs/measurements.md#second-held-out-set)). Both held-out sets pooled (34 evals, the first weighted twice for its six runs): Haiku +4.3 pp [−1.6, +9.9], Sonnet +11.4 [+4.1, +19.6], Opus +6.0 [+0.3, +13.3]. No human has checked the grades.

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

Raw runs and grades are release assets, not in the repository: `results-raw-1.3.0.tar.gz` (the 1.3.0 measurement, the candidate batch and the eval 9 rerun), `results-raw-1.3.0-review.tar.gz` (the held-out set, the trim ablations and the two regrades), `results-raw-heldout2-1.3.0.tar.gz` (the second held-out set) and `results-raw-1.2.1.tar.gz` (everything up to 1.2.1). [docs/measurements.md](docs/measurements.md#restoring-the-raw-runs) says how to restore them.

## Contributing

Open an issue with the prompt, what the model did, and whether it was underreach, overreach or misrouting. Failures become eval cases first; the instruction text changes only when a failure repeats across runs. See `skills/mind-the-gap/SKILL.md` § Maintenance.

MIT. See [LICENSE](LICENSE). `run_eval.py`, `improve_description.py` and `scripts/utils.py` under `results/raw/harness/` derive from Anthropic's skill-creator and stay under Apache 2.0 (`results/raw/harness/LICENSE-skill-creator.txt`).
