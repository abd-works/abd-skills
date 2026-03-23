# `abd-config.json.template`

This is **not** an empty template. **`scaffold_skill.py`** copies it to **`<new-skill>/conf/abd-config.json`** as plain JSON (no extra build step).

| Key | Role |
| --- | --- |
| **`active_skill_workspace`** | Path to the **skill workspace** root. **`"."`** means “the skill install directory is the workspace” (relative paths resolve from **`skill_path`**). Replace with an absolute path when work lives in a customer or solution tree. |
| **`known_skill_workspaces`** | Optional list of other workspace roots you have used (see **`parts/phases/plan-script-build.md`** → **Skill path, skill workspace, and configuration** in **abd-skill-builder**). |

Edit the generated **`conf/abd-config.json`** after scaffold so **`active_skill_workspace`** matches where **`docs/`** and project files actually live.
