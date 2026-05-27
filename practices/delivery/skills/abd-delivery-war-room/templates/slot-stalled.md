# Slot NN — Stalled

**Timestamp:** <ISO 8601>
**Stage:** <stage name>
**Role:** <team-role>
**Ticket:** Run <N> — <column was in_progress | review>

## Stall signal

Claim open longer than `manifest.md` `stall_timeout_minutes` without `slot-NN-finished.md`.

```yaml
claimed_by: <agent slug>
claimed_at: <ISO 8601 from slot-NN-claim.md>
stall_detected_at: <ISO 8601>
stall_timeout_minutes: <from manifest>
```

## Last known activity

<What the agent was doing — slot scope, skill, artifact paths touched>

## Delivery lead actions

1. Nudge or re-spawn isolated subagent for `<role>`.
2. Clear stall via `slot-NN-answer.md` or finish/blocked path.
3. Re-run `sync_kanban_board.py` — ticket column returns to `in_progress` or `review`, or moves to `blocked`.

## Relevant artifacts

| Artifact | Path | State |
|----------|------|-------|
| Claim | slot-NN-claim.md | open |
| Start | slot-NN-start.md | — |
