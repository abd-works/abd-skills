# Generate — abd-architecture-blueprint

## Read before generating

- **`reference/concepts.md`** — what a blueprint is, the platform diagram, modules vs mechanisms, how mechanisms are deepened from the outline (module interactions + platform detail), testing architecture, decision records, and what the blueprint does NOT contain.
- **`reference/examples.md`** — typical blueprint file tree and the shape of a good blueprint.
- **[`common/reference/record-all-architecture-violations.md`](../../../../../common/reference/record-all-architecture-violations.md)** — violation workflow (existing systems only). Read [`common/reference/decision-record.md`](../../../../../common/reference/decision-record.md) for the DR template and criteria.

Also read the project's **`architecture-outline.md`** to obtain the mechanism technology choices, NFR justifications, and guiding principles before starting. The blueprint deepens the outline — it does not re-state or re-decide what the outline recorded.

### Scan existing distributed context (existing systems)

If the target project already contains `architecture-context.md` files (per-folder, distributed alongside the code — see [`architecture-context-model.md` § 1](../../../reference/architecture-context-model.md#1-centralized-documents-and-distributed-context-files)), scan them before authoring the blueprint. Pick up signals at blueprint fidelity:

- **Module signals** — context files often name the module that owns a folder; gather these to validate the modules section.
- **Code-shape descriptions** — existing mechanism-tier files describe canonical patterns and rules; cross-check against the code-shape constraints you intend to write for each mechanism.
- **Mechanism-modules hints** — when a folder's context file describes both a mechanism and a public API surface, that folder is a candidate mechanism-module.
- **Inter-module dependencies** — `Across the Codebase` / consumer lists in package-tier files surface real dependencies between modules.

Treat the per-folder files as a contributing source of truth, not as authority over the blueprint. Where context files and the intended blueprint disagree, surface the conflict via the violation workflow rather than silently overwriting either side.

## Output

Generate from all templates in `templates/`, preserving subfolder structure. Write to `docs/architecture/`. Add a `<name>-` prefix to `architecture-blueprint.md` only when disambiguation is needed.

## Step 2a — Platform element inventory

| Template | Output file |
| --- | --- |
| `templates/platform-architecture-elements.md` | `docs/architecture/platform-architecture-elements.md` |

Fill every section with real names and 1–2 sentence descriptions; no placeholder tokens (`{…}`) should remain.

## Step 2b — Blueprint document and ADRs

| Template | What to produce |
| --- | --- |
| `templates/architecture-blueprint.md` | The blueprint document — scope, platform runtime (diagram + runtime-components table), mechanisms (technology + how modules implement each), architecture flow diagram(s), modules (mechanism-modules + domain modules), testing architecture, and ADR list. |
| `templates/decisions/decision-record.md` | One ADR per blueprint-level decision (module boundaries, test-tier vocabulary, data ownership patterns) under `docs/architecture/decisions/`. Number continues from the outline. |

### Mechanism guidance

Mechanisms go first — they define the code shapes modules must adopt. For each mechanism:

- Technology and platform (brief)
- 1–2 prose paragraphs: how modules implement or extend the mechanism (the code shape it requires)
- Note if the mechanism also has a concrete module surface (e.g. Security — Identity module)

### Module guidance

Modules come after mechanisms. Two kinds:

- **Mechanism-modules** — mechanisms that also have a concrete implementation surface; describe their functional behaviour and surface API in 1–2 paragraphs
- **Domain modules** — 1–2 sentence business scope; mechanisms used (list, using *common set* shorthand + module-specific extras); dependencies on other modules

### Diagram workflow

See [`diagram-workflow.md`](diagram-workflow.md). Fill `platform-architecture.drawio`, `module-overview.drawio`, and `architecture-flow.drawio` from the element-inventory file and module subsections. Fill `testing-flow.drawio` from the testing architecture tiers.

**Quality bar:** Platform element file fully described. Mechanisms described in prose (code shape each module must adopt). Mechanism-modules described with functional surface. Domain modules described in 1–2 sentences + mechanisms + dependencies. Module diagram has legend for universal mechanisms.

## Step 2c — Record violations (existing systems only)

If you are documenting an existing system, follow [`common/reference/record-all-architecture-violations.md`](../../../../../common/reference/record-all-architecture-violations.md) after completing steps 2a and 2b. Collect all violations found across mechanism and module descriptions, present the table, ask fix or defer, and write a Deferral ADR for every deferred item. Append the violation resolution summary to the blueprint document.

## Step 3 — Scaffold (opt-in, mode: scaffold only)

**Skip this step entirely when running in default mode (`mode: blueprint`).** Run it only when the invocation specifies `mode: scaffold`. Concepts and boundaries: [`concepts.md` § Optional: scaffold mode](./concepts.md#optional-scaffold-mode). Rule: [`../rules/scaffold-stubs-are-blueprint-only.md`](../rules/scaffold-stubs-are-blueprint-only.md).

### Step 3a — Pre-flight checks

Before writing anything to disk:

1. Confirm the blueprint document (Step 2b) is complete and validated.
2. Resolve `<src-root>` — the project's source root (`src/`, `app/`, `lib/`, `packages/<name>/src/`). Ask the user if ambiguous; never guess.
3. Read existing `architecture-context.md` files under `<src-root>` and tabulate which folders already have stubs. The pre-flight table reports for each module/mechanism-host folder: folder exists? context file exists? blueprint-fidelity content present and matching?
4. Surface any conflict (existing blueprint-fidelity content disagreeing with the current blueprint document) via the violation workflow before proceeding — do not silently overwrite.

### Step 3b — Folder creation

For each module named in the blueprint's Modules section and each mechanism-host folder named in the Mechanisms section:

- Create the folder under `<src-root>` if it does not exist.
- Never delete or rename existing folders. Surface a conflict instead.

### Step 3c — Stub seeding

For each created (or pre-existing) folder:

| Folder type | Template | Pre-filled blueprint-fidelity content |
|---|---|---|
| Module folder | [`../templates/scaffold/module-package-context-stub.md`](../templates/scaffold/module-package-context-stub.md) | Owning module, mechanisms used, test tier, dependencies |
| Mechanism-host folder | [`../templates/scaffold/mechanism-context-stub.md`](../templates/scaffold/mechanism-context-stub.md) | Mechanism name, code-shape paragraph, technology + ADR link |

Write each stub as `<folder>/architecture-context.md`. Leave spec-fidelity slots (File Structure, Participants, Class Specification, Rules, Canonical Pattern) marked `<!-- spec to fill -->`.

If `architecture-context.md` already exists in a target folder, **do not overwrite**. Append any newly added blueprint-fidelity content (a new mechanism, a changed dependency, a flipped test tier) under a "Blueprint updates" section dated with the run timestamp. Surface a conflict if existing content disagrees with the current blueprint.

### Step 3d — Reachability update

After seeding, update (or create) the central spec hub at `docs/architecture/specification/architecture-specification.md` so every newly seeded `architecture-context.md` is reachable. If the central spec does not exist yet, write only the navigation entries — leave Where-to-Start, Source Layout, and other spec-fidelity sections empty for `abd-architecture-specification` to fill.

### Step 3e — Report

Produce a run report listing:

- Folders created
- Stubs seeded
- Stubs skipped (already exist)
- Stubs updated (blueprint-fidelity content appended)
- Conflicts surfaced
- Central-spec entries added

**Quality bar:** Every module and mechanism-host folder in the blueprint has a corresponding `architecture-context.md`. Every seeded stub uses blueprint vocabulary verbatim. No spec-fidelity content invented at scaffold time. Run is idempotent — re-running produces the same result modulo new blueprint additions.

## Validate

After generation, also verify diagrams:

```powershell
.\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
```

Then run [`common/reference/rule-checklist.md`](../../../../../common/reference/rule-checklist.md) and practice [`validate-checklist.md`](../../../reference/validate-checklist.md).
