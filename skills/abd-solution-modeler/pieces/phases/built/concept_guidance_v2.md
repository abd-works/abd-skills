# Phase 5 — Concept Guidance v2

**Actor:** AI | 
## Purpose

Refine domain structure using evidence graph.

**Domain detail:** Refined concepts, modules.


## Trigger

refine concepts, concept guidance v2, second-cut domain, epics and stories, refine structure, story placement

## Inputs


## Instructions

### Domain
- merge duplicate concepts
- split overloaded concepts
- **detect hidden concepts by scanning `evidence/terms.json`** — do not rely on background knowledge; surface terms that appear frequently but are not yet in the concept list
- **coverage check per module** — for each module, read `context/context_chunks.json` chunks that mention module concepts and verify EVERY distinct subsystem, variant, or mechanic in those chunks is named as a concept. If a chunk describes a mechanic with its own trigger, its own conditions, its own state transitions, or its own interaction rules and it's not in the concept list, add it. Do not stop at the top 20-30 terms; scan the FULL term list.
- **split overloaded variation axes** — if a variation axis from v1 (e.g. "payment method: Credit, Debit, Wire, Wallet") lists items that each have distinct mechanics (own validation, own settlement, own fee rules), promote each to a separate concept. A variation axis is for cosmetic variants (visa vs mastercard branding); a concept is for mechanical variants (CreditPayment vs WireTransfer vs DigitalWallet).
- **check for missing category concepts** — scan evidence for grouping patterns (e.g. "standard plans", "enterprise plans", "custom plans"). If each group has different rules, eligibility, or pricing mechanics, each group is a concept.
- **check for missing interaction concepts** — scan evidence for interaction variants with distinct mechanics (e.g. batch processing vs real-time processing, synchronous vs asynchronous flows, approval workflows vs auto-approval). If each variant has its own rules, it's a concept.
- refine modules — a module should be created when a subsystem has its own internal concepts, interactions, and rules (e.g. a dispute resolution subsystem with dispute types, escalation stages, and resolution outcomes is a module, not a line item under Billing)
- refine operations cautiously
- **alias cleanup** — remove any aliases that are 2-3 characters long or common English words. These poison extraction with false positives.
- **refine concept hierarchy** — review the `concept_hierarchy` from v1. Check that subtypes are correctly placed under their parent. Split subtypes that are too broad; merge subtypes that are really the same mechanic with a different name. Add new subtypes surfaced by evidence. Update `-> related:` links based on evidence relationships. Ensure every subtype still appears in `priority_concepts`.

- refine epic structure from v1
- add sub-epics under each epic
- place story names under sub-epics where evident
- Epics, Sub-Epics, some stories where possible — defer Trigger, Response, scenarios, steps to later phases
- **scan `performs` edges in `evidence/evidence_graph.json` for predicate clusters** — groups of verbs (e.g. grab, restrain, choke, redirect) that don't map to any existing epic indicate a missing epic or sub-epic; do not assume the v1 epic list is complete

## Outputs



---

## Domain Model Rules (2)

Apply these rules when producing the domain model output for this phase.

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
title: Derive from context
impact: HIGH
---

## Derive from context

**DO** derive concepts from the interactions you find in the context; focus on *who* exchanges *what* and *what must be true before and after*.
- Example (right): Context says "Customer adds to cart" → interaction: Add to Cart; concepts: Shopping Cart, LineItem. Context says "User selects country for payment" → interaction: Select Country; concepts: Country, PaymentType.

**DO NOT** invent workflows or mechanics not present in the context.
- Example (wrong): Story "Express checkout" or concept "LoyaltyPoints" when context never mentions them. Right: Omit; if needed, state assumption.


---

