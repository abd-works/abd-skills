# Workspace and config

This doc is **Workspace and config** in [`../process.md`](../process.md). **All** workspace routing, **`conf/abd-config.json`**, **`active_skill_workspace`**, and related **config** norms live **here**—not scattered through **Plan Script Build** or other phases. Do **Workspace and config** (or read this doc) before you rely on **where the skill runs**.

Emit for an AI session:

```bash
python scripts/generate.py --phase workspace-and-config
```

---

## Purpose

Make  **`skill_workspace`**, and **`conf/abd-config.json`** unambiguous for **this** skill. **[`conf/abd-config.json`](../../conf/abd-config.json)** in **abd-skill-builder** (`skills/abd-skill-builder/conf/abd-config.json`) is the **reference file**: same JSON shape for any skill—**create it at your skill root if missing**, then **set `active_skill_workspace`**.

---

## Skill path, skill workspace, and configuration

### Terms (do not conflate)

| Term | Meaning |
| --- | --- |
| **`skill_path`** | The directory where this  **skill package is installed** (`SKILL.md`, `rules/`, `scripts/`, install-time **`conf/`**). **Workspace routing** (when used) reads **`conf/abd-config.json`** at **`skill_path`**: which **skill workspace** is active, and optionally **`known_skill_workspaces`**, so you can **switch** without hunting paths in prose. |
| **`skill_workspace`** | The **root of the project or solution** you are working on right now (e.g. MM3, a customer repo). This is the **mandatory “where am I running?”** location. Context defaults (e.g. `context/`) are under this root unless you pass paths explicitly. **Anything generated, created, or rendered by the skill** goes under **`skill_workspace/<skill_directory_name>/`** unless the skill’s workspace config overrides the output folder. |
| **Solution workspace** | Same **root** as **`skill_workspace`** in this pipeline: the solution/project tree—not the skill install folder. |

### Two levels of `conf/`

#### 1. Install: `<skill_path>/conf/abd-config.json`

Canonical example in **abd-skill-builder**: **[`skills/abd-skill-builder/conf/abd-config.json`](../../conf/abd-config.json)**. Same path on disk as **`conf/abd-config.json`** at the **skill root**—**that JSON file** is what you edit.

**If your skill has no `conf/` yet:** create **`conf/abd-config.json`** with the same keys (**`active_skill_workspace`**, **`known_skill_workspaces`**) as the builder skill’s file, then **set `active_skill_workspace`** to your workspace root (absolute preferred). **`.`** means the skill install directory **is** the workspace.

**Required** (when this file is used for routing)

| Key | Meaning |
| --- | --- |
| **`active_skill_workspace`** | Path to the **`skill_workspace`** root (absolute preferred). Skills that **route** through this file need a real value **before** meaningful runs against a customer tree; until then, **`.`** is fine. Relative paths resolve from **`skill_path`** (the skill install directory), not the shell cwd. |

**Optional**

| Key | Meaning |
| --- | --- |
| **`known_skill_workspaces`** | Array of paths (strings) for **other** workspaces this skill has worked on, so tooling or operators can **pick** or **add** a workspace without editing unrelated files. |

**Deprecated (still read by older scripts):** `solution_workspace`, `skill_space_path` — same role as **`active_skill_workspace`**; migrate to **`active_skill_workspace`**.

The install folder does **not** hold customer data or large generated trees—only the skill package and this routing config.

#### 2. Workspace: `<skill_workspace>/conf/` (per workspace)

Each **`skill_workspace`** should have a **`conf/`** directory for **parameters that are unique to that workspace** (and optionally per-skill files inside it). Examples:

- **`solution.conf`** at the workspace root (some skills) or under **`conf/`** as the skill evolves.
- **`conf/abd-config.json`** inside the workspace (e.g. story-synthesizer) for **context paths** and other **workspace-local** settings.

Skills document the exact filenames and precedence.

### Overrides

Environment variables may override for CI or local runs; each skill’s **`README`** or **`scripts/_config.py`** states precedence. Prefer editing **`active_skill_workspace`** in **`conf/abd-config.json`** when you need a stable default.

### New skill from scaffold

When **`scaffold_skill.py`** creates a **new** tree, it may **add** **`conf/abd-config.json`** (and **`conf/README.md`**) if missing—**same shape** as **[`../../conf/abd-config.json`](../../conf/abd-config.json)** in **abd-skill-builder**. **Then** (or any time): **set `active_skill_workspace`**.

---

## Related

- **[`plan-script-build.md`](plan-script-build.md)** — **`docs/skill-plan.md`**; assumes workspace terms are clear after **Workspace and config**.
- **[`conf/README.md`](../../conf/README.md)** — short pointer at **`conf/`** in this repo.
