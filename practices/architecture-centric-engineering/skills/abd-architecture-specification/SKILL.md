---
catalog_garden_tier: practice
catalog_garden_order: 40
name: abd-architecture-specification
catalogue_one_liner: >-
  Specification that defines how to create code that follows a particular architecture.
description: >-
  Produce an architecture specification that instantiates domain and story scope into runnable code.
  Use when you need to specify how stories and domain objects map to files, classes, and tests across a stack.
---
# abd-architecture-specification

## Purpose

An **architecture specification** tells engineers exactly how domain concepts and stories become code in a chosen stack — which files, classes, interactions, and tests implement each entity, operation, and scenario. The specification is one artifact: documentation and working example code stay aligned; each mechanism is documented once and reused; later runs extend only what is missing.

---

## When to use

- A stack or project needs a **concrete mapping** from domain model and stories to production code and tests.
- You are starting a new architecture spec or **extending** an existing one with additional mechanisms.
- A kanban ticket names mechanisms in scope and you need to **assign** (reuse) or **create** (author) specification content.
- Example code must be **runnable** and validated against the architecture's own rules and scanners.

---

## Core concepts

### Specification directory

The deliverable is a **specification directory** — not a lone markdown file. Where it lives does not matter; the shape does: `architecture-specification.md`, `example/`, `rules/`, and `scanners/` together form one specification. Produce a new directory for a project, or **assign** an existing complete directory when the architecture is already specified.

### Mechanism

A **mechanism** is how the architecture handles a cross-cutting runtime concern — persistence, error handling, web client, app server, and the like. Each mechanism gets the same five-part shape in the doc (principles, file structure, participants, flow, walkthrough). Testing strategy lives in the top-level **Testing Architecture** section, not inside individual mechanisms.

### Assign vs create

**Assign** links existing specification directories to a **story map node** — system, epic, or sub-epic — via that node's **`architecture-spec`** field. **Create** when no assigned spec covers what that node's stories need.

A node may reference **more than one** spec. Typical reasons: a stack baseline (e.g. `specs/mern/`) plus a scoped companion (e.g. an increment or integration spec), or different stacks touching the same epic.

| Node level | Assign when | Create when |
| --- | --- | --- |
| **System** | Complete spec directory exists for this stack | Bootstrapping a new architecture |
| **Epic** | Spec(s) already document this epic's mechanisms and patterns | Epic needs a new spec directory or mechanisms not in any assigned spec |
| **Sub-epic** | Assigned spec(s) already cover this sub-epic's stories | Sub-epic needs new mechanism sections or example slices |

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

### Templates, example, and doc are peers

A complete spec directory has three peer folders:

- **`templates/`** — parameterized scaffold with `{{placeholders}}` for the full file layout (domain module, app roots, tests).
- **`example/`** — a filled instance of the templates with concrete domain values, plus `domain-spec.md` and `specification-by-example.md`.
- **`rules/`** and **`scanners/`** — validation against the architecture.

The doc (`architecture-specification.md`) references files in `example/`; `example/` is an instantiation of `templates/`. When either side changes, the others change in the same edit.

Full teaching — document skeleton, five-part shape, section organization, example modes, validation passes — lives in **`reference/concepts.md`**.

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

### 2. Ask — toy or real story?

If the answer is not already clear from context, ask the user:

> Should the runnable example use a **real story** from this project, or a **toy domain** (Calculator, Pet Store, Library, or agent's choice)?

Record the answer in a short **Example decisions** block at the top of the run output.

### 3. Create or update the specification

If a specification directory already exists for this architecture, update it — add missing mechanisms, fix drift. If none exists, create one.

Each spec directory has a **`templates/`** folder — a parameterized scaffold that is the peer of `example/`. The scaffold mirrors the example's file layout with `{{placeholders}}` instead of concrete domain values. When the spec already has templates (e.g. `specs/mern/templates/`), use them to generate the example; when bootstrapping a new spec, create the templates alongside the example.

**a. Example first.** Build the runnable example before writing the documentation:

1. **Domain spec** — produce `domain-spec.md` following `abd-domain-specification`.
2. **Spec by example** — produce `specification-by-example.md` following `abd-specification-by-example`.
3. **Tests** — write acceptance tests from the scenarios following `abd-acceptance-test-driven-development`.
4. **Code** — write the production code from the spec's `templates/` (replace placeholders with domain values), following `abd-clean-code` and the spec's own `rules/`.
5. **Run tests and fix** — tests must pass before moving on.
6. **Human review** — present the example code to the user for review. Wait for go-ahead.

**b. Documentation and validation artifacts.** On go-ahead from the user, create or update the rest of the specification directory:

1. **`architecture-specification.md`** — write from this skill's `templates/architecture-specification.md`. Every walkthrough step must reference a real file in `example/`.
2. **`templates/`** — parameterized scaffold that mirrors `example/` file-for-file. Every source file in `example/` must have a corresponding template file with `{{placeholders}}` replacing the concrete domain values. The scaffold includes the same folder structure: `domain-module/` (shared, server, client), `app-server/`, `app-client/`, `tests/`, root configs. See `specs/mern/templates/` for the shape.
3. **`rules/`** — one rule file per checkable concern, following the rule shape in this skill's own `rules/`.
4. **`scanners/`** — automated checks that enforce the rules against generated code.

Create all four from scratch for the architecture being specified.

### 4. Assign to story map

Link the specification directory to the relevant story map node(s) — system, epic, or sub-epic — via the node's `architecture-spec` field. A node can hold more than one spec path.

### 5. Validate

Follow **`execute-skill-using-skills-rules`** — two passes:

**A — Specification document:** Read every file in **`abd-architecture-specification/rules/`**; emit a per-rule PASS/FAIL verdict per `../agent-protocol.md`.

**B — Example code:** Read every file in the spec directory's own **`rules/`**; emit per-rule PASS/FAIL on the example. Then run scanners:

```bash
python foundational/skill-helpers/skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root <path-to-spec-directory> \
  --workspace <path-to-example-root> \
  --language typescript
```

Re-run until all scanners pass. Repeat both passes after any fix.

---

## Validate

**Goal:** Inspect what was built — read the docs and run the code as reviewers.

- **Per-rule verdict** — every file in **`rules/`** gets PASS or FAIL with reason; no silent skips.
- **Example decisions recorded** — Q1/Q2 answers appear before any generation.
- **Reuse honored** — story map node(s) for this run have `architecture-spec` updated with every assigned or created spec path; multiple specs per node when warranted; no duplicate mechanism sections inside assigned specs.
- **Specification directory complete** — doc, `example/`, `templates/`, `rules/`, and `scanners/` present for new specs; assigned specs cited, not recreated.
- **Templates mirror example** — every source file in `example/` has a corresponding parameterized file in `templates/` with `{{placeholders}}`; same folder structure, same file names (modulo domain substitution).
- **Doc template shape followed** — deliverable matches this skill's `templates/architecture-specification.md` skeleton; template instructions not copied into output.
- **Example artifact set aligned** — code, `specification-by-example.md`, and `domain-spec.md` use consistent concept names; tests pass; no stubs.
- **Example validation** — when example code was created or edited, architecture spec rules pass and `run_scanners.py` exits zero.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
