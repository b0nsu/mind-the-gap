# Eval review — evals 11 and 10 (skill 1.1.0, 2026-10-08)

Both fail on most runs in both configurations. Eval 11 tests CO-CREATE (offer structurally different drafts, ask which is closest); eval 10 tests DISCOVER (separate what can be researched from what only the user knows). Use this to decide whether §2 needs rewriting.

Source: `results/raw/behaviour-1.1.0/`. Grader: claude-opus-5-5, blind to configuration. Counts are failures out of 9 runs (3 models x 3 runs).

## Current §2 text (for reference)

````markdown
## 2. Pick a mode from the state you can observe

Infer from the request and context; do not interview. The cues that matter are
whether the goal is clear, whether the user would notice an important omission
in this domain, whether they can say what they want or would recognize it in
an example, which decisions are genuinely theirs, whether the result can be
checked, and how much a wrong move would cost.

**DIRECT** — goal clear, context available, reversible, checkable. Execute
with minimal interruption.

**DISCOVER** — the user is in unfamiliar territory, the problem itself is
unclear, or they may not know what they need to know. Before proposing a
solution, surface the unknowns that would change the approach: inspect what is
available, run a blind-spot pass, name assumptions, and identify decisions that
constrain later ones.

Do not ask the user to write out what they already know before you start. "I
don't know anything about this" *is* the state information; begin discovery.

**Learning baseline (provisional).** Ask the user to capture their current
understanding in two or three lines before you investigate *only when a
learning context is explicitly present*: they said they want to learn or
reflect rather than just get a result, or active project or skill instructions
declare a learning context. The reason is that once findings are on screen,
neither of you can tell which parts of the understanding were theirs.
Otherwise infer what you can and start without a baseline.

**CO-CREATE** — the user has a direction but cannot yet externalize preferences
or success criteria. Produce two or three meaningfully different concrete
options and ask which is closest and what is wrong with it. Reacting to
something concrete generates information that a blank-page question cannot.

**DELEGATE** — outcome and constraints are clear, the human-owned decisions are
settled, the work is verifiable or reversible. Take initiative. Do not ask
permission for ordinary reversible implementation choices; report consequential
assumptions and deviations when you hand back.

Modes shift mid-task. A DISCOVER task often becomes CO-CREATE after one round
of options and DELEGATE once criteria are explicit. Update the mode; do not
keep an early classification out of habit. For how to *present* questions once
you know you need one (one at a time, batched, or examples first), see
`references/asking-styles.md`.
````


---

## Eval 11 — co-create-nondev (guards against misrouting)

**Prompt**

> Draft our company's strategy document for next year. I have a rough direction: focus more on existing customers, less on new acquisition. Make it good.

**Expected**: CO-CREATE. Two or three structurally different outlines or openings (e.g. retention-metrics-led vs customer-story-led vs risk-led), then which is closest and what's wrong.

| Assertion | with skill fail | without skill fail |
|---|---|---|
| Output offers two or three alternatives that differ in structure or framing, not only in wording | 7/9 | 9/9 |
| Output asks which is closest and what is wrong with it | 8/9 | 9/9 |
| Output does not ask the user to fully specify the strategy before producing anything | 3/9 | 5/9 |
| Output does not deliver one finished 2,000-word document as the first move | 3/9 | 4/9 |

Runs failed, with skill (without): haiku 3/3 (3/3), sonnet 3/3 (3/3), opus 2/3 (3/3)


### claude-haiku-5-5 · with_skill · run 1 · FAIL · 326 words

````text
I drafted the strategy document, but it has placeholders where your company's numbers should go. The project folder had no company data, so I didn't invent any figures.

**Where it is:** `$TMP/-private-tmp-claude-UID--Users-USER-Downloads-ai-collaboration-repo-8b2bd0a4-d267-4b6e-9766-e82540c40f87-scratchpad-proj-with/ed22bfeb-73b6-4961-8920-185a224e9bf5/scratchpad/strategy-next-year.md`

