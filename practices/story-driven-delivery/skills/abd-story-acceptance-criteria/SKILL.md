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

## Agent Instructions

**MANDATORY:** Read **`common/skill-workflow.md` in its entirety** and complete § Read-gates before generating.

### 1. Generate

| Template | What to produce |
| --- | --- |
| `templates/acceptance-criteria.md` | Story-level AC using WHEN/THEN/AND/BUT per `reference/concepts.md`. Per story, include a **Domain terms** section: key words and phrases for concepts, state, actions, and rules used in that story's AC. **Source traceability:** each numbered AC must cite **Evidence** (chapter, section, page, paragraph, chunk id, etc.) or a per-story **Source evidence** table. |

**Consistency:** WHEN/THEN semantics, story coverage, **domain terms** (same vocabulary; italics on domain terms and domain list), **source evidence per AC**, and ordering must be complete throughout the `.md` artifact.

### 2. Validate

See `common/skill-workflow.md` § Validate output.

---

## Validate

- **Behavioral language** — every AC uses observable language; no capability statements ("can do").
- **Domain terms** — each story has a Domain terms section; all terms traced to a domain source.
- **WHEN/THEN/AND/BUT** — correct keywords; no Given in AC; no implementation detail.
- **Atomic AC** — general case once; follow-on AC are deltas only.
- **Actor alternation** — no long runs of the same actor without switching (scanner enforces).
- **Source evidence** — each AC cites evidence or a per-story source table.

---
