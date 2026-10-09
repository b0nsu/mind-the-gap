#!/bin/zsh
cd $EVAL_SCRATCH
ALL="1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20"
CFGS=with_skill,without_skill python3 -I run_behaviour.py claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5 3 1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17 > ao_new.log 2>&1
CFGS=always_on python3 -I run_behaviour.py claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5 3 5,6,7 > ao_a.log 2>&1
CFGS=always_on python3 -I run_behaviour2.py claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5 3 5,6,7 > ao_b.log 2>&1
python3 -I grade.py 4 > ao_grade.log 2>&1
BEH=$EVAL_SCRATCH/beh_x110 python3 -I grade.py 4 > ao_gx110.log 2>&1
BEH=$EVAL_SCRATCH/beh_x120 python3 -I grade.py 4 > ao_gx120.log 2>&1
for f in ao_new.log ao_a.log ao_b.log ao_grade.log ao_gx110.log ao_gx120.log; do echo "$f ok=$(grep -cE '^(ok|graded)' $f) bad=$(grep -cE '^(ERROR|TIMEOUT|NORESULT|FAIL)' $f)"; done
