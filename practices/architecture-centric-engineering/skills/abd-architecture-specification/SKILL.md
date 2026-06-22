---
catalog_garden_tier: practice
catalog_garden_order: 40
name: abd-architecture-specification
catalogue_one_liner: >-
  Tell engineers exactly how domain concepts become files, classes, and tests in a chosen stack.
description: >-
  Specify how domain concepts and stories map to files, classes, and tests in a chosen stack. Use when starting or extending an architecture spec for a project.
context-perspective: architecture
context-fidelity:
  - level: exploration
    mode: document
  - level: specification
    mode: template
---
# abd-architecture-specification

## Purpose

Tell engineers exactly how domain concepts and stories become files, classes, and tests in a chosen stack — so agents know exactly how to generate working code for a domain and story that follows the architecture.

---

## When to use

- A stack or project needs a **concrete mapping** from domain model and stories to production code and tests.
- You are starting a new architecture spec or **extending** an existing one with additional mechanisms.
- A kanban ticket names mechanisms in scope and you need to **assign** (reuse) or **create** (author) specification content.
- Template code must be **runnable** and validated against the architecture's own rules and scanners.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Domain-to-file mapping** — when a new domain concept appears, does the spec make it obvious which files get created, where they live, and what they're named — or does that require a judgment call every time?
- **Mechanism boundaries in code** — for each mechanism, can you point to exactly where its code starts and stops? If two mechanisms touch the same file or class, is the ownership clear or are they entangled?
- **Walkthrough vs. real flow** — does the walkthrough trace a path that a real request actually follows, or does it show an idealized sequence that skips the messy parts (retries, fallbacks, partial failures)?
- **Test tier proof** — what does each test tier actually prove about the architecture? If a tier is just re-testing the same behavior at a different layer, what unique architectural risk is it supposed to catch?
- **Pattern fit for edge cases** — the spec defines patterns for the common case, but what happens when a story doesn't fit the pattern cleanly? Where are the seams that will need judgment, and are those documented or left implicit?

---

## Core concepts

### Specification directory

The deliverable is a **specification directory** — not a lone markdown file. Where it lives does not matter; the shape does: `architecture-specification.md`, `template/`, `rules/`, and `scanners/` together form one specification. Produce a new directory for a project, or **assign** an existing complete directory when the architecture is already specified.

### Run modes

| Mode | Produces | When to use |
| --- | --- | --- |
| **document** | `architecture-specification.md` | Mechanism sections only; assigned spec with `template/` already exists |
| **template** | `template/` runnable code, spec `templates/` scaffold, `rules/`, `scanners/` | Code-first; documentation assigned separately |
| **both** (default) | Full specification directory | New spec or full refresh |

Respect the mode the user asks for (see **`reference/concepts.md` — Run modes**). Default to **both** when unspecified.

**Kanban defaults:** Exploration runs **document** mode; Specification runs **template** mode.

### Mechanism

A **mechanism** is how the architecture handles a cross-cutting runtime concern — persistence, error handling, web client, app server, and the like. Each mechanism gets the same five-part shape in the doc (principles, file structure, participants, flow, walkthrough). Testing strategy lives in the top-level **Testing Architecture** section, not inside individual mechanisms.

### Assign vs create

**Assign** links existing specification directories to a **story map node** — system, epic, or sub-epic — via that node's **`architecture-spec`** field. **Create** when no assigned spec covers what that node's stories need.

A node may reference **more than one** spec. Typical reasons: a stack baseline (e.g. `specs/mern/`) plus a scoped companion (e.g. an increment or integration spec), or different stacks touching the same epic.

| Node level | Assign when | Create when |
| --- | --- | --- |
| **System** | Complete spec directory exists for this stack | Bootstrapping a new architecture |
| **Epic** | Spec(s) already document this epic's mechanisms and patterns | Epic needs a new spec directory or mechanisms not in any assigned spec |
| **Sub-epic** | Assigned spec(s) already cover this sub-epic's stories | Sub-epic needs new mechanism sections or template slices |

