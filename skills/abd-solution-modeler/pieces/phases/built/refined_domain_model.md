# Phase 10 — Refined Domain Model

**Actor:** AI | 
## Purpose

Clean structure and finalize modules.


## Trigger

refined domain model, scenarios, failure modes, constraints

## Instructions

- split large classes
- remove fake concepts
- refine module boundaries

## Inputs


## Outputs


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

