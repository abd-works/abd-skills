# Diagram workflow — abd-architecture-specification

Shared commands: [`../../../reference/diagram-workflow.md`](../../../reference/diagram-workflow.md) (when using `arch-drawio.ps1` elsewhere in the engagement).

**This skill:** two diagrams alongside `architecture-specification.md`. Both must exist before the cell is marked done.

### `architecture-flow.drawio`

Start from `templates/architecture-flow.drawio`; replace every placeholder label with the actual layer or file name for this architecture. Plain boxes and lines only. No script — fill the template manually and save as `architecture-flow.drawio` next to `architecture-specification.md`.

### `architecture-specification-participants.drawio`

UML class diagram of the 14 domain module participants. Run from the spec directory:

```bash
python scripts/build_participants_diagram.py
```

Output: `architecture-specification-participants.drawio` in the same directory as the script.
