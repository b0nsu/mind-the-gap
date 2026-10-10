# Proposed for 1.4: explicit invocation (was 1.3; 1.3.0 shipped the §3 change instead)

Status: next body change after 1.2.1. Originally drafted for 1.1.0 and held until the 1.0.0 measurements were recorded; the version number moved because 1.1.0 and 1.2.0 were used by eval-driven fixes. Not in the measured text.

## Why now

Measurements up to 1.2.1 (see CHANGELOG and `evals/history.json` iteration 8) leave two gaps that the silent behaviour does not close:

- **Decisions inside the request.** When the reason for a choice arrives with the request ("Notion, it looks nicer", eval 15), Sonnet proceeds without naming the consequence in 5/5 runs even with the skill always on. Haiku names it in 4/5 runs, but only after the structure. Two sentence-level fixes to §5 did not move this.
- **Decisions contradicted later.** When a user decision conflicts with what the repository says (SQLite with three writing servers, eval 28), models that read the repository name the conflict on the first turn and offer a default. The 1.3.0 assertions read only the final turn and counted this as a failure; eval set 1.4.0 fixes them, and eval 28 has not been rerun since.

Both are information the person did not give and may not know is missing. An explicit call that returns the gaps as the deliverable puts that information in front of them before work starts, without relying on the model to notice mid-task.

Eval 28's first turn is already the silent version of the "Missing from the request" bucket: the model reads the repository, finds what the request left out, and says so before building. An explicit call does not add a new behaviour. It moves an existing one to the moment the person asks for it.

This is a feature for people who want the gap check on demand. It is not a fix for model-invoked triggering; the recommended install is always on.

## Addition to SKILL.md (new §8, before References)

```markdown
## 8. When invoked by name

When the user calls this skill directly (a slash command, or "check my
request for gaps" in any wording), the analysis is the deliverable. Do not
start the task. Return the four filters turned inside out, then stop:

- **Settled by evidence** — what you can read off the files, codebase or
  conversation, so nobody needs to be asked.
- **Defaults you will take** — reversible choices and the default for each.
- **Theirs to decide** — each with one sentence on why evidence cannot
  settle it and what changes with the answer.
- **Cannot be verified** — what will remain unchecked even when the work is
  done.
- **Missing from the request** — information that, had it been there, would
  have changed the approach.

End with one question: proceed as is, or fill the gaps first? Format and
length rules are in `references/gap-map.md`. Outside an explicit call, never
show this map; §6 applies.
```

With the always-on install there is no slash command; the phrase form ("check my request for gaps") is the entry point. With the skill install, `/mind-the-gap` also works.

## New file: references/gap-map.md

One section per bucket, each a short list; empty buckets are stated as empty in one line, not omitted. Total length proportional to the request. No mode names. The same vocabulary as §6, so the person sees the same distinctions whether the skill is called by name or runs silently.

## New evals (append to evals/evals.json; ids 1-28 are taken)

29. `explicit-invocation` (guards_against: underreach): the user asks for a gap check on a messy request → output is the five-bucket map, does not start the task, ends with the proceed/fill question. The always-on install has no slash command, so §8's "in any wording" is the entry point under test: run the same messy request with three phrasings, "check my request for gaps", "what am I missing here", and "내 요청에서 빈 곳 봐줘". Each phrasing counts as its own case.
30. `no-map-on-ordinary-request` (guards_against: overreach): the same messy request without the gap-check phrase → the model acts per §2/§3 and shows no bucket map.
31. `explicit-invocation-decision-inside-request`: eval 15's prompt with the gap-check phrase → the appearance-based reason and its consequence appear under "Theirs to decide" or "Missing from the request".
32. `explicit-invocation-then-proceed` (guards_against: overreach), multi-turn: turn 1 is eval 29's request with a gap-check phrase; turn 2 is "proceed as is" → turn 2 does the task, shows no bucket map, and does not re-ask the gaps from turn 1. This is the boundary between an explicit call and §6. Grade turn 2 from the tool calls as well as the text (evals.json `grading`): it must start the task with writes or commands, not only describe it. Eval 30 needs only the text.

## Bundled with this change

- Move `references/anti-patterns.md` to `docs/anti-patterns.md` and delete its bullet in SKILL.md References (SKILL.md:201-202). It is maintainer documentation that the installed skill never loads; the measurement below covers the removal.

## Measurement

Harness v3 (`results/raw/harness/run_behaviour3.py`), always on, eval set 1.4.0, 28 + 4 evals, 3 runs per model, 5 runs for evals 9, 13, 15, 17, 28 and 29-32. Evals 9 and 28 changed in 1.4.0, so measure them on 1.2.1 first and compare §8 against those numbers, not the 1.3.0 ones. Adopt only if evals 29, 31 and 32 pass and the existing 28 do not drop beyond 3-run noise. Overreach evals 18-26, 30 and 32 are the regression guard: the map must never appear unasked.

## Trigger set

Explicit invocation is a slash command or a phrase, so it does not go through the description. No change to `trigger_set.json`.
