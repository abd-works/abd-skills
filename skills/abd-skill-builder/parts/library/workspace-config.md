s filel path, skill workspace, and configuration (normative)

**Where this belongs:** **`library/`** normative text (merged into **`AGENTS.md`**). **Primary use:** **Stage 1 — Plan Script Build** — you read this when routing **`active_skill_workspace`** and **`conf/abd-config.json`** before scaffold/migrate. **Procedure** (checklist order, **`docs/skill-plan.md`**, templates): **[plan-script-build](../phases/plan-script-build.md)**.

---

## Terms (do not conflate)

| Term | Meaning |
| --- | --- |
| **`skill_path`** | The directory where the **skill package is installed** (`SKILL.md`, `rules/`, `scripts/`, install-time `conf/`). Almost nothing here is **about** a customer corpus or generated artifacts. What **must** live here for workspace routing is **`conf/abd-config.json`**: which **skill workspace** is active, and optionally which workspaces you have used before, so you can **switch** without hunting paths in prose. |
| **`skill_workspace`** | The **root of the project or solution** you are working on right now (e.g. MM3, a customer repo). This is the **mandatory “where am I running?”** location. Context defaults (e.g. `context/`) are under this root unless you pass paths explicitly. **Anything generated, created, or rendered by the skill** goes under **`skill_workspace/<skill_directory_name>/`** unless the skill’s workspace config overrides the output folder. |
| **Solution workspace** | Same **root** as **`skill_workspace`** in this pipeline: the solution/project tree—not the skill install folder. |

## Two levels of `conf/`

### 1. Install: `<skill_path>/conf/abd-config.json` (mandatory)

**Greenfield source:** **`scaffold_skill.py`** materializes **`conf/abd-config.json`** from **[`templates/abd-config.json.template`](../../templates/abd-config.json.template)** in **abd-skill-builder** (same keys; edit the **generated** file in your skill). **`active_skill_workspace`** is the field that names **`skill_workspace`**—set it accurately to the tree where **`docs/`**, customer files, and outputs live.

**Required**

| Key | Meaning |
| --- | --- |
| **`active_skill_workspace`** | Path to the **`skill_workspace`** root (absolute preferred). You **cannot** run the skill in a meaningful way without this. Relative paths are resolved from **`skill_path`** (the skill install directory), not from the current shell cwd. |

**Optional**

| Key | Meaning |
| --- | --- |
| **`known_skill_workspaces`** | Array of paths (strings) for **other** workspaces this skill has worked on, so tooling or operators can **pick** or **add** a workspace without editing unrelated files. |

**Deprecated (still read by older scripts):** `solution_workspace`, `skill_space_path` — same role as **`active_skill_workspace`**; migrate to **`active_skill_workspace`**.

The install folder does **not** hold customer data or large generated trees—only the skill package and this routing config.

### 2. Workspace: `<skill_workspace>/conf/` (per workspace)

Each **`skill_workspace`** should have a **`conf/`** directory for **parameters that are unique to that workspace** (and optionally per-skill files inside it). Examples:

- **`solution.conf`** at the workspace root (some skills) or under **`conf/`** as the skill evolves.
- **`conf/abd-config.json`** inside the workspace (e.g. story-synthesizer) for **context paths** and other **workspace-local** settings.

Skills document the exact filenames and precedence.

## Overrides

Environment variables may override for CI or local runs; each skill’s **`README`** or **`scripts/_config.py`** states precedence. Default: set **`active_skill_workspace`** in **`conf/abd-config.json`** first.

## Scaffold guarantee

**`abd-skill-builder`** scaffold (**`scaffold_skill.py`**) creates **`conf/abd-config.json`** from **[`templates/abd-config.json.template`](../../templates/abd-config.json.template)** and **`conf/README.md`** from **`conf_README.md.template`**, both with **`active_skill_workspace`** and **`known_skill_workspaces`**. Replace **`active_skill_workspace`** with the real **`skill_workspace`** root (or keep **`.`** only when the install folder is the workspace) before running pipelines.
