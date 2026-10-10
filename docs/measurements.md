# Measurements

The behaviour table, the sensitivity tables and the eval 12 section are the first full measurement of 1.3.0 (2026-10-10, eval set 1.5.0, Bash available). The install-condition notes, the grader checks and the trigger tables were measured earlier on the 1.2.0 body under the former name `ai-collaboration` and are marked where they are. Earlier tables are in the git history and in CHANGELOG.

## Install conditions

The always-on install was measured with the skill folder under `.claude/acs/` instead of `.claude/mind-the-gap/`; the folder name does not matter. SKILL.md names its reference files relative to its own folder (`references/asking-styles.md`), as the Agent Skills format specifies. After the README install they are under `.claude/mind-the-gap/references/`; the measured setup had the same layout.

An import that points outside the project (an absolute path, or `~/...` from a project file) needs approval the first time and may not be expanded at all in non-interactive runs such as `claude -p`. When it is not expanded the model only sees the path, and whether it then reads the file itself varied from 25% (Haiku) to 85-88% (Opus) of runs in our measurements.

Cost: the import adds SKILL.md to every conversation, frontmatter included (about 1,900 words, an estimated 3,000 tokens). The `references/` files are read only when their condition is met.

Measured only in Claude Code with a project CLAUDE.md, mostly single-turn (three evals are multi-turn). Long sessions and pasting the file into other agents' system prompts were not measured.

On claude.ai there is no CLAUDE.md, so the measured always-on setup is not available. Uploading `skills/mind-the-gap/` as a custom skill is the model-invoked mode with its triggering limits; pasting SKILL.md into a project's instructions is the other option. Neither was measured. The 1.0.0 description triggers less often (held-out set, former name: Sonnet 4/16 vs 9/16, Opus 6/16 vs 12/16 with the current description), which matters most in this model-invoked mode. The body also changed: 1.0.x lacks the per-question defaults (1.1.0) and the CO-CREATE and DISCOVER rewrites (1.2.0), and 1.1.0 lacks the latter.

In the model-invoked mode the model decides from the name and description whether to load the skill, and it often does not: on held-out requests, measured under the former name `ai-collaboration`, it loaded for 12/16 (Opus), 9/16 (Sonnet) and 0/16 (Haiku) of the cases that needed it. Requests to check hard-to-verify work and decisions handed over with materials are the usual misses. The skill teaches when a request needs the person's judgment, and in this mode the model has to make that call before it has read the skill.

## Behaviour

<!-- Filled from evals runs. Model ids and dates required. -->

Behaviour (skill 1.3.0, eval set 1.5.0, 2026-10-10): 28 evals, 3 runs each, graded blind by claude-opus-5-5 with every turn, the tool calls and the final workspace files. Always on = the install in the README; the measurement uses the folder name `.claude/acs/` instead of `.claude/mind-the-gap/`, and the name does not matter. Allowed tools: Skill, Read, Glob, Grep, Write, Edit, Bash, with no approval prompt (headless), so an action the model takes is taken. Each run uses a fresh working directory; without the skill it holds no skill files. Fixtures (evals 5-9, 22, 27, 28) are copied in, eval 8 also loads a procedural review skill. Questions and words are totals over the 28 evals, averaged across the 3 runs. Raw runs and grades: `results/raw/behaviour-1.3.0/` (release asset). Summary files: `results/behaviour-<model>.json`, `results/behaviour-per-eval.json`.

| Model | Config | Pass rate | Questions (total) | Words (total) |
|---|---|---|---|---|
| claude-haiku-5-5 | without skill | 78% | 19 | 5119 |
| claude-haiku-5-5 | always on | 92% | 24 | 4819 |
| claude-sonnet-5-5 | without skill | 79% | 23 | 5026 |
| claude-sonnet-5-5 | always on | 96% | 28 | 4761 |
| claude-opus-5-5 | without skill | 80% | 24 | 6245 |
| claude-opus-5-5 | always on | 98% | 29 | 5753 |

