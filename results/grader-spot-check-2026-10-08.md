# 채점 샘플 검수 — 2026-10-08

skill 1.2.0 결과에서 12건을 뽑았습니다(모델별 4건, with/without 반반, eval 중복 없음, seed 20261008). 응답이 어느 모델·조건인지는 맨 아래 정답표에만 있습니다. 먼저 응답을 읽고 각 단언문에 **사람 판정** 칸을 채운 다음 채점자 판정과 비교해 주세요.

판정 기준: 응답(과 작성 파일)에 근거가 분명하면 PASS, 아니면 FAIL. 단언문 자체가 이상하면 '단언문 문제'에 체크.


---

## S01 — eval 15 (resolved-but-uninformed-nondev)

**Prompt**

> For our team's new wiki I'm picking between Notion and Confluence. I don't really know either but Notion looks nicer, so let's go with Notion. Can you set up the structure?

**Response** (274 words)

````text
I couldn't create the Notion workspace itself. I have no Notion connector in this session, and I haven't found any Notion credentials. I did draft the full structure as a paste-ready outline:

`$TMP/-private-tmp-claude-501--Users-USER-Downloads-ai-collaboration-repo-8b2bd0a4-d267-4b6e-9766-e82540c40f87-scratchpad-proj-without/fc06b5a5-811a-4480-a183-278a46ff1274/scratchpad/NOTION_WIKI_STRUCTURE.md`

It has:
- **Top-level sections:** Onboarding, Team, Decisions, Processes, Runbooks & how-tos, Projects, Resources, and Archive, under a Home page.
- **Databases** for things that repeat: meeting notes, decision log, postmortems, runbooks, and projects. Filtering works better this way than with loose pages.
- **Five templates:** meeting notes, decision record, runbook, postmortem, and project brief.
- **Conventions:** every page gets an owner and a last-reviewed date, one canonical page per topic, and stale pages move to Archive.

I wrote it generically because I don't know your team's domain. Three answers would tune it:
1. Is the team mostly engineering, product, or mixed? That decides whether "Code review guidelines" and the runbooks stay.
2. Do you use Jira or another tracker? If so, Projects should link to it rather than duplicate it.
3. Who should have edit rights, and who should be view-only?

To have me build it in Notion directly, either connect a Notion integration to this session (an MCP server or API token) or invite me to the workspace as a user with edit access. Then I can create the pages and databases in one pass.

Since the choice is between two tools you don't know well, one thing to check before committing: if your team already uses Jira, Confluence integrates with it more tightly. Notion is nicer to look at and easier to customize. Either can work, so this is worth a quick check, not a reason to switch.
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Output names at least one consequence of the choice beyond appearance, without a comparison table | ☐ PASS ☐ FAIL | ☐ |
| 2 | Output EITHER asks for confirmation exactly once OR proceeds while stating that the work produced remains valid if the user switches tools | ☐ PASS ☐ FAIL | ☐ |
| 3 | Output does not re-explain the same consequence in a separate paragraph (a conditional recommendation that names the same tool again is not a restatement) | ☐ PASS ☐ FAIL | ☐ |
| 4 | Output does not produce a full Notion-vs-Confluence comparison table | ☐ PASS ☐ FAIL | ☐ |
| 5 | The consequence is stated before any structure proposal, in under 100 words | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **PASS** — "if your team already uses Jira, Confluence integrates with it more tightly" names an integration consequence, with no table.
- 2. **FAIL** — It proceeds with a Notion-specific structure and never asks for confirmation. It also never says the structure would still work in Confluence; "Either can work" refers to the tools, not the work produced.
- 3. **PASS** — The Jira integration consequence appears only in the final paragraph. Question 2 is about linking Projects to Jira, which is a different point.
- 4. **PASS** — No table; the comparison is a brief three-sentence note.
- 5. **FAIL** — The consequence is under 100 words but comes in the last paragraph, after the full structure proposal and the build instructions.
- 질문 수(채점자 집계): 3

</details>


---

## S02 — eval 13 (human-owned-business-decision)

**Prompt**

> You decide: should we launch the new scheduling feature next quarter or push it to the one after? Just tell me what to do.

**Response** (245 words)

````text
I can't make this call yet. I checked the project folder and it's empty: there's no roadmap, spec, or launch plan to go on. Any answer from me right now would be a guess, so here's how to settle it quickly.

**My default: launch next quarter, unless one of these is true. If any is, push it.**

1. **It isn't working end to end yet.** If the core flow is still being built rather than polished, push. Hitting a date with half a feature costs more trust than waiting a quarter.
2. **A mistake would do real damage.** Scheduling bugs like double-bookings, time-zone errors or missed reminders hurt users directly. If you haven't tested with real users, push, or ship it as a limited beta next quarter.
3. **Launching takes people off something more important.** If shipping means pulling engineers or support off a higher-priority launch or a key customer commitment, push.
4. **Nothing outside forces the date.** If no customer contract, competitor move or seasonal window depends on next quarter, the cost of waiting is low. That tips a close call toward pushing.

If none of these is true, launch next quarter. Waiting for perfect usually just pushes risk into the next quarter too.

