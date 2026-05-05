---
name: abd-specification-by-example
catalog_garden_tier: practice
catalog_garden_order: 40
catalogue_one_liner: >-
  Given/When/Then scenarios with real domain values; plain or outline (data tables) templates.
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

### 0. Ground in the domain model

Before writing any scenario steps, check whether any of the following types of domain model content exist in the workspace or have been provided as context:

- **Object model** — typed classes with attributes and typed relationships between classes. The most precise source: use it first.
- **CRC model** — each concept listed with its responsibilities and the other concepts it works with. Use when no object model is available.
- **Domain language or key abstractions** — a glossary, list of defined terms, or grouped concept names with definitions. Use as the fallback when no structural model exists.

These types of content are the outputs of domain-driven design practices. Look for object model content first, then CRC, then domain language.

**If domain content exists (grounded mode):**
- Use exact concept names from that source — do not paraphrase, abbreviate, or rename.
- Reflect relationships in Given/And step structure: if the model shows **Customer** uses **Account**, that relationship should appear explicitly in a Given or And step, not just as two disconnected nouns.
- The example tables in Scenario Outlines should expose the relational chain across concept columns — they do the exact same job as connected step language, but in data form. A table column set of `customer_name | dda_account_number | payment_product_name` reads the domain structure; `customer_name | account_status` in isolation does not.

**If no domain content exists (derived mode):**
- Derive concept names and relationships from the story narrative and any acceptance criteria.
- Make relationships deliberate in step language — how bold concept names appear relative to each other in a step is the implied domain model. Do not flatten this to a list of unrelated nouns.

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

This `SKILL.md` bundles `rules/*.md` into the block below. Run `bundle_rules_into_skill_md.py` from `skills/execute-skill-using-skills-rules/scripts/` whenever any rule file changes.

This **`SKILL.md`** is assembled from **`rules/*.md`** into the bundled block below. Use **`bundle_rules_into_skill_md.py`** from **`skills/execute-skill-using-skills-rules/scripts/`** whenever **`rules/*.md`** changes:

---

## What is specification by example?

**Specification by example** is a practice where we create specifications for stories through **concrete scenarios** demonstrated through **examples**. Spec scenarios include preconditions (**Given**), the triggering action (**When**), and an observable outcome (**Then**).

**Inputs:** Scenarios are often created from **acceptance criteria** (WHEN/THEN statements in a story). This is useful, not mandatory. When AC exist, start from the main-flow AC, add Given steps until the flow is concrete, then add scenarios for failures, edges, and alternate flows. The same quality rules apply when the only inputs are a story name, bullet notes, or shared understanding.


**Living documentation:** Specifications by example are not throwaway analysis artifacts. They become **executable requirements** — testable without translation — captured in **live documentation** that stays current as the system evolves. The scenarios you write here are direct inputs to automated tests.

**Multiple perspectives, not solo work.** When writing specifications, ensure the available context covers multiple perspectives: business logic, technical constraints, and testing concerns. If context from a key perspective is missing (e.g. no technical input on system-to-system behaviour, or no business rules for edge cases), flag it as an unknown rather than inventing plausible-sounding scenarios. Specifications written from a single viewpoint produce gaps that surface late.
---

## Core concepts

### Given, When, Then (and And)

- **Given** — preconditions: data and state that exist before the behavior. Use Background for setup shared by three or more scenarios.
- **When** — an action or event under test. A scenario may have **multiple** When/Then beats when the behaviour is a sequence of interactions (e.g. user acts, system responds, user checks result). Each new When starts the next beat.
- **Then** — observable outcomes to assert after the preceding When.
- **And** — continues a Given, When, or Then block with another line of the same kind. Use And for additional outcomes within the **same** beat. Start a new **When** when the actor or trigger changes — do not chain unrelated actions with And.

### Formatting convention

