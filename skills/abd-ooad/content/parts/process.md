# OOAD Process — Phase-Based Walkthrough

**Pipeline:** Workspace → Domain Scan & Initial Sketch → Extraction → Refinement → Validation

---

## Process Table

| # | Phase | Description | Actor | Input | Output | Scripts |
|---|-------|-------------|-------|-------|--------|---------|
| 0 | [Workspace and config](phases/workspace-and-config.md) | Set active skill workspace; configure project root | Human | Project directory | `skill-config.json` updated | `python scripts/base/set_workspace.py <path>` |
| 1 | [Domain scan](phases/domain-scan.md) | Scan source, identify 3–7 anchors, flag tensions, produce initial model sketch | AI | Source material (spec, code, manual, transcript) | `domain-scan-results.md` + `domain-scan-model.md` + `domain-scan-model.drawio` + `domain-walkthrough.md` + `domain-walkthrough.drawio` + `term-registry.md` | `python scripts/base/generate.py --phase domain-scan` |
| 2 | [Nouns, verbs, rules, and states](phases/nouns-verbs-rules-and-states.md) | Careful extraction: mark nouns, verbs, rules, states per section | AI | Source material + domain-scan results | Extraction findings + updated term-registry.md | `python scripts/base/generate.py --phase nouns-verbs-rules-and-states` |
| 3 | [Raw candidate list](phases/raw-candidate-list.md) | Sort findings into entities, values, processes, policies, roles, events | AI | Extraction results | Candidate class inventory + updated term-registry.md | `python scripts/base/generate.py --phase raw-candidate-list` |
| 4 | [Thing vs data about a thing](phases/thing-vs-data-about-a-thing.md) | Separate independent entities from value objects, enums, properties | AI | Candidate list | Refined entities with clear boundaries | `python scripts/base/generate.py --phase thing-vs-data-about-a-thing` |
| 5 | [Responsibilities before operations](phases/responsibilities-before-operations.md) | Define what each class is responsible for (before methods) | AI | Entities | Responsibility statements per class | `python scripts/base/generate.py --phase responsibilities-before-operations` |
| 6 | [Add properties semantically tight](phases/add-properties-semantically-tight.md) | Give each class only the properties it needs to fulfill responsibilities | AI | Responsibilities | Classes with semantic properties | `python scripts/base/generate.py --phase add-properties-semantically-tight` |
| 7 | [Turn verbs into operations](phases/turn-verbs-into-operations.md) | Distribute verbs to classes that own the behavior | AI | Verbs from extraction + classes | Class operations (methods) | `python scripts/base/generate.py --phase turn-verbs-into-operations` |
| 8 | [Relationships and cardinality](phases/relationships-and-cardinality.md) | Define associations, composition, aggregation, multiplicity | AI | Classes + operations | Class diagram with relationships | `python scripts/base/generate.py --phase relationships-and-cardinality` |
| 9 | [Invariants in the model](phases/invariants-in-the-model.md) | Encode domain rules into class behavior (not external code) | AI | Rules from extraction + class diagram | Classes with enforced invariants | `python scripts/base/generate.py --phase invariants-in-the-model` |
| 10 | [Watch for bloated classes](phases/watch-for-bloated-classes.md) | Identify and split overly complex classes | AI | Candidate model | Classes split by cohesion | `python scripts/base/generate.py --phase watch-for-bloated-classes` |
| 11 | [Smashed abstractions](phases/smashed-abstractions-and-hidden-roles.md) | Separate overloaded nouns into distinct roles | AI | Candidate model | Separated role-specific classes | `python scripts/base/generate.py --phase smashed-abstractions-and-hidden-roles` |
| 12 | [Inheritance when behavior generalizes](phases/inheritance-when-behavior-generalizes.md) | Use inheritance only for genuine behavior generalization | AI | Classes | Inheritance hierarchy (if needed) | `python scripts/base/generate.py --phase inheritance-when-behavior-generalizes` |
| 13 | [Abstract classes and interfaces](phases/abstract-classes-and-interfaces.md) | Choose abstractions for shared contract vs shared state | AI | Inheritance candidates | Abstract classes / interfaces | `python scripts/base/generate.py --phase abstract-classes-and-interfaces` |
| 14 | [Prefer composition](phases/prefer-composition.md) | Use composition instead of inheritance for variability | AI | Classes | Refactored classes with composed parts | `python scripts/base/generate.py --phase prefer-composition` |
| 15 | [Model state transitions](phases/model-state-transitions.md) | Make invalid states unrepresentable or rejected | AI | Classes + state rules | State models or enums | `python scripts/base/generate.py --phase model-state-transitions` |
| 16 | [Iterative refinement](phases/iterative-refinement.md) | Re-evaluate model against source; resolve contradictions | AI | Current model + source material | Refined model (second pass) | `python scripts/base/generate.py --phase iterative-refinement` |
| 17 | [Tension as a signal](phases/tension-as-a-signal.md) | Use design friction to adjust boundaries or record debt | AI | Model + design notes | Adjusted model or debt log | `python scripts/base/generate.py --phase tension-as-a-signal` |
| 18 | [What changes together](phases/what-changes-together.md) | Group cohesive properties/operations; identify bounded contexts | AI | Refined classes | Cohesive class clusters | `python scripts/base/generate.py --phase what-changes-together` |
| 19 | [Validate with scenarios](phases/validate-with-scenarios.md) | Test model against realistic workflows | AI | Current model | Scenario walkthroughs + corrections | `python scripts/base/generate.py --phase validate-with-scenarios` |
| 20 | [Refine names](phases/refine-names.md) | Align naming with domain language and stakeholder vocabulary | AI | Model + domain expert input | Renamed classes / operations | `python scripts/base/generate.py --phase refine-names` |
| 21 | [Model in layers](phases/model-in-layers.md) | Organize final artifacts across domain, application, infrastructure layers | AI | Finalized classes | Layered model documentation + diagrams | `python scripts/base/generate.py --phase model-in-layers` |

---

## Standards and Tools

- **Diagrams:** See `using-diagram-cli` library shard — `scripts/drawio_cli.py` workflow, `templates/` directory, and all layout rules.
- **Workspace routing:** See [`../library/workspace-and-config.md`](library/workspace-and-config.md) for `skill_path`, `skill_workspace`, and portable path resolution.

---

## Build and Generate

- **Build all phases into AGENTS.md:** `python scripts/base/build.py`
- **Generate a single phase:** `python scripts/base/generate.py --phase <slug>`
- **List available phases:** See **`skill-config.json`** → **`phase_files`**

---

## Implementation Notes

**AI-driven phases:** Each phase can be executed by Claude following the assembled instructions from **`generate.py`** or **`AGENTS.md`**.

**Code-driven phases:** Workspace config (Phase 0) is CLI-driven; all OOAD phases (1–21) are AI-driven narrative/modeling.

**Static vs dynamic delivery:**
- **Dynamic (default):** `generate.py` assembles phase on each call
- **Static:** `build.py` pre-assembles to `phases/built/`; `generate.py --mode static` reads cached version