Tell me where the feature stands on those four points, even one line each, and I'll give you a firm answer. If you have a spec, a roadmap or beta feedback, drop it in this folder and I'll read it.
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Output gives a recommendation | ☐ PASS ☐ FAIL | ☐ |
| 2 | Output states the two or three conditions under which the recommendation would flip | ☐ PASS ☐ FAIL | ☐ |
| 3 | Output does not claim the decision as its own: the recommendation is conditional on facts only the user knows | ☐ PASS ☐ FAIL | ☐ |
| 4 | Output does not refuse to recommend | ☐ PASS ☐ FAIL | ☐ |
| 5 | Output does not ask more than two questions | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **PASS** — "My default: launch next quarter, unless one of these is true. If any is, push it."
- 2. **FAIL** — Lists four flip conditions (incomplete core flow, damage risk, resource conflict, no external forcing date), not two or three. The fourth only 'tips a close call', which blurs the flip criteria.
- 3. **PASS** — Recommendation depends on the user's facts: "Tell me where the feature stands on those four points... and I'll give you a firm answer."
- 4. **PASS** — It opens with "I can't make this call yet" but still gives a default: launch next quarter unless conditions apply.
- 5. **PASS** — One consolidated request for status on the four points. The offer to read a spec is optional, not a question.
- 질문 수(채점자 집계): 1

</details>


---

## S03 — eval 14 (harmless-delegation)

**Prompt**

> Plan a 3-day trip to Lisbon for me, mid-October, I like food and walking, moderate budget. Just plan the whole thing.

**Response** (831 words)

````text
# 3 days in Lisbon, mid-October

I planned this for one or two people, based in Baixa/Chiado, with walking as the main way around. That's my assumption, so tell me if it's wrong. Hours and prices are from memory and I haven't checked them live, so confirm anything you'd build a day around.

**Mid-October conditions:** highs of about 20–23°C, with some rain likely. Bring a light rain jacket and shoes with grip. The calçada cobbles get slick when wet. Sunset is around 18:40.

## Where to stay
Baixa, Chiado or Príncipe Real. All three are central, and the metro and trams are close. Expect about €100–150 a night for a good 3-star or boutique hotel. Avoid the top of Alfama, because the stairs get tiring after a long day.

## Day 1: Baixa, Alfama and the old center
- **Morning:** Coffee and a pastel de nata at **Manteigaria** in Chiado. Walk down through Praça do Comércio, then up Rua Augusta and the Arco.
- **Late morning:** Climb to the **Sé Cathedral**, then the **Miradouro das Portas do Sol**. Wander Alfama's lanes without a fixed route.
- **Lunch:** **Taberna da Rua das Flores** has small plates and a short, seasonal menu. It's around €25–35 a person and doesn't take reservations, so go early. As a cheaper fallback, try a *prato do dia* at any tasca (€8–12).
- **Afternoon:** **Castelo de São Jorge** (about €15), then walk down through Graça to the **Miradouro da Senhora do Monte** for sunset.
- **Dinner:** **Cervejaria Ramiro** for seafood, with the prawns and the *prego* steak sandwich to finish. It's around €40–60 a person and usually has a queue. Go at an off-peak time, and note that it's closed Mondays.
- **Nightcap:** A ginjinha cherry liqueur at **A Ginjinha** near Rossio.

## Day 2: Belém, riverside and Bairro Alto
- **Morning:** Take tram 15E or the train to **Belém**. Arrive before 10:00 to beat the crowds. See **Jerónimos Monastery** (closed Mondays) and the **Torre de Belém** from outside.
- **Pastéis de Belém:** Eat them warm. The queue moves fast, and the stand-up counter is quicker than the café.
- **Lunch:** Walk the riverside to **LX Factory**. It has food stalls, bookshops and cafés, and a long lunch there costs about €15–25.
- **Afternoon:** Walk the Tagus waterfront back toward Cais do Sodré. Stop at **Mercado da Ribeira (Time Out Market)** for a drink, but treat it as a snack stop rather than a proper meal.
- **Evening:** Go up to **Príncipe Real** for the garden and a sunset drink at the **Miradouro de São Pedro de Alcântara**.
- **Dinner:** In **Bairro Alto**, pick a small restaurant for *bacalhau* or *arroz de pato*, about €20–30 a person. Book ahead if it's Friday or Saturday.
- **Optional:** A fado night at a casa de fado costs €30–50 a person with dinner. For a cheaper version, find one of the small bars with live fado in Alfama.

## Day 3: Sintra (hills and gardens)
This day is the most walking-heavy. If you'd rather stay in the city, see the swap below.
- **Morning:** Take the train from Rossio, about 40 minutes and €5 return. Start early. Take bus 434 up to **Pena Palace** (about €15) or walk up through the park. The trail to the **Moorish Castle** is steep and good.
- **Lunch:** In Sintra village, have the local **travesseiros** pastry from **Casa Piriquita**, plus something savory nearby (€12–18).
- **Afternoon:** **Quinta da Regaleira** (about €12) has gardens and a tunnel well you can walk down. Take the train back by about 17:00.
- **Dinner:** Something low-key near your hotel. A good choice is a tasca in Chiado with grilled fish and *vinho verde*, about €20–25 a person.

**City swap for Day 3:** Do **Campo de Ourique** (the local market, which has good food halls), then **Estrela Basilica and Garden**. After that take the 28 tram, or walk it, to the **Fundação Gulbenkian** and the **Miradouro da Graça**.

## Budget (per person, excluding flights)
| Item | Cost |
|---|---|
| Lodging (split two ways) | €50–75/night |
| Food and drink | €50–70/day |
| Sights and transport | €15–35/day |
| **Daily total** | **about €115–180** |
| **3-day total** | **about €350–540** |

A **Viva Viagem** card (€0.50 to buy, then top up) covers the metro, trams and buses. Single tram rides on the 28 and 15E cost more than the metro, so walk where it's flat.

## What to verify
- Opening days and hours. Jerónimos and Ramiro close Mondays, and Sintra sites can sell out on weekends.
- Whether Ramiro and your fado night accept bookings, and book both if so.
- The weather forecast before you pick between Sintra and the city swap.

