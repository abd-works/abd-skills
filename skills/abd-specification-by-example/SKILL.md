---
name: abd-specification-by-example
description: >-
  Teaches specification by example for BDD-style scenarios: Given/When/Then steps,
  Background, Scenario Outline with Examples, {Concept} parameterization, and domain-
  grounded example tables. When building scenarios from sources, output **all** template
  artifacts in `templates/` (currently `specification-by-example.md` and
  `specification-by-example.txt`) with the same coverage. Use when writing Gherkin
  scenarios, story-graph `scenarios` / `scenario_outlines`, example tables, or
  tightening scenario language; optional handoff from exploration acceptance criteria
  (abd-acceptance-criteria) when that artifact exists. Ships Markdown rules and a
  **ScenarioDomainTermEmphasisScanner** under this skill for **execute_rules** (mechanical
  checks alongside human review).
---
# abd-specification-by-example

## Purpose

Describe what good **specification-by-example** scenarios *are* (structure, language, tables, and persistence expectations). **How** to run the Agile Bot, workspace setup, and CLI flows belong in the agent and other skills — not here.

## When to use this skill

Load this skill when **any** of the following apply:

- You are writing or reviewing **Given / When / Then** scenarios (including **Background** and **Scenario Outline**) for stories in **`story-graph.json`** or equivalent.
- You have only a **story title**, **rough notes**, or **general understanding**—not necessarily formal exploration AC—and you want executable **examples** anyway.
- Exploration **acceptance criteria** (WHEN/THEN — `abd-acceptance-criteria`) exist and you want scenarios that **trace** to them (optional path).
- You need **domain-parameterized** steps with **{Concept}** placeholders and matching **example tables**.
- An agent is asked to “write BDD,” “add scenarios,” “outline examples,” or “make scenarios concrete.”
- You are running **execute_rules** scanners against a workspace whose **`story-graph.json`** contains **scenarios** (step strings with optional markdown emphasis).

---

## Agent Instructions

1. **Templates**

Generate content using **every** template file in this skill’s `templates/` folder. **Do not** emit only Markdown or only plain text unless the user **explicitly** asks for a single format.

**Use every template file (required)**

When you **create or rewrite** scenarios from **whatever inputs exist** (AC, notes, conversation, or story text) plus domain context, you **must** deliver **one output artifact per file** in `templates/`.

| Template | What to produce |
| --- | --- |
| `templates/specification-by-example.md` | Story-level **Background** (if warranted), **example tables**, **Scenario** and optional **Scenario Outline** blocks in Gherkin style, using **{Concept}** / **{Concept.property}** with **domain words beside each placeholder** (e.g. `the User {User}`) per rules below. Optional title or short context at the top is fine. **Do not** paste the template’s `## Instructions` section (or equivalent) into generated project files — that material is for skill maintainers. |
| `templates/specification-by-example.txt` | The **same** scenario coverage and semantics as **plain text** only — structure matching the `.txt` template style. |

**Consistency:** Scenario names, Background presence, step semantics, and example-table data must match between `.md` and `.txt` for the same work. Generated artifacts contain **only** scenario content (plus optional brief context in `.md`); heuristics stay in this skill and in `templates/` for reference.

**If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

**Depth:** Stay at scenario / example-table level; do not paste long exploration AC prose unless a one-line pointer or summary helps readers (and skip entirely if AC was never written).

**Quality bar:** Match **Core concepts** and **The shape of good specification-by-example** below, then **Validate** using the bundled rules.

**Relationship:** **`abd-acceptance-criteria`** is for story-level WHEN/THEN AC when you want that layer; **this skill** is for **BDD steps** (**Given** lives here, not inside AC lines). Teams may author **only** scenarios, or AC then scenarios, or scenarios first and backfill AC later—this skill does not require a particular order.

2. **Rules**

