
# Rule: Every property traces to a CRC responsibility

Every property in a domain-model block must be justified by a "Responsible for" line in the corresponding CRC class. Passing means each property answers the question *what must this class remember to fulfil that responsibility?* Failing means a property appears with no CRC backing, or a CRC responsibility that implies stored state has no matching property.

## DO

- Derive each property from a specific "Responsible for" line and type it where the domain makes the type obvious.

  **Example (pass):**
  ```
  CRC — Responsible for: tracking the total price of the order

  Domain-model block:
  + totalPrice: Money
  ```

- Include at least one property for every CRC class that owns domain behavior.

  **Example (pass):** A CRC class with three "Responsible for" lines produces a domain-model block with three or more properties, each traceable to one of those lines.

## DO NOT

- Add a property that has no corresponding CRC responsibility.

  **Example (fail):**
  ```
  CRC — (no mention of "color")

  Domain-model block:
  + color: String       ← invented, not sourced from CRC
  ```

- Leave a CRC class that holds state without any domain-model properties.

  **Example (fail):** A CRC class is "Responsible for: maintaining the remaining budget" but its domain-model block has zero properties — the stored state was never surfaced.
