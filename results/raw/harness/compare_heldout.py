"""Compare first-run grades (eval set 1.0.0) with the 1.0.1 regrade of evals 101, 107, 108,
and recompute the pooled held-out pass rate per model/config with the regrade substituted."""
import json, glob, sys, collections
old, new = sys.argv[1], sys.argv[2]
M = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
changed = collections.Counter(); flips = []
newg = {}
for f in sorted(glob.glob(f'{new}/*/eval-*/*/run-?.grade.json')):
    rel = f[len(new) + 1:]
    newg[rel] = json.load(open(f))
    og = json.load(open(f'{old}/{rel}'))
    for i, (a, b) in enumerate(zip(og['expectations'], newg[rel]['expectations']), 1):
        if a['passed'] != b['passed']:
            k = f"{'pass->fail' if a['passed'] else 'fail->pass'}"
            changed[k] += 1
            flips.append((rel, i, k, b['evidence'][:140]))
print(f"regraded runs: {len(newg)}; verdicts changed: {sum(changed.values())} {dict(changed)}")
for r in flips: print("  ", r)

def rates(sub):
    out = {}
    for m in M:
        for cfg in ("without_skill", "always_on"):
            p = t = 0
            for f in sorted(glob.glob(f'{old}/{m}/eval-*/{cfg}/run-?.grade.json')):
                rel = f[len(old) + 1:]
                g = newg[rel] if (sub and rel in newg) else json.load(open(f))
                for e in g['expectations']:
                    t += 1; p += e['passed']
            out[(m, cfg)] = (p, t)
    return out

a, b = rates(False), rates(True)
print("\npooled pass rate, all 16 evals x 3 runs: 1.0.0 grades -> with 1.0.1 regrade of 101/107/108")
for m in M:
    w0, w1 = a[(m, 'without_skill')], b[(m, 'without_skill')]
    s0, s1 = a[(m, 'always_on')], b[(m, 'always_on')]
    r = lambda x: x[0] / x[1]
    print(f"  {m:18} without {r(w0):.3f} -> {r(w1):.3f}   always_on {r(s0):.3f} -> {r(s1):.3f}   gain {100*(r(s0)-r(w0)):+.1f} -> {100*(r(s1)-r(w1)):+.1f} pp  (n={w0[1]})")
