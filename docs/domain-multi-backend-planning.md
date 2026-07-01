# Domain skills — multi-backend migration plan

**Status:** Phase 1 complete. Phase 2 in progress — P2.1 (all templates + concepts.md + generate.md for both skills) and P2.4 (`domain_graph_cli.py generate` CLI, TypeScript emitter) are done and verified end-to-end against `tmp/pml-my-model.json` (12 files emitted, both fidelities, refuse-on-overwrite guard fires with exit 5). Remaining Phase 2 work: P2.2 (AST parsers TS/Python/Java), P2.3 (markdown emitters), P2.5 (skill flow doc — already partially done inside generate.md), P2.6 (scanner migration), P2.7 (pml-my validation).
**Scope:** `abd-domain-specification`, `abd-domain-model`, `domain-ops`, `drawio-domain-sync`.
**Author intent:** Allow domain specifications and domain models to be authored as **code** (TypeScript / Python / Java) in addition to markdown, with code as the source of truth and markdown as a rendered or fallback format. Diagrams, scanners, and other consumers run against a canonical in-memory model the source loaders produce.

This document is the runnable plan. Read it end-to-end before touching code.

---

## 1. Problem we're solving

Today the domain spec lives as hand-authored markdown (`docs/domain/specification/domain-specification.md` in each project). The codebase that's supposed to satisfy the spec (e.g. `pml-domain/src/*.ts`) drifts because:

