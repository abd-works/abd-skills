# Rule: A concept is not responsible for being acted upon

**Scanner:** Manual review

The receiver of an action does not need a responsibility to receive it. Only the actor that performs the action owns the responsibility. If a behavior describes something happening *to* a concept, identify the acting concept and place the responsibility there.

## DO

- Place the responsibility on the concept that performs the action.

  **Example (pass):** A character makes a resistance check against a power effect. `Ongoing Effects` (on `Character`) owns `make resistance check for ongoing targets`. `Power Effect` owns `resistance trait` (declaring how it is resisted) — not a `resist` operation.

  **Example (pass):** A condition is applied to a character. `Imposed Conditions` owns `apply new condition`. `Character` does not own `receive condition`.

## DO NOT

- Give a concept a responsibility that amounts to "be resisted," "be applied to," or "receive X."

  **Example (fail):** `Power Effect` has `resist | Resistance Check` — the effect does not resist itself; the character makes the check.

  **Example (fail):** `Character` has `receive condition | Condition` — the character does not receive; the `Imposed Conditions` collection applies it.

  **Example (fail):** `Condition` has `be imposed | Character` — the condition doesn't impose itself; it is imposed by a `Power Effect` through `Imposed Conditions`.

## Clarification

A concept *may* have a property that describes what is used to act upon it. This is not the same as a responsibility to be acted upon.

  **Example (pass):** `Power Effect` has `resistance trait | Trait` — this declares which trait a character uses to resist the effect. The effect is not doing the resisting; it is providing the information needed for the character to resist.

**Source:** Engagement convention (class-responsibility-collaborator skill).
