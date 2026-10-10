#!/usr/bin/env python3
"""Behaviour evals, v3 (harness fix after review E-1).

- Work dirs live under $EVAL_SCRATCH/evalwork/<random>; the path carries no skill or repo name.
- The skill under test lives outside the work dir. always_on copies SKILL.md and references/ into
  .claude/acs and imports them from CLAUDE.md with '@.claude/acs/SKILL.md' (claude -p does not expand
  imports that point outside the project), so always_on runs can see those files.
  with_skill loads it as a plugin via --plugin-dir. without_skill and with_skill work dirs hold no skill files.
- Fixtures (eval "files") are copied in; eval "plugins" are passed with --plugin-dir; eval "force_skill"
  appends a system prompt telling the model to load that skill (used by eval 8).
- Multi-turn evals ("turns") reuse one session via --session-id / --resume.
- Records the final file snapshot and the full transcript of user/assistant turns.
- Allowed tools come from $TOOLS (default includes Bash). Runs recorded before 2026-10-10 used
  "Skill,Read,Glob,Grep,Write,Edit": every Bash call, including eval 9's --dry-run, was refused by
  claude -p (no prompt is shown in headless mode), and every eval 9 response mentioned the refusal.

Usage: run_behaviour3.py <models,comma> <runs> <eval ids,comma|all> <cfg,cfg> [skill_tag]
  cfg: without_skill | always_on | with_skill
  skill_tag: name of a dir under $EVAL_SCRATCH/evalskills (default: current). The tag "current" is
  created from $REPO/skills/mind-the-gap when missing; other tags are snapshots you place there by hand
  (<tag>/skill = a copy of the skill folder, <tag>/plugin = a plugin wrapper around the same files).
Env: EVAL_SCRATCH, OUT, TOOLS, WORKERS, CLAUDE_BIN, EVALS_JSON (default evals/evals.json; grade3.py takes the same variable).
"""
import json, os, shutil, subprocess, sys, uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

S = Path(os.environ.get("EVAL_SCRATCH", "/tmp/mind-the-gap-eval"))
REPO = Path(__file__).resolve().parents[3]
EVALS = REPO / "evals"
WORKROOT = S / "evalwork"
SKILLS = S / "evalskills"
OUT = Path(os.environ.get("OUT", S / "beh3"))
MODELS = sys.argv[1].split(",")
RUNS = int(sys.argv[2])
ALL = json.load(open(os.environ.get("EVALS_JSON", EVALS / "evals.json")))["evals"]  # e.g. evals/evals_heldout.json
IDS = {e["id"] for e in ALL} if sys.argv[3] == "all" else {int(x) for x in sys.argv[3].split(",")}
CFGS = sys.argv[4].split(",")
TAG = sys.argv[5] if len(sys.argv) > 5 else "current"
SKILLDIR = SKILLS / TAG / "skill"          # .../skill/SKILL.md, references/
PLUGDIR = SKILLS / TAG / "plugin"          # plugin wrapper around the same files
TOOLS = os.environ.get("TOOLS", "Skill,Read,Glob,Grep,Write,Edit,Bash")
FORCE = ("The {name} skill is installed for this session. Before you respond, "
         "invoke it with the Skill tool and follow its instructions for this request.")

evals = [e for e in ALL if e["id"] in IDS]
env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")  # absolute path when PATH has another claude first


