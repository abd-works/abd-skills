# Workspace configuration

## `abd-config.json`

| Key | Meaning |
| --- | --- |
| **`solution_workspace`** | **Required.** Root of the **solution workspace** (e.g. customer repo or MM3). Scripts resolve outputs under this tree. Use an absolute path in real use. The skill package only holds this pointer—not the project itself. |
| **`skill_space_path`** | Deprecated; same meaning as **`solution_workspace`**. Older configs may still set only this key; the engine maps it to **`solution_workspace`**. |

Other keys (`skills`, `skills_config`, `context_paths`, …) are documented in **`SKILL.md`**.
