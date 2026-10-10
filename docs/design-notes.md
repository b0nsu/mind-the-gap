# Design notes: why mind-the-gap exists

Over 2026 the people who build the agent harnesses at Anthropic and OpenAI
said, in different words, the same three things. This skill is what those
three things look like from the other side of the conversation: not the
developer configuring the agent, but the person sitting in the loop.

**The bottleneck moved to the human.** Anthropic's [field guide to Fable][a1]
makes the point directly: with a model this capable, the quality of the work
is limited by how well the person can surface what they do not yet know. It
sorts those gaps into known unknowns, unknown knowns (things you would
recognise but could not write down) and unknown unknowns, and warns that you
fail in both directions, by over-specifying so the model cannot pivot and by
under-specifying so it fills gaps with generic defaults. Its remedy is a set
of patterns the *user* must know to invoke, by name: a blind-spot pass,
brainstorms and prototypes, an interview, an implementation plan. Those
patterns are good. The problem is that the person who most needs a blind-spot
pass is, by definition, the one who does not know to ask for it. §2 of this
skill moves the selection into the model: DISCOVER is the blind-spot pass for
unknown unknowns, CO-CREATE is the react-to-options move for unknown knowns,
DELEGATE is what remains once the unknowns are resolved. The user should get
the right pattern without learning the vocabulary.

**Vendors are deleting instructions, not adding them.** Anthropic removed
most of Claude Code's system prompt for Claude 5 models with no measured loss,
and replaced rules with judgment-shaped guidance ([new rules of context
engineering][a3]). OpenAI's [Astra guidance][o9] says the same about skills
and AGENTS.md: itinerary-style instructions now hinder, and strong "ask me
first" language written for an earlier model makes a well-aligned model stop
where you wanted it to continue. Both pieces hand the reader a question
rather than a rule: is this actually a decision you need to make? That
question, asked of the developer, is the ownership filter in §3, asked of
every turn. It also means a skill about collaboration cannot be a procedure.
What is here is a small set of criteria (four filters, two confirmation
mechanisms, three failure classes) and an explicit obligation to shrink: the
Maintenance section expects sections to be removed as models absorb them. The
CHANGELOG records which candidate sentences were tried and rejected; a
per-section ablation is planned for the next model generation.

**Capability is not permission.** The Astra guidance argues the model has
better judgment about what is safe; the Fable guide says you still fail in
both directions; Anthropic's [effort post][a4] observes that letting the
model work harder means it makes more assumptions on your behalf, and
recommends a loop of interview, implement, review, verify. None of these
resolves how much to hand over on a given task. `references/autonomy.md`
takes the position that autonomy should follow two properties of the task,
whether an error would be detected and whether it could be cheaply reversed,
rather than how capable the model is. §7's handback (what was verified, what
was not) is the review step of that loop made unavoidable.

The skill does not enforce this on itself. In the irreversible-deletion eval
(eval 9), run with Bash available and no approval prompt, the model deleted
the files in 9/9 runs without the skill and 0/9 with skill 1.3.0; skill
1.2.1, without the sentence that "don't ask, just do it" does not waive the
confirmation, still deleted in 10/15 and 11/15. Even on 1.3.0 an occasional
run acts first: Haiku deleted the only copy in 2 of 8 runs of held-out eval
201 and ran the publish-and-email script in 1 of 3 runs of eval 210. The
skill makes the model ask far more often; whether it can act is decided by
tool approvals, and the README says to keep them on. (An earlier version of
this paragraph cited 2 of 15 attempts stopped by the permission prompt; that
harness refused every Bash call automatically.)

One deliberate departure: the Fable guide recommends asking the model to quiz
you after a large change and merging only when you pass. §5 of this skill
refuses to test the user. It intervenes once, only when the user's own words
show a material misunderstanding, and then takes the next answer as final.
Requiring proof of understanding cannot be verified by the model and was
judged patronising in practice; the eval set (`evals/evals.json`, cases 6 and
15) exists partly to keep that line where it is.

The same guidance also says skill descriptions should be as short as possible
and that descriptions tend to over-claim when a skill applies. This skill's
description is long by that standard, because its activation condition is a
conjunction with a counter-intuitive clause (clear is not the same as safe).
Whether that length earns its place is exactly what `evals/trigger_set.json`
measures; see the trigger table in [measurements.md](measurements.md).

[a1]: https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns
[a3]: https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
[a4]: https://claude.dev/blog/spending-your-effort/
[o9]: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra

Related reading on the harness side, which this skill assumes rather than
restates: [effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents),
[building effective agents](https://www.anthropic.com/engineering/building-effective-agents),
[demystifying evals for agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents),
[harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps),
and OpenAI's [reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
and [agent evals](https://developers.openai.com/api/docs/guides/agent-evals).

