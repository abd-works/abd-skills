---
name: abd-specification-by-example
description: >-
  Produce specification-by-example scenarios: concrete Given/When/Then steps with real
  domain values, bold concept names, italic values. Two templates: plain scenarios
  (inline values, default) and outline (same steps, multiple data rows). Use when
  writing BDD scenarios, refining AC into specs, or making story behavior concrete.
---
# abd-specification-by-example

## Purpose

Write **Given/When/Then** scenarios that make a story's expected behavior concrete and testable, using real domain values and named outcomes so the team can verify what the system must do.

## When to use this skill

Load this skill when **any** of the following apply:

- You want to specify system behavior in response to user / system initiated actions for specific stories. 
- You want multiple concrete scenarios including preconditions - *Given*, triggers - *When*, and results - *Then*, made real through one or more *Examples*
- You want want to refine exploration AC (`abd-acceptance-criteria`) into specifications.
- An agent is asked to “write BDD,” “add scenarios,” specify examples,” or “make scenarios concrete.”
---

## Agent Instructions

### 1. Scenarios vs Scenario Outlines

If the user/agent has not specified which approach they want, then 
1. try to determine the based on the nature of the requirements,Would requirements be more specific if there are multiple data scenariosor is only one sufficient?
2. check with the user at slash agent based on the approach chosen and get confirmation, explain your reasoning

**Scenarios**
Each scenario has its own distinct context. All values are written inline — real names, amounts, and statuses directly in the step text. **Domain Concept** *value*. No tables, no `{placeholder}` tokens.
Use for: main flow, failure path, edge cases — any scenario where the context or setup differs. Use the `specification-by-example.md` + `.txt` templates.

**Scenario Outlines**
The same Given/When/Then steps run against multiple rows of data (boundary amounts, multiple instruments, different roles). Steps use `{column_name}` tokens bound to an **Examples** block. **Domain Concept** *{column_name}*.
Use only when the steps are genuinely identical across every row. If rows need different **Given** setup, write separate plain scenarios instead. Use the `specification-by-example-outline.md` + `.txt` templates.

When you **create or rewrite** scenarios from whatever inputs exist (AC, notes, conversation, or story text), choose the right template first  — then regenerate. Scenario names, Background presence, and step semantics must match between .md and .txt. 

Generated artifacts contain only scenario content; instructions stay in the templates for maintainers.
If you find yourself writing the same steps three or more times with only values changing, then switch to  **Scenario Outlines**.

### 2. Writing scenarios

- Use **Background** when three or more scenarios share identical starting state. Given and And only; no When or Then.
- Name each scenario by its **outcome**, not its action.
- Cover at least one happy path, one failure or rejection, and any edge cases the story implies.
- If *Acceptance Criteria* exist, use the main-flow set of *Acceptance Criteria* as your spine: convert WHEN → When, THEN → Then, add Given preconditions and examples. Remaining *Acceptance Criteria* become additional *scenarios*.
- Stay at scenario level; do not paste long AC prose unless a one-line pointer helps.


### 3. Rules
- Generate content following the rules attached to this skill (listed below, assembled from **`rules/*.md`**).
- After content exists, act as a *peer reviewer*: walk each rule’s constraints, DO/DON’T sections, and examples; be helpful but critical when comparing the deliverable to each rule.

- **Who is checking:** A **product owner** (coverage vs intent—AC, notes, or story), a **developer/tester** (given/when/then discipline and testability), and a **domain expert** (language and tables) should all agree the scenarios are specific enough to implement and automate.

### 4. Assembling this skill

This `SKILL.md` bundles `rules/*.md` into the block below. Run `bundle_rules_into_skill_md.py` from `skills/execute_using_rules/scripts/` whenever any rule file changes.

This **`SKILL.md`** is assembled from **`rules/*.md`** into the bundled block below. Use **`bundle_rules_into_skill_md.py`** from **`skills/execute_using_rules/scripts/`** whenever **`rules/*.md`** changes:

---

## What is specification by example?

**Specification by example** is a practice where we create specifications for stories through **concrete scenarios** demonstrated through **examples**. Spec scenarios include preconditions (**Given**), the triggering action (**When**), and an observable outcome (**Then**).

