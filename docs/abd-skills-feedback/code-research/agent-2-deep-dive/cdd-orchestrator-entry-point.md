# Deep Dive: CDD Orchestrator Entry Point

## Principles & Patterns

- **Routing-as-prose**: the entry-point algorithm is encoded as a Markdown checklist in the orchestrator skill, not as runnable logic. Compliance is contractual.
- **Workspace-tree-first detection**: the algorithm prefers reading `cdd-context-index.md`, the scaffold tree under `docs/`, and `skill-index.md` outputs. It does not read the user's opening message for attached-skill signals.
- **Stage gradient assumes greenfield-to-engineering**: the six entry-point conditions (lines 47–53) walk from "no source material" → "specification done, code needed". The "existing running app" case is not first-class.
- **Self-correction is real-time but not retroactive**: `cdd-self-correction.instructions.md` enforces logging when a user signals a wrongness now. There is no equivalent "load existing journal corrections as immediate constraints on resume" rule.

## File Structure

```
practices/context-driven-delivery/
├── skills/
│   ├── abd-context-driven-delivery/SKILL.md     ← orchestrator; entry-point algorithm in §1
│   └── cdd-handoff/SKILL.md                    ← session-pause; appends RESUME POINT block
├── prompts/
│   └── cdd-resume.prompt.md                     ← session-resume; reads checklist + journal
└── instructions/
    └── cdd-self-correction.instructions.md       ← real-time correction logging
```

## Participants

| Component | Role | Reads | Writes |
|---|---|---|---|
| `abd-context-driven-delivery` SKILL.md | Orchestrator | workspace tree, skill-index.md, folder-conventions.md | cdd-session-checklist.md, cdd-session-journal.md |
| `cdd-handoff` SKILL.md | Session-pause | checklist + journal | RESUME POINT block in checklist |
| `cdd-resume.prompt.md` | Session-resume | checklist + journal | continues from first unchecked cell |
| `cdd-self-correction.instructions.md` | Correction-logging | user signal | `## Corrections` in journal |

## Flow

1. User triggers a CDD session (with or without context).
2. Orchestrator scans workspace tree per `### 1. Assess entry point`.
3. Orchestrator recommends a stage from the six-condition list and asks the user to confirm.
4. User confirms (or corrects, as happened in the pml-midtier session).
5. Orchestrator walks the fidelity-level × perspective grid; spawns specialists; runs consistency checks.
6. On pause: `cdd-handoff` appends a RESUME POINT block to the checklist.
7. On resume: `cdd-resume.prompt.md` reads the checklist + journal and continues from the first unchecked cell. Existing `## Corrections` entries are not enumerated as preflight.

## Walkthrough Example — pml-midtier reverse-engineer session

A user opened a session against `pml-midtier` (an existing midtier API with a running app and `docs/external/code-research/` already present). They attached `abd-context-app-sandbox` to the opening message.

**What happened (wrong):** the orchestrator scanned `docs/` , found `docs/external/code-research/agent-1-explorer/`, mapped it onto "scope defined → discovery", and recommended **Discovery**. The attached skill was ignored. The user had to manually challenge "why didn't you suggest setting up a sandbox and then extracting?" before the orchestrator corrected to **Context**.

**What should have happened:** the orchestrator should have (a) noticed the attached `abd-context-app-sandbox` skill, (b) checked whether `docs/external/app-extraction/` existed, (c) recognized this as an existing-app-without-extraction case, (d) recommended **Context** (sandbox + extract) as the entry point.

Later in the same session, the user paused. On resume, the journal already had several `## Corrections` entries including "DO NOT grill after generating" and "DO NOT use docs/sessions/ — use docs/cdd-sessions/". The resuming agent read the handoff, acknowledged the corrections in prose, then immediately began generation in the same turn — violating the first correction. The resume prompt did not have a rule that says "every correction is in force from response 1; list them as a numbered preflight before any work".
