# Rule: Cross-Model Ancestors Shown on Page

**Scanner:** Manual review

When a page's local concepts extend or use concepts that belong to a different Key Abstraction, the full ancestor chain from that other KA must appear at the top of the page as imported classes (dashed border, `«from: KA Name»` stereotype). A passing diagram lets the reader trace the complete ancestry without leaving the page. A failing diagram shows only the immediate imported parent while omitting the grandparent that explains where the parent comes from, leaving an incomplete ancestry chain.

## DO

- Import every ancestor class needed to understand the full ancestry chain, including grandparents, at the top of the page.

  **Example (pass):** An Attack-and-Damage page imports both `Rollable [from: Resolution System]` and `Check [from: Resolution System]`, with a `creates` dependency edge from `Rollable` to `Check`. The reader sees the full chain: `Rollable → Check → AttackCheck / DamageResistance`.

- Render imported classes with a dashed border and a `«from: KA Name»` stereotype label placed above the class name.

  **Example (pass):** `add-class … --imported-from "Resolution System"` produces a dashed-border box with stereotype `«from: Resolution System»` shown above `Rollable`.

- Show only the key properties on an imported class — enough to recognise it; full detail stays on the home-KA page.

  **Example (pass):** Imported `Check` shows `+ modifier: Integer` and `+ degree: Degree` only. Full operations and invariants are not duplicated.

## DO NOT

- Show only the immediate imported parent while omitting the grandparent that establishes context.

  **Example (fail):** Attack-and-Damage page imports `Check` but not `Rollable` — the reader cannot see that `Check` originates from `Rollable.perform_check()` and cannot understand where the `Check` concept comes from.

- Render an imported class as a normal solid-border class indistinguishable from local classes.

  **Example (fail):** `Rollable` appears with a solid border and no stereotype on the Attack-and-Damage page — readers cannot tell it belongs to a different KA.
