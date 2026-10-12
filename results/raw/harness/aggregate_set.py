#!/usr/bin/env python3
"""Aggregate one run_behaviour3.py output directory (any eval set) into a summary JSON.
Pooled pass rate, gain with a 95% bootstrap interval over evals, eval-weighted gain, questions and words
(totals over evals, averaged over runs), and per eval the failed assertions and file removals of every run.
Same definitions as sensitivity.py and aggregate_heldout2.py; written for skill 1.3.1 so that one script covers
the tuning set and both held-out sets.

Usage: aggregate_set.py <runs dir> <out json> <date> <skill_version> <eval_set> [--runs 1,2,3] [--drop NAME=ids ...] [--boot N] [--seed S]
  runs dir   <OUT>/<tag> of run_behaviour3.py (<model>/eval-NN/<cfg>/run-N.json + .grade.json)
  --drop     a subset with these eval ids left out, e.g. --drop without_17=17 --drop without_17_11=17,11
"""
import argparse, glob, json, random
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("runs"); ap.add_argument("out"); ap.add_argument("date"); ap.add_argument("skill"); ap.add_argument("eval_set")
ap.add_argument("--runs", dest="run_ids", default="1,2,3"); ap.add_argument("--drop", action="append", default=[])
ap.add_argument("--boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=0)
a = ap.parse_args()
RUNS = Path(a.runs); RUN_IDS = [int(x) for x in a.run_ids.split(",")]
M = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
CFG = ["without_skill", "always_on"]


def load(model):
    per, fails, removed = {}, {}, {}
    for c in CFG:
        for r in RUN_IDS:
            for f in sorted(glob.glob(str(RUNS / model / "eval-*" / c / f"run-{r}.json"))):
                e = int(f.split("eval-")[1].split("/")[0])
                gr = json.load(open(f.replace(".json", ".grade.json"))); rr = json.load(open(f))
                d = per.setdefault(e, {k: [0, 0, 0, 0] for k in CFG})[c]
                d[0] += sum(x["passed"] for x in gr["expectations"]); d[1] += len(gr["expectations"])
                d[2] += gr["questions"]; d[3] += rr["words"]
                fails.setdefault(e, {k: [] for k in CFG})[c].append([i for i, x in enumerate(gr["expectations"], 1) if not x["passed"]])
                removed.setdefault(e, {k: 0 for k in CFG})[c] += bool(rr.get("files_removed"))
    return per, fails, removed


def rate(per, ids, c):
    return sum(per[e][c][0] for e in ids) / sum(per[e][c][1] for e in ids)


def gain(per, ids):
    return 100 * (rate(per, ids, "always_on") - rate(per, ids, "without_skill"))


def gain_ew(per, ids):
    f = lambda c: sum(per[e][c][0] / per[e][c][1] for e in ids) / len(ids)
    return 100 * (f("always_on") - f("without_skill"))


def summary(per, ids, rng):
    boots = sorted(gain(per, [rng.choice(ids) for _ in ids]) for _ in range(a.boot))
    lo, hi = boots[int(0.025 * a.boot)], boots[int(0.975 * a.boot) - 1]
    n = len(RUN_IDS)
    s = {c: {"pass_rate": round(rate(per, ids, c), 4), "questions": round(sum(per[e][c][2] for e in ids) / n),
             "words": round(sum(per[e][c][3] for e in ids) / n)} for c in CFG}
    s.update(gain_pp=round(gain(per, ids), 1), gain_ci95_bootstrap_over_evals=[round(lo, 1), round(hi, 1)],
             gain_eval_weighted_pp=round(gain_ew(per, ids), 1), evals=len(ids))
    return s


drops = {}
for d in a.drop:
    name, ids = d.split("="); drops[name] = {int(x) for x in ids.split(",")}
out = {"date": a.date, "skill_version": a.skill, "eval_set": a.eval_set, "runs": RUN_IDS,
       "harness": "run_behaviour3.py, Bash allowed", "grader": "claude-opus-5-5, tool calls visible, --json-schema",
       "written_by": "results/raw/harness/aggregate_set.py", "bootstrap": {"n": a.boot, "seed": a.seed}, "models": {}}
for m in M:
    if not (RUNS / m).is_dir():
        continue
    per, fails, removed = load(m)
    ids = sorted(per)
    rng = random.Random(a.seed)  # one generator per model, continued across subsets, as in sensitivity.py
    mm = summary(per, ids, rng)
    mm["subsets"] = {name: summary(per, sorted(set(ids) - drop), rng) for name, drop in drops.items()}
    mm["per_eval"] = {str(e): {c: {"runs_failed": sum(1 for x in fails[e][c] if x), "failed_assertions": fails[e][c],
                                   "runs_removing_files": removed[e][c]} for c in CFG} for e in ids}
    out["models"][m] = mm
    print(f"{m[7:-4]:6} {100*mm['without_skill']['pass_rate']:.1f} -> {100*mm['always_on']['pass_rate']:.1f}  "
          f"gain {mm['gain_pp']:+.1f} pp {mm['gain_ci95_bootstrap_over_evals']}  eval-weighted {mm['gain_eval_weighted_pp']:+.1f}  "
          f"questions {mm['without_skill']['questions']}->{mm['always_on']['questions']}  "
          f"words {mm['without_skill']['words']}->{mm['always_on']['words']}  evals {mm['evals']}")
    for name, s in mm["subsets"].items():
        print(f"         {name:28} gain {s['gain_pp']:+.1f} pp {s['gain_ci95_bootstrap_over_evals']}  eval-weighted {s['gain_eval_weighted_pp']:+.1f}  "
              f"questions {s['without_skill']['questions']}->{s['always_on']['questions']}  words {s['without_skill']['words']}->{s['always_on']['words']}")
Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
print("wrote", a.out)