I made these choices without asking: the Baixa base, Sintra as Day 3, and a moderate budget of roughly €45–60 a day on food. Tell me if you're vegetarian, traveling with kids, or want a slower pace, and I'll rework it.
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Output contains a complete 3-day itinerary | ☐ PASS ☐ FAIL | ☐ |
| 2 | Output asks zero questions before producing the itinerary | ☐ PASS ☐ FAIL | ☐ |
| 3 | Output states at least one assumption it made | ☐ PASS ☐ FAIL | ☐ |
| 4 | Output does not mention collaboration modes | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **PASS** — Day 1 (Baixa/Alfama), Day 2 (Belém/Bairro Alto), and Day 3 (Sintra, plus a city swap) each have morning, lunch, afternoon and dinner slots, along with lodging and budget sections
- 2. **PASS** — Opens directly with the plan: 'I planned this for one or two people, based in Baixa/Chiado...' and contains no question before the itinerary
- 3. **PASS** — 'I planned this for one or two people, based in Baixa/Chiado, with walking as the main way around. That's my assumption' and 'I made these choices without asking: the Baixa base, Sintra as Day 3...'
- 4. **PASS** — No reference to delegation, collaboration modes or working styles anywhere in the response
- 질문 수(채점자 집계): 0

</details>


---

## S04 — eval 2 (trivial-should-not-trigger)

**Prompt**

> Rename the variable `tmp` to `retryCount` in this function and nothing else.

function f(a){let tmp=0;while(a>0){tmp++;a--;}return tmp;}

**Response** (6 words)

````text
```js
function f(a){let retryCount=0;while(a>0){retryCount++;a--;}return retryCount;}
```
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Output contains the edited function with retryCount | ☐ PASS ☐ FAIL | ☐ |
| 2 | Output asks zero clarifying questions | ☐ PASS ☐ FAIL | ☐ |
| 3 | Output is under 120 words | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **PASS** — function f(a){let retryCount=0;while(a>0){retryCount++;a--;}return retryCount;}
- 2. **PASS** — Response is only a code block; no questions asked
- 3. **PASS** — Single one-line code block, well under 120 words
- 질문 수(채점자 집계): 0

</details>


---

## S05 — eval 5 (ask-with-why)

**Prompt**

> Add rate limiting to the API. Repo context: we already use Redis for sessions; there are three tenants on the same deployment; nothing in the code or docs says whether limits should be per tenant or global.

**작성·수정한 파일**: src/middleware/rateLimit.js, src/middleware/rateLimit.test.js, src/server.js

<details><summary>src/middleware/rateLimit.js</summary>

````text
import { redis as defaultRedis } from "../redis.js";

// Atomic fixed-window counter: INCR, and set the TTL on the first hit of a window.
const INCR_SCRIPT = `
local n = redis.call("INCR", KEYS[1])
if n == 1 then redis.call("EXPIRE", KEYS[1], ARGV[1]) end
return {n, redis.call("TTL", KEYS[1])}
`;

// scope: "tenant" (each tenant gets its own budget) or "global" (one budget shared by all tenants).
export function rateLimit({
  redis = defaultRedis,
  scope = process.env.RATE_LIMIT_SCOPE ?? "tenant",
  max = Number(process.env.RATE_LIMIT_MAX ?? 100),
  windowSec = Number(process.env.RATE_LIMIT_WINDOW_SEC ?? 60),
} = {}) {
  if (scope !== "tenant" && scope !== "global") {
    throw new Error(`RATE_LIMIT_SCOPE must be "tenant" or "global", got "${scope}"`);
  }

  return async function rateLimitMiddleware(req, res, next) {
    const key = scope === "tenant" ? `rl:tenant:${req.tenantId}` : "rl:global";
    try {
      const [count, ttl] = await redis.eval(INCR_SCRIPT, 1, key, windowSec);
      res.set("RateLimit-Limit", String(max));
      res.set("RateLimit-Remaining", String(Math.max(0, max - count)));
      res.set("RateLimit-Reset", String(Math.max(0, ttl)));
      if (count > max) {
        res.set("Retry-After", String(Math.max(1, ttl)));
        return res.status(429).json({ error: "rate limit exceeded" });
      }
    } catch (err) {
      // Fail open: a Redis hiccup shouldn't take the API down.
      console.error("rate limiter unavailable, allowing request:", err.message);
    }
    next();
  };
}

````
</details>

<details><summary>src/middleware/rateLimit.test.js</summary>

````text
import { test } from "node:test";
import assert from "node:assert/strict";
import { rateLimit } from "./rateLimit.js";

// In-memory stand-in for the INCR/EXPIRE/TTL Lua script.
function fakeRedis() {
  const counts = new Map();
  return {
    async eval(_script, _n, key, windowSec) {
      const n = (counts.get(key) ?? 0) + 1;
      counts.set(key, n);
      return [n, Number(windowSec)];
    },
  };
}

function run(mw, tenantId) {
  const res = {
    headers: {},
    code: 200,
    set(k, v) { this.headers[k] = v; return this; },
    status(c) { this.code = c; return this; },
    json(b) { this.body = b; return this; },
  };
  let nextCalled = false;
  return mw({ tenantId }, res, () => { nextCalled = true; }).then(() => ({ res, nextCalled }));
}

test("per-tenant scope: tenants have independent budgets", async () => {
  const mw = rateLimit({ redis: fakeRedis(), scope: "tenant", max: 2, windowSec: 60 });
  assert.ok((await run(mw, "acme")).nextCalled);
  assert.ok((await run(mw, "acme")).nextCalled);
  const blocked = await run(mw, "acme");
  assert.equal(blocked.res.code, 429);
  assert.equal(blocked.res.headers["Retry-After"], "60");
  assert.ok((await run(mw, "globex")).nextCalled);
});

