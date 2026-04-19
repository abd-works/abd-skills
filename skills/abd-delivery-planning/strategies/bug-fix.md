# Strategy: Bug Fix

**When to use:** A defect or regression — something that used to pass or should pass and does not. Often **test- and code-led**. Scope stays small until you widen it deliberately.

**Typical scope:** One story or a handful of AC after scope is cut to the **smallest honest repro scope** (often one failing test, one scenario, or one AC).


| Step | Stage                           | Intent                                                                                                                                                                                            | Scope                                                  | Checkpoint policy               | Rationale                                                                                       |
| ---- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------- | ----------------------------------------------------------------------------------------------- |
| 1    | Exploration                    | **Isolate:** find the regression surface (failing or missing test, expected vs actual), and **cut scope** to the smallest **reproducible** surface — not a product “slice,” a **bounded defect**. | Defect surface only                                    | User confirms scope before code | You cannot fix what you have not bounded.                                                       |
| 2    | Acceptance Tests → Engineering | **Prove the fix:** change code so the right tests pass; RED → GREEN when a test exists; add a test when none exists.                                                                              | **Single test method** (or smallest repro you can run) | After tests pass                | Behavior is anchored in executable checks.                                                      |
| 3    | Exploration → Story Definition | **Reverse-engineer specification:** write or update AC and scenarios **from** the corrected behavior — document what is true after the fix, not invent intent in a vacuum.                        | Single story scenario; single story AC                 | User reviews captured intent    | Spec trails truth; formats match your pipeline without pretending this is greenfield discovery. |


**Key constraints:**

- Touch the existing story graph; add/update the defect story; avoid map-wide refactors in the same plan.
- Forward order (full AC before code) is optional when reverse engineering after the fix is faster and more honest.
- If the bug exposed missing written intent, capture it after the fix so the gap does not repeat.
