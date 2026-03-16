# Phase 6 — Concept Model

**Actor:** AI | 
## Purpose

Identify core concepts and modules. Convert refined concepts into class-like model.

**Interaction detail:** Same depth as concept guidance but more fleshed out; more sub-epics; epics can have stories. Link concepts to stories. No Trigger, Response, steps yet.

## Trigger

concept model, core concepts, link concepts to stories

## Inputs

`generated/domain/concept_guidance.md`, `evidence/terms.json`, `evidence/actions.json`, `generated/interaction_model/interaction_tree.md`

## Instructions

- Convert refined concepts into class-like model with properties and operations
- **Ground properties and operations in `evidence/terms.json` and `evidence/actions.json`** — do not invent from background knowledge; use extracted evidence to confirm what each concept actually does

## Outputs

`generated/domain/concept_model.md`, `generated/interaction_model/interaction_tree.md`


---

## Domain Model Rules (3)

Apply these rules when producing the domain model output for this phase.

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
title: Derive from context
impact: HIGH
---

## Derive from context

**DO** derive concepts from the interactions you find in the context; focus on *who* exchanges *what* and *what must be true before and after*.
- Example (right): Context says "Customer adds to cart" → interaction: Add to Cart; concepts: Shopping Cart, LineItem. Context says "User selects country for payment" → interaction: Select Country; concepts: Country, PaymentType.

**DO NOT** invent workflows or mechanics not present in the context.
- Example (wrong): Story "Express checkout" or concept "LoyaltyPoints" when context never mentions them. Right: Omit; if needed, state assumption.


---



## Interaction Tree Rules (5)

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

