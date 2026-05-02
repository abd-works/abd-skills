# Rule: Concept block follows the required structure

**Scanner:** Manual review

Each `### Concept` block (and each subtype block) must follow the prescribed sequence: intent paragraph, `----` behaviors, `-----` collaborations, `#### Decisions made`, `#### Core terms`, `**Ref —**` entries. Passing means every concept follows this order with all required parts. Failing means a concept is missing a required part or has them in the wrong order.

## DO

- Write an intent paragraph immediately after the concept heading — what it is for, who it cooperates with, two to three sentences, no subheading.

  **Example (pass):**
  ```
  ### Shipment Lifecycle

  Coordinates whether a shipment is allowed to leave the warehouse and when
  it is considered delivered. Works with Payment Clearance to gate exit.
  ```

- Separate behaviors with `----`, collaborations with `-----` (one dash longer).

  **Example (pass):**
  ```
  ----
  gates warehouse exit until payment clearance is on record
  -----
  depends on Payment Clearance for the all-clear to ship
  ```

- Include a `#### Decisions made` section with bullet points listing the judgment calls behind the concept.

  **Example (pass):**
  ```
  #### Decisions made
  - Shipment Lifecycle owns the exit gate, not Payment Clearance — payment is a prerequisite, not an orchestrator.
  - Customer sign-off vs carrier scan disagreement is an open question for the domain expert.
  ```

- End every concept with `#### Core terms` (bullet list) and at least one `**Ref —**` entry.

  **Example (pass):** `#### Core terms` with bullets, then `**Ref — Gate before ship**` with Source/Locator/Extract fields.

## DO NOT

- Omit the intent paragraph and jump straight to behaviors.

  **Example (fail):** Concept heading followed immediately by `----` with no prose paragraph.

- Use the same separator length for both behaviors and collaborations.

  **Example (fail):** Both behaviors and collaborations separated by `----` — collaborations must use `-----`.

- Skip the `#### Decisions made` section on a concept.

  **Example (fail):** A concept with intent, behaviors, and collaborations but no decisions — the modeling choices are hidden.

- Skip the `**Ref —**` entries on a concept.

  **Example (fail):** A concept with intent, behaviors, and collaborations but no `**Ref —**` entry — uncited concept.

- Use `Shape hint:` or `Tension:` labels instead of `#### Decisions made`.

  **Example (fail):** `Shape hint: orchestration object` or `Tension: customer vs carrier` — these are replaced by Decisions made.

**Source:** Engagement convention (domain-sketch skill).
