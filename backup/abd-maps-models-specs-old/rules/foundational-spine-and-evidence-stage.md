---
rule_id: foundational-spine-and-evidence-stage
phases: [step1]
order: 5
impact: HIGH
---

## Foundational spine and evidence-stage ladder

Before naming modules or epics, establish the **domain spine**: the minimal set of concepts and mechanisms without which the rest of the model cannot be read coherently. In [`parts/process.md`](../parts/process.md) this is the **Foundational mechanisms** row (Stage 2), separate from **Modules and Epics** (scaffold breadth).

**DO**

- Identify **foundational** concepts: core entities, invariants, and mechanisms that other concepts presuppose. Mark them in JSON with `module.foundational: true` on the module that primarily owns that spine (or split if the spine spans modules — then mark each contributing module).
- Assign every concept an **`evidence_stage`** aligned with [`parts/process.md`](../parts/process.md) / AGENTS. Start conservative; promote only when chunk evidence supports it.
- Cite chunks from the first substantive claim (`description_chunk`, `owns_chunk`, `chunk_ids` / `chunk_evidence`) — see `chunks-must-be-referenced.md`.

**Evidence-stage ladder (concept-level)**

Use these values on each `concept` (add `open_questions` when the schema or material is unclear):

| Stage | Meaning |
|--------|---------|
| `hypothesis` | **[Foundational mechanisms](../parts/process.md)** or early **[Modules and Epics](../parts/process.md)**: named from skim/structure; provisional citations; not yet substantiated by the **K** full-read pass |
| `scaffolded` | **[Modules and Epics](../parts/process.md)**: substantiated by the orientation / **K** chunk reads — chunk-anchored names and any `owns` / properties / operations you cite there |
| `deepened` | After **[Concept Classes and Stories](../parts/process.md)** (deepen): full properties/operations/invariants from pair chunks (optional until deepen runs) |

**Human gate**

- If a concept would be promoted to **`scaffolded`** or **`deepened`** but the source is ambiguous, **stop** and record under `open_questions` instead of inventing detail.

**DON'T**

- Collapse foundational spine and **Modules and Epics** into one pass: do not skip the explicit “what is foundational?” pass and jump straight to epic titles.
- Mark `module.foundational: true` for convenience modules (helpers, cross-cutting buckets) without a spine role.