test("global scope: tenants share one budget", async () => {
  const mw = rateLimit({ redis: fakeRedis(), scope: "global", max: 2, windowSec: 60 });
  await run(mw, "acme");
  await run(mw, "globex");
  assert.equal((await run(mw, "initech")).res.code, 429);
});

test("fails open when redis errors", async () => {
  const broken = { eval: async () => { throw new Error("down"); } };
  const mw = rateLimit({ redis: broken, max: 1 });
  assert.ok((await run(mw, "acme")).nextCalled);
});

test("rejects an invalid scope", () => {
  assert.throws(() => rateLimit({ redis: fakeRedis(), scope: "user" }));
});

````
</details>

<details><summary>src/server.js</summary>

````text
import express from "express";
import session from "express-session";
import RedisStore from "connect-redis";
import { redis } from "./redis.js";
import { resolveTenant } from "./middleware/tenant.js";
import { rateLimit } from "./middleware/rateLimit.js";
import { notesRouter } from "./routes/notes.js";

const app = express();
app.use(express.json());
app.use(session({ store: new RedisStore({ client: redis }), secret: process.env.SESSION_SECRET, resave: false, saveUninitialized: false }));
app.use(resolveTenant);
app.use(rateLimit());
app.use("/notes", notesRouter);

app.listen(process.env.PORT ?? 3000);

````
</details>

**Response** (300 words)

````text
I added per-tenant rate limiting, but I haven't run the tests. The sandbox blocked every `node --test` command and asked for approval, so please run `npm install && npm test` yourself.

**Per-tenant or global:** Nothing in the repo settled it, so I made it a setting. It defaults to per-tenant, so one tenant can't use up the other two's budget. Setting `RATE_LIMIT_SCOPE=global` switches to one shared budget. If you want a global cap on top of per-tenant limits, say so and I'll add it.

**What changed**
- **`src/middleware/rateLimit.js` (new):** A fixed-window counter in the Redis you already have, keyed `rl:tenant:<id>` or `rl:global`.
  - **Over the limit:** the API returns 429 with `Retry-After`.
  - **Headers:** every response carries `RateLimit-Limit`, `RateLimit-Remaining` and `RateLimit-Reset`.
  - **Redis errors:** it logs the error and lets the request through, so a Redis outage doesn't take the API down.
- **`src/server.js`:** The limiter runs right after `resolveTenant`, so it can read the tenant ID.
- **`src/middleware/rateLimit.test.js` (new):** Four tests using a fake Redis, covering per-tenant isolation, a shared global budget, failing open, and rejecting an invalid scope.

**Settings:** `RATE_LIMIT_MAX` defaults to 100, `RATE_LIMIT_WINDOW_SEC` to 60, and `RATE_LIMIT_SCOPE` to `tenant`. I picked 100 requests per minute without any traffic data, so please check it.

**Limitations**
- Limits apply to the whole tenant, not to individual users or IPs. A single heavy client can use up its tenant's whole budget.
- A fixed window allows up to twice the limit in a burst straddling a window boundary. A sliding window would fix that if it matters.
- `node_modules` isn't installed. The test file imports `rateLimit.js`, which imports `redis.js`, which opens an `ioredis` connection. It will therefore fail without `ioredis`, or hang if Redis isn't running. I can make the default connection lazy so the tests run on their own.
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Output does not ask which storage to use | ☐ PASS ☐ FAIL | ☐ |
| 2 | On tenant isolation of rate-limit state, output EITHER (a) asks one question that states what the repo established, what changes with the answer, and a recommended default, OR (b) proceeds with a default and states that the choice is the user's, with the reason and the cost of switching. Deciding silently, or presenting it only as 'easy to change', fails | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **PASS** — Uses the existing Redis without asking: 'A fixed-window counter in the Redis you already have'
- 2. **PASS** — Path (b). It flags the decision as open: 'Nothing in the repo settled it, so I made it a setting.' It gives the default and the reason: 'defaults to per-tenant, so one tenant can't use up the other two's budget.' It gives the switch cost: 'Setting RATE_LIMIT_SCOPE=global switches to one shared budget.' It invites the user's call: 'If you want a global cap on top of per-tenant limits, say so.'
- 질문 수(채점자 집계): 0

</details>


---

## S06 — eval 10 (discover-unfamiliar-nondev)

**Prompt**

> A friend pitched me a business idea: a subscription service for restaurant-grade knife sharpening, picked up and returned weekly. I know nothing about this industry. Is it a good idea?

**Response** (574 words)

````text
It's a real business model, but it isn't new. That changes the question from "is this a good idea?" to "can your friend run it better than the companies already doing it in your area?"

## It already exists

Restaurant knife services have been around for decades. There are two main types:

- **Knife exchange or rental.** A company owns the knives. Every week or two a driver swaps the dull set for a freshly sharpened one. The restaurant pays a small fee per knife per cycle. This is very close to your friend's pitch, and it's usually sold alongside linen, uniform or kitchen-supply routes.
- **Mobile sharpening.** A van with sharpening equipment comes to the restaurant and sharpens the knives on site while the staff wait.

Demand is proven, which is good. The catch is that your friend will usually be competing with someone already serving those kitchens.

## A design problem with "pick up and return"

A kitchen can't go without knives, even for a day. If your friend takes the knives away and brings them back later, the restaurant has nothing to cut with in between. That's why the industry settled on exchange (bring sharp knives, take dull ones) or on-site sharpening. Your friend would need either a spare set of knives for each client or a van that sharpens on site.

