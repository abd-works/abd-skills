# Record Architecture Violations

> **Read gate — CURRENT STATE ONLY.**
> Read this file ONLY when you are documenting an **existing** system — rendering what code already does, not designing what new code should do. If the skill is producing a greenfield design, stop here and do not read further.

---

## Violation categories in scope

Only three categories qualify. Do not record anything outside them.

| Category | What it is | Examples |
|---|---|---|
| **Pattern deviation** | Code that crosses a boundary the architecture defines — wrong layer, wrong direction, wrong owner | Direct `process.env` access outside the Config module; business logic in a React component; a domain service importing from an HTTP adapter |
| **Orphan concern** | A cross-cutting concern with no mechanism and no named owner — it exists but nothing in the architecture claims it | Auth token refresh logic spread across three unrelated files; retry logic duplicated per-module with no shared owner |
| **Missing mechanism** | A cross-cutting concern the system needs but the architecture does not describe at all | No error boundary mechanism when the app has multi-step flows; no feature-flag mechanism when the product ships experiments |

If you observe a security risk, NFR gap, or technical debt that does not fit one of these three — record it as a plain observation in the document, but do not start the violation workflow for it.

---

## Workflow

### Step 1 — Collect silently during the documentation pass

Do not interrupt generation. While documenting each mechanism or module, note every violation you find. Complete the full documentation pass first.

### Step 2 — Stop and inform

After the documentation pass is complete, stop and surface every violation found:

```
## Architecture Violations Found

| # | Category | Location | Description |
|---|---|---|---|
| 1 | Pattern deviation | Catalog module | `process.env.API_URL` accessed directly in catalog.service.ts |
| 2 | Orphan concern | Session handling | Token refresh logic in three unrelated files with no owner |
| 3 | Missing mechanism | Error Handling | No error boundary mechanism — multi-step flows have no fallback |
```

If no violations are found: state `No violations in scope found during this documentation pass.` and proceed to validation.

### Step 3 — Ask the user how to proceed

For each violation, present the three options:

```
For each violation, choose how to proceed:

  2a — DR and proceed
       Write a Decision Record documenting this violation and the decision to live with it for now.
       Architecture work continues unchanged.

  2b — DR and strategy
       Write a Decision Record plus an architecture strategy note describing the target design
       (e.g. "domain model deviates from current code; implement correct shape in domain-test layer first").
       Useful when the fix requires a design rethink before any code can change.

  2c — DR and refactor
       Write a Decision Record, add a thin-slice refactor entry to the story map,
       and append a downstream note to the CDD log.
       The thin slice is not planned in detail here — it is a flag that planning is needed.

Reply as: 1. 2a   2. 2b   3. 2c
```

### Step 4 — Launch a non-blocking sub-agent

After the user replies, **immediately launch a background Task sub-agent** to handle all violation resolutions. Do not handle them inline — the sub-agent runs in the background so the main architecture work (validation, diagram check) continues without waiting.

The sub-agent receives:
- The violation table
- The user's choices (2a/2b/2c per item)
- The target project root
- The current highest ADR/DR number on disk in `docs/architecture/decisions/`

The sub-agent executes the actions for each item (see below) and produces a resolution summary.

---

## Resolution actions (executed by the sub-agent)

### 2a — DR and proceed

1. Read `../common/decision-record.md` — DR template and criteria.
2. Write one DR file to `docs/architecture/decisions/` numbered after the current highest.
3. Use the **Violation DR** format (see below).
4. Add the DR to the ADR list in the architecture document.

**No code change. No strategy. No thin slice.**

### 2b — DR and strategy

1. Write the DR (same as 2a).
2. Write a brief strategy note appended to the architecture document as a `> **Strategy note:**` blockquote directly under the relevant mechanism or module heading. The note names the target design and the layer where it will first be implemented correctly. Keep it to 2–4 sentences.

Example strategy note:

```
> **Strategy note (ADR-012):** The domain model currently deviates from the Account boundary defined in the domain specification. The target design treats Account as the aggregate root for all onboarding state. The correct shape will be implemented first in the domain-test layer so tests drive conformance before production code is updated.
```

### 2c — DR and refactor

1. Write the DR (same as 2a).
2. Add one thin-slice entry to `docs/stories/story-map/thin-slicing.md`:

```markdown
### Refactor: {short violation description} (→ DR-NNN)

- **Scope:** {which module or mechanism}
- **What needs to change:** {one sentence}
- **Downstream planning needed:** {shaping | discovery | thin slicing} — steps not defined here; this is a flag to plan them.
```

3. Append to the active CDD log (session journal) a single line:

```
REFACTOR FLAGGED: {violation description} — thin slice added, DR-NNN, planning required.
```

The thin slice is not fully planned here. It is a placeholder that signals planning work is downstream.

---

## Violation DR format

Use `../common/decision-record.md` as the base template. For violations, fill the fields as follows:

```markdown
# DR-{NNN}: Live with — {category}: {short description}

> **Status:** Accepted
> **Date:** {YYYY-MM-DD}
> **Violation category:** {Pattern deviation | Orphan concern | Missing mechanism}
> **Resolution path:** {2a — proceed | 2b — strategy | 2c — refactor}

## Context

{What was found during the documentation pass. Name the exact file, module, or mechanism. What principle or architecture constraint it violates.}

## Decision

We will {proceed with the current state | address this through the strategy described below | refactor via a dedicated thin slice} and document it here so the deviation is visible and tracked.

## Known risk

{One sentence: what could go wrong by leaving this unresolved.}

## Recommended resolution

{Concise description of the correct target state — enough for an engineer to implement.}

## Trigger for revisit

{A specific event, milestone, or condition — not "when we have time."}
```

---

## DO / DO NOT

**DO:**
- Read this file only when documenting an existing system.
- Collect all violations before surfacing them — one stop, not many.
- Launch the resolution sub-agent in the background; do not block main architecture work.
- Write the DR immediately when the user confirms the choice — not at the end of the session.
- Use `../common/decision-record.md` for the DR template.

**DO NOT:**
- Record security risks, NFR breaches, or technical debt through this workflow — they are plain observations only.
- Interrupt generation mid-section to ask about a violation.
- Write a violation DR without explicit user confirmation of the resolution path.
- Plan the refactor thin slice in detail here — 2c is a flag, not a plan.
- Apply this workflow when designing something new.
