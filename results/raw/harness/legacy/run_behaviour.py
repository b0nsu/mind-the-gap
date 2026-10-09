#!/usr/bin/env python3
"""Run behaviour evals: each eval x {with_skill, without_skill} x runs x models.

Isolation: claude -p --setting-sources project from a scratch project dir, so
user-level skills (incl. the installed ai-collaboration), plugins and CLAUDE.md
are not loaded. with_skill dir has the skill under .claude/skills/; the
append-system-prompt tells the model to load it first (skill-creator style).
"""
import json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

S = Path(os.environ.get("EVAL_SCRATCH", "/tmp/mind-the-gap-eval"))
REPO = Path(__file__).resolve().parents[3]
SKILL = Path(os.environ.get("SKILL_SRC", REPO / "skills/mind-the-gap"))
OUT = Path(os.environ.get("OUT", S / "beh"))
MODELS = sys.argv[1].split(",")
RUNS = int(sys.argv[2])
SKIP = {8} | {int(x) for x in sys.argv[3].split(',')} if len(sys.argv) > 3 else {8}

dirs = {"with_skill": S / os.environ.get("PROJ", "proj_with"), "without_skill": S / "proj_without", "always_on": S / "proj_always"}
CFGS = os.environ.get("CFGS", "with_skill,without_skill").split(",")
if os.environ.get("ONLY_WITH"): CFGS = ["with_skill"]
dirs = {k: v for k, v in dirs.items() if k in CFGS}
for d in dirs.values():
    (d / ".claude").mkdir(parents=True, exist_ok=True)
if "with_skill" in dirs:
    dst = dirs["with_skill"] / ".claude/skills/mind-the-gap"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(SKILL, dst, ignore=shutil.ignore_patterns("evals"))
if "always_on" in dirs:
    # Always-on install: project CLAUDE.md imports the skill body; no skill registered.
    dst = dirs["always_on"] / "mind-the-gap"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(SKILL, dst, ignore=shutil.ignore_patterns("evals"))
    (dirs["always_on"] / "CLAUDE.md").write_text("@mind-the-gap/SKILL.md\n")

APPEND = ("The mind-the-gap skill is installed for this session. Before you respond, "
          "invoke it with the Skill tool and follow its instructions for this request.")

evals = [e for e in json.load(open(REPO / "evals/evals.json"))["evals"] if e["id"] not in SKIP]
env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}


def one(job):
    model, cfg, ev, run = job
    f = OUT / model / f"eval-{ev['id']:02d}" / cfg / f"run-{run}.json"
    if f.exists():
        return
    f.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["claude", "-p", ev["prompt"], "--model", model, "--setting-sources", "project",
           "--output-format", "stream-json", "--verbose", "--allowedTools", "Skill,Read",
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
    if cfg == "with_skill":
        cmd += ["--append-system-prompt", APPEND]
    try:
        p = subprocess.run(cmd, cwd=dirs[cfg], env=env, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        print("TIMEOUT", f, flush=True)
        return
    tools, result, real_model = [], None, None
    for line in p.stdout.splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "system" and e.get("subtype") == "init":
            real_model = e.get("model")
        elif e.get("type") == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "tool_use":
                    tools.append({"name": c["name"], "input": c.get("input")})
        elif e.get("type") == "result":
            result = e.get("result")
            if e.get("is_error") or str(result).startswith("You've hit your"):
                print("ERROR", f, str(result)[:120], flush=True)
                return
    if result is None:
        print("NORESULT", f, p.stderr[-300:], flush=True)
        return
    json.dump({"eval_id": ev["id"], "config": cfg, "run": run, "model": real_model,
               "prompt": ev["prompt"], "tools": tools, "response": result,
               "words": len(result.split())}, open(f, "w"), ensure_ascii=False, indent=1)
    print("ok", f.relative_to(OUT), flush=True)


jobs = [(m, c, e, r) for m in MODELS for e in evals for c in dirs for r in range(1, RUNS + 1)]
with ThreadPoolExecutor(6) as ex:
    list(ex.map(one, jobs))
print("done", len(jobs))
