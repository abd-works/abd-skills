---
title: Hierarchy from evidence, not invention
impact: HIGH
---

## Build concept_hierarchy from evidence

**DO** derive parent-child relationships from evidence in `registries.actions` and concept `performs`/`receives`:
- **Shared mechanics** — concepts that share the same resolution, cost, or validation role (e.g. Wire Transfer, ACH, Card Payment all resolve as Payment; Checking, Savings, Money Market → Account) → Child → Parent
- **Shared protocol** — concepts that participate in the same workflow, lifecycle, or parent's collection → introduce a common base
- **Subtype patterns** — when evidence describes different rules, formulas, or state transitions for variants → model as Child : Parent

**DO** scan actions for each concept: subject, object, predicate, raw. Look for:
- Co-occurrence (concepts that appear together as subject/object)
- Shared terminology (term_ids, chunk_ids overlap)
- Domain language (e.g. "Transaction", "Account", "Payment", "Fee", "Product", "Order" in raw text)

**DO** build a **comprehensive** hierarchy. With hundreds of concepts, expect many parent types: Transaction, Account, Payment, Fee, Product, Order, Customer, etc. Each parent should have all its subtypes listed.

**DO NOT** infer hierarchy from chapter titles, section headers, or ToC alone. Read the raw action text to confirm different mechanics.

**DO NOT** leave hierarchy sparse. If you have 10+ concepts that share mechanics (e.g. Wire Transfer, ACH, Card Payment → Payment; Checking, Savings → Account), add them. If you have Transaction subtypes beyond Purchase/Refund/Chargeback, add them.

**Related rules:** [concept-model-subtypes-first-class](concept-model-subtypes-first-class.md), [variation-base-inheritance](variation-base-inheritance.md), [domain-mechanics-not-toc](domain-mechanics-not-toc.md), [refined-integrate-concepts](refined-integrate-concepts.md).
