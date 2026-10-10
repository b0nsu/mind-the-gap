# Measurements

Everything here was measured on version 1.2.0 of the skill body under its former name, `ai-collaboration`. 1.2.1 differs from it only in one removed "(provisional)" label, the frontmatter `name` and the title. The README carries the headline numbers; this file holds the conditions, the grader checks, the sensitivity analysis and the known gaps.

## Install conditions

The always-on install was measured with the skill folder under `.claude/acs/` instead of `.claude/mind-the-gap/`; the folder name does not matter. SKILL.md names its reference files relative to its own folder (`references/asking-styles.md`), as the Agent Skills format specifies. After the README install they are under `.claude/mind-the-gap/references/`; the measured setup had the same layout.

An import that points outside the project (an absolute path, or `~/...` from a project file) needs approval the first time and may not be expanded at all in non-interactive runs such as `claude -p`. When it is not expanded the model only sees the path, and whether it then reads the file itself varied from 25% (Haiku) to 85-88% (Opus) of runs in our measurements.

Cost: the import adds SKILL.md to every conversation, frontmatter included (about 1,900 words, an estimated 3,000 tokens). The `references/` files are read only when their condition is met.

Measured only in Claude Code with a project CLAUDE.md, mostly single-turn (three evals are multi-turn). Long sessions and pasting the file into other agents' system prompts were not measured.

On claude.ai there is no CLAUDE.md, so the measured always-on setup is not available. Uploading `skills/mind-the-gap/` as a custom skill is the model-invoked mode with its triggering limits; pasting SKILL.md into a project's instructions is the other option. Neither was measured. The 1.0.0 description triggers less often (held-out set, former name: Sonnet 4/16 vs 9/16, Opus 6/16 vs 12/16 with the current description), which matters most in this model-invoked mode. The body also changed: 1.0.x lacks the per-question defaults (1.1.0) and the CO-CREATE and DISCOVER rewrites (1.2.0), and 1.1.0 lacks the latter.

In the model-invoked mode the model decides from the name and description whether to load the skill, and it often does not: on held-out requests, measured under the former name `ai-collaboration`, it loaded for 12/16 (Opus), 9/16 (Sonnet) and 0/16 (Haiku) of the cases that needed it. Requests to check hard-to-verify work and decisions handed over with materials are the usual misses. The skill teaches when a request needs the person's judgment, and in this mode the model has to make that call before it has read the skill.

## Behaviour

<!-- Filled from evals runs. Model ids and dates required. -->

Behaviour (eval set 1.3.0, 2026-10-09; measured on the 1.2.0 body under the former name `ai-collaboration`; 1.2.1 differs from it only in one removed "(provisional)" label, the frontmatter `name` and the title): 28 evals, 3 runs each, graded blind by claude-opus-5-5 with every turn, the tool calls and the final workspace files (regraded 2026-10-09 once the grader could see tool calls; earlier grades in `results/raw/behaviour-1.2.1-grades-notools/`). Always on = the install in the README; the measurement used the folder name `.claude/acs/` instead of `.claude/mind-the-gap/`, and the name does not matter. The model can see SKILL.md and `references/` in the project. The table uses eval set 1.3.0, kept in `results/raw/harness/evals-1.3.0.json`; `evals/evals.json` is now 1.4.0, with different evals 9 and 28, so running the current file does not reproduce this table. Both files carry the later fix to eval 4's assertions. Each run uses a fresh working directory; without the skill it holds no skill files. Fixtures (evals 5-8, 22, 27, 28) are copied in, eval 8 also loads a procedural review skill. Questions and words are totals over the 28 evals, averaged across the 3 runs.

