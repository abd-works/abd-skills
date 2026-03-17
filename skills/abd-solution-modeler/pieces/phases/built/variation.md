# Critical Quality Steps

**These steps MUST be followed for every AI phase. No exceptions.**

---

## Step 0 — Deep Scan of Evidence and Conceptual Guidance (REQUIRED FIRST)

Before generating any output, you MUST:

1. **Do a deep scan of the evidence** — Read all files in `evidence/` (terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json, evidence_graph.json). Understand every concept, every action, every decision, every state.
2. **Do a deep examination of the conceptual guidance** — Read `concept_guidance.md` and `concept_guidance.json`. Examine ALL concepts. Understand the nuance at a very detailed level.
3. **Verify understanding** — Before writing, confirm you can articulate: What are the key mechanisms? What are the subtypes and their distinct data/behavior? What variations exist? What constraints apply?

Do not proceed to generation until you have done this deep scan. Shallow or partial understanding produces shallow, broken models.

---

## Three-Stage Process (MUST follow for every AI step)

Each AI phase uses three validation layers. All three are required.

**Layer 1 — Generate with rules.** Phase spec + accumulated rules are included in the generation instructions. Follow DO/DO NOT guidance while producing output. Rules are guidance — produce natural output that complies.

**Layer 2 — Scan.** After generation, run `pipeline.py scan <phase>`. Scanners check structural violations mechanically (naming, child counts, concept sync, property types). Fix reported violations before proceeding.

**Layer 3 — Validate.** After scanners, run `pipeline.py validate <phase>`. This prints all applicable rules. AI re-reads generated output against the rules AND the completeness checklists. For each rule: does the output comply with the spirit, not just the letter? Report violations with rule name, location, proposed fix. Fix all violations. Re-validate until clean.

**This layer is critical.** Be adversarial. Take a contrarian stance. A scanner says "all clear" but the AI reviewing the rules sees that 3 operations on a concept all make decisions that belong to other concepts.

---

## AI Behavior Per Layer

| Layer           | Behavior                                                                            |
| --------------- | ----------------------------------------------------------------------------------- |
| Step 0          | Deep scan evidence + concept_guidance; verify understanding before generating       |
| Generation      | Pay strict attention to rules naturally while producing output                      |
| Scanner fixes   | Fix reported violations mechanically; re-run until clean                            |
| Validation pass | Adversarial checklist review — each rule is a checklist item; report ALL violations |

---

## Corrections Format

When recording corrections:

- **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be
- **Scanner or rule:** (if applicable) Name of scanner or rule that caught the error
- **Likely source:** (if known) One of: code issue | prompt issue | rule priority | rule guidance quality


---

# Phase 9 — Variation

**Actor:** AI

## Purpose

Split stories by subtype when mechanics differ; add failure modes. Subtype concepts already exist from Phase 4; Variation does not discover them.

## Trigger

variation, subtype stories, failure modes, split by mechanics

## Inputs

- `generated/solution_model.json` v2 (from Behavior)

## Instructions

- Split stories by subtype when mechanics differ (per Story vs Scenario rule)
- Add failure-mode scenarios
- Do not discover new subtypes — work with existing concepts from hypothesis

## Outputs

`generated/solution_model.json` v3 — interaction_tree gains subtype stories, failure-mode scenarios


---

# Solution Model Format

# Solution Model Format (solution_model.json)

From Phase 7 onward, the single artifact is `solution_model.json`. Schema:

## Sections

- **concepts** — Array of concept objects. Each has: id, module, kind, inherits, summary, properties, operations, relationships, behavior_refs, story_refs, evidence_refs.
- **behaviors** — Array of behavior objects. Each has: id, name, owner, collaborators, linked_steps, story_refs, evidence_refs.
- **interaction_tree** — Object with epics array. Each epic has sub_epics; each sub_epic has stories. Each story has: id, name, actors, steps, scenarios. Each step has: id, name, linked_behaviors, trigger, response.
- **evidence_refs** — Registry: actions, decisions, states, relationships keyed by ID. Concepts and behaviors reference these IDs.

