# Process

Pipeline: 12-phase concept-anchored. `pipeline.py` orchestrates all phases.

- **Code phases** — run scripts directly (normalize, extract_concepts, extract_evidence, index)
- **AI phases** — `generate <phase>` prints built phase spec from `phases/built/` (phase instructions + baked-in rules)
- **Scan** — `scan <phase>` runs programmatic scanners against generated output
- **Validate** — `validate <phase>` prints rules for adversarial AI validation pass

**Workspace layout** (relative to `output_dir`):

- `context/` — context_chunks.json
- `concept_signals/` — term_candidates.json, definition_candidates.json, dependency_actions.json, cooccurrence_graph.json, table_vocabularies.json
- `evidence/` — terms.json, actions.json, decisions.json, states.json, relationships.json, evidence_index.json
- `generated/` — extraction_config.json, hypothesis.json, solution_model.json, assessment.json
- `generated/domain/` — legacy .md outputs, solution_model.drawio

**Match user phrase to phase Trigger** — each phase file has a `## Trigger` section; run that phase when the user says one of those phrases.

**Log corrections immediately** — when the user corrects any output, add an entry to `corrections.md` in the solution directory before continuing. Format: phase, what was wrong, what is correct.

---

## Phases 1–6: Context and Evidence

| # | Phase | Actor | Output |
|---|-------|-------|--------|
| 1 | Normalize | Code | context_chunks.json |
| 2 | Configure extraction | AI | extraction_config.json |
| 3 | Extract Concepts | Code | concept_signals/*.json |
| 4 | Concept synthesis | AI | hypothesis.json |
| 5 | Extract evidence | Code | evidence/*.json |
| 6 | Index | Code | evidence_index.json |

---

## Phases 7–12: Solution Model

From Phase 7 onward, a single artifact: `solution_model.json` (concepts, behaviors, interaction_tree, evidence_refs).

| # | Phase | Actor | Output |
|---|-------|-------|--------|
| 7 | Structure | AI | solution_model.json v1 |
| 8 | Behavior | AI | solution_model.json v2 |
| 9 | Variation | AI | solution_model.json v3 |
| 10 | Consolidate | AI | solution_model.json v4 |
| 11 | Assess | AI+Human | assessment.json |
| 12 | Finalize | AI | solution_model.json final |
