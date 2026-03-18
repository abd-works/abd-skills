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

# Phase 5 — Concept Synthesis

**Actor:** AI

## Purpose

Curate the concept list from Phase 4 (merge/split/kill), build hierarchy, allocate evidence. Reads source chunks via `chunk_ids` for semantic understanding.

## Trigger

concept synthesis, curate concepts, refine hypothesis, merge split kill, build hierarchy

## Inputs

- `generated/hypothesis.json` — concept index from Phase 4 (concepts, registries, concept_guidance, chunk_ids per concept)
- `context/` — source chunks (read via chunk_ids for semantic understanding)

## Instructions

1. **Curate concepts** — Merge duplicates, split overloaded concepts, remove noise. Use `chunk_ids` to read relevant source chunks; do not guess from chunks alone.
2. **Build concept_hierarchy** — Derive parent-child from evidence (shared mechanics, shared protocol, subtype patterns). See rules for hierarchy-from-evidence.
3. **Update concept_guidance** — priority_concepts, concept_aliases, mechanisms, actors, variation_axes, noise_filters.
4. **Allocate evidence** — Ensure term_ids, performs, receives, states, decisions, relationships are correctly assigned to curated concepts.

Subtype discovery happens here; Phase 10 (Variation) works with concepts that already exist.

## Outputs

- `generated/hypothesis.json` (refined) — concept_hierarchy, updated concept_guidance, evidence allocation

## Run

```bash
python scripts/pipeline.py generate concept_synthesis
```


---

## Domain Model Rules (15)

Apply these rules when producing the domain model output for this phase.

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

**Related rules:** [concept_synthesis-subtypes-first-class](concept_synthesis-subtypes-first-class.md), [variation-base-inheritance](variation-base-inheritance.md), [domain-mechanics-not-toc](domain-mechanics-not-toc.md), [refined-integrate-concepts](refined-integrate-concepts.md).


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



## Interaction Tree Rules (6)

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



## Hypothesis Rules (10)

Apply these rules when producing hypothesis.json for this phase.

---
phases: [concept_synthesis]
order: 10
---

## Merge alias concepts into canonical

**DO** merge alias concepts into their canonical using `concept_guidance.concept_aliases`. If concept_aliases has "Account": ["ACCT"], then concepts must NOT contain both "ACCT" and "Account" as separate entries.

**DO NOT** leave abbreviation concepts (ACCT, REV, CUST, SKU, etc.) as separate concepts when concept_aliases maps them to a canonical.


---

---
phases: [concept_synthesis]
order: 20
---

## No extraction artifacts as concepts

**DO NOT** leave extraction artifacts as separate concepts: "All Transactions", "All Orders", "Rev", "Cust", "Compli", "Transac", "COST PER ITEM An".

**DO** merge "All X" → "X", truncations → full form, fragments → cleaned form.


---

---
phases: [concept_synthesis]
order: 30
---

## No nonsense concepts

**DO NOT** leave non-words, typos, proper nouns, or garbage as concepts. Remove: Smith, Choose, Choose One, Although, Because, McDonald, Acme Corp.

**DO** remove instruction phrases mistaken for concepts ("Choose", "Select One" from rule text).


---

---
phases: [concept_synthesis]
order: 40
---

## No section headers as concepts

**DO NOT** leave section headers, ToC labels, or structural categories as concepts. Remove: BALANCE SHEET, INCOME STATEMENT, CHECKOUT, PRODUCT CATALOG, COST PER ITEM, THE BASICS, SERVICE TIERS.

**DO** remove concepts that are structural labels rather than domain entities.


---

---
phases: [concept_synthesis]
order: 50
---

## Merge singular/plural variants

**DO** merge singular/plural variants into one canonical (usually singular). Do NOT leave both "Account" and "Accounts", "Order" and "Orders", "Customer" and "Customers" as separate concepts.


---

---
phases: [concept_synthesis]
order: 60
---

## Actions reference valid concepts

**DO** ensure every action's subject and object (when non-empty) reference a concept in the concepts dict. Orphan references (subject/object not in concepts) indicate merged/removed concepts whose actions were not updated.


---

---
phases: [concept_synthesis]
order: 70
---

## All concepts have evidence

**DO** ensure each concept has at least one of: term_ids, chunk_ids, performs, receives. Concepts with no evidence are noise and should be removed.


---

---
phases: [concept_synthesis]
order: 80
---

## Concept names are valid domain terms

**DO NOT** use single instruction verbs (Choose, Apply, Because) or article+noun fragments ("A Transaction", "The Balance") as concept names.

**DO** use domain nouns or noun phrases (Account, Order, Subscription, Customer).


---

---
phases: [concept_synthesis]
order: 90
---

## concept_hierarchy derived from evidence

**DO** build concept_hierarchy from evidence (shared mechanics, co-occurrence in actions, subtype patterns). Parent and child names must exist in concepts.

**DO NOT** infer hierarchy from chapter titles or ToC alone.


---

---
phases: [concept_synthesis]
order: 95
---

## performs/receives match actions registry

**DO** ensure each concept's performs list contains only act_ids where that concept is subject; receives only act_ids where that concept is object. After merge/remove, rebuild performs/receives from actions.


---

