# Rule: Increments of Value names a minimum valuable increment

**Scanner:** Manual review

The **Increments of Value** section passes when it identifies a first increment that is smaller than the full solution — something the team could ship and learn from — and states which customer segment receives that value first. Failing means the section treats the full feature set as a single delivery event, uses vague language with no specificity about what ships first, or lists features rather than increments.

## DO

- Name the minimum valuable increment explicitly and state who it reaches first.

  **Example (pass):** `INCREMENTS_OF_VALUE: (1) Live bay calendar for dealer coordinators — minimum increment, validates core scheduling visibility; (2) Push notification on booking change for fleet managers; (3) Dealer-facing reschedule self-service flow.`

## DO NOT

- Describe all features as one delivery without naming a minimum or an ordering.

  **Example (fail):** `INCREMENTS_OF_VALUE: Full scheduling platform with calendar, notifications, and self-service reschedule` — this is a scope description, not a sequenced increment plan.

- Use a vague phrase that does not commit to a slice.

  **Example (fail):** `INCREMENTS_OF_VALUE: Digital solution for dealers` — no minimum, no segment, no ordering.

**Source:** Agile by Design Opportunity Canvas — Increments of Value section.
