---
title: Domain Model — Extract Shared Behavior into Base Concepts
impact: HIGH
---

## Shared Behavior and Structure in Base Concepts

**DO** when multiple concepts share the same behavioral pattern or structural pattern, extract a base concept. Place it in the system that owns the behavior, not the system that owns the data. Separate orthogonal concerns into independent bases.

- Example (right): Multiple concepts can "validate" → extract `Validatable` with `validate()` and `validation_rules`. Multiple concepts have "amount, currency, status" → extract `FinancialRecord` with shared properties and invariants. Invoice combines both: `Invoice : FinancialRecord, Validatable`. Order has amount but different validation: `Order : FinancialRecord`.

**DO NOT** duplicate behavioral or structural patterns across concepts without a shared base. Do not conflate orthogonal concerns into a single base (e.g., "has amount" and "can validate" are separate concerns).

- Example (wrong): Invoice, Order, and Payment each independently declare `validate()` and `validation_rules` with no shared base. Or: everything extends `Validatable` even when some concepts have amounts but no validation.
