# Phase 9 — Variation Model

**Actor:** AI | 
## Purpose

Model inheritance/strategy/modifier variation.

**Interaction detail:** Additional detail to interaction based on variation analysis.

## Trigger

variation model, inheritance, strategy, variation paths

## Inputs

`modifiers.json`, `terms.json`, `decisions.json`, `interaction_tree.md`

## Instructions

- **Build inheritance hierarchies from `terms.json`** — scan for subtype candidates (e.g. named Effect subtypes, Check subtypes) rather than relying on background knowledge
- **Build variation paths from `decisions.json`** — conditional branches are in the extracted decisions
- Model Extras/Flaws from `modifiers.json`

## Outputs

`generated/domain/variation_model.md`, `generated/interaction_model/interaction_tree.md`


---

## Domain Model Rules (5)

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
title: Base and Inheritance Check
impact: HIGH
---

## Base and Inheritance Check

### Concepts that share structure — should they extend a common base?

**Check each cluster** for shared protocol and shared invariants. When concepts share:
- (a) cost or acquisition mechanics
- (b) participation in validation (e.g. PL caps)
- (c) lifecycle (bought/allocated during build)
- (d) membership in a parent's collection

…then a common base may be appropriate. Shared protocol: `cost()`, participation in validation, acquisition via budget.

**Look for:**
- Missing base — concepts that share acquisition, cost, and validation role but lack a common supertype
- Over-inheritance — base with no real semantics; subtypes share only fields, not behavior

**Verdict:** Introduce a base when the *role* is the same and variation is in implementation. Avoid over-bias against inheritance when concepts clearly share protocol and invariants.

**DO NOT** defer to future refinement. When concepts share protocol (cost, acquisition, validation role, lifecycle, membership in a parent's collection), introduce the shared base in the current phase. Do not say "consider base in future refinement" when the protocol is shared now.

**AI must propose minimal corrections** (e.g. add CharacterTrait as base for AbilityRank, Defense, Skill, Advantage).


---

---
title: Domain Model — Decompose Mechanically Distinct Variants
impact: HIGH
---

## Decompose Variants by Mechanical Distinction

**DO** when subtypes have fundamentally different properties, operations, or resolution mechanics, decompose into an inheritance hierarchy with invariant examples per subtype. Conversely, when operations differ only by a type discriminator with the same logic, consolidate into a single parameterized operation with a type property.

- Example (right — decompose): Maneuver subtypes have different mechanics — CombatManeuver uses opposed checks and applies Conditions, TradeManeuver adjusts character stats, DefensiveManeuver consumes standard action for defense bonus. Each gets its own class with distinct properties and operations. Variant rules captured as invariant examples (Grab, Trip, Disarm on CombatManeuver; Power Attack, All-out on TradeManeuver).
- Example (right — consolidate): Two operations `from_effect_rank(rank)` and `from_damage_rank(rank)` that differ only in base value → one operation `from_rank(rank, effect_type)` with type property and invariant: `base = 15 when damage, 10 otherwise`.

**DO NOT** collapse mechanically distinct behaviors into a flat class with a type enum when subtypes need different properties and operations. Don't create duplicate operations that differ only by a hardcoded value.

- Example (wrong): `Maneuver` with `ManeuverType {grab, trip, disarm, power_attack, defend}` — five mechanically different things in one class.


---

---
title: Domain Model — Invariants for Rules, Derived Properties Not Getters
impact: HIGH
---

## Rules and Formulas in Invariants, Not Descriptions

**DO** express domain rules, formulas, value mappings, and constraints as explicit invariants. Properties declare type and name only. Operations declare signature only. Model computed/derived values as properties with invariants, not as getter operations.

- Example (right): Property: `Number cost`. Invariant: `cost = rank × 2`. Property: `Number defense_class`. Invariant: `defense_class = 10 + total_bonus`. Property: `Boolean is_natural_20`. Invariant: `is_natural_20 when natural_roll is 20`.

**DO NOT** embed formulas or hardcoded values in property descriptions or operation signatures. Do not model simple derived values as getter operations.

- Example (wrong): `Number value (+2 minor, -2 penalty, +5 major)` — values in description. `Number cost_per_rank (2 power points)` — formula in property. `get_defense_class() → Number` — getter for a derived value. `calculate_cost() → Number (rank × 2)` — formula in operation signature.


---

---
title: Domain Model — Extract Shared Behavior into Base Concepts
impact: HIGH
---

## Shared Behavior and Structure in Base Concepts

**DO** when multiple concepts share the same behavioral pattern or structural pattern, extract a base concept. Place it in the system that owns the behavior, not the system that owns the data. Separate orthogonal concerns into independent bases.

- Example (right): Multiple concepts can "roll a check" → extract `Rollable` in Resolution System with `modifier` and `perform_check()`. Multiple concepts have "rank, cost, power-level limit" → extract `Trait` with shared properties and invariants. Ability combines both: `Ability : Trait, Rollable`. Advantage has rank but isn't rollable: `Advantage : Trait`.

**DO NOT** duplicate behavioral or structural patterns across concepts without a shared base. Do not conflate orthogonal concerns into a single base (e.g., "has rank" and "can be rolled" are separate concerns).

- Example (wrong): Ability, Defense, and Skill each independently declare `Number modifier` and `perform_check()` with no shared base. Or: everything extends `Rollable` even when some concepts (Advantage, Effect) have ranks but can't be rolled.


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

