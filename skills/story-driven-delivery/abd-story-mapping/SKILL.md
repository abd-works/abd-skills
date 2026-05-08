---
name: abd-story-mapping
catalog_garden_tier: practice
catalog_garden_order: 10
catalogue_one_liner: >-
  Patton-style story maps (epics, stories, verb-noun naming); writes story-map templates from sources.
description: >-
  Teaches Patton-style story mapping: epics, sub-epics, stories, verb–noun naming, and
  actors via story_type. When building a map from sources, outputs **all** template
  artifacts in `templates/` (currently `story-map.md` and `story-map.txt`) with the
  same tree — not one or the other. Use when structuring product discovery, decomposing
  user journeys, identifying epics and flows, story mapping, organizing requirements
  into a hierarchical map, or when the user mentions story maps, epics, sub-epics, or
  Jeff Patton–style backlog structure.
---
# abd-story-mapping

## Purpose

A **story map** in the **Jeff Patton** sense is a **single shared picture** of the product: you organize understanding into a **small stack of nested levels**—**epics** (broad capability areas), **sub-epics** (flows or feature areas within an epic), and **stories** (leaves: one observable **user** or **system** interaction each). The map is **not** a dump of source material, a WBS, or a list of build tasks; it is **outcomes and behaviors**—*what* happens in the product—so product, delivery, and domain people can read the same structure.

**Naming** is part of the model: epics, sub-epics, and stories use **verb–noun** titles; **who** is acting (persona/actor, user vs. system) is carried **outside** the name (e.g. `story_type` / diagram convention), not stuffed into the title. Good maps read as a **journey** (sequence along the backbone) and a **skeleton of scope** (depth into detail), with **consistent language** from top to bottom.

This document defines **concepts, naming, and quality** for that structure. **How** to run agents, lay out a workspace, or use CLIs belongs in the **agent** and **tooling** skills—not here.

## When to use this skill

Load this skill when **any** of the following apply:

- You need to capture goals, decompose user journeys, or capture a solution as a set of user–system interactions (stories grouped into epics).
- A user or agent wants to restructure sources of context (eg: requirements docs, interviews, a product brief, or even a rough description) into a new or existing story map.
- An agent is asked to "map out the system", "identify the epics", "structure the work", or "figure out what we're building using stories"
- You want to organize existing code, solutions, or tests into a hierarchical story-map format.

## Output file

**Where to write the deliverables (`<deliverables-folder>` resolution):**

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **Where the engagement already keeps deliverables.** Look at the workspace; if previous phase output (key-abstractions, domain sketch, `process.md`, `corrections-log.md`) already lives in a folder, write next to them in the **same** folder.
3. **The workspace root.** If neither applies, write to the workspace root.

Do **not** assume a predetermined folder name like `stories/` or `docs/`. The only DDD/story skill that creates a sub-folder is **`abd-module-partition`**.

**File names:** Default to the template filenames — `story-map.md` (and `story-map.txt` when present). Add a `<name>-` engagement prefix only when you need disambiguation — multiple products in the same workspace, or the user asks for it explicitly. Both `story-map.md` and `<name>-story-map.md` are valid. The companion `story-graph.json` (managed by **`story-graph-ops`**) follows the same convention.

---

## Agent Instructions

1. **Templates**

Generate content using **every** template file in this skill’s `templates/` folder. **Do not** emit only Markdown or only plain text unless the user **explicitly** asks for a single format.

**Use every template file (required)**

When you **create or rewrite** a story map from requirements, you **must** deliver **one output artifact per file** in `templates/`.

| Template | What to produce |
| --- | --- |
| `templates/story-map.md` | The epic/sub-epic/story tree using that layout. Optional title or short context above the tree is fine. **Do not** paste the template’s notation / `## Instructions` section (or equivalent) into generated project files — that material documents the template for skill maintainers, not stakeholders reading the map. |

**Consistency:** Connectors (`or`, `opt`), nested `(AC)` lines, and actor/story lines must match between `.md` and `.txt` for the same map. Generated artifacts contain **only** the map (plus optional brief context in `.md`); notation rules stay in this skill and in `templates/story-map.md` for reference.

**If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

**Depth:** Respect the depth level the user asks for (see **Depth levels** under *Iterating the map*). At **Story Map Outline (breadth pass)**, produce epics with confirming stories — include sub-epics where the domain naturally groups into distinct flows, but do not apply the full rule set. At **Level 2+**, apply the full hierarchy and rules. Default to Level 2 when the user does not specify.



**Quality bar:** Match the naming and layout expectations in **Core concepts** and **The shape of a good story map** below.

**Where it lives:** In a project, the map is often mirrored in **`docs/story/story-graph.json`** (or the workspace’s graph path) via **story-graph-ops** or the bot; this skill still treats **`story-map.md`** and **`story-map.txt`** as the template-aligned outputs you author first.

2. **Rules**

- Generate content following the rules attached to this skill (listed below, assembled from **`rules/*.md`**).
- After content exists, act as a *peer reviewer*: walk each rule’s constraints, DO/DON’T sections, and examples; be helpful but critical when comparing the deliverable to each rule.

- **Who is checking:** A **product owner** (scope and outcomes), a **developer** (clarity and testability of behaviors), and a **domain expert** (language and flows) should all agree on what the map says.
- **Cross-artifact parity:** The `.md` and `.txt` trees must match (connectors, nesting, actors on story lines).

3. **Assembling this skill**

This **`SKILL.md`** is assembled from **`rules/`** into the bundled block below. Use **`bundle_rules_into_skill_md.py`** from **`skills/execute-skill-using-skills-rules/scripts/`** whenever **`rules/*.md`** changes:

---

## What is a story map?

A **story map** is a visual, hierarchical model of how users and systems interact with a product or service. It was popularized by Jeff Patton and is central to Agile by Design's approach to discovery.

A story map answers three questions:
1. **Who** uses the system? (Actors)
2. **What** are the major capability areas? (Top Level Epics)
3. **How** do users move through those areas, step by step? (Lower Level Epics and Stories)

Story maps are intentionally **not implementation plans**. They describe *outcomes and behaviors*, not tasks, tickets, or technical steps, although they can be used to describe system to system interactions and complex system behaviors. A good story map can be understood by a product owner, a developer, and a domain expert — all at once.

### Why story map?

A story map is a **collaborative method** to break work down. It provides a structure to guide collaborative thought in order to achieve **shared understanding** — alignment from more than one perspective, the engineering team, the product and stakeholders affected by the product. It is a method to break down *what you are working on*, not *the way you work*.

The perspective provided by a story map is **cross-functional**: SMEs, analysts, developers, testers, delivery lead — various viewpoints that together produce a more complete picture than any individual could. Story maps are useful when a project, initiative, or product is in discovery and the scope of functions, features, and goals needs to be fleshed out and understood.