def ensure_current_skill():
    """Create evalskills/current from the repository skill folder when it does not exist."""
    if TAG != "current" or SKILLDIR.exists():
        return
    src = REPO / "skills" / "mind-the-gap"
    shutil.copytree(src, SKILLDIR)
    plug = PLUGDIR / "skills" / "mind-the-gap"
    shutil.copytree(src, plug)
    (PLUGDIR / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (PLUGDIR / ".claude-plugin" / "plugin.json").write_text(json.dumps(
        {"name": "mind-the-gap", "version": "eval", "description": "Skill under test (eval snapshot)."}))
    print("created", SKILLDIR.parent, flush=True)


def snapshot(d):
    return {str(p.relative_to(d)): p.read_text(errors="replace")
            for p in sorted(d.rglob("*")) if p.is_file() and ".claude" not in p.parts and p.name != "CLAUDE.md"
            and not ({"__pycache__", "node_modules", ".venv", ".git", ".pytest_cache"} & set(p.parts))}


def one(job):
    model, cfg, ev, run = job
    f = OUT / TAG / model / f"eval-{ev['id']:02d}" / cfg / f"run-{run}.json"
    if f.exists():
        return
    f.parent.mkdir(parents=True, exist_ok=True)
    wd = WORKROOT / uuid.uuid4().hex[:10]
    wd.mkdir(parents=True)
    for src in ev.get("files", []):
        shutil.copytree(REPO / src, wd, dirs_exist_ok=True)
    (wd / ".claude").mkdir(exist_ok=True)  # created before always_on copy
    if cfg == "always_on":
        # In-project import: -p does not expand @imports that point outside the project.
        shutil.copytree(SKILLDIR, wd / ".claude/acs")
        (wd / "CLAUDE.md").write_text("@.claude/acs/SKILL.md\n")
    before = snapshot(wd)
    base = ["--model", model, "--setting-sources", "project", "--output-format", "stream-json", "--verbose",
            "--allowedTools", TOOLS, "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
    for pl in ev.get("plugins", []):
        base += ["--plugin-dir", str(REPO / pl)]
    sysp = []
    if cfg == "with_skill":
        base += ["--plugin-dir", str(PLUGDIR)]
        sysp.append(FORCE.format(name="mind-the-gap"))
    if ev.get("force_skill"):
        sysp.append(FORCE.format(name=ev["force_skill"]))
    if sysp:
        base += ["--append-system-prompt", " ".join(sysp)]
    sid = str(uuid.uuid4())
    prompts = [ev["prompt"]] + ev.get("turns", [])
    transcript, tools, real_model = [], [], None
    for i, prompt in enumerate(prompts):
        cmd = [CLAUDE, "-p", prompt] + base + (["--session-id", sid] if i == 0 else ["--resume", sid])
        try:
            p = subprocess.run(cmd, cwd=wd, env=env, capture_output=True, text=True, timeout=900)
        except subprocess.TimeoutExpired:
            print("TIMEOUT", f, flush=True); shutil.rmtree(wd, ignore_errors=True); return
        result = None
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
                        tools.append({"turn": i + 1, "name": c["name"], "input": c.get("input")})
            elif e.get("type") == "result":
                result = e.get("result")
                if e.get("is_error") or str(result).startswith("You've hit your"):
                    print("ERROR", f, str(result)[:120], flush=True); shutil.rmtree(wd, ignore_errors=True); return
        if result is None:
            print("NORESULT", f, p.stderr[-300:], flush=True); shutil.rmtree(wd, ignore_errors=True); return
        transcript.append({"user": prompt, "assistant": result})
    after = snapshot(wd)
    changed = {k: v for k, v in after.items() if before.get(k) != v}
    removed = [k for k in before if k not in after]
    json.dump({"eval_id": ev["id"], "config": cfg, "run": run, "model": real_model, "skill_tag": TAG,
               "prompt": ev["prompt"], "allowed_tools": TOOLS, "transcript": transcript, "tools": tools,
               "response": transcript[-1]["assistant"], "files_changed": changed, "files_removed": removed,
               "final_files": {k: v for k, v in after.items() if k in {*changed, *before}},
               "words": len(transcript[-1]["assistant"].split())},
              open(f, "w"), ensure_ascii=False, indent=1)
    shutil.rmtree(wd, ignore_errors=True)
    print("ok", f.relative_to(OUT), flush=True)


ensure_current_skill()
jobs = [(m, c, e, r) for m in MODELS for e in evals for c in CFGS for r in range(1, RUNS + 1)]
with ThreadPoolExecutor(int(os.environ.get("WORKERS", 6))) as ex:
    list(ex.map(one, jobs))
print("done", len(jobs))
