---
title: Subtypes as first-class concepts
impact: HIGH
---

## Subtypes as first-class concepts

**DO** give each subtype its own `### **SubtypeName** : Parent` section with its own properties, operations, collaborators, and composition. Subtypes inherit from parent but have distinct mechanics — model those mechanics explicitly.

**DO** ground each subtype's definition in evidence. Scan `actions.json` and `terms.json` for the subtype name (e.g. Purchase, Refund, Chargeback) and derive properties/operations from what the evidence says that subtype does.

**DO NOT** list subtypes only in a parent's `Subtypes:` line without creating first-class sections for them.

**DO NOT** collapse subtypes that have distinct rules (e.g. Purchase vs Refund vs Chargeback each have different validation, settlement, reversal) into a single parent definition.

- Example (wrong): `### **Transaction**` with `Subtypes: Purchase, Refund, Chargeback` and no separate sections for Purchase, Refund, Chargeback.
- Example (right): `### **Transaction**` plus `### **Purchase** : Transaction`, `### **Refund** : Transaction`, `### **Chargeback** : Transaction`, etc., each with its own properties, operations, and collaborators.
