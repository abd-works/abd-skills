# Phase 3 — Guided Evidence Extraction

**Actor:** Code | 
## Purpose

Extract structured domain evidence from rule text using Concept Guidance v1.

This phase converts raw rule text into structured evidence that later phases use
to construct the domain model and interaction model.

The extractor is **domain-agnostic** and must not rely on hard-coded verbs
or domain-specific terminology.

## Trigger

extract evidence, guided extraction, extract terms, extract actions, extract decisions

## Inputs

- `context/context_chunks.json` — text chunks extracted from the source material
- `generated/domain/concept_guidance.json` — guidance produced in Phase 2:
  - priority concepts
  - concept aliases
  - priority mechanisms
  - actors
  - variation axes
  - noise filters
  - focus sections

## Outputs

`evidence/terms.json`, `evidence/actions.json`, `evidence/decisions.json`, `evidence/states.json`, `evidence/relationships.json`, `evidence/modifiers.json`

## Run

```bash
python scripts/pipeline.py run evidence_extraction
```

Script: `scripts/evidence_extraction_guided.py`

## Post-extraction (AI self-check)

After the script completes, scan a sample of extracted items (actions, decisions, terms) against concept_guidance:

- **Concept alignment:** Subject or object in priority_concepts (from guidance)
- **Rule prose:** Raw text is mechanical rule content, not structural junk (headings, TOC, chapter labels, all-caps titles)
- **No narrative flavor:** No archetype names, "The X does...", or prose that describes rather than specifies
- **No weak subjects:** No You, It, Perhaps, They as subject/object
- **No prose fragments:** No transitional phrases (Alternatively, Otherwise, Compare) as rule content

If junk found: warn user and suggest fixes (remove from JSON manually, or tighten extractor filters).

Also print the **top 20 most frequent predicates** from `evidence/actions.json` — these surface what the domain *does*, not just what it *has*. Predicate clusters that don't map to an existing epic concept are a signal of missing behavior coverage. Report them to the user for Phase 5 input.
