# mind-the-gap

A skill that reads a request, decides whether the person's judgment is needed anywhere in it, and asks only there. Everything else it does.

Measured against the same model without it, it asks more questions (21-64% more, excluding the eval that tests its own learning-baseline instruction; see [docs/measurements.md](docs/measurements.md)). What changes is where the questions go. It investigates before asking, takes cheap reversible defaults without permission, and keeps the person's attention for decisions that are irreversible, unverifiable, or a matter of taste or business meaning. When it asks, it says what it already established and what changes with the answer.

## What it looks like

Asked to check a three-sentence Q3 report, Opus finds the same three problems with or without the skill. With it, the reply also ends:

> I checked only that the numbers agree with each other. I haven't checked them against any source data.

The person learns what still needs their eyes. Opus and Sonnet add that sentence in 3/3 runs with the skill and 0/3 without; Haiku goes the other way, 2/3 without and 0/3 with (eval 12, details in [docs/measurements.md](docs/measurements.md#eval-12-in-detail)).

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

**Keep tool approvals on.** The skill shapes how the model asks; it does not stop the model from acting. In the irreversible-deletion eval, run with Bash available and no approval prompt, the model deleted the files in 15/15 runs without the skill and in 10/15 with it (Haiku 4/5, Sonnet 5/5, Opus 1/5). Only Opus with the skill reliably stopped after the dry run and asked. An earlier figure here (2 of 15 attempts, stopped by the permission prompt) came from a harness that refused every Bash call automatically; it is superseded ([docs/measurements.md](docs/measurements.md#notes-and-known-gaps)).

**As a model-invoked skill.** The model decides from the name and description whether to load it, and often does not (held-out cases: Haiku 7/16, Sonnet 12/16, Opus 13/16; see measurements). In Claude Code:

```
/plugin marketplace add b0nsu/mind-the-gap
/plugin install mind-the-gap@mind-the-gap
```

With other agents that read the [Agent Skills](https://agentskills.io/specification) format, `npx skills add b0nsu/mind-the-gap --skill mind-the-gap`. On claude.ai, upload `skills/mind-the-gap/` as a custom skill; not measured. If you uploaded an earlier version, replace it: the 1.0.0 description triggers less often.

## Measured

28 evals, 3 runs each, always on, graded blind by claude-opus-5-5 with tool calls visible. Conditions, intervals, grader checks and known gaps: [docs/measurements.md](docs/measurements.md).

| Model  | Pass rate, without → with | Questions | Words |
|--------|---------------------------|-----------|-------|
| Haiku  | 77% → 88%                 | 19 → 22   | −10%  |
| Sonnet | 81% → 93%                 | 28 → 30   | −2%   |
| Opus   | 77% → 97%                 | 28 → 33   | −6%   |

Simple requests stay simple: across 108 trivial-request runs, 8 failed with the skill and 9 without. A procedural skill keeps control (eval 8, 0 failures). Known gaps: a tool chosen for appearance (Sonnet, Haiku), a decision contradicted by the repository on a later turn (Haiku), and the irreversible deletion, where with Bash available the skill stops Opus (1/5 runs deleted vs 5/5) but not Haiku or Sonnet (9/10 deleted). Model-invoked triggering is unreliable on every model (7/16 to 13/16 of held-out cases). No human has checked the grades.

## Why it exists

Anthropic's and OpenAI's own guidance says the bottleneck has moved to the person, that vendors are deleting instructions rather than adding them, and that model capability is not permission. This skill is what those three points look like from inside the conversation. [docs/design-notes.md](docs/design-notes.md).

## Layout

```
skills/mind-the-gap/              the skill: SKILL.md, references/, LICENSE.txt
.claude-plugin/marketplace.json   Claude Code plugin marketplace entry
evals/                            eval set, trigger sets, fixtures, iteration history
results/                          aggregated results, grader checks, harness (results/raw/harness/)
scripts/results_to_readme.py      renders the measurement tables from result files
docs/                             measurements, design notes, next planned change
CHANGELOG.md
```

Raw runs and grades are a release asset (`results-raw-1.2.1.tar.gz`), not in the repository. [docs/measurements.md](docs/measurements.md#restoring-the-raw-runs) says how to restore them.

## Contributing

Open an issue with the prompt, what the model did, and whether it was underreach, overreach or misrouting. Failures become eval cases first; the instruction text changes only when a failure repeats across runs. See `skills/mind-the-gap/SKILL.md` § Maintenance.

MIT. See [LICENSE](LICENSE).
