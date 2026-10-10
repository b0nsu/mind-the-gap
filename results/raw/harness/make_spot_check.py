#!/usr/bin/env python3
"""Draw a blind grader spot-check sheet from a run_behaviour3.py output directory.

Writes two files: the sheet (runs, tool calls, workspace files, assertions with empty verdict boxes;
no model, configuration or grader verdict) and the KEY (grader verdicts and evidence per sample).
Layout follows results/grader-spot-check-2026-10-09b.md.

Stratification, as in the 2026-10-09b sample: 2 runs each from evals 15, 28 and 9 (for 28 and 9 one that
the grader passed and one it failed, when both exist), 3 from the overreach evals 18-26 (one per model),
6 from the remaining evals; 5 per model; 4 to 8 without_skill.

Usage: make_spot_check.py <run_dir> <sheet.md> <key.md> [seed] [label]
  run_dir  e.g. results/raw/behaviour-1.3.0 (<model>/eval-NN/<cfg>/run-N.json + .grade.json)
  EVALS_JSON  eval file (default evals/evals.json)
"""
import glob, json, os, random, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
RUN_DIR, SHEET, KEY = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
SEED = int(sys.argv[4]) if len(sys.argv) > 4 else 20261011
LABEL = sys.argv[5] if len(sys.argv) > 5 else RUN_DIR.name
EVALS = {e["id"]: e for e in json.load(open(os.environ.get("EVALS_JSON", REPO / "evals/evals.json")))["evals"]}
MODELS = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
CFGS = ["without_skill", "always_on"]
FILE_CAP = 4000

runs = []
for g in sorted(glob.glob(str(RUN_DIR / "*" / "eval-*" / "*" / "run-*.grade.json"))):
    p = Path(g); r = json.load(open(p.with_suffix("").with_suffix(".json"))); gr = json.load(open(p))
    if r["config"] not in CFGS: continue
    runs.append(dict(model=r["model"], cfg=r["config"], ev=r["eval_id"], run=r["run"], r=r, g=gr,
                     failed=not all(x["passed"] for x in gr["expectations"])))

rng = random.Random(SEED)


def pick(pool, n, per_model=None):
    pool = [x for x in pool if x not in chosen]
    rng.shuffle(pool)
    out = []
    for x in pool:
        if len(out) >= n: break
        if per_model is not None and per_model.get(x["model"], 0) >= 1: continue
        out.append(x)
        if per_model is not None: per_model[x["model"]] = per_model.get(x["model"], 0) + 1
    return out


chosen = []
for ev in (15, 28, 9):
    pool = [x for x in runs if x["ev"] == ev]
    if ev in (28, 9):
        f = pick([x for x in pool if x["failed"]], 1); chosen += f
        chosen += pick([x for x in pool if not x["failed"]], 1) or pick(pool, 1)
    else:
        chosen += pick(pool, 2)
chosen += pick([x for x in runs if 18 <= x["ev"] <= 26], 3, per_model={})
rest = [x for x in runs if x["ev"] not in (15, 28, 9) and not 18 <= x["ev"] <= 26]
for _ in range(500):  # draw six that balance models to 5 each and 4 <= without_skill <= 8
    cand = chosen + pick(rest, 6)
    pm = {m: sum(1 for x in cand if x["model"] == m) for m in MODELS}
    if all(v == 5 for v in pm.values()) and 4 <= sum(1 for x in cand if x["cfg"] == "without_skill") <= 8:
        chosen = cand; break
else:
    sys.exit("could not balance the sample; change the seed")
rng.shuffle(chosen)

leak = re.compile(r"CLAUDE\.md|\.claude/acs|\bskill\b", re.I)
leaks = []
sheet = [f"# 채점 검수 샘플 (blind) — {LABEL}\n",
         f"{len(chosen)}건, 단언문 {sum(len(x['g']['expectations']) for x in chosen)}개. 모델·조건·채점자 판정은 이 파일에 없고 `{KEY.name}`에 있습니다. 판정을 다 채운 뒤에 여세요.\n",
         "구성: eval 15·28·9에서 각 2건(eval 28·9는 채점자 통과 1건과 실패 1건), overreach eval 18~26에서 3건(모델별 1건), 나머지 eval에서 6건. 모델별 5건, 스킬 없음 4~8건. "
         f"seed {SEED}, `results/raw/harness/make_spot_check.py`.\n",
         "판정 기준: 응답, 도구 호출, 작업 공간 파일에 근거가 분명하면 PASS, 아니면 FAIL. 단언문 자체가 이상하면 '단언문 문제'에 체크하세요.\n"]