In .md artifacts, use **bold** for domain concept names and *italics* for their actual values — for example **User** *Jane Doe*, **Enterprise** *Acme Corp*, **Payment Amount** *,000.00 USD*. In .txt artifacts, use ALL-CAPS for concept names and plain text for values.

### Working from acceptance criteria

If the story has AC (WHEN/THEN from bd-acceptance-criteria), use the main-flow AC as the spine: convert WHEN to When, THEN/AND to Then/And, then add Given preconditions to make it runnable. Remaining AC become additional scenarios (failures, edges, alternate flows). The mapping is rarely one-to-one, but readers should see the relationship.

### Scenarios vs Scenario Outlines

- **Scenario** (plain) — one path, all values inline. Use for distinct flows: happy path, rejection, edge case.
- **Scenario Outline** (parameterized) — same steps, varying data rows. Values use *{column_name}* tokens bound to an **Examples** block. Use only when variation is real and the steps are genuinely identical.

### Background

Use Background only when three or more scenarios share identical starting state. Given and And only — no When or Then.

### Domain concept grounding

Specification by example works at two levels simultaneously: it specifies *behavior* and it confirms *the domain model*. The Given/When/Then steps are where both happen at once.

When domain model content — an object model, CRC model, or domain language glossary — is available, the scenarios are its behavioral proof. Concept names must match exactly. The relationships the model defines should be visible in step structure through connected language: *a Customer with a valid DDA Account applying for a Payment Product Agreement using an Owner with Contact Details* expresses three concepts and four relationships in one scenario — not a list of unrelated nouns.

When no domain model exists, the scenarios themselves reveal the model. The deliberate way a step names a concept and connects it to another — **Customer** *Jane Doe* applies using **DDA Account** *DDA-001* naming **Owner** *John Doe* — documents the model for the team.

**This is exactly the same job the example tables do in Scenario Outlines.** A table column set of `customer_name | dda_account_number | payment_product_name` grounds the data in the domain relational structure. Tables that show only one concept's fields in isolation lose the relationships that make the domain model legible — a car, a driver, and three passengers tells you nothing about who is driving whom.

### Specification level

The default level for specification by example is the **story** — each story gets its own scenarios. But specifications can be written at **any level** of the story map when it adds clarity:

- **Epic or sub-epic level** — a specification that describes the end-to-end flow across its child stories. This is useful for verifying that the children compose into a coherent journey, and for giving stakeholders a feature-level view of “done.”
- **Story level** (default) — the standard: scenarios for one discrete behaviour.
- **Cross-story** — when a scenario naturally spans multiple stories in sequence (e.g. an integration flow), write it at the parent sub-epic and reference the child stories it exercises.

Higher-level specifications help answer the question: “when these stories are all done, is the feature actually complete?” They do not replace story-level scenarios but complement them.


```gherkin
# Epic-level: Manage Customer Orders
Scenario: Customer places and tracks a new order
  Given a Customer with an active account
  When the Customer adds items to the cart and submits the order
  Then the order is confirmed with a tracking number
  When the Customer views the active orders for their account
  Then that order is displayed along with any other active orders
  And the status for that order is displayed as Processing
  When the order is dispatched
  Then the Customer receives a shipment notification
  And the order status changes to Shipped
```

---


Quick checklist:

- **Given** is state-only; **When** is an action or trigger; **Then** asserts outcomes. Multiple **When/Then** beats are fine for multi-step journeys.
- **{Concept}** ↔ tables **both ways**; no random `<column>` prose; domain words sit beside each `{Concept}` where this skill’s convention applies.
- Happy, edge, and error paths implied by the story, notes, or AC (if any) are **visible** in scenarios or outlines.
- Outlines used only when **variation** is real, not ceremonial.
- **Domain emphasis:** in **Markdown** scenario artifacts, domain-significant terms use *italics* consistently (plain `.txt` stays markdown-free; the graph may still use `*italic*` in step strings if your pipeline stores markdown there — the **ScenarioDomainTermEmphasisScanner** checks scenario name + steps).


