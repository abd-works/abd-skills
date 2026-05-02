---
scanner: no-jargon-added
---

# Rule: No identification-model jargon or labeled definition sections

The key-abstractions step must not introduce fields from the old identification model (`Intent:`, `Shape hint:`, `Tension:`, `Core terms (absorbed`) and must not use labeled sections to define a KA (`Role:`, `Boundary:`, `Responsibilities:`, `Invariants:`). KA definitions are flowing prose paragraphs. Passing means none of these appear. Failing means any of them are present.

## DO

- Write KA definitions as 1–2 paragraphs of flowing prose covering role, boundary, responsibilities, and rules/invariants naturally.

  **Example (pass):** A paragraph that says "A check is the core resolution mechanic — it interacts with Trait and DC, owns the roll-versus-DC formula, and must always produce a binary result."

## DO NOT

- Add `Intent:` lines to any term or KA.

  **Example (fail):** `Intent: The atomic resolution mechanic that determines success or failure.`

- Add `Shape hint:` lines.

  **Example (fail):** `Shape hint: Procedure-like — verb-shaped with trigger and outcome.`

- Add `Tension:` lines.

  **Example (fail):** `Tension: May merge with opposed check in later modeling.`

- Add `Core terms (absorbed` lists that group terms under another term.

  **Example (fail):**
  ```
  Core terms (absorbed from this module's Core terms list):
  - d20
  - modifier
  ```

- Use labeled sections to structure the KA definition.

  **Example (fail):**
  ```
  Role: Determines success or failure of uncertain actions.
  Boundary: Owns the roll+modifier vs DC formula.
  Responsibilities: Resolves checks, produces degrees.
  Invariants: Must always yield binary success/failure.
  ```
  (These must be woven into prose, not listed as fields.)