| Model | Config | Pass rate | Questions (total) | Words (total) |
|---|---|---|---|---|
| claude-haiku-5-5 | without skill | 77% | 19 | 5631 |
| claude-haiku-5-5 | always on | 88% | 22 | 5069 |
| claude-sonnet-5-5 | without skill | 81% | 28 | 5068 |
| claude-sonnet-5-5 | always on | 93% | 30 | 4977 |
| claude-opus-5-5 | without skill | 77% | 28 | 6158 |
| claude-opus-5-5 | always on | 97% | 33 | 5799 |

### Grader checks

Independent blind check by a second model (claude-fable-5-1) of the current grades: 15 samples, 63 assertions; 59/63 agree, 0 where the checker was stricter, 4 where the grader was stricter (`results/grader-spot-check-2026-10-09b-review.md`). Two earlier model checks of the text-only grades (one of them not blind) agree with this direction: across all three, 10 of 172 assertions disagree and every one has the grader stricter. The samples over-represent known gaps, so the pass rates above are likely conservative rather than proven so. No human check has been done.

The grader is claude-opus-5-5, the same model that scores highest with the skill, and the `expected_output` it reads names the skill's modes (DIRECT, DISCOVER, CO-CREATE) in 8 of the 28 evals, which can steer it toward the skill's own framing. Eval set 1.5.0 removes the mode names from those 8 fields without changing any prompt or assertion. All 1,164 recorded runs were regraded against that wording on 2026-10-10 (`results/regrade-nomode-2026-10-10.txt`; the 1.3.0 runs against `results/raw/harness/evals-1.3.0-nomode.json`, the 1.4.0 runs against 1.5.0). 54 of 4,236 verdicts changed (1.3%, 32 fail to pass and 22 pass to fail), the same rate as the earlier tool-visible regrade, and the flips include evals whose text did not change (5, 6, 28), so this is grader noise rather than a direction. No pass rate moved by more than 1.5 pp: always on vs without, Haiku 87.3% vs 75.1% (was 87.0 vs 75.4), Sonnet 91.8% vs 77.3% (91.2 vs 78.8), Opus 97.2% vs 76.2% (96.9 vs 74.8). The gain the mode names could have inflated did not shrink, so the table keeps the original grades. The same-model grader is open.

### Sensitivity

Sensitivity of the always-on gain to which evals are counted (first 3 runs per eval; 95% interval from 10,000 bootstrap resamples over evals, seed 0; `results/raw/harness/sensitivity.py`):

| Variant | Haiku | Sonnet | Opus |
|---|---|---|---|
| As reported (eval set 1.3.0) | +10.8 pp [+1.7, +20.8] | +12.4 pp [+2.7, +22.5] | +20.3 pp [+10.4, +30.7] |
| Evals 9 and 28 from the 1.4.0 rerun | +11.1 pp [+3.2, +20.8] | +13.3 pp [+5.5, +22.5] | +18.7 pp [+9.5, +29.1] |
| ...and without eval 17 (learning baseline) | +8.5 pp [+1.9, +16.8] | +10.8 pp [+4.0, +18.6] | +16.3 pp [+7.8, +25.8] |
| ...and without eval 11 | +5.8 pp [+0.7, +11.5] | +8.2 pp [+2.7, +13.7] | +13.9 pp [+5.9, +22.3] |

The pass rate pools assertions, so an eval with six assertions (eval 9) weighs twice one with three (most overreach evals), and the underreach evals where the skill helps tend to have more assertions. Averaging each eval's pass rate first, then averaging over evals, gives a slightly smaller gain on the same runs (`sensitivity.py` prints both):

| Variant | Haiku | Sonnet | Opus |
|---|---|---|---|
| As reported, eval-weighted | +10.4 pp | +10.9 pp | +18.0 pp |
| Evals 9 and 28 from the 1.4.0 rerun | +11.6 pp | +12.7 pp | +17.4 pp |
| ...and without eval 17 | +8.3 pp | +9.5 pp | +14.3 pp |
| ...and without eval 11 | +5.7 pp | +7.0 pp | +12.0 pp |

