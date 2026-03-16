# Process

Pipeline: Context → Model → Validate. `pipeline.py` orchestrates all phases.

- Code phases — run scripts directly (normalize, extract, graph)
- `generate <phase>` — prints built phase spec from `phases/built/` (phase instructions + baked-in rules)
- `scan <phase>` — runs programmatic scanners against generated output
- `validate <phase>` — prints rules for adversarial AI validation pass

**Workspace layout** (relative to `output_dir`):
- `context/` — context_chunks.json
- `evidence/` — terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json, evidence_graph.json
- `generated/domain/` — concept_guidance.md, concept_guidance.json, concept_model.md, structural_model.md, behavior_model.md, variation_model.md, refined_domain_model.md, model_assessment.md, final_domain_model.md
- `generated/interaction_model/` — interaction_tree.md
- `generated/deltas/` — phase version snapshots

**Match user phrase to phase Trigger** — each phase file has a `## Trigger` section; run that phase when the user says one of those phrases.

**Log corrections immediately** — when the user corrects any output, add an entry to `corrections.md` in the solution directory before continuing. Format: phase, what was wrong, what is correct.


---

## Stage 1: Context (Phases 1–5)

| Phase | Actor | Ref | Outputs |
| ----- | ----- | --- | ------- |
| 1 | Code | [normalize_context.md](phases/normalize_context.md) | rule_chunks.json |
| 2 | AI | [concept_guidance_v1.md](phases/concept_guidance_v1.md) | concept_guidance.md, concept_guidance.json, interaction_tree (Story Map Skeleton: Epics, Sub-Epics, some stories) |
| — | **Checkpoint 1** | Verify domain framing: concepts, modules, mechanisms, actors, epics | — |
| 3 | Code | [evidence_extraction.md](phases/evidence_extraction.md) | terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json |
| 4 | Code | [evidence_graph.md](phases/evidence_graph.md) | evidence_graph.json |
| — | **Checkpoint 2** | Verify rule coverage: evidence graph covers rules | — |
| 5 | AI | [concept_guidance_v2.md](phases/concept_guidance_v2.md) | concept_guidance.md (refined), interaction_tree (Epics, Sub-Epics, some stories) |
| — | **Checkpoint 3** | Verify structure: epic/sub-epic/story placement | — |

---

## Stage 2: Model (Phases 6–10)

| Phase | Actor | Ref | Outputs |
| ----- | ----- | --- | ------- |
| 6 | AI | [concept_model.md](phases/concept_model.md) | concept_model.md, interaction_tree (more fleshed out; more sub-epics; epics can have stories) |
| 7 | AI | [structural_model.md](phases/structural_model.md) | structural_model.md, interaction_tree (+ Triggering/Responding-Actor, long name, state, pre-conditions) |
| 8 | AI | [behavior_model.md](phases/behavior_model.md) | behavior_model.md, interaction_tree (+ Trigger, Response, steps) |
| 9 | AI | [variation_model.md](phases/variation_model.md) | variation_model.md, interaction_tree (+ variation detail) |
| 10 | AI | [refined_domain_model.md](phases/refined_domain_model.md) | refined_domain_model.md, interaction_tree (+ Scenarios, Failure-Modes, Constraints, examples) |
| — | **Checkpoint 5** | Verify structural validation: modules, boundaries | — |

---

## Stage 3: Assess (Phases 11–12)

| Phase | Actor | Ref | Outputs |
| ----- | ----- | --- | ------- |
| 11 | AI+Human | [model_assessment.md](phases/model_assessment.md) | model_assessment.md |
| 12 | AI | [final_domain_model.md](phases/final_domain_model.md) | final_domain_model.md, interaction_tree (with Examples) |

