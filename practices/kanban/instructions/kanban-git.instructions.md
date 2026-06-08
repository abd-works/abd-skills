# Kanban Git Instructions (always-on)

Use this rule whenever work is being executed from a Kanban board ticket.

## Activation conditions

Apply when any of the following is true:

- The **Kanban app** is the active execution context.
- A **kanban-family skill** is driving work.
- Ticket **state**, **stage**, or **scope** can be inferred from available context.

If the context is ambiguous, ask one clarification question before performing git actions.

## Core rule

Git activity is driven by **ticket lifecycle events** (skill start/done, stage done, ticket done/scatter), not by ad-hoc timing.

Read the full policy, commit format, branching strategy, and PR behavior from **[`abd-kanban-repo/SKILL.md`](../skills/abd-kanban-repo/SKILL.md)**.

If `kanban.json` contains `git_policy`, follow it. Otherwise use the defaults in the skill.

## Do not apply this rule when

- Work is outside Kanban delivery flow.
- No board/ticket context exists.
- Policy explicitly disables Git orchestration.
