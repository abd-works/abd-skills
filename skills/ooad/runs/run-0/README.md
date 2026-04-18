# Run 0 — Reference Baseline

**Source commit:** `bd4dc7a8` (agile_bots_demo — "ooad 2")
**Original workspace:** `mm3e-experiment/abd-ooad/`
**Extracted:** 2026-04-08

---

## Purpose

This is the **reference baseline** for all subsequent ooad runs on MM3E.
It represents the last known-good output from a real OOAD session on the MM3e Heroes Handbook
using the `abd-ooad` skill methodology.

**Use this as the gold standard** for:
- Output format and structure
- Model notation conventions (domain model template syntax)
- Slice folder organisation (`1 - basics-checks-conditions/`)
- Progress tracking files (`progress/process-checklist.md`)
- Domain scan results layout
- Strategy and term-registry structure

---

## What's Here

### Root workspace files
| File | Phase | Notes |
|------|-------|-------|
| `domain-scan-model.md` | Step 0 | 4 anchors: Character, Check, Condition, Effect — uses exact domain model template notation |
| `domain-scan-results.md` | Step 0 | Source map, anchor justification, tensions T1–T3 |
| `domain-scan-model.drawio` | Step 0 | Anchors-only class diagram |
| `domain-scan-model - IDEAL.drawio` | Step 0 | Corrected/ideal version of diagram |
| `domain-scan-model fixed assoc.drawio` | Step 0 | Association-fixed diagram |
| `domain-scan-model - Ideal.md` | Step 0 | Ideal model prose |
| `domain-noun-verb.md` | Phase 2 | Root-level noun/verb extraction (superseded by slice folder) |
| `strategy.md` | Planning | Slice plan, phase-id execution order, tensions to resolve |
| `term-registry.md` | Global | Running classification registry across all phases |

### Slice folder: `1 - basics-checks-conditions/`
| File | Phase | Notes |
|------|-------|-------|
| `domain-noun-verb.md` | Phase 2 | Slice-specific nouns/verbs/rules/states — the correct slice output |
| `domain-raw-candidates.md` | Phase 3 | Integrated model: `### Class : << kind >>` under anchor modules |
| `domain-verb-noun-manual.md` | Phase 2 | Manual walkthrough variant |
| `nouns-verbs.md` | Phase 2 | Early/partial extraction |
| `raw-candidates-list.md` | Phase 3 | Deprecated tabular form (kept for reference) |
| `thing-vs-data-about-a-thing.md` | Phase 2 | Pattern analysis file |

### `progress/`
| File | Notes |
|------|-------|
| `process-checklist.md` | Phase-by-phase completion tracking |
| `strategy-run-checklist.md` | Run-level checklist |
| `nouns-verbs-rules-and-states-checklist.md` | Phase 2 checklist |
| `nouns-verbs-rules-and-states-prompt.md` | Phase 2 prompt template |
| `README.md` | Progress folder overview |

### `skill/`
Snapshot of the `abd-ooad` skill files (at commit `138cb56` — pre-refactor) that governed this run:
- `SKILL.md` — skill entry point and workspace configuration
- `process.md` — full 20-step OOAD methodology
- `domain-scan.md` — Step 0 detailed technique
- `domain-model-template.md` — canonical model notation
- `domain-noun-verb-template.md` — Phase 2 template
- `domain-raw-candidates-template.md` — Phase 3 template
- `strategy-template.md` — strategy file template
- `domain-scan-results-template.md` — scan results template
- `domain-model-guide.md` — model authoring guide
- `term-registry-guide.md` — term registry guide

---

## Key Format Conventions (reverse-engineered)

### Domain Model Notation
```
ClassName : <<kind>>
+ property: Type
      Invariant: constraint
      Note: annotation
+ method(param: Type): ReturnType
-----
```

- `<<Anchor>>` for anchor classes (Step 0)
- `<<Entity>>` / `<<ValueObject>>` / `<<Process>>` / `<<Policy>>` / `<<Role>>` / `<<Event>>` for Phase 3
- `-----` as class separator
- `### Note :` block for cross-cutting tensions per class

### Module grouping
```markdown
## [module name]

ClassName : <<Anchor>>
...
-----
```

### Slice folder naming
`{N} - {slice-label}/` — e.g. `1 - basics-checks-conditions/`

### Tension annotations in `domain-raw-candidates.md`
```
*[S# · Phase n]* Tension — description
```
Always `[S# · Phase n]` first, then `Tension`.

---

## Anchors from Run 0

| # | Module | Core Class | Supporting |
|---|--------|-----------|------------|
| 1 | character | Character | Ability, Skill, HeroPoint, Advantage, Power, Complication |
| 2 | check | Check | — |
| 3 | condition | Condition | — |
| 4 | effect | Effect | Modifier |

## Tensions from Run 0

| # | Tension | Resolution target |
|---|---------|------------------|
| T1 | Power vs Effect | Ch.6 deep read — slice S1 |
| T2 | Device vs Equipment vs Construct | Ch.7 — slice S2 |
| T3 | Modifier as class vs cost delta | Ch.6 deep read — slice S1 |
