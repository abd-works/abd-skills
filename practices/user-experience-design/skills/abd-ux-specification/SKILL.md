---
catalog_garden_tier: practice
catalog_garden_order: 30
name: abd-interface-design
catalogue_one_liner: >-
  Translate approved hi-fi mockups into production-grade, accessible interface code.
description: >-
  Translate the approved hi-fi mockup for a screen into production-grade,
  functional, accessible interface code in the chosen framework — without
  changing the domain labels, acceptance criteria, or visual decisions.
  Use when implementing a screen from an approved hi-fi, bringing a drifted
  implementation back to the hi-fi and AC, or verifying that every AC is
  implemented and every UL label is used verbatim in the running UI.
---
# abd-interface-design

## Purpose

Hi-fi mockups settle look and feel. The interface stage is where they become real code — and where most teams quietly stop honouring the upstream artifacts because "we're shipping now". This skill keeps that integrity: the implementation renders the same regions, the same affordances, the same labels, the same acceptance criteria, and the same visual decisions as the approved hi-fi, in production-grade code that an end user can actually use. It treats acceptance criteria as the testable surface (every clause is a working behaviour with a check), treats the ubiquitous language as the public vocabulary (labels and copy stay verbatim from the UL and AC), and treats accessibility and performance as constraints that are met, not aspirations that are mentioned.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `interface-design.md` (structured spec). Add a `<name>-` prefix only when disambiguation is needed. Plus working code on disk in the host project (screen component, supporting modules, tests).

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what an interface implementation is, carry-over from upstream, production-grade and functional, memorable differentiation, accessibility, performance constraints, traceability (AC → test → running screen), and the shape of a good implementation.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/interface-design.md` | Structured spec: screen name, source paths, framework, host conventions, carried-over decisions, AC → behaviour → test mapping, accessibility checklist, and performance budget |

**Generation flow:**

1. **Resolve inputs** — hi-fi path, lo-fi path, AC file, screen name, target framework, host project root. Confirm host project's gates (lint, format, test, accessibility, performance).
2. **Discover host conventions** — folder layout, component shape, state management, styling, token system, test conventions.
3. **Carry over upstream decisions** — labels, copy, AC, regions, affordances, typography/colour/density/spacing from lo-fi and hi-fi. Resolve to host tokens.
4. **Author `interface-design.md` first** — fill the template before writing code.
5. **Implement the screen** — each region a container, each affordance an interactive primitive with verbatim label. Inputs labelled programmatically. Focus order matches reading order.
6. **Implement AC behaviours** — every AC clause becomes a working behaviour.
7. **Write tests** — one test per AC clause, named to reference story and clause number.
8. **Pass the host project's gates** — lint, format, type-check, accessibility, performance.
9. **Verify against the hi-fi visually.**
10. **Sync changes back into `interface-design.md`.**

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-interface-design \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Read the committed code and the running screen as reviewers.

- **Upstream fidelity** — every region, affordance, and label from the hi-fi appears in the running screen with the same wording.
- **AC coverage** — every acceptance criterion is implemented and has at least one test named for its story and clause number.
- **Host gates pass** — lint, format, type-check, accessibility, and performance gates pass without silencing.
- **Accessibility** — every input has a programmatic label; focus order matches reading order; focus is visible; state cues are not colour-only.
- **Visual fidelity** — typography roles, colour roles, and spacing scale map to host project tokens, used consistently.
- **Cross-artifact parity** — `interface-design.md` and the running code describe the same implementation.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
