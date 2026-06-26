---
name: abd-practice-skill-builder
description: >-
  Orchestrate the full practice-skill authoring pipeline: retrieve evidence from
  abd-answers, author SKILL.md + rules, add optional scanners, generate the
  catalog card, and produce an HTML manual. Coordinates abd-query-practice-sources,
  abd-author-practice-skill, abd-build-practice-scanners, abd-skill-catalog,
  and abd-practice-skill-manual in sequence.
---

# abd-practice-skill-builder

Orchestrate the **practice skill authoring pipeline**. You coordinate five sub-skills in sequence to produce a complete, validated skill package in the abd-skills repository.

Read each sub-skill's `SKILL.md` and all files in its `rules/` and `reference/` folders before running that stage. Do not skip read-gates.

---

## Pipeline

| # | Stage | Sub-skill | What happens |
|---|-------|-----------|--------------|
| 1 | **Retrieve** | `abd-query-practice-sources` | Structured queries against abd-answers; write `inputs/abd-answers-retrieval.md` with verbatim Kept chunks only — no `rules/` or `SKILL.md` edits at this stage |
| 2 | **Author** | `abd-author-practice-skill` | Copy `SKILL_template.md`, fill `SKILL.md` as a thin router, write `rules/*.md`, move concept prose to `reference/` — no scanners, no bundling |
| 3 | **Scanners** | `abd-build-practice-scanners` | Optional `scanners/*.py`, add `scanner:` to rules, run `run_scanners.py` |
| 4 | **Catalog** | `abd-skill-catalog` | Write `skills/<name>/README.md` AI Garden card; from repo root run `python common/scripts/generate_abd_catalog.py` |
| 5 | **Manual** | `abd-practice-skill-manual` | Copy `assets/` into `manual/<skill-name>/`; write HTML sections; add `Manual:` links in `SKILL.md` |

---

## Stage boundary rule

During **Retrieve** you work only under `skills/<skill-name>/inputs/`. Do not create or edit `rules/*.md`, `SKILL.md`, or `templates/` on the target until **Author**. If stages were mixed, run the corrections workflow before continuing.

---

## Teaching voice

In the target `SKILL.md`, teach the method — concepts, outcomes, who, behaviour change, options. Keep diagram symbols, notation, template positioning, and file prefix labels in `templates/` and `rules/`. Do not pad body prose with provenance comments ("training-aligned", "tightened for this notation"). Use `Source:` on rules when lineage must be auditable.

---

## Corrections workflow

When any deliverable is wrong or a rule was missed:

1. **Identify** — note the problem; open or create the corrections log under the engagement tree (e.g. `logs/corrections-log.md`, `progress/corrections-log.md`). Not inside the skill package.
2. **Log (initial)** — add an entry: Rule, Affects (include `stage:` — `retrieve`, `author`, `scanners`, `catalog`, `manual`, or `*`), DO / DO NOT, Example (wrong); leave Example (correct) blank, Status: open.
3. **Re-generate** — fix the artifact on disk per the violated rule; expect multiple iterations.
4. **Review** — repeat until the deliverable is acceptable, not after one quick edit.
5. **Confirm** — fill Example (correct); set Status: confirmed.

Fix the output first. Only edit source skill files after the output steps are complete, or when the user explicitly asks.

---

## Sub-skill index

| Sub-skill | Path |
| --- | --- |
| Query sources | [`abd-query-practice-sources`](../abd-query-practice-sources/SKILL.md) |
| Author SKILL + rules | [`abd-author-practice-skill`](../abd-author-practice-skill/SKILL.md) |
| Scanners | [`abd-build-practice-scanners`](../abd-build-practice-scanners/SKILL.md) |
| Catalog | [`abd-skill-catalog`](../abd-skill-catalog/SKILL.md) |

---

## Scanner command

```bash
python common/scripts/run_scanners.py --skill-root skills/<skill-name> --workspace <path-to-output>
```

---

## Process (end-to-end)

1. Confirm topic and skill name (kebab-case).
2. Run **abd-query-practice-sources** — `inputs/` only; write `inputs/abd-answers-retrieval.md` with verbatim Kept chunks.
3. Run **abd-author-practice-skill** — copy `SKILL_template.md`, fill `SKILL.md`, write `rules/*.md`.
4. Run **abd-build-practice-scanners** (optional).
5. Run **abd-skill-catalog** — write `README.md`; regenerate catalog from repo root.
6. Run **abd-practice-skill-manual** — copy assets, write HTML, add Manual links.
