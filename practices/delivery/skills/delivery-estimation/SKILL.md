---
name: delivery-estimation
catalog_garden_tier: practice
catalog_garden_order: 72
catalogue_one_liner: >-
  Collaborative estimation at any scope level — contributing factors, categories, team vote, and recorded rationale.
description: >-
  Facilitate collaborative estimation sessions for backlog items at any scope level
  (epics, features, stories, thin slices). Identify contributing factors, assign
  estimation categories, record rationale, and surface new stories or acceptance
  criteria discovered during discussion. Interactive and item-by-item, not batch.
---
# delivery-estimation

**Manual:** `./manual/index.html`

## Purpose

Teams estimate badly not because they lack a formula but because they skip the conversation. Effort gets assigned by one person's hunch, contributing factors go unexamined, and nobody records why a number landed where it did — so every future re-estimate starts from scratch. Delivery estimation packages the facilitation pattern that makes sizing collaborative, factor-aware, and traceable: teams walk through backlog items one at a time, name what drives effort, agree on a category, and save the reasoning alongside the number.

## When to use this skill

Load this skill when **any** of the following apply:

- You have a backlog (epics, features, stories, or thin slices) and need **size or effort categories** before planning delivery order or capacity.
- A **new team** is forming and needs a structured scratch-estimation pass to build shared understanding of the work ahead.
- You want to **decompose effort by contributing factor** (complexity, uncertainty, dependencies, skill gaps, testing scope) rather than assign a single gut-feel number.
- The team needs an **interactive, item-by-item** estimation session — not a batch AI sweep — so discussion surfaces hidden risk and missing acceptance criteria.
- You already have estimates and want to **re-estimate** after scope changed, contributing factors shifted, or new information arrived.

---

## Core concepts

### Scope item

The **thing being estimated**. It can sit at any level of the backlog hierarchy. The skill works the same way regardless of granularity; what changes is the resolution of the contributing factors, the width of the estimation category, and what backlog changes are possible during discussion.

**Scope types:**

- **Epic** — a large user journey or capability area (e.g. "Adopt a Pet"). Estimating at this level gives rough portfolio sizing. Splits produce sub-epics or stories.
- **Sub-epic** — a segment of an epic that is still too broad to implement directly (e.g. "Submit and Track Adoption"). Splits produce stories.
- **Story** — a single user-valuable behaviour (e.g. "Submit Adoption Application"). The most common estimation level. Splits produce thin slices; merges combine stories that are too small to stand alone.
- **Thin slice** — a minimal vertical slice through a story (e.g. "Submit application with only required fields, happy path"). The finest estimation granularity. Merges combine slices that are trivially small.

Before estimating, the team must agree on **which delivery stages the estimate covers**. Use the **five bootcamp stages** from [`../../content/stages/README.md`](../../content/stages/README.md), plus cross-cutting test activities. Defaults apply unless the team opts in or out at session start.

| Bootcamp stage | What the estimate may include | Default |
| --- | --- | --- |
| **Shaping** | Outline map, module partition, architecture outline | *Out* |
| **Discovery** | Full map, domain/UX IA, blueprint, thin-slice placement | *Out* |
| **Exploration** | UL refresh, acceptance criteria, UX mockups, architecture template | *In* (AC at minimum; mockups/template opt in per session) |
| **Specification** | CRC, spec-by-example, scenario walkthrough, interface design, architecture reference | *In* |
| **Engineering** | `abd-interface-design` implementation (UX), object model (Engineer), acceptance tests / ATDD (Engineer), production code (Engineer) | *In* (interface implementation opt in when UI-heavy) |
| **Regression testing** | Broader regression suite maintenance | *In* |
| **User testing / UAT** | End-user validation outside the team | *Out* |

Engineering step 3 (**ATDD**) is executed by **Engineer** (package: `skills/story-driven-delivery/`); not a separate stage. Thin slicing is **last in Discovery**, not a separate prioritization stage.

An estimate without a stated coverage boundary is not comparable to another estimate. The session file records which stages are in and which are out.

### Contributing factor

