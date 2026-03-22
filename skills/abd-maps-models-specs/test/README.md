# `test/` — abd-maps-models-specs

All **tests and test-only assets** for this skill live here (under **`skills/abd-maps-models-specs/test/`**).

| Path | Role |
|------|------|
| **`mm3/`** | **Active skill workspace** for MM3 — referenced by **`conf/abd-config.json`** → `"active_skill_workspace": "test/mm3"`. Contains `solution.conf`, inputs, generated outputs under `abd-maps-models-specs/`, etc. (see **`mm3/README.md`** if present). |
| **`fixture/mm3/`** | **Frozen MM3 fixture** — bundled inputs, sample phase artifacts, and **`solution.conf`** for reproducible checks / docs. Not necessarily the same tree as a live `test/mm3` run. |
| **`mm3/orchestration/`** | Example logs / orchestration artifacts (optional). |

**Convention:** Script tests target **`scripts/`**; workspaces and fixtures stay under **`test/`** so the skill package root stays clean.

See **`abd-skill-builder`** **`docs/skill-repo-standards.md`** (Tests & fixtures) and the generic **`test/README.md`** pattern from **`scaffold_skill.py`**.
