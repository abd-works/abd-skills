---
name: abd-story-acceptance-criteria
catalog_garden_tier: practice
catalog_garden_order: 30
catalogue_one_liner: >-
  State exactly what must be true for a story to be done — so everyone agrees on 'finished'.
description: >-
  Write When/Then/And/But behaviors that define done for each story. Use when writing or reviewing exploration-phase behavior for stories.
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

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

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

Produces `docs/stories/acceptance-criteria.drawio` from `story-graph.json`. Requires `story-graph.json` to exist (built by `story-graph-ops`). Must exist before the cell is marked done.

```bash
python drawio_story_sync_cli.py render \
  --mode acceptance-criteria \
  --graph docs/stories/story-graph.json \
  --out   docs/stories/acceptance-criteria.drawio
```

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what AC are, WHEN/THEN/AND/BUT, domain terms, atomic AC, actor alternation, pitfalls.
- **`reference/examples.md`** — worked AC for one story (same domain as `abd-story-mapping` examples).
- **`templates/acceptance-criteria-example.md`** — full multi-story filled example (Manage Customer Orders).

**Non-negotiable before writing any Domain terms section:** every term must already exist in a domain source artifact (Domain Language, domain sketch, domain model, Class Model, or any team-designated vocabulary file). If a term is missing, **stop — list every missing term and ask the user how to proceed** before writing it into AC. **NEVER create `domain-terms.md` if any domain source file already exists.** Only create `domain-terms.md` as a bootstrap when the engagement has no domain sources at all. See rule **Domain terms must come from the domain model** in `rules/`.

### 2. Generate

**Produce the template:**

| Template | What to produce |
| --- | --- |
| `templates/acceptance-criteria.md` | Story-level behaviors using *When*/*Then*/*And*/*But* per `reference/concepts.md`. Per story: **Domain terms** section, a **Behaviors** numbered list, and an **Evidence** table at the end of the story (one row per behavior #). Never inline Evidence after individual behaviors. **Do not** paste the template's `## Instructions` section into generated project files. |

**Notation:** Step keywords (*When*, *Then*, *And*, *But*) use `*single-star italic*`, sentence case. Domain terms in step text use `**double-star bold**`. Domain term list entries use `*italic*`. Evidence lives in a `### Evidence` table at the end of each story.

**Consistency:** *When*/*Then* semantics, story coverage, domain terms (same vocabulary throughout), source evidence (per-story table), and ordering must be complete throughout the `.md` artifact. Generated artifacts contain **only** stakeholder-facing sections from the templates.

**If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect what was built — read artifacts as reviewers.

- **Behavioral language** — every behavior uses observable language; no capability statements ("can do").
- **Domain terms** — each story has a Domain terms section; all terms traced to a domain source; terms in step text use `**bold**`; step keywords use `*italic*`.
- **When/Then/And/But** — correct keywords, sentence case, single-star italic; no *Given* in AC; no implementation detail.
- **Atomic behaviors** — general case once; follow-on behaviors are deltas only.
- **Actor alternation** — no long runs of the same actor without switching (scanner enforces).
- **Evidence table** — each story has a `### Evidence` table after `### Behaviors`; no inline Evidence after individual behavior items.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
