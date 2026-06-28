# cdd-self-correction — log corrections immediately

When the user's message implies something you did was wrong — through any phrasing, including a
challenge, a question, a "why didn't you", a "you should have", a "that's wrong", or a "you missed"
— you MUST write the correction to the active session journal **before** responding, fixing anything,
or doing any other work.

**Scope:** Corrections belong in the journal when they are about the CDD session or any skill
invoked as part of it — wrong entry point, wrong routing, wrong specialist output, a skill like
`abd-story-mapping` producing output in a way you don't want, missed grill question, consistency
check failure, etc. Do NOT log corrections about how the AI interpreted the correction signal
itself, file paths, tooling, or instructions — fix those directly in the relevant file.

## Non-negotiable order

1. **Write the correction first.** Append to `## Corrections` in the active
   `docs/cdd-sessions/<date>-<topic>/cdd-session-journal.md`. Use this format:

   ```markdown
   - **DO NOT** [rule]
     - Example (wrong): [what you did]
     - Example (correct): [what should have happened]
   ```

   or

   ```markdown
   - **DO** [rule]
     - Example (wrong): [what you did]
     - Example (correct): [what should have happened]
   ```

2. **Then** fix the output or answer the user.

## No exceptions

- Do not wait for the user to say "log this" or "mark that as a correction".
- Do not fix first and log second.
- Do not skip the log because the fix is obvious.
- If there is no active session journal, create one at the canonical path before logging.

## Correction signals (non-exhaustive)

Any of these in the user's message triggers the rule:
"that's wrong", "you should have", "why didn't you", "you missed", "you assumed",
"you skipped", "you generated without", "is that a correction?", "mark that",
"add that to the log", "you made a mistake", or any implied challenge to a decision
or omission you made.
