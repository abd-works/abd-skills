# Critical Quality Steps

**These steps MUST be followed for every AI phase. No exceptions.**

---

## DO NOT write scripts for AI phases

**AI phases = the AI does the work.** You read the inputs, reason about them, and produce the output directly.

**DO** read the inputs (hypothesis.json, evidence/, context chunks), analyze them, and edit/write the output files yourself.

**DO NOT** write a Python (or other) script to "run" the phase. Do not create `synthesize_concepts.py`, `build_structure.py`, or similar. The pipeline has no script runners for AI phases — by design. Writing a script delegates the cognitive work to code; the AI must perform it.

Wrong: "I'll create a script that merges concepts and builds hierarchy."
Right: "I'll read the hypothesis and actions, curate concepts, build the hierarchy from evidence, and write the refined hypothesis.json."

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

# Phase 12 — Finalize

**Actor:** AI

## Purpose

Apply assessment fixes; produce validated model with full traceability.

## Trigger

finalize, validated model, apply fixes, full traceability

## Inputs

- `generated/solution_model.json` v4 (from Consolidate)
- `generated/assessment.json` (from Assess)

## Instructions

- Apply fixes from assessment
- Produce validated solution_model.json with full traceability

## Outputs

`generated/solution_model.json` final


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

## Domain Model Rules (16)

Apply these rules when producing the domain model output for this phase.

---
title: Anemia / Centralization Critique
impact: HIGH
---

## Anemia / Centralization Critique

Explicitly attack the candidate model before accepting it. This phase is mandatory.

**Look for:**
- Centralized handlers, resolvers, or managers
- Anemic entities with no decisions
- Objects that are just data bags
- Config-holder pseudo-objects
- Orphan concepts (referenced but not modeled)
- State with no owner
- Rules with no owner
- Fake inheritance (shared fields, no shared semantics)
- Type, mode, or effect switches that should be polymorphism
- Orchestration making domain decisions
- Relationships with no behavioral significance

**AI must propose minimal corrections** for each issue found.

**DO NOT** truncate. Full Model Assessment requires an explicit anemia critique table covering all issue types (centralized handlers, anemic entities, data bags, orphan concepts, state with no owner, rules with no owner, fake inheritance, type switches, orchestration making domain decisions). Persist the full assessment in run-N-ooad.md. A one-line note is insufficient.


---

---
title: Domain Model — Wirfs-Brock Role Stereotypes
impact: MEDIUM
---

## Concept Roles (Optional)

When clarifying how a concept participates in interactions, you may assign a **role**:

| Role | Responsibility | Example |
|------|----------------|---------|
| **Information Holder** | Knows and provides information | Customer, Order, Product |
| **Structurer** | Maintains relationships between objects | Cart (holds line items) |
| **Service Provider** | Performs work; often stateless | TaxCalculator, Validator |
| **Coordinator** | Delegates to others | CheckoutController |
| **Controller** | Handles system events; represents use case | ProcessOrderHandler |
| **Interfacer** | Connects to outside world | PaymentGateway, EmailSender |


---

---
title: Domain Model — Domain Language
impact: HIGH
---

## Use Domain Language from Source

**DO** use domain language from stories and acceptance criteria. Mine vocabulary from source material.

**DO** use standard types (String, Number, Boolean, List, Dictionary, UniqueID, Instant) for Properties; prefer domain concepts over scattering primitives. See domain-ooa-property-types.

**DO** write Operation names in natural English (Calculates total, Validates inventory, Is exhausted when fully redeemed).

**DO NOT** use Hold, Get, Has as defaults — find domain-specific verbs (Is identified by, Defines, Starts valid at, Expires at).

**DO NOT** use Manager, Service, Handler, Factory suffixes for concept names.

**DO NOT** use abbreviations or technical jargon when simple English works.


---

---
title: Domain Model — Integrate Concepts
impact: HIGH
---

## Nest Related Capabilities Under Parent

**DO** integrate related capabilities under a parent concept (e.g. Portfolio with multiple Operations, not separate PortfolioValue, PortfolioRisk concepts).

**DO** group concepts by business domain, not technical layers (Data Layer, Business Logic Layer).

