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

**Deliverables folder:** see `../common/story-driven-delivery/skill-extensions.md` — Output file resolution.

**File name:** `acceptance-criteria.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Hidden actors** — who actually triggers this — is "the user" hiding three different actors with different journeys and different expectations of "done"?
- **One story or a bundle** — does this story describe one observable interaction, or is it actually three behaviors wearing a trenchcoat? If you can't state done in 4-9 criteria, it might be a bundle.
- **Unstated negative paths** — what should explicitly NOT happen? Every happy path has a shadow — rejection, timeout, conflict, unauthorized. Have those been surfaced or assumed away?
- **Domain vocabulary drift** — are the terms in these criteria the same terms the domain experts use, or has the team invented its own words? Synonyms become bugs.
- **Observable vs. internal** — can a stakeholder verify each criterion by looking at the system's behavior, or do some criteria describe internal state that nobody outside the code can see?

---

## Diagram workflow

See `../common/story-driven-delivery/diagram-workflow.md` — **mode `acceptance-criteria`**, output `docs/stories/acceptance-criteria.drawio`.

---

## Agent Instructions

Follow `../common/story-driven-delivery/skill-extensions.md` and `common/skill-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what AC are, WHEN/THEN/AND/BUT, domain terms, atomic AC, actor alternation, pitfalls.
- **`reference/examples.md`** — worked AC for one story (same domain as `abd-story-mapping` examples).
- **`templates/acceptance-criteria-example.md`** — full multi-story filled example (Manage Customer Orders).

**Non-negotiable before writing any Domain terms section:** every term must already exist in a domain source artifact. See `../common/story-driven-delivery/domain-input-priority.md` and rule **Domain terms must come from the domain model** in `rules/`.

### 2. Generate

**Produce the template:**

| Template | What to produce |
| --- | --- |
| `templates/acceptance-criteria.md` | Story-level AC using WHEN/THEN/AND/BUT per `reference/concepts.md`. Per story, include a **Domain terms** section: key words and phrases for concepts, state, actions, and rules used in that story's AC. **Source traceability:** each numbered AC must cite **Evidence** (chapter, section, page, paragraph, chunk id, etc.) or a per-story **Source evidence** table. **Do not** paste the template's `## Instructions` section into generated project files. |

**Consistency:** WHEN/THEN semantics, story coverage, **domain terms** (same vocabulary; italics on domain terms and domain list), **source evidence per AC**, and ordering must be complete throughout the `.md` artifact. Generated artifacts contain **only** stakeholder-facing sections from the templates.

**If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/story-driven-delivery/skill-extensions.md` § Validate output and `../common/story-driven-delivery/validate-checklist.md`.

---

## Validate

**Goal:** Inspect what was built — read artifacts as reviewers.

- **Behavioral language** — every AC uses observable language; no capability statements ("can do").
- **Domain terms** — each story has a Domain terms section; all terms traced to a domain source.
- **WHEN/THEN/AND/BUT** — correct keywords; no Given in AC; no implementation detail.
- **Atomic AC** — general case once; follow-on AC are deltas only.
- **Actor alternation** — no long runs of the same actor without switching (scanner enforces).
- **Source evidence** — each AC cites evidence or a per-story source table.

---
