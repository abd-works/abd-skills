---
scanner: core-terms-disjoint
---

# Rule: Core terms disjoint within module

Within a single module (or the whole flat file), every Core-terms phrase must be attached to exactly one Key Abstraction. No phrase should appear under two different abstractions in the same scope. Passing means every bullet in every Core terms list is unique within its module. Failing means a phrase is duplicated across two or more Key Abstractions.

## DO

- Attach each Core-terms phrase to the single Key Abstraction whose extracts primarily speak about that concept.

  **Example (pass):** `reconciliation window` appears only under `Funds Transfer`, not also under `Wire Transfer`.

- When two abstractions share vocabulary, assign the phrase to the one with stronger source grounding and note the overlap in a `Tension:` line on the other.

  **Example (pass):** `Tension: "KYC tier" also appears in Funds Transfer context — assigned here because cap rules use it more directly.`

## DON'T

- List the same phrase under two Key Abstractions in the same module.

  **Example (fail):**
  ```
  ### Key Abstraction: Funds Transfer
  Core terms:
  - reconciliation window

  ### Key Abstraction: Settlement
  Core terms:
  - reconciliation window    ← duplicate
  ```

- Use slightly different wording of the same concept to bypass disjointness (e.g., "reconciliation window" vs "recon window" for the same thing).

  **Example (fail):** Two entries that are clearly the same phrase with cosmetic variation, placed under different abstractions.
