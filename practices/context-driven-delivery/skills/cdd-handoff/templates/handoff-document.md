# CDD Handoff

**Generated:** <ISO date>
**Session folder:** `<workspace>/docs/cdd-sessions/<YYYY-MM-DD>-<topic>/`
**Journal:** `cdd-session-journal.md` — read this first to restore grill context
**Checklist:** `cdd-session-checklist.md` — first unchecked `[ ]` is the next cell
**Saved to:** `cdd-handoff-<YYYY-MM-DD>.md` (and `cdd-handoff-latest.md`)
**Next session focus:** <from user argument or "not specified">

---

## Resume in three lines

1. **Stage × Perspective × Scope:** <e.g. Exploration · Stories · Voucher Redemption epic>
2. **Last ran:** `<skill>/SKILL.md` → `<output path>` — accepted / needs revision
3. **Start here:** run `<exact-skill/SKILL.md>` — <one sentence on what it produces>

---

## Session entry point

- **Confirmed entry point:** <fidelity level> — <reason user confirmed>
- **Scope:** <epic name / feature / thin slice / all>

---

## Checklist state

Copy the checklist grid here (abridged — done rows collapsed, pending rows in full):

```
- [x] Entry point confirmed: <fidelity> — <reason>
- [x] Shaping: Domain — abd-domain-glossary/SKILL.md
- [x] Shaping: Stories — abd-story-mapping/SKILL.md (outline)
- [ ] Shaping: UX — abd-ux-user-impact-map/SKILL.md          ← NEXT
- [ ] Shaping: Architecture — abd-architecture-outline/SKILL.md
- [ ] Consistency check — Shaping
...
```

---

## Artifacts produced this session

| Stage | Perspective | Skill run | Output path | Status |
|---|---|---|---|---|
| <stage> | <perspective> | `<skill>/SKILL.md` | `<path>` | accepted / needs revision |

---

## Grill answers (carry forward)

Key Q→A pairs from the journal — enough context for the next agent to skip re-asking:

- Q: <question> → A: <answer>
- Q: <question> → A: <answer>

---

## Corrections in force

DO / DO NOT rules added this session (carry these into the next spawn):

- **DO NOT** <rule>
  - Example (wrong): ...
  - Example (correct): ...

---

## Open questions / risks

- <unresolved item with enough context to resume>

---

## Non-standard paths (from cdd-context-index.md)

| Artifact | Actual path |
|---|---|
| <artifact> | `<path>` |

---

## Commands to resume

```powershell
# Open session journal
code "docs/cdd-sessions/<YYYY-MM-DD>-<topic>/cdd-session-journal.md"

# Open checklist
code "docs/cdd-sessions/<YYYY-MM-DD>-<topic>/cdd-session-checklist.md"
```

**Next skill to run:** `<exact-skill-name>/SKILL.md`
Spawn with: role (`<perspective> AGENT.md`) + skill + journal Q→A answers above + Corrections above.
