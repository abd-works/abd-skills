# Rule: Explicit chain of responsibility — no nebulous behaviors

**Scanner:** Manual review

When a behavior implies a chain of actors or steps, every actor in that chain must be traceable to a property or operation with explicit collaborators in the CRC. Nothing may be left implied or nebulous. "May" and "requires" language in a behavior must be fully modeled.

## DO

- Trace each step in the implied chain to a named responsibility with collaborators.

  **Example (pass):** Ubiquitous Language behavior: "may be ongoing for a target character: requires a resistance check at the end of each of the target's turns until ended."

  This implies: someone tracks which characters are ongoing targets, and someone triggers end-of-turn resistance checks. The CRC must reflect both:
  ```
  ongoing targets             | Character
  make resistance check       | Character, Check
                              |   invariant: check made at end of each ongoing target's turn
  ```

  **Example (pass):** Ubiquitous Language behavior: "supersedes a less severe condition from the same source — removing the lesser."

  This implies: someone knows the supersession hierarchy, and someone performs the removal. The CRC must reflect both — `supersedes | Condition` on `Condition` and `apply new condition` with the supersession invariant on `Imposed Conditions`.

## DO NOT

- Write a property and leave the downstream action it implies without an owner.

  **Example (fail):** CRC has `is ongoing | (active or ended)` with no corresponding operation for who tracks ongoing targets or who triggers the end-of-turn check.

- Leave "may" or "requires" language in a behavior with an incomplete CRC chain.

  **Example (fail):** Behavior says "requires a resistance check at end of each turn" but no operation for making that check appears anywhere in the CRC.

- Leave an implied actor out of the collaborator column.

  **Example (fail):** Operation `make resistance check | Check` with no `Character` collaborator — the character is the one making the check.

**Source:** Engagement convention (class-responsibility-collaborator skill).
