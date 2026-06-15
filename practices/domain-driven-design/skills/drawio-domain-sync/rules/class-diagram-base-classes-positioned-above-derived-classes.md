# Rule: Base Classes Positioned Above Derived Classes

**Scanner:** Manual review

A passing diagram positions base (parent) and imported ancestor classes at higher vertical positions (lower y-coordinates) than their derived classes. Inheritance arrows point upward — from child to parent — so the visual hierarchy matches the conceptual hierarchy: readers see the most general abstraction first, then specialisations below. A failing diagram places a derived class at a lower y than its parent, or puts a base class at the bottom of the page with children stacked above it, forcing the reader to scan backwards to find the root of an inheritance chain.

## DO

- Position base and imported classes at the top of the page (low y-value) with derived classes extending downward.

  **Example (pass):** `Rollable` import at y=40, `Check` import at y=180, `AttackCheck` and `DamageResistance` side-by-side at y=400. Inheritance arrows point upward from children to parents.

- Place multiple sibling derived classes at the same y-level, side by side below their shared parent.

  **Example (pass):** `AttackCheck` at (x=40, y=400) and `DamageResistance` at (x=340, y=400) — same row, each pointing up to `Check` at (x=190, y=180).

## DO NOT

- Place a base class below its derived classes.

  **Example (fail):** `AttackCheck` at y=40, `Check` at y=550. Inheritance arrow points downward — readers see the specialisation before the abstraction.

- Mix inheritance depth levels on the same y-row, so a grandchild appears at the same height as its grandparent.

  **Example (fail):** `Rollable` at y=40 and `AttackCheck` (which inherits `Check`, which inherits `Rollable`) also at y=40 on the same page — three levels flattened to one row.