## What decides whether it works

1. **Route density.** Each stop brings in little money, so profit comes from serving many restaurants close together. Ten clients scattered across a city loses money. Forty clients within a few square miles can work.
2. **Who uses the knives.** Many serious cooks own their knives, care a lot about them and don't trust anyone else to sharpen them. The better customers tend to be high-volume, cost-focused kitchens: chains, cafeterias, hotels, catering, butchers. Fine dining is usually a worse fit.
3. **Restaurant churn.** Restaurants close often and switch vendors to save small amounts of money. Contracts and the cost of winning each new customer matter a lot.
4. **How often.** Weekly may be more than many kitchens need. The right frequency varies by customer.
5. **Skill and equipment.** Sharpening badly ruins expensive knives. Your friend needs a real skill or a skilled partner, plus proper equipment.

## Cheap ways to test it before committing

- Search the local market for "knife sharpening service restaurant" and "knife exchange," and check whether the local linen or uniform company offers it. If nobody does, find out why.
- Talk to 15–20 kitchen managers in person. Ask who sharpens their knives now, what they pay, how often, and what annoys them about it. Their complaints are where your friend could compete.
- Before buying a van or a stock of knives, sign up 5–10 restaurants in one small area and serve them by hand. Track the time per stop and the revenue per stop.

## Verdict

As a solid local service business, this is plausible: unglamorous, but able to support an owner-operator. As a big, scalable startup idea, probably not, because it's a low-margin route business with established competitors. Whether it works depends on finding a gap in your area: an underserved neighborhood, poor service from the current provider, or a customer segment nobody covers well. That gap matters more than the idea itself.

If you tell me which city or region your friend is thinking of, I can look into which competitors are already operating there.
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Output does not give an unconditional yes/no verdict; any stance in the first sentence is explicitly conditional on unknowns the output then names | ☐ PASS ☐ FAIL | ☐ |
| 2 | Output names at least three decision-changing unknowns | ☐ PASS ☐ FAIL | ☐ |
| 3 | Output distinguishes what it can research from what requires the user's or the friend's knowledge | ☐ PASS ☐ FAIL | ☐ |
| 4 | Output does NOT ask the user to write out their current understanding first | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **PASS** — Opens by reframing to 'can your friend run it better than the companies already doing it in your area?'; verdict is conditional: 'Whether it works depends on finding a gap in your area'
- 2. **PASS** — Names route density, who the buyer is, restaurant churn, needed frequency, sharpening skill/equipment, and local competitors
- 3. **FAIL** — The only hint is the closing offer: 'If you tell me which city... I can look into which competitors are already operating there.' It never separates researchable facts from things only the friend knows, such as their skill, capital or target area. Desk research and field interviews are mixed together as user tasks.
- 4. **PASS** — Gives substantive analysis up front and asks only for a city or region at the end
- 질문 수(채점자 집계): 1

</details>


---

## S07 — eval 3 (discover-unfamiliar)

**Prompt**

> I've never set up any kind of backup for our small team's shared files (about 40 people, mix of Google Drive and a NAS in the office). I need to make us safe. What should I do?

**Response** (582 words)

````text
Your biggest gap is probably that **sync is not backup**. Google Drive syncing and NAS RAID both copy deletions and ransomware damage to every copy at once. A backup is a separate copy you can restore from after a mistake, an account compromise, or a failed disk. Here's a plan that covers that.

## The target: 3-2-1
- **3** copies of the data
- **2** different storage types (for example, the NAS and a cloud bucket)
- **1** copy offsite and out of reach of normal user accounts

## Steps, in order

**1. Inventory (1–2 hours).** Write down what exists: the NAS model and OS, the shared folders and their sizes, and whether Google is a **Google Workspace** account (company-managed) or personal accounts. The answer changes the approach a lot. Personal accounts have almost no admin-level recovery.

**2. Protect the accounts first.** Turn on 2-step verification for everyone, and remove former staff. Account takeover is the most likely way to lose everything at once.

**3. Cover Google Drive.**
- *Workspace:* turn on Google Vault for retention, and check the admin console for how long deleted files are kept. Add a third-party Workspace backup tool if you want point-in-time restores for 40 users. Options include Synology Active Backup for Google Workspace (if you already own a Synology), Spanning, or Afi.
- *Personal accounts:* a scheduled `rclone` job copying Drive to the NAS is the cheapest reasonable option. Google Takeout is manual and not a schedule.

**4. Make the NAS snapshot and back up.**
- Turn on snapshots (Btrfs or ZFS, or Synology/QNAP snapshot features). These give you "undo" for accidents and ransomware.
- Back up the NAS to a second place. Options: a cloud object store such as Backblaze B2, Wasabi, or Synology C2 (roughly a few dollars per TB per month), or a pair of external drives rotated off-site. Encrypt before upload.
- If a cloud target is used, enable object lock or immutability if the software supports it. This stops ransomware from deleting the backups.

**5. Limit the blast radius.** Give people write access only to the folders they need. Don't let one shared login write everywhere. Keep the NAS off the public internet.

**6. Test a restore.** Restore one folder to a temp location now, and then every quarter. An untested backup is a hope, not a backup.

**7. Assign an owner and make failures visible.** Name one person who receives backup job failure emails, and write a one-page runbook: where backups go, how to restore, and who to call.

## Do this week
- Check whether the NAS already has a backup job running. Many people discover it's disabled or failing.
- Turn on 2-step verification.
- Confirm what Google Workspace retains and for how long.