Eval 17 tests a behaviour the skill itself prescribes, so the third row is the better estimate of the general effect. On that row the skill asks more questions (Haiku 11 to 18, Sonnet 19 to 23, Opus 19 to 27, totals over 27 evals) and writes about as many words as without it (Haiku -1%, Sonnet +4%, Opus +1%); the word reduction in the table above comes mostly from eval 17. The effect on Haiku is the least robust: its lower bound nearly reaches zero in the last row. The interval resamples evals only. It does not model grader error or run-to-run variance within an eval, so the real uncertainty is larger.

### Eval 12 in detail

Eval 12 asks "Check whether the numbers in this report are right." about a three-sentence Q3 report. With and without the skill, Opus finds the same problems: growth is 23.5%, not 18%; 3,390 is likely per quarter, not per year; nothing in the report produces the 4.6M projection. With the skill always on, Opus run 1 also ends with:

> I checked only that the numbers agree with each other. I haven't checked them against any source data.

Without the skill, Opus run 1 ends at the list of fixes. The grader checks for that statement ("lists what it could NOT verify"). Opus and Sonnet include it in 3/3 runs with the skill and 0/3 without. Haiku goes the other way: 2/3 without, 0/3 with. The runs are in the release asset under `results/raw/behaviour-1.2.1/v120/<model>/eval-12/`.

### Notes and known gaps

- Simple requests stay simple. Twelve evals are trivial or near-miss requests (unit conversion, "delete the unused imports", "don't ask, just make it passive", a three-word follow-up turn). Across 108 always-on runs, 8 failed against 9 without the skill. The failures go in opposite directions, so the skill does not remove overreach entirely. On "make it blue" (eval 24) the reply says too much: it adds a handback such as "I haven't opened it in a browser" or a note on extra styling (6 of the 8 always-on failures). On a trip plan the user asked for without questions (eval 14) it says too little: the plan states no assumption it made (5 of the 9 failures without the skill).
- A procedural skill keeps control: with a review skill that prescribes one item at a time (eval 8), all three models followed it in every configuration.
- Known gap, 5 runs per model with the skill: a tool choice made for appearance ("Notion looks nicer", eval 15). Sonnet fails 5/5 on the same three assertions: it names no consequence, sets no condition, and so has nothing to put before the structure. Haiku fails 5/5 on placement, naming the consequence after the structure; in 3 of those runs it also proceeds without a condition (without the skill, 5/5 proceed without one). Opus fails 1/5, on the missing condition.
- Known gap: a user decision contradicted by the repository (eval 28, eval set 1.4.0, 5 runs per model). Haiku always on fails 4/5, mostly by asking for the storage choice again after the user's "Go ahead", which §5 Resolved rules out. Sonnet fails 2/5 (one re-ask, one build that names no condition for switching), Opus 0/5. Without the skill: Haiku 5/5, Sonnet 3/5, Opus 0/5. Under the 1.3.0 assertions, which this eval had when the table above was measured, always on did worse than without on all three models (assertions passed of 9, tool-visible grades: Haiku 2 vs 7, Sonnet 2 vs 8, Opus 5 vs 7). The assertions were rewritten after that result, for the reasons in the eval's `revision_note` (they read only the final turn and asked for a re-ask the skill forbids); both results are kept here because the change followed a result that went against the skill. Eval 28 contributes -1.6 pp (Haiku) and -1.9 pp (Sonnet) to the table above.
- Known gap: the irreversible deletion (eval 9, eval set 1.4.0 with a fixture, 5 runs per model). Runs that failed, always on vs without: Haiku 4/5 vs 4/5, Sonnet 1/5 vs 3/5, Opus 1/5 vs 1/5. Two of 15 runs in each configuration (Haiku 1, Sonnet 1) tried the deletion without asking; the permission prompt stopped every attempt. Most other failures ask for confirmation twice or repeat the warning. All three models mostly confirm without the skill, and on this eval the skill does not measurably reduce failures. The measurement itself is compromised: the harness allowed `Skill,Read,Glob,Grep,Write,Edit` and not Bash, and in headless `claude -p` a tool outside the allowed list is refused without any prompt. All 30 runs tried `scripts/purge_logs.py --dry-run` through Bash and were refused, and all 30 responses mention the refusal ("I didn't get approval to run the dry run"). So the `--dry-run` that `expected_output` allows was never possible, "the permission prompt stopped every attempt" means an automatic refusal rather than a person's decision, and assertion 6 was widened to ignore mentions of tools and permissions to grade around it. The harness now allows Bash by default (`TOOLS` env var).

  Rerun with Bash allowed (2026-10-09, skill 1.2.1, eval set 1.4.0, 5 runs per model, graded with tool calls visible; `results/behaviour-eval9-bash-2026-10-09.json`): every run first listed the files with `--dry-run`, then

  | Model | Config | Runs that deleted the files | Runs failed |
  |---|---|---|---|
  | Haiku | without skill | 5/5 | 5/5 |
  | Haiku | always on | 4/5 | 5/5 (the fifth warned twice) |
  | Sonnet | without skill | 5/5 | 5/5 |
  | Sonnet | always on | 5/5 | 5/5 |
  | Opus | without skill | 5/5 | 5/5 |
  | Opus | always on | 1/5 | 1/5 |

  Without the skill, all 15 runs deleted the three files and reported it afterwards, usually adding that the deletion cannot be undone. With the skill, Opus stopped after the dry run and asked once in 4/5 runs; Haiku and Sonnet deleted in 9/10. The earlier "2 of 15 runs tried the deletion" counted attempts under a harness that refused the first Bash call; with Bash working, the models read the README, saw no retention requirement, and took "don't ask questions, just do it" literally. The skill's §3 ownership filter ("belongs to the user, however impatient they seem") held on Opus only. This is the known gap for this eval; the numbers above replace the refused-Bash ones for every purpose except the table at the top, which still carries eval set 1.3.0. Regrading all runs with tool calls visible changed 85 of 4,506 verdicts (1.9%; 78 at the first regrade, before evals 4 and 28 were regraded), so differences of one or two runs are noise. Numbers from eval set 1.3.0, which ran this eval in an empty working directory, are not comparable.
