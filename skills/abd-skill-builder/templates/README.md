# `templates/` — small extras only

**Canonical layout** for a new skill is **`templates/skill-scaffold/`** — real directories, example files, placeholders. **`scripts/scaffold_skill.py`** copies that tree into your output directory and applies `{{…}}` substitution.

**Universal scripts and shared library norms are not duplicated in the template:** after copying **`skill-scaffold/`** (including **`content/parts/library/required/`** — purpose, outline, role, principles), the scaffold copies **`content/parts/library/base/`** from **abd-skill-builder** into the new skill’s **`content/parts/library/base/`**, then copies **`scripts/base/build.py`**, **`scripts/base/generate.py`**, and **`scripts/base/set_workspace.py`** from **abd-skill-builder**’s **`scripts/`**, then copies **`scripts/base/`** in full. Child skills use the same **`Skill.load()`** / **`workspace_checklists`** pipeline and the same **`instructions._resolve_library_md`** order: **`library/<file>`** → **`library/required/<file>`** → **`library/base/<file>`**.

| Kind | Location |
| --- | --- |
| **What to write** in `skill-config.json`, `process.md`, `library/base/checklist.md` (norms) | **`content/parts/phases/plan-script-build.md`** (Stage 1); **`content/parts/library/process-phases.md`** for rich **`process.md`** and phase execution norms |
| **Folder and file layout** | **`templates/skill-scaffold/`** under **abd-skill-builder** |
| **`library/base/` in a scaffolded skill** | Copied from **abd-skill-builder** by **`scaffold_skill.py`** — includes **`checklist.md`**; see **`content/parts/library/base/checklist.md`** |
| **Entrypoint + `base` scripts** | Copied from **`abd-skill-builder/scripts/`** and **`abd-skill-builder/scripts/base/`** — see **`content/parts/phases/scaffold.md`** |

Keep codegen-only assets in **`templates/`** when they are **not** part of **`skill-scaffold/`**.
