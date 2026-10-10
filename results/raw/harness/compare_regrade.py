#!/usr/bin/env python3
"""Compare old grades (asset) vs regrade (mode-free expected_output), per verdict and per model/config pass rate.
Usage: compare_regrade.py <old_root> <new_root>   (same directory layout below both)"""
import json, sys, collections
from pathlib import Path
old, new = Path(sys.argv[1]), Path(sys.argv[2])
M = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
changed = collections.Counter(); tot = 0; flips = []
rate = collections.defaultdict(lambda: [0, 0, 0])  # (tag,model,cfg) -> [old_pass, new_pass, n]
ev8 = collections.defaultdict(lambda: [0, 0, 0])   # per 8 touched evals, (eval,model,cfg)
for g in sorted(new.rglob("run-?.grade.json")):
    rel = g.relative_to(new); o = old / rel
    if not o.exists(): continue
    a = json.load(open(o))["expectations"]; b = json.load(open(g))["expectations"]
    tag, model, ev, cfg = rel.parts[-5], rel.parts[-4], int(rel.parts[-3][5:]), rel.parts[-2]
    if tag not in ("v120", "v130", "v131", "v121-evalset-1.4.0"): tag, model, ev, cfg = rel.parts[-4], rel.parts[-3], int(rel.parts[-2][5:]), rel.parts[-1]
    for i, (x, y) in enumerate(zip(a, b)):
        tot += 1
        r = rate[(tag, model, cfg)]; r[0] += x["passed"]; r[1] += y["passed"]; r[2] += 1
        if ev in (3, 4, 7, 9, 10, 11, 14, 17):
            e = ev8[(ev, model, cfg)]; e[0] += x["passed"]; e[1] += y["passed"]; e[2] += 1
        if x["passed"] != y["passed"]:
            changed["pass->fail" if x["passed"] else "fail->pass"] += 1
            flips.append((str(rel), ev, i + 1, "P>F" if x["passed"] else "F>P"))
print(f"verdicts compared: {tot}; changed: {sum(changed.values())} ({dict(changed)})")
print("\nper tag/model/config pass rate old -> new (n):")
for k in sorted(rate): o, n, c = rate[k]; print(f"  {k[0]:22s} {k[1]:18s} {k[2]:14s} {o/c:.3f} -> {n/c:.3f} ({c})")
print("\nthe 8 touched evals, assertions passed old -> new (n):")
for k in sorted(ev8): o, n, c = ev8[k]; print(f"  eval {k[0]:2d} {k[1]:18s} {k[2]:14s} {o:3d} -> {n:3d} ({c})")
cf = collections.Counter((e, d) for _, e, _, d in flips)
print("\nflips by eval:", sorted(cf.items()))
