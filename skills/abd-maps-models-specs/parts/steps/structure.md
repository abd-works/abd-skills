# Structure

## Purpose

AI builds the full model from the canonical scaffold plus evidence. Properties, operations, inheritance, stories, and steps are populated from `map-model-spec.json` and `evidence/`.

---

## Inputs

- `map-model-spec.json` — canonical scaffold from **[Integrate and Harmonize](../process.md)** (Stage 2)
- `evidence/` — actions.json, decisions.json, states.json, relationships.json

---

## Process

AI step. Read the scaffold and evidence. For each module/epic pair:

1. **Domain model** — Populate properties, operations, invariants from evidence. Assign types. Add inheritance where subtypes are finalized.
2. **Story map** — Populate stories with Trigger, Response, Pre-Condition, Failure-Modes. Add scenarios and steps. Ground in `**Concept**`.
3. **Sync** — Ensure every concept participates in at least one story. Ensure every story references concepts.

---

## Rules

These rules apply after structuring. Rules with a scanner are mechanically enforced. Rules without a scanner are enforced in the adversarial validation pass.

Full rule files: `rules/`

---

### Use evidence where available (AI-only)
*(AI-only — no scanner)*

**DO** populate properties, operations, and invariants from `evidence/` when evidence exists for a concept.

**DO NOT** ignore evidence — **Structure** merges scaffold with evidence. Empty evidence for a concept is acceptable; populated evidence must be reflected.

---

### No duplicates (reuse)
*Scanner: `scripts/scanners/no_duplicates.py` → Rule: `no-duplicates.md`*

**DO** ensure concept and module names remain unique.

---

### Domain–story map sync (reuse)
*Scanner: `scripts/scanners/domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept participates in at least one story.

---

### Hierarchy sizing (reuse)
*Scanner: `scripts/scanners/hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

**DO** keep child count in the 4–9 range.

---

### Concepts must have owns (reuse)
*Scanner: `scripts/scanners/concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept has an `owns` field.

---

### Stories must have trigger and response (reuse)
*Scanner: `scripts/scanners/stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

**DO** ensure every story has trigger and response.

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

```
python scripts/scanners/no_duplicates.py --input map-model-spec.json
python scripts/scanners/domain_interaction_sync.py --input map-model-spec.json
python scripts/scanners/hierarchy_sizing.py --input map-model-spec.json
python scripts/scanners/concepts_have_owns.py --input map-model-spec.json
python scripts/scanners/stories_have_trigger_response.py --input map-model-spec.json
```

Review each violation. Fix or document. Re-run until all scanners report PASS.

### Pass 2 — Adversarial validation (AI)

- Any evidence ignored when it should have been used?
- Any property or operation invented without evidence?
- Any concept with evidence that has no properties/operations populated?

---

## Output

- `map-model-spec.json` — structured (full domain model + story map)