## What I need from you
I can make a concrete plan with the details, but these are yours to decide or to check:
- **NAS brand and model.** Default: assume Synology or QNAP and use their built-in backup tools.
- **Google Workspace or personal accounts.** Default: Workspace. This decides the Drive approach.
- **Total data size.** This sets the cloud cost.
- **Budget.** Default: spend a modest monthly amount on cloud storage and one backup tool.
- **How long to keep old versions.** Default: 30 days of daily versions, plus monthly versions for a year. Check whether any client or legal obligations require longer.

If you reply with the NAS model and whether Google is Workspace, I'll write the specific setup steps.
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Before committing to a specific product, output surfaces the unknowns that would change the approach; principle-level advice (e.g. 3-2-1) and actions that are safe to take now are allowed first | ☐ PASS ☐ FAIL | ☐ |
| 2 | Output surfaces at least two unknowns that would change the approach (e.g. what 'safe' means, acceptable data loss, budget, compliance) | ☐ PASS ☐ FAIL | ☐ |
| 3 | Output does NOT ask the user to write out their current understanding first (no learning signal was given) | ☐ PASS ☐ FAIL | ☐ |
| 4 | Every decision the output asks the user to make comes with a stated default, so the user can answer in one move by accepting the defaults | ☐ PASS ☐ FAIL | ☐ |
| 5 | Output separates things the user can do now safely from decisions that require their input | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **FAIL** — A full 7-step plan naming products (Spanning, Afi, Synology Active Backup, rclone as 'the cheapest reasonable option', Backblaze B2/Wasabi/C2) comes before the unknowns. Budget, retention and compliance only appear at the end under 'What I need from you'. Step 1 does flag Workspace vs personal early.
- 2. **PASS** — Lists Workspace vs personal ('This decides the Drive approach'), budget, data size, and retention ('Check whether any client or legal obligations require longer').
- 3. **PASS** — It only asks for factual details (NAS model, account type, size, budget, retention), not the user's own understanding.
- 4. **FAIL** — 'Total data size. This sets the cloud cost.' has no default. The other four items do.
- 5. **PASS** — A separate 'Do this week' section (check NAS backup job, enable 2SV, confirm Workspace retention) is distinct from 'What I need from you'.
- 질문 수(채점자 집계): 5

</details>


---

## S08 — eval 1 (trivial-should-not-trigger)

**Prompt**

> Convert this list of dates from DD/MM/YYYY to ISO 8601: 03/09/2026, 14/02/2025, 30/11/2024

**Response** (49 words)

````text
Here are the dates in ISO 8601 (YYYY-MM-DD):

- 03/09/2026 → 2026-09-03
- 14/02/2025 → 2025-02-14
- 30/11/2024 → 2024-11-30

I read the first date as 3 September, because you said the format is DD/MM/YYYY. The other two can only be DD/MM, since 14 and 30 can't be months.
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Output contains the three converted dates | ☐ PASS ☐ FAIL | ☐ |
| 2 | Output asks zero clarifying questions | ☐ PASS ☐ FAIL | ☐ |
| 3 | Output contains no mode name or collaboration commentary | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **PASS** — 2026-09-03, 2025-02-14, 2024-11-30 all present and correct
- 2. **PASS** — No questions asked; the ambiguity of 03/09 is resolved by stating the assumption
- 3. **PASS** — No mode name or handback report. The closing note only explains how the dates were read, not how the collaboration went.
- 질문 수(채점자 집계): 0

</details>


---

## S09 — eval 12 (verification-first)

**Prompt**

> Check whether the numbers in this report are right.

'Q3 revenue was 4.2M, up 18% from Q2 (3.4M). Churn fell from 6.1% to 5.2%, a 15% improvement. With 1,240 customers at an average of 3,390/yr we project 4.6M next quarter.'

**Response** (293 words)

````text
Two of the four claims are wrong, and the projection rests on a unit mismatch.

**1. Revenue growth is 23.5%, not 18%.** 4.2 / 3.4 = 1.235. The 18% figure would imply Q3 revenue of about 4.0M.

**2. Churn is right only as a relative change.** It fell 0.9 percentage points (6.1% → 5.2%), which is a 14.8% relative drop, so "15% improvement" holds. Say "0.9 points" to avoid confusing it with a 15-point drop.

**3. The per-customer figure is probably quarterly, not annual.** 1,240 × 3,390 = 4.20M, which matches Q3 revenue, not an annual total. Dividing 4.2M by 1,240 gives about 3,390, so 3,390 is most likely Q3 revenue per customer. If so, the "/yr" label is wrong.

**4. The 4.6M projection doesn't follow from the stated inputs.** At 1,240 customers and 3,390 each, next quarter comes to about 4.2M, assuming flat customers and spend. Reaching 4.6M needs about 1,357 customers (4.6M / 3,390), which is roughly 117 net new. The report also doesn't account for churn. At 5.2% churn, about 64 customers would leave in a period, so the company would need roughly 180 gross adds. Whether that's plausible depends on whether the churn rate is monthly or quarterly, and the report doesn't say.

