#!/usr/bin/env python3
"""Aggregate a run_behaviour3.py OUT/<tag> directory into results/behaviour-<model>.json and behaviour-per-eval.json.
Usage: aggregate5.py <OUT/tag dir> <date> <skill_version> <eval_set> [note]
Pass rate pools assertions over the first 3 runs per eval; questions and words are totals over evals, averaged over runs."""
import collections, glob, json, sys
from pathlib import Path
SRC = Path(sys.argv[1]); DATE, SKILL, EVALSET = sys.argv[2:5]; NOTE = sys.argv[5] if len(sys.argv) > 5 else ""
OUT = Path(__file__).resolve().parents[3] / "results"
M = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
detail = {"_meta": {"date": DATE, "skill_version": SKILL, "eval_set": EVALSET, "grades": "tool calls visible", "runs_per_eval": 3,
                    "harness": "run_behaviour3.py, Bash allowed", "note": NOTE, "written_by": "results/raw/harness/aggregate5.py"}}
for m in M:
    if not (SRC / m).is_dir(): continue
    out = {"model": m, "date": DATE, "skill_version": SKILL, "eval_set": EVALSET, "harness": "run_behaviour3.py, Bash allowed", "evals": 0, "runs_per_eval": 3}
    per = collections.defaultdict(dict)
    for cfg in ["without_skill", "always_on"]:
        p = n = q = w = 0
        for g in sorted(glob.glob(str(SRC / m / "eval-*" / cfg / "run-[123].grade.json"))):
            e = int(g.split("eval-")[1][:2]); gr = json.load(open(g)); r = json.load(open(g.replace(".grade", "")))
            d = per[e].setdefault(cfg, {"runs": 0, "runs_failed": 0, "words": [], "failed": [], "files_removed": 0})
            d["runs"] += 1; d["words"].append(r["words"]); d["files_removed"] += bool(r.get("files_removed"))
            f = [x["text"] for x in gr["expectations"] if not x["passed"]]
            if f: d["runs_failed"] += 1; d["failed"] += f
            p += sum(x["passed"] for x in gr["expectations"]); n += len(gr["expectations"]); q += gr["questions"]; w += r["words"]
        if n: out[cfg] = {"pass_rate": round(p / n, 4), "questions": round(q / 3), "words": round(w / 3), "assertions": n}
    out["evals"] = len(per)
    json.dump(out, open(OUT / f"behaviour-{m}.json", "w"), indent=1)
    detail[m] = dict(sorted(per.items()))
    print(m, {k: out[k]["pass_rate"] for k in ("without_skill", "always_on") if k in out}, "evals", len(per))
json.dump(detail, open(OUT / "behaviour-per-eval.json", "w"), indent=1, ensure_ascii=False)
