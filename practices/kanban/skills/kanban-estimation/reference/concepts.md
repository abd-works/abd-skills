# kanban-estimation — Concepts

## Scope item

The **thing being estimated**. It can sit at any level of the backlog hierarchy. The skill works the same way regardless of granularity; what changes is the resolution of the contributing factors, the width of the estimation category, and what backlog changes are possible during discussion.

**Scope types:**

- **Epic** — a large user journey or capability area (e.g. "Adopt a Pet"). Estimating at this level gives rough portfolio sizing. Splits produce sub-epics or stories.
- **Sub-epic** — a segment of an epic that is still too broad to implement directly (e.g. "Submit and Track Adoption"). Splits produce stories.
- **Story** — a single user-valuable behaviour (e.g. "Submit Adoption Application"). The most common estimation level. Splits produce thin slices; merges combine stories that are too small to stand alone.
- **Thin slice** — a minimal vertical slice through a story (e.g. "Submit application with only required fields, happy path"). The finest estimation granularity. Merges combine slices that are trivially small.

Before estimating, the team must agree on **which delivery stages the estimate covers**. Use the **five bootcamp stages** from the stage files in `reference/stages/`, plus cross-cutting test activities. Defaults apply unless the team opts in or out at session start.

| Bootcamp stage | What the estimate may include | Default |
| --- | --- | --- |
| **Shaping** | Outline map, module partition, architecture outline | *Out* |
| **Discovery** | Full map, domain/UX IA, blueprint, thin-slice placement | *Out* |
| **Exploration** | UL, acceptance criteria, UX mockups, architecture template | *In* (AC at minimum; mockups/template opt in per session) |
| **Specification** | domain model, spec-by-example, clickable UX prototype, architecture reference | *In* |
| **Engineering** | domain code (BE), acceptance tests / ATDD (PO), production code incl. UI (Engineer) | *In* |
| **Regression testing** | Broader regression suite maintenance | *In* |
| **User testing / UAT** | End-user validation outside the team | *Out* |

Engineering step 3 (**ATDD**) is executed by **Engineer** (package: `skills/story-driven-delivery/`); not a separate stage. Thin slicing is **last in Discovery**, not a separate prioritization stage.

An estimate without a stated coverage boundary is not comparable to another estimate. The session file records which stages are in and which are out.

---

## Contributing factor

A **dimension that drives effort** for a particular scope item. Common factors include technical complexity, domain uncertainty, external dependencies, skill gaps on the team, integration surface, testing depth, and regulatory overhead — but the catalog is team-owned. At the start of a session the team reviews a seed list and adds or removes factors that matter for their context. Each factor is scored or noted per item so the team can see **where** effort concentrates, not just how much there is.

## Estimation category

A **named range** rather than a precise number. Categories keep the conversation honest — nobody pretends to know whether a story is 11 or 13 points. The skill supports any scheme the team agrees on (T-shirt sizes, modified Fibonacci, simple Small / Medium / Large / Extra-Large, or custom ranges). Categories are defined once per session and reused for every item so estimates stay comparable.

## Split threshold

A **guideline that triggers proactive decomposition** when a story estimate lands above it. The threshold is set per session based on what the team considers "too big to commit to without breaking it down."

Default guidelines when estimating stories (coverage = exploration through engineering, including ATDD):

- **Points schemes:** > 5 points ? suggest splitting into smaller stories
- **Day schemes:** > 8 days ? suggest splitting into smaller stories

"Days" here means the full story lifecycle through **engineering** — exploration (AC), specification, acceptance tests, and implementation — not coding time alone. The threshold is a conversation trigger, not a hard rule: the team may keep a story whole if the estimate is confident and the contributing factors are well-understood. But crossing the threshold should always prompt the question: *Can this be broken into independently deliverable pieces?*

When a story crosses the threshold, use **`abd-thin-slicing`** (Discovery stage, last skill) to break it into thin slices. Each slice is estimated separately. The original story is marked "split — see children" in the session file.

