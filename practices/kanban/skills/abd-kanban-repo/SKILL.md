---
name: abd-kanban-repo
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Git operations driven by Kanban board state changes — commits, branches, PRs per ticket lifecycle.
description: >-
  Manage git history for a delivery engagement. Commits, branches, pushes, and PRs
  are driven by ticket state changes on the Kanban board — not by slots or runs.
  Configurable granularity (per-skill, per-stage, per-ticket) and branching strategy.
  Use when configuring git policy for a Kanban delivery or when role agents need
  commit, branch, or PR operations tied to board events.
---
# abd-kanban-repo

## Purpose

Manage git history for a delivery engagement. Commits, branches, pushes, and PRs are driven by **ticket state changes** on the Kanban board — not by slots or runs.

---

## Git granularity (configurable per strategy)

The kanban lead configures when git operations fire. Three levels:

| Granularity | Commit | Push | Branch | PR |
| --- | --- | --- | --- | --- |
| **per-skill** (default) | After each skill completes on a ticket | After each skill completes | Per ticket | Off by default |
| **per-stage** | After all skills in a stage complete (ticket state change) | On stage completion | Per ticket | Off by default |
| **per-ticket** | After ticket completes (all stages done, or scattered) | On ticket completion | Per scope level | Off by default |

Default: **per-skill commit + push**. This gives git-level tracking of every ticket state change.

PRs are **off by default**. Enable per strategy or autonomy setting.

---

## Branching strategy

| Scope | Branch name | When created | When merged |
| --- | --- | --- | --- |
| Ticket | `delivery/<ticket-id>` | When ticket enters active | When ticket completes or scatters |
| Scope level | `delivery/<scope>/<name>` | e.g. `delivery/increment/inc-1` | When all tickets at that scope complete |
| Main | `main` | — | Merge target |

The kanban lead chooses branching scope based on autonomy:

- **tight** → branch per ticket, PR required before merge
- **moderate** → branch per ticket, auto-merge on all reviews pass
- **autonomous** → commit directly to main (no branches)

---

## Pull and push behavior

**Pull** (git pull) happens:
- Before starting work on a skill (agent pulls latest before producing)

**Push** (git push) happens at the configured granularity:
- **per-skill**: push after each skill done on a ticket
- **per-stage**: push after ticket completes a stage
- **per-ticket**: push after ticket archived/scattered

---

## Commit message convention

```
<ticket-id>.<stage>.<skill>: <one-line summary>

Ticket: <ticket-id>
Lineage: <lineage path>
Stage: <stage>
Skill: <skill-name>
Role: <executor | reviewer>
```

Examples:

```
inc-1.exploration.abd-acceptance-criteria: Write AC for Browse Characters stories

Ticket: inc-1
Lineage: Hero VTT > Increment 1
Stage: exploration
Skill: abd-acceptance-criteria
Role: executor
```

```
sprint-1.engineering.abd-clean-code: Implement character browser module

Ticket: sprint-1
Lineage: Hero VTT > Increment 1 > Sprint 1
Stage: engineering
Skill: abd-clean-code
Role: executor
```

---

## Tool: `scripts/git_ops.py`

The kanban lead (or role agents) invoke this script for git operations.

### Usage

```bash
python scripts/git_ops.py commit --workspace <path> --ticket <id> --stage <stage> --skill <skill> --role <role> --message "<msg>"
python scripts/git_ops.py branch --workspace <path> --name delivery/<ticket-id>
python scripts/git_ops.py push   --workspace <path>
python scripts/git_ops.py pull   --workspace <path>
python scripts/git_ops.py status --workspace <path>
python scripts/git_ops.py pr     --workspace <path> --title "<title>" --base main
```

### When to call it

Depends on configured granularity:

**per-skill (default):**
1. Agent pulls before starting a skill.
2. Agent commits after completing a skill (executor done or reviewer done).
3. Push immediately after commit.

**per-stage:**
1. Agent pulls before starting first skill in stage.
2. Delivery lead commits after all skills in stage complete.
3. Push on stage completion.

**per-ticket:**
1. Pull when ticket enters active.
2. Commit when ticket completes (all stages done) or scatters.
3. Push on ticket archive.

---

## PR behavior

PRs are **off by default**. When enabled:

| Trigger | PR scope | Base branch |
| --- | --- | --- |
| Ticket completes | Per ticket branch → main | `main` |
| Scope level completes | Per scope branch → main | `main` |
| User requests | Any current branch | `main` or specified |

Enable in `kanban.json`:

```yaml
git_policy:
  granularity: per-skill
  branch_scope: ticket
  pr_enabled: false
  push_on: skill_done
```

---

## Branch lifecycle (per-ticket branching)

```
main
 └─ delivery/inc-1              ← created when inc-1 enters active
      ├─ commit: inc-1.discovery.abd-domain-terms
      ├─ commit: inc-1.exploration.abd-domain-language
      ├─ commit: inc-1.exploration.abd-acceptance-criteria
      ├─ commit: inc-1.exploration.abd-ux-mockup
      └─ merge → main           ← when inc-1 scatters (or PR if enabled)
 └─ delivery/sprint-1           ← created when sprint-1 enters active
      ├─ commit: sprint-1.specification.abd-spec-by-example
      ├─ commit: sprint-1.engineering.abd-clean-code
      └─ merge → main           ← when sprint-1 completes
```

---

## Manifest git_policy section

```yaml
git_policy:
  granularity: per-skill | per-stage | per-ticket
  branch_scope: ticket | scope-level | none
  pr_enabled: true | false
  push_on: skill_done | stage_done | ticket_done
  pull_on: skill_start | stage_start | ticket_start
```

---

## Relationship to Kanban

Git operations are **driven by board state changes**:

| Board event | Git action |
| --- | --- |
| Ticket enters active | Pull, create branch (if branching enabled) |
| Skill completes (executor or reviewer) | Commit (+ push if per-skill) |
| Stage completes | Commit + push (if per-stage) |
| Ticket scatters or completes | Commit + push + merge branch (+ PR if enabled) |

The kanban lead scan cycle triggers git ops at the configured granularity. Role agents only commit; the lead manages branches and PRs.