A **dimension that drives effort** for a particular scope item. Common factors include technical complexity, domain uncertainty, external dependencies, skill gaps on the team, integration surface, testing depth, and regulatory overhead — but the catalog is team-owned. At the start of a session the team reviews a seed list and adds or removes factors that matter for their context. Each factor is scored or noted per item so the team can see **where** effort concentrates, not just how much there is.

### Estimation category

A **named range** rather than a precise number. Categories keep the conversation honest — nobody pretends to know whether a story is 11 or 13 points. The skill supports any scheme the team agrees on (T-shirt sizes, modified Fibonacci, simple Small / Medium / Large / Extra-Large, or custom ranges). Categories are defined once per session and reused for every item so estimates stay comparable.

### Split threshold

A **guideline that triggers proactive decomposition** when a story estimate lands above it. The threshold is set per session based on what the team considers "too big to commit to without breaking it down."

Default guidelines when estimating stories (coverage = exploration through engineering, including ATDD):

- **Points schemes:** > 5 points → suggest splitting into smaller stories
- **Day schemes:** > 8 days → suggest splitting into smaller stories

"Days" here means the full story lifecycle through **engineering** — exploration (AC), specification, acceptance tests, and implementation — not coding time alone. The threshold is a conversation trigger, not a hard rule: the team may keep a story whole if the estimate is confident and the contributing factors are well-understood. But crossing the threshold should always prompt the question: *Can this be broken into independently deliverable pieces?*

When a story crosses the threshold, use **`abd-thin-slicing`** (Discovery stage, last skill) to break it into thin slices. Each slice is estimated separately. The original story is marked "split — see children" in the session file.

### Team vote

The moment contributors **individually commit** to a category before discussion begins — the same principle as planning poker but applicable to any estimation scheme. Simultaneous reveal prevents anchoring. Disagreement is the signal, not the problem: when votes diverge, the highest and lowest voices explain their reasoning, contributing factors get re-examined, and the team votes again. The final category is the team's consensus, not an average.

### Estimate record

The **saved output** for one scope item: the chosen category, the contributing-factor breakdown, any comments or risks surfaced during discussion, and — critically — new stories or acceptance criteria that emerged because estimation forced the team to think concretely. Estimate records accumulate into the session log and become the input for delivery planning, capacity allocation, and future re-estimation.

### Interactive estimation

Estimation is **item-by-item and conversational**, not a batch operation. The agent (or facilitator) presents one scope item, proposes an initial category based on contributing factors, and the team discusses and votes before moving to the next. This deliberate pace is what makes estimation a discovery activity: rushing through a list defeats the purpose because the side-conversations — "wait, does this include the API migration?" — are where hidden scope and risk surface.

### Backlog changes during estimation

Estimation forces concrete thinking, and concrete thinking changes the backlog. Four kinds of change happen naturally during a session:

- **New acceptance criteria** — discussion reveals missing WHEN/THEN behaviour. Record and feed to **`abd-acceptance-criteria`** (Exploration, Product Owner).
- **New domain or UX artifacts needed** — record and note **Business Expert** or **UX Designer** extension work in the relevant stage.
- **New items** — work not on the map. Record and feed to **`abd-story-mapping`** (Discovery).
- **Split** — an item is too large or uncertain to estimate as one piece. The team breaks it apart. What it becomes depends on what it was:
  - Epic → sub-epics or stories (**`abd-story-mapping`**)
  - Story → thin slices (**`abd-thin-slicing`**)
  - Thin slice → rarely split further; consider whether it is really a story
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

---

## Build

**Goal:** Run an estimation session for a set of backlog items, producing an estimation-session setup and per-item estimate records.

1. **Establish the session scope.** Agree with the team on what is being estimated and at what granularity (epics, sub-epics, stories, thin slices). Review the **five bootcamp stages** and confirm which are included — defaults are **exploration** (AC), **specification**, **engineering** (ATDD + implementation), and **regression testing**. Opt in to **shaping**, **discovery**, exploration extras (mockups, arch template), engineering prototype, or **user testing** when the team wants those covered. Record the scope and coverage in the session setup using **`templates/estimation-session.md`**.

