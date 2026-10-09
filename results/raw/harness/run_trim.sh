#!/bin/zsh
# docs/proposed-trim-ablations.md: always on, eval set 1.5.0.
# 3 runs on all evals per tag, then 5 runs on the evals each change targets.
H=${0:A:h}
: ${EVAL_SCRATCH:=/tmp/mind-the-gap-eval}
export EVAL_SCRATCH
M=claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5
OUT=$EVAL_SCRATCH/beh-trim
python3 -I $H/make_trim_candidates.py || exit 1
cd $EVAL_SCRATCH
for T in v121 t1-maint t2-s7 t3-s5conf; do
  OUT=$OUT python3 -I $H/run_behaviour3.py $M 3 all always_on $T > trim_$T.log 2>&1
  OUT=$OUT python3 -I $H/run_behaviour3.py $M 5 9,12,14,24,27 always_on $T > trim_${T}x5.log 2>&1
done
python3 -I $H/grade3.py $OUT 4 > trim_grade.log 2>&1
python3 -I $H/grade3.py $OUT 4 >> trim_grade.log 2>&1
echo "runs=$(find $OUT -name 'run-?.json' | wc -l) graded=$(find $OUT -name '*.grade.json' | wc -l) errors=$(grep -hcE '^(ERROR|TIMEOUT|NORESULT|FAIL)' trim_*.log | paste -sd+ - | bc)"
