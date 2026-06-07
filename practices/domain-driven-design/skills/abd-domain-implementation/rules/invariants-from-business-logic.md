# Rule: Invariant lines trace to domain model invariants or always-true rules

Every `Invariant: ...` line under a member must be sourced from the domain model `invariants:` field of the corresponding concept. Passing means each invariant is short, tab-indented under the member it constrains, and traceable to the domain model block. Failing means an invariant is invented, placed outside a member context, or contradicts the domain model source.

## DO

- Write each invariant as a single tab-indented line directly under the property or operation it constrains, sourced from the domain model `invariants:` field.

  **Example (pass):**
  ```
  + remainingBudget: Money
  	Invariant: remainingBudget = 0 (from: "budget must never go negative")
  ```

- Keep invariants declarative — "must", "cannot", "only if" — matching the domain model phrasing.

  **Example (pass):**
  ```
  + ship(destination: Address): void
  	Invariant: cannot ship unless paymentCleared is true
  ```

## DO NOT

- Invent an invariant that has no corresponding domain model `invariants:` line.

  **Example (fail):**
  ```
  + quantity: Integer
  	Invariant: quantity must be a prime number   ? no domain model source
  ```

- Place an invariant as a free-standing line outside any member context.

  **Example (fail):**
  ```
  Invariant: total must match sum of line items
  + totalPrice: Money                             ? invariant floats above, not under a member
  ```

- Write multi-line prose instead of a single declarative constraint.

  **Example (fail):**
  ```
  + status: OrderStatus
  	Invariant: When the order transitions from pending to confirmed
  	           the system must verify that all line items are in stock
  	           ? too long; split into atomic invariants or keep prose in domain model
  ```
