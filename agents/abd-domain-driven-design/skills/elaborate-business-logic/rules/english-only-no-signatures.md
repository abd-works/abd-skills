---
---

# Rule: English only — no method signatures

All lifecycle and invariant content must be written in plain English prose. No method signatures, typed parameters, return types, or code-level notation may appear. Passing means every line reads as natural language. Failing means design-level notation has leaked into the business-logic elaboration.

## DO

- Describe transitions and constraints in natural English.

  **Example (pass):** "A character transitions from active to staggered when damage equals or exceeds the staggered threshold."

- Use domain vocabulary without formalising it into code.

  **Example (pass):** "Damage condition must equal the highest single penalty applied, not the sum."

## DO NOT

- Include method signatures with typed parameters.

  **Example (fail):** `applyDamage(amount: int, type: DamageType): void`

- Use return-type annotations or generic type syntax.

  **Example (fail):** `getCondition(): Condition<Staggered>`

- Use code-style boolean expressions instead of English.

  **Example (fail):** `damage >= threshold && !isImmune` instead of "damage equals or exceeds the threshold and the character is not immune."
