# Progress checklists (live ticks)

This folder holds **session** `- [ ]` progress only. Normative methodology stays in the skill repository.

## Layout

| Path | Role |
|------|------|
| **`strategy-run-checklist.md`** | Which **phase-ids** you completed, in order, with **scope** (mirror **strategy.md** execution plan). |
| **`slices/<slice-id>/`** | One **folder per slice** from **strategy.md** §1. Each slice has **`<phase-id>-checklist.md`** files — action steps from that phase’s **## Action Checklist** in the skill. |
| **`process-checklist.md`** | Legacy: one row per phase in **phase_files**. Prefer **strategy-run-checklist** + **slices/** for OOAD work. |

## Commands

Create missing files when you run **`generate.py`** (unless **`--no-ensure-checklists`**):

```text
python scripts/base/generate.py --phase <phase-id> --slice <slice-id>
```

Default **`--slice`** is **`main`** (single-slice engagements). Multi-slice work: use the **same slice ID** as in **strategy.md** §1 for each pass.

**`--stage`** uses the same **`--slice`** for every phase in that stage.
