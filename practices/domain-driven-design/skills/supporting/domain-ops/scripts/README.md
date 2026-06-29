# domain-ops scripts

| Module | Purpose |
| --- | --- |
| `domain_map.py` | Typed in-memory model — `DomainMap`, `Module`, `KeyAbstraction`, `DomainClass` |
| `domain_graph_file.py` | Validate, load, save `domain-model.json` |
| `domain_graph_cli.py` | CLI entrypoint |
| `graph_filters.py` | Filter graph by module or class names |

**Schema:** `abd-domain-model/v1` — documented in `practices/domain-driven-design/references/domain-model-json.md`.

**Tests:** `../tests/` — run with `python3 -m pytest tests/ -v` from the skill root.
