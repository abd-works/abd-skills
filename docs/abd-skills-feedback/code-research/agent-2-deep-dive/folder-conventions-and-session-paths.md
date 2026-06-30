# Deep Dive: Folder Conventions & Session Paths

## Principles & Patterns

- **One canonical session folder**: `docs/cdd-sessions/<YYYY-MM-DD>-<topic>/`. Established by `cdd-handoff/SKILL.md` line 24.
- **Rename in flight**: a repository-wide migration from `docs/sessions/` to `docs/cdd-sessions/` is partly complete. 8 files still use the legacy path.
- **No lint or guard**: nothing in the build or in `common/scripts/` fails when the legacy path appears.

## File Structure

```
abd-skills/
├── practices/context-driven-delivery/
│   ├── skills/
│   │   ├── abd-context-driven-delivery/SKILL.md   ← legacy `docs/sessions/` at line 43
│   │   └── cdd-handoff/SKILL.md                  ← canonical `docs/cdd-sessions/` at line 24
│   ├── scripts/
│   │   ├── session-setup.ps1                      ← legacy
│   │   ├── session-setup.sh                       ← legacy
│   │   ├── detect-correction.ps1                  ← legacy
│   │   └── detect-correction.sh                   ← legacy
│   └── prompts/
│       └── cdd-resume.prompt.md                   ← uses cdd-sessions/
├── common/
│   └── decision-record.md                          ← legacy
├── docs/
│   └── eval-loop-planning.md                       ← legacy
└── catalog/doc/skill/abd-context-driven-delivery/
    └── SKILL.html                                  ← legacy (generated artifact)
```

## Participants

| File | Path used | Role |
|---|---|---|
| `cdd-handoff/SKILL.md` | `docs/cdd-sessions/` | Canonical writer |
| `cdd-resume.prompt.md` | `docs/cdd-sessions/` | Canonical reader |
| `abd-context-driven-delivery/SKILL.md` | `docs/sessions/` (legacy) | Conflicts with handoff |
| `session-setup.ps1` / `.sh` | `docs/sessions/` (legacy) | Bootstraps wrong folder name |
| `detect-correction.ps1` / `.sh` | `docs/sessions/` (legacy) | Looks for journal in wrong place |
| `common/decision-record.md` | `docs/sessions/` (legacy) | Reference doc — propagates the error |
| `docs/eval-loop-planning.md` | `docs/sessions/` (legacy) | Planning doc |
| `catalog/doc/skill/.../SKILL.html` | `docs/sessions/` (legacy) | Generated; re-renders the bug |

## Flow

A fresh agent reads the orchestrator SKILL.md first → sees `docs/sessions/` → starts a session under that name. Later it reads `cdd-handoff/SKILL.md` → sees `docs/cdd-sessions/` → user is now looking in the wrong folder. Or the bootstrap script ran first and created `docs/sessions/<date>-<topic>/` but the handoff later writes to `docs/cdd-sessions/<date>-<topic>/` — two folders, two states.

## Walkthrough Example — pml-midtier session

The session correctly lives under `pml-midtier/docs/cdd-sessions/2026-06-26-reverse-engineer-discovery-to-test/`. Three artifacts inside it (`cdd-session-checklist.md`, `cdd-session-journal.md`, and now this `abd-skills-feedback/` folder) all follow the new path because the user established it explicitly. The journal correction (lines 117–119) names the rule. **Until the repository rename is finished, every new session is one user-correction away from going to the wrong folder.**
