# Workspace and Configuration

This document specifies **workspace routing**, **`skill-config.json`**, **`active_skill_workspace`**, and related **configuration norms** for the abd-diagrams skill.

**All workspace-related configuration lives here—not scattered through documentation.**

---

## Generate Workspace Config (for new projects)

```bash
python scripts/base/set_workspace.py
```

Shows the current **`active_skill_workspace`** from **`skill-config.json`**.

---

## Command Line: Set Workspace

From the **skill package root** (the folder that contains **`scripts/`** and **`skill-config.json`**):

- **`python scripts/base/set_workspace.py`** — prints **`active_skill_workspace`** from **`skill-config.json`** (or **`(not set)`**).

- **`python scripts/base/set_workspace.py <path>`** — sets **`active_skill_workspace`** in **`skill-config.json`** to **`<path>`** (resolved; stored **relative to the skill package** when that keeps the value portable, otherwise absolute). **`<path>`** must be an existing directory (the **skill workspace** root — project or solution tree you run against).

---

## Purpose

Make **`skill_workspace`**, and **`skill-config.json`** unambiguous for **this** skill.

---

## Skill Path, Workspace, and Configuration

### Terms (do not conflate)

| Term                  | Meaning                                                      |
| --------------------- | ------------------------------------------------------------ |
| **`skill_path`**      | The directory where this **skill package is installed** (`SKILL.md`, `rules/`, `scripts/`). **Workspace routing** (when used) reads **`skill-config.json`** at **`skill_path`**: which **skill workspace** is active, and optionally **`known_skill_workspaces`**, so you can **switch** without hunting paths in prose. |
| **`skill_workspace`** | The **root of the project or solution** you are working on right now (e.g. a customer repo like mm3e-experiment). This is the **mandatory "where am I running?"** location. Context defaults (e.g. `context/`) are under this root unless you pass paths explicitly. **Anything generated, created, or rendered by the skill** goes under **`skill_workspace/<skill_directory_name>/`** unless the skill's workspace config overrides the output folder. |

### Install: `<skill_path>/skill-config.json`

**Reference example:** `/sessions/kind-inspiring-cori/mnt/abd-diagrams/skill-config.json`

**Location:** The same path on disk as **`SKILL.md`** — at the **skill root**.

**If your skill has no `skill-config.json` yet:** create it with the same keys (**`active_skill_workspace`**, **`known_skill_workspaces`**) as shown below, then **set `active_skill_workspace`** to your workspace root (absolute preferred). **`.`** means the skill install directory **is** the workspace.

#### Required (when this file is used for routing)

| Key                          | Meaning                                                      |
| ---------------------------- | ------------------------------------------------------------ |
| **`active_skill_workspace`** | Path to the **`skill_workspace`** root (absolute preferred). Skills that **route** through this file need a real value **before** meaningful runs against a customer tree; until then, **`.`** is fine. Relative paths resolve from **`skill_path`** (the skill install directory), not the shell cwd. |

#### Optional

| Key                          | Meaning                                                      |
| ---------------------------- | ------------------------------------------------------------ |
| **`known_skill_workspaces`** | Array of paths (strings) for **other** workspaces this skill has worked on, so tooling can **pick** or **add** a workspace without editing unrelated files. |

The install folder does **not** hold customer data or large generated trees—only the skill package and this routing config.

### Project Workspace: `<skill_workspace>/`

Each **`skill_workspace`** (the customer or project tree like mm3e-experiment) may hold **parameters unique to that workspace** — e.g. **`solution.conf`**, extra **`context/`** paths, or a workspace-local **`skill-config.json`** for overrides. Filenames and precedence are **per skill**; there is **no** required top-level **`conf/`** folder.

### Output Convention

**Anything generated, created, or rendered by the skill** goes under:

```
<skill_workspace>/<skill_directory_name>/
```

For abd-diagrams, this is:

```
<skill_workspace>/abd-diagrams/
```

Examples:
- `/sessions/kind-inspiring-cori/mnt/mm3e-experiment/abd-diagrams/domain-scan-model.drawio`
- `/sessions/kind-inspiring-cori/mnt/mm3e-experiment/abd-diagrams/step-1-extraction.drawio`

### Overrides

Environment variables may override for CI or local runs; see **`scripts/_config.py`** for precedence. Prefer editing **`active_skill_workspace`** in **`skill-config.json`** when you need a stable default.

---

## Example: MM3E Project

**Skill path (install):** `/sessions/kind-inspiring-cori/mnt/abd-diagrams/`

**Skill workspace (project):** `/sessions/kind-inspiring-cori/mnt/mm3e-experiment/`

**skill-config.json (at skill_path):**
```json
{
  "active_skill_workspace": "/sessions/kind-inspiring-cori/mnt/mm3e-experiment",
  "known_skill_workspaces": [
    "/sessions/kind-inspiring-cori/mnt/mm3e-experiment"
  ]
}
```

**Set workspace:**
```bash
cd /sessions/kind-inspiring-cori/mnt/abd-diagrams
python scripts/base/set_workspace.py /sessions/kind-inspiring-cori/mnt/mm3e-experiment
```

**Output location:**
```
/sessions/kind-inspiring-cori/mnt/mm3e-experiment/abd-diagrams/
  ├── domain-scan-model.drawio
  ├── step-1-extraction.drawio
  ├── step-2-refined-model.drawio
  └── [other diagram files]
```

---

## Integration with abd-ooad

When abd-ooad and abd-diagrams work together on the same project:

1. **Both skills** set their `active_skill_workspace` to the **same project root**
2. **abd-ooad** creates Markdown descriptions in `<workspace>/abd-ooad/`
3. **abd-diagrams** creates diagrams in `<workspace>/abd-diagrams/`
4. **Domain model files** are paired:
   - `abd-ooad/domain-scan-model.md` ↔ `abd-diagrams/domain-scan-model.drawio`
   - `abd-ooad/step-1-extraction.md` ↔ `abd-diagrams/step-1-extraction.drawio`
   - etc.

---

## Changelog

- **2026-04-06:** Ported workspace-and-config specification from skill-creator standard
