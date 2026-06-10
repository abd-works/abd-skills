# Cost of Delay — Examples

## Why CD3 beats FIFO

Three features with different Cost of Delay and Duration:

| Feature | CoD ($/week) | Duration (weeks) | CD3 |
| --- | --- | --- | --- |
| A | $1 | 5 | 0.2 |
| B | $4 | 1 | 4.0 |
| C | $5 | 2 | 2.5 |

**FIFO order (A → B → C):**

| Week | Working on | A earning | B earning | C earning | Revenue gained | Opportunity cost |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | A | $0 | $0 | $0 | $0 | $10 |
| 2 | A | $0 | $0 | $0 | $0 | $10 |
| 3 | A | $0 | $0 | $0 | $0 | $10 |
| 4 | A | $0 | $0 | $0 | $0 | $10 |
| 5 | A | $0 | $0 | $0 | $0 | $10 |
| 6 | B | $1 | $0 | $0 | $1 | $9 |
| 7 | C | $1 | $4 | $0 | $5 | $5 |
| 8 | C | $1 | $4 | $0 | $5 | $5 |
| **Total** | | | | | **$11** | **$69** |

**CD3 order (B → C → A):**

| Week | Working on | A earning | B earning | C earning | Revenue gained | Opportunity cost |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | B | $0 | $0 | $0 | $0 | $10 |
| 2 | C | $0 | $4 | $0 | $4 | $6 |
| 3 | C | $0 | $4 | $0 | $4 | $6 |
| 4 | A | $0 | $4 | $5 | $9 | $1 |
| 5 | A | $0 | $4 | $5 | $9 | $1 |
| 6 | A | $0 | $4 | $5 | $9 | $1 |
| 7 | A | $0 | $4 | $5 | $9 | $1 |
| 8 | A | $0 | $4 | $5 | $9 | $1 |
| **Total** | | | | | **$53** | **$27** |

**Result:** Same 8 weeks, same three features. CD3 ordering delivers **$53 revenue** vs FIFO's **$11** (nearly 5× more), and incurs only **$27 opportunity cost** vs **$69** — a **61% reduction** in total delay cost.
