# Workspace configuration

## Install: `<skill_path>/conf/abd-config.json`

| Key | Required | Meaning |
| --- | --- | --- |
| **`active_skill_workspace`** | **Yes** | Root of the **skill workspace** (same as “solution workspace”): the directory that contains **`solution.conf`** for this skill. Paths relative to the skill install directory resolve under **`skill_path`**; absolute paths are allowed. The skill package only holds the skill and this pointer—not the customer corpus. |

**Optional:** **`known_skill_workspaces`** — other roots this skill may switch to (see **`abd-skill-builder`** [`content/parts/library/workspace-config.md`](../abd-skill-builder/content/parts/library/workspace-config.md)).

**Deprecated:** **`solution_workspace`**, **`skill_space_path`** — same role as **`active_skill_workspace`**; migrate to **`active_skill_workspace`**.

This skill’s **`scripts/_config.py`** resolves **`solution.conf`** and phase outputs from that root.

## Workspace: `<skill_workspace>/conf/`

Workspace-local parameters (unique to that project) may live under **`conf/`** at the skill workspace root alongside **`solution.conf`** (or as documented per skill). See **`abd-skill-builder`** [`content/parts/library/workspace-config.md`](../abd-skill-builder/content/parts/library/workspace-config.md) for the two-level model.