## Concept

```json
{
  "id": "Character",
  "module": "Core",
  "kind": "aggregate_root",
  "inherits": null,
  "summary": "The entity that performs actions.",
  "properties": [],
  "operations": [],
  "relationships": [{"type": "owns", "target": "AbilityScore", "cardinality": "1..*"}],
  "behavior_refs": ["beh_activate"],
  "story_refs": ["story_resolve_attack"],
  "evidence_refs": ["act_0042", "rel_0012"]
}
```

## Behavior

```json
{
  "id": "beh_activate",
  "name": "activate",
  "owner": "Character",
  "collaborators": ["Attack", "Effect"],
  "linked_steps": ["step_activate_attack"],
  "story_refs": ["story_resolve_attack"],
  "evidence_refs": ["act_0042", "dec_0001"]
}
```

## Step

Each step has at least one linked_behavior. Scenarios group steps (e.g. hit vs miss).


---

# Interaction Tree Format

# Interaction Tree Format

## Hierarchy

Epic → Sub-Epic → Story → Scenario → Step

| Node | Meaning | Heading |
| ----- | ----- | ----- |
| Epic | Large domain capability — a major area of the system | `# Epic: <name> (<statement>)` |
| Sub-Epic | Logical grouping of related stories — a feature area, not a behavior itself | `## Epic: <name> (<statement>)` |
| Story | Smallest independently valuable behavior — has a triggering actor, a responding actor, and produces observable state change. If it has no actor and no state change, it is not a story. | `### Story: <name> (<statement>)` |
| Scenario | A condition-specific grouping of steps within a story (e.g. success path, failure path) | `#### Scenario: <name>` |
| Step | A single atomic interaction — one action by one actor | `- Step N: <name> (When/Then <statement>)` |

## Per Interaction

- **Trigger** — Triggering-Actor, Behavior
- **Response** — Responding-Actor, Behavior
- **Pre-Condition** — label only (Given/And)
- **Failure-Modes** — bullet list, max 3; rule/state based only (no infrastructure failures)
- **Domain Concepts** - Domain Concepts related to Interaction, must exist in the domain model
- **Examples** — tables per concept


### Commonly Generated Fields Per Node

| Node | Commonly Generated | Case-by-Case |
|------|--------------------|--------------|
| Epic | Triggering-Actor, Responding-Actor, Name, Pre-Condition | Constraints |
| Story | Trigger, Response, Name, Examples, Pre-Condition, Failure-Modes | Constraints |
| Scenario | Trigger, Response, Pre-Condition, Examples | |
| Step | Trigger, Response, Examples | Constraints (when step-specific) |

## Domain Grounding

Use `**Concept**` in labels. Every concept must exist in Domain Model.

## Inheritance

Parent → child; use `[brackets]` for inherited values (e.g. `Triggering-Actor: [User]`).

## Example Tables

Tables live on the interaction. One per concept referenced in labels, should be identical to examples in the domain model

```
ConceptName (qualifier):
| scenario | field1 | field2 |
|----------|--------|--------|
| success  | val1   | val2   |

AnotherConcept (qualifier):
| scenario | field1 |
|----------|--------|
| success  | val1   |
```

- Qualifier in parentheses after concept name
- Scenario column required; use kebab-case (e.g. `success`, `invalid-details`)
- `===` separator between tables
- Inherited examples: `Examples: [Table Name 1, Table Name 2]`

## Validation Checklist

**Epic**
- [ ] Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- [ ] Triggering-Actor, Responding-Actor, Pre-Condition, Examples present (or inherited)
- [ ] Pre-Condition on parent only when shared; children list only new or specialized state

