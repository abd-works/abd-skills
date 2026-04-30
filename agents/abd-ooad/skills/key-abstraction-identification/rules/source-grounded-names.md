# Rule: Source-grounded names for Key Abstractions

Every Key Abstraction name must be the noun phrase the source itself uses for the unit — not an invented generalization, compound glue word, or source-structure label. Passing means names come directly from the source vocabulary. Failing means names are invented, compound, or structural.

## DO

- Use the noun phrase the source repeats when discussing this unit, capitalized once: `Funds Transfer`, `Settlement Window`, `Loyalty Point`.

  **Example (pass):** The source says "A funds transfer moves…" repeatedly — name it `Funds Transfer`.

- When the source uses multiple phrases for the same unit, pick one and absorb the others into Core terms.

  **Example (pass):** Source uses "wire transfer" and "outbound wire" — name is `Wire Transfer`; "outbound wire" goes into Core terms.

- Keep names short and singular where possible.

  **Example (pass):** `Settlement Window` not `Settlement Windows and Their Reconciliation Mechanics`.

## DON'T

- Invent generalizing names the source never uses.

  **Example (fail):** `### Key Abstraction: Financial Instrument` — the source never says "financial instrument"; it says "funds transfer" and "wire transfer".

- Use compound glue names that merge two units or name a module inside an abstraction.

  **Example (fail):** `### Key Abstraction: Funds Transfer and Settlement` or `### Key Abstraction: Core Payment Mechanisms`.

- Use source-structure labels as names.

  **Example (fail):** `### Key Abstraction: Section 3.2` or `### Key Abstraction: Ch. 1 subsection 4`.

- Name after a quality or adjective rather than the thing itself.

  **Example (fail):** `### Key Abstraction: Compliance` when the source actually orbits `Wire Transfer Caps`.