---

## Core concepts

### Actors

An **actor** is anyone (or anything) that interacts with the system. Actors are the *who* behind every story.

| Actor type | Description | Examples |
|---|---|---|
| **User** | A human who uses the system directly | Customer, Administrator, Agent |
| **System** | An external system or automated process | Payment gateway, Email service, Scheduler |

Actors do NOT appear in story names — they are captured in the `story_type` field and optionally in `notes`. The name describes the *behavior*, not who does it.

### Personas

A **persona** is a representative description of a segment of customers or users. Personas create a unified view of who the target is and their needs, and model customer behaviour based on validated information.

Before building the map, identify the personas from the available context. For each persona determine their goals and the activities they need to meet those goals — these drive the epics and stories below.

In the story map, personas sit at the **top layer** — each persona's goals drive the epics below them. Actors in `story_type` may map to one or more personas.

---

### Epics

An **epic** is a major **capability area** of the system — a broad theme that groups related user journeys together.

Epics answer: *"What is this area of the product responsible for?"*

- They are not **user stories** — they are containers for flows
- A medium sized system typically has 3–8 top level epics
- Named in **verb-noun format**: `Manage Customer Orders`, `Track Fleet Vehicles`, `Process Payments`
- Each epic spans the entire left-to-right axis of the story map at the top level

**Good:** Manage Customer Orders, Process Online Payments. **Weak:** Orders, Backend, Admin.

---

### Epic Hierarchy

Top level epics often have one or more layers of children epics, often called **sub-epic**.  Each sub-epic is often a **flow or feature area** within that epic — a coherent sequence of interactions that achieves a meaningful outcome.

Sub-epics answer: *"What are the distinct flows or phases within this capability area?"*

- A sub-epic often maps to a user journey (e.g., "place an order" is a flow within "manage orders")
- Each sub-epic groups the stories that belong to that flow
- Also named in **verb-noun format**: `Place New Order`, `Review Order History`, `Cancel Order`
- Sub-epics can nest (a flow can have sub-flows), but depth will likely be shallow — 1–2 levels usually enough, unless the system is quite large.

**Good:** Place New Order, Review Order History. **Weak:** Order flow, Checkout stuff.

---

### Stories

A **story** is a **discrete, observable behavior** — a single thing a user or system does within a flow.

Stories answer: *"What is the specific action or interaction happening here?"*

- Stories are the leaves of the story map — they cannot be decomposed further at this stage
- Each story should be independently testable in principle
- **Verb + noun** (e.g. Place Order, Validate Payment). Put the actor in `story_type`, not in the title.
- Stories are behaviors, not tasks — “call the payments API” is a task; “process payment” is a story.

**Good:** Place Order, Select Delivery Address, Validate Payment. **Weak:** Customer Places Order; Payment Processing; Selects Tokens; API call; button click.

Prefer what happens over how it is shown — **Show order confirmation** beats **Displaying order confirmation** as the main verb.

#### Story types

| `story_type` | Meaning | Style in diagram |
|---|---|---|
| `user` | Human user | Yellow |
| `system` | External or automated system | Dark blue |
| `technical` | Infra, background jobs, non-visible | Black |

Use **user** and **system** for normal product behavior. **technical** (black) sparingly — only when someone explicitly wants that on the map.

---

### Notes on context capture

If useful detail does not fit a node name, put it in that node’s `notes` and cite the source (file, page, section, or `"type": "chat"`). Check `notes` before re-reading raw sources when you continue work on the same map.

---

### Pitfalls for agents

**Assess context coverage before mapping.** Before building or extending a story map, check whether the available context covers the perspectives needed: product/business intent, technical constraints, operational concerns, and user experience. If an entire dimension is absent (e.g. no technical input on system interactions, or no business rules for a domain area), flag it as a gap. A map built from a single perspective will churn when the missing viewpoint surfaces.

**Don't fabricate to fill gaps.** When context is incomplete — a business rule is unclear, a system boundary is unknown, a domain has no source material — do not invent stories or structure to cover the gap. Capture what is missing, state your assumption, and recommend a validation action (e.g. "confirm with product owner whether returns follow the same flow as exchanges"). Unknowns surfaced honestly are more valuable than a plausible-looking map that turns out to be wrong.

**Don't defer analysis the source material supports.** If the source describes how a workflow or entity type works, map it now {em} don't write "not yet mapped" as a gap. Gaps are for missing information, not unfinished work.

When building or reviewing a story map, chase down all available context sources for gaps or filters: don't let important perspectives be silently excluded due to missing domain input, technical details, or user workflows. Critically assess whether any actors, flows, or constraints have been filtered out or overlooked; thoroughness means actively hunting for missing context, not just mapping what is easily present.


**Don't add scope the user didn't ask for.** If the user describes one path (e.g., manual onboarding), don't add a second (e.g., self-service onboarding) and present it as part of the map. When a choice exists, ask.

### Recording context gaps in the story map

Context gaps must be captured **inside the story map output files** (`story-map.md` and `story-map.txt`) so they travel with the map. Use one or both placements depending on scope:

**Inline gaps** — when a gap applies to a specific epic, sub-epic, or story, place a `* Gap:` line indented under that node:

```
(E) Direct Mob Combat
    (E) Assign Mob Strategy
        (S) GM --> Select Mob Strategy
        * Gap: Is the strategy list extensible by the GM, or fixed?
    (E) Execute Mob Attack
        (S) System --> Resolve Melee Attack
```

**Map-level gaps** — when a gap applies to the whole map or cuts across multiple areas, place a `## Context Gaps` section at the bottom of the file:

```
## Context Gaps
- No technical input on Foundry VTT module API constraints.
- Single perspective (GM only); no QA or dev viewpoint yet.
```

Use **inline** when the gap is local to a node; use **map-level** when it is broad. Both can appear in the same file. The `.md` and `.txt` outputs must include the same gaps in the same positions.

---

### Iterating the map

Do not treat the map as a one-shot deliverable. Deeper analysis will surface information that invalidates earlier structure — stories split, epics merge, flows reorder. This is expected.

When new context arrives or downstream work (AC, scenarios, tests) exposes gaps, revise the map rather than working around stale structure. Keep the map lightweight enough that restructuring is cheap.

#### Depth levels

Apply progressive depth. Each level builds on the previous — do not skip ahead.

**Story Map Outline — Breadth pass (Idea Shaping)**

Go wide, not deep. Produce **epics** and **confirming stories** — enough to prove each epic is real and the scope is right.

A confirming story is a short verb-noun name that exercises the epic's key domain nouns. It exists to validate that the epic covers real, distinct behavior — not to describe a full flow. Each epic needs at least two confirming stories; add more when the epic spans obviously different areas, but do not decompose into sub-flows.

What you produce:

