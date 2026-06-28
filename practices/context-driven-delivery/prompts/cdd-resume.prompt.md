---
description: >-
  Resume an existing CDD session. Reads the checklist and journal to find
  where work stopped, then continues from that point using full skill protocol.
agent: agent
---

# Resume CDD Session

You are resuming a context-driven delivery session that was previously handed off.

---

## 1. Read the skill

Read **`abd-context-driven-delivery`** (`practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md`) in full — including grill-me rules, skill index, folder conventions, and stage navigation.

---

## 2. Locate and read the session

Find the session checklist the user referenced (or the most recently modified `docs/cdd-sessions/*/cdd-session-checklist.md`).

Read these files in order:

| File | Purpose |
|---|---|
| `cdd-session-checklist.md` | Grid state — what's done `[x]`, what's next `[ ]`, resume point |
| `cdd-session-journal.md` | Grill Q→A history, `Ran` lines, corrections — know what was already answered |
| `cdd-context-index.md` (workspace root) | Non-standard artifact paths |

---

## 3. Find the resume point

Look for the `## ↓ RESUME POINT` marker at the bottom of the checklist. It tells you:

- **Stage × Perspective × Scope** — where you are on the grid
- **Last ran** — which skill completed last and whether it was accepted
- **Next** — which skill to run next (or "session complete")
- **Open items** — deferred work, known gaps

If there is no resume marker, use the first unchecked `- [ ]` line as the current step.

---

## 4. Resume — follow full protocol

From the resume point, continue `abd-context-driven-delivery` workflow:

1. **Navigate** — use the checklist to identify the current cell (stage × perspective).
2. **Grill** — read the skill's grill prompts; check the journal for already-answered questions; only ask what's unanswered.
3. **Read the appropriate skill** — look up the exact skill from the checklist item (each item names its skill), read its full SKILL.md.
4. **Route** — spawn the specialist subagent with role + skill + all prior context + journal answers.
5. **Validate** — after output, run consistency checks per the CDD skill.
6. **Mark done** — flip `- [ ]` to `- [x]` in the checklist.
7. **Advance** — move to the next cell or perspective.

**Do not skip steps.** Do not self-generate — spawn specialists. Do not assume answers — check the journal first, then grill.

---

## 5. Session state management

- Update the checklist after each completed cell.
- Append to the journal with `Ran` lines and any new grill Q→A.
- If the user provides corrections, add them to the journal `## Corrections` section and re-run the affected cell.

---

## Quick reference — where to start

| Situation | Action |
|---|---|
| Resume marker says "next: `<skill>`" | Read that skill, grill if needed, run it |
| Last `Ran` says "needs revision" | Re-run that skill with corrections appended |
| All cells `[x]`, "session complete" | Tell the user; offer to start a new CDD session |
| No checklist found | Start `abd-context-driven-delivery` from scratch |
