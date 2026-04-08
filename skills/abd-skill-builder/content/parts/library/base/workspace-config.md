# Workspace and config

This doc is **Workspace and config** in [`../process.md`](../process.md). **All** workspace routing, **`skill-config.json`**, **`active_skill_workspace`**, and related **config** norms live **here**—not scattered through **Plan Script Build** or other phases. Do **Workspace and config** (or read this doc) before you rely on **where the skill runs**.

Emit for an AI session:

```bash
python scripts/base/generate.py --phase workspace-and-config
```

**Command line (workspace pointer):** From the **skill package root** (the folder that contains **`scripts/`** and **`skill-config.json`**), same as **abd-maps-models-specs** **Set workspace** / **`scripts/base/set_workspace.py`**:

- `python scripts/base/set_workspace.py` — prints **`active_skill_workspace`** from **`skill-config.json`** (or **`(not set)`**).

- `python scripts/base/set_workspace.py <path>` — sets **`active_skill_workspace`** in **`skill-config.json`** to **`<path>`** (resolved; stored **relative to the skill package** when that keeps the value portable, otherwise absolute). **`<path>`** must be an existing directory (the **skill workspace** root — project or solution tree you run against).

  Scaffold copies **`scripts/base/set_workspace.py`** from **abd-skill-builder** into every new skill.

---

## Purpose

Make  **`skill_workspace`**, and **`skill-config.json`** unambiguous for **this** skill. 

---

## Skill path, skill workspace, and configuration

### Terms (do not conflate)

| Term                  | Meaning                                                      |
| --------------------- | ------------------------------------------------------------ |
| **`skill_path`**      | The directory where this **skill package is installed** (`SKILL.md`, `rules/`, `scripts/`). **Workspace routing** (when used) reads **`skill-config.json`** at **`skill_path`**: which **skill workspace** is active, and optionally **`known_skill_workspaces`**, so you can **switch** without hunting paths in prose. |
| **`skill_workspace`** | The **root of the project or solution** you are working on right now (e.g. a customer repo). This is the **mandatory “where am I running?”** location. Context defaults (e.g. `context/`) are under this root unless you pass paths explicitly. **Anything generated, created, or rendered by the skill** goes under **`skill_workspace/<skill_directory_name>/`** unless the skill’s workspace config overrides the output folder. |
|                       |                                                              |

### Install: `<skill_path>/skill-config.json`

Canonical example in **abd-skill-builder**: **[`skills/abd-skill-builder/skill-config.json`](../../skill-config.json)**. Same path on disk as **`skill-config.json`** at the **skill root**—**that JSON file** is what you edit.

**If your skill has no `skill-config.json` yet:** create it with the same keys (**`active_skill_workspace`**, **`known_skill_workspaces`**) as the builder skill’s file, then **set `active_skill_workspace`** to your workspace root (absolute preferred). **`.`** means the skill install directory **is** the workspace.

**Required** (when this file is used for routing)

| Key                          | Meaning                                                      |
| ---------------------------- | ------------------------------------------------------------ |
| **`active_skill_workspace`** | Path to the **`skill_workspace`** root (absolute preferred). Skills that **route** through this file need a real value **before** meaningful runs against a customer tree; until then, **`.`** is fine. Relative paths resolve from **`skill_path`** (the skill install directory), not the shell cwd. |

**Optional**

| Key                          | Meaning                                                      |
| ---------------------------- | ------------------------------------------------------------ |
| **`known_skill_workspaces`** | Array of paths (strings) for **other** workspaces this skill has worked on, so tooling can **pick** or **add** a workspace without editing unrelated files. |

The install folder does **not** hold customer data or large generated trees—only the skill package and this routing config.

### Project workspace: `<skill_workspace>/`

Each **`skill_workspace`** (the customer or project tree) may hold **parameters unique to that workspace** — e.g. **`solution.conf`**, extra **`context/`** paths, or a workspace-local **`skill-config.json`** for overrides. Filenames and precedence are **per skill**; there is **no** required top-level **`conf/`** folder in the skill-builder layout.

### Overrides

Environment variables may override for CI or local runs; each skill’s **`README`** or **`scripts/_config.py`** states precedence. Prefer editing **`active_skill_workspace`** in **`skill-config.json`** when you need a stable default.

### New skill from scaffold

When **`scaffold_skill.py`** creates a **new** tree, it may **add** **`skill-config.json`** if missing—**same shape** as **[`../../skill-config.json`](../../skill-config.json)** in **abd-skill-builder**. **Then** (or any time): **set `active_skill_workspace`**.
