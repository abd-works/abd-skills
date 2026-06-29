# ux-ops scripts

| Module | Purpose |
| --- | --- |
| `ux_map.py` | Typed in-memory model — `UxGraph`, `Flow`, `Screen`, `Region` |
| `ux_graph_file.py` | Validate, load, save `ux-graph.json` |
| `ux_graph_cli.py` | CLI entrypoint |
| `graph_filters.py` | Filter graph by flow or screen names |

**Schema:** `abd-ux-graph/v1` — documented in `practices/user-experience-design/references/ux-graph-json.md`.

**Tests:** `../tests/` — run with `python3 -m pytest tests/ -v` from the skill root.
