---
name: abd-story-acceptance-criteria
catalog_garden_tier: practice
catalog_garden_order: 30
catalogue_one_liner: >-
  State exactly what must be true for a story to be done — so everyone agrees on 'finished'.
description: >-
  Write WHEN/THEN/AND/BUT acceptance criteria that define done for each story. Use when writing or reviewing exploration-phase behavior for stories.
context-perspective: stories
context-fidelity:
  - level: exploration
    mode: acceptance-criteria
---
# abd-story-acceptance-criteria

## Purpose

State exactly what must be true for a story to be done — so everyone agrees on "finished" before coding starts.

---

## Output file

**Deliverables folder:** see `common/skill-workflow.md` — Output file resolution.

**File name:** `acceptance-criteria.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

Follow `common/skill-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what AC are, WHEN/THEN/AND/BUT, domain terms, atomic AC, actor alternation, pitfalls.
- **`reference/examples.md`** — worked AC for one story (same domain as `abd-story-mapping` examples).
- **`templates/acceptance-criteria-example.md`** — full multi-story filled example (Manage Customer Orders).
- **[`../../../reference/domain-input-priority.md`](../../../reference/domain-input-priority.md)** — domain terms must come from domain sources before writing AC.

### 2. Generate

**Produce the template:**

| Template | What to produce |
| --- | --- |
| `templates/acceptance-criteria.md` | Story-level AC using WHEN/THEN/AND/BUT per `reference/concepts.md`. Per story, include a **Domain terms** section: key words and phrases for concepts, state, actions, and rules used in that story's AC. **Source traceability:** each numbered AC must cite **Evidence** (chapter, section, page, paragraph, chunk id, etc.) or a per-story **Source evidence** table. **Do not** paste the template's `## Instructions` section into generated project files. |

**Consistency:** WHEN/THEN semantics, story coverage, **domain terms** (same vocabulary; italics on domain terms and domain list), **source evidence per AC**, and ordering must be complete throughout the `.md` artifact. Generated artifacts contain **only** stakeholder-facing sections from the templates.

**If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

### 3. Validate

Run scanners and emit per-rule verdicts — see `common/skill-workflow.md` § Validate output and [`../../../reference/validate-checklist.md`](../../../reference/validate-checklist.md).

---

## Validate

**Goal:** Inspect what was built — read artifacts as reviewers. Also apply [`../../../reference/validate-checklist.md`](../../../reference/validate-checklist.md).

- **Behavioral language** — every AC uses observable language; no capability statements ("can do").
- **Domain terms** — each story has a Domain terms section; all terms traced to a domain source.
- **WHEN/THEN/AND/BUT** — correct keywords; no Given in AC; no implementation detail.
- **Atomic AC** — general case once; follow-on AC are deltas only.
- **Actor alternation** — no long runs of the same actor without switching (scanner enforces).
- **Source evidence** — each AC cites evidence or a per-story source table.

---
