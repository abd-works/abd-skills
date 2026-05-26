# Reviewer workflow (shared)

**When:** your agent is a **reviewer** (`slot_type: reviewer`).

You **validate only** — no new stage artifacts, no graph writes, no edits to executor files.

Shared definitions: [../../content/stages/README.md](../../content/stages/README.md) · war room: [../../skills/abd-delivery-war-room/SKILL.md](../../skills/abd-delivery-war-room/SKILL.md)

## Skills

| Skill | Purpose |
| --- | --- |
| Practice skill `SKILL.md` + `rules/` | read to **judge** |
| `execute-skill-using-skills-rules` | **run scanners** |
| `../../content/stages/<stage>.md` | exit-gate items scoped to the skill |
| `skill-helpers/` | workspace paths |

You do **not** use `story-graph-ops` or write new deliverables.

## Checkpoint protocol

1. **Present** findings and flag unknowns.
2. **Stop** and wait.
3. On confirm → finish slot · on correct → log corrections first, then re-review · on question → answer, re-present.

---

### Step 1 — Set up

Read `slot-NN-start.md`: `prior_executor_slot`, `artifact_paths`, `stage`, and **`skills`** (practice skill under review).

#### Which practice skill? (not from role playbook alone)

Your fixed **`team-role`** only decides **which reviewer slots you claim** — not which practice skill to run. Each slot names the skill explicitly:

1. **`skills:` on this reviewer `slot-NN-start.md`** — primary source; must match the paired executor slot (delivery lead copies the same skill name when authoring the plan).
2. **Fallback** — if `skills:` is empty (old war rooms only), read `skills:` from `slot-<prior_executor_slot>-start.md`.
3. **Resolve `--skill-root`** — `<workspace>/.cursor/skills/<skill-name>` (deployed skill package). Use the skill slug exactly as listed (e.g. `abd-clean-code`, `abd-acceptance-test-driven-development`).

[../../content/roles/team-roles.md](../../content/roles/team-roles.md) and your role playbook list skills that role **may** run across stages — that helps planning, not slot execution. **Never guess** the skill from role alone; always read the slot file.

Announce: reviewer slot **NN**, team-role, prior executor slot id, **practice skill name and resolved path**.

### Step 2 — Load executor output

Read prior executor `slot-<prior>-finished.md` and **every** artifact path. Missing → `slot-NN-blocked.md` and stop.

### Step 3 — Read practice skill (review criteria)

Read the same practice skill's `SKILL.md` and **rules** to **judge** artifacts (DO / DO NOT per rule).

### Step 4 — Run scanners

```bash
python skill-helpers/skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
    --skill-root <practice-skill-path> \
    --workspace <workspace-path>
```

Add `--language javascript` or `--language typescript` when required.

Record pass/fail per rule in finished file.

#### Scanner infrastructure failure (mandatory FAIL — stop)

If subprocess stderr contains `Traceback`, `ImportError`, or `ModuleNotFoundError`; report says ALL CLEAN but scanners crashed; `[INFO] No scanners found` when rules exist; or summary shows `[MISSING/CRASH]`:

1. Set **All scanners: FAIL** and **Overall gate: FAIL**.
2. List **Blockers: scanner infrastructure** with command and error excerpt.
3. Write `slot-NN-blocked.md` if the lead should halt (`blocker_type: scanner-infra`).
4. **Stop** — do not fix executor artifacts.

#### Scanner obviously not relevant (narrow exception)

After scanners **execute**, if a rule fails but is **obviously inapplicable** to this slot:

1. Record **Scanner exception** in finished file: scanner/rule name, why irrelevant, what still passes.
2. Set **Overall gate: PASS with documented scanner exception** only if exit-gate items still pass without that rule.
3. If arguable, **FAIL**.

Import crashes and false ALL CLEAN are **never** eligible.

### Step 5 — Review against exit gate

Read `../../content/stages/<stage>.md` — exit-gate items scoped to this skill. Numbered findings: what · where · why · rule.

**CHECKPOINT** if findings are large or ambiguous.

### Step 6 — Finish reviewer slot

Write `slot-NN-finished.md` using **`slot-finished-reviewer.md`** template:

- Scanner results (Step 4)
- Gate review (Step 5)
- **Suggested fixes** for rework, or **clean pass**

Remove `slot-NN-claim.md`. **Claim the next eligible slot** per [work-queue.md](work-queue.md). Board sync moves ticket toward **done** or next stage **in_progress**.

**When blocked:** write `slot-NN-blocked.md` — ticket column **`blocked`**. Do not produce new stage artifacts when blocked.

Announce: **Reviewer slot NN complete** — ticket column updates on **`sync_kanban_board.py`**.

Announce: **Review complete — pass** or **rework required** (N findings).

Do **not** fix executor artifacts. The delivery lead logs corrections and opens a **rework executor** slot when needed.
