# Phase 10 — Refined Domain Model

**Actor:** AI | 
## Purpose

Clean structure and finalize modules.

**Interaction detail:** Add Scenarios (group steps by condition), Failure-Modes, Constraints — and examples.

## Trigger

refined domain model, scenarios, failure modes, constraints

## Instructions

- split large classes
- remove fake concepts
- refine module boundaries

## Inputs

`variation_model.md`, `interaction_tree.md`

## Outputs

`generated/domain/refined_domain_model.md`, `generated/interaction_model/interaction_tree.md`

## Checkpoint 5

Human structural validation before proceeding.


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

**DO** integrate related capabilities under a parent concept (e.g. Character Animation with multiple Operations, not separate Walk Animation, Run Animation concepts).

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
title: Failure modes
impact: MEDIUM
---

## Failure modes

**DO** limit failure modes to a maximum of 3 per interaction; derive from domain rules, state conditions, or authorization.
- Example (right): "Insufficient balance"; "Account suspended"; "Cart is empty"; "Payment type not available for country".

**DO NOT** include infrastructure or technical failures.
- Example (wrong): "Database timeout"; "Network unreachable"; "Server crash". Right: "Insufficient balance"; "Account suspended".


---