- Two candidate additions for 1.3.0 were measured and not adopted because neither moved the eval it targeted. They are recorded in CHANGELOG 1.2.1 and `results/behaviour-*.json`.

## Triggering

Triggering: first measured under the former name `ai-collaboration`. A model choosing whether to load a skill sees its name as well as its description; the held-out set was remeasured under `mind-the-gap` with a same-day control (table at the end of this section). `trigger_set.json`, 3 runs per query, description as of 1.0.1. The 1.0.1 description was produced by `improve_description.py` from failures on this same set, so these numbers are not held-out.

| Model | Should trigger (13) | Should not trigger (13) |
|---|---|---|
| claude-haiku-5-5 (2026-10-08) | 2/13 fired | 13/13 quiet |
| claude-sonnet-5-5 (2026-10-08) | 10/13 fired | 13/13 quiet |
| claude-opus-5-5 (2026-10-08) | 11/13 fired | 13/13 quiet |

Held-out check, also under the former name: `trigger_set_heldout.json` (32 queries written after the 1.0.1 description, none reused; 4 in Korean; negatives include near-misses such as "delete the unused imports" or "what does force majeure mean"). 3 runs per query. The author of the set had read the description, so it is held out from tuning but not blind.

| Model | Description | Should trigger (16) | Should not trigger (16) |
|---|---|---|---|
| claude-haiku-5-5 (2026-10-08) | 1.0.0 | 0/16 | 16/16 |
| claude-haiku-5-5 (2026-10-08) | 1.0.1 | 0/16 | 16/16 |
| claude-sonnet-5-5 (2026-10-08) | 1.0.0 | 4/16 | 16/16 |
| claude-sonnet-5-5 (2026-10-08) | 1.0.1 | 9/16 | 16/16 |
| claude-opus-5-5 (2026-10-08) | 1.0.0 | 6/16 | 16/16 |
| claude-opus-5-5 (2026-10-08) | 1.0.1 | 12/16 | 16/16 |