**DO NOT** create separate concepts with the same noun when they should be one (PortfolioValue, PortfolioRisk, PortfolioAllocation → Portfolio).

**DO NOT** split related capabilities into separate sibling concepts (PortfolioValue, PortfolioRisk as separate concepts when they belong under Portfolio).

**DO NOT** group by technical layers or implementation patterns (Factories, Builders, Repositories).


---

---
title: Domain Model — Module Folder Mapping
impact: LOW
---

## When Mapping to Code

**DO** when mapping to code, use Module = folder path in dot notation (e.g. `actions.render`, `repl_cli.cli_bot`).

**DO NOT** use `src/` prefix or slashes — use dots for nesting (e.g. `repl_cli.cli_bot`, not `src/repl_cli` or `repl_cli/cli_bot`).

**Note:** Applies when the synthesizer output is mapped to existing or planned code structure. Synthesizer may run before code exists — rule is optional when applicable.


---

---
title: Domain Model — Resource Concept Naming
impact: HIGH
---

## Concepts as Resources

**DO** name concepts as nouns (resources): Order, Portfolio, Voucher, not OrderManager, InstructionPreparer.

**DO** give concepts both Properties and Operations where behavior exists — no anemic concepts (only Properties, no Operations).

**DO NOT** use Manager/Service/Handler/Preparer/Builder suffixes. Name after the resource itself.

**DO NOT** create concepts that are only data carriers with no Operations.

**DO NOT** pass another concept's data to it — concepts own their data. Encapsulation: don't pass another concept's Properties as parameters to its Operations.


---

---
title: Scenario / Message Walkthrough Validation
impact: HIGH
---

## Scenario / Message Walkthrough

Make sure the model can actually behave. A model that looks elegant but fails in message flow is not good OOAD.

**Run walkthroughs for:**
- Happy path
- Error path
- Edge case
- Exception path
- Stateful repetition
- Alternate variation mode
- Recovery, retry, or cancellation where relevant

**Validate at two levels:**

**Scenario flow:** What happens in the domain?

**Message flow:** Which object sends what message to whom? Does the receiver know enough to act? Is the sender delegating a decision or making it centrally?

**This step exposes:** missing objects, misplaced behavior, centralization, fake relationships, state with no owner.

**DO NOT** truncate. Full Model Assessment requires multiple scenario walkthroughs with message flow (happy path, error path, edge case, stateful repetition, alternate variation, recovery where relevant). Persist the full assessment in run-N-ooad.md. A one-line note is insufficient.


---

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
title: Hierarchy from evidence, not invention
impact: HIGH
---

## Build concept_hierarchy from evidence

**DO** derive parent-child relationships from evidence in `registries.actions` and concept `performs`/`receives`:
- **Shared mechanics** — concepts that share the same resolution, cost, or validation role (e.g. Wire Transfer, ACH, Card Payment all resolve as Payment; Checking, Savings, Money Market → Account) → Child → Parent
- **Shared protocol** — concepts that participate in the same workflow, lifecycle, or parent's collection → introduce a common base
- **Subtype patterns** — when evidence describes different rules, formulas, or state transitions for variants → model as Child : Parent

**DO** scan actions for each concept: subject, object, predicate, raw. Look for:
- Co-occurrence (concepts that appear together as subject/object)
- Shared terminology (term_ids, chunk_ids overlap)
- Domain language (e.g. "Transaction", "Account", "Payment", "Fee", "Product", "Order" in raw text)

**DO** build a **comprehensive** hierarchy. With hundreds of concepts, expect many parent types: Transaction, Account, Payment, Fee, Product, Order, Customer, etc. Each parent should have all its subtypes listed.

**DO NOT** infer hierarchy from chapter titles, section headers, or ToC alone. Read the raw action text to confirm different mechanics.

**DO NOT** leave hierarchy sparse. If you have 10+ concepts that share mechanics (e.g. Wire Transfer, ACH, Card Payment → Payment; Checking, Savings → Account), add them. If you have Transaction subtypes beyond Purchase/Refund/Chargeback, add them.

