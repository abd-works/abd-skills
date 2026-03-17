---
title: Domain Model — Parts Manage Their Own State
impact: HIGH
---

## Parts Manage Their Own State

**DO** let each concept manage its own properties through its own invariants. A container holds references to its parts (composition/aggregation) but does not orchestrate their configuration. Each part knows its own rules.

- Example (right): Order has `Dictionary line_items` (composition). LineItem has `Number quantity` with invariant `subtotal = quantity × unit_price`. OrderTotal has `validate_threshold(min) → Boolean`. Each concept owns its rules — Order just holds references.

**DO NOT** put `configure_X()`, `set_X()`, or orchestration methods on the container that delegate to owned objects. If LineItem knows how to compute its subtotal from quantity and price, that's LineItem's concern.

- Example (wrong): Order has `configure_line_item(sku, qty) → LineItem`, `configure_payment(method, amount) → Payment`, `validate_order_total() → Boolean`. Order is orchestrating what each part should do instead of letting parts manage themselves.

**Related rules:** [domain-ooa-traverse-from-root](domain-ooa-traverse-from-root.md) — traverse from root; source owns creation. [domain-ooa-model-instances-not-smashed](domain-ooa-model-instances-not-smashed.md) — model instances, not smashed properties.