body = []
key = [f"# 정답표 — {LABEL}\n", "| 샘플 | 모델 | 조건 | eval·run | 채점자 판정 (단언문 순서) | 채점자가 실패로 본 단언문과 근거 |", "|---|---|---|---|---|---|"]
for i, x in enumerate(chosen, 1):
    r, g, e = x["r"], x["g"], EVALS[x["ev"]]
    hid = f"H{i:02d}"
    body.append(f"---\n## {hid} — eval {x['ev']} ({e['group']})\n")
    for t, turn in enumerate(r["transcript"], 1):
        q = "\n".join("> " + l for l in turn["user"].splitlines())
        body.append(f"**User (turn {t})**\n\n{q}\n")
        a = turn["assistant"]
        body.append(f"**Assistant (turn {t})** ({len(a.split())} words)\n\n````text\n{a}\n````\n")
        if leak.search(a): leaks.append(hid)
    tools = r.get("tools", [])
    body.append(f"<details><summary>도구 호출 {len(tools)}건 (입력만 기록, 권한 거부로 막힌 호출도 포함)</summary>\n\n````text")
    body.append("\n".join(f"turn {t['turn']}: {t['name']} {json.dumps(t['input'], ensure_ascii=False)}" for t in tools) or "(없음)")
    body.append("````\n</details>\n")
    ff = r.get("final_files") or {}
    removed = r.get("files_removed") or []
    if not ff and not removed:
        body.append("**작업 공간 파일 (마지막 턴 이후)**: 없음\n")
    else:
        body.append("**작업 공간 파일 (마지막 턴 이후)**" + (f" — 삭제됨: {', '.join(removed)}" if removed else "") + "\n")
        for name, content in sorted(ff.items()):
            c = content if isinstance(content, str) else json.dumps(content, ensure_ascii=False)
            if len(c) > FILE_CAP: c = c[:FILE_CAP] + f"\n… ({len(c) - FILE_CAP} more characters)"
            body.append(f"<details><summary>{name}</summary>\n\n````text\n{c}\n````\n</details>\n")
    body.append(f"**기대 행동**: {e['expected_output']}\n")
    body.append("| # | 단언문 | 판정 | 단언문 문제 |\n|---|---|---|---|")
    for n, a in enumerate(e["expectations"], 1):
        body.append(f"| {n} | {a} | ☐ PASS ☐ FAIL | ☐ |")
    body.append("")
    verdicts = " ".join("P" if a["passed"] else "F" for a in g["expectations"])
    ev_txt = " / ".join(f"{n}: {a.get('evidence', '')[:200]}" for n, a in enumerate(g["expectations"], 1) if not a["passed"])
    key.append(f"| {hid} | {x['model']} | {x['cfg']} | eval {x['ev']} run {x['run']} ({r.get('skill_tag', '')}) | {verdicts} | {ev_txt.replace('|', '¦')} |")
sheet.append("blind가 깨질 수 있는 샘플: " + (", ".join(leaks) + " (응답에 `CLAUDE.md`, `.claude/acs` 또는 skill 언급)" if leaks else "없음. 응답에서 `CLAUDE.md`, `.claude/acs`, skill 언급을 검색해 찾지 못했습니다.") + " 도구 호출 목록에는 `CLAUDE.md`를 읽은 기록이 보일 수 있습니다.\n")
SHEET.write_text("\n".join(sheet + body))
KEY.write_text("\n".join(key) + "\n")
print(f"{len(chosen)} samples, {sum(len(x['g']['expectations']) for x in chosen)} assertions; leaks: {leaks or 'none'}")
for x in chosen: print(f"  {x['model']:18s} {x['cfg']:14s} eval {x['ev']:2d} run {x['run']}  {'FAIL' if x['failed'] else 'pass'}")
