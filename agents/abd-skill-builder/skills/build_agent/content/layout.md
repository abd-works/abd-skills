# Multi-skill agent layout

| Path | Role |
| --- | --- |
| `SKILL.md` | Short discovery for the agent package (optional if repo is agent-only). |
| `AGENTS.md` | **Generated** — do not hand-edit; built from `content/*.md`. |
| `content/outline.md` | Stages, flow, hand-offs between skills. |
| `content/principles.md` | Non-negotiables for this agent. |
| `content/purpose.md` | Why this agent exists. |
| `content/role.md` | Who the orchestrator is and what it delegates. |
| `skill-config.json` | **`agents_md.title`**, **`agents_md.sections`** (four files above), **`workspace.active_skill_workspace`**, optional **`build`**. |
| `scripts/build.py` | Concatenate `content/` sections into `AGENTS.md` (thin merge). |
| `skills/workspace/` | Workspace skill: **`SKILL.md`**, **`scripts/get_workspace.py`**, **`scripts/set_workspace.py`**. |
| `skills/<skill>/` | Other leaf skills for each stage (convert, chunk, …). |

**Not** used in the minimal agent pattern: `content/parts/process.md`, `phase_files`, `scripts/base/generate.py` (those belong to a **skill package**).