---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Background vs scenario setup

**Background** contains only **Given** / **And** lines (state), never **When** or **Then**. Use it only when three or more scenarios share the same starting state. Do not repeat Background lines inside individual scenarios.

In a **plain scenario** (`specification-by-example.md`), Background steps use real values inline with **bold** concept names and *italic* values.

In an **outline scenario** (`specification-by-example-outline.md`), Background steps use `{column_name}` tokens with the domain concept name beside each brace.

#### DO

- Model shared state once in Background when many scenarios need the same starting world.
- Keep Background free of actions; the first behavior under test belongs in **When** inside each scenario.

Plain example:
``Background:
  Given a **User** *Jane Doe* is logged into ChannelOne 2.0
  And that **User** *Jane Doe* is representing **Enterprise** *Acme Corp* with **Role** *Wire Operator*
``
Outline example:
``Background:
  Given a User {user_name} is logged into ChannelOne 2.0
  And that User {user_name} is representing an Enterprise {enterprise_name} with the Role {user_role}
``
#### DON'T

- Put **When** / **Then** in Background, or encode actions inside **Given** lines.
- Duplicate a Background **Given** inside a scenario's own steps.

``# WRONG — action in Background
Background:
  When user logs in

### WRONG — repeats Background
Scenario: Pay wire
  Given user is logged into ChannelOne 2.0
  When ...
``

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

### Rule: Example tables use domain language (outline template)

This rule applies to **`specification-by-example-outline.md`** — scenarios that use example tables. It does not apply to plain scenarios, which use inline values instead.

Example tables ground an outline in domain data: column names follow the domain model, values are concrete and meaningful, and tables connect to steps through the matching `{column_name}` tokens.

#### DO

- Name each table after a domain concept; columns are attributes of that concept, not UI labels.
- Use domain terminology consistent with the model (Recipient, PaymentAmount — not "dropdown value").
- Omit surrogate ID columns when they add no specification value.
- When the scenario computes a report or aggregate, show the inputs that justify the output — not just counts.

```text
Recipient:
| recipient_name | recipient_status |
| Global Supply  | Active           |
``
## DON'T

- Build tables around UI controls (`button_enabled`, `modal_visible`) when the story is about domain outcomes.
- Encode only aggregated outputs (`renames_count: 1`) for the scenario responsible for producing that aggregate — show the underlying entities.

```text
### WRONG — UI columns
| dropdown_selection | checkbox_state |

### WRONG — only counts when this scenario builds the report
| renames_count | new_count |
| 1             | 2         |
``

### Rule: Given describes state, not actions

**Given** steps state what is true **before** the behavior under test: preconditions and persisted state. Things that **happen** — user gestures, system events, commands — belong in **When**. **Then** captures observable outcomes (including errors). A scenario may contain multiple **When/Then** beats for multi-step journeys; each When starts a new action. Do not hide behavior under test inside **Given**.

#### DO

- Phrase **Given** as state: the **User** is logged in, the **Account** is active, the **Entitlement** is granted.
- Move verbs like *clicks*, *invokes*, *submits* to **When**.
- When you need prior actions, express the **resulting state**, not the past action.

Plain example:
``Given the **User** *Jane Doe* is logged into ChannelOne 2.0
  And **Account** *Acme Operating* is *Active*
When the **User** *Jane Doe* submits a **Wire Payment**
Then the **Wire Payment** is marked as *successful*
``
#### DON'T

- Use **Given** for UI navigation ("user is on Payment Details step") when you can state domain state.
- Put past-tense actions in **Given** ("user has clicked Continue").
- Describe the functionality you are trying to prove inside **Given** instead of **Then**.

``# WRONG
Given user clicks Pay
When payment succeeds

### BETTER
Given the **Wire Payment** is ready to authorize
When the **User** authorizes the **Wire Payment**
Then the **Wire Payment** status is *Authorized*
``

### Rule: Ground scenarios in domain model content when available