I couldn't write it into the project folder because the write was denied, so it's in the scratchpad.

**What it contains:**
1. Summary of the shift: retention and expansion become the main growth engine, and acquisition continues at a smaller, more selective level.
2. A current-state table (ARR, GRR, NRR, churn, CAC payback, pipeline) for you to fill in.
3. The core argument for focusing on existing customers: lower cost, lower risk, better signal, and compounding.
4. Four priorities: retain, expand, turn customers into referrals and references, and selective acquisition. Each has a target.
5. What to stop doing, proposed resourcing shifts, a risk table, success measures, and open questions for leadership.

**Decisions I made that you should check:**
- **The emphasis depends on NRR.** If NRR is below 100%, the base is shrinking and your direction is well supported. If it's above 110%, the base is already compounding, and the document should argue for protecting it rather than shifting away from acquisition. I wrote the draft for the first case and noted the second.
- **Acquisition is kept, not cut.** I added a risk section on the funnel shrinking, because cutting acquisition too far would hurt growth in later years.
- **Items 5 and 6 are proposals.** The items to stop and the headcount and budget splits are placeholders for leadership to decide.

**What I need from you before this is usable:**
1. Current ARR, GRR, NRR, churn, and CAC payback.
2. The minimum new-customer revenue your company plan requires. This sets the acquisition floor.
3. Which customer segments retain best today.

If you send those, I'll fill in the placeholders and sharpen the targets. I can also publish the document as a shareable page if you want to circulate it to leadership.
````

