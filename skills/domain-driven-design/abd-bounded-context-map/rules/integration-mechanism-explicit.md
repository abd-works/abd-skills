# Rule: Integration mechanism names a concrete approach

The integration mechanism on every dependency arc must name a concrete, implementable communication approach — not a vague category or a deferred placeholder. The mechanism constrains consistency, latency, coupling, and operational complexity; leaving it vague means the architecture is not actually decided. Failure is a dependency whose integration mechanism is missing, says only "TBD" without a follow-up action, or uses a label too broad to implement ("various", "as needed").

## DO

- Name a specific mechanism from the recognized catalogue: Events, Messaging, REST/API, Batch, Shared DB, File Transfer, or Shared Kernel codebase.

  **Example (pass):**

  ```
  - Integration mechanism: Messaging (message queue for inbound/outbound business messages)
  ```

- Add a brief qualifier when it clarifies the implementation (protocol, transport, frequency).

  **Example (pass):**

  ```
  - Integration mechanism: Batch (nightly extract from Trading into Invoice ledger)
  ```

- When the mechanism is genuinely undecided, state what is blocking the decision, who owns it, and when it will be resolved.

  **Example (pass):**

  ```
  - Integration mechanism: TBD — choosing between Events and REST/API pending latency requirements from Product. Owner: Tech Lead. Target: Sprint 14.
  ```

## DO NOT

- Leave the integration mechanism field blank or missing.

  **Example (fail):**

  ```
  ### Trading → Invoice
  - Direction: upstream/downstream
  - Domain mapping: deal identifiers and pricing terms
  - Team engagement model: Conformist — Service Provider
  ```

  Integration mechanism is absent — the arc does not say how the systems actually talk.

- Use a label that is too broad to implement without further decisions.

  **Example (fail):**

  ```
  - Integration mechanism: various
  ```

  "Various" is not a mechanism — it defers every question about consistency, latency, and coupling.

- Write "TBD" without a named owner and resolution target.

  **Example (fail):**

  ```
  - Integration mechanism: TBD
  ```

  No owner, no timeline — the placeholder will persist indefinitely.

**Source:** Kept chunk #7 in `inputs/abd-answers-retrieval.md` — ABD three-dimension dependency model lists Events, Batch, Messaging, REST/API as the integration mechanism catalogue.