**Story**
- [ ] Heading: `### Story: <name using **Domain Concepts**> (<statement>)`
- [ ] Pre-Condition, Failure-Modes (max 3), Trigger, Response present
- [ ] Trigger: sub-bullets Triggering-Actor, Behavior
- [ ] Response: sub-bullets Responding-Actor, Behavior

**Step**
- [ ] `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- [ ] Trigger and Response with [inherited] when from parent

**Example tables**
- [ ] Qualifier in parentheses: `ConceptName (qualifier):`
- [ ] Scenario column required; kebab-case
- [ ] Each table: label, header row, separator row, data rows

**Hierarchy**
- [ ] Epic → Epic/Story → Scenario → Step
- [ ] Each node touches at least one domain concept via `**Concept**`


---

## Domain Model Rules (8)

Apply these rules when producing the domain model output for this phase.

---
title: Derive from context
impact: HIGH
---

## Derive from context

**DO** derive concepts from the interactions you find in the context; focus on *who* exchanges *what* and *what must be true before and after*.
- Example (right): Context says "Customer adds to cart" → interaction: Add to Cart; concepts: Shopping Cart, LineItem. Context says "User selects country for payment" → interaction: Select Country; concepts: Country, PaymentType.

**DO NOT** invent workflows or mechanics not present in the context.
- Example (wrong): Story "Express checkout" or concept "LoyaltyPoints" when context never mentions them. Right: Omit; if needed, state assumption.


---

---
title: Mechanics from evidence, not table of contents
impact: HIGH
---

## Mechanics from evidence, not table of contents

**DO** read evidence chunks for mechanical depth. For each candidate subtype, scan actions.json and terms.json for that name. Derive properties, operations, and collaborators from what the evidence says that variant does. A subtype is justified when the evidence describes different rules, formulas, state transitions, or interaction patterns.

**DO** verify each subtype has its own trigger, conditions, or resolution path in the source. Different mechanics = subtype. Same mechanics with different label = enum.

**DO NOT** infer subtypes from chapter titles, section headers, or bullet lists without reading the actual rule text. A table of contents that lists "Volume Discount, Loyalty Reward, Bundle Offer" under Promotions does not make them subtypes — only the rules for each do.

**DO NOT** create subtypes from variation axes or category lists when each item shares the same resolution logic. "Transaction types: Purchase, Return, Exchange" in a summary is a categorization; read the rules to see if each resolves differently.

- Example (wrong): Source has section "Transaction Types" with Purchase, Return, Exchange. You list those as subtypes. But the ToC categories are wrong — the mechanics show different resolution types (e.g. forward payment vs reversal vs disputed reversal). Right: Read the rules. Derive subtypes from resolution mechanics, not from ToC labels.
- Example (wrong): Source lists "Payment Methods: Credit Card, Bank Transfer, Invoice" and you model each as a subtype because they use different rails. But the mechanics are identical — same flow, different input. Right: PaymentMethod with `method_type {credit_card, bank_transfer, invoice}` — data field, not subtypes. Same mechanics with different input = variable, not subtype.


---

---
title: Subtypes vs enum — distinct mechanics required
impact: HIGH
---

## Subtypes vs enum — distinct mechanics required

**DO** use subtype when the evidence shows different properties, operations, or resolution mechanics for each variant. A subtype is a concept when it has its own rules — different validation, different settlement, different formulas, different state transitions.

**DO** use enum (or type property) when variants share the same logic and differ only by label. Same behavior, different data = enum. Format: `EnumType property_name {value1, value2, value3}`.

**DO NOT** derive subtypes from table of contents or section headers alone. Verify each subtype has distinct mechanics in the evidence (actions.json, terms.json, context chunks). If the source only lists names under a category without different rules per name, it's an enum.

**DO NOT** create both a parent "Type" or "Category" enum and subtypes that mirror it. Example (wrong): Transaction has `TransactionType type {purchase, refund, chargeback}` AND subtypes Purchase, Refund, Chargeback. Use one representation: either enum or subtypes with genuinely different mechanics.

- Example (right — subtype): Transaction subtypes Purchase, Refund, Chargeback — each has different validation, settlement, and reversal rules. Purchase: forward payment, creates obligation. Refund: reversal, requires original. Chargeback: disputed reversal, involves issuer. Each gets its own concept.
- Example (right — enum): Order has `OrderStatus status {pending, shipped, delivered}` — same state machine, different state. Or: LineItem has `ItemType type {product, service, subscription}` — same line-item logic, different label.
- Example (wrong): Transaction types Purchase, Return, Exchange as Transaction subtypes when the rules treat them the same way and only categorize by label. Right: `TransactionType type {purchase, return, exchange}` on Transaction.
- Example (wrong): Subtypes inferred from a bullet list "Promotions: Volume Discount, Loyalty Reward, Bundle Offer..." without reading whether each has different mechanics. Right: Read the actual rule text; if Volume Discount has tier-based calc, Loyalty Reward has points logic, Bundle has bundle rules, they're subtypes. If they're just names under a category, enum.


---

---
title: Variation axes from rules, not table of contents
impact: HIGH
---

## Variation axes from rules, not table of contents

### What a variation axis is

A **variation axis** is a dimension along which the domain's *mechanics* differ — different rules, different resolution, different triggers, different state transitions. Switching from one value to another on a real axis changes *how things work*.

### What is NOT a variation axis

**Variable values are not variation axes.** When the source lists values for a single variable (e.g. payment method: credit card, bank transfer, invoice; order status: pending, shipped, delivered; customer tier: gold, silver, bronze), those are just different values the same variable can take. The *mechanism* is the same — only the input changes. Listing them as a variation axis adds noise and means nothing for extraction.

**ToC and headers are not evidence.** Table of contents, section headers, and bullet lists name things; they do not prove distinct mechanics. You must read the actual rule text before adding an axis.

### How to justify a variation axis

1. **Read the rules** — For each candidate axis, scan context chunks for the rules that govern each variant: triggers, conditions, resolution, state transitions.
2. **Mechanical difference test** — Does switching from variant A to variant B change the *rules* that apply? If yes, it may be a variation axis. If it only changes which value a variable has (same rules, different input), it is not.
3. **Avoid collapsing** — When the source describes many named variants, each with distinct rules, do not collapse them into one superficial axis. Either list the mechanically distinct variants or treat the area as an epic.

### High-complexity areas

When the source describes many named variants, each with its own rules, that area is likely an epic — not a single variation axis. Model as concepts and stories, not as one axis with an enum of values.

### Examples (from unrelated domains)

- **Wrong:** Axis = "payment method (credit card, bank transfer, invoice)" — same settlement flow, different input. Variable values, not a mechanical dimension.
- **Wrong:** Axis = "order status (pending, shipped, delivered)" — same state machine, different state. Variable values.
- **Wrong:** Axis copied from ToC or headers without reading rule text.
- **Right:** Axis documents a dimension where variants have different mechanics — e.g. Purchase vs Refund vs Chargeback each have different validation, settlement, and reversal rules. You have read the rules and can state what differs.


---

---
title: Base and Inheritance Check
impact: HIGH
---

## Base and Inheritance Check

### Concepts that share structure — should they extend a common base?

**Check each cluster** for shared protocol and shared invariants. When concepts share:
- (a) amount or currency mechanics
- (b) participation in validation (e.g. threshold caps)
- (c) lifecycle (created/processed during workflow)
- (d) membership in a parent's collection

…then a common base may be appropriate. Shared protocol: `amount()`, participation in validation, contribution to totals.

**Look for:**
- Missing base — concepts that share acquisition, cost, and validation role but lack a common supertype
- Over-inheritance — base with no real semantics; subtypes share only fields, not behavior

**Verdict:** Introduce a base when the *role* is the same and variation is in implementation. Avoid over-bias against inheritance when concepts clearly share protocol and invariants.

**DO NOT** defer to future refinement. When concepts share protocol (cost, acquisition, validation role, lifecycle, membership in a parent's collection), introduce the shared base in the current phase. Do not say "consider base in future refinement" when the protocol is shared now.

**AI must propose minimal corrections** (e.g. add FinancialRecord as base for Invoice, LineItem, Payment).


---

---
title: Domain Model — Decompose Mechanically Distinct Variants
impact: HIGH
---

## Decompose Variants by Mechanical Distinction

**DO** when subtypes have fundamentally different properties, operations, or resolution mechanics, decompose into an inheritance hierarchy with invariant examples per subtype. Conversely, when operations differ only by a type discriminator with the same logic, consolidate into a single parameterized operation with a type property.

- Example (right — decompose): Promotion subtypes have different mechanics — VolumeDiscount uses tier-based calc, LoyaltyReward uses points logic, BundleOffer has bundle rules. Each gets its own class with distinct properties and operations. Variant rules captured as invariant examples.
- Example (right — consolidate): Two operations `price_for_quantity(qty)` and `price_for_weight(kg)` that differ only by unit → one operation `price_from_amount(amount, unit)` with unit property and invariant: `base = 100 when unit=kg, 10 when unit=each`.

**DO NOT** collapse mechanically distinct behaviors into a flat class with a type enum when subtypes need different properties and operations. Don't create duplicate operations that differ only by a hardcoded value.

- Example (wrong): `Promotion` with `PromotionType {volume_discount, loyalty_reward, bundle, clearance}` — four mechanically different things in one class.


---

---
title: Domain Model — Invariants for Rules, Derived Properties Not Getters
impact: HIGH
---

## Rules and Formulas in Invariants, Not Descriptions

**DO** express domain rules, formulas, value mappings, and constraints as explicit invariants. Properties declare type and name only. Operations declare signature only. Model computed/derived values as properties with invariants, not as getter operations.

- Example (right): Property: `Number amount`. Invariant: `amount >= 0`. Property: `Number discount_percent`. Invariant: `discount_percent <= 100`. Property: `Boolean is_eligible`. Invariant: `is_eligible when order_total >= min_threshold`.

**DO NOT** embed formulas or hardcoded values in property descriptions or operation signatures. Do not model simple derived values as getter operations.

- Example (wrong): `Number value (+2 minor, -2 penalty, +5 major)` — values in description. `Number cost_per_unit (2.50)` — formula in property. `get_total()` — getter for a derived value. `calculate_discount() → Number (qty × 0.1)` — formula in operation signature.


---

---
title: Domain Model — Extract Shared Behavior into Base Concepts
impact: HIGH
---

## Shared Behavior and Structure in Base Concepts

**DO** when multiple concepts share the same behavioral pattern or structural pattern, extract a base concept. Place it in the system that owns the behavior, not the system that owns the data. Separate orthogonal concerns into independent bases.

- Example (right): Multiple concepts can "validate" → extract `Validatable` with `validate()` and `validation_rules`. Multiple concepts have "amount, currency, status" → extract `FinancialRecord` with shared properties and invariants. Invoice combines both: `Invoice : FinancialRecord, Validatable`. Order has amount but different validation: `Order : FinancialRecord`.

**DO NOT** duplicate behavioral or structural patterns across concepts without a shared base. Do not conflate orthogonal concerns into a single base (e.g., "has amount" and "can validate" are separate concerns).

- Example (wrong): Invoice, Order, and Payment each independently declare `validate()` and `validation_rules` with no shared base. Or: everything extends `Validatable` even when some concepts have amounts but no validation.


---



## Interaction Tree Rules (7)

Apply these rules when producing the interaction tree output for this phase.

---
title: Verb-noun format
impact: HIGH
order: 1
---

## Verb-noun format

Use verb-noun format for epic/story/step names and steps. Actor documented separately. Use active voice, base verb forms, and business language for all interaction text. Use behavioral language — describe what happens, not how it's implemented. Use domain concepts in steps (Given/When/Then) — not UI labels. Applies to all nodes (epic, story, step, scenario), including steps in or out of scenarios.
**DO** use Actor → verb noun [qualifiers]. Actor is documented separately, NOT in the name.
- Names: "Places Order" (actor: Customer); "Validates Payment" (actor: System); "Process Order Payment".
- **Step format** — strategy may specify When/Then (strict) or vanilla (verb-noun). Show both:
  - **When/Then:** `When **User** browses countries; Then **System** displays list of **Country** options`.
  - **Vanilla:** `User submits form`, `System validates payment`, `Select item from list`.
- Use base verb forms (infinitive/imperative): "Select Tokens", "Group Minions", "Process Payment".
- Use behavioral terms: "When user enters name; Then system saves character information" (not "system writes to JSON").
- Use domain concepts in steps: "User selects **Country**", "User enters **PaymentDetails**" (not "User clicks dropdown", "User fills form field").

**DO NOT** include actor in name, use noun-only, gerunds, or third-person singular.
**DO NOT** use technical implementation terms (config, json, api, sql, class, method). Use behavioral language instead.
- Wrong: "Customer Places Order" (actor in name). Right: "Places Order" (actor: Customer).
- Wrong: "Order submission", "Payment processing", "Form validation" (noun-only). Right: "Submit order", "Process payment", "Validate form".
- Wrong: "Submitting order", "Selects item", "Displays confirmation" (gerund/third-person). Right: "Submit order", "Select item", "Display confirmation".
- Wrong: "Then system saves to JSON file", "Then system parses XML", "Then system executes SQL query" (technical). Right: "Then system saves configuration data", "Then system processes data", "Then system retrieves data".
- Wrong: "User clicks dropdown", "User fills form field", "User submits button" (UI). Right: "User selects **Country**", "User enters **PaymentDetails**", "User submits payment".


---

---
title: Outcome-oriented language
impact: HIGH
order: 2
---

## Outcome-oriented language

Use outcome-oriented language over mechanism-oriented language. Focus on what is created or achieved, not how it's shown or communicated.

**DO** use verbs that describe artifacts and outcomes — name concepts by what they ARE or CREATE.
- Example (right): "System → displays power activation animation" (not "Visualizing Power Activation"); "System → provides combat outcome feedback" (not "Showing Combat Results"); "System → displays hit indicators" (not "Displaying Hit Information").

**DO NOT** use generic communication or mechanism verbs.
- Example (wrong): "Visualizing Power Activation", "Showing Combat Results", "Displaying Hit Information", "Presenting Configuration Options".
- Wrong: "Showing results", "Displaying information", "Visualizing data", "Presenting options", "Providing settings", "Enabling features", "Allowing access".


---

---
title: Story granularity
impact: MEDIUM-HIGH
order: 4
---

## Story granularity

**DO** break down by distinct requirements areas, distinct concept structure, or workflow steps; sufficient stories to capture rule detail.
- Example (right): Story "View Product Details", Story "Make Payment" (each has distinct logic). Story "Drive Bike", Story "Drive Car" (concept structure differs).

**DO NOT** collapse large rule sections into one story.
- Example (wrong): Story "All combat effects" or "All attack types" when the context has dozens of distinct rules. Right: Story "Apply damage effect", Story "Apply condition effect", Story "Resolve melee attack", etc.


---

---
title: Small and testable
impact: HIGH
order: 5
---

## Small and testable

Stories must be testable as complete interactions and deliverable independently. Story = testable outcome; Step = implementation detail.

**DO** create stories that can be tested and delivered independently.
- Example (right): "Customer → places order" (testable: order created, payment processed).
- Story = User/system outcome (testable independently with clear acceptance criteria).
- Step = Implementation detail (not testable alone, verified as part of parent story test).

**DO NOT** create stories too small to test meaningfully or make implementation steps into stories.
- Example (wrong): "Add order button" (can't test without full order flow); "Display error message" (can't test without validation context).
- Wrong: "Convert Diagram to StoryGraph Format", "Serialize Components to JSON", "Calculate Component Positions" (implementation steps, not testable alone).


---

---
title: Interactions inheritance — actors
impact: HIGH
---

## Actors inheritance

**DO** use [User] or [System] at every trigger/response so the actor is visible without looking up. Use Title Case; no dot notation (e.g. `Triggering-Actor`, not `trigger.actor`). Stories inherit Triggering-Actor and Responding-Actor from Epic. Steps inherit from Story or higher; exception: when a step is system-triggered (e.g. "When **System** receives payment type selection"), that step may override Triggering-Actor. See `core.md`.
- Example (right): Epic "Make Checks": Triggering-Actor: User, Responding-Actor: System. Story: Triggering-Actor: [User], Responding-Actor: [System]. Step: Triggering-Actor: [User] or Triggering-Actor: User (when override).

**DO NOT** omit actor at every trigger/response. Do not use lowercase or dot notation for field names.
- Example (wrong): Step has Trigger without Triggering-Actor; reader must look up. Right: Every Trigger and Response shows actor explicitly.


---

---
title: Interactions inheritance — Examples
impact: MEDIUM-HIGH
---

## Examples inheritance

**DO** live on the interaction. Use [inherited] when tables come from parent; list the qualitative names (e.g. `[Logged In User, Active User Session, User Payment Type Access]`). Include step-specific or story-specific examples unbracketed. Name by state or condition — "Selected Country", "Selected PaymentType", "Approved Payment" — not generic labels like "Payment" or "Country". See `core.md`.
- Example (right): Epic has Examples: Logged In User, Active User Session. Story: Examples: [Logged In User, Active User Session]. Step: Examples: [Logged In User], Selected PaymentType (step-specific).

**DO NOT** repeat parent tables on children. Do not use generic labels like "Payment" or "Country". When inherited, list those names: `examples: [Logged In User, Active User Session, User Payment Type Access]`.
- Example (wrong): Story "Search by title" has full Examples table when Epic already has it. Right: Story: Examples: [inherited] or list names.


---

---
title: Interactions inheritance — Pre-Condition
impact: HIGH
---

## Pre-Condition inheritance

**DO** declare shared Pre-Condition on the parent only; list only new or unique Pre-Condition on children; make Pre-Condition comprehensive — ask "Would this work if [X] didn't exist?". Assign to ONE level only — if unique to a story, keep on story; if on more than one story, promote to parent. When the child uses only parent concepts/state, leave Pre-Condition and domain concepts blank (inheritance assumed). See `core.md`.
- Example (right): Epic "Browse Books": Pre-Condition "Books exist in catalog"; Story "Search by title": Pre-Condition "Books match search criteria" (specializes). Epic "Make Checks": State Concepts Check, Modifier, DifficultyClass; Stories have State Concepts blank. PowerPointBudget on 3 of 4 stories → promote to Sub-epic; remove from the 3.

**DO NOT** duplicate shared Pre-Condition on children or omit required preconditions. Do not repeat parent concepts on children. Do not put concepts on individual stories when they apply to multiple — that causes you to omit them on some. Stories rarely define domain concepts — they inherit from epic.
- Example (wrong): Story "Search by title" has Pre-Condition "Books exist in catalog" when Epic already has it. Epic "Make Checks" has State Concepts on each story; Story "Make Secret Check" has State Concepts blank and the model omits Check, Modifier, DifficultyClass — they were forgotten. Right: Epic has concepts; all stories inherit (blank).


---

