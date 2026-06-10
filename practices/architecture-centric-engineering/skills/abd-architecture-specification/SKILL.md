---
catalog_garden_tier: practice
catalog_garden_order: 40
name: abd-architecture-specification
catalogue_one_liner: >-
  Specification that defines how to create code that follows a particular architecture.
description: >-
  Produce an architecture specification that instantiates domain and story scope into runnable code.
  Use when you need to specify how stories and domain objects map to files, classes, and tests across a stack.
  Run in document, template, or both modes (default both).
---
# abd-architecture-specification

## Purpose

An **architecture specification** tells engineers exactly how domain concepts and stories become code in a chosen stack — which files, classes, interactions, and tests implement each entity, operation, and scenario. The specification is one artifact: documentation and working template code stay aligned; each mechanism is documented once and reused; later runs extend only what is missing.

---

## When to use

- A stack or project needs a **concrete mapping** from domain model and stories to production code and tests.
- You are starting a new architecture spec or **extending** an existing one with additional mechanisms.
- A kanban ticket names mechanisms in scope and you need to **assign** (reuse) or **create** (author) specification content.
- Template code must be **runnable** and validated against the architecture's own rules and scanners.

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

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**Primary output:** a specification directory (see **Core concepts**).

| This skill's template | What to produce |
| --- | --- |
| `templates/architecture-specification.md` | The specification document — mechanism sections, walkthroughs, diagrams. |

The spec directory's own `templates/` folder (e.g. `specs/mern/templates/`) holds the parameterized code scaffold — that is the spec's asset, not this skill's.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read all of these before doing anything else:
- **`reference/concepts.md`** and **`reference/examples.md`** — the ideas and worked examples behind this skill.
- Every file in **`rules/`** — the pass/fail bar for the specification document.
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

When mode is **document** only, do not create or edit files under `template/` unless the user explicitly asks to refresh template code in the same run.

When mode is **template** only, skip `architecture-specification.md` unless the user explicitly asks for document work in the same run.

### 4. Assign to story map

Link the specification directory to the relevant story map node(s) — system, epic, or sub-epic — via the node's `architecture-spec` field. A node can hold more than one spec path.

### 5. Validate

Follow **`execute-skill-using-skills-rules`**. Run only the passes that match the mode:

**A — Specification document** (modes **document** and **both**): Read every file in **`abd-architecture-specification/rules/`**; emit a per-rule PASS/FAIL verdict per `../agent-protocol.md`.

**B — Template code** (modes **template** and **both**): Read every file in the spec directory's own **`rules/`**; emit per-rule PASS/FAIL on the template slice. Then run scanners:

```bash
python foundational/skill-helpers/skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
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
- **Template artifact set aligned** — when mode includes **template**: code, `specification-by-example.md`, and `domain-spec.md` use consistent concept names; tests pass; no stubs.
- **Template validation** — when mode includes **template** and template code was created or edited, architecture spec rules pass and `run_scanners.py` exits zero.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
