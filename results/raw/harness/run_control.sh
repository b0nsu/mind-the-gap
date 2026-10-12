#!/bin/bash
# docs/proposed-minimal-control.md: v131 (shipped body) vs t4-minimal (~60-word control), always on,
# both held-out sets, 3 runs, three models. Run inside the harness container (Bash is auto-approved).
set -u
H=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$H/../../.." && pwd)
: ${EVAL_SCRATCH:=/tmp/mind-the-gap-eval}
export EVAL_SCRATCH
M=${MODELS:-claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5}
RUNS=${RUNS:-3}
python3 -I "$H/make_control_candidates.py" || exit 1
mkdir -p "$EVAL_SCRATCH"; cd "$EVAL_SCRATCH"
for SET in $(echo "${SETS:-heldout heldout2}" | tr , " "); do
  if [ "$SET" = tuning ]; then export EVALS_JSON="$REPO/evals/evals.json"; else export EVALS_JSON="$REPO/evals/evals_${SET}.json"; fi
  OUT="$EVAL_SCRATCH/control-$SET"; export OUT
  for T in $(echo "${TAGS:-v131 t4-minimal}" | tr , " "); do
    python3 -I "$H/run_behaviour3.py" "$M" "$RUNS" all always_on "$T" > "control_${SET}_${T}.log" 2>&1
  done
  python3 -I "$H/grade3.py" "$OUT" 4 > "control_${SET}_grade.log" 2>&1
  python3 -I "$H/grade3.py" "$OUT" 4 >> "control_${SET}_grade.log" 2>&1   # second pass fills grades that errored
done
echo "runs=$(find "$EVAL_SCRATCH"/control-* -name 'run-?.json' | wc -l) graded=$(find "$EVAL_SCRATCH"/control-* -name '*.grade.json' | wc -l) errors=$(grep -hcE '^(ERROR|TIMEOUT|NORESULT|FAIL)' control_*.log | paste -sd+ - | bc)"
