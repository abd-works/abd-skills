---
name: domain-terms
catalog_garden_tier: practice
catalog_garden_order: 2
catalogue_one_liner: >-
  Extract domain terms, group into Key Abstractions; single domain-terms file per module.
description: >-
  Extract domain terms, group them into Key Abstractions, and produce a single
  domain-terms file — the shared vocabulary and building blocks for the module.
  Use when the user asks to "extract domain terms", "define terms", "identify key
  abstractions", "build the domain terms", or "what are the building blocks."
---
# abd-domain-terms

## Purpose

Build a shared, rigorous vocabulary for each module — the terms, behaviors, and rules that domain experts and modelers agree on — and immediately structure them into **Key Abstractions** (named building blocks) so that every conversation, document, and downstream artifact uses the same language without translation.

This is a single-pass skill. It does not produce a flat term list first and a KA file second. It reads source, identifies terms, groups them into KAs, and writes one file.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `domain-terms.md`. Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `<deliverables-folder>/modules/<module-name>-domain-terms.md`.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — Key Abstractions, domain terms, the two tests, three outcomes, boundary terms, and the consistent file shape.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/domain-terms-template.md` | The domain terms file with KA groupings, behavioral bullets, per-term decisions and references. |

**Quality bar:** A typical module has 3–8 Key Abstractions. Every KA intro paragraph opens with "*KAName* is …" and weaves role, boundary, responsibilities, relationships, and invariants. Every domain term in behavioral bullets and KA intro paragraphs is *italicized*. Per-term `#### Decisions made` and `#### References` with fenced `source` blocks. State marker set to `domain-terms` in front matter.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-domain-terms \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **One file** — named `[<name>-]domain-terms.md`. No separate key-abstractions file.
- **KA inventory in header** — a `**Key Abstractions (term grouping)**` list names every KA and its subordinate terms.
- **Every KA has an intro paragraph** — opens with "*KAName* is …".
- **No separate KA-as-term entry** — the KA intro paragraph is the definition.
- **Behavioral bullets per term** — at least one per `### term`.
- **Decisions and References per term** — `#### Decisions made` and `#### References` immediately after each term's bullets (h4 — never `###`, which makes them peer domain terms in the outline).
- **Separators** — `---` after every term block.
- **Domain terms italicized** — every domain term in bullets and KA intro paragraphs.
- **Boundary terms have owners** — every `### boundary_term` carries `*(owned by: Module)*`.
- **State marker** — front matter reads `state: domain-terms`.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
