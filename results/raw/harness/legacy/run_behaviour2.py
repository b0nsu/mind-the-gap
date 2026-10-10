#!/usr/bin/env python3
"""Behaviour evals, v2: one fresh project dir per run, fixture files copied in,
file-editing tools allowed, final file contents recorded for the grader.

Usage: run_behaviour2.py <models,comma> <runs> <eval ids,comma>
"""
import json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

S = Path(os.environ.get("EVAL_SCRATCH", "/tmp/mind-the-gap-eval"))
REPO = Path(__file__).resolve().parents[4]
SKILL = Path(os.environ.get("SKILL_SRC", REPO / "skills/mind-the-gap"))
OUT = Path(os.environ.get("OUT", S / "beh"))
WORK = S / "work"
MODELS = sys.argv[1].split(",")
RUNS = int(sys.argv[2])
IDS = {int(x) for x in sys.argv[3].split(",")}

APPEND = ("The mind-the-gap skill is installed for this session. Before you respond, "
          "invoke it with the Skill tool and follow its instructions for this request.")
TOOLS = "Skill,Read,Glob,Grep,Write,Edit"

evals = [e for e in json.load(open(REPO / "evals/evals.json"))["evals"] if e["id"] in IDS]
env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}


def snapshot(d):
    return {str(p.relative_to(d)): p.read_text(errors="replace")
            for p in sorted(d.rglob("*")) if p.is_file() and ".claude" not in p.parts and "mind-the-gap" not in p.parts and p.name != "CLAUDE.md"}


def one(job):
    model, cfg, ev, run = job
    f = OUT / model / f"eval-{ev['id']:02d}" / cfg / f"run-{run}.json"
    if f.exists():
        return
    f.parent.mkdir(parents=True, exist_ok=True)
    wd = WORK / f"{model}-{ev['id']:02d}-{cfg}-{run}"
    shutil.rmtree(wd, ignore_errors=True)
    for src in ev.get("files", []):
        shutil.copytree(SKILL / src, wd, dirs_exist_ok=True)
    (wd / ".claude").mkdir(parents=True, exist_ok=True)
    if cfg == "with_skill":
        shutil.copytree(SKILL, wd / ".claude/skills/mind-the-gap", ignore=shutil.ignore_patterns("evals"))
    if cfg == "always_on":
        shutil.copytree(SKILL, wd / "mind-the-gap", ignore=shutil.ignore_patterns("evals"))
        (wd / "CLAUDE.md").write_text("@mind-the-gap/SKILL.md\n")
    before = snapshot(wd)
    cmd = ["claude", "-p", ev["prompt"], "--model", model, "--setting-sources", "project",
           "--output-format", "stream-json", "--verbose", "--allowedTools", TOOLS,
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
    if cfg == "with_skill":
        cmd += ["--append-system-prompt", APPEND]
    try:
        p = subprocess.run(cmd, cwd=wd, env=env, capture_output=True, text=True, timeout=900)
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
    after = snapshot(wd)
    changed = {k: v for k, v in after.items() if before.get(k) != v}
    json.dump({"eval_id": ev["id"], "config": cfg, "run": run, "model": real_model,
               "prompt": ev["prompt"], "tools": tools, "response": result,
               "files_changed": changed, "words": len(result.split())},
              open(f, "w"), ensure_ascii=False, indent=1)
    print("ok", f.relative_to(OUT), flush=True)


jobs = [(m, c, e, r) for m in MODELS for e in evals for c in os.environ.get("CFGS", "with_skill,without_skill").split(",") for r in range(1, RUNS + 1)]
with ThreadPoolExecutor(6) as ex:
    list(ex.map(one, jobs))
print("done", len(jobs))
