#!/usr/bin/env python3
"""Turn skill-creator result files into the two README tables.

Usage:
  python scripts/results_to_readme.py \
      --behaviour results/behaviour-<model>.json [more...] \
      --trigger  results/trigger-<model>.json  [more...]

behaviour-<model>.json (one per model, written by hand or by a grader):
  {"model": "...", "date": "YYYY-MM-DD",
   "without_skill": {"pass_rate": 0.77, "questions": 41, "words": 9849},
   "with_skill":    {"pass_rate": 0.93, "questions": 19, "words": 7094}}

trigger-<model>.json: the JSON that scripts/run_eval.py writes, plus a
top-level "model" key added by hand if run_eval did not record it.

Prints markdown to stdout; paste over the tables in README.md.
"""
import argparse, json

ap = argparse.ArgumentParser()
ap.add_argument("--behaviour", nargs="*", default=[])
ap.add_argument("--trigger", nargs="*", default=[])
a = ap.parse_args()

if a.behaviour:
    print("| Model | Config | Pass rate | Questions (total) | Words (total) |")
    print("|---|---|---|---|---|")
    for p in a.behaviour:
        d = json.load(open(p))
        for cfg in ("without_skill", "with_skill", "always_on"):
            if cfg not in d:
                continue
            r = d[cfg]
            print(f"| {d['model']} ({d.get('date','')}) | {cfg.replace('_',' ')} | "
                  f"{r['pass_rate']:.0%} | {r['questions']} | {r['words']} |")
    print()

if a.trigger:
    print("| Model | Should trigger | Should not trigger |")
    print("|---|---|---|")
    for p in a.trigger:
        d = json.load(open(p))
        pos = [r for r in d["results"] if r["should_trigger"]]
        neg = [r for r in d["results"] if not r["should_trigger"]]
        print(f"| {d.get('model','?')} | {sum(r['pass'] for r in pos)}/{len(pos)} fired | "
              f"{sum(r['pass'] for r in neg)}/{len(neg)} quiet |")
