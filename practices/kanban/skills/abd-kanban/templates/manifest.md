# War Room Manifest

```yaml
goal: "<one-line engagement goal>"
strategy: "<strategy-name from abd-kanban-planning/strategies/>"
system_of_work: "<name from system-of-work.json definitions>"
autonomy: tight | moderate | full
checkpoint_policy: per_skill | per_stage | per_increment
scanner_infra_policy: block_chain_until_fixed
runtime: isolated-subagent
kanban:
  board_file: board.json
  sync_script: kanban/skills/abd-kanban/scripts/sync_kanban_board.py
  scatter_script: kanban/skills/abd-kanban/scripts/scatter_ticket.py
  metrics_script: kanban/skills/abd-kanban/scripts/track_metrics.py
wip_policy:
  product-owner:    { executor: 1, reviewer: 1 }
  business-expert:  { executor: 1, reviewer: 1 }
  ux-designer:      { executor: 1, reviewer: 1 }
  engineer:         { executor: 1, reviewer: 1 }
  max_active_tickets: 3
  scan_interval_seconds: 30
  stall_timeout_minutes: 15
```

## How it works

- **System of work** defines stages, scope per stage, and ordered skills.
- **Strategy** defines scatter rules, sprint grouping, JIT policy, and checkpoint timing.
- **Board** tracks tickets with per-skill progress (to_do, in_progress, done + review status).
- **Agents** pull skill-level work from active tickets matching their role.
- **Delivery lead** manages the board: advances tickets, triggers scatters, scales agent pool.

## Scatter rules

When a ticket's stage completes and the next stage has finer scope, the ticket scatters:

- Parent ticket is archived (with timing data)
- Children enter backlog at the finer scope level
- Children carry lineage from parent

See `strategy.md` for engagement-specific scatter heuristics.

## Notes

- No slot files — agents claim skills directly from board.json tickets.
- No pre-planned runs — strategy + system of work drives all flow.
- Delivery lead scan loop reads `wip_policy` every `scan_interval_seconds`.
- Role agents pull downstream-first (engineering > spec > explore > discovery > shaping).
- `max_active_tickets` limits how many tickets are in `active` simultaneously.
