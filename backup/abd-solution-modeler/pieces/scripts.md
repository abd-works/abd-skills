## Scripts

```bash
python scripts/pipeline.py generate <phase>                  # Layer 1: phase spec + rules
python scripts/pipeline.py generate <phase> render-diagram   # Layer 1 + DrawIO
python scripts/pipeline.py scan <phase>                      # Layer 2: run scanners
python scripts/pipeline.py validate <phase>                  # Layer 3: rules + checklist for AI pass
python scripts/pipeline.py drawio [<phase>]                  # DrawIO from domain model
python scripts/pipeline.py pipeline                          # Run all phases (use --stop <phase>)
```

**Assemble AGENTS.md from pieces:**

```bash
python scripts/assemble_agents.py
```