- Top-level epics (verb-noun) covering the major capability areas
- 2+ confirming stories per epic — each names a concrete behavior that proves the epic belongs
- Actors identified per epic (who triggers, who responds)
- Context gaps where the source is genuinely silent

What you do **not** produce at this level:

- Detailed flows, scenarios, or steps
- System/application lifecycle behaviors (persistence, logging, sync)
- Consolidation notes or mechanic-by-mechanic analysis
- Full story decomposition per the deeper rules

When to stop: every major capability area has an epic, each epic has confirming stories, and a reviewer can see the product scope. If the map reads as a credible table of contents for the product, the outline is done.

When to use: first contact with new context, early discovery, scope alignment with stakeholders, or when the user asks for "just the epics", a "breadth pass", "outline", or "idea shaping."

**Level 2 — Increment discovery**

Deepen selected epics into sub-epics and fully decomposed stories. Apply the full rule set: distinct mechanics get distinct stories, consolidate superficial duplicates, analyze before grouping, map system behaviors, scale by domain. Leave epics the team will not build soon at outline depth.

**Level 3 — Story refinement**

Detail stories for the next delivery increment: acceptance-criteria hooks, failure modes, consolidation notes, passive-vs-active runtime analysis. Later increments stay at outline or Level 2.

Do not over-elaborate areas the team will not build soon. Go deep where uncertainty is highest or delivery is imminent.

---

## Example

```
Epic: Manage Customer Orders
  └── Sub-Epic: Place New Order
        ├── Story: Browse Product Catalog         [user]
        ├── Story: Add Item To Cart             [user]
        ├── Story: Enter Shipping Address       [user]
        ├── Story: Select Delivery Option       [user]
        └── Story: Submit Order                 [user]
  └── Sub-Epic: Track Order Status
        ├── Story: View Current Order Status    [user]
        └── Story: Receive Shipment Notification [system]
  └── Sub-Epic: Cancel Order
        ├── Story: Cancel Order Request         [user]
        └── Story: Process Cancellation Refund [system]
```

Notice:

- Epics are **wide** — they span the whole capability area
- Sub-epics are **flows** — each tells a coherent mini-story
- Stories are **small** — one behavior each; names are verb–noun; actor only in `story_type`

---

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers, not a second authoring pass.


Checklist:

- **Hierarchy** — epics → sub-epics → stories; **verb–noun** names; actors only in `story_type`, not in titles.
- **Story size** — one observable behavior per story; flows grouped in sub-epics.
- **Intent** — outcomes and behaviors, not implementation tasks, tickets, or internal structure spelled out as “stories.”

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Active Business and Behavioral Language

**Scanner:** `scanners/active-business-and-behavioral-language-scanner.py` — **`ActiveBusinessAndBehavioralLanguageScanner`**


Use **active** business language focused on **user/system behavior**: clear action verbs, not technical implementation or passive constructions.

#### DO

- Use **active voice** with business language and **base verb forms** (infinitive/imperative): e.g. `User --> submit order`, `System --> validate payment`, `Customer --> place order`, `Admin --> approve request`.
- Prefer **action verbs** that describe behavior: submit, view, validate, send, display, place, edit, create, load, save, invoke, process, generate, update — as fits the story.
- Prefer **user/system stories** over raw technical tasks. Rephrase technical wording into business behavior (e.g. `System --> store user data` rather than “set up database schema”). When technical work is required, use `story_type: technical` and keep it minimal.
- When technical stories are necessary, mark with **`story_type: technical`** and keep them focused.
- When the domain has its own vocabulary (financial instruments, medical protocols, logistics terms, regulatory language), use the domain's terms in story names instead of inventing generic application language.

  **Example (pass):** `(S) Operator --> Settle Transaction` — "Settle" and "Transaction" are the domain's terms for this action on this entity.

#### DON'T

- **Passive or vague:** not “Order is submitted” — use `User --> submit order`. Not “Payment gets validated” — use `System --> validate payment`.
- **Implementation/task language** as the main story: avoid “write code”, “create class”, “set up CI/CD”, “configure database” as the behavior — express **business outcome** instead where possible.
- **Development-task verbs** for primary stories: implement feature, create module, refactor code, fix bug, build system — unless framed as real behavioral outcomes with `story_type` as appropriate.
- Invent generic application language when the source material provides precise domain terms.

  **Example (fail):** `(S) Operator --> Complete Money Transfer` when the domain calls this action "Settle Transaction" — the generic name obscures what the story actually does and makes the map harder to validate against source material.

### Rule: Analyze before grouping

**Scanner:** Manual review

Before writing stories for a domain with multiple entity types (instrument types, account types, fulfilment methods, power types, notification channels, shipping methods), read the source description of **each** type and list: (a) what the user configures, (b) what the system validates or resolves, (c) what runtime lifecycle it has. Group stories by that analysis — not by category label, source heading, or shared name.

#### DO

- For each entity type under a shared heading, document a brief **configuration / validation / lifecycle** summary before deciding whether to consolidate or split.

  **Example (pass):** Five "shipping methods" appear under one heading. Before writing stories the agent lists: ground (zone-based rate tables), overnight (cutoff-time validation + carrier API booking), LTL freight (freight-class calculation + BOL generation), ocean container (container-type selection + customs declaration), white-glove (scheduling windows + assembly instructions). The map shows five stories:

  ```
  (E) Configure Shipping Methods
      (S) Shipper --> Configure Zone-Based Ground Rates
      (S) Shipper --> Configure Overnight Cutoff and Carrier Booking
      (S) Shipper --> Calculate LTL Freight Class and Generate BOL
      (S) Shipper --> Select Ocean Container Type and File Customs Declaration
      (S) Shipper --> Schedule White-Glove Delivery Window
  ```

- When the analysis reveals identical workflows, consolidate per *Consolidate Superficial Stories*.

  **Example (pass):** Ground and economy-ground share the same zone-rate lookup and carrier selection — one parameterized story:

  ```
  (S) Shipper --> Configure Zone-Based Ground Rates (ground, economy-ground)
  ```

#### DO NOT

- Group entities into one story because they share a heading or category name in the source.

  **Example (fail):** Seven control effects appear under "Control" in the source. The agent writes one story:

  ```
  (S) Player --> Configure Control Effect (choose: create/move object/summon/environment/transform/element control/illusion)
  ```

  But Create makes objects with Toughness, Move Object uses telekinetic Strength for opposed checks, Summon creates controllable entities with their own sheets, Transform has narrow/broad/any scope affecting cost, and Illusion requires selecting which sense types are fooled. The heading groups them; the mechanics don't.

- Skip the analysis step and group by intuition or label similarity.

  **Example (fail):** Five defense effects appear under "Defense." The agent writes:

  ```
  (S) Player --> Configure Defense Effect (choose: protection/immunity/force field/deflect/regeneration)
  ```

  But Immunity has a cost catalogue (1–80 ranks), Deflect is a combat reaction, Protection is permanent, Force Field is sustained (can be knocked offline), and Regeneration has a rate-based recovery schedule — five different configuration workflows behind one label.

