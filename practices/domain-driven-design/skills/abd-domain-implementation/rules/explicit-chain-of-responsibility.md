# Rule: Explicit chain of responsibility — no nebulous operations

**Scanner:** Manual review

When a typed operation implies a chain of actors or steps, every actor in that chain must be traceable to a typed property or operation with explicit parameters in the Class Model. Nothing may be left implied or nebulous. "May" and "requires" language in a behavior must be fully modeled as typed members.

## DO

- Trace each step in the implied chain to a named typed operation or property.

  **Example (pass):** Behavior: "may be ongoing for a target character: requires a resistance check at the end of each of the target's turns until ended."

  This implies: someone tracks which characters are ongoing targets, and someone triggers end-of-turn resistance checks. The Class Model must reflect both:
  ```
  PowerEffect : Trait
  + << aggregation >> ongoingTargets: List<Character>
  + resist(effect: PowerEffect, check: Check): void    ? on OngoingEffects, not PowerEffect
      Invariant: resistance check made at end of each of the character's turns while effect is active
  ```

  **Example (pass):** Behavior: "supersedes a less severe condition from the same source — removing the lesser."

  This implies: someone knows the supersession hierarchy, and someone performs the removal. Both must appear — `+ supersedes: Condition` on `Condition` and `+ applyCondition(...)` with the supersession invariant on `ImposedConditions`.

## DO NOT

- Write a property and leave the downstream action it implies without an owning operation.

  **Example (fail):**
  ```
  PowerEffect
  + ongoingTargets: List<Character>   ? who triggers the end-of-turn resistance check? No operation owns it.
  ```

- Leave "may" or "requires" language from a behavior with an incomplete typed chain.

  **Example (fail):** Behavior says "requires a resistance check at end of each turn" but no operation for triggering that check appears anywhere in the model.

- Leave an implied collaborator out of the operation signature.

  **Example (fail):**
  ```
  + resist(check: Check): void   ? missing the PowerEffect parameter; which effect is being resisted?
  ```

**Source:** Engagement convention (class-model skill). Adapted from class-responsibility-collaborator/rules/explicit-chain-of-responsibility.md.
