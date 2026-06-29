# Rule: All domain model collaborators are accounted for in the typed member

**Scanner:** Manual review

Every collaborator listed for a domain model responsibility must appear somewhere in the corresponding typed property or operation. A collaborator may be accounted for as:

1. A **parameter** to the operation
2. The **return type** of the operation
3. A **type** on the property
4. A step in the **`Interaction:`** block

If a collaborator appears nowhere in 1–4, it has been silently dropped. That is a modeling gap — either the collaborator belongs in the signature, the property type, or the interaction, or a deliberate decision to exclude it must be recorded.

## DO

- Account for every collaborator in the parameter list, return type, or interaction.

  **Example (pass):** domain model responsibility: `resolve | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result`

  None of these are parameters on `+ resolve(): CheckResult`. They are all internal. Every one must appear in the `Interaction:` block:
  ```
  + resolve(): CheckResult
      Invariant: shape is always rollTotal vs dc.value
      Interaction:
          roll: Integer = d20.roll()                              ? D20 accounted for
          total: Integer = trait.rank + roll + circumstanceModifier.value   ? Trait, CircumstanceModifier
          success: Boolean = total >= dc.value                   ? DifficultyClass (dc)
          margin: Integer = total - dc.value
          result: CheckResult = new CheckResult(...)             ? CheckResult
          return result
  ```

- Account for a collaborator as a property type when the responsibility becomes a property.

  **Example (pass):** domain model responsibility: `difficulty ladder | Difficulty Ladder` becomes `+ difficultyLadder: DifficultyLadder` — collaborator is the property type.

## DO NOT

- Drop a collaborator silently.

  **Example (fail):** domain model responsibility `resolve | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result` becomes:
  ```
  + resolve(): CheckResult
  ```
  with no `Interaction:` block — D20, Trait, CircumstanceModifier, and DifficultyClass are all unaccounted for.

- Assume a collaborator is "obvious" and omit it from the model.

  **Example (fail):** Interaction traces `d20.roll()` but never references `trait.rank` or `dc.value` — Trait and DifficultyClass are dropped.

## When a collaborator is intentionally excluded

Record it as a decision: state which collaborator is excluded and why (e.g., "D20 is an internal implementation detail not exposed at this fidelity level"). Without an explicit decision, any missing collaborator is a gap.

**Source:** Engagement convention (domain-specification skill).
