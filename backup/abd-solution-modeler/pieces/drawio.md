## DrawIO Diagram Rendering

DrawIO class diagrams are generated from domain model `.md` files in `generated/domain/`.

- **Mandatory** — auto-generated after `finalize`
- **Optional** — append `render-diagram` to any `generate` command

```bash
python scripts/pipeline.py generate finalize render-diagram
python scripts/pipeline.py generate structure render-diagram
python scripts/pipeline.py drawio  # standalone, from latest solution model
```

Output: `generated/domain/<phase>.drawio` (alongside the source `.md` file).
