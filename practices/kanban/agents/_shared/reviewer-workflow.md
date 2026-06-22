# Reviewer workflow (shared)

**When:** your agent is a **reviewer** (`slot_type: reviewer`).

Announce each step. Reviewers validate — they do not produce new stage artifacts.

## Skills

| Skill | Use |
| --- | --- |
| `skill-helpers/` | workspace paths |
| Practice skill `SKILL.md` + `rules/` | read to **judge** |
| `common` / scanners | **yes** — run scanners |
| `track_task` | optional |

**Reviewers validate; executors produce.**

Stage definitions: [../../content/stages/README.md](../../content/stages/README.md)

## Checkpoint protocol

When a step says **CHECKPOINT**:

1. **Present** findings.
2. **Stop** and wait.
3. **On response:** confirm → proceed · correct → log · question → answer, re-present.

---

### Step 1 — Claim review from board

Read `board.json` and `system-of-work.json`. Find next eligible review per [work-queue.md](work-queue.md):

- Match your `team-role`
- Skill `status: done` AND `review_status: null`
- Prior skills in stage order are done
- Downstream stage priority

Claim: set `review_status: in_progress`, `reviewer: <your-role>`, `review_start: <now>`.

Announce: ticket ID, lineage, stage, skill being reviewed, executor who produced it.

### Step 2 — Load executor output

Read the artifacts produced by the executor for this skill. Identify file paths from workspace conventions and the skill's expected outputs.

### Step 3 — Read practice skill (judge)

Read the same practice skill's `SKILL.md` and `rules/` — but now to **validate** against the quality bar, not to author.

### Step 4 — Run scanners

Run scanners for the practice skill:

```bash
python skills/common/scripts/run_scanners.py \
    --skill-root <skill-name> \
    --workspace <workspace>
```

Record results. If scanner infrastructure fails (import errors, tracebacks, false clean), mark review as **blocked** — do not proceed.

### Step 5 — Review exit gate

Check the stage exit gate criteria from `stages/<stage>.md` for this skill's contribution:

- Artifacts match templates and rules
- Domain language is verbatim
- Traceability to stories/AC
- Scanner results are clean or violations explained

**CHECKPOINT.** Present findings:

- **PASS** — all rules pass, scanners clean
- **FAIL** — list specific violations with rule references

### Step 6 — Mark review complete and pull next

Update `board.json`:

- **PASS**: set `review_status: done`, `review_end: <now>`
- **FAIL**: set `review_status: failed` — this resets the skill's `status` to `to_do` for rework; log corrections in `docs/corrections-log.md`

Announce: review result on ticket/skill.

**Pull next eligible review** per [work-queue.md](work-queue.md). If nothing available, report idle.