- Assume a generic "configure + set level" story covers an entity type whose configuration changes other derived attributes.

  **Example (fail):** Four employment types appear under "Employment." The agent writes:

  ```
  (S) HR --> Set Employment Type (full-time, contractor, seasonal, intern)
  ```

  But full-time triggers benefit-eligibility cascades (health, dental, 401k vesting), contractor triggers a different tax-withholding path (1099 vs W-2) and disables PTO accrual, and seasonal has fixed-term end-date logic with auto-termination. The generic story hides three different downstream configuration cascades. After analysis:

  ```
  (E) Onboard by Employment Type
      (S) HR --> Enroll Full-Time Benefits and Verify I-9
      (S) HR --> File Contractor W-9 and Link SOW
      (S) HR --> Set Seasonal End Date and Auto-Termination
      (S) HR --> Verify Intern University Agreement and Provision Time-Limited Access
  ```

**Source:** Engagement corrections log — entries 2, 3, 4, 5.

### Rule: Consolidate Superficial Stories

**Scanner:** Manual review (policy; pairs with *Review and Expand Stories* — see below)


Consolidate stories that differ **only superficially** (same logic, different data values or enumeration). Combine into **one parameterized story** where it applies.

**Relationship to other rules:** This rule removes **data-value duplication** (same behavior, different inputs). *Review and Expand Stories* splits by **component behavior**. Apply **consolidation first**, then expansion if you still need component-level depth.

#### DO

- Merge stories that share the same validation logic but differ only by the value validated (e.g. six ability scores → one **`Assign Ability (STR, DEX, …)`** story).
- Merge stories that share the same calculation but differ only by attribute (e.g. multiple “calculate X modifier” → **`Calculate Ability Modifiers`**).
- Merge the same operation across entity types when only the type differs (e.g. create character / weapon / armor → **`Create Game Entity (types…)`**).

#### DON'T

- Enumerate every permutation when logic is identical and only data changes — use one parameterized story (e.g. one **`Validate Input Format`** for email, phone, postal code).
- Split by data value when business rules are the same (e.g. separate add-book / add-electronics / add-clothing → **`Add Product`**).
- One story per status when the **workflow pattern** is the same — prefer one **`Update Order Status`** story with allowed values.
- Consolidate without leaving a trail. Parenthetical hints like `(type A, type B, type C)` inside story text are insufficient for downstream work — the AC author needs to know which variants have different validation, parameters, or outcomes.

  **Example (fail):** The story map contains only:

  ```
  (S) HR --> Onboard New Hire (full-time, contractor, intern)
  ```

  The parenthetical hint is all that remains. But full-time requires benefits enrollment + I-9 verification, contractor requires W-9 + SOW linkage + rate-card approval, and intern requires university-agreement check + duration-limited access provisioning. No Consolidation Notes document these differences — the AC author has no idea what to specify per variant.

#### Consolidation Notes requirement

When consolidating stories, add a **`## Consolidation Notes (for AC phase)`** section at the end of the story map listing: (a) each consolidation, (b) which source mechanics it groups, (c) what the AC phase must specify per variant.

**Example (pass):** The story map ends with:

```
## Consolidation Notes (for AC phase)

### Onboard New Hire (full-time, contractor, intern)
Groups three onboarding workflows into one parameterized story.
AC must specify per variant:
- Full-time: benefits enrollment (health, dental, 401k), I-9 verification
- Contractor: W-9 filing, SOW linkage, rate-card approval
- Intern: university-agreement check, duration-limited access provisioning

### Choose Attack Trade-Off (accurate, all-out, defensive, power)
Groups four attack modifiers that share the same "apply modifier to hit/effect" pattern.
AC must specify per variant:
- Accurate: bonus to hit, no effect change
- All-out: bonus to hit, penalty to active defenses
- Defensive: penalty to hit, bonus to active defenses
- Power: penalty to hit, bonus to effect
```

### Rule: Context gaps are genuinely missing information

**Scanner:** Manual review

Every entry in the **Context Gaps** section of `story-map.md` / `story-map.txt` states information that is **genuinely unavailable** — a business decision not yet made, a stakeholder perspective not yet gathered, or a technical constraint not yet known. The gap names what is unknown, what options exist, and what depends on the answer. Failure is a gap that the source material already answers, a gap that parks unfinished analysis, a gap outside the product scope, or a gap that questions a decision the user already stated.

#### DO

- Before writing a gap, check: "Does the source material answer this?" If yes, finish the analysis — it is unfinished work, not a gap.

  **Example (pass):** Gap: "Settlement currency for cross-border wires — source material covers domestic wires only; need to confirm whether the platform supports multi-currency settlement or converts at initiation." The source genuinely does not answer this.

- Write each gap in plain stakeholder language: what is unknown, what options exist, what depends on the answer.

  **Example (pass):** Gap: "Chargeback handling — two options: (a) platform manages disputes end-to-end, (b) platform routes to external dispute processor. Affects whether we need a dispute resolution epic. Awaiting product owner decision."

- **Verification pass before finalising:** After writing Context Gaps, search the source material for each gap phrase. If the source describes the mechanic, remove the gap and map stories instead.

  **Example (pass):** Draft Context Gaps section included:

  ```
  ## Context Gaps
  - Character advancement: The source describes gaining power points and increasing
    power level between sessions. Is post-session advancement in scope?
  ```

  Verification pass finds the source describes the mechanic in detail. Gap removed; stories mapped instead:

  ```
  (E) Advance Hero
      (S) GM --> Award Power Points after Adventure
      (S) Player --> Spend Earned Power Points on Traits
      (S) System --> Enforce Power Level Limits on Advancement
  ```

#### DO NOT

- Use gaps as a parking lot for analysis you haven't done yet.

  **Example (fail):** Gap: "Transaction rules per account type — not yet mapped." The source material describes IRA contribution limits, margin maintenance calls, and trust beneficiary distributions. This is deferred work, not missing information.

- Flag domain-obvious answers as gaps.

  **Example (fail):** Gap: "Do refund transactions use the same ledger as payments?" when the source material describes a single unified ledger for all transaction types. The answer is in the source — no gap needed.

- Raise concerns outside the product scope unless the user asks.

  **Example (fail):** Gap: "Licensing and redistribution rights for third-party payment network logos." This is legal/business, not product scope.

- Question something the user has already stated as a decision.

  **Example (fail):** Gap: "Should onboarding be self-service or manual?" after the user said "manual onboarding only for now." The user already decided — this is not a gap.

**Scanner heuristic:** Flag gap text containing phrases like "not yet mapped," "is X in scope?," "TBD," or "to be determined" as candidates for false gaps — these phrases often indicate deferred analysis rather than genuinely missing information.