2. **Build the contributing-factors catalog.** Start with the seed factors in the session template. Ask the team: *What else drives effort for this kind of work?* Add team-nominated factors, remove any that do not apply, and lock the catalog for the session. New factors can still be added mid-session if an item reveals a dimension nobody anticipated — record the addition.

   Seed factors:

   | Factor | What it captures |
   | --- | --- |
   | Technical complexity | Moving parts, unfamiliar APIs, non-trivial algorithms |
   | Domain uncertainty | How well the team understands the business rules and edge cases |
   | External dependencies | Waiting on other teams, third-party services, vendor deliverables |
   | Skill gaps | Whether the team has done this kind of work before |
   | Integration surface | Number and complexity of integration points |
   | Testing depth | Amount of test coverage expected (unit, integration, E2E, manual) |

3. **Define estimation categories.** The team picks a scheme and records what each category roughly means in their context. Common schemes:

   | Scheme | Categories | Notes |
   | --- | --- | --- |
   | T-shirt | XS / S / M / L / XL | Most common; easy to explain |
   | Fibonacci-like | 1 / 2 / 3 / 5 / 8 / 13 | Gaps widen with uncertainty |
   | Simple | S / M / L / XL | Fewer buckets, faster sessions |
   | Custom | Team-defined | When the above do not fit |

   Each category needs a **rough meaning** in the team's context — e.g. "L = 3–5 days, multiple factors at play or significant uncertainty." Record the scheme and meanings in the session file's category-scheme section.

4. **Prioritize the backlog before estimating.** Present the full list of scope items and suggest a priority order — highest-risk or highest-value items first, so the team spends its sharpest attention where it matters most. Save the suggested order, then let the team reorder. The agreed priority becomes the estimation sequence. Record the final order in the session file's items table.

5. **Walk the backlog item by item, in priority order.** For each scope item:

   a. **Present the item** — name, description, and any known acceptance criteria.

   b. **AI suggests a starting category** — based on visible contributing factors (complexity signals, dependency count, domain novelty). The suggestion is a conversation starter, not a verdict.

   c. **Team votes** — each member commits to a category before seeing others. Reveal simultaneously.

   d. **Discuss divergence** — when votes disagree, the outliers explain. Re-examine contributing factors. Vote again if needed.

   e. **Check split threshold** — if the consensus category crosses the session's split threshold (default: > 5 points or > 8 days for stories), proactively suggest breaking the item into smaller stories or thin slices. The team decides: split now (pause estimation, decompose via **`abd-thin-slicing`**, estimate the pieces), or keep whole with a recorded justification. Do not silently accept large estimates — always surface the question.

   f. **Record the estimate** — fill an estimate record using **`templates/estimate-record.md`**: chosen category, contributing-factor scores or notes, discussion comments, and any risks surfaced.

   g. **Handle backlog changes** — estimation surfaces new scope and restructuring. Record every change in the estimate record's emergent-scope section, then use the right downstream skill to action it:

      - **New AC** on the current item → record it, then use **`abd-acceptance-criteria`** to write the WHEN/THEN.
      - **New story or epic** discovered → record it, then use **`abd-story-mapping`** to place it in the hierarchy.
      - **Split** — item is too large or uncertain to estimate as one piece:
        - Splitting an **epic** into sub-epics or stories → **`abd-story-mapping`**
        - Splitting a **story** into thin slices → **`abd-thin-slicing`**
      - **Merge** — items are too small or redundant → combine via **`abd-story-mapping`**, re-estimate the merged item.
      - After any structural change, persist to `story-graph.json` via **`story-graph-ops`**.

      When an item is split, **pause estimation on it**, estimate the resulting pieces instead, and mark the original as "split — see children" in the session file.

6. **Save the session.** The completed estimation session file and all estimate records together form the estimation output. Review the session for consistency: do the categories feel calibrated against each other? Flag any item where the team was deeply split and may need a spike or further decomposition before committing.

- **`templates/estimation-session.md`** — one file per session: scope level, coverage boundary, contributing-factors catalog, estimation-category scheme, priority-ordered items, and session summary.
- **`templates/estimate-record.md`** — one record per scope item: chosen category, factor breakdown, discussion notes, emergent scope.

