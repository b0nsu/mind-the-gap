#!/usr/bin/env python3
"""Aggregate beh4 (harness v3 with in-project import) into results/. First 3 runs per eval for totals.
behaviour-per-eval.json: all graded runs per eval (3 for most evals; 5 for evals 9, 13, 15, 17, which were run
x5 for the 1.2.1 candidates). Eval set 1.3.0 for every eval, so eval 9 there ran in an empty working directory
and eval 28 used the old assertions; the 1.4.0 rerun of evals 9 and 28 is under v121-evalset-1.4.0 and is not
in this file. Set AGG_SRC to results/raw/behaviour-1.2.1 as unpacked from results-raw-1.2.1.tar.gz at the repository root."""
import json, glob, collections, os
from pathlib import Path
S = Path(os.environ.get("AGG_SRC", str(Path(__file__).resolve().parents[1] / "behaviour-1.2.1")))
OUT = Path(__file__).resolve().parents[3] / "results"
M = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
V = {"without_skill": ("v120", "without_skill"), "always_on": ("v120", "always_on"),
     "always_on_cand_s4_s5": ("v130", "always_on"), "always_on_cand_s4_lb_ref": ("v131", "always_on")}
detail = {}
for m in M:
    out = {"model": m, "date": "2026-10-09", "skill_version": "1.2.0 body (1.2.1 differs only in the provisional label)",
           "eval_set": "1.3.0", "evals": 28, "runs_per_eval": 3}
    per = collections.defaultdict(dict)
    for name, (tag, cfg) in V.items():
        p = n = q = w = 0
        for g in sorted(glob.glob(str(S / tag / m / "eval-*" / cfg / "run-?.grade.json"))):
            run = int(g[-12]); e = int(g.split("eval-")[1][:2])
            gr = json.load(open(g)); r = json.load(open(g.replace(".grade", "")))
            d = per[e].setdefault(name, {"runs": 0, "runs_failed": 0, "words": [], "failed": []})
            d["runs"] += 1; d["words"].append(r["words"])
            f = [x["text"] for x in gr["expectations"] if not x["passed"]]
            if f: d["runs_failed"] += 1; d["failed"] += f
            if run > 3: continue
            p += sum(x["passed"] for x in gr["expectations"]); n += len(gr["expectations"]); q += gr["questions"]; w += r["words"]
        out[name] = {"pass_rate": round(p / n, 4), "questions": round(q / 3), "words": round(w / 3), "assertions": n}
    json.dump(out, open(OUT / f"behaviour-{m}.json", "w"), indent=1)
    detail[m] = per
    print(m, {k: out[k]["pass_rate"] for k in V})
detail = {"_meta": {"date": "2026-10-09", "eval_set": "1.3.0", "skill_version": "1.2.0 body (1.2.1 differs only in the provisional label)",
                    "grades": "tool calls visible (regrade of 2026-10-09)", "runs_per_eval": "3; 5 for evals 9, 13, 15, 17",
                    "source_tags": V, "note": "eval 9 ran in an empty working directory and eval 28 used the 1.3.0 assertions; "
                    "the 1.4.0 rerun of evals 9 and 28 (v121-evalset-1.4.0) is not included. Written by results/raw/harness/aggregate4.py."},
          **detail}
json.dump(detail, open(OUT / "behaviour-per-eval.json", "w"), indent=1, ensure_ascii=False)
