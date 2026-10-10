#!/usr/bin/env python3
"""Aggregate the held-out set over several runs and grade sets.
Usage: aggregate_heldout.py <runs dir> <regrade dir> <out json> [n_boot] [seed]
  runs dir    OUT/current of run_behaviour3.py with EVALS_JSON=evals/evals_heldout.json (run-1..6)
  regrade dir grade files of runs 1-3 regraded under eval set 1.0.1 (evals 101, 107, 108), same layout
Variants: first3 = runs 1-3 under 1.0.0 (as first published); second3 = runs 4-6 under 1.0.1;
all6 = runs 1-6 under 1.0.1 (runs 1-3 with the regrade substituted where it exists).
Pooled pass rate, bootstrap over evals, eval-weighted gain, questions and words per run (as sensitivity.py)."""
import glob, json, random, sys
from pathlib import Path

RUNS, RG, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
NB = int(sys.argv[4]) if len(sys.argv) > 4 else 10000
SEED = int(sys.argv[5]) if len(sys.argv) > 5 else 0
M = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
CFG = ["without_skill", "always_on"]


def load(model, runs, substitute):
    per, fails = {}, {}
    for c in CFG:
        for r in runs:
            for f in sorted(glob.glob(str(RUNS / model / "eval-*" / c / f"run-{r}.json"))):
                e = int(f.split("eval-")[1][:3])
                g = Path(f.replace(".json", ".grade.json"))
                rgf = RG / g.relative_to(RUNS)
                if substitute and rgf.exists():
                    g = rgf
                gr = json.load(open(g)); rr = json.load(open(f))
                d = per.setdefault(e, {k: [0, 0, 0, 0] for k in CFG})[c]
                d[0] += sum(x["passed"] for x in gr["expectations"]); d[1] += len(gr["expectations"])
                d[2] += gr["questions"]; d[3] += rr["words"]
                fails.setdefault(e, {k: [] for k in CFG})[c].append([i for i, x in enumerate(gr["expectations"], 1) if not x["passed"]])
    return per, fails


def rate(per, ids, c):
    return sum(per[e][c][0] for e in ids) / sum(per[e][c][1] for e in ids)


def gain(per, ids):
    return 100 * (rate(per, ids, "always_on") - rate(per, ids, "without_skill"))


def gain_ew(per, ids):
    f = lambda c: sum(per[e][c][0] / per[e][c][1] for e in ids) / len(ids)
    return 100 * (f("always_on") - f("without_skill"))


VARIANTS = {"first3": ([1, 2, 3], False, "eval set 1.0.0 grades, as first published"),
            "second3": ([4, 5, 6], True, "eval set 1.0.1 grades"),
            "all6": ([1, 2, 3, 4, 5, 6], True, "eval set 1.0.1 grades; runs 1-3 of evals 101, 107, 108 from the regrade")}
out = {"date": "2026-10-10", "skill_version": "1.3.0", "eval_set": "evals_heldout.json 1.0.0 (first 3 runs) / 1.0.1 (runs 4-6 and the all6 variant)",
       "harness": "run_behaviour3.py, Bash allowed", "grader": "claude-opus-5-5, tool calls visible",
       "raw": "results/raw/behaviour-heldout-1.3.0/ (runs 1-6) and results/raw/behaviour-heldout-1.3.0-regrade-1.0.1/ (release asset)",
       "written_by": "results/raw/harness/aggregate_heldout.py", "variants": {}}
for name, (runs, sub, desc) in VARIANTS.items():
    v = {"runs": runs, "grades": desc, "models": {}}
    print(f"\n== {name}: runs {runs}, {desc}")
    for m in M:
        per, fails = load(m, runs, sub)
        ids = sorted(per)
        rng = random.Random(SEED)
        boots = sorted(gain(per, [rng.choice(ids) for _ in ids]) for _ in range(NB))
        lo, hi = boots[int(0.025 * NB)], boots[int(0.975 * NB) - 1]
        n = len(runs)
        mm = {c: {"pass_rate": round(rate(per, ids, c), 4), "questions": round(sum(per[e][c][2] for e in ids) / n),
                  "words": round(sum(per[e][c][3] for e in ids) / n)} for c in CFG}
        mm["gain_pp"] = round(gain(per, ids), 1); mm["gain_ci95_bootstrap_over_evals"] = [round(lo, 1), round(hi, 1)]
        mm["gain_eval_weighted_pp"] = round(gain_ew(per, ids), 1)
        mm["per_eval"] = {str(e): {c: {"runs_failed": sum(1 for x in fails[e][c] if x), "failed_assertions": fails[e][c]} for c in CFG} for e in ids}
        v["models"][m] = mm
        print(f"  {m[7:-4]:6} {100*mm['without_skill']['pass_rate']:.1f} -> {100*mm['always_on']['pass_rate']:.1f}  gain {mm['gain_pp']:+5.1f} pp [{lo:+5.1f}, {hi:+5.1f}]  "
              f"eval-weighted {mm['gain_eval_weighted_pp']:+5.1f}  questions {mm['without_skill']['questions']}->{mm['always_on']['questions']}  "
              f"words {mm['without_skill']['words']}->{mm['always_on']['words']}  evals {len(ids)}")
    out["variants"][name] = v
    print("  failed runs per eval, without -> always on (Haiku | Sonnet | Opus):")
    for e in sorted(v["models"][M[0]]["per_eval"]):
        cells = [f"{v['models'][m]['per_eval'][e]['without_skill']['runs_failed']} -> {v['models'][m]['per_eval'][e]['always_on']['runs_failed']}" for m in M]
        print(f"    {e}  {' | '.join(cells)}")
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
print("\nwrote", OUT)
