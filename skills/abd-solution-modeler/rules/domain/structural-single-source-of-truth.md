---
title: Domain Model — Single Source of Truth
impact: HIGH
---

## No Duplicate Primitive and Relationship for Same Value

**DO** when a concept has its own class with behavior (operations, invariants), reference it through a relationship only. The owning class accesses the value through the relationship. One source of truth.

- Example (right): Order has aggregation to OrderTotal. Order gets the total value through its OrderTotal reference. No redundant `Number total` property on Order.

**DO NOT** have both a primitive property AND a relationship to a class that holds the same value. Two sources of truth create inconsistency.

- Example (wrong): Order has `Number total` property AND an aggregation to OrderTotal class (which has `Number amount`). Two places to get the same value — which is authoritative?
