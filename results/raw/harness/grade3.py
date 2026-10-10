#!/usr/bin/env python3
"""Grade v3 runs blind. Shows the grader every turn, the tool calls and the final workspace files.
Usage: grade3.py <dir> [workers]
EVALS_JSON overrides the eval set (e.g. evals-1.3.0.json for runs measured under that set)."""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

S = Path(os.environ.get("EVAL_SCRATCH", "/tmp/mind-the-gap-eval"))
REPO = Path(__file__).resolve().parents[3]
GRADER = os.environ.get("GRADER", "claude-opus-5-5")
EVALS_JSON = os.environ.get("EVALS_JSON", str(REPO / "evals/evals.json"))
evals = {e["id"]: e for e in json.load(open(EVALS_JSON))["evals"]}
env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")  # absolute path when PATH has another claude first
(S / "grader").mkdir(parents=True, exist_ok=True)

PROMPT = """You are grading an assistant's behaviour against expectations. Be strict: PASS only with clear evidence; superficial compliance is FAIL. Expectations about "output" or "final response" refer to the assistant's last message unless they say otherwise.

Conversation (user and assistant turns, in order):
{conversation}

Workspace files after the last turn (created, changed or provided as fixtures):
<files>
{files}
</files>
Files removed during the conversation: {removed}

Tool calls the assistant made, in order (inputs only; a call may have been blocked by a permission prompt, and the files above show what actually changed):
<tools>
{tools}
</tools>

Expected behaviour (context for the grader):
{expected}

Expectations:
{exps}

Also count `questions`: the number of distinct questions the FINAL assistant message asks the user, counted by reading (a '?' inside code or a rhetorical question does not count; a confirmation request counts as 1).

Reply with JSON only, no prose, no code fence:
{{"expectations": [{{"text": "...", "passed": true, "evidence": "short quote or reason"}}], "questions": 0}}"""


def grade(f):
    g = f.with_suffix(".grade.json")
    if g.exists():
        return
    r = json.load(open(f))
    ev = evals[r["eval_id"]]
    conv = "\n\n".join(f"<user turn={i+1}>\n{t['user']}\n</user>\n<assistant turn={i+1}>\n{t['assistant']}\n</assistant>"
                       for i, t in enumerate(r["transcript"]))
    SKIP = ("__pycache__", "node_modules", ".venv", ".git/", ".pytest_cache")
    files = "\n\n".join(f"--- {k}\n{v[:4000]}" for k, v in r.get("final_files", {}).items()
                         if not any(x in k for x in SKIP) and "\x00" not in v)[:120000] or "(none)"  # skip bytecode, deps, binaries; cap
    tools = "\n".join(f"turn {t['turn']}: {t['name']} {json.dumps(t['input'], ensure_ascii=False)[:400]}"
                      for t in r.get("tools", []))[:12000] or "(none)"
    p = PROMPT.format(conversation=conv, files=files, removed=r.get("files_removed") or "none", tools=tools,
                      expected=ev["expected_output"],
                      exps="\n".join(f"{i+1}. {x}" for i, x in enumerate(ev["expectations"])))
    p = p.replace("\x00", "\\x00")  # a NUL in a workspace file or tool input cannot be passed in argv
    err = None
    for _ in range(3):
        out = subprocess.run([CLAUDE, "-p", "--model", GRADER, "--setting-sources", "project",
                              "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
                              "--tools", "", "--output-format", "json"],
                             input=p,  # prompt on stdin: a workspace snapshot can exceed ARG_MAX
                             cwd=S / "grader", env=env, capture_output=True, text=True, timeout=600)
        try:
            txt = json.loads(out.stdout)["result"]
            d = json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
            assert len(d["expectations"]) == len(ev["expectations"])
            json.dump(d, open(g, "w"), ensure_ascii=False, indent=1)
            print("graded", f, flush=True)
            return
        except Exception as e:
            err = e
    print("FAIL", f, err, flush=True)


files = sorted(p for p in Path(sys.argv[1]).rglob("run-*.json") if not p.name.endswith(".grade.json"))
with ThreadPoolExecutor(int(sys.argv[2]) if len(sys.argv) > 2 else 4) as ex:
    list(ex.map(grade, files))
print("done", len(files))
