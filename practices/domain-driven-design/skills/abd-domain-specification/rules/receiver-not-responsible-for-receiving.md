# Rule: A class is not responsible for being acted upon

**Scanner:** Manual review

The receiver of an action does not need an operation to receive it. Only the class that performs the action owns the operation. If a typed operation describes something happening *to* a class, find the acting class and place the operation there instead.

## DO

- Place the operation on the class that performs the action.

  **Example (pass):** A character makes a resistance check against a power effect. `OngoingEffects` owns `+ resist(effect: PowerEffect, check: Check): void`. `PowerEffect` owns `+ resistanceTrait: Trait` (declaring how it is resisted) — not a `resist` operation.

  **Example (pass):** A condition is applied to a character. `ImposedConditions` owns `+ applyCondition(source: ConditionSource, condition: Condition): void`. `Character` does not own `+ receiveCondition(...)`.

## DO NOT

- Give a class an operation that amounts to "be resisted," "be applied to," or "receive X."

  **Example (fail):**
  ```
  PowerEffect
  + resist(check: Check): void   ? the effect does not resist itself; the character makes the check
  ```

  **Example (fail):**
  ```
  Character
  + receiveCondition(condition: Condition): void   ? Character does not receive; ImposedConditions applies
  ```

  **Example (fail):**
  ```
  Condition
  + imposeOn(character: Character): void   ? Condition doesn't impose itself; PowerEffect does through ImposedConditions
  ```

## Clarification

A class *may* have a property that describes what is used to act upon it. This is not the same as an operation to be acted upon.

  **Example (pass):**
  ```
  PowerEffect
  + resistanceTrait: Trait   ? declares which trait a character uses to resist; the effect is not doing the resisting
  ```

**Source:** Engagement convention (domain-specification skill). Adapted from abd-domain-model/rules/receiver-not-responsible-for-receiving.md.