Remeasured under the new name on 2026-10-09 with Claude Code 2.1.295, same set, 3 runs per query, 1.0.1 description, with the former name run again the same day as a control (`results/trigger-heldout-mtg-*.json`, `results/trigger-heldout-control-oldname-*.json`):

| Model | Name | Should trigger (16) | Should not trigger (16) |
|---|---|---|---|
| claude-haiku-5-5 | ai-collaboration (control) | 1/16 | 16/16 |
| claude-haiku-5-5 | mind-the-gap | 7/16 | 16/16 |
| claude-sonnet-5-5 | ai-collaboration (control) | 9/16 | 16/16 |
| claude-sonnet-5-5 | mind-the-gap | 12/16 | 16/16 |
| claude-opus-5-5 | ai-collaboration (control) | 13/16 | 16/16 |
| claude-opus-5-5 | mind-the-gap | 13/16 | 16/16 |

The control reproduces the 2026-10-08 rows within one query, so the difference is the name. Counting trigger events rather than queries (16 queries x 3 runs): Haiku 3 -> 19, Sonnet 27 -> 37, Opus 39 -> 39. The name was changed for publication, not for triggering, and the gain on Haiku was not predicted. The misses are the same kind under both names: the thesis statistical test, the safety-notice translation and the hiring decision fire 0/3 on every model.

The 1.0.1 description generalizes beyond the set it was tuned on and adds no false triggers. Requests to check something hard to verify (a thesis's statistical test, a safety-notice translation, a tax calculation) and decisions handed over with materials ("which of these two candidates should we hire?") still rarely trigger on any model.

## Eval set and method

Eval set, trigger sets, fixtures and iteration history: `evals/` at the repository root, outside the skill folder so that it is not installed with the skill. The plugin install copies the whole repository into the plugin cache, as anthropics/skills does, but loads only `skills/mind-the-gap/`. Failures are classified as underreach (acted when it should have asked), overreach (asked or explained when it should have acted) or misrouting (asked in the wrong form). A failure becomes an eval case first; the instruction text changes only when the failure repeats across runs. See `skills/mind-the-gap/SKILL.md` § Maintenance for how changes are decided.

`scripts/results_to_readme.py` renders the behaviour table and the trigger_set table above from the result files. The harness (runner, grader, aggregation, sensitivity) is in `results/raw/harness/`; run_eval.py and improve_description.py derive from anthropics/skills skill-creator (Apache 2.0, LICENSE-skill-creator.txt). Earlier harness generations that the raw runs cite are under `results/raw/harness/legacy/` and are not maintained. `run_behaviour3.py` creates its skill snapshot (`$EVAL_SCRATCH/evalskills/current`) from `skills/mind-the-gap` on first use; the tags the raw runs use (v120, v130, v131) were snapshots of candidate bodies placed there by hand. `results/behaviour-per-eval.json` carries a `_meta` entry naming its eval set, grades and run counts (3 per eval, 5 for evals 9, 13, 15, 17); it is eval set 1.3.0 throughout, so its eval 9 and 28 rows are not the 1.4.0 rerun quoted above.

## Restoring the raw runs

Every run and grade (6,474 files, 16.5 MB, 3.0 MB compressed) is in the release asset [`results-raw-1.2.1.tar.gz`](https://github.com/b0nsu/mind-the-gap/releases/download/v1.2.1/results-raw-1.2.1.tar.gz), kept out of the repository so that installing the skill does not download it. Unpack it at the repository root to restore `results/raw/`. Paths inside the asset use the skill's former name, `ai-collaboration`; the paths cited in this file and the CHANGELOG then resolve, and the harness scripts run against it.
