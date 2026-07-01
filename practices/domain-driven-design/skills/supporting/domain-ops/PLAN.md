# domain-ops rebuild — ABD-sequenced plan

**Status:** Ready to execute. All architectural questions locked via grill-me. Fresh chat can run this end-to-end.

**Target root:** `practices/domain-driven-design/skills/supporting/domain-ops/`

**Mirror pattern:** [`story-graph-ops/src/`](../../../../story-driven-delivery/skills/supporting/story-graph-ops/src/) — same layout, same context-file placement, same three-layer inheritance, same uniform callable surface, same one-shot bootstrap rule for code.

---

## 1. Grill-me lockdown (architectural decisions)

| # | Decision | Answer |
|---|---|---|
| 1 | Overall shape | **Star around code.** Code is source. All other formats are projections off code, or one-shot bootstrap inputs. No N × N matrix. |
| 2 | In-memory pivot | `DomainMap` — exists only during a CLI operation. Not persisted. Produced by parsers, consumed by renderers. |
| 3 | Code generation rule | **One-shot bootstrap.** CLI refuses to overwrite existing code files unless `--force`. Once code exists, edit directly in code with AI/skills. Project outward freely. |
| 4 | Domain class shape in code | **Always `abstract class`.** Never interfaces. TS, Py, Java all use their abstract-class idiom. |
| 5 | Properties and operations | Public abstract members of the abstract class. |
| 6 | Invariants and interactions | **Private methods inside the same abstract class.** Method name is the label. Comment above if not self-describing. No decorators, no sidecar, no doc-tags. |
| 7 | Type references | `(label, referent)` pairs extracted once by the parser. Label = display text after unwrapping (`List<X>` → `X [0..*]`). Referent = class name for edge targeting. |
| 8 | Boundary domain | **Not stored.** Computed at render time: referent whose owning module ≠ current module → boundary treatment. |
| 9 | File layout for generated code | Ask at `generate` time. Support `--layout=file-per-ka` and `--layout=folder-per-ka`. |
| 10 | drawio backend | **Absorb `drawio-domain-sync` into domain-ops.** Preserve its AI-driven layout logic verbatim inside `formats/diagram/drawio/`. Common callable surface (parse / render / sync) same as every other backend. |
| 11 | Shared libraries | Extract to shared when boundary is clear — drawio XML utilities, markdown utilities. Defer forced extraction. |
| 12 | Phase / fidelity annotation in code | Language convention only — TSDoc / docstring / Javadoc. No invented tag format. |

---

## 2. Target file tree

Files marked `NEW` do not exist yet. Files marked `MOVE` are current flat scripts to be relocated. Files marked `KEEP` stay put.

