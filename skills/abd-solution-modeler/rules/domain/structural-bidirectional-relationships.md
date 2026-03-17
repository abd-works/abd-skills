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

- Example (right): Invoice creates Payment (dependency "creates"). Payment has `Invoice source` property (association back). Payment navigates `source.line_items`, `source.customer`. Diagram shows both edges.

**DO NOT** model created objects as isolated snapshots when they need live access to creator state. A copied `Number amount` loses navigation to the creator's line items and customer.

- Example (wrong): Payment has `Number amount` but no reference to the Invoice that created it — can't navigate to line items, customer, or order.
