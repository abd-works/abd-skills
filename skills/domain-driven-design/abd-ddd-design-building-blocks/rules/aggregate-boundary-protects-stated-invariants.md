---
scanner:
---
# Rule: Aggregate boundary protects stated invariants

Every Aggregate in the output must name its root Entity, list its boundary members, and state the invariants the boundary protects. The boundary exists **because** those invariants must hold atomically — not because the concepts happen to be related. Passing means each Aggregate has a defensible reason for its boundary size. Failing means aggregates are drawn by "relatedness" rather than invariant protection, or invariants are missing.

## DO

- Name the root Entity explicitly — it is the single external access point and the invariant enforcer.

  **Example (pass):** "**Root:** Order (Entity) — all status transitions and total-recalculation pass through Order."

- List boundary members and explain why each one is **inside** rather than a separate aggregate referenced by ID.

  **Example (pass):** "**Boundary members:** OrderLine (local identity within Order) — lines cannot exist without the order; the order-total invariant spans all lines."

- State at least one invariant that requires the boundary members to be modified atomically with the root.

  **Example (pass):** "**Protected invariants:** Order total must equal sum of line amounts at all times; status can only advance forward (Draft → Confirmed → Fulfilled)."

- Keep aggregates small — the minimum cluster needed for invariant enforcement.

  **Example (pass):** Customer is a separate Aggregate from Order — no cross-invariant requires them to change atomically, so they are independent aggregates regardless of whether the implementation uses ID references or direct object references.

## DO NOT

- Draw an aggregate boundary around "everything that is related" without stating what invariant requires atomicity.

  **Example (fail):** "**Boundary members:** Customer, Order, OrderLine, Product, Warehouse" — no invariant needs all five to change atomically; this is a relational model, not an aggregate.

- Omit the root or list multiple roots.

  **Example (fail):** "**Root:** Order and OrderLine" — an aggregate has exactly one root Entity.

- State invariants that are actually cross-aggregate eventual-consistency rules as if they required a single boundary.

  **Example (fail):** "**Protected invariants:** Customer's lifetime spend must always equal sum of all orders" — this spans Order and Customer aggregates; it is an eventual-consistency concern, not a single-aggregate invariant.

**Source:** Kept chunks #6, #8 in `inputs/abd-answers-retrieval.md`