**Related rules:** [concept-model-subtypes-first-class](concept-model-subtypes-first-class.md), [variation-base-inheritance](variation-base-inheritance.md), [domain-mechanics-not-toc](domain-mechanics-not-toc.md), [refined-integrate-concepts](refined-integrate-concepts.md).


---

---
title: Model Instances, Not Smashed Properties
impact: HIGH
---

## Model Instances, Not Smashed Properties

**DO** consider when a concept is best represented as instances/examples (objects in diagram) vs smashing it into a property or method.

**DO** model context with tables as one or more concepts with relationships.

**DO** model instances and examples explicitly when structure matters.

**DO NOT** smash complex objects with multiple concepts into a single property or method.


---

---
title: Domain Model — Standard Types for Properties
impact: HIGH
---

## Standard Types for Properties

**DO** use standard types for Properties when defining concepts:

| Type | Use when | Example |
|------|----------|---------|
| **String** | Text, names, labels | `Customer.name`, `Product.sku` |
| **Number** | Quantities, amounts, counts | `Cart.total`, `LineItem.quantity` |
| **Boolean** | Yes/no, flags | `Order.isPaid`, `Cart.isEmpty` |
| **List** | Ordered collection | `Cart.lineItems` (List of LineItem) |
| **Dictionary** | Key-value mapping | `Product.attributes`, `Config.settings` |
| **UniqueID** | Identifier, reference | `Order.customerId`, `LineItem.productId` |
| **Instant** | Point in time (ISO 8601) | `Order.createdAt`, `Payment.processedAt` |

| **EnumType** | Fixed set of valid values | `ModifierType type {bonus, penalty}`, `ActionType action_type {standard, move, free, reaction}` |

Use `List<T>` or `Dictionary<K,V>` when element types matter.

**DO** use a named enum type when a property has a constrained set of valid values. Format: `EnumType property_name {value1, value2, value3}`.

**DO NOT** use `String` with parenthetical options (e.g., `String type (bonus/penalty)`). Strings imply free-form text; constrained options are a distinct type.

- Example (wrong): `String type (bonus/penalty)`, `String attack_type (close/ranged)`.
- Example (right): `ModifierType type {bonus, penalty}`, `AttackType attack_type {close, ranged}`.


---

---
title: Speculation and assumptions
impact: HIGH
---

## Speculation and assumptions

**DO** state an assumption when something is unclear.
- Example (right): "Assumption: Shipping Address is provided before checkout"; "Assumption: Loyalty points not in scope".

**DO NOT** speculate beyond the provided material or invent mechanics when unclear.
- Example (wrong): Story "Apply loyalty points at checkout" when context never mentions loyalty. Right: Omit, or state "Assumption: Loyalty points not in scope."


---

---
title: Subtypes as first-class concepts
impact: HIGH
---

## Subtypes as first-class concepts

**DO** give each subtype its own `### **SubtypeName** : Parent` section with its own properties, operations, collaborators, and composition. Subtypes inherit from parent but have distinct mechanics — model those mechanics explicitly.

**DO** ground each subtype's definition in evidence. Scan `actions.json` and `terms.json` for the subtype name (e.g. Purchase, Refund, Chargeback) and derive properties/operations from what the evidence says that subtype does.

**DO NOT** list subtypes only in a parent's `Subtypes:` line without creating first-class sections for them.

**DO NOT** collapse subtypes that have distinct rules (e.g. Purchase vs Refund vs Chargeback each have different validation, settlement, reversal) into a single parent definition.

- Example (wrong): `### **Transaction**` with `Subtypes: Purchase, Refund, Chargeback` and no separate sections for Purchase, Refund, Chargeback.
- Example (right): `### **Transaction**` plus `### **Purchase** : Transaction`, `### **Refund** : Transaction`, `### **Chargeback** : Transaction`, etc., each with its own properties, operations, and collaborators.


---

---
title: Subtypes vs enum — verify before modeling
impact: HIGH
---

## Subtypes vs enum — verify before modeling

**DO** before creating a subtype section: verify actions.json and terms.json show different mechanics for that subtype. Different properties, operations, or resolution paths = subtype. Same logic, different label = enum on parent.