- Generate content following the rules attached to this skill (listed below, assembled from **`rules/*.md`**).
- After content exists, act as a *peer reviewer*: walk each rule’s constraints, DO/DON’T sections, and examples; be helpful but critical when comparing the deliverable to each rule.

- **Who is checking:** A **product owner** (coverage vs intent—AC, notes, or story), a **developer/tester** (given/when/then discipline and testability), and a **domain expert** (language and tables) should all agree the scenarios are specific enough to implement and automate.

- **Cross-artifact parity:** The `.md` and `.txt` outputs must match in scenario coverage and data.

3. **Mechanical checks (execute_rules)**

From **`skills/execute_using_rules/`**, with workspace root containing **`docs/story/story-graph.json`** or **`story-graph.json`**:

```text
python skills/execute_using_rules/scripts/run_scanners.py --skill-root skills/abd-specification-by-example --workspace <path-to-project>
```

Scanners live under this skill’s **`scanners/*-scanner.py`**; which scripts run is driven by **`scanner:`** in each rule file’s YAML frontmatter and by discovered **`-scanner.py`** entrypoints (see **`skills/execute_using_rules/SKILL.md`**).

4. **Assembling this skill**

This **`SKILL.md`** is assembled from **`rules/*.md`** into the bundled block below. Use **`bundle_rules_into_skill_md.py`** from **`skills/execute_using_rules/scripts/`** whenever **`rules/*.md`** changes:

---

## What is specification by example?

**Specification by example** (here) means **concrete scenarios** that describe **how** a story behaves using **examples**: preconditions (**Given**), the triggering action (**When**), and observable outcomes (**Then**), with **tables** that ground **{Concept}** placeholders in real domain data.

**Inputs:** Scenarios are often paired with exploration **acceptance criteria** (WHEN/THEN — a concise *what must hold*). That pairing is **useful, not mandatory**. The same scenario quality rules apply when the only inputs are a **story name**, **bullet notes**, or **shared understanding**—you still make behavior explicit in Given/When/Then and tables.

Good scenarios answer:

1. **What world do we start in?** (Background + **Given** — state, not actions.)
2. **What happens?** (**When** — domain-meaningful trigger.)
3. **What do we observe?** (**Then** / **And** — outcomes, including errors.)
4. **Which rows exercise variation?** (Example tables and **Scenario Outline** when the same steps repeat with different data.)

---

## Core concepts

### Given, When, Then (and And)

| Keyword | Role |
| --- | --- |
| **Given** | Preconditions: data and state that exist **before** the behavior. |
| **When** | The action or event under test (often the **first** action in the scenario). |
| **Then** | Observable outcomes to assert. |
| **And** | Continues Given, When, or Then block with another line of the same kind. |