**Inputs:** Scenarios are often created from **acceptance criteria** (WHEN/THEN statements in a story). This is useful, not mandatory. When AC exist, start from the main-flow AC, add Given steps until the flow is concrete, then add scenarios for failures, edges, and alternate flows. The same quality rules apply when the only inputs are a story name, bullet notes, or shared understanding.

---

## Core concepts

### Given, When, Then (and And)

- **Given** — preconditions: data and state that exist before the behavior. Use Background for setup shared by three or more scenarios.
- **When** — the action or event under test (the first action in the scenario).
- **Then** — observable outcomes to assert.
- **And** — continues a Given, When, or Then block with another line of the same kind.

### Formatting convention

In .md artifacts, use **bold** for domain concept names and *italics* for their actual values — for example **User** *Jane Doe*, **Enterprise** *Acme Corp*, **Payment Amount** *,000.00 USD*. In .txt artifacts, use ALL-CAPS for concept names and plain text for values.

### Working from acceptance criteria

If the story has AC (WHEN/THEN from bd-acceptance-criteria), use the main-flow AC as the spine: convert WHEN to When, THEN/AND to Then/And, then add Given preconditions to make it runnable. Remaining AC become additional scenarios (failures, edges, alternate flows). The mapping is rarely one-to-one, but readers should see the relationship.

### Scenarios vs Scenario Outlines

- **Scenario** (plain) — one path, all values inline. Use for distinct flows: happy path, rejection, edge case.
- **Scenario Outline** (parameterized) — same steps, varying data rows. Values use *{column_name}* tokens bound to an **Examples** block. Use only when variation is real and the steps are genuinely identical.

### Background

Use Background only when three or more scenarios share identical starting state. Given and And only — no When or Then.

---


Quick checklist:

- **Given** is state-only; **When** is the first real action; **Then** asserts domain outcomes.
- **{Concept}** ↔ tables **both ways**; no random `<column>` prose; domain words sit beside each `{Concept}` where this skill’s convention applies.
- Happy, edge, and error paths implied by the story, notes, or AC (if any) are **visible** in scenarios or outlines.
- Outlines used only when **variation** is real, not ceremonial.
- **Domain emphasis:** in **Markdown** scenario artifacts, domain-significant terms use *italics* consistently (plain `.txt` stays markdown-free; the graph may still use `*italic*` in step strings if your pipeline stores markdown there — the **ScenarioDomainTermEmphasisScanner** checks scenario name + steps).


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
  Given a User {user_name} is logged into ChannelOne 2.0
  And that User {user_name} is representing an Enterprise {enterprise_name} with the Role {user_role}
  And that Enterprise {enterprise_name} has {payment_service} Payment Service enabled
  And that User has an Entitlement {entitlement_name} with an Entitlement Status of {entitlement_status}
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

Every placeholder in steps must resolve to example data: either **`{column_name}`** (header on the table under the right domain concept), **`{Concept}`** (a row from the table titled for that concept), or **`{Concept.property}`** when you name both the concept row and a specific column. In prose, put readable domain words beside each placeholder (see **Mention the domain concept beside the placeholder**). Work **both directions**: no orphan columns, no unused tables.

**Document order:** If **`{column_name}`** appears only in **Background** or scenario **Given** (including **And** that extend **Given**), put that table **immediately above** that block. If a placeholder is **not** in **Given** but first appears in **When**, **Then**, or **And** after **When**, put its table **immediately below** that scenario’s last step so the story reads first, then the rows that bind the action and outcomes. **Scenario Outline** **Examples** (and any matching concept table) stay with the outline. You may group all precondition tables in one block above **Background** when everything feeds **Given**.

#### DO

- Work **both directions**: step placeholder ↔ table name ↔ columns ↔ readable label next to the brace.
- Use **{Concept.property}** when a column is specifically asserted (e.g. `{Recipient.status}` is Active).
- Keep tables **minimal**: only concepts and attributes the scenario actually needs.

```gherkin
Given that User has an Entitlement {entitlement_name} with an Entitlement Status of {entitlement_status}
```

```text
User:
| user_name | user_role |
| Jane Doe | Wire Operator |

Entitlement:
| entitlement_name | entitlement_status |
| WirePayment.Create | Granted |
```

#### DON'T

- Use angle-bracket **`<column_name>`** placeholders in prose instead of **{Concept}**.
- Leave **orphan** tables (no **{Concept}** in steps) or **{Concept}** placeholders with no table.
- Dump angle-bracket placeholders into prose instead of `{column_name}` headers that exist on your concept tables (“User `<user_name>`” with no matching column).

