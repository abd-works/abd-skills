# Diagram workflow — abd-domain-model

Shared CLI: [`../../../reference/diagram-workflow.md`](../../../reference/diagram-workflow.md)

Produces `<deliverables-folder>/domain-model.drawio` (one tab per KA) from `domain-model.md`. Must exist before the cell is marked done.

```bash
python scripts/drawio_domain_cli.py \
  <deliverables-folder>/domain-model.md \
  --output <deliverables-folder>/domain-model.drawio
```

Run once after `domain-model.md` is written. To regenerate, re-run the same command — the markdown is the source of truth.