- **Outputs:** One estimation-session file plus one estimate-record per backlog item.
- **While writing:** Use domain language from the backlog. Contributing factors should be specific to the item, not generic filler. Every estimate record should be traceable to its scope item.

---

## Validate

**Goal:** Inspect the estimation outputs as a reviewer — check that the session is honest, the records are complete, and the conversation was real.

- **Coverage boundary stated** — the session file names what the estimate includes (dev, test, design, etc.) so estimates are comparable.
- **Contributing factors are specific** — factor notes per item reflect that item's reality, not copy-pasted boilerplate across every record.
- **Categories are calibrated** — a quick scan of all records shows the categories make sense relative to each other (a "Large" item genuinely looks harder than a "Medium").
- **Discussion is visible** — estimate records with divergent votes show what the disagreement was about, not just the final number.
- **Emergent scope captured** — new AC, new stories, splits, merges, and open questions surfaced during estimation are recorded with the downstream skill tagged, not lost in discussion notes.
- **No invented precision** — estimates use the agreed categories, not fake-precise numbers that imply certainty the team does not have.
- **Split threshold honoured** — every story above the session's split threshold was either decomposed or has a recorded justification for staying whole.
- **Re-estimation path clear** — items flagged as deeply split or uncertain have a next step noted (spike, decompose, revisit after X).

---

## Deploy

This skill ships IDE-deployable files under **`ide-files/`**. Deploy them to any project:

```powershell
.\agents\abd-practice-skill-builder\skills\abd-author-practice-skill\scripts\Deploy-SkillOutputs.ps1 -SkillPath delivery-estimation -ProjectRoot <target-project> -Force
```

Default **`-IDE Cursor`**. Use **`-IDE Both`** when the target project should also receive **`.vscode/*.instructions.md`** and **`.github/prompts/*.prompt.md`**.

| File | Deploy target |
| --- | --- |
| `ide-files/delivery-estimation.mdc` | `.cursor/rules/` (Cursor always-on rule) |
| `ide-files/delivery-estimation.instructions.md` | `.vscode/` when deploy uses **`-IDE Both`** (VS Code — **same body** as `.mdc` after frontmatter; see **mdc-instructions-parity** rule in **abd-author-practice-skill**) |
| `ide-files/delivery-estimation.prompt.md` | `.cursor/commands/` (always); also `.github/prompts/` when deploy uses **`-IDE Both`** |

After editing `.mdc` or `.instructions.md`, validate parity (use an **absolute** `--workspace` path):

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-practice-skill-builder/abd-author-practice-skill \
  --workspace /absolute/path/to/repo/delivery-estimation
