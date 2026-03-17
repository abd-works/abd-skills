---
title: Domain Model — Invariants for Rules, Derived Properties Not Getters
impact: HIGH
---

## Rules and Formulas in Invariants, Not Descriptions

**DO** express domain rules, formulas, value mappings, and constraints as explicit invariants. Properties declare type and name only. Operations declare signature only. Model computed/derived values as properties with invariants, not as getter operations.

- Example (right): Property: `Number amount`. Invariant: `amount >= 0`. Property: `Number discount_percent`. Invariant: `discount_percent <= 100`. Property: `Boolean is_eligible`. Invariant: `is_eligible when order_total >= min_threshold`.

**DO NOT** embed formulas or hardcoded values in property descriptions or operation signatures. Do not model simple derived values as getter operations.

- Example (wrong): `Number value (+2 minor, -2 penalty, +5 major)` — values in description. `Number cost_per_unit (2.50)` — formula in property. `get_total()` — getter for a derived value. `calculate_discount() → Number (qty × 0.1)` — formula in operation signature.
