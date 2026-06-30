# Deep Dive: Grill Skill

## Principles & Patterns

- **Opt-in grilling**: line 11 of `common/grill-me-with-practice-skill.md` says grilling is opt-in. The CDD orchestrator (`abd-context-driven-delivery/SKILL.md` line 65) overrides this by mandating grilling at every cell. The two signals can collide if a reader follows only the grill skill.
- **One question at a time** (line 19) is a hard rule with no detector.
- **"Read first, ask later"** (lines 21–22) lists sources without a procedure.
- **Question sources are listed** (lines 60–66): skill `## Grill prompts`, rule FAIL examples, existing outputs — but the agent is not told to **publicly answer each candidate question from these sources before surfacing to the user**.
- **No "grill before generate" forcing function**: there is no rule that flags "you started generating before grilling completed".

## File Structure

```
common/
└── grill-me-with-practice-skill.md   ← single file; 83 lines

practices/context-driven-delivery/skills/abd-context-driven-delivery/
└── SKILL.md
    └── §2 Walk the grid  (lines 56–117)  — refers to grill rules but does not duplicate them
```

## Participants

| Component | Role |
|---|---|
| `grill-me-with-practice-skill.md` | Source of grilling rules |
| Each practice skill's `## Grill prompts` section | Skill-specific input traps |
| Each practice skill's `rules/*.md` FAIL examples | Implicit grill question source |
| Existing workspace outputs | First-stop answer source |

## Flow

1. User invokes a skill with `grill me` (opt-in).
2. Agent reads `common/grill-me-with-practice-skill.md`.
3. Agent gathers questions from the skill's `## Grill prompts` and each `rules/*.md` FAIL example.
4. Agent **should** publicly attempt to answer each candidate question from rules + outputs first.
5. Agent surfaces unanswered questions one at a time.
6. Once enough is answered, the skill generates; grilling stops.

Steps 4 and 6 are where the session failures occurred.

## Walkthrough Example — pml-midtier session

Three distinct failure modes:

1. **Multiple questions at once**: the agent surfaced five numbered grill questions in a single response. The fix (per journal lines 145–147) is "ask one, wait, ask the next" — but no mechanism enforces it.

2. **Grill after generate**: the agent generated `docs/stubs/story-map.md` then raised a grilling concern afterwards. The fix (journal lines 125–127) is "grill before generate, not after" — also unenforced.

3. **Asked the user a question whose answer was in a rule's FAIL example**: when grilling for `abd-story-acceptance-test`, the agent could have publicly answered seven candidate questions from the skill's rules folder and existing AC outputs. Instead it surfaced them to the user. The fix (journal lines 198–208) demonstrates the corrected procedure — but no rule was written into the grill skill to require it.

All three failures are pure compliance gaps against rules that are *almost* present. They are exactly the kind of bug that strengthening the grill skill body (with a counter-check, an explicit "answer-yourself-first" procedure, and a "grilling-before-generate" forcing function) can prevent.
