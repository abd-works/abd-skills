# Pipeline invariants

This skill **optimizes** for object-oriented discipline, provenance, and explicit promotion. The following **invariants** guide automation and prompts. Background detail: [`../plan/pipeline-deep-dive.md`](../plan/pipeline-deep-dive.md).

## Four layers before most rows become `concepts[]`

| Layer | Question | Stored as |
|-------|----------|-----------|
| **1** Mention / term | What nouns appear? | Glossary / term index |
| **2** Mechanism | What named processes (workflows, lifecycles)? | Mechanism nodes — candidates before classes |
| **3** Domain type | What stateful things have distinct lifecycles? | `concepts[]` — **sparingly** |
| **4** Subtype / enum | Per family: enum vs `extends`? | Decision log **before** bulk properties |

## Gates (priority)

1. **Inheritance from promotion** — `inherits` / `extends` enter the model through **explicit** promotion with evidence, not from regex on raw chunk text alone.
2. **Candidate queue** — Classification proposes **candidates**; merge into `concepts[]` in **Integrate** (Phase 7) after variant rules.
3. **`classify-variants-before-modeling`** — Per mechanism/module, variant decision is **written** before breadth classification fills subtypes.
4. **Foundational spine** — Prefer a **small** spine of cores + mechanisms + citations over deep `extends` trees grown from headings alone.
5. **K-read stratification** — Breadth sampling uses **`modeling_priority`** and **`evidence_type`**, including stratified chunk coverage.
6. **Deepen** — Harvest maps **terms → mechanisms → types** for approved scope.
7. **Stories** — Confirming stories are **behavioral** (actor + operation + outcome on domain concepts); story text may reference **terms** while **Concept** rows follow promotion rules.

## Design goals

- **`extends`** edges carry **substitutability** evidence, not just name co-occurrence.
- **Aliases** and **term references** resolve naming alignment before minting new **Concept** rows.

See **`pipeline-deep-dive`** §11 for automation and prompt alignment with these gates.

---

## Phases 4–8 — artifact summary

| Phase                   | Primary artifacts                                       | Implementation levers                                                                                                 |
| ----------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **4** Domain types      | `map-model-spec` concepts, sparse `concepts[]`          | JSON schema + promotion log; each concept row carries `evidence_chunk_ids[]` or explicit promotion record             |
| **5** Variants          | `variant_decisions` (markdown table or JSON per family) | Human-authored or LLM-assisted **decision doc** checked in; scanners enforce enum vs `extends` before bulk properties |
| **6** Deepen            | responsibilities, `depends_on`, evidence                | Optional LLM-assisted deepen (prompts under `docs/prompts/`); outputs cite `chunk_id`s                                |
| **7** Integrate         | merged map-model-spec, queue drained                    | Code merge scripts + manual review gates                                                                              |
| **8** Validate & render | scanner outputs, reports                                | `skill-config.json` scanner list; deterministic scanners in `scripts/scanners/`                                       |

Per-phase steps live in [`content/parts/process.md`](../content/parts/process.md) and [`content/parts/phases/`](../content/parts/phases/).
