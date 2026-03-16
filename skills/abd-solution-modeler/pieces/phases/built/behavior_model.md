# Phase 8 — Behavior Model

**Actor:** AI | 
## Purpose

Assign operations to concepts based on interaction steps.

**Interaction detail:** Add Trigger, Response, steps.

## Trigger

behavior model, assign operations, trigger response, pre-condition steps

## Inputs

`generated/interaction_model/interaction_tree.md`, `generated/domain/structural_model.md`

## Outputs

`generated/domain/behavior_model.md`, `generated/interaction_model/interaction_tree.md`


---

## Domain Model Rules (7)

Apply these rules when producing the domain model output for this phase.

---
title: Domain Model — Atomic Operations
impact: HIGH
---

## One Operation = One Behavior

**DO** keep Operations atomic: one Operation = one behavior.

**DO** describe behavior (Acquires, Releases, Calculates, Validates), not outcome (Prevents, Issues).

**DO NOT** pack multiple conditions into one Operation (e.g. "Releases on unlock, redemption complete, or timeout" → split into separate Operations).

**DO NOT** use outcome phrasing (Prevents, Issues) when behavior phrasing is clearer (Acquires, Releases).


---

---
title: Behavior Owns Decision
impact: HIGH
---

# Behavior Owns Decision

Place behavior on the object that owns the data needed for the decision. The information expert should own the rule.

**DO:** Assign decisions, validation, and rule enforcement to the object that holds the state needed to make the decision. If an object has properties, it should also have operations that use those properties.

Example (correct):
```
Account
- Number balance
- can_debit(amount) → balance >= amount
- debit(amount) → enforces invariant, updates balance
```

**DO NOT:** Split data from the logic that operates on it. Objects with properties but no meaningful operations are anemic — the decisions are elsewhere, typically in a service or manager.

Example (wrong):
```
Account
- Number balance
(no operations — debit logic lives in AccountService.debit(account, amount))

AccountService
- debit(account, amount) → checks account.balance >= amount, sets account.balance -= amount
```


---

---
title: Domain Model — Code Representation
impact: MEDIUM
---

## Align to Implementation

**DO** use concise concept names that could exist as types (Order, Portfolio, LineItem).

**DO** use typed Properties and Operations — actual type names (Money, Symbol, Quantity), not prose descriptions.

**DO NOT** use long prose sentences as concept names (e.g. "Collection of customer investments that aggregates all holdings...").

**DO NOT** use prose descriptions for Property or Operation types — use actual type names (e.g. `RiskScore, RiskModel, Holding`, not "detailed object containing volatility calculations").


---

---
title: No Generic Resolvers
impact: HIGH
---

# No Generic Resolvers

Generic resolver, handler, manager, or processor classes that route all behavior through one point are a sign of missing domain abstractions.

**DO:** Create specific domain objects for specific behaviors. If multiple types share a pattern, use polymorphism — each type owns its own behavior.

Example (correct):
```
WireTransfer
- validate() → validates SWIFT code, multi-day settlement rules
- execute() → executes wire-specific settlement

ACHTransfer
- validate() → validates routing number, batch rules
- execute() → executes ACH-specific settlement
```

**DO NOT:** Use generic "resolver" or "handler" classes that route all behavior through one point. These centralize decisions that should be distributed to domain objects.

Example (wrong):
```
TransferResolver
- resolve(type, data) → if type == "wire": ... elif type == "ach": ... elif ...
```


---

---
title: Thin Orchestration
impact: HIGH
---

# Thin Orchestration

Orchestration layers coordinate — they do not decide. Business logic belongs to the object that owns the data needed for the decision.

**DO:** Keep orchestrators thin — they sequence calls, pass messages, and handle lifecycle. Decisions, validation, and rule enforcement live on domain objects.

Example (correct):
```
PaymentProcessor (orchestration)
- process(payment) → delegates to payment.validate(), account.debit(), settlement.execute()

Payment (domain object)
- validate() → owns validation rules
- apply_fees() → owns fee calculation
```

