---
title: Domain Model — Decompose Mechanically Distinct Variants
impact: HIGH
---

## Decompose Variants by Mechanical Distinction

**DO** when subtypes have fundamentally different properties, operations, or resolution mechanics, decompose into an inheritance hierarchy with invariant examples per subtype. Conversely, when operations differ only by a type discriminator with the same logic, consolidate into a single parameterized operation with a type property.

- Example (right — decompose): Promotion subtypes have different mechanics — VolumeDiscount uses tier-based calc, LoyaltyReward uses points logic, BundleOffer has bundle rules. Each gets its own class with distinct properties and operations. Variant rules captured as invariant examples.
- Example (right — consolidate): Two operations `price_for_quantity(qty)` and `price_for_weight(kg)` that differ only by unit → one operation `price_from_amount(amount, unit)` with unit property and invariant: `base = 100 when unit=kg, 10 when unit=each`.

**DO NOT** collapse mechanically distinct behaviors into a flat class with a type enum when subtypes need different properties and operations. Don't create duplicate operations that differ only by a hardcoded value.

- Example (wrong): `Promotion` with `PromotionType {volume_discount, loyalty_reward, bundle, clearance}` — four mechanically different things in one class.
