---
scanner: cd3-ranking-by-highest-first
---
# Rule: CD3 ranking by highest first

When multiple items have been scored, the ranking orders them by highest CD3 first — this is the scheduling decision that minimises total delay cost across the set. A ranking passes when items are ordered by CD3 descending, arithmetic is correct (CoD / Duration = CD3), and any deviation from pure CD3 order has explicit stated rationale. It fails when items are ordered by CoD alone (ignoring duration), by arrival order, or by unstated preference with no economic justification.

## DO

- Order items by **highest CD3 first** (descending).

  **Example (pass):**
  ```
  | Rank | Item | CoD ($/month) | Duration (months) | CD3 |
  | 1 | Feature B | $4,000 | 1 | 4,000 |
  | 2 | Feature C | $5,000 | 2 | 2,500 |
  | 3 | Feature A | $1,000 | 5 | 200 |
  ```

- Verify arithmetic: CD3 = CoD / Duration for every row.

  **Example (pass):** Feature C: $5,000 / 2 = 2,500. Checks out.

- When deviating from pure CD3 order (e.g. for dependencies, fixed dates, or expedite items), state the rationale explicitly.

  **Example (pass):**
  ```
  | Rank | Item | CD3 | Override rationale |
  | 1 | Compliance fix | 800 | Expedite: regulatory deadline Nov 1 — must go first regardless of CD3 |
  | 2 | Feature B | 4,000 | — |
  ```

## DO NOT

- Order by Cost of Delay alone without dividing by duration.

  **Example (fail):** Feature C ($5,000 CoD) ranked above Feature B ($4,000 CoD) even though B has CD3 of 4,000 vs C's 2,500 — duration was ignored.

- Use arrival order (FIFO) or stakeholder preference as the default without stating why CD3 was overridden.

  **Example (fail):** "Feature A first because the VP asked for it" with no CD3 comparison or economic justification.

- Present CD3 scores with incorrect arithmetic.

  **Example (fail):** CoD = $5,000, Duration = 2, CD3 shown as 5,000 — division was not performed.

**Source:** Kept chunks #7, #8, #12 in `inputs/abd-answers-retrieval.md` — FIFO ($69 delay cost) vs CD3 ordering ($27 delay cost), 61% reduction.