**DO** use `EnumType property_name {value1, value2}` when the evidence shows same behavior across variants. Do not create subtype sections for enum-like variation.

**DO NOT** create subtype sections from concept_hierarchy without evidence check. If concept_guidance listed Purchase, Refund, Chargeback as Transaction subtypes but the evidence treats them identically (same validation, same settlement flow), convert to `TransactionType type {purchase, refund, chargeback}` on Transaction.

**DO NOT** have both a type enum and mirroring subtypes. If Transaction has `TransactionType type {purchase, refund, chargeback}`, do not also create Purchase, Refund, Chargeback as subtypes.

- Example (right): Transaction has Purchase, Refund, Chargeback as subtypes — evidence shows Purchase has forward-payment validation, Refund has reversal rules and original-required check, Chargeback has issuer workflow. Each has distinct mechanics.
- Example (wrong): Transaction has Purchase, Return, Exchange as subtypes when the rules only categorize by label. Right: Transaction with `TransactionType type {purchase, return, exchange}`.


---



## Interaction Tree Rules (9)

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
title: Hierarchy — approximately 4 to 9 children
impact: MEDIUM
order: 3
---

## Hierarchy — approximately 4 to 9 children

Any node (epic, story, scenario) has approximately 4–9 children. Does not apply to steps. For stories, count **steps** as children (not scenarios).
**DO** keep child count in the 4–9 range for manageable granularity.
- Epic: ~4–9 sub-epics or stories.
- Story: ~4–9 steps (total across scenarios; scenarios are containers, not counted).
- Scenario: ~4–9 steps.

**DO NOT** create nodes with many more than 9 children — split or regroup.
- Wrong: Epic with 15 stories (split into sub-epics).
- Wrong: Story with 12 steps (consider splitting story or grouping steps into scenarios).


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
title: Background vs scenario setup
impact: MEDIUM
---

## Shared setup as Pre-Condition with Examples at story level

**Background** (BDD) = **Pre-Condition with Examples at the story level**. Scenarios below inherit that Pre-Condition and Examples. No separate Background section — use the interaction hierarchy.

**DO** put shared setup as Pre-Condition with Examples on the story (or epic). Use Given/And only — state, not actions. Use **Concept** notation. Scenarios show inherited Pre-Condition and Examples in brackets.

**Example (right):**

```
#### Story: User Triggers Country-Specific PaymentType
- Pre-Condition: Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)
- Examples:
  Logged In User:
  | scenario   | user_name | user_role |
  |------------|-----------|-----------|
  | success    | Jane Doe  | Payer     |
  ===
  Active User Session:
  | scenario   | user_name | session_id | expires_at |
  |------------|-----------|------------|------------|
  | success    | Jane Doe  | sess-001   | 2025-03-08 |

##### Scenario: Success — payment validated and confirmed
- Pre-Condition: [Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)]
- Examples: [Logged In User, Active User Session]

###### Steps
- Step 1: Browse Country for Payment ...
```

**DO NOT** repeat setup in each scenario when it applies to all. Do not put actions in Pre-Condition — only state (Given/And). Do not use a separate "Background" block; use story-level Pre-Condition + Examples and inheritance.

**Example (wrong):** Each scenario repeats full Given/And and example tables. **Right:** Story holds Pre-Condition + Examples; scenarios show `[inherited]` or list names.


---

---
title: Example tables match Domain Model
impact: HIGH
---

## Example tables must align with Domain Model

**DO** ensure every example table corresponds to a domain concept in the Domain Model. Table columns must match the concept's properties. Table relationships must match the Domain Model's concept relationships (composition, aggregation). Every `**Concept**` referenced in Pre-Condition, Trigger, or Response labels must have a corresponding example table (or inherit one). Every example table must be referenced via `**Concept**` in labels — no orphaned tables.
- Example (right): Domain Model has `Country` with properties `country_code`, `country_name`. Example table: `Selected Country: | scenario | country_code | country_name |`. Domain Model has `User` → `Session` (composition). Tables appear in order: `Logged In User`, then `Active User Session` — relationship expressed through table ordering.

