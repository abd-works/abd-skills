---
name: abd-acceptance-criteria
catalog_garden_tier: practice
catalog_garden_order: 30
catalogue_one_liner: >-
  WHEN/THEN/AND/BUT acceptance criteria for stories; behavioral language, atomic AC, domain terms.
description: >-
  Writes exploration-phase acceptance criteria (WHEN/THEN/AND/BUT) for stories as a Markdown document.
  Use when writing or reviewing acceptance criteria, exploration behavior, or WHEN/THEN quality.
---
# abd-acceptance-criteria

## Purpose

Build acceptance criteria per **story**, that explain what must be true when users and systems interact: observable triggers (**WHEN**), expected outcomes (**THEN**), chained effects (**AND**), and explicit negatives (**BUT**). These act as informal first-draft BDD-style steps that guide downstream scenario work. Focus on interactions using domain terms, avoid implementation detail unless the story is technical, and even then keep it minimal.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `acceptance-criteria.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what AC are, WHEN/THEN/AND/BUT, domain terms, atomic AC, actor alternation, pitfalls.
- **`reference/examples.md`** — a complete worked AC example showing the expected format.

**Non-negotiable before writing any Domain terms section:** every term must already exist in a domain source artifact (Domain Language, domain sketch, domain model, Class Model, or any team-designated vocabulary file). If a term is missing, **stop — list every missing term and ask the user how to proceed** before writing it into AC. **NEVER create `domain-terms.md` if any domain source file already exists.** Only create `domain-terms.md` as a bootstrap when the engagement has no domain sources at all. See rule **Domain terms must come from the domain model** in `rules/`.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce the template:**

| Template | What to produce |
| --- | --- |
| `templates/acceptance-criteria.md` | Story-level AC using WHEN/THEN/AND/BUT per `reference/concepts.md`. Per story, include a **Domain terms** section: key words and phrases for concepts, state, actions, and rules used in that story's AC. **Source traceability:** each numbered AC must cite **Evidence** (chapter, section, page, paragraph, chunk id, etc.) or a per-story **Source evidence** table. **Do not** paste the template's `## Instructions` section into generated project files. |

**Consistency:** WHEN/THEN semantics, story coverage, **domain terms** (same vocabulary; italics on domain terms and domain list), **source evidence per AC**, and ordering must be complete throughout the `.md` artifact. Generated artifacts contain **only** stakeholder-facing sections from the templates.

**If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-acceptance-criteria \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read artifacts as reviewers.

- **Behavioral language** — every AC uses observable language; no capability statements ("can do").
- **Domain terms** — each story has a Domain terms section; all terms traced to a domain source.
- **WHEN/THEN/AND/BUT** — correct keywords; no Given in AC; no implementation detail.
- **Atomic AC** — general case once; follow-on AC are deltas only.
- **Actor alternation** — no long runs of the same actor without switching (scanner enforces).
- **Source evidence** — each AC cites evidence or a per-story source table.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
