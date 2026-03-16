# Phase 9 — Variation Model

**Actor:** AI | 
## Purpose

Model inheritance/strategy/modifier variation.


## Trigger

variation model, inheritance, strategy, variation paths

## Inputs


## Instructions

- **Build inheritance hierarchies from `terms.json`** — scan for subtype candidates (e.g. named Effect subtypes, Check subtypes) rather than relying on background knowledge
- **Build variation paths from `decisions.json`** — conditional branches are in the extracted decisions
- Model Extras/Flaws from `modifiers.json`

## Outputs



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