```

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Categories not fake precision

Estimates must use the agreed category scheme (T-shirt, Fibonacci-like, S/M/L/XL, or whatever the team chose), not precise numbers that imply certainty the team does not have. The whole point of categories is intellectual honesty — sizing conversation, not false exactness. Passing means all estimate records use the session's declared categories. Failing means records slip into point estimates, hour counts, or decimal-precision numbers outside the agreed scheme.

#### DO

- Use only the categories defined in the session's estimation-category scheme for every estimate record.

  **Example (pass):** Session defines S/M/L/XL. Every estimate record shows one of those four categories — no "M+" or "between M and L" or "7 points."

- Express calibration notes in category terms, not numbers.

  **Example (pass):** "This feels like the upper end of M but not yet L — team agreed M." — the team stayed in category language even when calibrating.

#### DO NOT

- Assign precise numbers (story points, hours, days) as the estimate when the session agreed on categories.

  **Example (fail):** Session defines T-shirt sizes, but estimate records say "3 story points" or "2.5 days" — the team abandoned the agreed scheme for false precision.

- Invent sub-categories or hybrid labels not in the session scheme.

  **Example (fail):** Session defines S/M/L/XL, but a record says "M/L" or "Medium-Large" — this is not a category the team agreed on, and it signals the team could not commit to a decision.

**Source:** Engagement convention (delivery-estimation rough requirements — "create estimation range and categories").

### Rule: Contributing factors are item-specific not boilerplate

Each estimate record's contributing-factor breakdown must reflect the reality of **that specific scope item**, not a copy-paste of the same scores across every record. Factors exist to show where effort concentrates for each item — when every row reads identically, the factors are decoration, not analysis. Passing means a reviewer can read the factor breakdown and learn something specific about the item's effort profile. Failing means factors are generic filler that could apply to any item in the backlog.

#### DO

- Score or note each contributing factor based on what is actually true for this scope item — different items should show different factor profiles.

  **Example (pass):**

  | Factor | Score / Note |
  | --- | --- |
  | Technical complexity | High — shelter API integration, multi-step submission |
  | Domain uncertainty | Medium — adoption rules known but shelter validation rules undocumented |
  | External dependencies | High — shelter API contract not finalized |

  Each cell names concrete reasons tied to this item.

- Add or remove factors mid-session when an item reveals a dimension the catalog did not anticipate, and note the addition.

  **Example (pass):** Estimate record for item 5 adds "payment latency" as a new factor with the note: "Added mid-session — payment gateway response time affects confirmation flow."

#### DO NOT

- Copy the same factor scores across every estimate record without differentiation.

  **Example (fail):** Five estimate records all show "Technical complexity: Medium, Domain uncertainty: Medium, External dependencies: Low" with identical wording — the factors do not distinguish one item from another.

- Use only single-word scores ("High", "Low") with no explanation of why that score applies to this item.

  **Example (fail):**

  | Factor | Score / Note |
  | --- | --- |
  | Technical complexity | High |
  | Domain uncertainty | Medium |
  | External dependencies | High |

  No indication of what makes complexity "High" for this item specifically.

**Source:** Engagement convention (delivery-estimation rough requirements — "record contributing factors", "new data added to contributing factor").

### Rule: Coverage boundary stated before estimates begin

The estimation session file must declare which **bootcamp delivery stages** the estimate covers before any items are estimated. Without a coverage boundary, estimates from different sessions or teams are not comparable. Stage definitions: [`../../content/stages/README.md`](../../content/stages/README.md).

**Default (included unless opted out):** exploration (AC), specification, engineering (ATDD + implementation), regression testing.

**Not default (opt in):** shaping, discovery, exploration extras (UX mockup, arch template), engineering `abd-interface-design` implementation pass, user testing / UAT.

Passing means the session file has an explicit coverage boundary checklist in the scope section. Failing means estimates exist but the reader cannot tell which stages are included.

#### DO

- State the coverage boundary as a checklist of bootcamp stages, marking each as included or excluded, in the session scope section.

  **Example (pass):**

  - [ ] **Shaping** *(not needed — outline map exists)*
  - [ ] **Discovery** *(map and slices complete)*
  - [x] **Exploration** — acceptance criteria
  - [ ] **Exploration** — UX mockups, architecture template *(deferred)*
  - [x] **Specification**
  - [x] **Engineering** — object model, ATDD, production code
  - [x] **Regression testing**
  - [ ] **User testing / UAT** *(Increment 2)*

  A reader knows exactly which stages are covered.

- Add a brief reason when opting a default stage out or a non-default stage in, so the decision is traceable.

  **Example (pass):** "[ ] Regression testing *(existing suite stable; negligible effort this increment)*" — the team actively decided to exclude it and said why.

#### DO NOT

- Leave coverage boundary blank, vague, or as a free-text summary that does not name the specific stages.

  **Example (fail):** Scope section says "**Coverage boundary:** Standard" or "Development + testing" — does not map to bootcamp stages.

- Use legacy stage names (prioritization, story definition, acceptance tests as a stage, code) instead of bootcamp names.

  **Example (fail):** "[x] Story mapping" and "[x] Acceptance tests stage" — use **Discovery** and **Engineering (ATDD)** instead.

- Assume coverage carries over from a previous session without restating it.

  **Example (fail):** Session file references "same as last sprint's estimation" with no checklist — the session file must stand alone.

**Source:** Engagement convention; bootcamp stages in `../../content/stages/`.

### Rule: Divergent votes show reasoning not just final category

When team votes on an estimate diverge (not unanimous on the first round), the estimate record must capture **what the disagreement was about** — whose votes differed, what each outlier said, and how the team resolved it. The estimate record exists so future readers (and re-estimation sessions) can understand **why** a number landed where it did. Passing means a reader can reconstruct the conversation from the record. Failing means the record shows a final category with no trace of the disagreement that preceded it.

#### DO

- Name the voters and their categories in each round, and quote or paraphrase what the outliers said during the divergence discussion.

  **Example (pass):**

  - **Round 1:** Sarah: L, Marcus: XL, Priya: M, Tomás: L
  - **Divergence discussion:** Marcus (XL): "We have no API contract yet — could be a week just figuring out the integration." Priya (M): "The form and frontend are straightforward; only the API call is unknown."
  - **Round 2:** Sarah: L, Marcus: L, Priya: L, Tomás: L
  - **Final consensus:** L

- Record "No divergence" explicitly when the vote was unanimous — do not leave the field blank.

  **Example (pass):** "**Round 1:** All four voted S. **Divergence discussion:** No divergence. **Final consensus:** S"

#### DO NOT

- Record only the final category without showing votes or discussion.

  **Example (fail):** "**Final consensus:** L" — no vote rounds, no names, no discussion. A future reader has no idea whether this was unanimous or contentious.

- Show that votes diverged but omit the reasoning.

  **Example (fail):** "**Round 1:** votes ranged from M to XL. **Round 2:** all voted L." — who said what and why is missing; the record does not explain the resolution.

**Source:** Engagement convention (delivery-estimation rough requirements — "team vote", "user can tweak, new data added to contributing factor").

### Rule: Emergent scope captured during estimation

Estimation forces concrete thinking, and concrete thinking changes the backlog — new acceptance criteria, new stories, splits, merges, and open questions surface when the team actually talks through an item. The estimate record must capture every backlog change so it feeds back into the right downstream skill and gets persisted. If changes only live in someone's memory or a chat thread, they are lost. Passing means any change discovered during estimation of an item is recorded in that item's estimate record with the downstream skill tagged. Failing means the record has a final category but no trace of what the team discovered or changed along the way.

#### DO

- Record each backlog change in the estimate record's emergent-scope section, tagged with the downstream skill that actions it.

  **Example (pass):**

  - **New AC** → `abd-acceptance-criteria`: Adoption application must validate pet availability before submission
  - **New story** → `abd-story-mapping`: Handle shelter API timeout gracefully
  - **Split** → `abd-thin-slicing`: Split into (1) submit with mock shelter API, happy path; (2) real shelter API with error handling
  - **Open question:** Does the shelter API support idempotent submission?

  Each item is actionable, tagged, and traceable.

- Record splits with what the item was split into and which skill handles the split based on scope type (epic splits use `abd-story-mapping`; story splits use `abd-thin-slicing`).

  **Example (pass):** "**Split** → `abd-thin-slicing`: Story too uncertain — split into two thin slices: (1) happy-path submission, (2) error handling and retry."

- Record merges when the team combines items that are too small or redundant.

  **Example (pass):** "**Merge** → `abd-story-mapping`: Combined 'View Pet Photo' and 'View Pet Details' into single story 'View Pet Details' — photo display is not a separate user action."

- Mark the emergent-scope section as empty ("None") when estimation did not surface anything new — do not omit the section.

  **Example (pass):** "**Emergent scope:** None — estimation confirmed existing scope is sufficient."

#### DO NOT

- Omit the emergent-scope section entirely from an estimate record.

  **Example (fail):** Estimate record has Item, Estimate, Factor breakdown, Team vote, Discussion notes — but no emergent-scope section. A reader cannot tell whether nothing was discovered or whether discoveries were lost.

- Capture backlog changes only in discussion notes as unstructured prose, without tagging the downstream skill.

  **Example (fail):** Discussion notes mention "Priya said we should split this" and "Marcus found a new AC about validation" but the emergent-scope section is empty or missing — the changes are buried in narrative without skill tags, and will likely not get actioned.

- Record a split or merge without naming what the item becomes.

  **Example (fail):** "**Split** → `abd-thin-slicing`: Item was too big, split it." — into what? A reader cannot act on this.

**Source:** Engagement convention (delivery-estimation rough requirements — "capture any comments as part of discussion using acceptance criteria, new story", "split items, merge").

### Rule: Estimation is interactive not batch

The estimation session must process items **one at a time** with team discussion between items, not in a single batch pass where an AI or facilitator assigns categories to the entire backlog at once. Batch estimation defeats the purpose of the practice: the side-conversations, surfaced risks, and emergent scope that come from deliberate item-by-item pacing are the main value of collaborative estimation. Passing means each item has its own vote cycle, discussion, and record. Failing means items were estimated in bulk without individual team engagement.

#### DO

- Present one scope item at a time, collect votes, discuss, and record before moving to the next.

  **Example (pass):** Session log shows item 1 fully estimated (votes, discussion, record) before item 2 is presented — each item has its own vote round and discussion section.

- Allow the team to revisit a previous estimate if a later item's discussion changes their understanding — record the revision.

  **Example (pass):** "Revised item 2 from S to M after item 4 revealed a shared dependency we had not considered. Original vote: all S. Revised vote: Sarah M, Marcus M, Priya M, Tomás M."

#### DO NOT

- Estimate the entire backlog in one pass without per-item discussion.

  **Example (fail):** A table of 15 items with categories assigned, and one discussion section at the bottom covering "general observations" — no per-item votes, no per-item factor analysis.

- Let the AI assign categories to all items before the team sees them, presenting the result as "here are your estimates."

  **Example (fail):** "Based on the backlog, here are the suggested estimates: Item 1: S, Item 2: M, Item 3: L, Item 4: M, Item 5: XL. Do you agree?" — no per-item discussion, no team vote cycle.

**Source:** Engagement convention (delivery-estimation rough requirements — "needs to be interactive eg AI does not batch every 'thing' being estimated").

### Rule: Large stories proactively trigger split suggestion

When estimating at story level and the consensus category crosses the session's split threshold, the facilitator (or agent) must proactively suggest decomposition before recording the estimate. The default thresholds are > 5 points (point-based schemes) or > 8 days (day-based schemes, where "days" means through **engineering**, not coding alone). The threshold is a conversation trigger, not an automatic split — the team can keep the story whole if they justify it. Passing means every story above the threshold has either been split or has a recorded justification for staying whole. Failing means large stories are silently accepted without the question being raised.

#### DO

- Surface the split question whenever a story's consensus category crosses the session's declared split threshold.

  **Example (pass):** Story lands at XL in a session where the threshold is > L. Facilitator says: "This crossed our split threshold — can we break it into independently deliverable pieces?" Team discusses and splits into two thin slices via `abd-thin-slicing`.

- Record a justification when the team decides to keep a large story whole despite crossing the threshold.

  **Example (pass):** Estimate record notes: "Crossed split threshold (XL > L). Team decided to keep whole — the shelter API integration cannot be meaningfully separated into independent slices until the spike completes. Will re-estimate after spike."

- Define the split threshold as part of session setup and record it in the session file's category-scheme section.

  **Example (pass):** Session file says: "**Split threshold:** > L (any item estimated XL triggers a split discussion)."

#### DO NOT

- Silently accept a story estimate above the split threshold without raising the decomposition question.

  **Example (fail):** Story lands at 8 points in a session with a > 5 threshold. The estimate is recorded as 8 with no mention of whether splitting was considered — a reader cannot tell if the team consciously accepted the size.

- Treat the threshold as an automatic split without team discussion.

  **Example (fail):** Story lands at XL, agent immediately splits it into three thin slices without asking the team — the threshold is a prompt for conversation, not a mandate.

**Source:** Engagement convention (delivery-estimation requirements — "if the estimation is too large and we are doing stories, proactively suggest to break it up"; guidelines: > 5 points, > 8 days covering story through acceptance test).
<!-- execute_rules:bundle_rules:end -->
