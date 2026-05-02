---
catalogue_summary: "Fix the deliverable first, log corrections, iterate until right — only then improve the source."
---

# correct-output

## Overview

A general-purpose correction loop for any generated output. When something is wrong, fix the output first — iterate until it's right — then only improve the source when the user asks.

Works with or without a formal skill. Works with or without scanners. The log is the universal artifact.

## How it fits together

```ascii
output is wrong
       |
       v
  identify + log ──> re-generate ──> review ──> confirm
       ^                                          |
       └──────────── iterate ─────────────────────┘
                                                  |
                                          (output is right, move on)
                                                  |
                              (only when user asks: improve the source)
```

## Layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | Full skill |
| `ide-files/*.mdc` | Cursor always-on rule |
| `ide-files/*.instructions.md` | VS Code always-on (same body as `.mdc` after frontmatter) — deployed only with **`-IDE Both`** |
| `ide-files/*.prompt.md` | Cursor slash command (**.cursor/commands/**); **`.github/prompts/`** only with **`-IDE Both`** |
| `templates/corrections-log.md` | Log template |
| `scripts/Deploy-SkillOutputs.ps1` | Deploy links to a project + Cursor skills junction |

## Deploy

```powershell
.\skills\correct_output\scripts\Deploy-SkillOutputs.ps1 -ProjectRoot <target-project> -Force
```

Default **`-IDE Cursor`**. Use **`-IDE Both`** only when that project should also get VS Code instructions and **`.github/prompts/`**.

## Source

- [SKILL.md](SKILL.md)