## Team vote

The moment contributors **individually commit** to a category before discussion begins — the same principle as planning poker but applicable to any estimation scheme. Simultaneous reveal prevents anchoring. Disagreement is the signal, not the problem: when votes diverge, the highest and lowest voices explain their reasoning, contributing factors get re-examined, and the team votes again. The final category is the team's consensus, not an average.

## Estimate record

The **saved output** for one scope item: the chosen category, the contributing-factor breakdown, any comments or risks surfaced during discussion, and — critically — new stories or acceptance criteria that emerged because estimation forced the team to think concretely. Estimate records accumulate into the session log and become the input for delivery planning, capacity allocation, and future re-estimation.

## Interactive estimation

Estimation is **item-by-item and conversational**, not a batch operation. The agent (or facilitator) presents one scope item, proposes an initial category based on contributing factors, and the team discusses and votes before moving to the next. This deliberate pace is what makes estimation a discovery activity: rushing through a list defeats the purpose because the side-conversations — "wait, does this include the API migration?" — are where hidden scope and risk surface.

---

## Backlog changes during estimation

Estimation forces concrete thinking, and concrete thinking changes the backlog. Four kinds of change happen naturally during a session:

- **New acceptance criteria** — discussion reveals missing WHEN/THEN behaviour. Record and feed to **`abd-story-acceptance-criteria`** (Exploration, Product Owner).
- **New domain or UX artifacts needed** — record and note **Business Expert** or **UX Designer** extension work in the relevant stage.
- **New items** — work not on the map. Record and feed to **`abd-story-mapping`** (Discovery).
- **Split** — an item is too large or uncertain to estimate as one piece. The team breaks it apart. What it becomes depends on what it was:
  - Epic ? sub-epics or stories (**`abd-story-mapping`**)
  - Story ? thin slices (**`abd-thin-slicing`**)
  - Thin slice ? rarely split further; consider whether it is really a story
- **Merge** — two or more items are too small or too similar to justify separate estimates. Combine them into one item at the same scope level (**`abd-story-mapping`**).

After any backlog change, use **`story-graph-ops`** to persist the update to `story-graph.json` so the map and the estimates stay in sync.

---

## The shape of estimation output

An estimation session produces two kinds of file. The **session file** frames the whole pass — what is being estimated, what the estimate covers, which factors drive effort, and what categories the team agreed on. Each **estimate record** captures one item's category, factor breakdown, vote rounds, discussion, and any scope that surfaced.

### Session file (from `templates/estimation-session.md`)

```
Session metadata   — date, facilitator, participants
Scope              — granularity (epic / sub-epic / story / thin slice)
                     source (story map, sprint backlog, etc.)
                     coverage boundary checklist (bootcamp stages):
                       [ ] shaping (not default)
                       [ ] discovery (not default)
                       [x] exploration — AC (default); mockups/template optional
                       [x] specification
                       [x] engineering — ATDD + implementation (prototype optional)
                       [x] regression testing
                       [ ] user testing / UAT (not default)
Factors catalog    — team-agreed dimensions that drive effort
                     e.g. complexity, uncertainty, dependencies,
                     skill gaps, integration, testing depth
Category scheme    — the ranges the team will vote with
                     e.g. S / M / L / XL with rough meanings
                     split threshold (items above it trigger decomposition)
Items estimated    — priority-ordered table (priority, item, category, split?, notes)
                     AI suggests order; team reorders before starting
Session summary    — totals, flagged items, new stories/AC found
```

### Estimate record (from `templates/estimate-record.md`)

```
Item               — name, scope level, source
Estimate           — chosen category, coverage
Factor breakdown   — per-factor score + why (specific to this item)
Team vote          — round 1 votes, divergence discussion,
                     round 2 if needed, final consensus
Discussion notes   — what the team talked about
Emergent scope     — new AC, new stories, splits, merges, open questions
                     each tagged with the downstream skill to action it
Follow-up          — spike, decompose, or none
```
