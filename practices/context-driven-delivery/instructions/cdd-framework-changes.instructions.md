# cdd-framework-changes — always use a sub-agent for abd-skills changes during project work

Whenever a change is needed to any part of the abd-skills framework — including but not limited to:

- Any `SKILL.md` file (context-driven delivery, architecture, domain, story, UX, kanban, or any other practice)
- Any supporting script (`deploy-skills.ps1`, `set_workspace.py`, etc.)
- Any instruction file (`.instructions.md`)
- Any template, reference file, or common file used by skills
- Any command prompt file (`.prompt.md`)

— and the agent is currently in the middle of project work — the **default action is always to route the change to a non-blocking background sub-agent**.

## The rule

1. **Launch a background sub-agent** to apply the framework change.
2. **Continue project work immediately** — do not pause, do not wait for the sub-agent.
3. **Tell the user** in one sentence what the sub-agent will handle and that it is running in the background.

Do not apply framework changes inline during a project session unless the change is a single-line edit the user is actively watching you make and it takes less than 5 seconds.

## What the sub-agent needs

Give the sub-agent:
- The exact files to change (absolute paths)
- The intent of the change (what to add, remove, or fix)
- Whether to deploy after making the change (and to which deploy root)
- Enough context to validate its own output

## Deploy after every framework change

Any change to the canonical source (`abd-skills`) must be followed by a deploy to the active project's `.cursor/` folder. Include the deploy step in the sub-agent's instructions. Use:

```powershell
& "C:\dev\abd-skills\common\scripts\deploy-skills.ps1" -ide cursor -Package all -DeployRoot "<project-root>"
```

## Examples

**Goes to sub-agent:**
- Updating a SKILL.md rule or DO/DO NOT section
- Adding a new instruction file to `abd-skills/practices/`
- Fixing a deploy script parameter
- Wiring a new common reference file across multiple skills
- Updating a command prompt file

**Stays inline (no sub-agent):**
- Writing a line to `cdd-session-journal.md`
- Updating a project artifact (story map, acceptance criteria, architecture doc)
- A single-word fix the user is watching in real time
