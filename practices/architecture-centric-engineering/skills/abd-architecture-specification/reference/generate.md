# Generate — abd-architecture-specification

Teaching reference for run modes, assign vs create, mechanism shape, and template conventions: **`reference/concepts.md`**.

## When to use

- A stack or project needs a **concrete mapping** from domain model and stories to production code and tests.
- You are starting a new architecture spec or **extending** an existing one with additional mechanisms.
- A kanban ticket names mechanisms in scope and you need to **assign** (reuse) or **create** (author) specification content.
- Template code must be **runnable** and validated against the architecture's own rules and scanners.

## Read before generating

Read all of these before doing anything else:

- **`reference/concepts.md`** and **`reference/examples.md`** — ideas and worked examples behind this skill.
- **`reference/example.ts`** — merged template module (all tiers in one file); catalog hero and shape reference for the runnable template slice.
- **`templates/architecture-specification.md`** — the document skeleton and placeholder vocabulary.
- **[`common/reference/record-all-architecture-violations.md`](../../../../../common/reference/record-all-architecture-violations.md)** — violation workflow (existing systems only). Read [`common/reference/decision-record.md`](../../../../../common/reference/decision-record.md) for the DR template and criteria.

## Output

**Primary output:** a specification directory (see **`reference/concepts.md`** — specification directory shape).

| This skill's template | What to produce |
| --- | --- |
| `templates/architecture-specification.md` | The specification document — mechanism sections, walkthroughs, diagrams. |
| `templates/architecture-flow.drawio` | Draw.io flow diagram — one box per layer/participant, simple boxes and lines. Place next to the spec doc. |
| `templates/architecture-specification-participants.drawio` | UML class diagram of domain module participants — all 14 classes, full edge set, built by `scripts/build_participants_diagram.py`. |

The spec directory's own `templates/` folder (e.g. `specs/mern/templates/`) holds the parameterized code scaffold — that is the spec's asset, not this skill's.

## Run modes

| Mode | Produces | When to use |
| --- | --- | --- |
| **document** | `architecture-specification.md` | Mechanism sections only; assigned spec with `template/` already exists |
| **template** | `template/` runnable code, spec `templates/` scaffold, `rules/`, `scanners/` | Code-first; documentation assigned separately |
| **both** (default) | Full specification directory | New spec or full refresh |

Respect the mode the user asks for (see **`reference/concepts.md` — Run modes**). Default to **both** when unspecified.

**Kanban defaults:** Exploration runs **document** mode; Specification runs **template** mode.

## Assign vs create

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

## Ask — mode and template domain

If not already clear from context or kanban ticket:

**Run mode** — if the user did not specify:

> Should this run produce **document** only, **template** only, or **both** (default)?

**Template domain** — when mode is **template** or **both**, if the answer is not already clear:

