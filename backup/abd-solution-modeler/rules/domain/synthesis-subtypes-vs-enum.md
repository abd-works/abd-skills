---
title: Subtypes vs enum — verify before modeling
impact: HIGH
---

## Subtypes vs enum — verify before modeling

**DO** before creating a subtype section: verify actions.json and terms.json show different mechanics for that subtype. Different properties, operations, or resolution paths = subtype. Same logic, different label = enum on parent.

**DO** use `EnumType property_name {value1, value2}` when the evidence shows same behavior across variants. Do not create subtype sections for enum-like variation.

**DO NOT** create subtype sections from concept_hierarchy without evidence check. If concept_guidance listed Purchase, Refund, Chargeback as Transaction subtypes but the evidence treats them identically (same validation, same settlement flow), convert to `TransactionType type {purchase, refund, chargeback}` on Transaction.

**DO NOT** have both a type enum and mirroring subtypes. If Transaction has `TransactionType type {purchase, refund, chargeback}`, do not also create Purchase, Refund, Chargeback as subtypes.

- Example (right): Transaction has Purchase, Refund, Chargeback as subtypes — evidence shows Purchase has forward-payment validation, Refund has reversal rules and original-required check, Chargeback has issuer workflow. Each has distinct mechanics.
- Example (wrong): Transaction has Purchase, Return, Exchange as subtypes when the rules only categorize by label. Right: Transaction with `TransactionType type {purchase, return, exchange}`.
