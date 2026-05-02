# Rule: No hidden concepts in behavior bullets

**Scanner:** AI review

Every behavior bullet must pass the **active-verb test**: the hidden subject ("a *Concept*") naturally starts the sentence with an active verb — "is made using", "produces", "has", "applies". If the bullet describes something with its own distinct structure, its own DC or threshold, its own roles, or its own result-flow, it is hiding a concept that must be extracted. Passing means every bullet describes behavior that belongs to its parent concept. Failing means a bullet smuggles in a separate concept with distinct identity, state, or interactions.

## DO

- Apply the active-verb test to every behavior bullet: "a *[parent concept]* [verb]…" — does this read naturally?

  **Example (pass):** "is made using the *trait* of a *character*" — a *Check* is made using the trait. Natural.

- Extract hidden concepts when the test fails or the bullet describes distinct structure.

  **Example (pass):** "team helpers each roll the same trait versus difficulty class 10; each helper success grants the leader +2" — this has its own roles (leader, helper), its own DC (always 10), and its own result-flow (modifier on another check). Extracted as `### Team Check *is a type of* Check`.

## DO NOT

- Leave complex multi-actor behavior as a single bullet on a parent concept.

  **Example (fail):** Team check mechanics crammed into one bullet on Check — hides a subtype with distinct behavior.

- Accept vague statements that hide modeling decisions.

  **Example (fail):** "the system handles condition enforcement" — which system? What module? What mechanism?

**Source:** Corrections 22, 25 (mm3e-online-holistic engagement).