**Source:** Engagement corrections log — root cause B; entry 1.

### Rule: Distinct mechanics have distinct stories

**Scanner:** Manual review

When the source material describes multiple entity types (transaction types, account types, fulfilment methods, inspection types, instrument types), the story map groups them by **distinct mechanical pattern** — entities with identical workflows share one parameterized story; entities with different workflows get separate stories. This holds across all lifecycle phases: configuration/setup, runtime/execution, and observation/reporting. Failure is a single catch-all story covering entity types whose processing, parameters, or outcomes differ fundamentally, or the opposite — separate stories for entity types that share the same workflow.

#### DO

- Compare entity-type mechanics **before** writing stories: for each type, identify what a user configures, what the system validates, and what outcomes are possible. Group by workflow pattern, not by name.

  **Example (pass):** A payments domain has 8 instrument types. The story map shows `(S) Operator --> Initiate Wire Transfer` (correspondent-bank routing), `(S) Operator --> Submit Card Payment` (auth-capture-settle), `(S) Operator --> Submit ACH Batch` (batch windows + return codes) — three stories because three distinct clearing mechanics. Cheque, BPAY, and direct debit share the same batch-and-clear workflow as ACH, so they are handled by the same story with a type parameter, not duplicated.

- Perform the comparison across **all lifecycle phases** so the user never has to say "go deeper."

  **Example (pass):** A retail domain maps fulfilment stories for configuration (subscription has recurring billing setup; drop-ship has vendor onboarding), runtime (subscription has pause/resume; drop-ship has vendor handoff; digital has licence key generation), and reporting (subscription has churn metrics; drop-ship has vendor SLA). Three phases, distinct stories per distinct mechanic in each.

- Entities with different **lifecycles** (permanent vs sustained vs reactive) need separate stories even when they share a category.

  **Example (pass):** A healthcare system has four "patient protections" under one heading. The map separates them by lifecycle:

  ```
  (E) Enforce Patient Protections
      (S) System --> Request Insurance Pre-Authorization before Procedure
      (S) System --> Fire Allergy Alert on Medication Order
      (S) Nurse --> Reassess Infection-Control Isolation Daily
      (S) System --> File Adverse-Event Report to Regulator
  ```

  Pre-authorization is proactive (before procedure), allergy is passive (fires automatically), isolation is sustained (daily reassessment, can be overridden), adverse-event is reactive (post-incident). Four trigger types → four stories.

- When the source lists **5+ sub-types** under one heading, enumerate each sub-type's parameters before deciding whether to consolidate. If more than half have different parameter sets, default to separate stories.

  **Example (pass):** Five "notification channels" appear under one heading. After enumeration the map shows:

  ```
  (E) Configure Notification Channels
      (S) Admin --> Configure Email Provider and Template Builder
      (S) Admin --> Configure SMS Carrier Gateway and Opt-In Compliance
      (S) Admin --> Register Push Notification Device Tokens and Certificates
      (S) Admin --> Define In-App Targeting Rules and Read Receipts
      (S) Admin --> Set Webhook Endpoint URL and Retry Policy
  ```

- When a story describes a **state change** that creates a new actor context (trapped, locked, held, escalated), check whether the source describes a separate resolution mechanic for **exiting** that state. If the exit has a different actor, different action type, or different check, it is a distinct story.

  **Example (pass):** A support-ticket system maps escalation and the exits from that state:

  ```
  (SE) Escalate and Resolve Tickets
      (S) Agent --> Escalate Ticket to Tier 2
      (S) Tier 2 Agent --> Reject Escalation with Reason
      (S) Tier 2 Agent --> Accept Escalation and Reassign
  ```

  Reject and Accept are separate stories — different actor (Tier 2, not Tier 1), different checks (rejection criteria vs reassignment workflow).

- When the source describes a **pipeline** (request → validate → process → respond), map **filtering or short-circuit steps** that fire before the main processing step. Passive filters that prevent processing entirely are distinct stories, not implicit.

  **Example (pass):** An order-fulfilment system maps forward processing plus two pipeline filters:

  ```
  (SE) Process Order
      (S) System --> Screen Order Against Embargo and Sanctions List
      (S) System --> Evaluate Fraud Score Against Threshold
      (S) System --> Validate Order Items
      (S) System --> Charge Payment
      (S) System --> Ship Order
  ```

  Embargo screening and fraud scoring are pre-processing filters with different data sources — not implicit parts of `Validate Order`.

- When an entity type has both a **configuration phase** and a **runtime phase**, check whether it appears in the runtime context even if it was initially categorized under configuration. An entity classified as "setup-only" may have distinct runtime resolution.

  **Example (pass):** A banking system maps account configuration and runtime separately:

  ```
  (E) Open Accounts
      (S) Customer --> Open Savings Account
      (S) Customer --> Open Checking Account
      (S) Customer --> Open Money Market Account

  (E) Process Account Transactions
      (S) System --> Enforce Money Market Monthly Transaction Limit
      (S) System --> Assess Money Market Excess-Transaction Penalty
      (S) System --> Execute Checking Overdraft-Protection Transfer from Savings
  ```

  Money Market and Checking have runtime stories that differ from generic deposit/withdrawal — found by checking whether "setup-only" entities appear at runtime.

- When the domain includes entities that **may or may not** have runtime behaviors, document the analysis in a **Passive vs Active Runtime Analysis** subsection of Consolidation Notes. For each entity type, state whether it is (a) static/configuration-only (no runtime story needed), (b) passively enforced at runtime (system filter — needs a runtime story), or (c) actively triggered at runtime (user action — needs a runtime story).

  **Example (pass):** An insurance platform's Consolidation Notes include:

  ```
  ## Passive vs Active Runtime Analysis
  - Deductible Amount → static (applied as number in claims calc; no runtime story)
  - Coverage Exclusion → passive filter (system checks every claim against list before processing)
    → runtime story: (S) System --> Check Claim Against Coverage Exclusions
  - Rider Benefit → active trigger (policyholder files separate rider claim)
    → runtime story: (S) Policyholder --> File Rider Benefit Claim
  - Premium Discount → static (applied at renewal calculation; no runtime story)
  ```

#### Pitfall

Don't map only the **initiating side** of an interaction. After mapping all "forward" stories in a phase, re-scan the source for **reverse, compensating, defensive, supportive, and observational** actions in the same context — they often have distinct resolution mechanics.

**Example (fail):** An e-commerce platform maps only the forward purchase path:

```
(SE) Checkout
    (S) Customer --> Place Order
    (S) System --> Process Payment
    (S) System --> Reserve Inventory
```

But the source also describes `Issue Refund` (different gateway call), `Cancel Reservation` (releases held inventory, fires restock webhook), and `Apply Store Credit` (different tender type with balance-check logic). Three reverse/compensating actions missed.

