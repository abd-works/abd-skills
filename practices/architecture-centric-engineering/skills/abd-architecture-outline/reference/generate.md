# Generate — abd-architecture-outline

## Read before generating

- **`reference/concepts.md`** — outline scope, system context diagram, extended system-context scope (functions + tech + protocols), mechanisms catalogue, guiding principles, major systems catalogue, decision records.
- **`reference/system-context.md`** — deeper guidance on the system context diagram.
- **[`common/reference/record-all-architecture-violations.md`](../../../../../common/reference/record-all-architecture-violations.md)** — violation workflow (existing systems only): surface pattern deviations, orphan concerns, and missing mechanisms; stop and inform the user; ask 2a/2b/2c per violation; launch a non-blocking sub-agent to write DRs and downstream artefacts. Read [`common/reference/decision-record.md`](../../../../../common/reference/decision-record.md) for the DR template and criteria.

## Output

Generate from all templates in `templates/`, preserving subfolder structure. Write to `docs/architecture/diagrams/`. Add a `<name>-` prefix to `architecture-outline.md` only when disambiguation is needed.

## Step 2a — Element inventory first

Using `templates/system-context-elements.md` as the starting structure, fill in every section with real system names and 1–2 sentence descriptions. No placeholder tokens (`{…}`) should remain.

For the **system-context** file: add **Major functions** and **Platform technology** (app stack, persistence, tools/libs) to every owned system entry; add **Protocol** to every relationship entry.

Complete the element file before proceeding to step 2b.

| Template | Output file |
| --- | --- |
| `templates/system-context-elements.md` | `docs/architecture/diagrams/system-context-elements.md` |

## Step 2b — Outline document and ADRs

Only after the element file is complete:

| Template | What to produce |
| --- | --- |
| `templates/architecture-outline.md` | The outline document — a System Context section describing each owned system, an Architecture Mechanisms section with tech-choice + NFR justification per mechanism, guiding principles, tech stack table, major systems table, and ADR list. |
| `templates/decisions/decision-record.md` | One ADR file per outline-level decision (platform, architectural style, each mechanism technology choice) under `docs/architecture/decisions/`. |

### Mechanism guidance

Cover all eight standard mechanisms (Security, Error Handling & Resilience, Logging & Observability, Validation, Configuration & Secrets, Caching, Persistence, Communication). Then identify any context-specific or bespoke mechanisms this system requires that the standard set does not cover and add them as additional subsections. Do not leave any mechanism empty or placeholder; derive real choices from the project context.

### Diagram workflow

See [`diagram-workflow.md`](diagram-workflow.md). Fill placeholders in `system-context.drawio` using the element-inventory file as the source of truth. Reference the PNG and link the element file from the outline markdown.

**Quality bar:** Element-inventory file present and fully described (no placeholder tokens). System context element file includes functions + platform tech per system and protocol per relationship. Diagram present and matching its element file, accompanied by a caption of three sentences or fewer. Every mechanism has a named technology choice and NFR justification. ADRs on disk for all mechanism choices and platform decisions.

## Step 2c — Record violations (existing systems only)

If you are documenting an existing system, follow [`common/reference/record-all-architecture-violations.md`](../../../../../common/reference/record-all-architecture-violations.md) after completing steps 2a and 2b. Collect all violations, present the table, ask fix or defer, and write a Deferral ADR for every deferred item. Append the violation resolution summary to the outline document.

## Validate

After generation, also verify diagram:

```powershell
.\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
```

Then run [`common/reference/rule-checklist.md`](../../../../../common/reference/rule-checklist.md) and practice [`validate-checklist.md`](../../../reference/validate-checklist.md).
