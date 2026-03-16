# abd-solution-modeler

Transforms raw context into a validated OO domain model. Pipeline: Guidance → Sketch → Refine.

---

## Context Preparation

Use **abd-context-to-memory** before Phase 1 if source is documents:

- `index_memory.py --path <source_folder>` — convert, chunk, embed
- Output: `chunk_index.json` (required for evidence extraction)
- Path: `skills/abd-context-to-memory`

**Config:** Set `chunk_index_path` or `context_path` in `conf/abd-config.json`. Or pass `--chunk-index PATH` / `--context-path PATH` when running the pipeline.

---

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
- `generated/deltas/` — phase version snapshots

**Match user phrase to phase Trigger** — each phase file has a `## Trigger` section; run that phase when the user says one of those phrases.

**Log corrections immediately** — when the user corrects any output, add an entry to `corrections.md` in the solution directory before continuing. Format: phase, what was wrong, what is correct.


---

## Stage 1: Context (Phases 1–5)

| Phase | Actor | Ref | Outputs |
| ----- | ----- | --- | ------- |
| 1 | Code | [normalize_context.md](phases/normalize_context.md) | rule_chunks.json |
| 2 | AI | [concept_guidance_v1.md](phases/concept_guidance_v1.md) | concept_guidance.md, concept_guidance.json |
| — | **Checkpoint 1** | Verify domain framing: concepts, modules, mechanisms, actors, epics | — |
| 3 | Code | [evidence_extraction.md](phases/evidence_extraction.md) | terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json |
| 4 | Code | [evidence_graph.md](phases/evidence_graph.md) | evidence_graph.json |
| — | **Checkpoint 2** | Verify rule coverage: evidence graph covers rules | — |
| 5 | AI | [concept_guidance_v2.md](phases/concept_guidance_v2.md) | concept_guidance.md (refined) |
| — | **Checkpoint 3** | Verify structure: epic/sub-epic/story placement | — |

---

## Stage 2: Model (Phases 6–10)

| Phase | Actor | Ref | Outputs |
| ----- | ----- | --- | ------- |
| 6 | AI | [concept_model.md](phases/concept_model.md) | concept_model.md |
| 7 | AI | [structural_model.md](phases/structural_model.md) | structural_model.md |
| 8 | AI | [behavior_model.md](phases/behavior_model.md) | behavior_model.md |
| 9 | AI | [variation_model.md](phases/variation_model.md) | variation_model.md |
| 10 | AI | [refined_domain_model.md](phases/refined_domain_model.md) | refined_domain_model.md |
| — | **Checkpoint 5** | Verify structural validation: modules, boundaries | — |

---

## Stage 3: Assess (Phases 11–12)

| Phase | Actor | Ref | Outputs |
| ----- | ----- | --- | ------- |
| 11 | AI+Human | [model_assessment.md](phases/model_assessment.md) | model_assessment.md |
| 12 | AI | [final_domain_model.md](phases/final_domain_model.md) | final_domain_model.md |

---

# Validation

## Three-Layer Model

Each AI phase uses three validation layers. All three are required.

**Layer 1 — Generate with rules.** Phase spec + accumulated rules are included in the generation instructions. Follow DO/DO NOT guidance while producing output. Rules are guidance — produce natural output that complies.

**Layer 2 — Scan.** After generation, run `pipeline.py scan <phase>`. Scanners check structural violations mechanically (naming, child counts, concept sync, property types). Fix reported violations before proceeding.

**Layer 3 — Validate.** After scanners, run `pipeline.py validate <phase>`. This prints all applicable rules. AI re-reads generated output against the rules AND the completeness checklists in Domain Model Format above. For each rule: does the output comply with the spirit, not just the letter? Report violations with rule name, location, proposed fix. Fix all violations. Re-validate until clean.

**This layer is critical.** Be adversarial. Take a contrarian stance. A scanner says "all clear" but the AI reviewing the rules sees that 3 operations on a concept all make decisions that belong to other concepts.

## AI Behavior Per Layer


| Layer           | Behavior                                                                            |
| --------------- | ----------------------------------------------------------------------------------- |
| Generation      | Follow rules naturally while producing output                                       |
| Scanner fixes   | Fix reported violations mechanically; re-run until clean                            |
| Validation pass | Adversarial checklist review — each rule is a checklist item; report ALL violations |


---

## Corrections Format

When recording corrections:

- **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be

---

# Domain Model Format

## Module

Heading: `## Module: <name>`

```
## Module: <name>
- concepts — **ConceptA**, **ConceptB**, **ConceptC**
```

## Domain Concept

Heading: `**ConceptName** : <BaseConcept if any>`

```
**ConceptName** : <BaseConcept if any>
- <type> property
      <collaborating concepts if any>
      Invariant: <constraint on this property>
- <type> operation(<param>, ...) → <return>
      <collaborating concepts if any>
      Invariant: <constraint enforced by this operation>
- Interactions: interaction nodes this concept is used by

```

### Invariants

Place invariants under the specific property or operation they apply to — not as a separate section. Format: `Invariant: <constraint>`.

```
- Number balance
      Invariant: balance >= 0
- debit(amount) → Boolean
      Invariant: amount <= balance
```

## Guidelines

- Prefer **composition** over inheritance
- Use `Dictionary<K,V>` when items are keyed
- Use `List<T>` only when ordering matters
- Avoid central "service/manager" concepts
- Use `EnumType name {value1, value2}` for constrained options — not `String` with parenthetical options

## Validation Checklist

- [ ] Format: `**Concept** : <Base Concept if any>`
- [ ] Properties, operations, collaborating concepts listed
- [ ] Each concept referenced via `**Concept**` in domain model must exist here
- [ ] Invariants under specific property/operation they apply to
- [ ] No implementation details (APIs, services, databases, UI components, code)
- [ ] No speculation beyond the provided material
- [ ] Everything at logical/domain level

---

## DrawIO Diagram Rendering

DrawIO class diagrams are generated from domain model `.md` files in `generated/domain/`.

- **Mandatory** — auto-generated after `final_domain_model`
- **Optional** — append `render-diagram` to any `generate` command

```bash
python scripts/pipeline.py generate final_domain_model render-diagram
python scripts/pipeline.py generate structural_model render-diagram
python scripts/pipeline.py drawio                        # standalone, from latest domain model
python scripts/pipeline.py drawio final_domain_model # standalone, from specific phase
```

Output: `generated/domain/<phase>.drawio` (alongside the source `.md` file).

---

## Scripts

```bash
python scripts/pipeline.py generate <phase>                  # Layer 1: phase spec + rules
python scripts/pipeline.py generate <phase> render-diagram   # Layer 1 + DrawIO
python scripts/pipeline.py scan <phase>                      # Layer 2: run scanners
python scripts/pipeline.py validate <phase>                  # Layer 3: rules + checklist for AI pass
python scripts/pipeline.py drawio [<phase>]                  # DrawIO from domain model
python scripts/pipeline.py pipeline                          # Run all phases (use --stop <phase>)
```

**Assemble AGENTS.md from pieces:**

```bash
python scripts/assemble_agents.py
```