Record assignments on the story map — not a separate mechanism table. Each affected node gets an **`architecture-spec`** list of spec directory paths. When authoring new content inside an assigned spec, resolve mechanisms there: assign existing sections; create only what is missing.

**Example** — epic with two assigned specs:

```
Epic: Wire Payment
  architecture-spec:
    - specs/mern/                              # assign — stack baseline
    - docs/architecture/wire-transfer/         # assign — epic-specific companion
```

**Example** — sub-epic needing new content:

```
Sub-epic: Refund Processing
  architecture-spec:
    - specs/mern/                              # assign
    - docs/architecture/refunds/               # create — new companion for this sub-epic
```

### Templates, template slice, and doc are peers

A complete spec directory has three peer folders:

- **`templates/`** — parameterized scaffold with `{{placeholders}}` for the full file layout (domain module, app roots, tests).
- **`template/`** — a filled instance of the templates with concrete domain values, plus `domain-spec.md` and `specification-by-example.md`.
- **`rules/`** and **`scanners/`** — validation against the architecture.

The doc (`architecture-specification.md`) references files in `template/`; `template/` is an instantiation of `templates/`. When either side changes, the others change in the same edit.

Full teaching — document skeleton, five-part shape, section organization, template domain modes, run modes, validation passes — lives in **`reference/concepts.md`**.

---

## Output

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

**Primary output:** a specification directory (see **Core concepts**).

| This skill's template | What to produce |
| --- | --- |
| `templates/architecture-specification.md` | The specification document — mechanism sections, walkthroughs, diagrams. |
| `templates/architecture-flow.drawio` | Draw.io flow diagram — one box per layer/participant, simple boxes and lines. Place next to the spec doc. |
| `templates/architecture-specification-participants.drawio` | UML class diagram of domain module participants — all 14 classes, full edge set, built by `scripts/build_participants_diagram.py`. |

The spec directory's own `templates/` folder (e.g. `specs/mern/templates/`) holds the parameterized code scaffold — that is the spec's asset, not this skill's.

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read all of these before doing anything else:
- **`reference/concepts.md`** and **`reference/examples.md`** — the ideas and worked examples behind this skill.
- **`reference/example.ts`** — merged template module (all tiers in one file); catalog hero and shape reference for the runnable template slice.
- **`templates/architecture-specification.md`** — the document skeleton and placeholder vocabulary.

### 2. Ask — mode and template domain

If not already clear from context or kanban ticket:

**Run mode** — if the user did not specify:

> Should this run produce **document** only, **template** only, or **both** (default)?

**Template domain** — when mode is **template** or **both**, if the answer is not already clear:

