# Strategy: New Thin Slice

**When to use:** Medium-to-large change on an existing solution: new stories, maybe a new sub-epic; cuts across features or layers (e.g. new payment method, new role, new integration).

**Typical scope:** ~5–15 stories forming one vertical slice.

**Related:** `new-user-story.md` (1–3 stories). `brownfield-current-state.md` (mapping existing before adding). `new-initiative-`* strategies for greenfield.

---

## System of work


| Stage | Scope | Skills (ordered) |
| --- | --- | --- |
| Shaping | all | abd-story-mapping (extend existing), abd-thin-slicing |
| Discovery | increment | abd-information-architecture |
| Exploration | increment | abd-domain-language, abd-story-acceptance-criteria, abd-ux-mockup |
| Specification | sprint | abd-domain-model, abd-story-specification, abd-ux-specification |
| Engineering | sprint | abd-domain-code (BE), abd-story-acceptance-test (PO), abd-clean-code (EN), abd-architecture-code (conditional) |


---

## Scatter rules


| Transition                                       | Rule                                                                                                                                           |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Shaping (all) → Discovery (increment)            | Thin-slicing produces increments. Single vertical slice = single increment typically. For larger slices, multiple increments by epic boundary. |
| Exploration (increment) → Specification (sprint) | First epic becomes first sprint (prove the pipeline). Remaining stories grouped by epic                                                        |


### Sprint grouping heuristic

- **First sprint = first story only** (prove pipeline end-to-end)
- **Second sprint = remaining stories in first epic** (drain the epic with stable pattern)
- **Subsequent sprints = per-epic chunks** for remaining epics in the slice
- Default 3-4 stories per sprint

---

## JIT policy

- Scatter all increments after shaping (small total scope for thin slices)
- Scatter sprints for current increment only
- After first increment completes spec, scatter next increment's sprints

---

## Checkpoint policy


| Level      | When                                                                    |
| ---------- | ----------------------------------------------------------------------- |
| Per stage  | After discovery completes (single pass — do not split map from slicing) |
| Per skill  | First story through spec + engineering (prove pipeline)                 |
| Per sprint | Remaining stories                                                       |


---

## Key constraints

- The thin slice stays **end-to-end** (UI, API, logic, persistence) — not a horizontal-only increment.
- Do **not** checkpoint between full map and thin-slicing within discovery unless user explicitly wants a mid-pass stop.
- If extending existing stories or AC, do it openly — no silent forks.
- First story proves the pipeline before batching the rest.

---

## AI error rate adjustment

- First story at per-skill checkpoints regardless of confidence
- If output is clean after first story: expand to per-sprint for remaining
- If errors > 10%: stay at per-story through the increment

