# Rule: Every diagram ships paired markdown reference and drawio source

Every diagram referenced from `architecture-blueprint.md` must have a matching `.drawio` source file on disk under `docs/architecture/diagrams/`. The markdown is what readers see; the `.drawio` is what the team edits. Without the source file, the next person who needs to update the diagram has to redraw it from scratch, and the architecture document drifts from the running system within a release. The two blueprint-level diagrams this skill ships templates for are `entity-relationships.drawio` (the data model overview in section 4) and `component-overview.drawio` (the component-per-system overview that complements section 2). The CLI helper at `scripts/arch-drawio.ps1` initialises templates, exports PNGs, and verifies the pairs. Failing means a diagram appears in the markdown as a PNG with no `.drawio` source, or a `.drawio` source exists for a diagram that the markdown never references.

## DO

- Place every blueprint-level diagram source as `docs/architecture/diagrams/<name>.drawio` and reference either the rendered `<name>.png` or the `<name>.drawio` file directly from the markdown.

  **Example (pass):** `architecture-blueprint.md` section 4 contains `![Entity relationships](./diagrams/entity-relationships.png)`. The file `docs/architecture/diagrams/entity-relationships.drawio` exists. Running `.\scripts\arch-drawio.ps1 verify` prints `[verify] OK   diagrams/entity-relationships.png -> entity-relationships.drawio exists`.

- Use mermaid inside the blueprint markdown only for **small, walkthrough-style figures** that fit on one screen and benefit from being in-page (e.g. a tiny sequence sketch in a component description). The two **load-bearing** blueprint diagrams (entity-relationships and component-overview) need drawio sources because architects and reviewers edit them outside the codebase.

  **Example (pass):** Section 4 uses a drawio-sourced PNG for the entity overview; an inline mermaid `classDiagram` appears in a component description showing a single class — fine, that one does not need a paired drawio.

- Run `.\scripts\arch-drawio.ps1 init -ProjectRoot <path>` to seed templates without overwriting existing diagrams (unless `-Force`).

  **Example (pass):** Project gets two new `.drawio` files in `diagrams/`; existing diagrams are not touched.

## DO NOT

- Embed a screenshot or PNG of an entity diagram with no `.drawio` source.

  **Example (fail):** `architecture-blueprint.md` shows `./diagrams/entity-relationships.png` but `diagrams/` has no matching `.drawio`. The diagram becomes write-only.

- Use only inline mermaid for the entity overview when the blueprint promises a drawio-sourced diagram in its template.

  **Example (fail):** Section 4 has a 30-line mermaid `classDiagram` and no drawio source. Once the entity model grows past 5 aggregates, the mermaid block becomes unreadable in source view and the team cannot edit it visually.

- Leave orphan `.drawio` files in `diagrams/` that the blueprint never references.

  **Example (fail):** `diagrams/component-overview-old.drawio` and `diagrams/component-overview-v2.drawio` both exist; the blueprint links only to the v2 PNG. Delete the orphan or update the markdown to make its purpose clear.

**Source:** Practice-skill authoring convention (abd-architecture-blueprint); paired markdown + drawio keeps load-bearing diagrams editable.
