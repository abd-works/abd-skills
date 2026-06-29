# Diagram workflow — abd-domain-specification

Shared CLI: [`../../../reference/diagram-workflow.md`](../../../reference/diagram-workflow.md)

Produces `<deliverables-folder>/domain-specification.drawio` from `domain-specification.md`. Must exist before the cell is marked done.

If a `domain-model.drawio` already exists (from `abd-domain-model`), pass it as `--base-diagram` so layout is preserved and only updated in place:

```bash
# With existing domain model diagram (preserves layout):
python scripts/drawio_domain_cli.py \
  <deliverables-folder>/domain-specification.md \
  --base-diagram <deliverables-folder>/domain-model.drawio \
  --output <deliverables-folder>/domain-specification.drawio

# Without (fresh layout):
python scripts/drawio_domain_cli.py \
  <deliverables-folder>/domain-specification.md \
  --output <deliverables-folder>/domain-specification.drawio
```

Run once after `domain-specification.md` is written. Re-run the same command to regenerate — markdown is the source of truth.