**Example (fail):** A combat system maps only offensive attack effects:

```
(SE) Apply Attack Effect
    (S) System --> Apply Damage
    (S) System --> Apply Affliction
    (S) System --> Apply Weaken
    (S) System --> Apply Nullify
```

But the source in the same chapter describes: Healing (standard action, close range, removes conditions from others), Mind Reading (perception range, sustained, Will resistance), Summon (creates controllable entity), Deflect (reaction, substitutes check vs incoming ranged attack). Four non-attack combat effects with distinct resolution paths were missed because the agent only analyzed the offensive side.

#### DO NOT

- Write one generic story for a domain with 10+ entity types without comparing their mechanics.

  **Example (fail):** `(S) Operator --> Process Payment` as the only story for wire, ACH, card, cheque, BPAY, direct debit, real-time, and crypto — when wire requires correspondent-bank routing and card requires auth-capture-settle, the single story hides fundamentally different workflows.

- Assume entity names imply distinct stories when the mechanics are identical.

  **Example (fail):** Separate stories `(S) Operator --> Submit ACH Payment` and `(S) Operator --> Submit Direct Debit Payment` when both use the same batch-and-clear workflow with the same parameters, validations, and outcomes — duplicating without mechanical justification.

- Cover only one lifecycle phase (e.g., configuration) while leaving runtime or reporting as a gap.

  **Example (fail):** A wealth management map has stories for opening 12 account types but the `Context Gaps` section says "Transaction rules per account type — not yet mapped" when the source material describes IRA contribution limits, margin maintenance calls, and trust beneficiary distributions in detail.

**Source:** Engagement corrections log — root cause C; entries 3, 5, 6, 7, 8, 9, 15.

### Rule: Lightweight and Precise

**Scanner:** Manual review

Create **lightweight but precise** documentation during shaping. Focus on structure and scope, not detailed specifications.

#### DO

Make the map easy to walk through — it tells a story. Show hierarchy and flow without detailed specifications.

```
(E) Manage Orders
  (SE) Place Order
    (S) Validate Order Items
  (SE) Review Order
    (S) View Order Summary
    (S) Modify Order Items
```

This shows hierarchy and flow — that is enough at shaping stage.

#### DON'T

Do not add:
- Detailed API specs
- Database schema
- UI mockups
- Validation rules with detail
- Technical implementation notes

Example of over-elaboration (wrong at shaping):
```
(E) Manage Orders
  → Detailed API specs: POST /orders with JSON body {item_id, quantity, customer_id}
  → Database: orders table with FK to customers
  → UI: Modal with item picker and quantity stepper
```

If you have this kind of detail from context, put it in `notes` with a `context_source` citation — not in the story structure itself.

### Rule: Map system and application behaviors

**Scanner:** Manual review

Map system behaviors that actors (human or system) depend on: state persistence and versioning, session lifecycle (start/end with state carry-forward), event logging and audit trail, data synchronization, role-based overrides, and template management for repeatable workflows. These are product behaviors, not implementation details — they belong on the story map when any actor (user **or** system) observes or depends on them.

This rule applies to **every** product — not only interactive or user-facing applications. System-to-system integrations, batch pipelines, and back-office platforms all have persistence, lifecycle, logging, and sync behaviors that are observable by the systems and operators that depend on them.

#### DO

- After mapping domain workflows, add an epic or sub-epic for **application lifecycle behaviors**: persistence and versioning of domain data, event logging and audit trail, session or process start/end with state carry-forward, data sync between components or connected systems, and role-based or privilege-based overrides.

  **Example (pass):** A telemedicine platform maps clinical workflows, then adds application lifecycle stories:

  ```
  (E) Manage Visit Lifecycle
      (SE) Persist Visit Data
          (S) System --> Store Visit Recording with HIPAA Retention Policy
          (S) System --> Version Clinical Notes per Edit
      (SE) Log Clinical Decisions
          (S) System --> Log Clinical Decision to Audit Trail
      (SE) End Visit
          (S) System --> End Visit and Carry Forward Diagnoses to Patient Chart
          (S) System --> Push Real-Time Vitals to Provider Dashboard
  ```

- When actors repeat a workflow with variations, map **template management** behaviors: clone from existing, save as reusable template, load from template, customize clone independently of original.

  **Example (pass):** A restaurant platform maps menu creation, then adds reuse stories:

  ```
  (SE) Manage Menu Templates
      (S) Manager --> Clone Menu for New Season
      (S) Manager --> Save Menu as Reusable Template
      (S) Manager --> Load Menu from Template
      (S) Manager --> Customize Cloned Item Without Affecting Original
  ```

- For system-to-system products, map behaviors that downstream systems depend on: guaranteed delivery, retry/dead-letter handling, schema versioning, health signalling, and contract enforcement.

  **Example (pass):** A payment-gateway integration maps transaction processing, then adds integration-contract stories:

  ```
  (E) Manage Gateway Integration
      (S) System --> Publish Settlement Event to Downstream Ledger
      (S) System --> Route Failed Message to Dead-Letter Queue
      (S) System --> Version API Contract for Consumer Compatibility
      (S) System --> Report Gateway Health Status
  ```

#### DO NOT

- Treat persistence, logging, sync, or session management as "implementation details" that belong only in engineering. If any actor — human or system — will observe versioned data, event history, live updates, or process state, these are product behaviors.

  **Example (fail):** A combat encounter app maps game rules only:

  ```
  (E) Run Combat Encounter
      (SE) Execute Turns
          (S) Player --> Choose Hero Action
          (S) System --> Resolve Attack
          ...
  ```

  No stories for sheet versioning, combat event logging, encounter ending with condition carry-forward, live state sync, or GM condition override. The map covers domain rules but not the system behaviors that host them.

- Omit system-to-system behaviors because "no human sees them." If a downstream system depends on the behavior, it belongs on the map.

  **Example (fail):** An order-fulfilment pipeline maps only the forward path:

  ```
  (E) Fulfil Order
      (S) System --> Validate Order
      (S) System --> Charge Payment
      (S) System --> Ship Order
  ```

  Missing: `(S) System --> Publish Order Event to Warehouse System`, `(S) System --> Retry Failed Warehouse Acknowledgement`, `(S) System --> Reconcile Shipping Confirmation` — three behaviors the warehouse system depends on.

**Source:** Engagement corrections log — entries 10, 11.

### Rule: Outcome-Oriented Language

**Scanner:** `scanners/outcome-oriented-language-scanner.py` — **`OutcomeOrientedLanguageScanner`**

Use **outcome-oriented language** over mechanism-oriented language. Focus on what is created or achieved, not how it is shown or communicated.

**Alignment with other rules:** Outcomes still use **base verb forms** (verb–noun, imperative style after `Actor -->`), matching **Verb–Noun Format** and **Active Business and Behavioral Language**. Do not fix a mechanism title by switching to third person (`provides…`, `displays…`) or gerunds (`Showing…`) in the action phrase.

