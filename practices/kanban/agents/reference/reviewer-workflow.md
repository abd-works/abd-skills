# Reviewer workflow (shared)

**Shared kanban concepts**: [../../reference/kanban-board.md](../../reference/kanban-board.md) · [../../reference/agents-and-skills.md](../../reference/agents-and-skills.md)

**When:** your agent is a **reviewer** (`work_role: reviewer`).

Announce each step. Reviewers validate — and **fix simple issues in place** rather than bouncing them back to the executor.

## Skills

- **`skill-helpers/`** — workspace paths
- **Practice skill `SKILL.md` + `rules/`** — read to **judge**
- **`execute-skill-using-skills-rules` / scanners** — **yes** — run scanners
- **`track_task`** — optional

**Reviewers validate; executors produce.** When a reviewer finds a **simple, mechanical issue** (missing stub, typo, formatting, unresolved reference), the reviewer fixes it directly and marks the review as PASS. Only mark FAIL and bounce to executor for **substantive problems** (wrong domain model, missing Key Abstraction, incorrect invariants, structural redesign).

Stage definitions: [../../reference/stages/README.md](../../reference/stages/README.md)

## Checkpoint protocol

When a step says **CHECKPOINT**:

1. **Present** findings.
2. **Stop** and wait.
3. **On response:** confirm → proceed · correct → log · question → answer, re-present.

---

### Step 1 — Start review from board

Read `board.json` and `kanban.json`. Find next eligible review per [work-queue.md](work-queue.md):

- Match your `delivery-role`
- `execution_status: done` AND `review_status: null`
- Prior skills in stage order are done
- Downstream stage priority

Start review: set `review_status: in_progress`, `reviewer: <your-role>`, `review_start: <now>`.

Announce: ticket ID, lineage, stage, skill being reviewed, executor who produced it.

### Step 2 — Load executor output

Read the artifacts produced by the executor for this skill. Identify file paths from workspace conventions and the skill's expected outputs.

### Step 3 — Read practice skill (judge)

Read the same practice skill's `SKILL.md` and `rules/` — but now to **validate** against the quality bar, not to author.

### Step 4 — Run scanners

Run scanners for the practice skill:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
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
- **FIX-IN-PLACE** — simple, mechanical issues found (missing stub, typo, formatting, unresolved reference). Reviewer fixes them directly, then marks PASS.
- **FAIL** — substantive violations requiring executor rework (wrong model, missing abstraction, incorrect invariants, structural redesign)

### Step 5a — Fix simple issues in place (when applicable)

If the only violations are **simple and mechanical** — missing boundary stubs, unresolved italic terms, formatting errors, typos, missing labels — the reviewer fixes them directly in the artifact file:

1. Make the fix.
2. Re-run scanners to confirm the fix resolves the violation.
3. Log the fix in `docs/corrections-log.md` (what was wrong, what was fixed).
4. Mark review as **PASS** (not FAIL) — the skill does not need rework.

**Simple** means: the reviewer can confidently make the correct fix without domain judgment calls. If the fix requires choosing between modeling alternatives, it is not simple — mark FAIL.

### Step 6 — Mark review complete and pull next

Update `board.json`:

- **PASS** (including fix-in-place): set `review_status: done`, `review_end: <now>`
- **FAIL**: set `review_status: failed` — this resets the skill's `execution_status` to `not_started` for rework; log corrections in `docs/corrections-log.md`

Announce: review result on ticket/skill.

**Pull next eligible review** per [work-queue.md](work-queue.md). If nothing available, report idle.
