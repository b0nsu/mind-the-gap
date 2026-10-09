#!/usr/bin/env python3
"""Compare skill snapshots on a few evals: runs failed, failed assertion ids, files removed, questions.
Usage: compare_tags.py <OUT dir> <tag,tag,...> [eval ids,comma]"""
import glob, json, sys
from pathlib import Path
OUT = Path(sys.argv[1]); TAGS = sys.argv[2].split(",")
IDS = {int(x) for x in sys.argv[3].split(",")} if len(sys.argv) > 3 else None
M = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
for m in M:
    for e in sorted({int(p.split("eval-")[1][:2]) for t in TAGS for p in glob.glob(str(OUT / t / m / "eval-*"))}):
        if IDS and e not in IDS: continue
        for t in TAGS:
            for c in sorted({Path(p).name for p in glob.glob(str(OUT / t / m / f"eval-{e:02d}" / "*"))}):
                rows = []
                for f in sorted(glob.glob(str(OUT / t / m / f"eval-{e:02d}" / c / "run-?.json"))):
                    g = Path(f.replace(".json", ".grade.json"))
                    if not g.exists(): continue
                    r = json.load(open(f)); gr = json.load(open(g))
                    bad = [i + 1 for i, x in enumerate(gr["expectations"]) if not x["passed"]]
                    rows.append((bad, bool(r["files_removed"]), gr["questions"]))
                if not rows: continue
                print(f"{m[7:-4]:6} eval {e:2} {t:15} {c:14} failed {sum(1 for b,_,_ in rows if b)}/{len(rows)}"
                      f"  asserts {[b for b,_,_ in rows]}  removed {sum(d for _,d,_ in rows)}  questions {[q for _,_,q in rows]}")
