# Strategy: Spike / Proof of Concept

**When to use:** Answer one technical or design question before committing to a full plan. Learning goal is explicit; production quality optional.

**Typical scope:** 1–3 narrow stories; throwaway code allowed.

**Related:** `new-thin-slice.md` (when spike succeeds and you proceed to full delivery).

---

## System of work

| Stage | Scope | Skills (ordered) |
| --- | --- | --- |
| Discovery | all | abd-story-mapping (minimal — frame the experiment) |
| Exploration | story | abd-story-acceptance-criteria (minimal — learning-goal AC only) |
| Engineering | story | abd-story-acceptance-test (minimal), abd-clean-code (spike quality acceptable) |

**Minimal stages.** No specification. No architecture skills. Learning is the output, not production code.

---

## Scatter rules

| Transition | Rule |
| --- | --- |
| Discovery (all) → Exploration (story) | Frame the question in discovery; scatter into 1-3 story tickets for the experiment. |

---

## JIT policy

- All experiment stories enter backlog immediately (tiny scope)
- No further decomposition

---

## Checkpoint policy

| Level | When |
| --- | --- |
| Per stage | After discovery (confirm the question is clear before code) |
| Per story | After engineering (review learning, not code quality) |

---

## Key constraints

- Learning goal before code.
- Spike code is throwaway unless explicitly promoted through a full strategy later.
- Written conclusion required: what was learned, what it unlocks, which strategy fits next.
- Output is a **decision**, not a product.
