# SKILL.md — {{skill_name}}

## What this skill does

<!-- One paragraph. What problem does this skill solve? Who uses it? -->
{{skill_description}}

## How to start

1. Set your workspace:
   ```
   python scripts/set_workspace.py <path-to-workspace>
   ```
2. Run a phase:
   ```
   python scripts/generate.py --phase <phase-slug>
   ```
   Copy the output into your AI chat.

3. After the AI produces output, run the operator to verify:
   ```
   python scripts/build.py
   ```

## Phases

<!-- List phases in order. Match content/parts/process.md. -->
| # | Phase | What happens |
|---|-------|--------------|
| 1 | [workspace-and-config](content/parts/phases/workspace-and-config.md) | Confirm workspace path and config |
| 2 | [{{phase_slug}}](content/parts/phases/{{phase_slug}}.md) | {{phase_description}} |

## Rules enforced

<!-- List rules. Bindings are configured in conf/abd-config.json (rule_scanner_bindings). -->
| Rule | Scanner |
|------|---------|
| [{{rule_id}}](rules/{{rule_id}}.md) | `scripts/scanner_{{rule_id}}.py` |

## Requirements

```
pip install -r requirements-dev.txt
```
