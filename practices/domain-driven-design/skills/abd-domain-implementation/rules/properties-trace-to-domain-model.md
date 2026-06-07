
# Rule: Every property traces to a domain model responsibility

Every property in a domain-model block must be justified by a "Responsible for" line in the corresponding domain model class. Passing means each property answers the question *what must this class remember to fulfil that responsibility?* Failing means a property appears with no domain model backing, or a domain model responsibility that implies stored state has no matching property.

## DO

- Derive each property from a specific "Responsible for" line and type it where the domain makes the type obvious.

  **Example (pass):**
  ```
  domain model — Responsible for: tracking the total price of the order

  Domain-model block:
  + totalPrice: Money
  ```

- Include at least one property for every domain model class that owns domain behavior.

  **Example (pass):** a domain model class with three "Responsible for" lines produces a domain-model block with three or more properties, each traceable to one of those lines.

## DO NOT

- Add a property that has no corresponding domain model responsibility.

  **Example (fail):**
  ```
  domain model — (no mention of "color")

  Domain-model block:
  + color: String       ? invented, not sourced from the domain model
  ```

- Leave a domain model class that holds state without any domain-model properties.

  **Example (fail):** a domain model class is "Responsible for: maintaining the remaining budget" but its domain-model block has zero properties — the stored state was never surfaced.
