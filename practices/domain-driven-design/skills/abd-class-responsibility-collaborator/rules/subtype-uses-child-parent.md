# Rule: Subtypes use ConceptName : BaseConcept on the heading line

**Scanner:** Manual review

When a concept is a specialization of another, its CRC heading must use `#### **ConceptName : BaseConcept**` notation. The block states only delta responsibilities — what the subtype adds or overrides beyond the base. Passing means subtypes are correctly notated and carry only deltas. Failing means subtypes use the wrong format or duplicate base responsibilities.

## DO

- Use `#### **ConceptName : BaseConcept**` on the heading line for subtypes.

  **Example (pass):**
  ```
  #### **Opposed Check : Check**
  use opposing trait          | Trait
                              |   invariant: both sides resolve as standard Checks; higher result wins
  ```

- State only delta responsibilities that the subtype adds or overrides beyond the parent.

  **Example (pass):** Parent `Check` owns `resolve`; subtype `Opposed Check : Check` adds only `use opposing trait` and its invariants.

## DO NOT

- Use the Ubiquitous Language English heading form in CRC headings.

  **Example (fail):** `#### **Opposed Check** *(is a type of Check)*` — CRC uses `: BaseConcept` in the heading, not the sketch's English form.

- Use code-style inheritance syntax.

  **Example (fail):** `OpposedCheck extends Check`

- Duplicate base responsibilities in the subtype block.

  **Example (fail):** Subtype repeats `use trait`, `use difficulty class`, `apply circumstance` — those are identical to the parent `Check` and must not be restated.

**Source:** Engagement convention (class-responsibility-collaborator skill).
