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

# Phase 7 — Structure

**Actor:** AI

## Purpose

Build first `solution_model.json` from hypothesis + evidence index. Assign properties, inheritance, steps; concepts and tree gain structure in parallel.

## Trigger

structure, structural model, relationships, composition, collaborators

## Inputs

- `generated/hypothesis.json`
- `evidence/evidence_index.json`

## Instructions

- Create `solution_model.json` with concepts, behaviors, interaction_tree, evidence_refs
- Define composition relationships; attach collaborators
- Ground relationships in evidence (from_entity → type → to_entity)
- Use evidence/states.json for state-based relationships
- Use evidence/decisions.json for conditional relationships
- Preserve subtype structure from hypothesis

## Outputs

`generated/solution_model.json` v1 — concepts gain story_refs, evidence_refs, properties, relationships, kind; interaction_tree gains stories, steps (actors, pre-conditions), empty linked_behaviors


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

## Domain Model Rules (9)

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
title: Domain Model — Bidirectional Relationships
impact: MEDIUM
---

## When A References B, B Should Reference A

**DO** when Concept A has a Property or Operation that references B (non-primitive), B should have a corresponding reference to A — same relationship, both perspectives.

**DO** use relationship names that describe the relationship from each concept's viewpoint (Order contains LineItem; LineItem belongs to Order).

**DO NOT** require bidirectional mapping for primitives (String, Number, Boolean, etc.).

**DO NOT** use mismatched collaborators — the bidirectional pair must describe the SAME relationship from both sides.

## Creator → Created Back-Reference

**DO** when a concept creates another during execution (dependency "creates"), and the created object needs to navigate back to access creator state during its lifecycle, model a `source` reference property on the created object with an association edge back to the creator. Both the creates dependency AND the source association are needed.

- Example (right): Invoice creates Payment (dependency "creates"). Payment has `Invoice source` property (association back). Payment navigates `source.line_items`, `source.customer`. Diagram shows both edges.

**DO NOT** model created objects as isolated snapshots when they need live access to creator state. A copied `Number amount` loses navigation to the creator's line items and customer.

- Example (wrong): Payment has `Number amount` but no reference to the Invoice that created it — can't navigate to line items, customer, or order.


---

---
title: Domain Model — Caller, Receiver, State Mapping
impact: HIGH
---

## Caller, Receiver, Message → Trigger and Response

**DO** map OOA caller/receiver/message to the interaction model:
- **Caller** → Triggering-Actor (who starts the interaction)
- **Receiver** → Responding-Actor (who receives and responds)
- **Message** → Behavior in Trigger (what is requested) and Behavior in Response (what is done)

**DO** ensure every concept that participates as caller or receiver exists in the Domain Model with Properties and Operations that support that participation.

## State Before / State After → Pre-Condition, Triggering-State, Resulting-State

**DO** map OOA state before/after to interaction fields:
- **State Before** → Pre-Condition (what must be true) + Triggering-State (state that qualifies the trigger)
- **State After** → Resulting-State (state that results from the response)

**DO** reference domain concepts in these labels via `**Concept**` so state flows are traceable to the Domain Model.

## Event as Trigger

**DO** treat an **event** as the **Trigger** that causes the **Response**. The Trigger (Triggering-Actor, Behavior, Triggering-State) is the stimulus; the Response (Responding-Actor, Behavior, Resulting-State) is the reaction. Events often appear as user actions, system triggers, or state changes that qualify the interaction.


---

---
title: Domain Model — Composition and Aggregation
impact: HIGH
---

## Composition vs Aggregation

**DO** when a concept "has" another concept, distinguish:

| Relationship | Meaning | Lifecycle | Example |
|--------------|---------|-----------|---------|
| **Composition** | Strong has-a; part cannot exist without whole | Shared — part dies with whole | Order and LineItem; Book and Page |
| **Aggregation** | Weak has-a; whole has no meaning without multiple instances of the same part (e.g. crowd, flock, mob) | Independent | Crowd (people); Flock (birds); Cart and Product |

**DO** prefer composition and aggregation over inheritance for concept relationships. Inheritance couples types tightly; composition/aggregation keep flexibility.

## Sequence Diagrams

**DO NOT** generate sequence diagrams. Object flow and walkthrough strategies (object-to-object interactions) are in scope; formal sequence diagrams are not.


---

---
title: Domain Model — Interaction Patterns
impact: HIGH
---

## Interaction Patterns

**DO** recognize and use interaction patterns when describing Trigger → Response:

| Pattern | Description | Interaction Tree mapping |
|---------|-------------|--------------------------|
| **Producer-Consumer** | One-way; producer sends; consumer reacts | Trigger from one actor; Response from another; no return flow |
| **Client-Server** | Two-way; client requests; server responds | Trigger (request) → Response (reply); may chain to further interactions |
| **Coordinator** | One object orchestrates several others | Epic or Story where one concept delegates to multiple collaborators |


