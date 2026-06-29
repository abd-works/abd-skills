# Domain-Driven Design — Diagram Workflow (shared)

Domain class diagrams render from markdown via **`drawio_domain_cli.py`**. Skills that produce diagrams ship `reference/diagram-workflow.md` with output paths; this file owns the shared CLI.

**Prerequisites:** The source markdown (`domain-model.md` or `domain-specification.md`) must exist. The `.drawio` file must exist on disk before the CDD cell is marked done.

**CLI:** `scripts/drawio_domain_cli.py` relative to the skill package (or project copy).

---

## Fresh layout

```bash
python scripts/drawio_domain_cli.py \
  <deliverables-folder>/domain-model.md \
  --output <deliverables-folder>/domain-model.drawio
```

| Skill | Source markdown | Default output |
| --- | --- | --- |
| `abd-domain-model` | `domain-model.md` | `domain-model.drawio` (one tab per KA) |
| `abd-domain-specification` | `domain-specification.md` | `domain-specification.drawio` |

---

## Preserve layout from domain model

When `domain-model.drawio` already exists:

```bash
python scripts/drawio_domain_cli.py \
  <deliverables-folder>/domain-specification.md \
  --base-diagram <deliverables-folder>/domain-model.drawio \
  --output <deliverables-folder>/domain-specification.drawio
```

Re-run the same command to regenerate — markdown is the source of truth.
