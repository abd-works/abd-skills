# Strategy: Spike / Proof of Concept

**When to use:** Answer one technical or design question before committing to a full plan. Learning goal is explicit; production quality optional.

**Typical scope:** 1–3 narrow stories; throwaway code allowed.


| Step | Stage                     | Intent                                                                                                                            | Scope                                | Checkpoint policy                                    | Rationale                            |
| ---- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | ---------------------------------------------------- | ------------------------------------ |
| 1    | Discovery                 | **Frame the experiment:** what question must be answered; what outcome counts as success.                                         | Minimal stories to name the question | One checkpoint after framing                         | No code until the question is clear. |
| 2    | Exploration → Engineering | **Run the experiment:** **minimal** AC aimed at the learning goal, minimal scenarios, fast code — judge **learning**, not polish. | Spike stories                        | After implementation: review learning, not only code | Output is a decision, not a product. |


**Key constraints:**

- Learning goal before code.
- Spike code is throwaway unless explicitly promoted through a full strategy later.
- Written conclusion required: what was learned, what it unlocks, which strategy fits next.
