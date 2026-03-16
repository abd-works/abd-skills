# Phase 7 — Structural Model

**Actor:** AI | 
## Purpose

Add relationships and composition between concepts.


## Trigger

structural model, relationships, composition, collaborators

## Instructions

- define composition relationships
- attach collaborators
- **Ground relationships in `evidence/relationships.json`** — scan the relationship evidence for `from_entity` → `type` → `to_entity` patterns. Only add relationships that evidence supports. Cite the evidence (e.g. `[rel_0042: "raw text"]`).
- **Use `evidence/states.json` for state-based relationships** — states describe what conditions/states concepts can be in, which reveals lifecycle and escalation relationships.
- **Use `evidence/decisions.json` for conditional relationships** — decisions describe when/if/must/cannot rules that reveal invariants and dependencies between concepts.

## Inputs


## Outputs



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

| Pattern | Description | Domain Model mapping |
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