**Background** repeats only **Given**/**And** setup shared by many scenarios; omit it for one-off setup.

### {Concept} and example tables

- **{Concept}** names a domain object; **{Concept.property}** names a salient field.
- Every **{Concept}** in steps should have a **table**; every table should be referenced in steps (bidirectional check).
- In readable specs, **put the domain concept words beside the brace** (e.g. `the User {User}`, `Payment Amount {PaymentAmount}`) so ties to tables are obvious.
- Prefer collaboration language (“holds”, “belongs to”, “validates against”) over stacking placeholders without relations.

### Scenario vs Scenario Outline

- **Scenario:** one path, concrete tables still allowed for Given data.
- **Scenario Outline:** **same** steps, multiple **Examples** rows — formulas, boundaries, instrument variants. Avoid outlines for a single row or for materially different contexts.

### Where scenarios live

When **`story-graph.json`** is authoritative, scenarios belong on **`stories[].scenarios`** (and outlines on **`scenario_outlines`**). Authoring files from this skill should **align** with that model, not introduce a competing unofficial spec tree.

---

## Example (generated shape)

The following illustrates **structure only**; real projects use domain types from their model.

```gherkin
Background:
  Given the User {User} is logged into ChannelOne 2.0
  And the User {User} is entitled to the Entitlement {Entitlement}

Scenario: Wire payment captures amount
  Given the Account {Account} with activation status {Account.activation_status} is selected
  When the User {User} enters a Payment Amount {PaymentAmount}
  Then the Wire Payment {WirePayment} holds the Payment Amount {PaymentAmount}
```

---

## The shape of good specification-by-example

```
Story title + optional pointer to sources (AC, notes, or “tribal knowledge”)
Background (optional, 3+ scenarios)
Example tables per {Concept}
Scenario: ...
 Given the <Concept> {Concept} …  When the <Concept> {Concept} …
  Then the <Concept> {Concept} …
Scenario Outline + Examples (only if warranted)
```

**Bad shape:** UI-click scripts as **Given**; placeholders without tables; **only** `{User}` with no domain words beside it (when your convention is to label braces); only happy paths when failures or edge cases clearly matter; duplicate Background inside every scenario.

---

## Build

**Goal:** Turn **whatever is known about the story** (AC if present, notes, or informed judgment) plus domain language into **both** template artifacts.

- **Outputs:** `specification-by-example.md` and `specification-by-example.txt` with **matching** coverage.
- **Per format:** Markdown uses fenced **gherkin** where helpful; plain text uses indentation and labels per the `.txt` template.
- **While writing:** Name scenarios by **outcome**; keep tables **domain-true**; parameterize with **{Concept}** consistently and **label each placeholder** with domain words in the step (`the User {User}`).
- **Persistence (optional):** If the workspace uses **`story-graph.json`**, map scenarios into `scenarios` / `scenario_outlines` per project conventions; avoid orphan spec files.

---

## Validate

**Goal:** Review as PO + tester + domain expert — not a second full authoring pass.

- **Who is checking:** Same roles as **Agent Instructions**; each validates their lens (coverage, executability, vocabulary).
- **Cross-artifact parity:** `.md` and `.txt` stay in lockstep.

Quick checklist:

- **Given** is state-only; **When** is the first real action; **Then** asserts domain outcomes.
- **{Concept}** ↔ tables **both ways**; no random `<column>` prose; domain words sit beside each `{Concept}` where this skill’s convention applies.
- Happy, edge, and error paths implied by the story, notes, or AC (if any) are **visible** in scenarios or outlines.
- Outlines used only when **variation** is real, not ceremonial.
- **Domain emphasis:** in **Markdown** scenario artifacts, domain-significant terms use *italics* consistently (plain `.txt` stays markdown-free; the graph may still use `*italic*` in step strings if your pipeline stores markdown there — the **ScenarioDomainTermEmphasisScanner** checks scenario name + steps).

Run mechanical scanners via **execute_rules** as described in **Agent Instructions**.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Background vs scenario setup

**Background** is shared **precondition** text for **three or more** scenarios. It contains only **Given** / **And** lines (state), never **When** or **Then**. Steps use **{Concept}** (and **{Concept.property}** when a specific attribute matters) so each placeholder resolves to an example table. **Put the domain concept words beside each placeholder** (e.g. `the User {User}`) in Background and scenarios — see **Mention the domain concept beside the placeholder**. Do not repeat Background lines inside individual scenarios.

#### DO

- Model shared state once in **Background** when many scenarios need the same starting world (e.g. logged-in **User {User}**, **Entitlement {Entitlement}**, **Enterprise {Enterprise}**).
- Use **{Concept.property}** when the scenario hinges on a particular field (e.g. `activation status {Account.activation_status}`).
- Keep Background free of actions; the **first** behavior under test belongs in **When** inside each scenario.

```gherkin
Background:
  Given the User {User} is logged into ChannelOne 2.0
  And the User {User} is entitled to the Entitlement {Entitlement} for the Enterprise {Enterprise}
  And the Enterprise {Enterprise} has wire service enabled
```

#### DON'T

- Put **When** / **Then** in Background, or encode actions as “user logs in” inside Background **Given** lines.
- Hard-code identities or permissions inline when the scenario system expects **{Concept}** + tables (avoid “user is entitled to create wire payments” without **{Entitlement}**).
- Duplicate a Background **Given** inside a scenario’s steps.

```gherkin
# WRONG — action in Background
Background:
  When {User} logs in

# WRONG — repeats Background
Scenario: Pay wire
  Given {User} is logged into ChannelOne 2.0
  When ...
```

### Rule: Emphasize domain-significant terms (scenarios)

**Scanner:** `scanners/emphasize-domain-terms-scenario-scanner.py` — **`ScenarioDomainTermEmphasisScanner`**

Call out **domain language** — the nouns, verbs, and short phrases that belong to the problem space and show up in stories, tests, and talk with stakeholders — so readers see what is *specific* to this product versus generic wording. Apply this to **scenario** prose: **Background** lines, **Given / When / Then** steps, and the **scenario name** when it carries domain meaning (same bar as **abd-acceptance-criteria** emphasis on AC).

#### DO

- Wrap domain-significant terms in *italics* in **markdown** scenario artifacts and in **story-graph** step strings when you use markdown there.
- Use *title-style capitalization* inside those phrases for multi-word concepts (e.g. *Wire Payment*, *Export Job Progress*, *Beneficiary Bank*). Keep acronyms and product names in their normal form (e.g. *PDF*).
- Apply emphasis consistently for the same concept across scenarios on a story.
- Prefer this pattern over **exact** quoted UI copy unless the literal string is required for a contract or compliance check.

#### DON'T

- Italicize filler or purely grammatical words, or entire sentences.
- Use emphasis as decoration on every line — only mark terms that carry domain meaning.
- Replace behavioral clarity with a wall of highlighted words; if everything is emphasized, nothing is.

### Rule: Example tables use domain language

Example tables ground scenarios in **domain** data: column names follow the model, values are concrete and meaningful, and tables connect to steps through **concept names** and collaboration language (e.g. “owned by enterprise”). Prefer **source** rows that explain an outcome over bare counts or flags that hide what was renamed, added, or removed—unless this scenario only **consumes** a result produced upstream.

#### DO

- Name each table after a **domain concept**; columns are **attributes** of that concept, not UI labels.
- Omit implementation-only ID columns when they add no specification value; relate concepts with readable columns and table ordering / collaboration phrasing.
- When the scenario **computes** a report or aggregate, show the **inputs** (renamed rows, new rows) that justify the output—not only `renames_count = 1`.
- Use domain terminology consistent with the model (Recipient, BeneficiaryBank, PaymentAmount—not “dropdown value”).

```text
Recipient (creates() from Enterprise):
| recipient_name | recipient_status |
| Global Supply  | Active           |
```

#### DON'T

- Build tables around UI controls (`button_enabled`, `modal_visible`) when the story is about domain outcomes.
- Use disconnected “lookup” layouts that force readers to mentally join unrelated tables when a parent/child structure is part of the domain.
- Encode only aggregated outputs (`renames_count`, `reflects_additions: true`) for the scenario that is **responsible** for producing those aggregates—show the underlying entities unless the scenario only applies someone else’s report.

```text
# WRONG — UI-ish columns
| dropdown_selection | checkbox_state |

# WRONG — only counts when this scenario builds the report
| renames_count | new_count |
| 1             | 2         |
```

### Rule: Given describes state, not actions

**Given** steps state **what is true before** the behavior under test: preconditions and persisted state. The **first** thing that **happens**—a user gesture, system event, or command—belongs in **When**. **Then** captures observable outcomes (including errors). Do not hide the behavior under test inside **Given**.

#### DO

- Phrase **Given** as state: “**{User}** is logged in”, “**{Character}** exists”, “workflow state is persisted”.
- Move verbs like *clicks*, *invokes*, *submits*, *calls* to **When**.
- When you need prior actions, express the **resulting state**, not the past action (“**{WirePayment}** creation is in progress”, not “user has clicked Continue”).

```gherkin
Given {Agent} is initialized
And {Project} is finished initializing
When {Tool} invokes load_project
Then {Project} loads configuration
```

#### DON'T

- Use **Given** for UI navigation position (“user is on Payment Details step”) when you can state **domain** state (“**{PaymentDetails}** requires **{Account}** selection”).
- Put past-tense **actions** in **Given** (“Tool has invoked method”, “user has clicked”).
- Describe the functionality you are trying to prove inside **Given** instead of **Then**.

```gherkin
# WRONG
Given user clicks Pay
When payment succeeds

# BETTER
Given {Payment} is ready to authorize
When user authorizes {Payment}
Then {Payment} status is Authorized
```

### Rule: Keep scenarios consistent across connected domains

At small scale, one scenario can cover closely related behaviors. As domains grow, prefer **parallel** scenario shapes for parallel concepts (same step count and pattern, different **{Concept}**), diverging only where behavior genuinely differs. That keeps comparisons fair and reviews fast.

#### DO

- Reuse the same **Given / When / Then** skeleton for sibling concepts (e.g. **{WirePayment}** vs **{ACHPayment}**) when the business flow matches.
- Add **extra** scenarios only for real differences (e.g. intermediary bank required for wire only).
- Parameterize with **{Concept}** and tables instead of copy-pasting eight steps with only the product name changed.

```gherkin
# Wire
Given {WirePayment} has {Recipient}
When {WirePayment} is submitted
Then {WirePayment} is routed to the wire rail

# ACH — parallel structure
Given {ACHPayment} has {Recipient}
When {ACHPayment} is submitted
Then {ACHPayment} is routed to the ACH rail
```

#### DON'T

- Give one rail a six-step specification and a sibling rail a three-step soup for the “same” operation without justification.
- Fork scenarios by duplicating hard-coded values instead of shared structure + **{Concept}** tables.

### Rule: Map table columns to scenario parameters

Every **{Concept}** in Background and scenario steps must have a matching **example table**, and every example table must appear as **{Concept}** (or **{Concept.property}**) in the steps. In prose, put the **domain concept name beside** each placeholder (e.g. `the Entitlement {Entitlement}`) so the tie to the table is obvious in human-readable specs — see **Mention the domain concept beside the placeholder**. Verification columns belong in **Then** via **{Concept.property}** or explicit domain outcomes—keep **Given** tables aligned with preconditions only.

#### DO

- Work **both directions**: step placeholder ↔ table name ↔ columns ↔ readable label next to the brace.
- Use **{Concept.property}** when a column is specifically asserted (e.g. `{Recipient.status}` is Active).
- Keep tables **minimal**: only concepts and attributes the scenario actually needs.

```gherkin
Given the User {User} is entitled to the Entitlement {Entitlement}
```

```text
User:
| user_name | user_role     |
| Jane Doe  | Wire Operator |

Entitlement:
| entitlement_name   | entitlement_status |
| WirePayment.Create | Granted              |
```

#### DON'T

- Use angle-bracket **`<column_name>`** placeholders in prose instead of **{Concept}**.
- Leave **orphan** tables (no **{Concept}** in steps) or **{Concept}** placeholders with no table.
- Dump raw column names into a step without tying them to a concept (“User `<user_name>`”).

```gherkin
# WRONG
Given User <user_name> is logged in

# CORRECT
Given the User {User} is logged in
```

### Rule: Mention the domain concept beside the placeholder

In **Background** and **scenario** steps, put the **readable domain concept name** (the word or phrase stakeholders use) **next to** each **`{Concept}`** or **`{Concept.property}`** placeholder. Readers should see *what* the brace refers to without decoding braces alone; the placeholder still ties the line to the **example table** for that concept.

#### DO

- Use a short English cue before or after the brace: e.g. `the User {User}`, `the Entitlement {Entitlement}`, `the Enterprise {Enterprise}`, `activation status {Account.activation_status}`, `Payment Amount {PaymentAmount}`.
- Keep **one** `{Concept}` per table-backed object in that clause; the prose name should match the **table title** / domain type (singular or phrasing your team uses consistently).
- Apply the same pattern in **Background** (Given/And only) and in **scenario** steps (Given/When/Then/And).

```gherkin
Background:
  Given the User {User} is logged into ChannelOne 2.0
  And the User {User} is entitled to the Entitlement {Entitlement} for the Enterprise {Enterprise}
  And the Enterprise {Enterprise} has wire service enabled

Scenario: Wire capture
  Given the Account {Account} with activation status {Account.activation_status} is selected
  When the User {User} enters a Payment Amount {PaymentAmount}
  Then the Wire Payment {WirePayment} holds the Payment Amount {PaymentAmount}
```

#### DON'T

- Use **only** `{User}` with no surrounding domain words — unless your pipeline forbids extra words (default: prefer the paired pattern above).
- Repeat the brace twice in a clumsy way (`{User} User …`) — use **one** natural phrase: `the User {User}` or `User {User}`, not both duplicated back-to-back.
- Replace `{Concept}` with **only** the English name and drop the placeholder — you still need the brace for table mapping unless your tool explicitly uses another convention.

### Rule: Scenario language matches the domain

**Given / When / Then** lines should read like the team’s domain model: entities, value objects, and collaborations. Avoid UI implementation detail unless the story is explicitly about a literal label or widget. Pick the concept that **owns** the data in context (e.g. **Epic** in **StoryMap**, not a diagram cell type, unless the step is about rendering that cell).

#### DO

- Name entities the way the domain does (“**WirePayment** is created with status pending”).
- Use **When** for domain operations (“**User** selects **Recipient**”), not low-level driver events.
- Use **Then** for domain-visible effects and messages users or integrators care about.

```gherkin
Given an Enterprise with active Recipients
And a User with wire payment permissions
When the User selects a Recipient
Then the WirePayment is created with status pending
```

#### DON'T

- Anchor **Given** in pages, modals, or control names (“recipient list page is loaded”) when state can be said in domain terms.
- Use generic placeholders (“items”, “thing”) when real types exist.
- Misplace concepts: if something lives in **StoryMap**, say **{Epic}** / **{SubEpic}** there; reserve diagram-specific types for steps about the diagram.

```gherkin
# WRONG — UI-first
When the user clicks the dropdown

# STRONGER — domain
When the User selects a Recipient
```

### Rule: Scenarios cover all cases implied by the story

A solid story has **happy path** scenarios plus **edge** and **error** cases that trace to **whatever specifies behavior**: formal acceptance criteria, story text, notes, or agreed rules. If validation, persistence, or error handling matters, scenarios should show those outcomes explicitly—not assume “we’ll handle errors somewhere.”

#### DO

- Include at least one **success** path with realistic data.
- Add **boundary** or rule-adjacent cases when limits, optional fields, or transitions are stated (in AC, notes, or the story).
- Add **failure** paths with the observable error or prevention behavior (message, status, no persistence), using concrete example values.

```gherkin
Scenario: Valid payment amount is accepted
  When {User} enters {PaymentAmount}
  Then {WirePayment} holds {PaymentAmount}

Scenario: Negative amount is rejected
  When {User} enters {PaymentAmount}
  Then submission is blocked
  And {WirePayment} is not created
```

#### DON'T

- Ship only “everything works” scenarios when negatives or edge rules are known from any source.
- Describe errors abstractly (“invalid data”) without the concrete violating example the table supplies.

### Rule: Scenarios belong in the story graph (canonical persistence)

When the team uses **`story-graph.json`** as the system of record, add scenarios to **`stories[].scenarios`** and scenario outlines to **`stories[].scenario_outlines`**. Do not spin up parallel “feature specification” documents or ad-hoc `docs/.../scenarios.md` collections that compete with the graph—**this skill’s** `specification-by-example.md` / `.txt` artifacts are **authoring** outputs that should align with or feed the same structure, not a second source of truth.

#### DO

- Treat epics → features → stories → **scenarios** as the stable hierarchy in JSON when the bot or pipeline expects it.
- Keep scenario names stable enough to link to tests or automation IDs where your process requires it.

#### DON'T

- Create standalone markdown specs whose scenarios are not reflected in **`story-graph.json`** when that file is authoritative for the workspace.
- Fork the same scenario under multiple unofficial paths (harder diffing, drift).

```text
OK: story-graph.json → epics[].…stories[].scenarios[]
Avoid: docs/story/Epic/Feature/Feature Specification.md as the only home for scenarios
```

### Rule: Use scenario outline when the story needs data variation

Use a **Scenario Outline** with **Examples** when the **same** steps apply across multiple rows: calculations, fee tables, boundary sweeps, or named entity variations. Prefer separate **Scenario**s when setups differ materially, business meaning diverges, or you only have **one** row.

#### DO

- Outline **formula-like** or **table-driven** behavior (inputs → outputs) with a concise Examples block.
- Keep placeholders in steps consistent with Examples column headers.

```gherkin
Scenario Outline: Modifier depends on rank
  Given ability rank <rank>
  When modifier is calculated
  Then modifier is <modifier>

  Examples:
    | rank | modifier |
    | 10   | 0        |
    | 12   | +1       |
```

#### DON'T

- Wrap a single concrete path in an outline with one Examples row—use a normal **Scenario**.
- Use outlines when scenarios need different **Given** contexts that are clearer as separate scenarios.

```gherkin
# WRONG — outline adds noise for one row
Scenario Outline: User saves profile
  Examples:
    | name |
    | Jane |
```

### Rule: Write concrete, parameterized scenarios

Steps should read as **examples**, not abstracts: use **{Concept}** for domain objects and **{Concept.property}** for salient attributes. **Mention the domain concept in prose beside each placeholder** (e.g. `the User {User}`) so steps read naturally and still map to tables — see **Mention the domain concept beside the placeholder**. Every placeholder must appear in an **example table**; tables use domain column names. Work **backward** from the outcome to the base data the world needs (enterprise, user, entitlements, accounts). Relate concepts with collaboration language (“the **Wire Payment {WirePayment}** holds the **Payment Amount {PaymentAmount}**”), not jammed placeholders.

#### DO

- Replace vague actors with **{User}**, **{Enterprise}**, **{PaymentAmount}**, each backed by a table, and label each brace with the matching domain term in the same step.
- Trace dependencies: e.g. payment needs account, account needs enterprise, user needs entitlements—show those tables.
- Prefer domain collaboration verbs from the model (holds, belongs to, validates against).

```gherkin
Given the User {User} is logged into ChannelOne 2.0
And the User {User} is entitled to the Entitlement {Entitlement}
When the User {User} enters a Payment Amount {PaymentAmount}
Then the Wire Payment {WirePayment} holds the Payment Amount {PaymentAmount}
```

```text
PaymentAmount:
| amount   | currency | formatted_display |
| 10000.00 | USD      | $10,000.00        |
```

#### DON'T

- Hard-code literals in steps when the scenario system expects **{Concept}** + tables (“User Jane Doe…” without a **User** table).
- Invent generic placeholders (`<the_user>`, `{some_value}`) instead of type names from the domain.
- Stuff two unrelated placeholders next to each other without an English relation (“**{Enterprise}** **{User}** is logged in”).
- Describe **UI state** as **Given** when **data state** suffices (“on Payment Details step” vs “**{PaymentDetails}** awaits **{Account}**”).
- Use calculated fields (counts only) to stand in for the **records** that produce them when this scenario is the one doing the calculation.

```gherkin
# WRONG — no parameterization / tables
Given user enters $10,000.00

# BETTER
Given the User {User} enters a Payment Amount {PaymentAmount}
```
<!-- execute_rules:bundle_rules:end -->
