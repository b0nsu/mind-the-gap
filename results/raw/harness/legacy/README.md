Earlier harness generations, kept for the raw runs that cite them (results-raw-1.2.1.tar.gz).
They assume they were copied into $EVAL_SCRATCH and run from there (`cd $EVAL_SCRATCH`), use zsh,
and the runners do not clean up their working directories on errors. Not maintained.
Current harness: ../run_behaviour3.py, ../grade3.py, ../aggregate4.py, ../sensitivity.py, ../run_eval.py.