#### DO

Name concepts by what they **ARE** or **CREATE**. Ask: _What is being created? What does the user get?_ Phrase the story as **`Actor --> verb` + object** (same pattern as **Active Business and Behavioral Language**), not gerund-led or third-person labels.

| Wrong (mechanism / gerund title) | Correct (outcome, base verb) |
|-------------------|-------------------|
| `Visualizing Power Activation` | `System --> display power activation animation` |
| `Showing Combat Results` | `System --> provide combat outcome feedback` |
| `Displaying Hit Information` | `System --> display hit indicators` |
| `Presenting Configuration Options` | `System --> load configuration panel` |
| `Providing Settings` | `System --> load configuration` |

#### DON'T

Avoid generic communication/mechanism verbs that describe *how* something is shown rather than *what* is created:

- `Showing results`
- `Displaying information`
- `Visualizing data`
- `Presenting options`
- `Providing settings`
- `Enabling features`
- `Allowing access`

### Rule: Review and Expand Stories

**Scanner:** Manual review (policy; pairs with *Consolidate Superficial Stories* — see below)


When planning calls for **system stories** or explicit **component interactions**, **decompose** existing stories into those interactions. Story count **will increase**.

**Relationship to other rules:** This rule expands by **component behavior** (different behaviors inside one flow). *Consolidate Superficial Stories* merges **same logic, different data**. Apply **consolidation first**, then **this expansion** where needed.

#### DO

- With System / Technology / Infrastructure emphasis, split user stories into **user action + system/component** stories (e.g. `User --> group tokens`, `System --> create mob`, `System --> assign mob leader`).
- **Review** existing stories and add component steps for payment, validation, inventory, etc., when the approach requires it.
- Break flows into **discrete system steps** when the plan demands (e.g. `validate payment` → `call payment gateway` → `persist transaction` → `confirm payment`).

#### DON'T

- Keep **one** user story when the approach requires visible **component** interactions.
- Assume story count stays fixed after switching to a **finer** system/component approach — expect a larger map.

### Rule: Scale Story Map by Domain

**Scanner:** `scanners/scale-story-map-by-domain-scanner.py` — **`ScaleStoryMapByDomainScanner`**


**Domain first, operation second.** At small scale, related domains can share a sub-epic. As behavior diverges, split into **parallel sub-epics by domain** with **consistent** stories under each. After expanding stories (*review and expand stories*), **organize by domain**, not by technology layer.

#### DO

- At **small** scale, keep related domain objects together when behavior is similar and story count is low.
- As **complexity** grows, break out **by domain** with parallel structure (e.g. wire / ACH / check each with collect → validate → submit, plus domain-specific extras).
- Scale along **domain object** first; **operations** are stories **within** each domain.
- After component-level expansion, place stories under **domain** sub-epics, not under generic tech buckets.

#### DON'T

- Group primarily by **operation** or **technology** at scale (e.g. one “validate all payments” mixing domains; “database operations” as a layer).
- **Over-split** early (many sub-epics for a handful of stories). **Under-specify** sub-epics as bare nouns — keep **verb–noun** flow names where they help (e.g. “Make Wire Payment” not just “Wire Transfer”).

### Rule: Small and Testable

**Scanner:** `scanners/small-and-testable-scanner.py` — **`SmallAndTestableScanner`**

Stories must be **testable as complete interactions** and deliverable independently. Small enough to test, large enough to matter.

#### DO

Each story must:
- Have clear acceptance criteria
- Be testable without parent context
- Represent a complete enough behavior to verify
- Be small enough to test quickly

**STORY vs STEP distinction:**

| Type | Definition | Example |
|------|-----------|---------|
| Story | User/system outcome — testable independently | `User --> save story graph` |
| Step | Implementation detail — part of parent test | `convert format`, `serialize to JSON`, `write file` |

Examples:
- Story: `User --> render diagram` → Steps (not separate stories): `generate XML`, `calculate positions`, `apply styles`

#### DON'T

- Create stories too small to test meaningfully
- Turn implementation steps into stories

Implementation operation patterns that are **steps, not stories**:
- `Serialize`, `deserialize`, `convert`, `transform`, `format`
- `Calculate`, `compute`, `generate` (technical artifacts)
- `Apply`, `set`, `configure` (technical settings)
- `Save`, `write`, `store` (without user context)