When object model, CRC, or domain language content exists in the workspace or has been provided as context, scenario language must use the exact concept names and relationships that content defines.

Look in this order — use the first type you find:
1. **Object model** — typed classes with attributes and typed relationships between classes (most precise source)
2. **CRC model** — each concept with its responsibilities and the other concepts it works with
3. **Domain language or key abstractions** — glossaries, defined terms, or grouped concept names with definitions

These types of content are the outputs of domain-driven design practices. If such content is present in the workspace or supplied as context, it is the authoritative source for concept names and relationships.

#### DO

- Read any available domain model content before naming any concept in a step — object model first, then CRC, then domain language.
- Use the exact term the model defines.

```gherkin
Given a **Payment Product Agreement** {agreement_id} agreed to by **Customer** {customer_id}
    using **Account** {account_id}
    naming **Owner** {owner_id}
      with **Contact Details** {owner_email}
```

#### DON'T

- Use a synonym or informal shorthand for a concept the domain model has formally named.
- Rename or paraphrase concept names even when the formal name feels long or unfamiliar.

```gherkin
Given a **Contract** {agreement_id} for **Customer** {customer_id}
    using **Bank Account** {account_id}
    naming **Holder** {owner_id}
      with **Info** {owner_email}
```

---

#### DO

- In Scenario Outlines, structure example tables using the same language and cardinality as the domain model — a one-to-many relationship in the model means a separate table with a linking key, not repeated columns; a joining concept in the model means its own table with references to what it joins.

CRC model the scenario is grounded in:

```markdown
#### **User**
user id                             | (identifier)
user name                           | (string)
payment role                        | Payment Role
contact details                     | Contact Details
direct deposit account              | DDA Account

#### **Payment Role**
role type                           | (Customer, Owner)

#### **DDA Account**
account id                          | (identifier)
user                                | User

#### **Payment Product**
product id                          | (identifier)
product name                        | (string)
payment channel                     | Payment Channel

#### **Contact Details**
user                                | User
email                               | (string)

#### **Payment Product Agreement**
agreement id                        | (identifier)
customer                            | User
account                             | DDA Account
payment product                     | Payment Product
owner                               | User
application status                  | (Submitted, Approved, Rejected)
apply                               | User, DDA Account, Payment Product
```

Scenario Outline steps that trace the relational chain, with a normalized table per concept:

```gherkin
Given a **User** {customer_id} {customer_name} with **Payment Role** *Customer*
  And a **DDA Account** {account_id} for **User** {customer_id}
  And **Payment Product** {product_id} {product_name} is available
When the **User** {customer_id} applies for a **Payment Product Agreement** {agreement_id}
    with **DDA Account** {account_id} and **Payment Product** {product_id}
    naming **User** {owner_id} as **Owner**
Then **Payment Product Agreement** {agreement_id} has application status *Submitted*
  And **User** {owner_id} is notified at {owner_email}
```

```text
### User:
| user_id | user_name | payment_role |
| USR-001 | Jane Doe  | Customer     |
| USR-002 | John Doe  | Owner        |
| USR-003 | Bob Smith | Customer     |
| USR-004 | Alice Lee | Owner        |

### DDA Account: with User
| account_id | user_id |
| DDA-001    | USR-001 |
| DDA-002    | USR-003 |

### Payment Product:
| product_id | product_name     |
| PROD-001   | Savings Plus     |
| PROD-002   | Premium Checking |

### Contact Details: with User
| user_id | owner_email    |
| USR-002 | john@acme.com  |
| USR-004 | alice@corp.com |

### Payment Product Agreement: with User (Customer), DDA Account, Payment Product, and User (Owner)
| agreement_id | customer_id | account_id | product_id | owner_id | application_status |
| AGR-001      | USR-001     | DDA-001    | PROD-001   | USR-002  | Submitted          |
| AGR-002      | USR-003     | DDA-002    | PROD-002   | USR-004  | Submitted          |
```

