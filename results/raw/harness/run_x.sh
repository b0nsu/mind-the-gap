#!/bin/zsh
cd $EVAL_SCRATCH
SK="1,2,3,4,5,6,7,10,11,13,14,15,16,17"
ONLY_WITH=1 SKILL_SRC=$EVAL_SCRATCH/skill_110 OUT=$EVAL_SCRATCH/beh_x110 PROJ=proj_x110 python3 -I run_behaviour.py claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5 5 $SK > x110.log 2>&1
ONLY_WITH=1 SKILL_SRC=$EVAL_SCRATCH/skill_120 OUT=$EVAL_SCRATCH/beh_x120 PROJ=proj_x120 python3 -I run_behaviour.py claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5 5 $SK > x120.log 2>&1
BEH=$EVAL_SCRATCH/beh_x110 python3 -I grade.py 4 > gx110.log 2>&1
BEH=$EVAL_SCRATCH/beh_x120 python3 -I grade.py 4 > gx120.log 2>&1
for f in x110.log x120.log gx110.log gx120.log; do echo "$f ok=$(grep -cE '^(ok|graded)' $f) bad=$(grep -cE '^(ERROR|TIMEOUT|NORESULT|FAIL)' $f)"; done
