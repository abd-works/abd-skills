# `conf/abd-config.json` — authoring instructions

`conf/abd-config.json` is the **workspace routing config** for a skill. It tells scripts where to find the workspace (the project tree the skill reads and writes). The scaffold copy lives at [`skill-scaffold/conf/abd-config.json`](../skill-scaffold/conf/abd-config.json).

## Keys

| Key | Required | What to set |
|-----|----------|-------------|
| `active_skill_workspace` | Yes | Absolute path to the workspace root. Use `"."` only when the skill install directory **is** the workspace (e.g. a self-contained toy skill). For real projects, set an absolute path after scaffold: `python scripts/set_workspace.py /path/to/project`. |
| `known_skill_workspaces` | No | Optional list of other workspace roots you have used with this skill. Useful when switching between projects. Leave `[]` until needed. |
| `skills` | Yes (scaffolded) | Keep `["."]` — tells the operator the current directory is the skill root. |
| `skills_config` | Yes (scaffolded) | Keep `{"order": ["."]}` — controls operator load order when multiple skills are present. |
| `context_paths` | No | Extra directories the operator should treat as context. Leave `[]` unless you have project-level context files outside the workspace. |

## How to configure after scaffold

1. Run `python scripts/set_workspace.py` (no args) — prints the current value.
2. Run `python scripts/set_workspace.py <absolute-path>` — writes `active_skill_workspace`.
3. Verify the path is correct before running any phase that reads workspace files.

## Where the semantics are defined

Full normative detail on `skill_path` vs `skill_workspace` and two-level `conf/` resolution is in **abd-skill-builder** → `content/parts/phases/plan-script-build.md` → **Skill path, skill workspace, and configuration**.
