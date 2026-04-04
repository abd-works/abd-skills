# Process — {{skill_name}}

**Pipeline:** [Workspace and config](phases/workspace-and-config.md) → [{{phase_name}}](phases/{{phase_slug}}.md) → [{{code_phase_name}}](phases/{{code_phase_slug}}.md)

| #   | Phase                                                  | Description                                                                         | Actor      | Input                                | Output                         | Scripts                                                     |
| --- | ------------------------------------------------------ | ----------------------------------------------------------------------------------- | ---------- | ------------------------------------ | ------------------------------ | ----------------------------------------------------------- |
| 0   | [Workspace and config](phases/workspace-and-config.md) | Set workspace path; install `conf/abd-config.json`; confirm skill and workspace roots. | Human / AI | Skill directory; target project tree | `conf/abd-config.json` correct | `python scripts/base/set_workspace.py <path>`              |
| 1   | [{{phase_name}}](phases/{{phase_slug}}.md)             | {{phase_description}}                                                               | Human / AI | {{phase_input}}                      | {{phase_output}}               | `python scripts/base/generate.py --phase {{phase_slug}}`   |
| 2   | [{{code_phase_name}}](phases/{{code_phase_slug}}.md)   | {{code_phase_description}}                                                          | Code       | {{code_phase_input}}                 | {{code_phase_output}}          | `python scripts/{{skill_name}}/{{code_phase_script}}`      |

---

## Scripts layout

Base scripts (provided by abd-skill-builder — do not modify):

```
scripts/base/        Universal skill-builder scripts
  build.py           Assemble AGENTS.md from content/parts/
  generate.py        Generate a phase bundle for AI injection
  markers.py         Phase-scope and section marker utilities
  run_scanners.py    Run all scanners in conf/abd-config.json
  set_workspace.py   Read/write active_skill_workspace in conf/abd-config.json
  list_rules_by_order.py  List rules sorted by order
  skill_root.py      Shared utility — resolves skill root path
```

Skill-specific scripts (owned by this skill):

```
scripts/{{skill_name}}/   Scripts specific to this skill
  {{code_phase_script}}   {{description of what this script does}}
scripts/scanners/         One scanner per rule
  scanner_{{rule_id}}.py
```

> **Convention:** all scripts you write for this skill go under `scripts/{{skill_name}}/`.
> Never add skill-specific logic directly to `scripts/base/`.
