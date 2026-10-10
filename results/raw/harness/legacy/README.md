Earlier harness generations, kept for the raw runs that cite them (results-raw-1.2.1.tar.gz).
They assume they were copied into $EVAL_SCRATCH and run from there (`cd $EVAL_SCRATCH`), use zsh,
and the runners do not clean up their working directories on errors. Not maintained.
run_behaviour2.py reads eval fixtures from the skill folder (SKILL_SRC/<files>), the layout before evals/ moved to the
repository root, so it no longer runs against this tree.
Current harness: ../run_behaviour3.py and ../grade3.py (runs and grades), ../aggregate5.py (results/behaviour-*.json),
../aggregate_heldout.py and ../aggregate_heldout2.py (held-out sets), ../sensitivity.py and ../aggregate4.py (1.2.1 raw layout),
../compare_*.py (regrades and tags), ../make_trim_candidates.py, ../run_trim.sh and ../trim_summary.py (trim ablations),
../run_eval.py and ../improve_description.py (triggering), ../scrub_asset.py (release tarballs).