**DO** use source entity data in tables, not aggregated or calculated values. Show the actual records that produce the outcome. If a scenario computes a result, the table shows the inputs, not the output count.
- Example (right): `UpdateReport (renames): | original_name | new_name | parent |` — shows actual renamed entities.
- Example (wrong): `UpdateReport: | renames_count | new_count | | 1 | 2 |` — counts defer real work; where do these numbers come from?

**DO** express table relationships through table ordering and qualifier names — not through ID columns. IDs are implementation concerns. Domain Model says `Epic` contains `SubEpic`; tables appear in that order: `Epic` first, then `SubEpic (child of Epic)`.
- Example (right): `User: | user_name | user_role |` then `Session: | user_name | session_id | expires_at |` — connected by domain attribute, not by `user_id` foreign key.

**DO NOT** have `**Concept**` in labels without a matching example table. Do not have example tables that no label references. Do not invent column names not in the Domain Model — use the concept's actual property names.
- Example (wrong): Steps reference `**PaymentType**` but no PaymentType example table exists. Or: `Entitlement` table exists but no step mentions `**Entitlement**`.
- Example (wrong): Domain has `recipient_name` but table uses `payee` or `beneficiary_label`.

**DO NOT** flatten related concepts into one table or use lookup-style tables with ID columns for joining. Each concept gets its own table; relationships are expressed through ordering and qualifiers.
- Example (wrong): `| enterprise_id | recipient_id | account_id |` — flat table loses relationship structure. Right: separate tables for Enterprise, Recipient, Account in domain relationship order.


---

---
title: Failure modes
impact: MEDIUM
---

## Failure modes

**DO** limit failure modes to a maximum of 3 per interaction; derive from domain rules, state conditions, or authorization.
- Example (right): "Insufficient balance"; "Account suspended"; "Cart is empty"; "Payment type not available for country".

**DO NOT** include infrastructure or technical failures.
- Example (wrong): "Database timeout"; "Network unreachable"; "Server crash". Right: "Insufficient balance"; "Account suspended".


---

---
title: Scaffold pattern not enumeration
impact: HIGH
---

## Scaffold pattern not enumeration

The first cut of `interaction-tree.md` and `domain-model.md` establishes the pattern for each epic. Later phases expand and refine. If the first cut enumerates everything, later phases have nothing to do.

**DO** detail 2-3 representative stories per epic/sub-epic with full fields (Trigger, Response, Pre-Condition, domain concepts). List remaining stories by name only with "N more stories following this pattern based on [specific items]."
- Example (right): Two stories under a sub-epic shown in full with Trigger/Response and domain concepts; then "4 more stories following this pattern: [Story A], [Story B], [Story C], [Story D]."

**DO** have the session scaffold reference the output files and list every story by name with exact counts. Mark which stories have full trigger/response detail *(detailed)* and which are listed by name only. Use "N detailed + N more = total" counts per sub-epic that sum to the epic total.
- Example (right): Session scaffold says "See `interaction-tree.md` for full trigger/response detail on stories marked *(detailed)*." then lists: "Configure **Abilities** (2 stories): Set **AbilityRank** *(detailed)*, Validate **AbilityRank** *(detailed)*". Epic total: "16 sub-epics, 66 stories".
- Example (right): "Configure **Damage** Powers [MG1] (1 detailed + 4 more = 5 stories): Configure **Damage** *(detailed)*, 4 more following this pattern: Configure **Blast**, Configure **MentalBlast**, Configure **EnergyAura**, Configure **Strike**"
- Example (wrong): "Configure **Damage** Powers | 5 | DamageEffect, ResistanceCheck" — a table row with a count and concept names but no story names, no *(detailed)* markers, no reference to where the full content lives.
- Example (wrong): "~55 stories" when the actual count is 66 — approximate counts lose trust and make it impossible to verify completeness.

**DO NOT** enumerate every story with full detail in the first cut. The first cut is not the finished map — it is the pattern that runs expand.
- Example (wrong): All 6 stories in a sub-epic shown with full Trigger, Response, Pre-Condition, and domain concepts in the first-cut interaction-tree.md. Runs then have nothing to add for that sub-epic.


---

