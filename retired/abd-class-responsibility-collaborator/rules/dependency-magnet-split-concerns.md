# Rule: Dependency magnet — split unrelated business concerns

**Scanner:** Manual review

A concept whose responsibilities and collaborators span **multiple unrelated business concerns** (distinct domain areas that do not share a coherent purpose) behaves as a **dependency magnet**: it accumulates collaborators and responsibilities from different "worlds" and becomes hard to change or test. When you see that pattern during CRC, split by moving coherent groups of responsibilities to focused concepts or to appropriate collaborators — before the Class Model hardens the overload.

## DO

- Group responsibilities by concern; if a single concept mixes concerns (for example catalog + billing + shipping language on one card), extract or reassign so each concept owns one coherent thread.

  **Example (pass):** `Order` coordinates fulfillment; `Pricing`, `Shipment`, and `Payment` hold their own rules and collaborators instead of every rule living on `Order`.

- Use the collaborator column as a smell: a wide, heterogeneous list (many unrelated domain types with no single behavior story) often signals a magnet.

## DO NOT

- Leave one concept owning checklist-style responsibilities that read like unrelated stakeholder requests stapled together.

  **Example (fail):** One CRC card owns "calculate tax," "send email," "validate inventory," and "render PDF" with collaborators from messaging, tax, inventory, and document domains — none of which share a natural domain boundary.

**Source:** Engagement convention (class-responsibility-collaborator skill).
