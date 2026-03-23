# Process — ace-foo

**Pipeline:** [Workspace and config](phases/workspace-and-config.md) → Run Operator (structural checks)

| # | Phase | Description | Actor | Input | Output | Scripts |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | [Workspace and config](phases/workspace-and-config.md) | You set **`skill_path`** vs **`skill_workspace`** and edit **`conf/abd-config.json`** so runs are unambiguous. | Human / AI | Skill directory | **`conf/abd-config.json`** with **`active_skill_workspace`** | `python scripts/generate.py --phase workspace-and-config` |
| 3 | Run Operator | Compile check on **`scripts/`**, then **`build.py`**, then scanners listed in **`skill-config.json`**. | Code | **`skill-config.json`**; sources under **`content/parts/`** | Exit **0**; **`AGENTS.md`** current | `python scripts/build.py` · `python scripts/scanner_smoke.py` |

Routing details for **`conf/`** keys: see **[Workspace and config](phases/workspace-and-config.md)** — not repeated here.
