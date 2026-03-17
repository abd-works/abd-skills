---
title: Mechanics from evidence, not table of contents
impact: HIGH
---

## Mechanics from evidence, not table of contents

**DO** read evidence chunks for mechanical depth. For each candidate subtype, scan actions.json and terms.json for that name. Derive properties, operations, and collaborators from what the evidence says that variant does. A subtype is justified when the evidence describes different rules, formulas, state transitions, or interaction patterns.

**DO** verify each subtype has its own trigger, conditions, or resolution path in the source. Different mechanics = subtype. Same mechanics with different label = enum.

**DO NOT** infer subtypes from chapter titles, section headers, or bullet lists without reading the actual rule text. A table of contents that lists "Volume Discount, Loyalty Reward, Bundle Offer" under Promotions does not make them subtypes — only the rules for each do.

**DO NOT** create subtypes from variation axes or category lists when each item shares the same resolution logic. "Transaction types: Purchase, Return, Exchange" in a summary is a categorization; read the rules to see if each resolves differently.

- Example (wrong): Source has section "Transaction Types" with Purchase, Return, Exchange. You list those as subtypes. But the ToC categories are wrong — the mechanics show different resolution types (e.g. forward payment vs reversal vs disputed reversal). Right: Read the rules. Derive subtypes from resolution mechanics, not from ToC labels.
- Example (wrong): Source lists "Payment Methods: Credit Card, Bank Transfer, Invoice" and you model each as a subtype because they use different rails. But the mechanics are identical — same flow, different input. Right: PaymentMethod with `method_type {credit_card, bank_transfer, invoice}` — data field, not subtypes. Same mechanics with different input = variable, not subtype.
