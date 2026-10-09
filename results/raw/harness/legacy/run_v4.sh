#!/bin/zsh
cd $EVAL_SCRATCH
M=claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5
for T in v131 v120 v130; do OUT=$EVAL_SCRATCH/beh4 python3 -I run_behaviour3.py $M 3 all always_on $T > v4_$T.log 2>&1; done
for T in v131 v120 v130; do OUT=$EVAL_SCRATCH/beh4 python3 -I run_behaviour3.py $M 5 9,13,15,17 always_on $T > v4_${T}x5.log 2>&1; done
OUT=$EVAL_SCRATCH/beh4 python3 -I run_behaviour3.py $M 5 9,13,15,17 without_skill v120 > v4_wo_x5.log 2>&1
python3 -I grade3.py $EVAL_SCRATCH/beh4 4 > v4_grade.log 2>&1
python3 -I grade3.py $EVAL_SCRATCH/beh4 4 >> v4_grade.log 2>&1
echo "runs=$(find beh4 -name 'run-?.json' ! -name '*.grade*' | wc -l) graded=$(find beh4 -name '*.grade.json' | wc -l) errors=$(grep -hcE '^(ERROR|TIMEOUT|NORESULT|FAIL)' v4_*.log | paste -sd+ - | bc)"
