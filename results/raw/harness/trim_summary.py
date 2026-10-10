import json, glob, collections
from pathlib import Path
OUT=Path("/tmp/mind-the-gap-eval/beh-trim"); TAGS=["v121","t1-maint","t2-s7","t3-s5conf"]
M=["claude-haiku-5-5","claude-sonnet-5-5","claude-opus-5-5"]; TARGET=[9,12,14,24,27]
print("pass rate, first 3 runs, all 28 evals (assertions passed/total)")
for m in M:
    row=[]
    for t in TAGS:
        p=n=0; missing=0
        for g in glob.glob(str(OUT/t/m/"eval-*"/"always_on"/"run-[123].grade.json")):
            gr=json.load(open(g)); p+=sum(x["passed"] for x in gr["expectations"]); n+=len(gr["expectations"])
        row.append(f"{t}: {p/n:.3f} ({p}/{n})")
    print(f"  {m:18s} "+"  ".join(row))
print("\nfailed runs on target evals, 5 runs (runs failed / runs; failed assertion numbers)")
for e in TARGET:
    print(f" eval {e}")
    for m in M:
        row=[]
        for t in TAGS:
            fails=[]; n=0
            for g in sorted(glob.glob(str(OUT/t/m/f"eval-{e:02d}"/"always_on"/"run-?.grade.json"))):
                gr=json.load(open(g)); n+=1
                f=[i+1 for i,x in enumerate(gr["expectations"]) if not x["passed"]]
                if f: fails.append(f)
            row.append(f"{t}: {len(fails)}/{n} {fails}")
        print(f"  {m:18s} "+" | ".join(row))
print("\neval 9 files removed (runs that deleted), 5 runs")
for m in M:
    row=[]
    for t in TAGS:
        d=0;n=0
        for f in sorted(glob.glob(str(OUT/t/m/"eval-09"/"always_on"/"run-?.json"))):
            r=json.load(open(f)); n+=1; d+= bool(r.get("files_removed"))
        row.append(f"{t}: {d}/{n}")
    print(f"  {m:18s} "+"  ".join(row))
