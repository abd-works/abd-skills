# Reviewer workflow

The app assigns you a skill to review. You validate — and **fix simple issues in place** rather than bouncing them back to the executor.

**Reviewers validate; executors produce.** Fix simple, mechanical issues (missing stub, typo, formatting, unresolved reference) directly and mark PASS. Only mark FAIL for **substantive problems** (wrong domain model, missing Key Abstraction, incorrect invariants, structural redesign).

## Checkpoint protocol

When a step says **CHECKPOINT**:

1. **Present** findings.
2. **Stop** and wait.
3. **On response:** confirm → proceed · correct → log · question → answer, re-present.

---

### Step 1 — Load executor output

Read the artifacts produced by the executor for this skill. Identify file paths from workspace conventions and the skill's expected outputs.

### Step 2 — Read practice skill (judge)

Read the same practice skill's `SKILL.md` and `rules/` — to **validate** against the quality bar, not to author.

### Step 3 — Run scanners

```bash
python skills/common/scripts/run_scanners.py \
    --skill-root <skill-name> \
    --workspace <workspace>
```

Record results. If scanner infrastructure fails, mark review as **blocked**.

### Step 4 — Review exit gate

Check the stage exit gate from [stages/](./stages/) for this skill's contribution.

**CHECKPOINT.** Present findings:

- **PASS** — all rules pass, scanners clean
- **FIX-IN-PLACE** — simple mechanical issues found. Fix, re-run scanners, mark PASS.
- **FAIL** — substantive violations requiring executor rework

### Step 5 — Fix simple issues in place (when applicable)

1. Make the fix.
2. Re-run scanners to confirm resolution.
3. Log in `docs/corrections-log.md`.
4. Mark review as **PASS**.

**Simple** means: the fix requires no domain judgment. If choosing between modeling alternatives — mark FAIL.

### Step 6 — Signal review result

- **PASS** (including fix-in-place): signal done to the app.
- **FAIL**: signal failed — log corrections in `docs/corrections-log.md`.
