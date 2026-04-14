# Scripts map — build skill

Paths below are relative to the **abd-skill-builder** repository root (`agents/abd-skill-builder` in this monorepo).

| Script | Purpose |
| --- | --- |
| `skills/build_skill/scripts/build_skill.py` | Emit a new skill from **`skills/build_skill/templates/skill-scaffold/`** + copy `scripts/base/` + `library/base/` norms. |
| `scripts/base/build.py` | Batch merge `content/parts/` → root `AGENTS.md` (+ optional `content/built/`, phase built files); post-merge pipeline / scanners (logic inlined). |
| `scripts/base/set_workspace.py` | Read/write `skill-config.json` → `workspace.active_skill_workspace`. |
| `skills/execute_rules/scripts/run_scanners.py` | Scanner driver (CI / local); pass **`--skill-root`** and **`--workspace`**. |

Normative docs: `content/parts/library/base/skill-structure-and-concepts.md`, `rules-and-scanners.md`, `checklist.md`.

Assignment (**skill package** vs **multi-skill agent**): `scripts/base/README.md`.
