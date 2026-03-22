# Workspace configuration

## `abd-config.json` (optional for this skill)

| Key | Required | Meaning |
| --- | --- | --- |
| **`active_skill_workspace`** | For skills that operate on a customer tree | Root of the **skill workspace** (the project where this skill runs). Relative paths resolve from **`skill_path`** (the skill install directory). |
| **`known_skill_workspaces`** | No | Optional list of other workspace roots. |

**This skill** (`abd-skill-builder`) ships a minimal **`abd-config.json`** for template parity and local tests; routing is documented in [`../content/parts/library/workspace-config.md`](../content/parts/library/workspace-config.md).

## Other files here

- **`build-strategy.json`** — Strategizer / scaffold metadata for skills that use it.