```gherkin
# WRONG
Given User <user_name> is logged in

# CORRECT
Given a User {user_name} is logged in
```

### Rule: Mention the domain concept beside the placeholder

In **Background** and **scenario** steps, put the **readable domain concept name** (the word or phrase stakeholders use) **next to** each placeholder. That may be **`{column_name}`** (header on a concept table), **`{Concept}`** (whole row), or **`{Concept.property}`** when your convention uses dotted fields. Readers should see *what* the brace refers to without decoding braces alone.

#### DO

- Use a short English cue before or after the brace: e.g. `a User {user_name}`, `account name {account_name}`, `activation status {activation_status}`, `amount {amount}`, `Transactional Limit {limit_name}`.
- Keep one clear domain object per clause; prose should match the **table title** or field you mean (singular phrasing your team uses consistently).
- Apply the same pattern in **Background** (Given/And only) and in **scenario** steps (Given/When/Then/And).

```gherkin
Background:
  Given a User {user_name} is logged into ChannelOne 2.0
  And that User {user_name} is representing an Enterprise {enterprise_name} with the Role {user_role}
  And that Enterprise {enterprise_name} has {payment_service} Payment Service enabled
  And that User has an Entitlement {entitlement_name} with an Entitlement Status of {entitlement_status}

Scenario: Wire capture
  Given an Account with account name {account_name} and activation status {activation_status} is selected
  When the User {user_name} enters a Payment Amount with amount {amount} and currency {currency}
  Then Wire Payment outcome has status {status}
  And payment amount with amount {amount} and currency {currency} is validated against transactional limit {limit_name}
```

#### DON'T

- Use **only** `{user_name}` (or any bare brace) with no surrounding domain words — unless your pipeline forbids extra words (default: prefer `the User {user_name}` or similar).
- Repeat the brace twice in a clumsy way (`{user_name} User …`) — one natural phrase.
- Replace placeholders with **only** English paraphrase and drop the brace — you still need the brace for table mapping unless your tool uses another convention.

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

Steps should read as **examples**, not abstracts. Use **`{column_name}`** placeholders that match **example table headers** under each domain concept, or **`{Concept}`** / **`{Concept.property}`** when your team uses whole-row or dotted-field style. **Mention the domain concept in prose beside each placeholder** — see **Mention the domain concept beside the placeholder**. Every placeholder must appear in an **example table**. Work **backward** from the outcome to the base data the world needs (enterprise, user, entitlements, accounts). Use collaboration language (“validates against”, “holds”, “belongs to”), not jammed placeholders.

#### DO

- Replace vague actors and amounts with table-backed fields: e.g. `{user_name}`, `{account_name}`, `{amount}`, `{limit_name}`, each column present on the right concept table.
- Trace dependencies: payment needs account, account needs enterprise, user needs entitlements—show those tables.
- Prefer domain collaboration verbs from the model (holds, belongs to, validates against).

```gherkin
Given an Account with account name {account_name} and activation status {activation_status} is selected
When the User {user_name} enters a Payment Amount with amount {amount} and currency {currency}
Then Wire Payment outcome has status {status}
And payment amount with amount {amount} and currency {currency} is validated against transactional limit {limit_name}
```

```text
PaymentAmount:
| amount   | currency | formatted_display |
| 10000.00 | USD      | $10,000.00        |
```

#### DON'T

- Hard-code literals in steps when the scenario system expects tables (“User Jane Doe…” without a **User** table).
- Invent generic placeholders (`<the_user>`, `{some_value}`) instead of **column headers** from your tables.
- Stuff two unrelated placeholders next to each other without an English relation (“**{enterprise_name}** **{user_name}** is logged in”).
- Describe **UI state** as **Given** when **data state** suffices (“on Payment Details step” vs “**{PaymentDetails}** awaits **{Account}**”).
- Use calculated fields (counts only) to stand in for the **records** that produce them when this scenario is the one doing the calculation.

```gherkin
# WRONG — no parameterization / tables
Given user enters $10,000.00

# BETTER
When the User {user_name} enters a Payment Amount with amount {amount} and currency {currency}
```
<!-- execute_rules:bundle_rules:end -->
