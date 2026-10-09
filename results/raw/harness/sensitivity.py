#!/usr/bin/env python3
"""Sensitivity of the always-on gain to eval selection.
First 3 runs per eval; 95% interval from bootstrap resamples over evals.
Variants: A as reported (eval set 1.3.0, v120); B evals 9 and 28 from the 1.4.0 rerun (v121-evalset-1.4.0, runs 1-3);
C = B without eval 17; D = C without eval 11.
Usage: sensitivity.py [n_boot] [seed]"""
import glob, json, random, sys
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "behaviour-1.2.1"
M = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
CFG = ["without_skill", "always_on"]
NB = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 0

if not RAW.is_dir():
    sys.exit(f"{RAW} not found. Unpack results-raw-1.2.1.tar.gz at the repository root (see README).")


def load(tag, model, evals=None):
    out = {}
    for c in CFG:
        for g in glob.glob(str(RAW / tag / model / "eval-*" / c / "run-[123].grade.json")):
            e = int(g.split("eval-")[1][:2])
            if evals and e not in evals:
                continue
            gr = json.load(open(g)); r = json.load(open(g.replace(".grade", "")))
            d = out.setdefault(e, {k: [0, 0, 0, 0] for k in CFG})[c]
            d[0] += sum(x["passed"] for x in gr["expectations"]); d[1] += len(gr["expectations"])
            d[2] += gr["questions"]; d[3] += r["words"]
    return out


def rate(per, ids, c):
    p = sum(per[e][c][0] for e in ids); n = sum(per[e][c][1] for e in ids)
    return p / n


def gain(per, ids):
    return 100 * (rate(per, ids, "always_on") - rate(per, ids, "without_skill"))


def gain_eval_weighted(per, ids):
    """Mean over evals of each eval's pass rate, so an eval with 6 assertions weighs the same as one with 3."""
    f = lambda c: sum(per[e][c][0] / per[e][c][1] for e in ids) / len(ids)
    return 100 * (f("always_on") - f("without_skill"))


for m in M:
    a = load("v120", m)
    b = dict(a); b.update(load("v121-evalset-1.4.0", m, {9, 28}))
    variants = {"A": (a, sorted(a)), "B": (b, sorted(b)), "C": (b, sorted(set(b) - {17})), "D": (b, sorted(set(b) - {17, 11}))}
    rng = random.Random(SEED)
    for name, (per, ids) in variants.items():
        boots = sorted(gain(per, [rng.choice(ids) for _ in ids]) for _ in range(NB))
        lo, hi = boots[int(0.025 * NB)], boots[int(0.975 * NB) - 1]
        q = [round(sum(per[e][c][2] for e in ids) / 3) for c in CFG]
        w = [round(sum(per[e][c][3] for e in ids) / 3) for c in CFG]
        print(f"{m[7:-4]:6} {name}  {gain(per, ids):+5.1f} pp [{lo:+5.1f}, {hi:+5.1f}]  eval-weighted {gain_eval_weighted(per, ids):+5.1f} pp  "
              f"questions {q[0]}->{q[1]}  words {w[0]}->{w[1]}  evals {len(ids)}")
