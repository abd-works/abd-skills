# Skill fixture mode — return immediately (E2E / handoff testing)

When `<workspace>/CONTEXT.md` contains **`fixture_mode: true`**, agents **must not** read practice skill `SKILL.md`, run scanners, or generate new content. Copy pre-baked fixtures and mark the skill done.

## Detect fixture mode

1. Read `<workspace>/CONTEXT.md` — look for `fixture_mode: true`.
2. Read `<workspace>/skill-fixtures.json` — index of every skill and target paths.

If both exist → **fixture mode is active** for this engagement.

## Workflow (replaces executor-workflow Steps 3–6)

After `board_skill.py pull` claims a skill (or returns `"action": "resume"` from a manual board drop):

1. **Run the fixture CLI** (team member executors — not kanban-lead):

   ```bash
   python practices/kanban/skills/abd-kanban/scripts/apply_skill_fixture.py apply \
     --workspace <workspace> --ticket <id> --skill <name> --role <your-role>
   ```

   Manual drop already set `in_progress`:

   ```bash
   python practices/kanban/skills/abd-kanban/scripts/apply_skill_fixture.py apply-claim \
     --workspace <workspace> --role <your-role>
   ```

   Or follow steps 2–6 below manually if the CLI is unavailable.

2. **Lookup** the skill in `skill-fixtures.json` → `fixtures[<skill-name>]`.
2. Pick the entry matching ticket **scope** (`all`, `increment`, `sprint`) or `default`.
3. **Copy** each `source` file under `<workspace>/` to its `target` path (create parent dirs if missing).
4. Run **`post_copy`** CLI commands listed on the entry (graph sync only — no scanners).
5. **`board_skill.py complete`** twice (work_done → review done) with `--notes "fixture_mode: copied from skill-fixtures"`.
6. **Pull next** — do not checkpoint with the operator.

### DO NOT in fixture mode

- Read the practice skill's `SKILL.md` or `rules/`
- Run `run_scanners.py`
- Present Step 4 checkpoint to the operator
- Queue Draw.io background sync (optional — skip for speed)
- Regenerate or "improve" fixture content

### DO in fixture mode

- Copy bytes exactly from fixture sources
- Run graph sync commands when the fixture entry lists them
- Mark skill done via `board_skill.py` only
- Log `{"event":"skill_fixture_applied","skill":"...","ticket":"..."}` to `metrics-log.jsonl`

## Kanban lead in fixture mode

Same scatter/advance rules as normal. **Do not apply fixtures yourself** — spawn team member role agents; they run `apply_skill_fixture.py`. When spawning, append to the spawn prompt (or rely on `run_kanban_lead_tick.py` auto-injection):

```text
FIXTURE MODE: workspace has fixture_mode: true. Team member executor — read AGENT-SEED.md.
Run apply_skill_fixture.py after pull; do not execute practice skills.
```

## Fixture package location

E2E seed: `tests/e2e/_seed/pawplace-stubs/` — reset live workspace with `scripts/reset-e2e-fixture.ps1 -Fixture pawplace-stubs`.
