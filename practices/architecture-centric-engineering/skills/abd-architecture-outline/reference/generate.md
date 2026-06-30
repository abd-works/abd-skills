# Generate — abd-architecture-outline

## Read before generating

- **`reference/concepts.md`** — outline scope, system context diagram, extended system-context scope (functions + tech + protocols), mechanisms catalogue, guiding principles, major systems catalogue, decision records.
- **`reference/system-context.md`** — deeper guidance on the system context diagram.
- **[`common/reference/record-all-architecture-violations.md`](../../../../../common/reference/record-all-architecture-violations.md)** — violation workflow (existing systems only): surface pattern deviations, orphan concerns, and missing mechanisms; stop and inform the user; ask 2a/2b/2c per violation; launch a non-blocking sub-agent to write DRs and downstream artefacts. Read [`common/reference/decision-record.md`](../../../../../common/reference/decision-record.md) for the DR template and criteria.

### Scan existing distributed context (existing systems)

If the target project already contains `architecture-context.md` files (per-folder, distributed alongside the code — see [`architecture-context-model.md` § 1](../../../reference/architecture-context-model.md#1-centralized-documents-and-distributed-context-files)), scan them before authoring the outline. Pick up signals at outline fidelity:

- **Mechanism mentions** — every named mechanism the context files reference should appear in the outline's mechanisms catalogue (or be flagged as a missing mechanism per the violation workflow).
- **Technology choices** — when a context file already names the persistence engine, HTTP stack, identity provider, etc., corroborate it against the outline's tech-stack table; conflicts are violations.
- **System / boundary signals** — references to external systems in context files should match the system-context elements file.

Treat the per-folder files as a contributing source of truth, not as authority over the outline. Where context files and the outline disagree, surface the conflict via the violation workflow rather than silently overwriting either side.

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

## Handoff to downstream skills

Once the outline is on disk, the names and decisions captured here become the **top of the vocabulary chain** for the blueprint, the architecture specification, and the code skill.

See [`architecture-context-model.md`](../../../reference/architecture-context-model.md) — in particular [§ 3 The vocabulary chain](../../../reference/architecture-context-model.md#3-the-vocabulary-chain) and [§ 7 Skill-level handoff summary](../../../reference/architecture-context-model.md#7-skill-level-handoff-summary) — for the full handoff contract. Downstream skills must not rename or invent mechanisms / systems; if the blueprint or spec discovers a missing or wrongly named mechanism, this outline (and its ADR) is updated first, then propagated.
