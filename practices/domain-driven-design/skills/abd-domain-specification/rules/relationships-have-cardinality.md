
# Rule: Relationships have two named ends and cardinality

Every relationship in a domain-model block must name both ends and state cardinality (`1..1`, `0..1`, `1..*`, `0..*`). Direction must match the domain model collaborator that sourced it. Passing means both ends, cardinality, and direction are present and traceable. Failing means an end is unnamed, cardinality is missing, or the direction contradicts the domain model collaborator line.

## DO

- State both class names, the relationship kind (composition or association), and cardinality on both ends.

  **Example (pass):**
  ```
  Order *composes* OrderLine  [1..1 ? 1..*]
  ```

- Derive direction from the domain model collaborator entry — the class that lists the collaborator is the navigating end.

  **Example (pass):**
  ```
  domain model — Order collaborates with OrderLine
  ? Order navigates to OrderLine, not the reverse
  ```

## DO NOT

- Write a relationship with only one end named.

  **Example (fail):**
  ```
  *composes* OrderLine  [1..*]    ? owning end missing
  ```

- Omit cardinality entirely.

  **Example (fail):**
  ```
  Order *associates* Customer     ? no cardinality on either end
  ```

- Reverse the direction from what the domain model collaborator line states.

  **Example (fail):**
  ```
  domain model — Order collaborates with Customer
  Relationship written as: Customer *associates* Order  ? direction flipped
  ```