**DO NOT:** Put business logic in orchestrators, managers, or handlers. If an orchestrator is making decisions about domain state, the decision belongs on the domain object instead.

Example (wrong):
```
PaymentProcessor (orchestration)
- process(payment) → checks payment.amount > 0, checks account.balance >= amount, calculates fees, applies discount rules
```


---

---
title: Traverse From Root
impact: HIGH
---

## Traverse From Root

**DO** traverse from root. The source owns creation; the created object receives the source and derives the value internally. Do not pass raw derived values.

**DO NOT** pass raw values when the source object is available.

- Example (wrong): `validation.resolve(source.value)`
- Example (correct): `validation = source.create_validation(dc)` then `validation.resolve()` — validation gets value from source internally.


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



## Interaction Tree Rules (8)

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
title: Alternate actors in steps
impact: HIGH
---

## Alternate actors in steps

Alternate between actors every 1–2 steps. Scenarios should show back-and-forth interaction between user and system.

**DO** alternate actors every 1–2 steps to show interaction flow.
- Actor acts, system responds: `User submits order → System validates payment`
- System completes, actor reacts: `System displays confirmation → User reviews details`
- System can chain 1–2 sequential actions before returning to actor: `User submits form → System validates input → System saves data → System displays result → User confirms`

**DO NOT** have more than 2 consecutive steps from the same actor without switching.
- Example (wrong): `System validates → System processes → System stores → System notifies` — too many consecutive system steps
- Example (wrong): `User enters name → User enters email → User enters password → User clicks submit` — should have system validation between steps


---

---
title: Keep acceptance criteria consistent across connected domains
impact: HIGH
---

## Keep acceptance criteria consistent across connected domains

At small scale, AC can cover multiple domain objects together. As domain objects develop distinct behavior, keep AC consistent in structure across connected domains. AC crossing multiple domain behaviors is a signal to split the story.

**DO** at small scale keep AC together. As you scale, scope AC to one domain and keep structure consistent.
- At small scale, AC covering multiple domain objects together is acceptable: `User submits payment → System validates and routes` — covering wire and ACH together is fine when each has simple, similar validation
- As domain objects develop distinct behavior, scope AC to one domain: `User submits wire payment → System validates intermediary bank and routes to wire rail` — one payment type, one flow
- Keep AC consistent in structure across connected domains: wire and ACH stories both follow the same pattern with domain-specific details as the only variation
- AC crossing multiple domains is the signal to split the story: if an AC mentions both wire validation AND ACH routing, split into two stories

**DO NOT** write AC that mixes domain behaviors or write inconsistent AC across connected domains.
- Example (wrong): `User submits payment → System validates wire rules AND ACH rules AND check rules` — too broad when each has distinct validation
- Example (wrong): Wire story has 5 detailed AC covering every validation step, ACH story has 1 vague AC — keep the depth and structure parallel


---

---
title: Sequential order
impact: HIGH
---

## Sequential order

**DO** order the tree sequentially — required state creators before consumers; follow actual flow, not topic grouping.
- Example (right): Create Character → Set Scenario → Start Turn → Perform Action.

**DO NOT** organize by topic when it violates sequence.
- Example (wrong): "All checks together" or "Run Combat" before "Create Character" or "Set Scenario". Right: Create Character → Set Scenario → Start Turn → Perform Action.


---

---
title: Use And and But for conditions
impact: MEDIUM
---

## Use And and But for conditions

Use **And** for multiple system reactions to one event; use **But** for negative conditions and constraints. Applies to Trigger/Response and steps.
**DO** use And when listing multiple reactions or conditions.
- Right: "Then **System** validates payment **and** displays confirmation".
- Right: "When **User** selects **Country** and **PaymentType**; Then **System** displays form".

**DO** use But for negative conditions and constraints.
- Right: "When **User** has no **Session**; Then **System** redirects to login".
- Right: "**User** has **PaymentType** access **but** not for this **Country**".

**DO NOT** chain positives with But or use And for contrasting conditions.
- Wrong: "Then system validates but displays error" (use And for multiple outcomes, or split into separate steps).
- Wrong: "User has access and not for country" (use But for the negative).


---

