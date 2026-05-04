# Rule: Subtypes use ClassName : ParentClass on the heading line

**Scanner:** Manual review

When a class is a specialization of another, its object-model heading must use `#### **ClassName : ParentClass**` notation. The block states only delta members — typed properties, operations, and invariants that the subtype adds or overrides beyond the parent. Passing means subtypes are correctly notated and carry only deltas. Failing means subtypes use the wrong format or duplicate inherited members.

## DO

- Use `#### **ClassName : ParentClass**` on the heading line for subtypes.

  **Example (pass):**
  ```
  #### **OpposedCheck : Check**

  + resolve(opposing: Check): CheckResult
      Invariant: both sides resolve as standard Checks; higher result wins
  ```

- State only delta members — typed properties and operations the subtype adds or overrides beyond the parent.

  **Example (pass):** Parent `Check` owns `+ resolve(): CheckResult`; subtype `OpposedCheck : Check` overrides it with the opposing-check signature and adds its own invariants. No parent members are repeated.

## DO NOT

- Use the domain sketch English heading form in object-model headings.

  **Example (fail):** `#### **Opposed Check** *(is a type of Check)*` — use `: ParentClass` in the heading, not the sketch's English form.

- Use code-style syntax from the implementation language.

  **Example (fail):** `class OpposedCheck extends Check` or `OpposedCheck(Check)` — the domain model uses its own notation, not a language keyword.

- Repeat inherited members in the subtype block.

  **Example (fail):**
  ```
  #### **OpposedCheck : Check**

  + trait: Trait                      ← inherited from Check; do not repeat
  + dc: DifficultyClass               ← inherited from Check; do not repeat
  + resolve(opposing: Check): CheckResult
  ```

**Source:** Engagement convention (object-model skill). Adapted from class-responsibility-collaborator/rules/subtype-uses-child-parent.md.