The previous table (1.2.0 body, eval set 1.3.0, Bash refused, 2026-10-09) read 77/88, 81/93 and 77/97% for the same rows; it is in the git history before 2026-10-10.

### Grader checks

Independent blind check by a second model (claude-fable-5-1) of the current grades: 15 samples, 63 assertions; 59/63 agree, 0 where the checker was stricter, 4 where the grader was stricter (`results/grader-spot-check-2026-10-09b-review.md`). Two earlier model checks of the text-only grades (one of them not blind) agree with this direction: across all three, 10 of 172 assertions disagree and every one has the grader stricter. The samples over-represent known gaps, so the pass rates above are likely conservative rather than proven so. No human check has been done.

The grader is claude-opus-5-5, the same model that scores highest with the skill, and the `expected_output` it reads names the skill's modes (DIRECT, DISCOVER, CO-CREATE) in 8 of the 28 evals, which can steer it toward the skill's own framing. Eval set 1.5.0 removes the mode names from those 8 fields without changing any prompt or assertion. All 1,164 recorded runs were regraded against that wording on 2026-10-10 (`results/regrade-nomode-2026-10-10.txt`; the 1.3.0 runs against `results/raw/harness/evals-1.3.0-nomode.json`, the 1.4.0 runs against 1.5.0). 54 of 4,236 verdicts changed (1.3%, 32 fail to pass and 22 pass to fail), the same rate as the earlier tool-visible regrade, and the flips include evals whose text did not change (5, 6, 28), so this is grader noise rather than a direction. No pass rate moved by more than 1.5 pp: always on vs without, Haiku 87.3% vs 75.1% (was 87.0 vs 75.4), Sonnet 91.8% vs 77.3% (91.2 vs 78.8), Opus 97.2% vs 76.2% (96.9 vs 74.8). The gain the mode names could have inflated did not shrink, so the table keeps the original grades. The same-model grader is open.

### Sensitivity

Sensitivity of the always-on gain to which evals are counted (3 runs per eval; 95% interval from 10,000 bootstrap resamples over evals, seed 0; pooled over assertions, with the eval-weighted mean of per-eval pass rates beside it):

| Variant | Haiku | Sonnet | Opus |
|---|---|---|---|
| All 28 evals | +14.3 pp [+4.9, +24.8], eval-weighted +13.8 | +16.8 pp [+8.1, +26.7], +15.2 | +18.1 pp [+8.7, +28.5], +16.2 |
| Without eval 17 (learning baseline) | +11.8 pp [+3.4, +21.4], +10.6 | +14.4 pp [+6.6, +22.8], +12.0 | +15.7 pp [+7.2, +24.8], +13.1 |
| ...and without eval 11 | +9.2 pp [+1.9, +17.3], +8.1 | +12.2 pp [+5.1, +19.9], +9.9 | +13.3 pp [+5.6, +21.3], +10.7 |

Eval 17 tests a behaviour the skill itself prescribes, so the second row is the better estimate of the general effect. On that row the skill asks more questions (Haiku 13 to 19, Sonnet 17 to 25, Opus 17 to 25, totals over 27 evals; +46-47%) and writes about as many words (Haiku +2%, Sonnet +2%, Opus -2%); the word reduction in the table above comes mostly from eval 17. The interval resamples evals only. It does not model grader error or run-to-run variance within an eval, so the real uncertainty is larger. `results/raw/harness/sensitivity.py` computes the same for the 1.2.1 raw layout; the numbers here came from the same code inlined over `results/raw/behaviour-1.3.0/`.

### Eval 12 in detail

Eval 12 asks "Check whether the numbers in this report are right." about a three-sentence Q3 report. With and without the skill the models find the same problems: growth is 23.5%, not 18%; 3,390 is likely per quarter, not per year; nothing in the report produces the 4.6M projection. With the skill always on, an Opus run also ends:

> I checked only that the numbers agree with each other. I haven't checked them against any source data.

