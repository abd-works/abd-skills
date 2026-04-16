# Rule: Review and Expand Stories

**Priority:** 14  
**Scanner:** Manual review (policy; P14 vs P13 — see below)


When planning calls for **system stories** or explicit **component interactions**, **decompose** existing stories into those interactions. Story count **will increase**.

**Relationship to other rules:** P14 expands by **component behavior** (different behaviors inside one flow). P13 (*Consolidate Superficial Stories*) merges **same logic, different data**. Apply **P13 first**, then **P14** where needed.

## DO

- With System / Technology / Infrastructure emphasis, split user stories into **user action + system/component** stories (e.g. `User --> group tokens`, `System --> create mob`, `System --> assign mob leader`).
- **Review** existing stories and add component steps for payment, validation, inventory, etc., when the approach requires it.
- Break flows into **discrete system steps** when the plan demands (e.g. `validate payment` → `call payment gateway` → `persist transaction` → `confirm payment`).

## DON'T

- Keep **one** user story when the approach requires visible **component** interactions.
- Assume story count stays fixed after switching to a **finer** system/component approach — expect a larger map.
