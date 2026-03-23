# `test/` — abd-maps-models-specs

All **tests and test-only assets** for this skill live here (under **`skills/abd-maps-models-specs/test/`**).

| Path | Role |
|------|------|
| **`sample-workspace/`** | **Bundled example skill workspace** — referenced by default **`conf/abd-config.json`** → `"active_skill_workspace": "test/sample-workspace"`. Contains `solution.conf`, sample sources, and generated outputs under `<output_dir>/` (see **`sample-workspace/README.md`**). |
| **`fixture/<scenario>/`** | Optional frozen snapshots for reproducible checks (add per skill need). |

**Convention:** Script tests target **`scripts/`**; workspaces and fixtures stay under **`test/`** so the skill package root stays clean.

See **`abd-skill-builder`** **`docs/skill-repo-standards.md`** (Tests & fixtures) and the generic **`test/README.md`** pattern from **`scaffold_skill.py`**.
