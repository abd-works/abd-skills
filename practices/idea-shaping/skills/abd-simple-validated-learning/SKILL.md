---
name: abd-simple-validated-learning
catalog_garden_tier: practice
catalog_garden_order: 17
catalogue_one_liner: >-
  Turn surfaced assumptions into hypotheses, prioritise small tests, and run Plan / Validate / Learn before full build.
description: >-
  Turn surfaced assumptions into falsifiable hypotheses, prioritise small tests, and work each one
  through Plan, Validate, and Learn before committing to full build. Use when an opportunity canvas,
  impact map, or any model surfaces assumptions that need testing before the team commits to build.
---
# abd-simple-validated-learning

## Purpose

Opportunities, ideas, and initiatives often carry many unverified assumptions — about customers, value, feasibility, and economics — that the organisation has not yet checked. This skill is for **surfacing those assumptions explicitly** and **working through them** iteratively before the organisation treats them as fact or commits to a full build. The agent (or facilitator) **mines** the supplied context for **assumptions**, rewrites them as **falsifiable hypotheses**, **prioritises** them into a **validation backlog**, and structures each item to move through **Plan → Validate → Learn**.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `validated-learning-backlog.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what "simple" means, the 5-step method (mine → hypotheses → prioritise → Plan/Validate/Learn → checklist pass), input sources, and the discovery emphasis.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/validated-learning-backlog.md` | Prioritised list + Plan / Validate / Learn table (Kanban-style columns in one view). |
| `templates/experimentation-canvas.md` | One experiment per block: belief, method, success/fail signal, owner, by when — for workshops or a single high-stakes test. |

**Method:** Follow the 5-step method in `reference/concepts.md` — mine assumptions, convert to hypotheses, prioritise the backlog, define Plan/Validate/Learn per item, then run the multi-area checklist pass.

**Template parity:** The same experiments appear in the backlog; the experimentation canvas can zoom one experiment for deeper treatment.

**Scope:** Produce `validated-learning-backlog.md` always; add `experimentation-canvas.md` only when a single experiment needs a full canvas treatment.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-simple-validated-learning \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Traceability** — Every backlog item ties to a source line or section in the input context.
- **Falsifiability** — Each hypothesis can fail on evidence; "success" is learning, not only green lights.
- **Accountability** — Owner and date on each active item, or an explicit TBD with who picks it up.
- **Scope honesty** — Do not imply this skill runs the team's stand-up or their physical board; you document the rhythm they can follow.
- **Honest bar** — For build–measure–learn in shipped product, point to delivery / product practices; keep this skill in pre-build discovery unless the test is a thin release.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