- The spec is markdown, the code is TypeScript, and there's no shared schema both sides validate against.
- Invariants, interactions, stereotypes, and references live only in markdown — the type-checker can't enforce them.
- Multiple specs exist for the same domain at different layers (`pml-my`, `pml-midtier`) with bespoke shapes (e.g. midtier's "Two-Phase Proxy Pattern"), each drifting independently.

Goal: collapse those into one authoring surface (code) with a parser pipeline that feeds the same downstream consumers (scanners, diagrams, markdown rendering).

---

## 2. Reference architecture — story-graph-ops + drawio-story-sync

The plan mirrors the architecture already in place for stories. Read these first:

**Practice skills (audit their file layout before touching anything — the domain skills will get the same shape):**
- `practices/story-driven-delivery/skills/abd-story-mapping/` — minimal `SKILL.md`, `templates/story-map.md` (markdown only at outline fidelity), `reference/generate.md`, `reference/concepts.md`, `rules/`
- `practices/story-driven-delivery/skills/abd-story-acceptance-criteria/` — same layout **plus** per-language templates `templates/stories.ts` / `.js` / `.java`, and a **"Code format" section in `reference/concepts.md`** (lines 29–69) anchoring the code grammar
- `practices/story-driven-delivery/skills/abd-story-specification/` — same layout plus `templates/specification-by-example.ts` / `.js` / `.java` / `.md` and `reference/generate.md` documenting the code flow

**Supporting skills:**
- `practices/story-driven-delivery/skills/supporting/story-graph-ops/` — canonical JSON schema, typed walk model, CLI (`read` / `write` / `sha` / `inject-spec` / `generate`), validation, lifecycle on disk
- `practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_*_to_story_graph*.py` — markdown-to-canonical converters
- `practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_cli.py` — CLI including the `generate` verb (JSON → `*-stories.ts` scaffolding, refuses to overwrite) that P2.4 mirrors
- `practices/story-driven-delivery/skills/supporting/drawio-story-sync/scripts/drawio_story_sync/story_io_synchronizer.py` — consumer that loads the canonical model and renders diagrams

**Domain baseline (pre-migration):**
- Existing `c:\dev\paradise-mobile\.cursor\skills\domain-ops\SKILL.md` and its scripts — the domain analog, currently JSON-only
- Existing `practices/domain-driven-design/references/domain-model-json.md` — current schema `abd-domain-model/v1`
- Existing `practices/domain-driven-design/skills/abd-domain-specification/reference/concepts.md` — stereotype list and typed notation reference (P2.1 adds a "Code format" section here)

**Key insight from the story-skill audit:** the practice skills primarily author **code** now, not markdown. Markdown templates are retained as a design artifact for exploration, but as soon as a project scales, work moves into the code artifact (`*-stories.ts` for stories, `<ka-slug>.ts` for domain) and markdown is re-rendered on demand by ops. The **same source file evolves across skill stages** — story map → AC → scenarios all live in the same `*-stories.ts`; likewise model fidelity → specification fidelity in the same `<ka-slug>.ts`. The plan below applies this pattern to domain.

**Architectural pattern to copy:**

```
                  ┌──────────────────────────────────────────┐
                  │  source (skill-authored)                 │
   skill writes ─►│  TypeScript / Python / Java / Markdown   │
                  └──────────────────────────────────────────┘
                                  │
                                  ▼  CLI projection (read-side):
                                  │  language-specific AST parser
                                  │  + scanner pass
                                  ▼
                  ┌──────────────────────────────────────────┐
                  │  in-memory canonical model (typed walk)  │
                  └──────────────────────────────────────────┘
                                  │
                                  ▼  CLI persists if asked
                                  ▼
                  ┌──────────────────────────────────────────┐
                  │  JSON  →  diagrams, markdown render,     │
                  │           scanner outputs, other tools   │
                  └──────────────────────────────────────────┘

greenfield only (D22):
   markdown/JSON ── one-shot CLI `generate` ──► code (refuses to overwrite)
                                                  ▲
                                                  └─ skill takes over from here
```

The "swappable backends" of story-graph-ops are different markdown input shapes (story-map, AC, thin-slice). Here, the swappable backends are **languages** — TypeScript, Python, Java, and Markdown. Each backend has its own AST parser and its own scanner suite; all feed the same canonical model.

**Who writes what (D22 / D23):**

| Artefact | Owner | Tool |
|---|---|---|
| Source code (`*.ts`, `*.py`, `*.java`) when it exists | Skill (AI) | Practice-skill templates; AI direct edits |
| `domain-specification.md` / `domain-model.md` | Skill (AI) | Markdown template |
| `domain-context.md` (module-level prose) | Skill (AI) | Hand-written |
| Canonical JSON `domain-model.json` | CLI (derived) | `domain-ops` projection |
| Markdown render from code | CLI (derived) | `domain-ops` emitter |
| Initial code skeleton when **no** code exists | CLI (one-shot) | `generate` — uses skill templates as stamps; TypeScript in v1 |

---

## 3. Decisions log

Locked decisions from grilling. Do not relitigate without explicit user direction.

| # | Decision |
|---|---|
| D1 | Anything the target language's type system can carry, carries it (types, inheritance, parameter names, return types, visibility). Anything else that is a **structural marker** (stereotype, relationship kind, invariant vs. interaction classification, init policy, phase grouping) rides in language-standard doc comments — JSDoc in TypeScript, docstrings in Python, Javadoc in Java. Free-text **prose** (module intro, boundary-domain framing, cross-class rationale, source citations, decisions) does not ride in doc comments — it lives in `domain-context.md` at the folder root. **We are not building a DSL** — the container is idiomatic domain classes in the target language |
| D2 | One class per Key Abstraction. Phase grouping (e.g. "Onboarding operations" / "Self-care operations") is a comment-only concern, not a structural split |
| D3 | `domain-context.md` lives at the folder root holding the source files. Same convention as `architecture-context.md`. Module-level prose lives here |
| D4 | Code is the source of truth when it exists. Markdown is the source of truth when no code exists. Markdown is also a valid render output |
| D5 | Practice skills prompt for output format at generation time. Default = pick a language |
| D6 | Initial language matrix: **TypeScript**, **Python**, **Java**, **Markdown**. More can be added later |
| D7 | Pipeline: source → AST → in-memory canonical model → (optional) JSON → consumers |
| D8 | Mirror the story-graph-ops + drawio-story-sync architecture entirely. Do not invent a new pattern |
| D9 | Scope is `abd-domain-model` + `abd-domain-specification` only. `abd-domain-language` and `abd-domain-glossary` stay markdown-only — their value is the deliberation, not the structural artifact |
| D10 | Markdown→canonical and code↔canonical converters live in `domain-ops`, not in the practice skills. Practice skills produce markdown / code; `domain-ops` lifts them |
| D11 | Three phases — P1 markdown converters, P2 code emitters + AST parsers + skill prompts, P3 diagram sync switch |
| D12 | Code emit target = **abstract classes** (TS `abstract class`, Python `abc.ABC`, Java `abstract class`). Not interfaces alone. Carry constructors, init policy, abstract method signatures |
| D13 | The small set of structural doc-comment tags from D1 (`@stereotype`, `@initialisation`, `@composition`/`@aggregation`/`@association`, `@invariant`, `@interaction`) is **parser-readable, not runtime-enforced**. The AST loader lifts them; they do not generate runtime guards |
| D14 | `domain-context.md` catches any prose that doesn't fit cleanly in doc comments (module scope, boundary-domain framing, cross-class rationale, callouts) |
| D15 | Schema `abd-domain-model/v1` evolves **in place**. Single schema; sparser at model fidelity, fuller at specification fidelity. Do not fork into `domain-specification/v1` |
| D16 | Scanners walk the **source AST** (language-aware, format-specific). The in-memory canonical model feeds downstream consumers but is not the scanner target |
| D17 | File granularity is asked at generation time. Defaults: one folder per module + one file per KA. Also support one folder per KA when consumers need multiple files per KA (back end, front end, persistence) |
| D18 | Boundary domain = regular classes in their own files, imported where used, with `domain-context.md` describing the nature of the dependency. No special structural marker beyond stereotype |
| D19 | Migration order: `abd-domain-specification` first, then back-port to `abd-domain-model`. The specification skill carries the richest field set, so getting it right teaches us what the model skill needs |
| D20 | Stereotype canonical list inherited from `abd-domain-specification/reference/concepts.md` — Entity, ValueObject, Service, Factory, Repository, DomainEvent, and boundary types as documented. **No additions.** `ProxyController` and similar project-invented stereotypes get normalised to one of the canonical ones with a doc-comment note |
| D21 | Phase grouping uses each language's standard mechanism — TypeScript `@group` JSDoc tag (TypeDoc-recognised); Python docstring section headers; Java `//region` banner or equivalent. The AST parser handles whichever convention the language carries |
| D22 | **CLI is read-side / projection only** for existing code. Once language sources exist on disk, only the practice skill (AI) edits them. CLI responsibilities: `code → canonical JSON`, `code → markdown`, `JSON → markdown`. **One exception:** a `generate` bootstrap that seeds code from markdown/JSON when no code exists; it refuses to overwrite. After `generate` runs, the CLI never touches those files again. Verb name and semantics mirror `story_graph_cli.py generate` exactly |
| D23 | Practice skills carry **language templates** for TypeScript, Python, Java alongside the existing markdown template. The AI selects the template based on the user's chosen output format and authors the code directly — making the design judgments (file layout, naming, idioms, doc-comment phrasing). The CLI does **not** emit code in steady state; its only write path is the one-shot scaffold from D22 |
| D24 | Invariants and interactions are represented as **empty abstract methods with tight, intention-revealing names**. Signature is `abstract <camelCaseNameSayingTheRule>(): void`. The method name IS the rule — the `@invariant` / `@interaction` doc-comment tag is a **bare marker** (no free-text argument) that classifies the method. Step-by-step interaction narrative (from legacy markdown specs) does not survive into code; it lives in `domain-context.md` if it must be preserved, or as comments in the concrete implementation that calls the interaction method. The markdown → JSON path (P1) still lifts legacy free-text `invariants[]` / `interaction[]` arrays for backwards compatibility |
| D25 | **Practice skills primarily author code, not markdown, once a project scales.** Markdown templates are retained for exploration and as a fallback; language templates live alongside them (`.ts`/`.py`/`.java` — plain extensions, valid source files). The `reference/concepts.md` "Code format" section anchors the code grammar authoritatively. As soon as code exists for a module, all edits flow through the code, and markdown is regenerated on demand by `domain-ops`. This mirrors the story-driven-delivery skill layout exactly (audit `abd-story-acceptance-criteria/` and `abd-story-specification/` before making changes to the domain skills) |
| D26 | **Same file evolves across skill fidelities.** Just as `<slug>-stories.ts` grows through story-map → AC → spec stages without file splits, the `<ka-slug>.ts` file grows from model fidelity (`abd-domain-model`) to specification fidelity (`abd-domain-specification`) in place. The skill graduating a KA never creates a new file; it edits the existing one to add `@stereotype`, `@invariant` / `@interaction` methods, and `@composition`/`@aggregation`/`@association` markers |

### Out of scope

- Runtime invariant enforcement (D13)
- `abd-domain-language` / `abd-domain-glossary` migration (D9)
- Architecture-perspective skills (`abd-architecture-specification` and siblings) — same pattern would apply, separate plan
- Forking the schema — must evolve in place (D15)
- **Any CLI write path for code beyond the one-shot `generate`** (D22). Updates to existing `*.ts` / `*.py` / `*.java` are skill-only. No `derive-to-code`, no `sync-back-to-code`, no `--merge` for the scaffold

---

## 4. Phase 1 — schema evolution + markdown converters

**Goal:** `domain-ops` can lift existing markdown specs into the canonical model. No practice-skill changes. No code emission yet.

### P1.1 Evolve `abd-domain-model/v1` schema

File: `practices/domain-driven-design/references/domain-model-json.md` (the schema doc) and `practices/domain-driven-design/references/domain-model-template.json`.

Add these fields. All optional at model fidelity, populated at specification fidelity:

| Path | Type | Meaning |
|---|---|---|
| `class.stereotype` | enum string | `"Entity"`, `"ValueObject"`, `"Service"`, `"Factory"`, `"Repository"`, `"DomainEvent"`, `"Boundary"`. Per D20. Optional |
| `class.initialisation` | enum string | `"constructor"`, `"internal"`, `"factoryMethod"`, `"factoryObject"`. Optional. Describes how instances are bootstrapped |
| `class.constructor.parameters` | array of `{name, type}` | Replaces `parameter_types: [Type]` with named parameters. Existing field stays for back-compat; loader populates both |
| `operation.parameters` | array of `{name, type}` | Same replacement for operation parameters |
| `operation.phase` | string \| null | Free-text grouping label (e.g. `"onboarding"`, `"self-care"`). Optional |
| `module.intro` | string \| null | Long-form prose for the module's opening paragraph (markdown allowed) |
| `module.boundary_domain.intro` | string \| null | Long-form prose for the boundary-domain section |
| `key_abstraction.intro` | string \| null | KA-level intro paragraph (currently `definition` exists as one line — keep that; add `intro` for multi-paragraph) |

Validation update in `domain-ops/scripts/domain_graph_file.py`:
- New fields are accepted and validated (enum membership for `stereotype` and `initialisation`)
- Loader is forward-compatible — old JSON without these fields still validates

**Note on `invariants[]` / `interaction[]` (per D24):** the schema retains these as arrays of strings. Markdown-source specs lift free-text rules and step-by-step lines into these arrays (legacy shape). Code-source specs emit one entry per empty `@invariant` / `@interaction` method — the entry is the method name in camelCase. Downstream renderers render both shapes the same way (short bullet lines); the difference is invisible to diagrams.

### P1.2 Add markdown→canonical converters in `domain-ops`

Location: `c:\dev\paradise-mobile\.cursor\skills\domain-ops\scripts\` (and the upstream `practices/domain-driven-design/skills/supporting/domain-ops/scripts/`).

Mirror story-graph-ops naming:

- `md_domain_specification_to_domain_graph.py` — converts a specification-fidelity markdown into a `DomainMap` dict. **Build this first (D19).**
- `md_domain_model_to_domain_graph.py` — converts a model-fidelity markdown into a `DomainMap` dict. Build after the specification one stabilises.

Each script:

1. Parses frontmatter, module heading, KA headings, class blocks, property/operation lines, invariant lines, interaction blocks, references, decisions
2. Emits a validated `DomainMap` dict matching the evolved schema
3. Exposes a CLI: `python md_domain_specification_to_domain_graph.py --input <path.md> --output <path.json>`
4. Has unit tests under `tests/` (mirror the `test_md_*_to_story_graph.py` style)

### P1.3 Validate against existing markdown

First real input: `c:\dev\paradise-mobile\pml-my\docs\domain\specification\domain-specification.md`.

Expected behaviour:
- Frontmatter `state: class-model` triggers a warning ("expected `domain-specification`") but does not block
- KAs parse cleanly: Customer, Subscription, Catalog, Cart, Billing, Payment
- Stereotypes lift: `<< Entity >>`, `<< ValueObject >>`, `<< Service >>`, `<< DomainEvent >>` → `class.stereotype`
- Phase headers (`**Onboarding operations** (metadata.verified = false):`) lift each method below them with `operation.phase = "onboarding"` (and `"self-care"` for the next block)
- Invariants on properties and operations lift to `invariants[]`
- Interaction blocks lift to `interaction[]` as string lines
- References lift to `references[]`
- "decisions made" bullets lift to `decisions[]` per KA
- Boundary Domain section lifts to `module.boundary_domain` with `boundary_domain.intro` carrying the framing paragraph

Then: re-author `c:\dev\paradise-mobile\pml-midtier\docs\domain\domain-specification.md` to fit the canonical schema (per D20):
- `<< ProxyController >>` → `<< Service >>` with a doc-comment note
- "Two-Phase Proxy Pattern" callout → moved into `domain-context.md` at the midtier domain root
- Each operation's `Phase 1 — Inbound:` / `Phase 2 — Outbound:` blocks → folded into a single `Interaction:` block

### P1.4 P1 success criteria

- Both `md_domain_specification_to_domain_graph.py` and `md_domain_model_to_domain_graph.py` exist with tests
- `pml-my` and re-authored `pml-midtier` markdown specs round-trip through the converter into validated JSON
- `domain-ops/scripts/domain_graph_cli.py read` on the emitted JSON exits clean
- No practice-skill changes
- Existing `drawio-domain-sync` still works (it still reads the markdown directly; the new JSON is unused so far)

---

## 5. Phase 2 — language templates, AST parsers, and one-shot bootstrap

**Goal:** Authors can choose to maintain the domain as TypeScript, Python, or Java source. **Code is the source of truth, and the skill writes and evolves the code directly.** The CLI projects code into JSON / markdown for tools and humans, and provides a one-shot bootstrap from markdown when no code exists yet (D22).

### Contract reminder (D22 / D23)

| Operation | Owner |
|---|---|
| Author / edit `*.ts`, `*.py`, `*.java` when code already exists | **Skill** (AI), using language templates |
| Author / edit `domain-specification.md`, `domain-model.md`, `domain-context.md` | **Skill** (AI) |
| `code → canonical JSON` | **CLI** (AST parsers) |
| `code → markdown` rendering | **CLI** (emitter chain) |
| `JSON → markdown` rendering | **CLI** (emitter) |
| First-time skeleton when no code exists for the module | **CLI** `generate` (one-shot, refuses to overwrite; TS in v1) |
| Any subsequent edit to those files | **Skill** — CLI never touches them again |

This split mirrors story-graph-ops' `scaffold-from-json` (one-shot bootstrap) + `derive-from-fs` (read-side projection) — see `practices/story-driven-delivery/skills/supporting/story-graph-ops/reference/fs-migration.md`.

### P2.1 Skill updates — templates, concepts, generate reference

Mirror the story-driven-delivery layout **exactly** (audit `practices/story-driven-delivery/skills/abd-story-acceptance-criteria/`, `.../abd-story-specification/`, `.../abd-story-mapping/` before touching anything). Each affected practice skill grows:

**`practices/domain-driven-design/skills/abd-domain-specification/`**

| Path | Change | Content |
|---|---|---|
| `templates/domain-specification.md` | keep | existing markdown template |
| `templates/domain-specification.ts` | **new** | valid TypeScript file with placeholder identifiers (e.g. `<Ka Display Name>`, `Customer`, `Identity`) — the AI writes real code that looks like this |
| `templates/domain-specification.py` | **new** | valid Python file, same shape via `abc.ABC` + `@abstractmethod` and docstring tags |
| `templates/domain-specification.java` | **new** | valid Java file, `abstract class` + Javadoc tags + `//region` banners |
| `reference/concepts.md` | **edit** | add a **"Code format"** section (mirror `abd-story-acceptance-criteria/reference/concepts.md` lines 29–69) showing the exact code shape with tags per D24 |
| `reference/generate.md` | **new or edit** | explains the flow: bootstrap from markdown → code via `domain_graph_cli.py generate`, then AI takes over. Cite the story analog and `fs-migration.md` |
| `rules/*.md` | unchanged | rules stay language-agnostic — they enforce semantics (stereotype list, invariant coverage), not syntax |
| `SKILL.md` | unchanged | stays a minimal router pointing at `rules/`, `reference/`, `templates/` — same as `abd-story-*/SKILL.md` |

**`practices/domain-driven-design/skills/abd-domain-model/`** — same set of file-level changes, at the lower fidelity from D19 (types-only parameters, no `@stereotype` required, no `@invariant` / `@interaction` methods, no `@composition` markers on primitives).

**Naming (mirror `<slug>-stories.ts`):**

| Concern | Story convention | Domain convention |
|---|---|---|
| File name | `<sub-epic-slug>-stories.ts` | `<ka-slug>.ts` — one file per KA (D17 default) |
| Folder | `tests/<epic>/<sub-epic>/` | `src/domain/<module-slug>/` |
| Export identifier | `SCREAMING_SNAKE_STORY_NAME` | `PascalCaseKAName` (the class itself) |

**Same-file evolution (mirror story → AC → spec in one `*-stories.ts` file):**

The exact same `<ka-slug>.ts` file evolves as fidelity grows. At **model fidelity** (`abd-domain-model`) the file has only real types, inheritance, and constructor signatures. At **specification fidelity** (`abd-domain-specification`) the same file gains `@stereotype` on the class, `@composition`/`@aggregation`/`@association` on fields, `@invariant` and `@interaction` empty methods, and region banners for phase grouping. **No new file is created** when a KA graduates from model to spec — the existing file grows.

The TypeScript shape at specification fidelity (one KA per file by default — D17):

```ts
// === KA: Customer ===

/** @stereotype Entity @initialisation constructor */
export abstract class Customer {
  /** @composition */ abstract identity: Identity
  /** @composition */ abstract address: Address
  /** @composition */ abstract cart: Cart

  constructor(email: EmailAddress, password: Password) { /* ... */ }

  // region Onboarding operations        ← phase grouping per D21
  abstract searchNumber(keyword: Keyword): NumberOption[]
  abstract reserveNumber(option: NumberOption): Reservation
  // endregion

  // region Self-care operations
  abstract cancelSubscription(): void
  // endregion

  // region Invariants                    ← per D24: empty methods, name IS the rule
  /** @invariant */ abstract keywordMustBeAtMostFiveChars(): void
  /** @invariant */ abstract emailMustBeUniqueAcrossActiveCustomers(): void
  // endregion

  // region Interactions                  ← per D24: empty methods, name IS the summary
  /** @interaction */ abstract customerSearchesForNumberDuringOnboarding(): void
  // endregion
}
```

**What's in the file:** real types on properties and operations (compiler-checked), abstract-class inheritance for extension, region banners for phase grouping.

**What's in doc comments** — only the four structural markers the type system can't carry:
- `@stereotype <name>` on the class
- `@initialisation <mode>` on the class
- `@composition` / `@aggregation` / `@association` on each domain-relationship property
- `@invariant` / `@interaction` on empty methods to mark their role (bare markers — the method name carries the meaning per D24)

**What's NOT in the file:** module-level prose, boundary-domain framing, cross-class rationale, source citations, decision history. Those live in `domain-context.md` at the folder root (D3, D14).

Python template uses `abc.ABC` + `@abstractmethod` with docstring tag lines. Java template uses `abstract class` with Javadoc tags and `//region` banners. Both mirror the TS shape one-for-one so the canonical model is identical regardless of source language.

**Stereotype list per D20** — no `@stereotype ProxyController`; project-invented stereotypes get folded into one of the canonical ones (Entity / ValueObject / Service / Factory / Repository / DomainEvent / Boundary) with any explanatory prose living in `domain-context.md`, not in the doc comment.

**Templates are valid source files, not stamp fragments.** Each language template compiles / imports cleanly with its placeholder identifiers substituted. The AI uses the template as an authoring reference — it's the same source of truth used for the CLI `generate` scaffold (P2.4), so both paths produce identical structure. The `reference/concepts.md` "Code format" section is authoritative for the grammar; the templates are exemplars of that grammar.

**Templates are AI-fillable, not CLI-stampable in steady state.** The skill reads the chosen template, makes the design judgments (file layout, naming, idioms, doc-comment phrasing, what does and does not get factored into a separate file), and writes the code directly. The same templates are reused by `generate` (P2.4) as deterministic stamps when there is no code yet to make judgments about.

### P2.2 AST parsers (CLI read-side: code → canonical JSON)

New loaders under `practices/domain-driven-design/skills/supporting/domain-ops/scripts/loaders/`:

- `typescript_loader.py` — invokes a small Node helper using the TypeScript Compiler API (or `ts-morph`); emits canonical JSON over stdout; Python wrapper spawns and validates
- `python_loader.py` — stdlib `ast` + docstring parsing
- `java_loader.py` — `javalang` (Python pkg) or a small Java helper invoking JavaParser

Each produces a `DomainMap` dict matching the evolved schema. Test parity: the same `pml-my` domain authored in TypeScript must round-trip to the same canonical JSON as the markdown version produced by the P1 converters.

Tag dictionary the parsers must extract (kept deliberately small per D1 / D24):

| Tag | Where | Carries |
|---|---|---|
| `@stereotype <name>` | class | `class.stereotype` (validated against D20 list) |
| `@initialisation <mode>` | class | `class.initialisation` |
| `@composition` / `@aggregation` / `@association` | property | sets the corresponding `relationships[]` entry `kind` |
| `@invariant` (bare marker) | empty abstract method | classifies the method as an invariant; method name is the rule |
| `@interaction` (bare marker) | empty abstract method | classifies the method as an interaction; method name is the summary |
| `// region <name>` … `// endregion` (or language equivalent, D21) | wraps a group of operations | sets `operation.phase` for each operation inside |

Everything else the type checker already carries: parameter names and types, return types, visibility, inheritance. There is no `@ref`, no free-text `@invariant <rule>`, no multi-line `@interaction` block — source citations and step-by-step narratives live in `domain-context.md` (D14).

CLI surface:

```
python domain_graph_cli.py derive-from-code \
    --code-root <path>/src/domain \
    --language ts|py|java \
    --output <path>/docs/domain/domain-model.json
```

### P2.3 Markdown emitters (CLI read-side: canonical → markdown)

New scripts under `practices/domain-driven-design/skills/supporting/domain-ops/scripts/`:

- `domain_graph_to_md_specification.py` — takes a `DomainMap` dict, emits a `domain-specification.md` matching the shape the P1 spec converter consumes
- `domain_graph_to_md_model.py` — same, model-fidelity

Composed with the AST parsers (P2.2), this gives `code → markdown` for free: parse to canonical, emit markdown. CLI surface:

```
python domain_graph_cli.py render-md \
    --source <path>/src/domain \
    --language ts|py|java|json \
    --fidelity specification|model \
    --output <path>/docs/domain/domain-specification.md
```

Round-trip test: `pml-my` markdown spec → canonical → markdown emitter → diff against original (small whitespace deltas accepted; structural deltas are bugs).

### P2.4 One-shot `generate` (CLI write-once)

New CLI subcommand — the exact analog of `story_graph_cli.py generate`. **Only write path the CLI offers for code.**

```
python domain_graph_cli.py generate \
    --file <path>/docs/domain/domain-model.json \
    --output <path>/src/domain \
    --language ts \
    --layout folder-per-module|folder-per-ka \
    [--dry-run]
    [--expect-sha <sha-of-json>]
```

**Note on language coverage in v1:** story-graph-ops' `generate` command emits TypeScript only; other languages are AI-authored using the templates. Follow the same pattern for domain: **TypeScript is the initial generate target; Python and Java code is AI-authored using the templates as reference**. The AST parsers (P2.2) still cover all three languages for the read-side — the asymmetry is only in the one-shot scaffold.

Behaviour:

1. Parse the markdown via the P1 converters into the canonical model (if the input is markdown), or load JSON directly
2. Stamp out files using the same per-language template the skill uses (P2.1) as a deterministic template
3. Walk the canonical model and write one file per KA (or per module, depending on `--layout`)
4. **Convert legacy free-text invariants/interactions to empty methods (D24).** For each string in `invariants[]` or `interaction[]`, generate an empty abstract method with a camelCase name derived from the string, tagged `@invariant` / `@interaction`. The original free-text is dropped (it lived in markdown; it doesn't survive into code). If the free-text was step-by-step narrative that must be preserved, the scaffold appends it to a `TODO:` block at the top of the KA's sibling `domain-context.md` for the skill to relocate — the code file itself stays clean
5. Write a sibling `domain-context.md` at the module folder root carrying the module intro paragraph plus any TODO blocks from step 4
6. **Refuse to overwrite any existing file.** If the output tree already contains files, exit with a clear error pointing the user at the skill instead. No `--force` flag in v1
7. After running, the CLI must never edit those files again — the skill takes over

The verb is deliberately named `generate` (matching `story_graph_cli.py generate` — see `practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_cli.py`) rather than `scaffold-from-md`. Semantics are identical: one-shot, refuses to overwrite, safe to extend by hand after.

This mirrors story-graph-ops' `scaffold-from-json` per `fs-migration.md` line 53: "Without `--merge`, the command refuses to overwrite any file (safer default)."

Tests use `pml-my`'s markdown as input and verify the scaffold produces:
- A TypeScript skeleton that compiles
- That same skeleton parses back to the canonical model via P2.2
- That canonical model matches the one produced by parsing the original markdown directly

### P2.5 Skill flow (mirrors story-driven-delivery skill flow)

The story skills don't ask the user "what language?" — they discover the target from the project (existing `*-stories.ts` vs `.java` vs markdown) and route through `reference/generate.md`. Domain skills do the same:

1. **Discover target format.** If the module folder already contains `*.ts` / `*.py` / `*.java`, that's the target language. If only markdown exists, target = markdown. If nothing exists, ask.
2. **Read `reference/generate.md` and `reference/concepts.md`** — the "Code format" section anchors the grammar for the target language.
3. **Read the relevant template** — `templates/<name>.<lang>` for the target.
4. **If bootstrapping code from an existing markdown/JSON source and no code exists**, invoke `domain_graph_cli.py generate` (P2.4). The CLI writes the initial skeleton; the skill takes over from there.
5. **If code already exists**, the skill edits files directly using the template as an authoring reference. **CLI is never invoked to write code in this case.**
6. **Always maintain `domain-context.md`** at the module folder root — new prose the type system can't carry lands there (D14).

The `SKILL.md` file itself stays a minimal router — same shape as `abd-story-mapping/SKILL.md`. All routing lives in `reference/generate.md`.

Migration order per D19: do `abd-domain-specification` first (richer template surface teaches us what the lower-fidelity `abd-domain-model` template needs). After it stabilises, mirror the same skill-directory changes into `abd-domain-model`.

### P2.6 Scanner migration

Per D16, scanners walk the source AST.

- Existing markdown scanners continue to apply to the markdown backend
- New TypeScript scanners under `scanners/typescript/` enforce the same rules at the JSDoc/AST level (e.g. "every `abstract` method has `@invariant` or explicit `@invariant none`", "tag names match D20 stereotype list")
- Same for Python and Java scanner suites
- Each rule has parallel implementations across backends — the *rule* is single, the *enforcement* is per-language
- CLI exposes `validate --language <lang>` to run the suite for a given source tree

### P2.7 P2 success criteria

- All four language templates (md + ts + py + java) exist for both `abd-domain-specification` and `abd-domain-model`, as **valid source files** (compile / import clean with placeholder identifiers)
- `reference/concepts.md` in both skills has a **"Code format"** section documenting the code grammar (D24 tag set, empty-method invariant/interaction shape, region banners)
- `reference/generate.md` in both skills exists and documents the "discover target → read template → invoke `generate` if bootstrapping, else edit directly" flow (P2.5)
- Rules directories are unchanged (language-agnostic per D16)
- AST parsers for all three languages emit canonical JSON that validates against the evolved schema
- `pml-my` domain re-emitted as TypeScript (either via `generate` scaffold or AI hand-authoring from the template) parses back to a canonical JSON that matches the JSON produced by the P1 markdown converter
- Markdown emitter round-trips: `pml-my` markdown → canonical → emitted markdown ≈ original (structural equivalence)
- `domain_graph_cli.py generate` against `pml-my` markdown produces a TS skeleton that:
  - Compiles
  - Refuses to be re-run against the same `--output` tree (overwrite protection works, mirroring `story_graph_cli.py generate`)
  - Parses back to a canonical JSON matching the one produced from the source markdown
- Skill flows: when given an existing code tree, skill edits code files directly without invoking any CLI write command
- Same-file evolution works: a `<ka-slug>.ts` written at model fidelity can be grown to specification fidelity by the skill without any file split
- `pml-my` consumer code (which currently does `implements ICustomer`) still compiles after the skill regenerates the domain via the TS template

---

## 6. Phase 3 — diagram sync switch

**Goal:** `drawio-domain-sync` loads via the canonical model. Source format becomes irrelevant to the diagram pipeline.

### P3.1 Changes

`c:\dev\paradise-mobile\.cursor\skills\drawio-domain-sync\`:
- `drawio_domain_cli.py` accepts any source (md / ts / py / java) — extension or `--language` flag selects the loader from `domain-ops`
- Internally loads the source → canonical `DomainMap` → existing rendering pipeline (unchanged)
- **Sync-back honours D22.** Markdown sources can be written back directly (markdown is a CLI-rendered view). Code sources are **not** written by the diagram CLI. Two options to evaluate during P3.1:
  - **Option A — markdown-mediated sync-back:** diagram CLI emits a diff against the rendered markdown view of the code; the skill applies that diff to the code. CLI writes nothing to `*.ts` / `*.py` / `*.java`
  - **Option B — read-only for code:** sync-back is supported for markdown sources only. For code sources, the CLI errors with "diagram edits to code sources must be applied through the practice skill; re-run `render-md` first"

### P3.2 P3 success criteria

- Same diagram is produced whether the source is markdown or TypeScript / Python / Java
- Sync-back from diagram to markdown works as before
- Sync-back never writes to `*.ts` / `*.py` / `*.java` (D22). The chosen Option A / B behaviour is implemented and tested
- Python and Java sources are diagram-readable

---

## 7. Working file paths

Everything in the upstream `c:\dev\abd-skills\` tree must also land in the consumer copy at `c:\dev\paradise-mobile\.cursor\skills\` (the project pulls the skills from there). Keep both in sync per the existing convention.

Key paths:

| Concern | Upstream | Consumer |
|---|---|---|
| Schema doc | `practices/domain-driven-design/references/domain-model-json.md` | (consumed via skill) |
| Schema template | `practices/domain-driven-design/references/domain-model-template.json` | (consumed via skill) |
| domain-ops scripts | `practices/domain-driven-design/skills/supporting/domain-ops/scripts/` | `c:\dev\paradise-mobile\.cursor\skills\domain-ops\scripts\` |
| Domain-specification skill | `practices/domain-driven-design/skills/abd-domain-specification/` | `c:\dev\paradise-mobile\.cursor\skills\abd-domain-specification\` (if mirrored) |
| Domain-model skill | `practices/domain-driven-design/skills/abd-domain-model/` | `c:\dev\paradise-mobile\.cursor\skills\abd-domain-model\` (if mirrored) |
| Drawio sync | `practices/domain-driven-design/skills/supporting/drawio-domain-sync/` | `c:\dev\paradise-mobile\.cursor\skills\drawio-domain-sync\` |
| Example markdown spec (real-world test input) | — | `c:\dev\paradise-mobile\pml-my\docs\domain\specification\domain-specification.md` |
| Example markdown spec (proxy variant, needs re-authoring) | — | `c:\dev\paradise-mobile\pml-midtier\docs\domain\domain-specification.md` |
| Hand-crafted TS that motivated the plan (informational, not normative) | — | `c:\dev\paradise-mobile\pml-domain\src\*.ts` |

---

## 8. Tactical questions deferred to execution

The following are not strategic decisions; they get nailed down when the relevant phase starts:

- Tag names are locked (P2.2 dictionary). If a language convention forces a rename (e.g. Python docstring style prefers `:stereotype:` over `@stereotype`), that's a per-language spelling decision made when the loader is written, not a schema decision
- TypeScript Compiler API host vs `ts-morph` vs `.d.ts` parsing — pick during P2.2 based on which gives the cleanest doc-comment tag extraction
- Whether `// region <name>` or an alternative reads best for TypeScript phase grouping — pick during P2.1
- Diagram-to-code sync-back path (Phase 3) — **the CLI does not write code (D22)**, so a diagram edit that needs to change code must either: (a) produce a derived markdown delta that the skill applies to the code, or (b) error out and tell the user to re-author through the skill. Pick during P3.1 based on which gives the cleanest handoff
- Project-specific converter variants (e.g. `_pml_midtier.py` suffix) — only create one if the canonical converter genuinely can't handle the variant. Default = re-author markdown to fit the canonical shape per D20

---

## 9. How a fresh agent should run this plan

1. Read sections 1–3 of this document end-to-end. Do not skip the decisions log
2. Read the artefacts in section 2 — **especially the practice-skill layouts** for `abd-story-mapping`, `abd-story-acceptance-criteria`, and `abd-story-specification` (the domain skills will get the same shape)
3. Confirm the user wants to start P1 (or which phase). Do not start P2 before P1 is signed off
4. Within a phase, work top-to-bottom through the sub-sections (P1.1 → P1.2 → P1.3 → P1.4)
5. **When making skill-level changes (P2.1, P2.5), the story skills are the ground truth for layout.** Cross-reference their `templates/`, `reference/concepts.md`, `reference/generate.md`, `rules/`, and `SKILL.md` structure before authoring the domain equivalents. Diverge only where D24 or a domain-specific concern requires it, and note the divergence in the PR
6. For every script and template you produce, write tests in the same commit
7. Validate work against the real inputs in section 7 ("Example markdown spec") before declaring a sub-section done
8. When in doubt about a tactical choice (section 8), make the smallest reasonable decision and surface it in the PR description rather than re-grilling the user

Do **not**:
- Relitigate D1–D26 without explicit user direction
- Add new stereotypes beyond D20's list
- Split a single KA across multiple files when it graduates from model to spec fidelity (D26 — same file evolves)
- Try to do all three phases in one pass
- Touch architecture skills, story skills, glossary/language skills, or runtime invariant enforcement (out of scope)