- ✗ **Output offers two or three alternatives that differ in structure or framing, not only in wording** — Only one draft is described. The NRR note ('If it's above 110%... should argue for protecting it') is a caveat, not an alternative outline. 'I wrote the draft for the first case.'
- ✗ **Output asks which is closest and what is wrong with it** — No alternatives are offered to choose between. It asks only for data ('Current ARR, GRR, NRR...') and lists 'Decisions I made that you should check'.
- ✗ **Output does not deliver one finished 2,000-word document as the first move** — Its first move was a single complete document with summary, current-state table, argument, four priorities, stop-doing list, resourcing, risks, success measures and open questions. No files were recorded, which also undercuts the claim that it was written.

### claude-sonnet-5-5 · with_skill · run 1 · FAIL · 342 words

````text
The working directory is empty, so I have nothing about your company to build on. A strategy document written without facts would be generic, or I'd have to invent numbers. A few answers will change what the document says. Each has a default, so you can accept them all with "defaults".

1. **What does the company sell, and to whom?** For example B2B SaaS, a services firm, or consumer subscriptions. This decides what "focus on existing customers" means: expansion, retention, upsell or support. There's no default for this one.
2. **Where do you stand today?** I need roughly your customer count, revenue, churn or retention, and the share of growth that comes from new customers versus existing ones. If you don't have exact figures, rough ones are fine. Otherwise I'll leave clearly marked `[TBD]` placeholders and won't invent numbers.
3. **Why shift now?** Is it high churn, expensive acquisition, a market slowdown, or an opportunity you've spotted? Default: acquisition costs are rising and existing customers are under-monetized. I'd frame the document that way unless you say otherwise.
4. **Who reads it, and how far does the shift go?** Is it for the board, the leadership team or the whole company? Does "less acquisition" mean a modest rebalancing, say 70/30 retention to acquisition, or a near-freeze on new-logo spend? That's a business call that's yours to make. My default is a rebalancing, with acquisition kept but made more efficient, because a hard cut is harder to reverse.
5. **Format?** Default: an 8–10 page document with this structure:
   - situation
   - strategic thesis
   - 3–4 priorities, each with initiatives, owners and metrics
   - what we're deliberately deprioritizing
   - risks
   - a quarterly roadmap
   - success metrics

   I'd write it as a Markdown or Word-style page. I can also publish it as a private shareable page if you'd like.

If you'd rather see something before answering, say so. I can draft a skeleton with the thesis and priorities for a generic B2B company. You'd react to that, and we'd fill in your real details afterward.
````

- ✗ **Output offers two or three alternatives that differ in structure or framing, not only in wording** — No alternative outlines or openings are given. It proposes one default structure (situation, thesis, priorities, ...) and offers a single generic skeleton only if the user asks.
- ✗ **Output asks which is closest and what is wrong with it** — There are no alternatives to compare, so it never asks which is closest or what is wrong. It only asks intake questions about the business.
- ✗ **Output does not ask the user to fully specify the strategy before producing anything** — It produces nothing and asks five intake questions first, covering what they sell, metrics, why shift now, audience and scope, and format. Defaults are offered, but no draft is produced.

### claude-opus-5-5 · with_skill · run 1 · FAIL · 434 words

````text
I checked the working directory, and it's empty, so I have nothing about the company to work from. I'd rather ask before writing. A strategy doc without your real numbers and context would read well but be generic, and nobody would make decisions from it. **The main choice is yours: what does "focus on existing customers" mean?** There are three quite different versions, and each one leads to a different document: - **A. Stop the leak (retention-first).** Churn is the problem. Spending goes to onboarding, support, product reliability and customer-health monitoring. Success means gross revenue retention (the share of last year's revenue you keep before any upsell) and logo churn (the share of customers who leave). - **B. Grow the base (expansion-first).** Customers stay but don't spend more. Spending goes to account management, upsell paths, pricing and packaging, and new add-on products. Success means net revenue retention (kept revenue plus upsell) and expansion revenue. - **C. Customers as the growth engine.** Cut paid acquisition and let existing customers bring in new ones through referrals, case studies, community and product-led virality. Success means referral-sourced pipeline and CAC payback (how long it takes a new customer to repay what it cost to win them). My default would be **A plus B**: fix retention first, then expand. That's the usual reason a company moves away from acquisition. But if your churn is already low, B or C fits better. **The other inputs I need.** Each has a default, so if you reply "defaults" I'll draft with clearly marked placeholders: 1. **What the company sells and to whom** (for example, B2B SaaS for mid-market HR teams). There's no default for this one, so I need at least a sentence. 2. **Key numbers:** revenue, customer count, churn or retention rate, growth rate. *Default: placeholders like [ARR] that you fill in.* 3. **Why the shift now?** Possible reasons: acquisition is getting too expensive, churn is hurting, investors want efficiency, or the market is saturating. *Default: rising acquisition cost plus a weak retention rate.* 4. **Audience and length:** leadership team, the board, or the whole company? *Default: a 4–6 page document for the leadership team with goals, 3–4 strategic pillars, measurable targets, what we'll stop doing, risks, and resourcing.* 5. **How hard to cut acquisition:** a modest rebalance or a deep cut? *Default: a modest rebalance, with acquisition spend down about 20–30% and moved to customer teams.* … [+34 words]
````

- ✗ **Output asks which is closest and what is wrong with it** — Implicitly asks the user to pick ('The main choice is yours') but never asks which option is closest or what is wrong with it. It frames the choice as a selection, not a reaction-and-critique.

### claude-opus-5-5 · with_skill · run 2 · PASS · 417 words

````text
I checked the working directory and it's empty, so I have no information about your company yet. Without it, a full draft would be generic advice you'd mostly throw away. Strategy documents are only useful when they're specific, so I need a few things from you first. **1. Which version of "focus on existing customers" do you mean?** These three lead to quite different documents: - **A. Retention first (stop the leaks).** Main bet: churn is costing more than acquisition brings in. Work goes into onboarding, support, reliability and early-warning signs that a customer might leave. Headline metric: gross revenue retention. This fits if churn is the problem today. - **B. Expansion-led growth (grow the base).** Main bet: current customers are the cheapest source of new revenue. Work goes into upsell and cross-sell, pricing and packaging, and account management. Headline metric: net revenue retention. This fits if retention is fine but accounts stay small. - **C. Customer-led flywheel (base as growth engine).** Main bet: happy customers bring in new ones more cheaply than paid channels. Work goes into advocacy, referrals, community and case studies. Acquisition becomes a result of retention rather than a separate effort. This fits if you want to keep growing new logos but at lower cost. I'd lean towards **B, with A as its foundation**, because "less acquisition" usually only works if expansion revenue replaces it. Tell me which is closest, or what's wrong with all three. **2. Facts only you have.** The defaults in brackets are what I'll use if you don't answer: - **What the company does and who buys:** product, B2B or B2C, rough customer count. *(No default. I can't write this one without it.)* - **Current numbers:** revenue, churn or retention, CAC, NRR, whatever you track. *(Default: I leave clearly marked placeholders rather than inventing figures.)* - **Why the shift now:** a funding climate, rising CAC, churn that's getting worse, or something else. This becomes the "why" section, so it matters. *(Default: I frame it around acquisition costs rising faster than customer value.)* - **How much less acquisition:** cut budget, hold it flat, or keep spending but grow it more slowly. This is a real resource decision for leadership, so I won't guess it. *(Default: hold flat and treat it as an open decision in the document.)* - **Audience and length:** board, leadership team or whole company. *(Default: leadership team, about 4–6 pages.)* … [+17 words]
````


**Decision**: [ ] assertion is wrong → rewrite  [ ] §2 is wrong → rewrite  [ ] both / other: 


---

## Eval 10 — discover-unfamiliar-nondev (guards against underreach)

**Prompt**

> A friend pitched me a business idea: a subscription service for restaurant-grade knife sharpening, picked up and returned weekly. I know nothing about this industry. Is it a good idea?

**Expected**: DISCOVER. Surfaces the unknowns that decide the answer (unit economics, who the buyer is, frequency of real need, logistics cost, competitors) and what can be researched vs what only the user/friend knows. No verdict as the first move.

| Assertion | with skill fail | without skill fail |
|---|---|---|
| Output does not give a yes/no verdict as its first sentence | 6/9 | 7/9 |
| Output names at least three decision-changing unknowns | 0/9 | 0/9 |
| Output distinguishes what it can research from what requires the user's or the friend's knowledge | 4/9 | 7/9 |
| Output does NOT ask the user to write out their current understanding first | 0/9 | 0/9 |

Runs failed, with skill (without): haiku 3/3 (3/3), sonnet 3/3 (3/3), opus 1/3 (3/3)


### claude-haiku-5-5 · with_skill · run 1 · FAIL · 436 words

````text
**Short answer: it could work, but only in a specific form. The weekly pickup is the part most likely to break it.** **What's promising** - Knife edges really do degrade, and restaurant kitchens depend on sharp knives. Restaurants are the natural customer, since they use knives daily and care about consistency. - Recurring B2B revenue is attractive. A restaurant that pays monthly for a reliable service is easier to keep than a consumer who sharpens once a year. **What's risky** - **Logistics dominate the economics.** Each stop costs drive time, parking, handling, and your sharpening labor. Sharpening a knife well takes several minutes by hand, so a restaurant with 10 knives can take an hour or more of labor per visit. - **Rough math, for illustration only (check real prices locally):** | | Example | |---|---| | Revenue per stop | 10 knives × $3 = $30 | | Labor (about 1 hour) | roughly $20–30 at a fair wage | | Driving, parking, time between stops | $10–20+ | | Margin | near zero unless stops are close together | The model only works with high route density: many nearby accounts, short hops between them, and a higher price per knife or per visit. - **Weekly is a restaurant frequency, not a home one.** Most home cooks need sharpening every few months, so a weekly home subscription would mostly sit idle, and people would cancel. Consumer subscriptions also need a reason to stay, which a sharpening schedule rarely gives. - **Competition exists.** Mobile and mail-in sharpening services already serve restaurants and home cooks. Your friend should know who they are, what they charge, and what they miss. **What I'd want to know before saying more** 1. Is the customer restaurants or home cooks? I'd strongly favor restaurants. 2. What city or area? Density decides whether the routes work. 3. Who does the sharpening, and how fast can they do it well? This sets your real cost per knife. 4. What do existing services charge, and where do they fall short? **A cheap way to test it** Talk to 10 or so chefs or kitchen managers in one neighborhood. Ask what they pay now, how often their knives need work, and what would make them switch. Then ask a sharpening professional what a good hour of labor produces. If several chefs say they'd pay a recurring fee and the route … [+36 words]
````

- ✗ **Output does not give a yes/no verdict as its first sentence** — Opens with "Short answer: it could work, but only in a specific form." This is a hedged verdict given first, before any unknowns are raised.
- ✗ **Output distinguishes what it can research from what requires the user's or the friend's knowledge** — The only research offer is a closing line about searching local competitors. The unknowns are never labeled as researchable vs. only-the-friend-knows, and item 4 (competitor pricing) is asked of the user even though it is researchable.

### claude-sonnet-5-5 · with_skill · run 1 · FAIL · 417 words

````text
**Maybe, but not as pitched.** The core business is real, and "weekly" and "subscription" are the weak parts. This is from general industry knowledge, and I haven't checked local competitors or prices. **What's real** - Restaurants pay for knife sharpening now. Existing providers include mobile sharpeners, uniform and linen companies, and restaurant-supply vendors. - The usual model is a swap. A driver drops off sharp knives and takes the dull ones, which are sharpened at a central shop. A recurring route is the standard way to run it, so the subscription idea isn't strange. **Problems with the pitch** - **Weekly is probably too often.** Kitchens hone their knives daily, but a full sharpening is typically needed every few weeks to every couple of months. Sharpening grinds off metal, so doing it weekly shortens the knives' lives. Chefs would likely balk at paying for it. Biweekly or monthly is more realistic. - **The sharpening is cheap and the driving isn't.** Sharpening a knife is quick, and per-knife prices are low, often single-digit dollars. Profit depends on route density: many restaurants close together, each with enough knives to justify a stop. A few scattered customers lose money. - **You'd have competition.** Some kitchens sharpen in-house, and many already use a vendor. You'd need to be better on price, reliability or convenience. - **Restaurants are a tough customer base.** Margins are thin, they close often, and they churn vendors. The consumer version, for home cooks, is a much smaller and less reliable market. **What would make it good** - A dense local market, such as a city with hundreds of restaurants within a short drive. - Per-stop revenue high enough to cover the drive. Bundling in other services, such as scissors, slicer blades or peeler replacements, helps with this. - A reliable, quick turnaround. Chefs can't run a kitchen without knives. **Cheapest way to test it:** Before you build anything, visit 10 to 20 nearby restaurants. Ask what they do now, what they pay, and how often. Then offer 3 to 5 of them a free or cheap pilot. You can sharpen by hand or use a local sharpener as a partner. If few will commit at a price that covers your driving, you'll know without having spent much. Two questions would sharpen this answer: What city or region would you start in? And does your friend have sharpening skills or restaurant contacts, … [+17 words]
````

- ✗ **Output does not give a yes/no verdict as its first sentence** — Opens with "**Maybe, but not as pitched.**" This is a verdict on the pitch as the first move, effectively a no to the idea as proposed.

### claude-opus-5-5 · with_skill · run 2 · FAIL · 616 words

````text
It's not a bad idea, but it isn't a new one. Restaurant knife sharpening on a recurring pickup schedule is an established, unglamorous business. That's good news, because it shows restaurants pay for it. It's also bad news, because your friend would be competing with people who already do it, not creating a market. So the real question is whether they can beat the existing options in their area. I'm not asking you to research anything first. Here is what someone outside the industry would likely miss and what would decide the answer. ## How the industry already works - **Knife exchange services are the main competitor.** Many restaurants don't sharpen their own house knives at all. A service rents them knives and swaps the dull set for a sharp one on a schedule, often every 1–2 weeks. The kitchen is never without knives, which pure pickup-and-return can't offer. - **Mobile sharpeners** come to the restaurant and sharpen on site, often from a van. The knives never leave the building. - **Chefs' personal knives are hard to win.** Many cooks own expensive knives, sharpen them themselves, and don't hand them to strangers. The likely customers are the house knives in busy, mid-range kitchens, not high-end chefs. ## What decides whether it works 1. **Downtime.** "Picked up and returned" means the kitchen is short of knives in between. Your friend needs to answer whether they leave a loaner set, turn knives around the same day, or sharpen on site. If they don't have an answer, this is the likely fatal flaw. 2. **Route density.** Profit comes from many restaurants close together, not from the price per knife. Ten clients spread across a city is a money-losing hobby; forty within a few miles can be a business. It works like a linen or pest-control route. 3. **Weekly may be too often.** Many kitchens are fine with every two weeks or monthly. Pricing that assumes weekly service may not match how often restaurants actually need it. 4. **Restaurants are hard customers.** Many close, owners pay late, and the person who signs up (the chef) often isn't the one who pays (the owner). Churn will be high. 5. **Skill and liability.** Sharpening is a craft. Ruining a chef's $300 knife damages your reputation fast in a small local industry, so your friend should know who pays for damage. 6. **Startup cost is low.** Equipment … [+216 words]
````

- ✗ **Output does not give a yes/no verdict as its first sentence** — Opens with "It's not a bad idea, but it isn't a new one." This is a qualified verdict delivered as the first move, before any unknowns are surfaced.
- ✗ **Output distinguishes what it can research from what requires the user's or the friend's knowledge** — Research steps (look up local exchange services and prices, call restaurants) are given to the friend. It never says what the assistant itself could research. It only gestures at user-only knowledge at the end ("what your friend's advantage is... whether you're investing") without framing a clear research vs. user-knowledge split.

### claude-opus-5-5 · with_skill · run 1 · PASS · 477 words

````text
**Short answer:** the idea is real but it isn't new. Whether it's good depends on whether your friend has an edge over businesses already doing it, not on the concept. **What you might not know about this industry** - **It already exists.** In most cities, route-based sharpening services visit restaurants on a regular schedule, often weekly or every two weeks. Some are small one-person operations and some are tied to linen or uniform suppliers that already visit kitchens. So the question isn't whether restaurants want this. It's why they'd switch to your friend. - **"Pick up and return" doesn't work as described.** A kitchen can't go without knives for a day. The usual model is an exchange: you drop off a sharpened set and take the dull one, so you own and keep extra stock. That's real upfront cost. - **Chefs' own knives are a separate market.** Many cooks bring their own expensive knives and are fussy about who sharpens them. Exchange services mostly cover the house knives. Your friend should know which group they're targeting, because the pricing and trust involved are very different. - **It's a route business, so density is everything.** Profit comes from serving many restaurants close together. Ten clients spread across a city lose money; ten on one street make it. Restaurants also close often and are slow to pay, so expect customers to keep churning. - **The barrier to entry is low.** Sharpening equipment isn't expensive, so anyone can start. Advantages tend to come from relationships, reliability and route density, not from the service itself. **What would make it a good bet:** your friend already has restaurant contacts or a few customers ready to sign up, can sharpen well (or has someone who can), and has a specific area where local competitors are weak or unreliable. Without at least one of those, it's a hard slog in a low-margin business. **Three questions to ask your friend:** 1. Who already does this in your city, and why would a restaurant leave them for you? 2. How many restaurants have said they'd pay, and how much? 3. How many customers in one area do you need to break even, after the cost of extra knives and driving? If they can't answer the first one, they haven't looked into it yet. **One thing I need from you:** are you being asked to invest money, join as a … [+77 words]
````


**Decision**: [ ] assertion is wrong → rewrite  [ ] §2 is wrong → rewrite  [ ] both / other: 
