---
name: abd-story-mapping
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

## Steps

1. **Build** using **every** template file in this skill's `templates/` folder, and the `rules/` mentioned in this skill.
2. **Validate** using rules mentioned in this skill. For the **mechanical** scanner pass, use the **execute_rules** skill (same repo): run **`run_scanners.py`** with **`--skill-root`** = this skill directory and **`--workspace`** = the tree that contains **`docs/story/story-graph.json`** (or **`story-graph.json`**). To **list** which scanners would run, use **`rule_inventory.py --list-scanners`** with the same **`--skill-root`**. Full intent (AI/rules pass **plus** scanner pass) and exact commands are in **`skills/execute_using_rules/SKILL.md`** (Commands **§2** and **§3**). Implementation details and parity with **agile_bots** live in `scanners/README.md`. **Which** scanners run is defined only by **`rules/*.md`** (`scanner:` frontmatter → `scanners/<stem>-scanner.py`), not a separate manifest. **Story graph** types (`StoryMap`, `StoryScanner`, …) live in **`skills/story-graph-ops/scripts/`** (`story_map.py`, `story_scanner.py`, …); generic scanner types come from **`execute_using_rules`** **`scanner_bases`**. **`scanner_runner`** (execute_rules) drives every scanner CLI the same way (context holds files and/or graph JSON). For **CLI** read/search/filter/write on `story-graph.json` without the bot, use **`skills/story-graph-ops/`** (**story-graph-ops** skill).

### Use every template file (required)

When you **create or rewrite** a story map from requirements, you **must** deliver **one output artifact per file** in `templates/`. **Do not** emit only Markdown or only plain text unless the user **explicitly** asks for a single format.

| Template | What to produce |
| --- | --- |
| `templates/story-map.md` | The epic/sub-epic/story tree using that layout; include the **`## Instructions`** block from that template file at the end of the Markdown artifact (or equivalent rules summary). Optional title/context above the tree is fine. |
| `templates/story-map.txt` | The **same** hierarchy and semantics as **plain text** only — tree lines matching `story-map.txt` style (no requirement to duplicate the Instructions section in `.txt`). |

**Consistency:** Connectors (`or`, `opt`), nested `(AC)` lines, and actor/story lines must match between `.md` and `.txt` for the same map. Only the Markdown file carries the Instructions block.

**If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

**Purpose:** Describe what a good story map *is* (concepts and naming). **How** to run the bot, workspace setup, and step-by-step CLI belong in the agent and other skills — not here.

**Includes:** `templates/` — see **Use every template file** above.

---

## When to use this skill

Load this skill when **any** of the following apply:

- You need to capture goals, decompose user journeys, or capture a solution as a set of user–system interactions (stories grouped into epics).
- A user or agent wants to restructure sources of context (eg: requirements docs, interviews, a product brief, or even a rough description) into a new or existing story map.
- An agent is asked to "map out the system", "identify the epics", "structure the work", or "figure out what we're building using stories"
- You want to organize existing code, solutions, or tests into a hierarchical story-map format
---

## What is a story map?

A **story map** is a visual, hierarchical model of how users and systems interact with a product or service. It was popularized by Jeff Patton and is central to Agile by Design's approach to discovery.

A story map answers three questions:
1. **Who** uses the system? (Actors)
2. **What** are the major capability areas? (Top Level Epics)
3. **How** do users move through those areas, step by step? (Lower Level Epics and Stories)

Story maps are intentionally **not implementation plans**. They describe *outcomes and behaviors*, not tasks, tickets, or technical steps, although they can be used to describe system to system interactions and complex system behaviors. A good story map can be understood by a product owner, a developer, and a domain expert — all at once.

---

## Core concepts

### Actors

An **actor** is anyone (or anything) that interacts with the system. Actors are the *who* behind every story.

| Actor type | Description | Examples |
|---|---|---|
| **User** | A human who uses the system directly | Customer, Administrator, Agent |
| **System** | An external system or automated process | Payment gateway, Email service, Scheduler |

Actors do NOT appear in story names — they are captured in the `story_type` field and optionally in `notes`. The name describes the *behavior*, not who does it.

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

## The shape of a good story map

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

## Build

Produce **both** **`story-map.md`** and **`story-map.txt`** artifacts (same content tree), following **`templates/story-map.md`** and **`templates/story-map.txt`** respectively. See **Steps → Use every template file** — delivering a single format is incorrect unless the user explicitly requested only one. Match the bar under **Validate** below. Structure follows **epics → sub-epics → stories** as above; keep discovery to hierarchy and ordering unless a later workflow adds acceptance criteria or scenarios.

---

## Validate

Review **both** the **`.md`** and **`.txt`** for:

- **Hierarchy** — epics → sub-epics → stories; **verb–noun** names; actors only in `story_type`, not in titles.
- **Story size** — one observable behavior per story; flows grouped in sub-epics.
- **Intent** — outcomes and behaviors, not implementation tasks, tickets, or internal structure spelled out as “stories.”

Revise until a product owner, a developer, and a domain expert can all read the map and agree on what it says.

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

#### DON'T

- **Passive or vague:** not “Order is submitted” — use `User --> submit order`. Not “Payment gets validated” — use `System --> validate payment`.
- **Implementation/task language** as the main story: avoid “write code”, “create class”, “set up CI/CD”, “configure database” as the behavior — express **business outcome** instead where possible.
- **Development-task verbs** for primary stories: implement feature, create module, refactor code, fix bug, build system — unless framed as real behavioral outcomes with `story_type` as appropriate.

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
