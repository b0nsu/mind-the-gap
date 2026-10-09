# Task contract

For substantial work, assemble enough of this internally to work safely. Build
it from what the request and context already say; surface only the parts that
genuinely need the user's attention. Never hand this to the user as a form.

| Part | Question it answers |
| --- | --- |
| Outcome | What should be true when the work succeeds? |
| Context | What must the AI know that it cannot reasonably infer? |
| Constraints | What must not be violated? |
| Non-goals | What is explicitly outside this task? |
| Success criteria | How will a good result be recognized? |
| Assumptions | What is being assumed, and how reversible is each? |
| Decision ownership | What may the AI decide; what still belongs to the user? |
| Verification | What evidence could demonstrate success? |

## Procedure vs judgment

Some tasks are correct only if a specific procedure is followed — operational,
regulatory, security, or contractual steps, or another active skill that
prescribes an interaction pattern. Follow those procedures exactly; they are
part of the outcome.

For judgment-heavy work with no mandated procedure, specify outcome, context,
constraints, success criteria, and verification rather than dictating each
reasoning step. A prescribed step list written by a human is often worse than
the plan the model would form from a clear success condition.
