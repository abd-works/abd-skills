# Rule: The system context diagram ships a paired element-inventory markdown and drawio source

The system context diagram referenced from `architecture-outline.md` must have **two** matching files on disk under `docs/architecture/diagrams/`: a `system-context-elements.md` element-inventory file and a `system-context.drawio` editable source. The outline links both from the diagram section. Without the element file the diagram has no documented inventory; without the `.drawio` source the next person who updates the diagram has to redraw from scratch.

| Diagram | Element file | Draw.io source |
|---|---|---|
| System Context | `system-context-elements.md` | `system-context.drawio` |

Failing means the diagram appears in the outline with no `.drawio` source, no element file, or both; a `.drawio` source exists that the outline never references; the canonical filename is not used; or `arch-drawio.ps1 verify` does not print PASS.

## DO

- For the diagram section in the outline, both the `.drawio` source link and the element-inventory link are present.

  **Example (pass):** The System Context section of `architecture-outline.md` contains:
  ```markdown
  > Source: [diagrams/system-context.drawio](./diagrams/system-context.drawio)
  > Element inventory: [diagrams/system-context-elements.md](./diagrams/system-context-elements.md)
  ```
  Both files exist on disk under `docs/architecture/diagrams/`.

- Both files exist under `docs/architecture/diagrams/` using the canonical filenames; `arch-drawio.ps1 verify` prints PASS.

  **Example (pass):** `ls docs/architecture/diagrams/` shows `system-context-elements.md` and `system-context.drawio` with exactly the canonical names.

- The diagram referenced in the outline has exactly one matching `.drawio` source and exactly one matching `-elements.md` — no orphans in either direction.

  **Example (pass):** `diagrams/` contains `system-context.drawio`; the outline has one diagram section; the section links its matching source and element files.

## DO NOT

- Embed a PNG in the outline with no matching `.drawio` source on disk.

  **Example (fail):** `architecture-outline.md` has `![System Context](./diagrams/system-context.png)` but `docs/architecture/diagrams/` has no `system-context.drawio`. The diagram is write-only from this point forward.

- Reference the diagram in the outline with no matching `-elements.md` on disk.

  **Example (fail):** The System Context section links `system-context.drawio` and `system-context.png` but `docs/architecture/diagrams/system-context-elements.md` does not exist. The diagram has no auditable element inventory.

- Use a mermaid block in place of the canonical drawio diagram.

  **Example (fail):** Section 1 of the outline is a fenced ` ```mermaid ` block. Mermaid has no editable source on disk and cannot be opened in draw.io Desktop; the outline-level diagram requires a `.drawio` source.

- Ship a `.drawio` source that the outline never references, or leave an `-elements.md` with no matching `.drawio`.

  **Example (fail):** `diagrams/` contains `layered-architecture.drawio` but no section of the outline references it. Orphaned sources are documentation rot.

- Use a non-canonical filename for the system context diagram.

  **Example (fail):** A team saves the system context diagram as `context-c4.drawio` instead of `system-context.drawio`. The verify command reports a miss; downstream tooling and the outline template both expect the canonical name.

**Source:** Practice-skill authoring convention (abd-architecture-outline); the diagram must be auditable (element file) and editable (drawio source) — the PNG alone is neither.
