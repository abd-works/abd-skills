# Process — {{skill_name}}

**Pipeline:** [Workspace and config](phases/workspace-and-config.md) → [{{phase_name}}](phases/{{phase_slug}}.md) → [{{code_phase_name}}](phases/{{code_phase_slug}}.md)

| #   | Phase                                                  | Description                                                                         | Actor      | Input                                | Output                         | Scripts                                                     |
| --- | ------------------------------------------------------ | ----------------------------------------------------------------------------------- | ---------- | ------------------------------------ | ------------------------------ | ----------------------------------------------------------- |
| 0   | [Workspace and config](phases/workspace-and-config.md) | Set workspace path; install `skill-config.json`; confirm skill and workspace roots. | Human / AI | Skill directory; target project tree | `skill-config.json` correct | `python scripts/base/set_workspace.py <path>`              |
| 1   | [{{phase_name}}](phases/{{phase_slug}}.md)             | {{phase_description}}                                                               | Human / AI | {{phase_input}}                      | {{phase_output}}               | `python scripts/base/generate.py --phase {{phase_slug}}`   |
| 2   | [{{code_phase_name}}](phases/{{code_phase_slug}}.md)   | {{code_phase_description}}                                                          | Code       | {{code_phase_input}}                 | {{code_phase_output}}          | `python scripts/{{skill_name}}/{{code_phase_script}}`      |

---

## Scripts layout

**From the skill directory**, the usual commands are **`python scripts/base/build.py`**, **`python scripts/base/generate.py …`**, and **`python scripts/base/set_workspace.py …`**. Shared implementation lives under **`scripts/base/`** (merge into **`AGENTS.md`**, phase bundles, workspace, **`skill_root.py`**, **`run_scanners.py`**, **`scanner_paths.py`**, **`list_rules_by_order.py`**, **`skill.py`**, **`instructions.py`**, …). Optional rule scanners go under **`scripts/scanners/`**.

**Only in the abd-skill-builder repo:** **`scripts/scaffold_skill.py`** — create a new skill from **`templates/skill-scaffold/`** and copy **`scripts/base/`** from the builder.

Skill-specific scripts (owned by this skill):

```
scripts/{{skill_name}}/   Scripts specific to this skill
  {{code_phase_script}}   {{description of what this script does}}
```

> **Convention:** all scripts you write for this skill go under `scripts/{{skill_name}}/`.
> Never add skill-specific logic directly to `scripts/base/`.
