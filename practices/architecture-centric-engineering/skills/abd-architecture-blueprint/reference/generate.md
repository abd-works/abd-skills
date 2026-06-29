# Generate — abd-architecture-blueprint

## Read before generating

- **`reference/concepts.md`** — what a blueprint is, the platform diagram, modules vs mechanisms, how mechanisms are deepened from the outline (module interactions + platform detail), testing architecture, decision records, and what the blueprint does NOT contain.
- **`reference/examples.md`** — typical blueprint file tree and the shape of a good blueprint.
- **[`common/reference/record-all-architecture-violations.md`](../../../../../common/reference/record-all-architecture-violations.md)** — violation workflow (existing systems only). Read [`common/reference/decision-record.md`](../../../../../common/reference/decision-record.md) for the DR template and criteria.

Also read the project's **`architecture-outline.md`** to obtain the mechanism technology choices, NFR justifications, and guiding principles before starting. The blueprint deepens the outline — it does not re-state or re-decide what the outline recorded.

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

## Validate

After generation, also verify diagrams:

```powershell
.\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
```

Then run [`common/reference/rule-checklist.md`](../../../../../common/reference/rule-checklist.md) and practice [`validate-checklist.md`](../../../reference/validate-checklist.md).