#### DON'T

- Denormalize by repeating names across tables instead of linking through IDs — this hides ownership and breaks when a Customer has more than one Account or an Agreement covers more than one Product.

```gherkin
Given a **Customer** {customer_name} applies for a **Payment Product Agreement**
    with **Payment Product** {product_name}
Then the agreement is submitted
```

```text
| customer_name | account_number | product_name     | owner_name | owner_email   |
| Jane Doe      | DDA-001        | Savings Plus     | John Doe   | john@acme.com |
```

### Rule: Keep scenarios consistent across connected domains

At small scale, one scenario can cover closely related behaviors. As domains grow, prefer **parallel** scenario shapes for parallel concepts (same step count and pattern, different **{Concept}**), diverging only where behavior genuinely differs. That keeps comparisons fair and reviews fast.

#### DO

- Reuse the same **Given / When / Then** skeleton for sibling concepts (e.g. **{WirePayment}** vs **{ACHPayment}**) when the business flow matches.
- Add **extra** scenarios only for real differences (e.g. intermediary bank required for wire only).
- Parameterize with **{Concept}** and tables instead of copy-pasting eight steps with only the product name changed.

``# Wire
Given {WirePayment} has {Recipient}
When {WirePayment} is submitted
Then {WirePayment} is routed to the wire rail

### ACH — parallel structure
Given {ACHPayment} has {Recipient}
When {ACHPayment} is submitted
Then {ACHPayment} is routed to the ACH rail
``
#### DON'T

- Give one rail a six-step specification and a sibling rail a three-step soup for the “same” operation without justification.
- Fork scenarios by duplicating hard-coded values instead of shared structure + **{Concept}** tables.

### Rule: Map table columns to scenario parameters (outline template)

This rule applies to stories that use *Scenario Outlines* eg: that use `{column_name}` tokens and example tables. It does not apply to plain *Scenarios*, which use inline values instead.

Every `{column_name}` in steps must resolve to a column header on the matching concept table. Every column on a table must appear in at least one step. Work both directions — no orphan columns, no unused tables.

**Document order:** Tables whose columns appear in **Given** go immediately above that Background or scenario block. Tables whose columns first appear in **When** or **Then** go immediately below that scenario.

#### DO

- Match `{token}` spelling exactly to the table column header.
- Keep tables minimal — only the columns the scenario actually references.

```gherkin
Given a User {user_name} has Entitlement {entitlement_name} with status {entitlement_status}
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

- Leave orphan tables (columns never referenced in steps) or `{tokens}` with no matching table.
- Use `<angle_bracket>` placeholders in step prose — use `{column_name}` for outline steps.

```gherkin
# WRONG
Given User <user_name> is logged in