```
domain-ops/
├── PLAN.md                                           NEW (this file)
├── SKILL.md                                          KEEP (may need minor updates)
├── scripts/
│   ├── domain_graph_cli.py                           MOVE → src/cli/domain_ops_cli.py
│   ├── code_emitter_ts.py                            MOVE → src/formats/code/typescript/emitter.py
│   ├── domain_graph_file.py                          MOVE → src/formats/document/json/domain_map.py
│   ├── domain_map.py                                 MOVE → src/core/domain/domain_map.py (partial)
│   ├── graph_filters.py                              MOVE → src/core/domain/ (partial)
│   ├── md_domain_model_to_domain_graph.py            MOVE → src/formats/document/markdown/parser.py
│   ├── md_domain_specification_to_domain_graph.py    MOVE → src/formats/document/markdown/parser.py
│   └── README.md                                     UPDATE
├── src/
│   ├── architecture-context.md                       NEW  (Phase A)
│   ├── domain-context.md                             NEW  (Phase D)
│   ├── bdd-context.md                                NEW  (Phase B1)
│   ├── cli/
│   │   ├── architecture-context.md                   NEW  (Phase A)
│   │   └── domain_ops_cli.py                         NEW  (Phase C)
│   ├── core/
│   │   └── domain/
│   │       ├── architecture-context.md               NEW  (Phase A)
│   │       ├── domain_node.py                        NEW  (Phase C)  # abstract base
│   │       ├── module.py                             NEW  (Phase C)
│   │       ├── key_abstraction.py                    NEW  (Phase C)
│   │       ├── property.py                           NEW  (Phase C)
│   │       ├── operation.py                          NEW  (Phase C)
│   │       ├── invariant.py                          NEW  (Phase C)  # private-method wrapper
│   │       ├── interaction.py                        NEW  (Phase C)  # private-method wrapper
│   │       ├── type_ref.py                           NEW  (Phase C)  # (label, referent)
│   │       ├── domain_map.py                         NEW  (Phase C)  # container + find_ka()
│   │       ├── update_report.py                      NEW  (Phase C)
│   │       └── node_snapshot.py                      NEW  (Phase C)
│   └── formats/
│       ├── code/
│       │   ├── architecture-context.md               NEW  (Phase A)
│       │   ├── code_domain_node.py                   NEW  (Phase C)  # family mixin
│       │   ├── typescript/
│       │   │   ├── parser.py                         NEW  (Phase C)
│       │   │   ├── emitter.py                        NEW  (Phase C, absorbs code_emitter_ts.py)
│       │   │   └── domain_map.py                     NEW  (Phase C)  # TypeScriptDomainMap
│       │   ├── python/
│       │   │   ├── parser.py                         NEW  (Phase C)
│       │   │   ├── emitter.py                        NEW  (Phase C)
│       │   │   └── domain_map.py                     NEW  (Phase C)
│       │   └── java/
│       │       ├── parser.py                         NEW  (Phase C)
│       │       ├── emitter.py                        NEW  (Phase C)
│       │       └── domain_map.py                     NEW  (Phase C)
│       ├── document/
│       │   ├── architecture-context.md               NEW  (Phase A)
│       │   ├── markdown/
│       │   │   ├── parser.py                         NEW  (Phase C, absorbs md_*.py)
│       │   │   ├── emitter.py                        NEW  (Phase C)
│       │   │   └── domain_map.py                     NEW  (Phase C)
│       │   └── json/
│       │       ├── parser.py                         NEW  (Phase C)
│       │       ├── emitter.py                        NEW  (Phase C, absorbs domain_graph_file.py)
│       │       └── domain_map.py                     NEW  (Phase C)
│       └── diagram/
│           ├── architecture-context.md               NEW  (Phase A)
│           ├── drawio/
│           │   ├── architecture-context.md           NEW  (Phase A — layout rules recap)
│           │   ├── parser.py                         NEW  (Phase C)
│           │   ├── emitter.py                        NEW  (Phase C)
│           │   ├── layout.py                         NEW  (Phase C — absorbs drawio-domain-sync layout)
│           │   └── domain_map.py                     NEW  (Phase C)
│           └── miro/
│               ├── parser.py                         NEW  (Phase C)
│               ├── emitter.py                        NEW  (Phase C)
│               └── domain_map.py                     NEW  (Phase C)
└── tests/
    ├── conftest.py                                   KEEP + expand
    ├── unit/
    │   ├── core/
    │   │   └── test_*.py                             NEW  (Phase B3)
    │   └── formats/
    │       ├── code/
    │       │   ├── typescript/test_*.py              NEW
    │       │   ├── python/test_*.py                  NEW
    │       │   └── java/test_*.py                    NEW
    │       ├── document/
    │       │   ├── markdown/test_*.py                NEW
    │       │   └── json/test_*.py                    NEW
    │       └── diagram/
    │           ├── drawio/test_*.py                  NEW
    │           └── miro/test_*.py                    NEW
    └── integration/
        └── test_matrix.py                            NEW  # code → md/json/drawio/miro round-trips
```