---

---
title: Domain Model — Parts Manage Their Own State
impact: HIGH
---

## Parts Manage Their Own State

**DO** let each concept manage its own properties through its own invariants. A container holds references to its parts (composition/aggregation) but does not orchestrate their configuration. Each part knows its own rules.

- Example (right): Order has `Dictionary line_items` (composition). LineItem has `Number quantity` with invariant `subtotal = quantity × unit_price`. OrderTotal has `validate_threshold(min) → Boolean`. Each concept owns its rules — Order just holds references.

**DO NOT** put `configure_X()`, `set_X()`, or orchestration methods on the container that delegate to owned objects. If LineItem knows how to compute its subtotal from quantity and price, that's LineItem's concern.

- Example (wrong): Order has `configure_line_item(sku, qty) → LineItem`, `configure_payment(method, amount) → Payment`, `validate_order_total() → Boolean`. Order is orchestrating what each part should do instead of letting parts manage themselves.

**Related rules:** [domain-ooa-traverse-from-root](domain-ooa-traverse-from-root.md) — traverse from root; source owns creation. [domain-ooa-model-instances-not-smashed](domain-ooa-model-instances-not-smashed.md) — model instances, not smashed properties.


---

---
title: Domain Model — Single Source of Truth
impact: HIGH
---

## No Duplicate Primitive and Relationship for Same Value

**DO** when a concept has its own class with behavior (operations, invariants), reference it through a relationship only. The owning class accesses the value through the relationship. One source of truth.

- Example (right): Order has aggregation to OrderTotal. Order gets the total value through its OrderTotal reference. No redundant `Number total` property on Order.

**DO NOT** have both a primitive property AND a relationship to a class that holds the same value. Two sources of truth create inconsistency.

- Example (wrong): Order has `Number total` property AND an aggregation to OrderTotal class (which has `Number amount`). Two places to get the same value — which is authoritative?


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
title: Supporting actor and Response
impact: MEDIUM-HIGH
---

## Supporting actor and Response

**DO** treat Supporting as the system (or subsystem) that responds — use Actor → System exchange; keep Epic-level (and Sub-epic) Response coarse-grained — what is true after the actor triggers at that level.
- Example (right): "System saves campaign PL"; "System persists budget"; Epic "Build a Character" → Response "System creates valid Character for Campaign".

**DO NOT** frame Supporting as a human or use human-to-human exchange; do not use story-level or sub-epic-level detail in Epic-level or Sub-epic Response.
- Example (wrong): "GM sets and communicates"; "Player tells GM"; Epic "Build a Character" → Response "System applies cost formula; deducts PP; validates traits" (that belongs in stories). Right: Epic Response "System creates valid Character for Campaign".


---

---
title: Interactions inheritance — Resulting-State
impact: HIGH
---

## Resulting-State inheritance

**DO** apply the same inheritance rules to Resulting-State as Pre-Condition — shared on parent, child-specific on child. At Epic/Sub-epic level, express as a single, high-level outcome; use outcome language only (what is true afterward). Resulting-State is the state that results from the interaction (see `core.md`).
- Example (right): Parent: "Cart populated"; Child: "Shopping Cart: empty → has-items". Epic: "Character is built and valid within campaign PL and PP limits"; "validation result recorded".

**DO NOT** duplicate Resulting-State across levels or use action language in Resulting-State. Do not use intermediate steps, granular outcomes, or behavior/action language in Epic/Sub-epic Resulting-State.
- Example (wrong): "System validates" or "System records"; Epic "Build a Character" → "Character has PP budget allocated"; "Character is fully built; Character has all traits; Character validated against PL". Right: "validation result recorded"; Epic "Character is built and valid within campaign PL and PP limits".


---

---
title: Interactions inheritance — Triggering-State
impact: MEDIUM-HIGH
---

## Triggering-State inheritance

**DO** place Triggering-State at the level where it applies to all descendants. Epic holds trigger state for rules that apply to all children (e.g. user access to payment types by country). Epics (including epic children of epics) group; they do not add trigger/response state. Stories inherit Pre-Condition, Triggering-Actor, and Responding-Actor from Epic. Triggering-State qualifies the interaction (e.g. selecting an option of a certain type). See `core.md`.
- Example (right): Epic "Make Checks": Triggering-State: User has access to Check, Modifier, DifficultyClass. Story: inherits; adds only when story-specific.

**DO NOT** put Triggering-State at a level if it applies only to specific scenarios or stories — place it on those nodes. Do not put concepts on individual stories when they apply to multiple — promote to parent.
- Example (wrong): Epic "Make Checks" has no Triggering-State but each story has different access rules — promote shared rules to Epic. Right: Epic has rules that apply to all children.


---

