
# Rule: Operations use typed signatures tracing to domain model verbs

Every operation must be written as a typed method signature — `methodName(param: Type): ReturnType` — and must trace to a domain model responsibility verb phrase. Passing means the signature is complete and the source verb phrase is identifiable. Failing means the operation lacks types, uses prose instead of a signature, or has no domain model verb-phrase origin.

## DO

- Write each operation as `+ methodName(param: Type): ReturnType`, derived from a domain model "Responsible for" verb phrase.

  **Example (pass):**
  ```
  domain model — Responsible for: calculating shipping cost based on weight and destination

  Domain-model block:
  + calculateShippingCost(weight: Weight, destination: Address): Money
  ```

- Omit the return type only when the operation is genuinely void (a command with no meaningful return).

  **Example (pass):**
  ```
  + cancelOrder(reason: String): void
  ```

## DO NOT

- Write an operation as plain prose without a typed signature.

  **Example (fail):**
  ```
  + calculates the shipping cost     ? prose, not a signature
  ```

- Add an operation that does not trace to any domain model responsibility verb phrase.

  **Example (fail):**
  ```
  domain model — (no mention of "archiving")

  Domain-model block:
  + archiveRecord(id: RecordId): void   ? invented, no domain model source
  ```

- Leave parameters or return types untyped when the domain makes the type obvious.

  **Example (fail):**
  ```
  + calculateShippingCost(weight, destination)   ? missing types
  ```
