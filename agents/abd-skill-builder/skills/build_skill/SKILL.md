---
name: build-skill
description: Create a new skill package from the builder template (build_skill.py) and merge AGENTS.md via scripts/base/build.py.
---

# Build skill

Use this leaf when you need to **create** a skill package (Open Agent Skills layout with `skill-config.json`, `content/parts/`, `scripts/base/`) or **merge** the builder’s `AGENTS.md`.

## Commands (abd-skill-builder repo root)

| Action | Command |
| --- | --- |
| New tree | `python skills/build_skill/scripts/build_skill.py --name <id> --out <path>` |
| Merge `AGENTS.md` / built slices | `python scripts/base/build.py` |
| Workspace pointer | `python scripts/base/set_workspace.py [<path>]` |

**From anywhere** (each accepts **`--skill-root`**, default cwd — runs that skill’s vendored **`scripts/base/...`** when applicable):

| Script | Purpose |
| --- | --- |
| **`skills/build_skill/scripts/set_workspace.py`** | Delegates to target **`scripts/base/set_workspace.py`** |
| **`skills/build_skill/scripts/check_skill_layout.py`** | Smoke-check **`SKILL.md`**, **`skill-config.json`** / **`content/parts`** / **`rules/`** |
| **`skills/build_skill/scripts/build_pipeline_plan.py`** | Print **`build.build_pipeline`** vs merged scanner steps (loads **`skills/execute_rules/scripts/scanner_paths.py`** from this repo) |

## Docs

- **`content/scripts-map.md`** — scripts table + library norms.
- **`scripts/README.md`** — copy-paste for the commands above.

## See also

- **`../../content/builder-architecture.md`** — `build_agent` vs capability packs.
- **`../../content/parts/library/base/skill-structure-and-concepts.md`** — §3 layout.