> Should the runnable template use a **real story** from this project, or a **toy domain** (Calculator, Pet Store, Library, or agent's choice)?

Record answers in a short **Run decisions** block at the top of the run output.

### 3. Create or update the specification

If a specification directory already exists for this architecture, update it — add missing mechanisms, fix drift. If none exists, create one.

Each spec directory has a **`templates/`** folder — a parameterized scaffold that is the peer of `template/`. The scaffold mirrors the template's file layout with `{{placeholders}}` instead of concrete domain values. When the spec already has templates (e.g. `specs/mern/templates/`), use them to generate the template slice; when bootstrapping a new spec, create the templates alongside the template slice.

#### Mode: template or both — template slice first

When mode is **template** or **both**, build the runnable template before writing documentation:

1. **Domain spec** — produce `template/domain-spec.md` following `abd-domain-specification`.
2. **Spec by example** — produce `template/specification-by-example.md` following `abd-story-specification`.
3. **Tests** — write acceptance tests from the scenarios following `abd-story-acceptance-test`.
4. **Code** — write the production code from the spec's `templates/` (replace placeholders with domain values), following `abd-clean-code` and the spec's own `rules/`.
5. **Run tests and fix** — tests must pass before moving on.
6. **Human review** — when mode is **both**, present the template code to the user for review. Wait for go-ahead before the document pass. When mode is **template** only, present for review at the end of this pass.

#### Mode: template or both — scaffold and validation artifacts

After template slice is ready (and user go-ahead when mode is **both**):

1. **`templates/`** — parameterized scaffold that mirrors `template/` file-for-file. Every source file in `template/` must have a corresponding template file with `{{placeholders}}` replacing the concrete domain values. The scaffold includes the same folder structure: `domain-module/` (shared, server, client), `app-server/`, `app-client/`, `tests/`, root configs. See `specs/mern/templates/` for the shape.
2. **`rules/`** — one rule file per checkable concern, following the rule shape in this skill's own `rules/`.
3. **`scanners/`** — automated checks that enforce the rules against generated code.

Create all three from scratch when bootstrapping a new architecture spec. Skip recreation when assigning an existing complete spec.

#### Mode: document or both — specification document

When mode is **document** or **both**:

1. **`architecture-specification.md`** — write from this skill's `templates/architecture-specification.md`. Every walkthrough step must reference a real file in `template/` when that folder exists; otherwise use parameterized pattern comments and point at `templates/`.

2. **`architecture-flow.drawio`** — produce a Draw.io flow diagram alongside the specification document. Start from `templates/architecture-flow.drawio`; replace placeholder labels with the actual layer and file names for this architecture. Rules: plain boxes and lines only (no gradient fills, no swimlane shading); one box per layer/participant; network or tier boundaries as lightly shaded full-width rectangles; simple arrow labels ("renders", "calls", "routes to", "extends", "uses", "read/write"). Place the file next to `architecture-specification.md` and reference it with `> See [architecture-flow.drawio](./architecture-flow.drawio)` in the Architecture Flow section.

When mode is **document** only, do not create or edit files under `template/` unless the user explicitly asks to refresh template code in the same run.

When mode is **template** only, skip `architecture-specification.md` unless the user explicitly asks for document work in the same run.

### 4. Assign to story map

Link the specification directory to the relevant story map node(s) — system, epic, or sub-epic — via the node's `architecture-spec` field. A node can hold more than one spec path.

### 5. Validate

Follow **`common`**. Run only the passes that match the mode:

**A — Specification document** (modes **document** and **both**): Read every file in **`abd-architecture-specification/rules/`**; emit a per-rule PASS/FAIL verdict per `../common/skill-rule-workflow.md`.

**B — Template code** (modes **template** and **both**): Read every file in the spec directory's own **`rules/`**; emit per-rule PASS/FAIL on the template slice. Then run scanners:

```bash
python skills/common/scripts/run_scanners.py \
  --skill-root <path-to-spec-directory> \
  --workspace <path-to-template-root> \
  --language typescript
```

Re-run until all scanners pass. Repeat applicable passes after any fix.

---

## Validate

**Goal:** Inspect what was built — read the docs and run the code as reviewers.

- **Per-rule verdict** — every applicable file in **`rules/`** gets PASS or FAIL with reason; no silent skips.
- **Run decisions recorded** — mode and template-domain answers appear before any generation.
- **Reuse honored** — story map node(s) for this run have `architecture-spec` updated with every assigned or created spec path; multiple specs per node when warranted; no duplicate mechanism sections inside assigned specs.
- **Specification directory complete** — for mode **both** on a new spec: doc, `template/`, `templates/`, `rules/`, and `scanners/` present; assigned specs cited, not recreated.
- **Templates mirror template slice** — when mode includes **template**: every source file in `template/` has a corresponding parameterized file in `templates/` with `{{placeholders}}`; same folder structure, same file names (modulo domain substitution).
- **Doc template shape followed** — when mode includes **document**: deliverable matches this skill's `templates/architecture-specification.md` skeleton; template instructions not copied into output.
- **Flow diagram produced** — when mode includes **document**: `architecture-flow.drawio` exists next to `architecture-specification.md`; the Architecture Flow section references it; ASCII block is also present; drawio uses plain boxes and lines only.
- **Template artifact set aligned** — when mode includes **template**: code, `specification-by-example.md`, and `domain-spec.md` use consistent concept names; tests pass; no stubs.
- **Template validation** — when mode includes **template** and template code was created or edited, architecture spec rules pass and `run_scanners.py` exits zero.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
