# Rule: Text-orbits test for every Key Abstraction

Every Key Abstraction must pass the text-orbits test: the source speaks about it as a named unit with its own slice of vocabulary and its own sentences. If removing the candidate and folding its terms into another abstraction would not lose meaning the source actually carries, the candidate should be absorbed — not promoted to its own heading. Passing means every abstraction stands on its own vocabulary cluster. Failing means an abstraction exists that could be folded into another without losing source-carried meaning.

## DO

- Confirm each abstraction has vocabulary the source treats as belonging to that unit and not to another.

  **Example (pass):** Wire Transfer has `per-transaction cap`, `daily cap`, `beneficiary-jurisdiction cap` — terms the source discusses in sentences about Wire Transfer specifically, not about Funds Transfer generically.

- Fold weak candidates (rules, properties, or clusters that hang off another unit) into the parent abstraction and record the fold in `Tension:` if uncertain.

  **Example (pass):** "Reconciliation Deadline" is not its own Key Abstraction because the source only mentions it as a property of Funds Transfer — absorbed into that abstraction's Core terms.

## DON'T

- Promote a property, rule, or configuration value to its own Key Abstraction when the source treats it as vocabulary hanging off another unit.

  **Example (fail):** `### Key Abstraction: Per-Transaction Cap` — the source only discusses this as a rule belonging to Wire Transfer; it has no independent sentences or vocabulary cluster.

- Invent an abstraction the source does not orbit — one with no dedicated sentences, no repeated noun phrase, only a mention in passing.

  **Example (fail):** `### Key Abstraction: Compliance` — the source uses the word once in a sentence about Wire Transfer caps; it has no independent vocabulary cluster.
