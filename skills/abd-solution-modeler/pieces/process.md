# Process

Pipeline: Context → Model → Assess. `pipeline.py` orchestrates all phases.

- Code phases — run scripts directly (normalize, extract_concepts, extract_evidence, index)
- `generate <phase>` — prints built phase spec from `phases/built/` (phase instructions + baked-in rules)
- `scan <phase>` — runs programmatic scanners against generated output
- `validate <phase>` — prints rules for adversarial AI validation pass

**Workspace layout** (relative to `output_dir`):

- `context/` — context_chunks.json
- `concept_signals/` — term_candidates.json, definition_candidates.json, dependency_actions.json, cooccurrence_graph.json, table_vocabularies.json
- `evidence/` — terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json, evidence_index.json
- `generated/` — extraction_config.json, hypothesis.json, solution_model.json, assessment.json
- `generated/domain/` — legacy .md outputs, solution_model.drawio

**Match user phrase to phase Trigger** — each phase file has a `## Trigger` section; run that phase when the user says one of those phrases.

**Log corrections immediately** — when the user corrects any output, add an entry to `corrections.md` in the solution directory before continuing. Format: phase, what was wrong, what is correct.

---

## Stage 1: Context and Evidence (Phases 1–6)

| Phase | Actor            | Ref                                                                 | Outputs                                                                                                                       |
| ----- | ---------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 1     | Code             | [normalize.md](phases/built/normalize.md)                           | context_chunks.json                                                                                                            |
| 2     | AI               | [configure_extraction.md](phases/built/configure_extraction.md)       | extraction_config.json                                                                                                        |
| 3     | Code             | [extract_concepts.md](phases/built/extract_concepts.md)              | concept_signals/*.json (term_candidates, definition_candidates, dependency_actions, cooccurrence_graph, table_vocabularies)   |
| 4     | AI               | [concept_synthesis.md](phases/built/concept_synthesis.md)            | hypothesis.json, interaction tree skeleton (epics only)                                                                      |
| —     | **Checkpoint 1** | Verify concept framing and interaction skeleton                   | —                                                                                                                             |
| 5     | Code             | [extract_evidence.md](phases/built/extract_evidence.md)              | evidence/*.json (terms, actions, decisions, states, relationships, modifiers)                                                |
| 6     | Code             | [index.md](phases/built/index.md)                                   | evidence_index.json                                                                                                            |
| —     | **Checkpoint 2** | Verify evidence coverage                                           | —                                                                                                                             |

---

## Stage 2: Model (Phases 7–10)

From Phase 7 onward, a single artifact: `solution_model.json` (concepts, behaviors, interaction_tree, evidence_refs).

| Phase | Actor            | Ref                                                       | Outputs                                                                                          |
| ----- | ---------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 7     | AI               | [structure.md](phases/built/structure.md)                  | solution_model.json v1 (stories, steps, properties, inheritance, empty linked_behaviors)          |
| 8     | AI               | [behavior.md](phases/built/behavior.md)                    | solution_model.json v2 (+ operations, linked_behaviors, scenarios)                                |
| 9     | AI               | [variation.md](phases/built/variation.md)                  | solution_model.json v3 (+ subtype stories, failure-mode scenarios)                               |
| 10    | AI               | [consolidate.md](phases/built/consolidate.md)              | solution_model.json v4 (+ examples, anti-pattern fixes)                                          |
| —     | **Checkpoint 3** | Verify model quality and completeness                     | —                                                                                                |

---

## Stage 3: Assess (Phases 11–12)

| Phase | Actor    | Ref                                                   | Outputs                                                 |
| ----- | -------- | ----------------------------------------------------- | ------------------------------------------------------- |
| 11    | AI+Human | [assess.md](phases/built/assess.md)                   | assessment.json                                         |
| 12    | AI       | [finalize.md](phases/built/finalize.md)               | solution_model.json final (assessment fixes applied)    |
