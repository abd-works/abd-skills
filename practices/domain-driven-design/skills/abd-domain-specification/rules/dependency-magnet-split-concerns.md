# Rule: Dependency magnet — split unrelated business concerns

**Scanner:** Manual review

A class whose **properties, operations, and typed relationships** span **multiple unrelated business concerns** acts as a **dependency magnet**: unrelated domain areas converge on one type, which makes the model brittle and couples changes that should be independent. At domain-specification fidelity, the smell shows up as member clusters that do not share a coherent story — disparate collaborators, unrelated invariants, or operations that read like a cross-cutting checklist. Split by moving coherent groups to focused classes or collaborators (align with any domain model split; if domain model already separated concerns, the typed blocks should mirror that separation).

## DO

- Group members by concern; if one class mixes unrelated areas (for example catalog + billing + notifications), extract types so each class has one coherent responsibility thread. Collaborators and `Interaction:` blocks should tell one story per class.

  **Example (pass):** `Order` exposes coordination; `OrderPricing`, `Shipment`, `PaymentAuthorization` own their operations and properties instead of overloading `Order` with every detail.

## DO NOT

- Leave one class as a hub for unrelated domains with no structural boundary.

  **Example (fail):** A single class exposes tax calculation, email dispatch, inventory validation, and PDF generation — each with different collaborator types and no domain reason for them to share one type.

**Source:** Engagement convention (domain-specification skill).