Examples of wrong stories:
- ~~`Add order button`~~ (can't test without full order flow)
- ~~`Convert Diagram to StoryGraph Format`~~ (implementation step)
- ~~`Serialize Components to JSON`~~ (not testable alone)
- ~~`Calculate Component Positions`~~ (no user outcome)

### Rule: Source-supported mechanics mapped not listed as deferred gaps

**Scanner:** Manual review

The story map in **`story-map.md`** / **`story-map.txt`** reflects what the **available source material** already explains about workflows, entity types, and system behaviors: those mechanics appear as stories, sub-epics, or brief inline notes—not only as a **Context Gaps** bullet that says "not yet mapped" or equivalent. Failure is a gap or deferred phrase where the source already describes the mechanic in enough detail to break it into behaviors today.

#### DO

- After reading the source, map **mechanics the source already describes** into the tree (split or consolidate per other rules) instead of parking them in **Context Gaps** as unfinished analysis.

  **Example (pass):** The source defines wire vs card clearing (routing vs auth-capture-settle). The map has `(S) Operator --> Initiate Wire Transfer` and `(S) Operator --> Submit Card Payment`; **Context Gaps** has no line "Payment clearing mechanics — not yet mapped."

- Use **Context Gaps** only when information is **actually missing** from source and stakeholders (aligned with **Context gaps are genuinely missing information**).

  **Example (pass):** Source covers domestic wires only. Gap: "Cross-border settlement currency — not specified in source; need product decision."

- When the source describes a **distinct action type** that consumes a resource (time, action, turn, API call, dispatch slot) **differently** from the default action, map it as a separate story even if the actor is the same.

  **Example (pass):** A warehouse system's source describes `Direct Robot to Zone` as a supervisor action consuming a limited "dispatch slot." The map includes it alongside picking:

  ```
  (SE) Execute Warehouse Operations
      (S) Picker --> Pick Item from Bin
      (S) Picker --> Pack Order for Shipment
      (S) Supervisor --> Direct Robot to Zone
      (S) System --> Ship Order
  ```

  `Direct Robot to Zone` is a separate story — different actor (Supervisor, not Picker), different resource (dispatch slot, not pick time), different validation (zone-capacity + robot-availability).

- **Verification pass after drafting:** Re-read each source section's action/command list and confirm every named action appears as a story or is explicitly documented as consolidated into another story.

  **Example (pass):** The source's "Combat Actions" section lists: Attack, Grab, Trip, Disarm, Feint, Demoralize, Command, Escape. After drafting, the agent confirms each named action has a story or a consolidation note. `Command` was missing — added `(S) GM --> Command Minion or Summoned Creature` under Execute Turns.

#### DO NOT

- Record a map-level or inline gap that says an area is "not yet mapped" or "TBD" when the source material already spells out that workflow in enough detail to write stories.

  **Example (fail):** **Context Gaps** includes "Transaction rules per account type — not yet mapped" while the source documents IRA contribution limits, margin maintenance calls, and trust distributions in detail—the stories belong on the map, not as a deferral.

- Treat **Context Gaps** as a staging area for analysis you have not performed on **available** source text.

  **Example (fail):** Ten instrument types appear in the domain spec, but the map has only `(S) Operator --> Process Payment` and a gap listing "Break out instrument-specific flows — later" although the spec already distinguishes wire, card, and ACH mechanics.

- Map only the **named or labeled** actions from the source while ignoring the generic resolution mechanic that underlies them. If the source describes a general-purpose resolution path (e.g., "any skill check," "any API call," "any form submission") that specific named actions are special cases of, the general path needs its own story.

  **Example (fail):** A project-management tool maps only the named review actions:

  ```
  (SE) Review Artifacts
      (S) Reviewer --> Approve Budget
      (S) Reviewer --> Reject Change Request
      (S) Manager --> Escalate Risk
  ```

  But the source also describes a general `Resolve Review` action — any artifact can be submitted for review with a configurable checklist, and the reviewer can approve/reject/request-changes. The general resolution mechanic `(S) Reviewer --> Resolve Review with Checklist` is missing — the named actions are special cases of it.

**Source:** Engagement corrections log — map deferred instead of using available source; entries 12, 13.

### Rule: Story Map from Existing Code

**Scanner:** _(none in JSON — methodological guidance for code-to-map workflows)_


When deriving a story map from **code**, start from **entry points**, derive operations and **goals**, then **epics/sub-epics/stories** — not from class names alone.

#### DO

1. **Entry points** — CLI commands, UI handlers, MCP tools, APIs, acceptance tests.
2. **Operations** — list and group by functional purpose.
3. **Epics from goals** — group operations by higher-order goals (e.g. CLI entry points `render-outline`, `render-increments` → goal **Render StoryGraph** → epic **`Render StoryGraph`**).
4. **Sub-epics from behaviors** — e.g. under **Render StoryGraph** → **`Render Outline`**, **`Render Increments`** (verb–noun, same bar as **Verb–Noun Format**).
5. **Story journey** — trace flow start → middle → end; include when/why/outcome/actor and error paths where relevant.

#### DON'T

- Start from **internal classes** or mirror **class structure** as epics.
- Turn **every method** into a story.
- Omit **context** (when/why/outcome) or elevate **implementation detail** as if it were user-visible behavior.

### Rule: Story map stays within user-requested scope

**Scanner:** Manual review

The epic and story tree in **`story-map.md`** / **`story-map.txt`** reflects **only** the product scope the user (or product owner) has asked for: alternate journeys, build methods, or channels do not appear as parallel first-class flows unless the user asked for them or confirmed they are in scope. Failure is an extra path, persona flow, or "optional" track presented as part of the map when the user explicitly narrowed scope or chose a single path.

#### DO

- When the user states **one** path (e.g. "manual onboarding only", "custom build only"), map **that** path and treat other approaches as out of scope until the user expands scope.

  **Example (pass):** User: "Manual onboarding only for now." The map has sub-epics and stories for staff-led onboarding only; there is no sibling sub-epic "Self-service onboarding" unless the user later adds it.

- When a real choice exists and the user has **not** decided, capture **one** gap naming the decision and options—not two full parallel backlogs.

  **Example (pass):** Gap: "Onboarding: manual vs self-service not decided—no stories for self-service until PO confirms."

#### DO NOT

- Add a **second** major flow (e.g. self-service onboarding, quick-build archetype, alternate sales channel) as if it were in-scope when the user already chose or restricted to the other path.

  **Example (fail):** User said "custom build only, no quick start." The map still includes `(E) Quick-Start From Archetype` with stories—that is unrequested scope.

- Present **unrequested** alternatives as normal epics "for completeness" without asking.

  **Example (fail):** User asked for a B2B wholesale portal map; the map adds a full B2C retail epic "because many platforms have both" without product confirmation.

**Source:** Engagement corrections log — scope fabrication and parallel paths without user ask.

### Rule: Verb–Noun Format

**Scanner:** `scanners/verb-noun-format-scanner.py` — **`VerbNounFormatScanner`**


Use verb–noun format at every level. Document the actor separately (e.g. `story_type`, metadata)—**not** in the name. Prefer **base verb forms** (imperative / infinitive style: `Place Order`, `Select Tokens`), not gerunds (`Placing Order`) or third-person singular (`Places` / `Selects` as the *wrong* pattern when the rule asks for base form—see examples below).

#### DO

- **Format:** `verb` + `noun` [optional qualifiers]. Actor is separate. Use specific objects and context. Focus on what can be *done*, not what things *are*.

| Level | Examples (from rule) |
|--------|----------------------|
| Epic | `Manage Customer Orders`, `Process Online Payments` |
| Sub-Epic | `Place New Order`, `Validate Credit Card Payment` |
| Story (action phrasing) | `Process Order Payment`, `Validate Submitted Payments` — tie to lifecycle: Load → Read → Edit → Render → Synchronize → Search → Save |
| Story (system examples) | `Load Order Data`, `Validate Payment`, `Generate XML` |
| With actor (actor not in name) | `Place Order` (actor: Customer), `Validate Payment` (actor: System), `Update Stock` (actor: Inventory Manager) |
| Base verb form | `Select Tokens`, `Group Minions`, `Process Payment` — not `Selects Tokens`, not `Selecting Tokens` |

#### DON'T

- **Actor in the name:** e.g. not `Customer Places Order` → use `Place Order` and set actor in metadata. Same for `OrderProcessor Validates Payment` → `Validate Payment`; `Cart Adds Product` → `Add Product`.

- **Too generic or noun-only:** e.g. `Process Payment` without context when specificity is needed; `Payment Processing` (noun-only); `Order Management` (capability, not a concrete action); `Selects Tokens` (wrong verb form for this rule → `Select Tokens`).

- **Capability / structure phrasing instead of actions:** e.g. `PaymentValidator Contains Validation Logic`, `Cart Hierarchy Foundation`, `Product Represents Item`.

- **Transforming “capability” into action (examples from rule):** `Contains Logic` → e.g. `Generate XML`, `Render Diagram`; `Tracks Count` → `Read Count`, `Update Count`; `Represents X` → `Create X`, `Load X`.
<!-- execute_rules:bundle_rules:end -->
