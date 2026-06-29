# Generate — drawio-domain-sync

Follow every file in `rules/`. Read [`reference/concepts.md`](concepts.md) and [`reference/diagram-workflow.md`](diagram-workflow.md) before any CLI work.

## Per-KA tabs (default)

**Unless the user explicitly asks for a full single-page diagram, produce per-KA tabs.**

**Per-KA tab rules:**

1. **One tab per KA** — Each Key Abstraction gets its own page/tab in the `.drawio` file.
2. **Boundary classes (directly connected only)** — On each KA's tab, include classes from other KAs that are *directly connected* via an edge to a class in this KA. Dashed borders and reduced opacity signal context, not focus.
3. **Supertypes only, not subtypes** — A subtype crossing KA boundaries pulls in its supertype as a boundary class. A supertype does NOT pull in subtypes from other KAs.
4. **Exact layout from source** — Use the same positions as the source diagram for classes within the KA. Reposition boundary classes closer to the KA cluster they connect to.
5. **Edge labels preserved** — Role names on edges carry through to per-KA tabs.
6. **Optional overview tab** — Include an "All KAs (Overview)" tab as the first page when helpful.

**Workflow:**

1. **Identify the source file** — locate domain specification, domain model, or domain language markdown. Prefer highest fidelity available (domain specification > domain model > domain language). If a domain model diagram already exists, use `--base-diagram` to copy layout and update cells in place.
2. **Render all KAs** — Build the multi-tab file per the rules above.
3. **Audit** — Run `audit_diagram_report()` on each tab. Fix overlaps.
4. **Report** — Tell the user the diagram is ready for review.

**CLI (from skill `scripts/`):**

```bash
# Default: per-KA tabs
python scripts/drawio_domain_cli.py <source.md> --output <file.drawio>

# Full single-page (only when explicitly requested):
python scripts/drawio_domain_cli.py <source.md> --output <file.drawio> --full

# From a base diagram (domain spec inherits domain model layout):
python scripts/drawio_domain_cli.py <spec.md> --base-diagram <existing.drawio> --output <spec-diagram.drawio>

# Inspect:
python scripts/drawio_domain_cli.py inspect <file.drawio>

# Sync back:
python scripts/drawio_class_cli.py sync-to-model <file.drawio> --page "<KA Name>" --model <source-file>
```

**`--base-diagram`:** When rendering domain specification and a domain model diagram exists, pass `--base-diagram <model-diagram.drawio>`. Copies layout, updates cells with specification-level detail, adds new classes near related classes, redraws edges from spec relationships.

**Sync back (diagram → source):** Run `sync-to-model` to surface the diff; review with the user; apply confirmed changes to the source markdown.

## Full single-page (only when requested)

Use only when the user explicitly asks ("full diagram", "single page", `--full`).

1. For each Key Abstraction, init a page, plan layout (bases above derived), add imported ancestors, add local classes with rows/collaborators per source fidelity, add edges, inspect for overlaps, verify sync.
2. Persist build scripts when full renders produce bespoke Python scripts — see `reference/concepts.md` § Persisting module build scripts.
