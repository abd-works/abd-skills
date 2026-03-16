## DrawIO Diagram Rendering

DrawIO class diagrams are generated from domain model `.md` files in `generated/domain/`.

- **Mandatory** — auto-generated after `final_domain_model`
- **Optional** — append `render-diagram` to any `generate` command

```bash
python scripts/pipeline.py generate final_domain_model render-diagram
python scripts/pipeline.py generate structural_model render-diagram
python scripts/pipeline.py drawio                        # standalone, from latest domain model
python scripts/pipeline.py drawio final_domain_model # standalone, from specific phase
```

Output: `generated/domain/<phase>.drawio` (alongside the source `.md` file).
