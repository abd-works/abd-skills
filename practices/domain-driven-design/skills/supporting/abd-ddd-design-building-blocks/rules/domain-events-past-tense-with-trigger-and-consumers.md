---
scanner:
---
# Rule: Domain Events named in past tense with trigger and consumers

Every Domain Event must be named as a **past-tense verb phrase** in domain language, state what triggered it, and name at least one consumer. Events represent something that **already happened** — they are facts, not commands. Passing means events read like history ("OrderConfirmed", "PatientAdmitted") and carry enough context to be actionable. Failing means events are named as commands, lack triggers, or have no stated consumers.

## DO

- Name every Domain Event in past tense using domain vocabulary.

  **Example (pass):** `PetSold`, `OrderConfirmed`, `AppointmentCancelled`, `PaymentReceived` — each reads as "this happened."

- State the trigger: what state change in which aggregate causes this event to fire.

  **Example (pass):** "**Trigger:** An Order transitions from Draft to Confirmed after payment validation succeeds."

- Name at least one consumer that reacts to the event — another aggregate, bounded context, or external system.

  **Example (pass):** "**Consumers:** Inventory (decrement available count), Notifications (send confirmation email)."

- Include a payload summary — the key data the event carries, enough for consumers to react without calling back.

  **Example (pass):** "**Payload:** order ID, customer ID, pet ID, confirmed timestamp, total amount."

## DO NOT

- Name events as commands or present-tense verbs.

  **Example (fail):** `ConfirmOrder`, `SellPet`, `ProcessPayment` — these are commands, not events; they say "do this" not "this happened."

- Declare a Domain Event with no consumer identified.

  **Example (fail):** "**Consumers:** None identified." — if nothing reacts to it, it is not yet a Domain Event worth modeling; it is just internal state change.

- Use technical or infrastructure names instead of domain language.

  **Example (fail):** `MessagePublished`, `QueueUpdated`, `RecordInserted` — these are infrastructure concerns, not domain events.

**Source:** Kept chunks #9, #12 in `inputs/abd-answers-retrieval.md`