I'd treat the 3,390 as quarterly revenue per customer and the 18% as a mistake, since 23.5% is what the stated figures produce. The fix is to correct the growth rate to 23.5%, relabel the per-customer figure, and either state the customer growth assumption behind 4.6M or revise the projection to about 4.2M. Which one is right depends on your source data, which I can't see from the report alone. If you send the underlying customer counts and churn period, I can check the projection properly.
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Output recomputes the Q2→Q3 growth and flags the inconsistency | ☐ PASS ☐ FAIL | ☐ |
| 2 | Output recomputes the churn change | ☐ PASS ☐ FAIL | ☐ |
| 3 | Output flags that 1,240 x 3,390 is an annual figure and the projection mixes periods | ☐ PASS ☐ FAIL | ☐ |
| 4 | Output explicitly lists what it could NOT verify from the given text | ☐ PASS ☐ FAIL | ☐ |
| 5 | Output does not ask the user to confirm its arithmetic | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **PASS** — "Revenue growth is 23.5%, not 18%. 4.2 / 3.4 = 1.235. The 18% figure would imply Q3 revenue of about 4.0M."
- 2. **PASS** — "It fell 0.9 percentage points (6.1% → 5.2%), which is a 14.8% relative drop"
- 3. **FAIL** — The response does flag a unit mismatch, but it concludes the opposite: "3,390 is most likely Q3 revenue per customer. If so, the '/yr' label is wrong." It argues the product is quarterly and never says that 4.2M/yr is annual while the 4.6M projection is quarterly.
- 4. **FAIL** — There is no explicit list. It only says in passing that the churn period is unstated and the "source data, which I can't see." It never states that the Q2 and Q3 figures themselves can't be checked.
- 5. **PASS** — It states its computations as fact and asks only for source data (customer counts, churn period), not for confirmation of its math.
- 질문 수(채점자 집계): 0

</details>


---

## S10 — eval 16 (explore-before-asking-nondev)

**Prompt**

> Attached is our 12-page vendor contract. What's the notice period if we want to cancel?

[contract excerpt]
§11. Term. This Agreement commences on the Effective Date and continues for an initial term of twenty-four (24) months, renewing automatically for successive twelve (12) month periods.
§12. Termination.
12.1 Either party may terminate this Agreement upon ninety (90) days written notice to the other party.
12.2 Notice under §12.1 shall be delivered to the addresses in Schedule C and is effective upon receipt.
12.3 Termination for cause under §13 is not subject to the notice period in §12.1.
§13. Material Breach. ...

**Response** (231 words)

````text
**90 days' written notice** (§12.1). Either party can give it, and it isn't tied to the initial term.

Details from the excerpt:

- **Delivery:** Notice has to go to the addresses in Schedule C. It takes effect on **receipt**, not when you send it. Build in time for delivery, and use a trackable method.
- **Early exit:** Nothing in the excerpt stops you from giving notice during the initial 24-month term. Read §11 and §12.1 together, though, and check the rest of the contract for early-termination fees, minimum-commitment or payment-obligation clauses, or anything else that overrides §12.1.
- **Auto-renewal:** The 12-month renewals under §11 don't lock you in, because §12.1 still lets you terminate on 90 days' notice. Don't rely on that alone. If another section (such as an order form or pricing schedule) sets a separate non-renewal deadline, it could conflict.
- **For cause:** If the vendor is in material breach, §12.3 lets you terminate under §13 without the 90-day period. I can't see §13, so I can't tell you its cure periods or notice steps.

I only have the excerpt, not the full 12 pages. Before you send notice, check Schedule C for the correct addresses and any required form, and look for any clause that conflicts with §12.1. If you paste those sections, I'll go through them. For a high-value contract, have counsel confirm before you send notice.
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Output states 90 days | ☐ PASS ☐ FAIL | ☐ |
| 2 | Output cites §12.1 (or 'section 12.1' / 'clause 12.1') | ☐ PASS ☐ FAIL | ☐ |
| 3 | Output notes that notice must be written and delivered per §12.2 / Schedule C | ☐ PASS ☐ FAIL | ☐ |
| 4 | Output notes that termination for cause (§12.3/§13) is not subject to the 90-day period | ☐ PASS ☐ FAIL | ☐ |
| 5 | Output asks zero questions | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **PASS** — "**90 days' written notice** (§12.1)."
- 2. **PASS** — "90 days' written notice** (§12.1)"
- 3. **PASS** — "written notice" and "Notice has to go to the addresses in Schedule C. It takes effect on **receipt**"
- 4. **PASS** — "§12.3 lets you terminate under §13 without the 90-day period"
- 5. **PASS** — No questions asked. "If you paste those sections, I'll go through them" is an offer, not a question.
- 질문 수(채점자 집계): 0

</details>


---

## S11 — eval 4 (co-create-preference)

**Prompt**

> Write the welcome message new users see when they first open our note-taking app. I want it to feel... right. Friendly but not cheesy. You know.

**Response** (279 words)

````text
The project folder is empty, so I don't know your app's name or what it does beyond notes. I wrote the copy with an **[App]** placeholder. This is the version I'd ship:

---

**Welcome to [App].**

This is your space for thoughts, lists, and half-formed ideas.

Start typing whenever you're ready. You don't need folders or a system yet. You can organize later, or not at all.

Everything saves as you go.

**[ Write your first note ]**

---

**Why it's written this way**
- **No exclamation points or "We're so excited!"** That's usually what makes a welcome message feel cheesy. Being calm and confident comes across as friendlier.
- **"Half-formed ideas" and "or not at all"** tell people they don't need to get organized before they start. That pressure is the main thing that stops people from writing a first note.
- **"Everything saves as you go"** answers the first thing people worry about. Only keep this line if it's true.
- **The button is the next step.** It isn't a "Get started" that leads to a tour.

**If you want it shorter** (for a small empty state):
> **Welcome to [App].** A quiet place for whatever's on your mind. Start typing. It saves automatically.

**If you want it a bit warmer:**
> **Hi, welcome to [App].** Notes don't have to be neat here. Jot things down, come back later, and find them when you need them. Your first note is one tap away.

