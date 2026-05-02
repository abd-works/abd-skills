---
scanner: ~
---
# Rule: Value type and urgency assigned

Every item scored in this skill must have exactly one value type and one urgency profile selected, with enough rationale that a reviewer can see why that classification was chosen. A canvas passes when value type picks the right formula pattern and urgency profile matches the decay shape. It fails when classifications are missing, when both are left as "Standard" by default without reasoning, or when the selected value type contradicts the formula used.

## DO

- Assign exactly **one** value type per item: Increase Revenue, Protect Revenue, Reduce Cost, or Avoid Cost.

  **Example (pass):**
  ```
  Value Type: Reduce Cost
  Rationale: Customers currently call in to reactivate blocked cards; this reduces call volume.
  ```

- Assign exactly **one** urgency profile per item: Expedite, Fixed Date, Standard, or Intangible.

  **Example (pass):**
  ```
  Urgency Profile: Standard
  Rationale: Shallow but immediate cost saving; value accrues incrementally from day one with no hard deadline.
  ```

- Use a formula pattern that matches the selected value type (see Core concepts table in SKILL.md).

  **Example (pass):** Value type is "Reduce Cost" → formula uses `cost reduction/event × events × likelihood`.

## DO NOT

- Leave value type or urgency profile blank or unselected on a scored item.

  **Example (fail):** Canvas has CoD = $200,000/month but the Value Type row says "TBD" — classification was skipped.

- Default both to "Standard / Standard" without stated reasoning.

  **Example (fail):** Three items all marked Standard/Standard with no rationale — suggests the team skipped the conversation.

- Select a value type that contradicts the formula used.

  **Example (fail):** Value Type says "Increase Revenue" but the formula calculates `cost avoidance/event × events` — mismatch between classification and model.

**Source:** Kept chunks #4, #9 in `inputs/abd-answers-retrieval.md` — value type / urgency profile matrix with four types and four profiles.
