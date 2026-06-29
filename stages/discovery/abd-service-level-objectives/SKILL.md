---
name: abd-service-level-objectives
catalog_garden_tier: practice
catalog_garden_order: 55
catalogue_one_liner: >-
  Measurable NFRs as SLI/SLO/SLA — target × volume × percentage, scoped to story map, with error-budget policy.
description: >-
  Capture the non-functional requirements (NFRs) of a system as concrete
  Service Level Indicators, Objectives, and Agreements (SLI/SLO/SLA) tied
  to a specific scope — a story, an epic, a parent epic, or the whole
  system. NFRs are organised into six categories. Every objective states a
  target at a volume at a percentage so it can be measured, alerted on, and
  refused. Use when committing to measurable non-functional targets, after
  an incident reveals missing targets, when drafting SLAs, or when
  classifying features by criticality.
context-perspective: stage
context-fidelity:
  - level: discovery
    mode: non-functional-requirements
---
# abd-service-level-objectives

## Purpose

A non-functional requirement that cannot be measured is a wish. Teams that ship without measurable NFRs discover the truth in production — too late, too expensive, sometimes too public. This skill turns each NFR into a concrete **Service Level Indicator** (what is measured), **Service Level Objective** (the target on that indicator), and where a customer-facing commitment exists, a **Service Level Agreement**. Critically, each objective is scoped to the **functional area** it applies to: a single user story, an epic, a parent epic, or the system as a whole.

---

## Output file

**Deliverables folder:** see `../common/reference/skill-workflow.md` — Output file resolution.

**File name:** `service-level-objectives.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

> **MANDATORY — read `../common/reference/skill-workflow.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — SLI/SLO/SLA definitions, six NFR categories, scope levels, target-volume-percentage shape, and error budgets.
- **`reference/examples.md`** — typical SLO matrix structure and the shape of a good SLO row.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/service-level-objectives.md` | The SLO matrix — scope statement, criticality classification, system-level SLOs, parent-epic SLOs, story-level SLOs (high-criticality only), error-budget policy, and SLA section (if applicable). |

**Build steps:**
1. Establish scope vocabulary from story map (or system + parent epic fallback).
2. Classify features by criticality (mission-critical / business-important / best-effort).
3. Set system-level SLOs (availability, security, maintainability).
4. Set parent-epic SLOs where targets differ from system default.
5. Set story-level SLOs only for highest-criticality stories.
6. Define error-budget policy with concrete actions at 50%/25%/0%.
7. List SLAs separately — each looser than its supporting SLO.

### 3. Validate

Run the scanners:

```bash
python skills/common/scripts/run_scanners.py \
  --skill-root skills/abd-service-level-objectives \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../common/reference/skill-workflow.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Every SLO has target × volume × percentage** — no bare adjectives; no target without volume; no 100% on availability claims.
- **Every row picks one of the six NFR categories** — no "Other" or merged categories.
- **Every row has a named scope** — system, parent epic, epic, or story — that exists in the story map.
- **Every SLI is measurable today** — names a real tool or a planned tool with an owner.
- **Error-budget policy is concrete** — actions tied to thresholds (50%/25%/0%), not "review periodically".
- **SLAs are looser than supporting SLOs** — never the same number; internal target has headroom.
- **Criticality classification is explicit** — section marks each area as mission-critical / business-important / best-effort.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
