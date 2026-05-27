---
name: track-task
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Checkbox markdown task lists for pipelines or ad-hoc steps under the engagement workspace.
description: Track multi-step work with markdown checkboxes (- [ ] / - [x]) for any skill or agent—pipeline phases, per-phase steps, or ad-hoc lists—under the engagement workspace, without editing normative skill sources.
---

# Track task (checkbox progress)

Use this skill when the user (or another skill) needs to **track execution** of a workflow: **what step are we on?**, **mark this done**, **track skill A and skill B together**, **resume after a break**.

## When to activate

- User says: *track this*, *checkpoint*, *what’s next*, *mark step N done*, *track [skill name]*, *progress on …*
- You are orchestrating **one or more** leaf skills and must persist **session** state as checkboxes, not by editing `content/parts/process.md` or phase source files.

## What you do (agent behavior)

1. **Resolve the engagement root**  
   Read **`skill-config.json` → `workspace.active_skill_workspace`** on the **agent** (or skill) root. If missing, **set workspace first** (see **`skill-helpers/`** — **`workspace.prompt.md`** / **`python skill-helpers/scripts/set_workspace.py`**).

2. **Pick what to track**  
   - **Whole pipeline (abd-skill-builder style skill):** phases from **`skill-config.json` → `phase_files`** and/or rows in **`content/parts/process.md`**.  
   - **Single phase:** steps from **`## Action Checklist`** or any `- [ ]` / `- [x]` lines in **`content/parts/phases/<slug>.md`**.  
   - **Ad-hoc / non-builder skill:** build a numbered checklist from **`SKILL.md`**, README, or explicit user steps.

3. **Write only to live progress files**  
   Normative docs stay clean. Session ticks live under:

   ```text
   <active_skill_workspace>/<skill_name>/progress/
     process-checklist.md          # one line per phase (pipeline position)
     <phase-slug>-checklist.md      # steps inside that phase
   ```

   For **builder skill packages**, prefer **`python scripts/base/generate.py --phase <slug>`** to create those files when the target skill ships **`scripts/base/`** (see **Builder skill packages** below). If there is **no** `generate.py`, create the same paths **manually** (same checkbox format).

4. **Multiple skills**  
   One **`<skill_name>/progress/`** tree per tracked skill. Do not merge unrelated pipelines into one file unless the user asks.

5. **Each turn**  
   - Open the relevant **`progress/*.md`** file(s).  
   - **First unchecked** `- [ ]` is “next” unless the user names a step.  
   - After work completes, flip **only** that line to `- [x]`.  
   - Summarize: done / next / blocked.

## Tracking contract (detail)

**Goals:** Observable `- [ ]` / `- [x]` progress; **no** session edits to normative `content/parts/process.md` or `content/parts/phases/*.md`; same idea for builder packages, minimal skills, and agent-only repos.

**Workspace:** **`active_skill_workspace`** = engagement tree (not the skill install). **`skill_name`** = `skill-config.json → name` if set, else the skill directory name. Live files: **`<workspace>/<skill_name>/progress/`**.

**File kinds**

| File | Tracks |
| --- | --- |
| **`process-checklist.md`** | Which phase (one `- [ ]` line per phase) |
| **`<phase-slug>-checklist.md`** | Steps inside that phase (from **`## Action Checklist`** or task lines in the phase doc) |

**Rules**

1. Create missing **`progress/`** files when the user agrees to start; do **not** overwrite existing checklists unless they ask to reset.  
2. **Next step** = first unchecked item in scope.  
3. **Multi-skill:** separate **`progress/`** per skill; optional roll-up **`tracking-summary.md`** at workspace root only if requested.  
4. **No `skill-config.json`:** use **`<workspace>/_tracking/<id>/checklist.md`** (`id` = label or folder name).

**Anti-patterns:** ticking boxes inside **`content/parts/**`** sources; tracking only in chat when the user wanted files across sessions.

## Builder skill packages

If the **tracked** skill has **`scripts/base/generate.py`** and **`workspace_checklists.py`**:

1. Set **`workspace.active_skill_workspace`** for that skill (or wrapping agent).  
2. Run **`python scripts/base/generate.py --phase <slug>`**.  
3. First run may create **`process-checklist.md`** and **`<slug>-checklist.md`** under **`…/<skill_name>/progress/`**.

Exact creation rules: **`workspace_checklists.py`** and **`content/parts/library/base/checklist.md`** in **abd-skill-builder**. This skill **updates** those files after they exist; it does not replace **`generate.py`**. For prompt-only, no new checklists: **`--no-ensure-checklists`**.

## Commands (optional helpers)

From **agent root** (parent of `skills/`):

```bash
python skill-helpers/skills/track_task/scripts/progress_path.py
python skill-helpers/skills/track_task/scripts/progress_path.py --skill my-other-skill
```

Prints **`…/<skill_name>/progress`** for the configured workspace.

## `abd-delivery-lead` (agent checklist)

When the **abd-delivery-lead** agent tracks work, progress lives in the **war room**:

```text
<active_skill_workspace>/docs/planning/delivery-war-room/delivery-plan-checklist.md
<active_skill_workspace>/docs/planning/abd-delivery-lead/agile-delivery-plan.md
```

**`agile-delivery-plan.md`** — canonical **narrative** plan. **`delivery-plan-checklist.md`** — orchestration mirror **auto-synced from `run-log.jsonl`**. **Slot truth** = `slot-NN-finished.md`.

**Per-stage lines (generated):** executor → reviewer (scanners + exit-gate as separate checkboxes) → rework → delivery-lead gate. Sync ticks whole stage blocks when `stage_exit_gate` / `run_complete` land in the log.

**Commands** (from agilebydesign-skills repo root):

```bash
# Plan confirm / revision — regenerate structure + sync from log:
python skill-helpers/skills/track_task/scripts/generate_delivery_checklist.py --workspace <workspace>

# After every stage_exit_gate or run_complete (mandatory for delivery-lead):
python skill-helpers/skills/track_task/scripts/generate_delivery_checklist.py --sync-only --workspace <workspace>
```

Run full generate after **Step 2** and **Step 7**. Run **`--sync-only`** after **every stage exit gate** and **run complete**.

---

## See also

- **`skill-helpers/`** — set **`active_skill_workspace`** before tracking (`python skill-helpers/scripts/set_workspace.py`).
- **`delivery/agents/delivery-lead/AGENT.md`** — orchestration steps and when to populate the checklist.