# CORRECT (outline)
Given a User {user_name} is logged in
```

### Rule: Mention the domain concept beside the placeholder (outline template)

This rule applies to **`specification-by-example-outline.md`** — scenarios that use `{column_name}` tokens. In plain scenarios, the concept name is written in **bold** and the value in *italics* directly in the step; no token is needed.

In outline steps, put the readable domain concept name next to each `{token}` so readers can follow the step without decoding braces alone.

#### DO

- Use a short English cue before or after the brace: e.g. `a User {user_name}`, `activation status {activation_status}`, `Payment Amount of {amount} {currency}`.
- Apply the same pattern in Background (Given/And) and in scenario steps.

``Background:
  Given a User {user_name} is logged into ChannelOne 2.0
  And that User {user_name} is representing an Enterprise {enterprise_name} with the Role {user_role}
  And that Enterprise {enterprise_name} has {payment_service} Payment Service enabled
  And that User has an Entitlement {entitlement_name} with an Entitlement Status of {entitlement_status}

Scenario: Wire capture
  Given an Account with account name {account_name} and activation status {activation_status} is selected
  When the User {user_name} enters a Payment Amount with amount {amount} and currency {currency}
  Then Wire Payment outcome has status {status}
``
#### DON'T

- Use a bare `{token}` with no surrounding domain words — prefer `the User {user_name}`.
- Repeat the brace twice (`{user_name} User …`) — one natural phrase is enough.

### Rule: Prefer key examples over exhaustive enumeration

A specification that illustrates well with **a few key examples** is more useful than one that specifies a hundred examples poorly. List only the **key representative examples** — enough to show the pattern and catch the important boundaries. Too many examples overwhelm readers (developers cannot see the forest for the trees) and slow down test execution.

#### DO

- Pick examples that **illustrate the rule**, not every permutation of it.
- Cover happy path, one or two boundaries, and the key failure — enough that the pattern is unambiguous.
- Use a **Scenario Outline** with a focused Examples table when you need breadth, rather than writing dozens of near-identical plain scenarios.

#### DON'T

- Enumerate every data permutation when the underlying rule is the same — three rows that prove the formula beat thirty that restate it.
- Write exhaustive scenarios "just in case" — if you cannot articulate what a new row proves that existing rows do not, it is noise.

### Rule: Scenario language matches the domain

**Given / When / Then** lines should read like the team’s domain model: entities, value objects, and collaborations. Avoid UI implementation detail unless the story is explicitly about a literal label or widget. Pick the concept that **owns** the data in context (e.g. **Epic** in **StoryMap**, not a diagram cell type, unless the step is about rendering that cell).

#### DO

- Name entities the way the domain does (“**WirePayment** is created with status pending”).
- Use **When** for domain operations (“**User** selects **Recipient**”), not low-level driver events.
- Use **Then** for domain-visible effects and messages users or integrators care about.

``Given an Enterprise with active Recipients
And a User with wire payment permissions
When the User selects a Recipient
Then the WirePayment is created with status pending
``
#### DON'T

- Anchor **Given** in pages, modals, or control names (“recipient list page is loaded”) when state can be said in domain terms.
- Use generic placeholders (“items”, “thing”) when real types exist.
- Misplace concepts: if something lives in **StoryMap**, say **{Epic}** / **{SubEpic}** there; reserve diagram-specific types for steps about the diagram.

``# WRONG — UI-first
When the user clicks the dropdown

### STRONGER — domain
When the User selects a Recipient
``

### Rule: Scenarios cover all cases implied by the story

A solid story has at least one **happy path** scenario plus **edge** and **error** cases that trace to formal acceptance criteria, story text, notes, or agreed rules. If validation, persistence, or error handling matters, scenarios should show those outcomes explicitly — not assume "we'll handle errors somewhere."

#### DO

- Include at least one success path with realistic data.
- Add boundary or rule-adjacent cases when limits, optional fields, or transitions are stated.
- Add failure paths with the observable error or prevention behavior (message, status, no persistence).

Plain scenario examples:
``Scenario: Valid payment amount is accepted
  When the **User** *Jane Doe* enters a **Payment Amount** of *$10,000.00 USD*
  Then the **Wire Payment** is marked as *successful*

Scenario: Amount over limit is rejected
  When the **User** *Jane Doe* enters a **Payment Amount** of *$500,000.01 USD*
  Then the **Wire Payment** is *rejected*
  And no **Wire Payment** record is created
``
#### DON'T

- Ship only "everything works" scenarios when failures or edge cases are known.
- Describe errors abstractly ("invalid data") without the concrete violating example.

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
``

### Rule: Use real data over invented examples

Concrete examples should use **real or realistic domain data**, not abstract placeholders or made-up values. Invented examples hide inconsistencies that surface when real data arrives — teams that invent examples "assumed they could do certain things and left it out of examples; when the data from real systems came in, there were always too many surprises."

#### DO

- Use real customer names, product codes, amounts, and dates from the domain wherever possible.
- When real data is sensitive, create realistic synthetic data that preserves the structure and edge characteristics of production data (lengths, formats, special characters).
- On data-driven projects, pull sample rows from actual source systems rather than inventing them.

#### DON'T

- Use abstract entities like "customer A" or "order 123" when a concrete example would expose ambiguity (does the format include leading zeros? is the name unicode-safe?).
- Assume consistency in legacy data — invented examples based on expected rules will miss the inconsistencies that real data contains.
- Use yes/no answers in examples without separately illustrating the underlying concept.

### Rule: Use scenario outline when the story needs data variation

Use a **Scenario Outline** with **Examples** when the **same** steps apply across multiple rows: calculations, fee tables, boundary sweeps, or named entity variations. Prefer separate **Scenario**s when setups differ materially, business meaning diverges, or you only have **one** row.

#### DO

- Outline **formula-like** or **table-driven** behavior (inputs → outputs) with a concise Examples block.
- Keep placeholders in steps consistent with Examples column headers.

``Scenario Outline: Modifier depends on rank
  Given ability rank <rank>
  When modifier is calculated
  Then modifier is <modifier>

  Examples:
    | rank | modifier |
    | 10   | 0        |
    | 12   | +1       |
``
#### DON'T

- Wrap a single concrete path in an outline with one Examples row—use a normal **Scenario**.
- Use outlines when scenarios need different **Given** contexts that are clearer as separate scenarios.

``# WRONG — outline adds noise for one row
Scenario Outline: User saves profile
  Examples:
    | name |
    | Jane |
``

### Rule: Write concrete scenarios with real values

Steps should read as **specific examples**, not abstractions. The approach depends on which template you are using.

**Scenarios (`specification-by-example.md`):** Write all values inline in the step text — real names, amounts, statuses. Use **bold** for domain concept names and *italic* for their values. No tables, no `{placeholder}` tokens.

Given **Account** *Acme Operating* owned by **Enterprise** *Acme Corp* with **Activation Status** *Active* is selected
  And the **Transactional Limit** *daily_wire* is *$500,000.00 USD*
When the **User** *Jane Doe* enters a **Payment Amount** of *$10,000.00 USD*
Then the **Wire Payment** is marked as *successful*


**Outline Scenarios (`specification-by-example-outline.md`):** Use `{column_name}` tokens that match example table headers, with readable domain words beside each placeholder. Every `{token}` must appear in an example table column; every table column must appear in a step. Tables for **Given** go above the scenario; tables for **When** / **Then** go below.


Given an **Account** with account name {account_name} and **Activation Status** {activation_status} is selected
  And the **Transactional Limit** for that Account is {max_amount} {currency}
When the **User** {user_name} enters a **Payment Amount** of {amount} {currency}
Then the **Wire Payment** is marked as {validation_status}
And a **Report** is sent showing {formatted_display}


Account (Given — above scenario):
| enterprise_name | account_name   | activation_status |
| Acme Corp       | Acme Operating | Active            |

TransactionalLimit (Given — above scenario):
| limit_name | max_amount | currency |
| daily_wire | 500000.00  | USD      |

WirePayment (Then — below scenario):
| amount    | currency | formatted_display | validation_status |
| 10000.00  | USD      | $10,000.00        | successful        |
| 500000.01 | USD      | $500,000.01       | rejected          |

#### DO

- For plain scenarios: use real values directly in steps — domain concept **bold**, values *italic*.
- For outlines: name `{tokens}` after the domain field and keep the readable concept name beside the brace.
- Trace dependencies: payment needs account, account needs enterprise, user needs entitlements.
- Use collaboration language ("validates against", "owned by", "marked as"), not jammed placeholders.

#### DON'T

- Mix approaches: don't use `{column_name}` tokens in a plain scenario or hard-code values in every row of an outline.
- Use generic placeholders (`<the_user>`, `{some_value}`) instead of real names (plain) or domain field names (outline).
- Describe **UI state** as **Given** when domain state suffices ("on Payment Details step" vs **Payment Details** awaits *Account* selection).
<!-- execute_rules:bundle_rules:end -->
