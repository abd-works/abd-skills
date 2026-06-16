# Delivery Agent Kanban — Python domain layer

Canonical implementation of the domain model in `docs/domain/domain model.md` and `docs/domain/domain model-class-diagram.drawio`.

| Module | domain model concepts |
| --- | --- |
| `delivery_model.py` | KanbanBoard, Ticket, BoardPosition, SkillProgress, Stage, StageWorkRequired, Skill, TeamMembership, Heartbeat helpers |
| `board_mode.py` | Board mode (automatic / manual) |
| `action_state.py` | ActionIntent, action-state file |

Agent orchestration (`kanban_lead.py`, `agent.py`, `kanban_cli.py member`) stays in `practices/kanban/skills/abd-kanban/scripts/` and imports this package through thin shims (`delivery_model.py`, etc.).

**Tests:** `npm run test:domain` from the app root.
