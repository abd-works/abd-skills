# Rule: Subtypes use English heading form with delta behavior only

**Scanner:** Manual review

Subtype concepts use `### SubtypeName *is a type of* BaseName` — no bold, no code notation. The subtype block carries only delta behavior. Passing means every specialization uses the English form and adds only what is new. Failing means code notation is used, base behavior is duplicated, or bold appears on the names.

## DO

- Use the English heading form (no bold).

  **Example (pass):** `### opposed check *is a type of* check`

- Include only delta behavior.

  **Example (pass):**
  ```
  ### international shipment *is a type of* shipment
  - collects *customs commodity codes* before gate release
  ```

## DO NOT

- Use code-style notation.

  **Example (fail):** `### InternationalShipment : Shipment`

- Use bold on the names.

  **Example (fail):** `### **opposed check** *is a type of* **check**`

- Duplicate base behaviors in the subtype block.

  **Example (fail):** Subtype block repeats "gates warehouse exit" — the base already owns it.

**Source:** Inherited from abd-domain-language.
