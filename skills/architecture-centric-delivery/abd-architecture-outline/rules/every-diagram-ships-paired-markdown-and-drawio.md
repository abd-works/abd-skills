# Rule: Every diagram ships paired markdown reference and drawio source

Every diagram referenced from `architecture-outline.md` must have a matching `.drawio` source file on disk under `docs/architecture/diagrams/`. The markdown is what readers see; the `.drawio` is what the team edits. Without the source file, the next person who needs to update the diagram has to redraw it from scratch, and the architecture document drifts from the running system within a release. The canonical filenames for the four outline diagrams are `platform-architecture.drawio`, `layered-architecture.drawio`, `system-context.drawio`, and `deployment-architecture.drawio`. The CLI helper at `scripts/arch-drawio.ps1` initialises the templates, exports the PNGs, and verifies the pairs. Failing means a diagram appears in the markdown as a PNG with no `.drawio` source, a `.drawio` source exists for a diagram that the markdown never references, or the four canonical diagrams are not all present.

## DO

- Place every diagram source as `docs/architecture/diagrams/<name>.drawio` and reference either the rendered `<name>.png` or the `<name>.drawio` file directly from the markdown.

  **Example (pass):** `architecture-outline.md` contains `![Platform diagram](./diagrams/platform-architecture.png)`. The file `docs/architecture/diagrams/platform-architecture.drawio` exists. Running `.\scripts\arch-drawio.ps1 verify` prints `[verify] OK   diagrams/platform-architecture.png -> platform-architecture.drawio exists`.

- Use the canonical filenames for the four outline diagrams so the verify command can confirm all four are present.

  **Example (pass):** `platform-architecture.drawio`, `layered-architecture.drawio`, `system-context.drawio`, `deployment-architecture.drawio` all exist; verify prints PASS.

- Initialise a fresh project's diagrams folder by running `.\scripts\arch-drawio.ps1 init -ProjectRoot <path>` from this skill, which copies the four templates without overwriting existing diagrams (unless `-Force`).

  **Example (pass):** A new project runs `init`, opens each `.drawio` in draw.io Desktop, fills in the `{Placeholder}` text, runs `export`, then `verify` returns PASS.

## DO NOT

- Embed a screenshot or PNG in the markdown with no matching `.drawio` source on disk.

  **Example (fail):** `architecture-outline.md` references `./diagrams/platform-architecture.png` but `docs/architecture/diagrams/` contains only the PNG — no `.drawio`. The diagram becomes write-only; the next update redraws from scratch.

- Inline a mermaid diagram for the four canonical diagrams in place of a `.drawio` source.

  **Example (fail):** Section 1 of the outline has a fenced ` ```mermaid ` block for the platform diagram. Mermaid is fine for small ad-hoc figures inside mechanism walkthroughs, but the four outline-level diagrams need editable drawio sources so non-developer reviewers (architects, ops) can open and edit them in draw.io Desktop.

- Rename the canonical diagrams so the verify step cannot find them.

  **Example (fail):** A team renames `system-context.drawio` to `context-c4.drawio`. The verify step reports `MISS expected 'system-context' diagram not referenced in outline`. Either keep the canonical name, or update the skill convention and the CLI.

- Ship a `.drawio` source that the markdown never references.

  **Example (fail):** `diagrams/` contains five `.drawio` files; the outline only links to three. The two orphans are documentation rot — either reference them from the outline or delete them.

**Source:** Practice-skill authoring convention (abd-architecture-outline); paired markdown + drawio is what makes the outline maintainable past its first release.
