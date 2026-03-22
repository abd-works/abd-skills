# Process templates (`content/parts/templates/`)

**Purpose:** Authoring aids for **`content/parts/process.md`** in **other** skills. These files are **not** merged into **`AGENTS.md`** by default (not part of **`scripts/build.py`** library merge). Copy or adapt them when you define a multi-stage pipeline.

| File | Use |
|------|-----|
| **`process-team.md.template`** | **Team process plate** — starter structure with outcome, principles, inputs/outputs, stages, and a phase table (maps-models-specs style). Replace `{{skill_name}}`, add your phases, then save as **`content/parts/process.md`**. |

**Scaffold:** `scripts/scaffold_skill.py` still emits a **minimal** `process.md` from **`templates/process.md.template`** (skill root). Replace or merge with the team plate when your skill needs richer process documentation.