**Naming convention echo of story-graph-ops:** `core/domain/` (parallel to story-graph-ops's `core/stories/`). Format subdirectories keep the four-slot contract: `parser.py`, `emitter.py`, `domain_map.py`, plus a family mixin at the parent level.

---

## 3. ABD-sequenced execution

Each phase invokes one skill, produces a specific artefact family, and completes before the next phase begins.

### Phase A — Architecture Specification (`abd-architecture-specification`)

**Invoke:** `/abd-architecture-specification`

**Skill purpose recap:** produce mechanism catalogue, decisions, callable surface, patterns — the "how it hangs together" spec.

**Produce these `architecture-context.md` files:**

| Path | Contents |
|---|---|
| `src/architecture-context.md` | Top-level: **Multi-Format Domain Rendering** mechanism, star topology, one-shot bootstrap rule, uniform callable surface (`parse` / `render` / `sync`), one row per format backend. |
| `src/cli/architecture-context.md` | CLI as router only. Verbs: `generate`, `project`, `parse`, `sync`. Dispatch to `{fmt}DomainMap` by extension. Reports `UpdateReport`. |
| `src/core/domain/architecture-context.md` | Pure domain types. One-way dependency rule (core imports no format). `translateFrom` fixed algorithm (kept for non-code sync only). `find_ka(name)` resolver on `DomainMap`. |
| `src/formats/code/architecture-context.md` | Layer 2 mixin `CodeDomainNode` — holds `LanguageAst` boundary. Emitter always writes `abstract class` with public abstract members + private methods for invariants/interactions. Parser reads AST, extracts `(label, referent)` pairs. **`--force`-off overwrite guard**. |
| `src/formats/document/architecture-context.md` | Reference implementation of the base contract. Markdown and JSON. Bidirectional (unlike code). |
| `src/formats/diagram/architecture-context.md` | Layer 2 mixin for cross-KA edge extraction. Two backends: drawio (absorbs `drawio-domain-sync` layout) and miro. **AI-driven layout preserved verbatim inside drawio/layout.py.** |
| `src/formats/diagram/drawio/architecture-context.md` | Specific: page-per-KA, `«from: OtherModule»` ghost cards for cross-module referents, incremental edit preference, scanner rules from `drawio-domain-sync/rules/`. Links out to those rule files, does not duplicate them. |

**Verify:** [`abd-architecture-specification/reference/grill-me.md`](../../../../architecture-centric-engineering/skills/abd-architecture-specification/reference/grill-me.md) checklist. Mechanism instances share callable surface — see [`mechanism-instances-share-a-callable-surface.md`](../../../../architecture-centric-engineering/skills/abd-architecture-specification/rules/mechanism-instances-share-a-callable-surface.md).

---

### Phase D — Domain Specification (`abd-domain-specification`)

**Invoke:** `/abd-domain-specification`

**Skill purpose recap:** typed properties, operations with parameters, relationships, invariants, interactions — the "what the classes are" spec.

**Produce:** `src/domain-context.md`

**Domain of the domain-ops system itself:**

- **Module** (`core/domain/module.py`) — named group of KAs; children are `KeyAbstraction`.
- **KeyAbstraction** (`core/domain/key_abstraction.py`) — abstract class in the target language; children are `Property`, `Operation`, `Invariant`, `Interaction`.
- **Property** (`core/domain/property.py`) — public abstract member; carries `label`, `type_ref: TypeRef`, `cardinality`.
- **Operation** (`core/domain/operation.py`) — public abstract method; carries `label`, `parameters: [TypeRef]`, `return_type: TypeRef`.
- **Invariant** (`core/domain/invariant.py`) — private method wrapper; carries `label`, `description?`.
- **Interaction** (`core/domain/interaction.py`) — private method wrapper; carries `label`, `description?`.
- **TypeRef** (`core/domain/type_ref.py`) — value object `{label: str, referent: str | None}`. Referent is None for primitives.
- **DomainMap** (`core/domain/domain_map.py`) — root container; owns `modules`; exposes `find_ka(name) → KeyAbstraction | None`.
- **UpdateReport** (`core/domain/update_report.py`) — records changes from a `translateFrom` invocation. Used for non-code sync only.
- **NodeSnapshot** (`core/domain/node_snapshot.py`) — captures before-state for reversal. Same scope as `UpdateReport`.
- **LanguageAst** (boundary, held by composition in `CodeDomainNode` — no core file) — abstract handle to a language-specific AST fragment.

**Every class above is emitted as an `abstract class`** — this is dogfooding: domain-ops itself is written in Python using ABC as its abstract-class idiom, and the classes above are the domain of domain-ops itself.

**Boundary domain in `src/domain-context.md`:**

- `LanguageAst` — from language toolchains (TypeScript compiler API, Python `ast`, JavaParser).
- `DrawioXml` — from lxml or story-graph-ops's shared drawio utilities.
- `MiroSdk` — from Miro MCP server, when miro is wired.

**Verify:** [`abd-domain-specification/reference/grill-me.md`](../../../../.cursor/skills/abd-domain-specification/reference/grill-me.md). Every property has a typed `TypeRef`. Every operation has typed params and return. Cross-KA references resolved via `find_ka`. Boundary concepts explicitly marked.

---

### Phase B1 — BDD Behavior (`abd-bdd-behavior`)

**Invoke:** `/abd-bdd-behavior`

**Skill purpose recap:** plain-English "describe/it" hierarchy anchored to mechanisms and sub-epics.

**Produce:** `src/bdd-context.md`

**Behavior scaffold organised by mechanism:**

- **Multi-Format Domain Rendering**
  - given a code source tree
  - it should produce an in-memory `DomainMap`
  - it should refuse to write code files that already exist unless `--force`
  - it should project the same `DomainMap` to each registered format
- **Core Domain Model**
  - `DomainMap`
    - with modules containing key abstractions
    - it should resolve a KA name to its owning module
    - it should return None for an unknown name
  - `TypeRef`
    - with `List<X>` in the source
    - it should extract `X` as the referent and `X [0..*]` as the label
    - with `Optional<X>` in the source
    - it should extract `X` as the referent and `X [0..1]` as the label
- **Code Backend** (per language: TS, Py, Java)
  - with an abstract class in source
  - it should read it as a KeyAbstraction
  - it should read its public abstract members as properties/operations
  - it should read its private methods as invariants/interactions
  - given a DomainMap
  - it should emit an abstract class with public abstract members and private methods
- **Document Backend — Markdown**
  - with a domain-specification.md source
  - it should parse into a DomainMap
  - given a DomainMap
  - it should emit domain-specification.md
- **Document Backend — JSON**
  - with a domain-model.json source
  - it should parse into a DomainMap
  - given a DomainMap
  - it should emit domain-model.json
- **Diagram Backend — DrawIO**
  - given a DomainMap
  - it should render one page per KA using the preserved layout algorithm
  - it should render cross-module referents as `«from: OtherModule»` ghost cards
  - it should pass every scanner in `drawio-domain-sync/rules/`
  - with an existing .drawio file and a changed source
  - it should apply incremental edits, not regenerate from scratch
- **Diagram Backend — Miro**
  - given a DomainMap
  - it should render an equivalent board via Miro MCP
- **CLI**
  - given `generate --from foo.md --to typescript --out src/`
  - it should refuse if `src/` already contains matching class files
  - given `project --from src/ --to markdown --out foo.md`
  - it should always succeed and overwrite the target
  - it should print an `UpdateReport` summary

**Verify:** [`abd-bdd-behavior/reference/grill-me.md`](../../../../.cursor/skills/abd-bdd-behavior/reference/grill-me.md). Every subject-state-observable triple names one behavior. No implementation vocabulary. Every mechanism from Phase A appears in the scaffold.

---

### Phase B2 — BDD Test Skeleton (`abd-bdd-specification`)

**Invoke:** `/abd-bdd-specification`

**Skill purpose recap:** convert the behavior hierarchy into empty `describe`/`it` test structure with `# BDD: SIGNATURE` markers. No test bodies, no assertions, no mocks.

**Produce test skeleton files under `tests/unit/` and `tests/integration/`,** one per subject from Phase B1. Python `unittest` or `pytest` — whichever the repo already uses (check `conftest.py`).

Example — `tests/unit/core/domain/test_type_ref.py`:

```python
class TestTypeRef:
    class WithListXInSource:
        def test_it_should_extract_x_as_the_referent(self):
            # BDD: SIGNATURE
            pass

        def test_it_should_produce_x_multiplicity_zero_or_more_as_the_label(self):
            # BDD: SIGNATURE
            pass

    class WithOptionalXInSource:
        def test_it_should_extract_x_as_the_referent(self):
            # BDD: SIGNATURE
            pass

        def test_it_should_produce_x_multiplicity_zero_or_one_as_the_label(self):
            # BDD: SIGNATURE
            pass
```

**Verify:** every `it should` from Phase B1 has a corresponding `# BDD: SIGNATURE` test. No test contains logic. Structure mirrors the scaffold verbatim.

---

### Phase C — BDD Development + Clean Code (`abd-bdd-development` then `abd-clean-code`)

**Invoke sequentially:** `/abd-bdd-development` then `/abd-clean-code`

**abd-bdd-development produces:** test bodies (Arrange-Act-Assert) + minimum production code to pass each test. Standard red-green cycle. This is where the source files under `src/core/domain/`, `src/formats/*/`, and `src/cli/` come into being.

**abd-clean-code refines:** functions under 20 lines, domain language, constructor injection, no magic numbers, guard clauses, no dead comments.

**Execution order for source files** — do the leaves first, wire the CLI last:

1. **`src/core/domain/type_ref.py`** — value object, no dependencies.
2. **`src/core/domain/invariant.py`, `interaction.py`, `property.py`, `operation.py`** — leaf nodes.
3. **`src/core/domain/key_abstraction.py`, `module.py`** — containers of leaves.
4. **`src/core/domain/domain_map.py`** — top-level container + `find_ka` resolver.
5. **`src/core/domain/update_report.py`, `node_snapshot.py`** — sync bookkeeping.
6. **`src/formats/code/code_domain_node.py`** — family mixin (Layer 2).
7. **`src/formats/code/typescript/{parser,emitter,domain_map}.py`** — first code backend end-to-end. Reuse `scripts/code_emitter_ts.py` logic.
8. **`src/formats/code/python/…`** and **`src/formats/code/java/…`** — mirror TS.
9. **`src/formats/document/markdown/{parser,emitter,domain_map}.py`** — absorb existing `scripts/md_*.py` parsers.
10. **`src/formats/document/json/{parser,emitter,domain_map}.py`** — absorb existing `scripts/domain_graph_file.py`.
11. **`src/formats/diagram/drawio/{parser,emitter,layout,domain_map}.py`** — port from `drawio-domain-sync`. **Preserve layout logic verbatim.**
12. **`src/formats/diagram/miro/{parser,emitter,domain_map}.py`** — new, mirrors drawio structure.
13. **`src/cli/domain_ops_cli.py`** — router. Dispatch by target extension. Owns the `--force` guard for code targets.
14. **`tests/integration/test_matrix.py`** — round-trip suite: for every canonical fixture, project code → md/json/drawio/miro and back where allowed.

**Verify after each step:**
- Every `# BDD: SIGNATURE` in the corresponding test file is now a real test.
- Every `describe`/`it` group passes.
- `abd-clean-code` checklist (functions ≤ 20 lines, guard clauses, no magic numbers, no swallowed exceptions, no useless comments) — see [`abd-clean-code/SKILL.md`](../../../../../.cursor/skills/abd-clean-code/SKILL.md).

---

### Phase E — Cleanup & Migration

Post-implementation cleanup, not driven by a skill:

1. **Delete or archive** the old flat `scripts/` files that have been fully absorbed into `src/`. Update `README.md`.
2. **Update `SKILL.md`** at domain-ops root — new CLI verbs, new file paths.
3. **Deprecate `drawio-domain-sync`** — replace its `SKILL.md` with a redirect stub pointing to domain-ops's drawio backend. Move its rules (they're referenced from `formats/diagram/drawio/architecture-context.md`, not duplicated).
4. **Validate against pml-my** — round-trip pml-my's current domain-specification.md through the new pipeline. Diff should be zero (label-preserving).
5. **Update planning doc** at `docs/domain-multi-backend-planning.md` — mark phases done, retire obsolete rows.

---

## 4. What to run in a fresh chat

Paste this at the top of a fresh chat session:

> Read `practices/domain-driven-design/skills/supporting/domain-ops/PLAN.md`. Execute Phase A. Do not proceed to Phase D until Phase A's `architecture-context.md` files are written and I have approved them. When Phase A is complete, stop and wait for approval before continuing.

Same pattern for D, B1, B2, C, E.

---

## 5. Open items intentionally deferred

- **Miro backend implementation** can be stubbed in Phase C step 12 (empty emitter/parser) and completed after drawio is proven. Follow-up ticket.
- **Shared library extraction** (drawio XML utils, markdown utils between story-graph-ops and domain-ops) — defer to Phase E once both have landed. Do the copy-paste first, extract when the duplication is provably identical.
- **Rename detection** across code → markdown projections — not needed at bootstrap. If the user renames a KA in code, downstream projections regenerate labels/edges from scratch. No propagation logic.
- **AST parser depth** — start with what's needed to parse the pml-my and pml-midtier specs. Expand only when a real case fails.
