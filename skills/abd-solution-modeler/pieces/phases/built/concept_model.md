# Phase 6 — Concept Model

**Actor:** AI | 
## Purpose

Identify core concepts and modules. Convert refined concepts into class-like model.


## Trigger

concept model, core concepts, link concepts to stories

## Inputs


## Instructions

- Convert refined concepts into class-like model with properties and operations
- **Ground properties and operations in `evidence/terms.json` and `evidence/actions.json`** — do not invent from background knowledge; use extracted evidence to confirm what each concept actually does
- **Cite evidence** — for each property and operation, include the evidence ID or raw text snippet that supports it (e.g. `[act_0042: "raw text"]`). If you cannot find evidence for a property/operation, mark it `[UNGROUNDED]` and consider removing it.
- **Read the concept guidance first** — the concept guidance describes what each concept does in interaction-oriented terms. Convert those descriptions into properties and operations. Do not skip concepts from the guidance.
- **Use `concept_hierarchy` as starting point** — the guidance JSON contains `concept_hierarchy` with subtypes and related concepts. Use this as the initial inheritance and composition map. Subtypes become `: Parent` concepts in the model. Related concepts become collaborators. Do not rediscover hierarchy from scratch — refine what guidance provides.
- **Read evidence files per concept** — for each concept, scan actions.json for entries where `matched_concepts` includes that concept name, and scan terms.json for the concept's term entry. Use the `raw` field text to derive properties and invariants.
- **Do not substitute background knowledge** — if the evidence says "X works like Y", model what the evidence says, not what you know about X from training data. The evidence may be from a domain you've seen before, but this model must reflect THIS source material's rules, not the canonical rules.

## Outputs



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