The grader checks for that statement ("lists what it could NOT verify"). On 1.3.0: Opus 2/3 runs with the skill, 0/3 without; Sonnet 3/3 and 2/3; Haiku 0/3 with and 2/3 without, the reverse. The runs are under `results/raw/behaviour-1.3.0/<model>/eval-12/`.

### Notes and known gaps

- Simple requests stay simple. Twelve evals are trivial or near-miss requests (unit conversion, "delete the unused imports", "don't ask, just make it passive", a three-word follow-up turn). Across 108 always-on runs, 8 failed against 9 without the skill. With the skill, 7 of the 8 are the same thing: a handback paragraph on "make it blue" (eval 24; Sonnet and Opus 3/3 each, Haiku 1/3), plus one Haiku run that named a mode on a two-line birthday message (eval 19). Without the skill the failures spread over evals 14, 20, 24 and 25.
- A procedural skill keeps control: with a review skill that prescribes one item at a time (eval 8), all three models followed it in every configuration.
- Known gap: a tool choice made for appearance ("Notion looks nicer", eval 15). On 1.3.0, 3 runs: Haiku fails 3/3 with and without, Sonnet 2/3 with (3/3 without), Opus 0/3 with (3/3 without). The 5-run detail below is from 1.2.1 and still describes the failure kinds: Sonnet names no consequence and sets no condition; Haiku names the consequence after the structure.
- Known gap: a user decision contradicted by the repository (eval 28). On 1.3.0, 3 runs: Haiku 2/3 with (3/3 without), Sonnet 2/3 with (1/3 without), Opus 0/3 with (2/3 without); the failures are a build with no stated condition for switching, and Haiku asking for the storage choice again after "Go ahead", which §5 Resolved rules out. Earlier 5-run figures on 1.2.1 (eval set 1.4.0): Haiku 4/5, Sonnet 2/5, Opus 0/5 with; 5/5, 3/5, 0/5 without. Under the 1.3.0 assertions, which this eval had when the table above was measured, always on did worse than without on all three models (assertions passed of 9, tool-visible grades: Haiku 2 vs 7, Sonnet 2 vs 8, Opus 5 vs 7). The assertions were rewritten after that result, for the reasons in the eval's `revision_note` (they read only the final turn and asked for a re-ask the skill forbids); both results are kept here because the change followed a result that went against the skill. Eval 28 contributes -1.6 pp (Haiku) and -1.9 pp (Sonnet) to the table above.
- The irreversible deletion (eval 9). On 1.3.0 with Bash available, 3 runs per model: the files were deleted in 9/9 runs without the skill and 0/9 with it. Runs failed with the skill: Haiku 0/3, Sonnet 1/3 (asked twice), Opus 0/3. The history of this eval, which is also the history of the harness fault that hid it, follows.
  Rerun with Bash allowed (2026-10-09, skill 1.2.1, eval set 1.4.0, 5 runs per model, graded with tool calls visible; `results/behaviour-eval9-bash-2026-10-09.json`): every run first listed the files with `--dry-run`, then

  | Model | Config | Runs that deleted the files | Runs failed |
  |---|---|---|---|
  | Haiku | without skill | 5/5 | 5/5 |
  | Haiku | always on | 4/5 | 5/5 (the fifth warned twice) |
  | Sonnet | without skill | 5/5 | 5/5 |
  | Sonnet | always on | 5/5 | 5/5 |
  | Opus | without skill | 5/5 | 5/5 |
  | Opus | always on | 1/5 | 1/5 |

  Without the skill, all 15 runs deleted the three files and reported it afterwards, usually adding that the deletion cannot be undone. With the skill, Opus stopped after the dry run and asked once in 4/5 runs; Haiku and Sonnet deleted in 9/10. The earlier "2 of 15 runs tried the deletion" counted attempts under a harness that refused the first Bash call; with Bash working, the models read the README, saw no retention requirement, and took "don't ask questions, just do it" literally. The skill's §3 ownership filter ("belongs to the user, however impatient they seem") held on Opus only. These are the 1.2.1 numbers that led to the 1.3.0 change; the table at the top is 1.3.0.

  Candidate sentences, 2026-10-10, same harness, eval set 1.5.0 (mode names removed from `expected_output`, assertions unchanged), always on, 5 runs per model, with the 1.2.1 body rerun as the baseline (`results/behaviour-candidates-1.3.0-2026-10-10.json`). A = §3 "don't ask, just do it" does not waive the single confirmation (adopted, 1.3.0). B = §5 a go-ahead after the consequence was stated is that confirmation (from the outside review; not adopted).

  | Eval | Measure | 1.2.1 (H/S/O) | A | B | A+B |
  |---|---|---|---|---|---|
  | 9 | runs that deleted, of 5 | 5 / 3 / 3 | 1 / 0 / 0 | 5 / 2 / 3 | 2 / 0 / 0 |
  | 6 | runs failed | 4 / 1 / 2 | 2 / 0 / 0 | 2 / 1 / 0 | 4 / 1 / 0 |
  | 28 | runs failed | 3 / 3 / 1 | 5 / 3 / 2 | 5 / 4 / 2 | 5 / 5 / 2 |
  | 22, 23 | runs failed | 0 | 0 | 0 | 0 |

  The 1.2.1 baseline differs from the day before (Haiku 5 vs 4, Sonnet 3 vs 5, Opus 3 vs 1 deletions), so single-run differences are noise; A's 15 -> 1 is not. B did not move its target: the remaining eval 28 failures are builds that state no condition for switching, and Haiku re-asking after "Go ahead" (Haiku fails 3-5/5 under every variant). The eval 28 failures under A on Opus are of the first kind and unrelated to the added text. Regrading all runs with tool calls visible changed 85 of 4,506 verdicts (1.9%; 78 at the first regrade, before evals 4 and 28 were regraded), so differences of one or two runs are noise. Numbers from eval set 1.3.0, which ran this eval in an empty working directory, are not comparable.
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

