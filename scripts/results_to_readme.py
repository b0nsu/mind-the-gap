#!/usr/bin/env python3
"""Turn result files into the behaviour table and the trigger_set.json table in docs/measurements.md.

Usage (files in the order the README rows should appear):
  python scripts/results_to_readme.py \
      --behaviour results/behaviour-claude-{haiku,sonnet,opus}-5-5.json \
      --trigger  results/trigger-claude-{haiku,sonnet,opus}-5-5.json

behaviour-<model>.json (one per model, written by a grader aggregate):
  {"model": "...", "date": "YYYY-MM-DD",
   "without_skill": {"pass_rate": 0.7683, "questions": 28, "words": 6158},
   "always_on":     {"pass_rate": 0.9714, "questions": 33, "words": 5799}}
Rows are printed for without_skill, with_skill and always_on when present;
other keys (e.g. always_on_cand_*) are not printed.

trigger-<model>.json: the JSON that results/raw/harness/run_eval.py writes,
plus top-level "model" and "date" keys added by hand.

Prints markdown to stdout; paste over the two tables in docs/measurements.md. The
sensitivity and held-out trigger tables are not generated.
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
            print(f"| {d['model']} | {cfg.replace('_',' ')} | "
                  f"{r['pass_rate']:.0%} | {r['questions']} | {r['words']} |")
    print()

if a.trigger:
    rows = []
    for p in a.trigger:
        d = json.load(open(p))
        pos = [r for r in d["results"] if r["should_trigger"]]
        neg = [r for r in d["results"] if not r["should_trigger"]]
        rows.append((f"{d.get('model','?')} ({d.get('date','')})", pos, neg))
    print(f"| Model | Should trigger ({len(rows[0][1])}) | Should not trigger ({len(rows[0][2])}) |")
    print("|---|---|---|")
    for model, pos, neg in rows:
        print(f"| {model} | {sum(r['pass'] for r in pos)}/{len(pos)} fired | "
              f"{sum(r['pass'] for r in neg)}/{len(neg)} quiet |")