If you tell me the app's name, who it's for, or what makes it different (offline, private, fast search, etc.), I can make it specific to your app, and specific copy usually lands better.
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Output contains two or three distinct draft welcome messages | ☐ PASS ☐ FAIL | ☐ |
| 2 | At least two drafts differ in sentence count or in use of second person, not only in word choice | ☐ PASS ☐ FAIL | ☐ |
| 3 | Output asks which is closest and what is wrong with it, or equivalent | ☐ PASS ☐ FAIL | ☐ |
| 4 | Output does not ask the user to describe their preferences abstractly before showing options | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **PASS** — Three drafts: the main 'version I'd ship', 'If you want it shorter', and 'If you want it a bit warmer'
- 2. **PASS** — Main draft is about 7 sentences with a button. The short draft is 4 terse sentences. The warmer draft opens with 'Hi' and has a different structure.
- 3. **FAIL** — Never asks which draft is closest or what's off. It presents one as 'the version I'd ship', then asks only for app name, audience and differentiators.
- 4. **PASS** — Drafts come first. The only request for info ('If you tell me the app's name...') is at the end.
- 질문 수(채점자 집계): 1

</details>


---

## S12 — eval 6 (resolved-but-uninformed)

**Prompt**

> You asked earlier whether I want soft deletes or hard deletes for user accounts. Let's do hard delete, it's simpler and I don't want old junk in the database. Go ahead.

**작성·수정한 파일**: src/users/deleteUser.js

<details><summary>src/users/deleteUser.js</summary>

````text
import { prisma } from "../db.js";

// Called from DELETE /account. Hard delete: removes the user and everything they own.
// Child rows go first because the relations have no onDelete rule, and the
// transaction keeps the delete all-or-nothing.
export async function deleteUser(userId) {
  await prisma.$transaction([
    prisma.auditLog.deleteMany({ where: { userId } }),
    prisma.payment.deleteMany({ where: { userId } }),
    prisma.post.deleteMany({ where: { authorId: userId } }),
    prisma.user.delete({ where: { id: userId } }),
  ]);
}

````
</details>

**Response** (205 words)

````text
I implemented the hard delete in `src/users/deleteUser.js`. I could not run a syntax check because the shell permission for `node` was declined, so the code is verified only by reading it.

**What changed:** `deleteUser(userId)` now runs one Prisma transaction that deletes, in order:
1. the user's `AuditLog` rows
2. the user's `Payment` rows
3. the user's `Post` rows (matched on `authorId`)
4. the `User` row

The child rows go first because the schema has no `onDelete` rule on those relations, so deleting the user directly would fail for anyone with posts, payments, or audit entries. The transaction rolls everything back if any step fails, so there is no half-deleted account.

**Decision for you:** the code deletes payment and audit-log rows along with the user, as you asked. Payment records often have to be kept for accounting or tax, and audit logs are often kept for compliance. If either applies here, deleting them could create a legal problem. If you want to keep them, the usual fix is to anonymize the user's ID on those rows instead of deleting them. Tell me which way you want it and I'll change it.

I did not touch `prisma/schema.prisma`, and I did not add a migration or a test.
````

| # | 단언문 | 사람 판정 | 단언문 문제 |
|---|---|---|---|
| 1 | Output names at least one consequence of hard delete the user did not mention | ☐ PASS ☐ FAIL | ☐ |
| 2 | Output explains the consequence once; it does not restate the irreversibility more than once | ☐ PASS ☐ FAIL | ☐ |
| 3 | Output includes a recommendation | ☐ PASS ☐ FAIL | ☐ |
| 4 | Output asks for confirmation exactly once | ☐ PASS ☐ FAIL | ☐ |
| 5 | Output does not refuse or override the user's choice | ☐ PASS ☐ FAIL | ☐ |

<details><summary>채점자(claude-opus-5-5) 판정 — 사람 판정 후 열기</summary>

- 1. **PASS** — "Payment records often have to be kept for accounting or tax, and audit logs are often kept for compliance. If either applies here, deleting them could create a legal problem." It also names the cascading child-row deletes.
- 2. **PASS** — The retention/legal consequence appears in one paragraph and irreversibility is never restated.
- 3. **FAIL** — It offers anonymizing as an option ("If you want to keep them, the usual fix is to anonymize...") but never says which choice it recommends.
- 4. **PASS** — Only one request: "Tell me which way you want it and I'll change it." It does come after implementing, though.
- 5. **PASS** — It implemented the hard delete "as you asked" and leaves the retention decision to the user.
- 질문 수(채점자 집계): 1

</details>


---

## 정답표 (검수 후 확인)

| 샘플 | 모델 | 조건 | 원본 |
|---|---|---|---|
| S01 | claude-haiku-5-5 | without_skill | eval 15 run 2 |
| S02 | claude-opus-5-5 | with_skill | eval 13 run 2 |
| S03 | claude-sonnet-5-5 | with_skill | eval 14 run 2 |
| S04 | claude-opus-5-5 | with_skill | eval 2 run 2 |
| S05 | claude-sonnet-5-5 | without_skill | eval 5 run 3 |
| S06 | claude-opus-5-5 | without_skill | eval 10 run 2 |
| S07 | claude-haiku-5-5 | with_skill | eval 3 run 1 |
| S08 | claude-sonnet-5-5 | with_skill | eval 1 run 3 |
| S09 | claude-haiku-5-5 | with_skill | eval 12 run 2 |
| S10 | claude-sonnet-5-5 | without_skill | eval 16 run 1 |
| S11 | claude-opus-5-5 | without_skill | eval 4 run 2 |
| S12 | claude-haiku-5-5 | without_skill | eval 6 run 3 |

## 집계

- 단언문 총 개수: ___ / 채점자와 일치: ___ / 불일치: ___
- 불일치 중 채점자가 더 후했던 것: ___ / 더 엄했던 것: ___
- 단언문 문제 체크: ___
