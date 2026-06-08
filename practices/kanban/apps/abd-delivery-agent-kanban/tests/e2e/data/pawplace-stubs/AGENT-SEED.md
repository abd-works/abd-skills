# Team member executor â€” fixture mode (read first)

You are a **team member agent** (`product-owner`, `business-expert`, `ux-designer`, or `engineer`) in a **fixture_mode** workspace. Your job is to **return harness values immediately** â€” not to run practice skills, scanners, or checkpoints.

## Turn 1 checklist

1. Read this file and `<workspace>/CONTEXT.md`.
2. Read `practices/kanban/agents/reference/session-bootstrap.md` â€” arm pull loop, resolve paths.
3. Read your role's `agents/<role>/AGENT.md` and `agents/reference/skill-fixture-mode.md`.
4. **Do not** open any practice skill `SKILL.md` or `rules/`.

## Per skill (fixture workflow)

### A â€” Claim or resume

```bash
python practices/kanban/skills/abd-kanban/scripts/board_skill.py pull \
  --workspace <workspace> --role <your-role>
```

Manual board drop: kanban-lead sets your skill `in_progress` first. `pull` returns `"action": "resume"` â€” use that ticket and skill.

### B â€” Apply harness (you run this â€” not kanban-lead)

**If you have ticket + skill from pull/resume:**

```bash
python practices/kanban/skills/abd-kanban/scripts/apply_skill_fixture.py apply \
  --workspace <workspace> --ticket <ticket_id> --skill <skill_name> --role <your-role>
```

**If manual drop already set `in_progress` and you only need to finish:**

```bash
python practices/kanban/skills/abd-kanban/scripts/apply_skill_fixture.py apply-claim \
  --workspace <workspace> --role <your-role>
```

This copies files from `skill-fixtures/` per `skill-fixtures.json`, runs graph sync CLI when listed, and marks the skill done (work + review) on `board.json`.

### C â€” Pull next

Run `board_skill.py pull` again. Repeat until no eligible work â†’ `board_skill.py ready`.

## DO NOT

- Read practice skills or run `run_scanners.py`
- Present Step 4 checkpoints to the operator
- Hand-edit `board.json` skill_progress
- Let kanban-lead apply fixtures for you â€” **team member executors own this path**

## Index

- Fixtures: `<workspace>/skill-fixtures.json`
- Sources: `<workspace>/skill-fixtures/`
- Board: `<workspace>/docs/kanban/board.json`
