---
scanner: ~
---
# Rule: Assumptions explicit with confidence

Every Cost of Delay estimate must trace to a set of named assumptions — each with a factor, unit, and confidence level — so the team can see what drives the number and where uncertainty lives. A canvas passes when a reviewer can reconstruct the CoD calculation from the assumptions table without needing to ask "where did that number come from?" It fails when a CoD figure appears with no supporting model, or when assumptions are listed without confidence ratings that would let a team know what to validate.

## DO

- List every assumption that feeds the CoD formula as a row with **factor** (what you are estimating), **unit** (people/month, $/hour, %, events/month), and **confidence** (Strong / Reasonable / Uncertain).

  **Example (pass):**
  ```
  | Assumption | Factor | Unit | Confidence |
  | Customers travelling abroad/month | 500,000 | people/month | Strong |
  | Likelihood card is flagged | 30% | — | Strong |
  | Avg call duration | 0.25 | hours | Reasonable |
  | Hourly call center rate | $50 | $/hour | Strong |
  | % who would use self-service | 40% | — | Uncertain |
  ```

- Show the CoD formula as a product of the factors so arithmetic is transparent.

  **Example (pass):** `CoD = 500,000 × 0.30 × 0.25 × $50 × 0.40 = $750,000/month`

- Flag **Uncertain** assumptions as candidates for validated learning before committing to build.

  **Example (pass):** "% adoption (40%) is Uncertain — recommend quick survey or A/B before locking scope."

## DO NOT

- Present a CoD number with no underlying factors or formula.

  **Example (fail):** "Cost of Delay: $750,000/month" with no assumptions table and no formula — the reviewer cannot verify or challenge the estimate.

- List assumptions without confidence levels, treating all factors as equally certain.

  **Example (fail):** Five assumption rows, all blank in the Confidence column — hides which parts of the estimate are guesses.

- Use false precision (e.g. $748,213.47/month) when inputs are uncertain — round to appropriate significant figures.

  **Example (fail):** "CoD = $748,213.47/month" when the adoption rate is a SWAG at 40% — implies precision the model does not support.

**Source:** Kept chunks #6, #8, #11 in `inputs/abd-answers-retrieval.md` — "The process of surfacing our assumptions about value are more useful than the numbers we come up with!"
