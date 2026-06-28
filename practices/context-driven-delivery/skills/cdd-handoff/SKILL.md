---
name: cdd-handoff
catalog_garden_tier: practice
catalogue_one_liner: >-
  CDD session handoff — appends a resume marker to the checklist so a fresh agent knows exactly where to pick up.
description: >-
  No separate file. Appends a RESUME POINT block to the active cdd-session-checklist.md with a 3-line summary, open items, and a pointer to the journal. A fresh agent opens the checklist, hits the marker, reads the journal, and continues.
argument-hint: "What will the next session focus on? (optional)"
---

# cdd-handoff

## Purpose

Let a fresh agent resume a CDD session without re-reading the full repo or re-interviewing the user. The checklist already knows where the session stopped; the journal already has grill answers and corrections. The handoff marker ties them together at the point of pause — no third document needed.

---

## Output

No new file. Append a `## ↓ RESUME POINT` block to the bottom of:

```text
<workspace>/docs/cdd-sessions/<YYYY-MM-DD>-<topic>/cdd-session-checklist.md
```

---

## Process

### 1. Locate the active session

Look for `docs/cdd-sessions/` at the workspace root. The most recently modified subfolder is the active session. Read:

| File | What to use it for |
|---|---|
| `cdd-session-checklist.md` | Which cells are done `[x]` / pending `[ ]` / skipped; where to append the marker |
| `cdd-session-journal.md` | Grill Q→A answers, `Ran` lines, Corrections — confirm what's already captured |
| `cdd-context-index.md` (workspace root) | Non-standard artifact paths |

If no session folder exists, derive state from changed files and conversation.

### 2. Resolve the resume state

From the checklist and journal:

- **Last completed cell** — last `[x]` line and its output path
- **Next cell** — first `[ ]` line and its skill name, or "session complete" if all `[x]`
- **Scope** — from journal entry point, `cdd-context-index.md`, or conversation
- **Open items** — anything not captured in the checklist or journal (deferred work, known gaps, out-of-grid changes)

### 3. Append the resume marker

Add this block to the **bottom** of `cdd-session-checklist.md`:

```markdown
---

## ↓ RESUME POINT — handed off {YYYY-MM-DD}

**Stage × Perspective × Scope:** {stage} · {perspective} · {scope}
**Last ran:** {skill name} → {output path} → {accepted | needs revision}
**Next:** {skill name and SKILL.md path, or "start a new CDD session"}

**Open items:**
- {item 1 — deferred work, known gap, or risk not captured above}
- {item 2}

**Out-of-grid changes this session:**
- {framework or skill changes made outside the delivery grid, if any}

Read `cdd-session-journal.md` for grill answers, corrections, and Ran lines.
```

Omit any section that has nothing to say. If there are no open items, omit that block. If there are no out-of-grid changes, omit that block.

### 4. Tell the user

Reply with the **three-line resume** and confirm the marker was appended:

1. Current stage × perspective × scope
2. Last skill run and whether it was accepted
3. Next skill to run (or "session complete — start a new CDD session")

---

## Where to start (the marker must answer)

| Situation | Start here |
|---|---|
| Checklist has unchecked `[ ]` cell with skill name | Run that skill; pass journal Q→A as context |
| Last `Ran` line says "needs revision" | Re-run that same skill with Corrections appended |
| All cells `[x]`, marker says "session complete" | Start `abd-context-driven-delivery` for the next scope |
| No checklist found | Start `abd-context-driven-delivery` from scratch; assess entry point |

---

## Validate

- [ ] Active session checklist found and read
- [ ] Resume marker appended at bottom of checklist
- [ ] Three-line resume is explicit — no "unknown" fields
- [ ] Open items captured (or explicitly omitted as empty)
- [ ] Journal pointer included in the marker
