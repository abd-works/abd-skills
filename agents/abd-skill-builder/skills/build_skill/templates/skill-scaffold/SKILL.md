# SKILL.md — {{skill_name}}

<!-- Authoring: keep discovery + instructions in this file until ~1–2 screens of dense procedure; then split to references/ or library shards and link here. See library/base/skill-structure-and-concepts.md → "SKILL.md — default one file". -->

## What this skill does

<!-- One paragraph. What problem does this skill solve? Who uses it? -->
{{skill_description}}

## How to start

1. Set your workspace:
   ```
   python scripts/base/set_workspace.py <path-to-workspace>
   ```
2. Work from **`SKILL.md`** and the phase docs under **`content/parts/phases/`** (see **`content/parts/process.md`**). Use your agent with this skill attached; keep the repo as the source of truth.

3. When you need a merged **`AGENTS.md`** or validation, run:
   ```
   python scripts/base/build.py
   ```

## Phases

<!-- List phases in order. Match content/parts/process.md. -->
| # | Phase | What happens |
|---|-------|--------------|
| 1 | [workspace-and-config](content/parts/phases/workspace-and-config.md) | Confirm workspace path and config |
| 2 | [{{phase_slug}}](content/parts/phases/{{phase_slug}}.md) | {{phase_description}} |

## Rules enforced

<!-- List rules. Bindings: skill-config.json → workspace.rule_scanner_bindings. -->
| Rule | Scanner |
|------|---------|
| [{{rule_id}}](rules/{{rule_id}}.md) | `scanners/{{rule_id}}-scanner.py` |

## Requirements

```
pip install -r requirements-dev.txt
```
