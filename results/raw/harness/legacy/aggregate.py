#!/usr/bin/env python3
"""Aggregate graded runs into results/behaviour-<model>.json plus a per-eval breakdown."""
import os, json, glob, collections, sys
from pathlib import Path

S = Path(os.environ.get("EVAL_SCRATCH", "/tmp/mind-the-gap-eval"))
OUT = Path(__file__).resolve().parents[3] / "results"
DATE = "2026-10-08"
RUNS = 3

detail = {}
for m in ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]:
    agg = {}
    per_eval = collections.defaultdict(dict)
    missing = []
    for cfg in ["without_skill", "with_skill", "always_on"]:
        p = n = q = w = 0
        for f in sorted(glob.glob(str(S / "beh" / m / "eval-*" / cfg / "run-?.json"))):
            g = Path(f[:-5] + ".grade.json")
            r = json.load(open(f))
            if not g.exists():
                missing.append(f)
                continue
            gr = json.load(open(g))
            ok = sum(e["passed"] for e in gr["expectations"])
            p += ok; n += len(gr["expectations"]); q += gr["questions"]; w += r["words"]
            e = per_eval[r["eval_id"]].setdefault(cfg, {"runs_failed": 0, "assertions_failed": [], "words": [], "questions": []})
            e["words"].append(r["words"]); e["questions"].append(gr["questions"])
            fails = [x["text"] for x in gr["expectations"] if not x["passed"]]
            if fails:
                e["runs_failed"] += 1
                e["assertions_failed"] += fails
        # totals are per run-set: summed over evals, averaged over the RUNS repetitions
        agg[cfg] = {"pass_rate": round(p / n, 4) if n else None, "questions": round(q / RUNS),
                    "words": round(w / RUNS), "assertions": n}
    json.dump({"model": m, "date": DATE, "runs_per_eval": RUNS, "skipped_evals": [8], **{k: v for k, v in agg.items() if v["assertions"]}},
              open(OUT / f"behaviour-{m}.json", "w"), indent=1)
    detail[m] = per_eval
    print(m, agg, "missing grades:", len(missing))
json.dump(detail, open(OUT / "behaviour-per-eval.json", "w"), indent=1, ensure_ascii=False)
