# Process

Pipeline: Context → Model → Assess. `pipeline.py` orchestrates all phases.

- Code phases — run scripts directly (normalize, concept_index, evidence_extraction, evidence_index)
- AI phases — **the AI does the work** (concept_synthesis, structure, behavior, variation, consolidate, assess, finalize). Do NOT write scripts for AI phases. Read inputs, reason, produce output directly.
- `generate <phase>` — prints built phase spec from `phases/built/` (phase instructions + baked-in rules)
- `scan <phase>` — runs programmatic scanners against generated output
- `validate <phase>` — prints rules for adversarial AI validation pass

**Workspace layout** (relative to `output_dir`):

- `context/` — context_chunks.json
- `concept_signals/` — concept_signals.json, concept_signals.md (12-signal output + markdown render)
- `evidence/` — terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json, evidence_index.json
- `generated/` — extraction_config.json, hypothesis.json, hypothesis.md, solution_model.json, assessment.json
- `generated/domain/` — legacy .md outputs, solution_model.drawio

**Match user phrase to phase Trigger** — each phase file has a `## Trigger` section; run that phase when the user says one of those phrases.

**Log corrections immediately** — when the user corrects any output, add an entry to `corrections.md` in the solution directory before continuing. Format: phase, what was wrong, what is correct.

---

## Stage 1: Context and Evidence (Phases 1–7)


| #   | Phase                                       | Actor | What it does                                                                                                      | Ref                                                                                                   | Outputs                                                                       |
| --- | ------------------------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 1   | **Normalize**                               | Code  | Chunk and clean raw source into uniform text segments.                                                            | [normalize.md](phases/built/normalize.md)                                                             | context_chunks.json                                                           |
| 2   | **Configure concept extraction parameters** | AI    | Calibrate weights, patterns, thresholds for 12 evidence-signal techniques (3 scans: structure, behavior, tuning). | [configure_concept_extraction_parameters.md](phases/built/configure_concept_extraction_parameters.md) | extraction_config.json                                                        |
| 3   | **Concept Extraction**                      | Code  | Run extraction using config; produce concept signals. Loop to Phase 2 if signals fail.                            | [concept_extraction.md](phases/built/concept_extraction.md)                                           | concept_signals.json, concept_signals.md                                      |
| 4   | **Concept Index**                           | Code  | Merge signals into hypothesis (concept index) with chunk_ids per concept.                                         | [concept_index.md](phases/built/concept_index.md)                                                     | hypothesis.json, hypothesis.md                                                |
| 5   | **Concept Synthesis**                       | AI    | Curate concepts (merge/split/kill), build hierarchy, allocate evidence.                                           | [concept_synthesis.md](phases/built/concept_synthesis.md)                                             | hypothesis.json (refined)                                                     |
| 6   | **Evidence extraction**                     | Code  | Mine chunks for actions, decisions, states, relationships, terms; guided by hypothesis.                           | [evidence_extraction.md](phases/built/evidence_extraction.md)                                         | evidence/*.json (terms, actions, decisions, states, relationships, modifiers) |
| 7   | **Evidence Index**                          | Code  | Aggregate evidence into concept-anchored index.                                                                   | [evidence_index.md](phases/built/evidence_index.md)                                                   | evidence_index.json                                                           |


---

## Stage 2: Model (Phases 8–11)

From Phase 8 onward, a single artifact: `solution_model.json` (concepts, behaviors, interaction_tree, evidence_refs).


| #   | Phase            | Actor | What it does                                                                                          | Ref                                           | Outputs                |
| --- | ---------------- | ----- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------- | ---------------------- |
| 8   | **Structure**    | AI    | Build first solution_model from hypothesis + evidence index: properties, inheritance, stories, steps. | [structure.md](phases/built/structure.md)     | solution_model.json v1 |
| 9   | **Behavior**     | AI    | Assign operations, link behaviors to steps, group steps into scenarios.                               | [behavior.md](phases/built/behavior.md)       | solution_model.json v2 |
| 10  | **Variation**    | AI    | Split stories by subtype when mechanics differ; add failure modes.                                    | [variation.md](phases/built/variation.md)     | solution_model.json v3 |
| 11  | **Consolidate**  | AI    | Fix anti-patterns (anemia, over-centralization); add examples.                                        | [consolidate.md](phases/built/consolidate.md) | solution_model.json v4 |


---

## Stage 3: Assess (Phases 12–13)


| #   | Phase        | Actor    | What it does                                                                          | Ref                                     | Outputs                   |
| --- | ------------ | -------- | ------------------------------------------------------------------------------------- | --------------------------------------- | ------------------------- |
| 12  | **Assess**   | AI+Human | Produce model assessment: consistency, coverage, completeness, type-field-vs-subtype. | [assess.md](phases/built/assess.md)     | assessment.json           |
| 13  | **Finalize** | AI       | Apply assessment fixes; produce validated model.                                      | [finalize.md](phases/built/finalize.md) | solution_model.json final |


