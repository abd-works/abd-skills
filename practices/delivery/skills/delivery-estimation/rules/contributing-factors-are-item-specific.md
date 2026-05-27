---
scanner: ~
---
# Rule: Contributing factors are item-specific not boilerplate

Each estimate record's contributing-factor breakdown must reflect the reality of **that specific scope item**, not a copy-paste of the same scores across every record. Factors exist to show where effort concentrates for each item — when every row reads identically, the factors are decoration, not analysis. Passing means a reviewer can read the factor breakdown and learn something specific about the item's effort profile. Failing means factors are generic filler that could apply to any item in the backlog.

## DO

- Score or note each contributing factor based on what is actually true for this scope item — different items should show different factor profiles.

  **Example (pass):**

  | Factor | Score / Note |
  | --- | --- |
  | Technical complexity | High — shelter API integration, multi-step submission |
  | Domain uncertainty | Medium — adoption rules known but shelter validation rules undocumented |
  | External dependencies | High — shelter API contract not finalized |

  Each cell names concrete reasons tied to this item.

- Add or remove factors mid-session when an item reveals a dimension the catalog did not anticipate, and note the addition.

  **Example (pass):** Estimate record for item 5 adds "payment latency" as a new factor with the note: "Added mid-session — payment gateway response time affects confirmation flow."

## DO NOT

- Copy the same factor scores across every estimate record without differentiation.

  **Example (fail):** Five estimate records all show "Technical complexity: Medium, Domain uncertainty: Medium, External dependencies: Low" with identical wording — the factors do not distinguish one item from another.

- Use only single-word scores ("High", "Low") with no explanation of why that score applies to this item.

  **Example (fail):**

  | Factor | Score / Note |
  | --- | --- |
  | Technical complexity | High |
  | Domain uncertainty | Medium |
  | External dependencies | High |

  No indication of what makes complexity "High" for this item specifically.

**Source:** Engagement convention (delivery-estimation rough requirements — "record contributing factors", "new data added to contributing factor").
