# Phase 7 — Structural Model

**Actor:** AI | 
## Purpose

Add relationships and composition between concepts.

**Interaction detail:** Add Triggering-Actor and Responding-Actor per story; additional stories as gleaned from structure; add long name; initiating and resulting state; pre-conditions.

## Trigger

structural model, relationships, composition, collaborators

## Instructions

- define composition relationships
- attach collaborators

## Inputs

`generated/domain/concept_model.md`, `generated/interaction_model/interaction_tree.md`

## Outputs

`generated/domain/structural_model.md`, `generated/interaction_model/interaction_tree.md`


---

## Domain Model Rules (7)

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

- Example (right): Rollable creates Check (dependency "creates"). Check has `Rollable source` property (association back). Check navigates `source.modifier`, `source.owningCharacter.activeConditions`. Diagram shows both edges.

**DO NOT** model created objects as isolated snapshots when they need live access to creator state. A copied `Number modifier` loses navigation to the creator's owner and state.

- Example (wrong): Check has `Number modifier` but no reference to the Rollable that created it — can't navigate to rank, owning character, or conditions.


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

- Example (right): Character has `Dictionary abilities` (composition). Ability has `Number rank` with invariant `cost = rank × 2`. PowerLevel has `validate_pair(a, b) → Boolean`. Each concept owns its rules — Character just holds references.

**DO NOT** put `configure_X()`, `set_X()`, or orchestration methods on the container that delegate to owned objects. If Ability knows how to compute its cost from its rank, that's Ability's concern.

- Example (wrong): Character has `configure_ability(name, rank) → Ability`, `configure_defense(name, ranks) → Defense`, `validate_power_level() → Boolean`. Character is orchestrating what each part should do instead of letting parts manage themselves.

**Related rules:** [domain-ooa-traverse-from-root](domain-ooa-traverse-from-root.md) — traverse from root; source owns creation. [domain-ooa-model-instances-not-smashed](domain-ooa-model-instances-not-smashed.md) — model instances, not smashed properties.


---

---
title: Domain Model — Single Source of Truth
impact: HIGH
---

## No Duplicate Primitive and Relationship for Same Value

**DO** when a concept has its own class with behavior (operations, invariants), reference it through a relationship only. The owning class accesses the value through the relationship. One source of truth.

- Example (right): Character has aggregation to PowerLevel. Character gets the level value through its PowerLevel reference. No redundant `Number power_level` property on Character.

**DO NOT** have both a primitive property AND a relationship to a class that holds the same value. Two sources of truth create inconsistency.

- Example (wrong): Character has `Number power_level` property AND an aggregation to PowerLevel class (which has `Number level`). Two places to get the same value — which is authoritative?


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