> Should the runnable template use a **real story** from this project, or a **toy domain** (Calculator, Pet Store, Library, or agent's choice)?

Record answers in a short **Run decisions** block at the top of the run output.

## Create or update the specification

If a specification directory already exists for this architecture, update it — add missing mechanisms, fix drift. If none exists, create one.

Each spec directory has a **`templates/`** folder — a parameterized scaffold that is the peer of `template/`. The scaffold mirrors the template's file layout with `{{placeholders}}` instead of concrete domain values. When the spec already has templates (e.g. `specs/mern/templates/`), use them to generate the template slice; when bootstrapping a new spec, create the templates alongside the template slice.

### Mode: template or both — template slice first

When mode is **template** or **both**, build the runnable template before writing documentation:

1. **Domain spec** — produce `template/domain-spec.md` following `abd-domain-specification`.
2. **Spec by example** — produce `template/specification-by-example.md` following `abd-story-specification`.
3. **Tests** — write acceptance tests from the scenarios following `abd-story-acceptance-test`.
4. **Code** — write the production code from the spec's `templates/` (replace placeholders with domain values), following `abd-clean-code` and the spec's own `rules/`.
5. **Run tests and fix** — tests must pass before moving on.
6. **Human review** — when mode is **both**, present the template code to the user for review. Wait for go-ahead before the document pass. When mode is **template** only, present for review at the end of this pass.

### Mode: template or both — scaffold and validation artifacts

After template slice is ready (and user go-ahead when mode is **both**):

1. **`templates/`** — parameterized scaffold that mirrors `template/` file-for-file. Every source file in `template/` must have a corresponding template file with `{{placeholders}}` replacing the concrete domain values. The scaffold includes the same folder structure: `domain-module/` (shared, server, client), `app-server/`, `app-client/`, `tests/`, root configs. See `specs/mern/templates/` for the shape.
2. **`rules/`** — one rule file per checkable concern, following the rule shape in this skill's own `rules/`.
3. **`scanners/`** — automated checks that enforce the rules against generated code.

Create all three from scratch when bootstrapping a new architecture spec. Skip recreation when assigning an existing complete spec.

### Mode: document or both — specification document

When mode is **document** or **both**:

1. **`architecture-specification.md`** — write from this skill's `templates/architecture-specification.md`. Every walkthrough step must reference a real file in `template/` when that folder exists; otherwise use parameterized pattern comments and point at `templates/`.

2. **`architecture-flow.drawio`** — see [`diagram-workflow.md`](diagram-workflow.md). Place the file next to `architecture-specification.md` and reference it with `> See [architecture-flow.drawio](./architecture-flow.drawio)` in the Architecture Flow section.

3. **Grill Me section** — add a `## Grill Me — Map a Story to a Mechanism` section to `architecture-specification.md`, placed immediately before `## Rules`. This section is **architecture-specific**: it must reflect the actual mechanisms and patterns defined in this spec, not a generic list. Its purpose is to help an implementer — or an agent — pick the right mechanism and adapter pattern for any new story without reading the whole document.

   **Shape of the Grill Me section:**
   - **Decision questions** — a numbered sequence: What triggers the story? What does it output? Does the domain concept present itself on this surface, or does it own lifecycle objects? Does state need to persist? Any async / streaming concerns?
   - **Each question** maps answers to named mechanisms from this spec (not invented names). Use the mechanism heading as written — `## Mechanism: Commands`, `## Mechanism: Status Bar`, etc.
   - **Extend-or-wrap guidance** — where the spec distinguishes extend (IS-A domain concept + presentation shape) from wrap (HAS-A domain dependency + lifecycle objects), include a question that drives the decision with examples from this spec's `template/`.
   - **Do not repeat** mechanism prose. The Grill Me section points; the mechanism sections explain.

When mode is **document** only, do not create or edit files under `template/` unless the user explicitly asks to refresh template code in the same run.

When mode is **template** only, skip `architecture-specification.md` unless the user explicitly asks for document work in the same run.

### Mechanism guidance

A **mechanism** is how the architecture handles a cross-cutting runtime concern — persistence, error handling, web client, app server, and the like. Each mechanism gets the same five-part shape in the doc (principles, file structure, participants, flow, walkthrough). Testing strategy lives in the top-level **Testing Architecture** section, not inside individual mechanisms.

See **`reference/concepts.md`** — The five-part shape, section organization, and template domain modes.

### Record violations (existing systems only)

If you are specifying an existing system (document or both mode), follow [`common/reference/record-all-architecture-violations.md`](../../../../../common/reference/record-all-architecture-violations.md) after completing the specification document. Collect all violations observed across mechanism sections, present the table, ask fix or defer, and write a Deferral ADR for every deferred item. Append the violation resolution summary to `architecture-specification.md`.

## Assign to story map

Link the specification directory to the relevant story map node(s) — system, epic, or sub-epic — via the node's `architecture-spec` field. A node can hold more than one spec path.

## Validate

Follow [`common/reference/rule-checklist.md`](../../../../../common/reference/rule-checklist.md) and practice [`validate-checklist.md`](../../../reference/validate-checklist.md). Run only the passes that match the mode:

**A — Specification document** (modes **document** and **both**): Read every file in **`abd-architecture-specification/rules/`**; emit a per-rule PASS/FAIL verdict.

**B — Template code** (modes **template** and **both**): Read every file in the spec directory's own **`rules/`**; emit per-rule PASS/FAIL on the template slice. Then run scanners:

```bash
python skills/common/scripts/run_scanners.py \
  --skill-root <path-to-spec-directory> \
  --workspace <path-to-template-root> \
  --language typescript
```

Re-run until all scanners pass. Repeat applicable passes after any fix.