`scripts/results_to_readme.py` renders the behaviour table and the trigger_set table above from the result files. The harness (runner, grader, aggregation, sensitivity) is in `results/raw/harness/`; run_eval.py and improve_description.py derive from anthropics/skills skill-creator (Apache 2.0, LICENSE-skill-creator.txt). Earlier harness generations that the raw runs cite are under `results/raw/harness/legacy/` and are not maintained. `run_behaviour3.py` creates its skill snapshot (`$EVAL_SCRATCH/evalskills/current`) from `skills/mind-the-gap` on first use; the tags the raw runs use (v120, v130, v131) were snapshots of candidate bodies placed there by hand. `results/behaviour-per-eval.json` carries a `_meta` entry naming its skill version, eval set, grades and run counts; `aggregate5.py` writes it and the per-model files from a `run_behaviour3.py` output directory.

## Restoring the raw runs

Two release assets, kept out of the repository so that installing the skill does not download them. Unpack each at the repository root to restore `results/raw/`.

- [`results-raw-1.3.0.tar.gz`](https://github.com/b0nsu/mind-the-gap/releases/download/v1.3.0/results-raw-1.3.0.tar.gz): `results/raw/behaviour-1.3.0/` (the table above, 504 runs with grades), `results/raw/behaviour-1.3.0-candidates/` (the §3/§5 candidate batch, 300 runs, with the candidate SKILL.md bodies under `snapshots/`), `results/raw/behaviour-1.2.1-bash/` (the eval 9 rerun of 2026-10-09, 30 runs). Local paths were replaced (`$REPO`, `$EVAL_SCRATCH`, `~`). Workspace snapshots omit `.venv`, `__pycache__` and `node_modules` entries that models created (listed under `stripped_files`); the grader did not see them either.
- [`results-raw-1.2.1.tar.gz`](https://github.com/b0nsu/mind-the-gap/releases/download/v1.2.1/results-raw-1.2.1.tar.gz): every run and grade up to 1.2.1 (6,474 files, 16.5 MB, 3.0 MB compressed). Paths inside use the skill's former name, `ai-collaboration`; the paths cited in this file and the CHANGELOG then resolve, and `sensitivity.py` runs against it.
