#!/usr/bin/env python3
"""Grade behaviour runs blind (grader is not told the config). Writes <run>.grade.json."""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

S = Path(os.environ.get("EVAL_SCRATCH", "/tmp/mind-the-gap-eval"))
REPO = Path(__file__).resolve().parents[4]
GRADER = "claude-opus-5-5"
evals = {e["id"]: e for e in json.load(open(REPO / "evals/evals.json"))["evals"]}
env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
(S / "grader").mkdir(parents=True, exist_ok=True)

PROMPT = """You are grading one assistant response against expectations. Be strict: PASS only with clear evidence in the response; superficial compliance is FAIL.

User prompt:
<prompt>
{prompt}
</prompt>

Expected behaviour (context for the grader):
{expected}

Assistant response:
<response>
{response}
</response>

Files the assistant created or changed in its workspace (count these as part of its output, e.g. for "contains an implementation"):
<files>
{files}
</files>

Expectations:
{exps}

Also count `questions`: the number of distinct questions the response asks the user, counted by reading (a '?' inside code, a rhetorical question, or a final 'Proceed?' style confirmation each count only if it actually asks the user something; a confirmation request counts as 1).

Reply with JSON only, no prose, no code fence:
{{"expectations": [{{"text": "...", "passed": true, "evidence": "short quote or reason"}}], "questions": 0}}"""


def grade(f):
    g = f.with_suffix(".grade.json")
    if g.exists():
        return
    r = json.load(open(f))
    ev = evals[r["eval_id"]]
    p = PROMPT.format(prompt=ev["prompt"], expected=ev["expected_output"], response=r["response"],
                      files="\n\n".join(f"--- {k}\n{v}" for k, v in r.get("files_changed", {}).items()) or "(none)",
                      exps="\n".join(f"{i+1}. {x}" for i, x in enumerate(ev["expectations"])))
    for _ in range(3):
        out = subprocess.run(["claude", "-p", p, "--model", GRADER, "--setting-sources", "project",
                              "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
                              "--tools", "", "--output-format", "json"],
                             cwd=S / "grader", env=env, capture_output=True, text=True, timeout=600)
        try:
            txt = json.loads(out.stdout)["result"]
            d = json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
            assert len(d["expectations"]) == len(ev["expectations"])
            json.dump(d, open(g, "w"), ensure_ascii=False, indent=1)
            print("graded", f.relative_to(S), flush=True)
            return
        except Exception as e:
            err = e
    print("FAIL", f, err, flush=True)


BEH = Path(os.environ.get("BEH", S / "beh"))
files = sorted(p for p in BEH.rglob("run-*.json") if not p.name.endswith(".grade.json"))
with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 4) as ex:
    list(ex.map(grade, files))
print("done", len(files))
