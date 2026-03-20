# Step 7 — Integrate and Harmonize

## Purpose

Unify naming, wire cross-module relationships, resolve `[cross-cutting]` items, and finalize subtypes/enums. Produces a clean, consistent scaffold ready for evidence extraction.

---

## Inputs

- `map-model-spec.json` — deepened output from Step 6
- `mms-chunk-index.json` — reverse chunk index

---

## Tasks

1. **Unify naming** — Resolve synonyms, standardize terminology across modules. Ensure concept names are consistent where they refer to the same thing.

2. **Wire cross-module relationships** — For each `[cross-cutting]` item in `cross_cutting_notes`: assign to a primary module or create a shared module; add explicit `relationships` between concepts across modules.

3. **Resolve [cross-cutting]** — Move resolved items out of `cross_cutting_notes`. Document decisions in `open_questions` if human input was needed.

4. **Finalize subtypes and enums** — For deferred subtype candidates: create subtype concepts or confirm enum. For enum decisions: ensure `EnumType {val1, val2}` is applied consistently.

---

## Rules

These rules apply after canonicalization. Rules with a scanner are mechanically enforced. Rules without a scanner are enforced in the adversarial validation pass.

Full rule files: `rules/`

---

### Cross-cutting resolved
*Scanner: `scan_cross_cutting_resolved.py` → Rule: `cross-cutting-resolved.md`*

**DO** resolve every item in `cross_cutting_notes` — assign to a primary module, create a shared module, or document in `open_questions` if human input is needed.

**DO NOT** leave unresolved `[cross-cutting]` items. The scaffold must be clean before evidence extraction.

---

### No duplicates (reuse)
*Scanner: `scan_no_duplicates.py` → Rule: `no-duplicates.md`*

**DO** ensure concept names remain unique within their module after unification. **DO** ensure module names remain unique across the output.

**DO NOT** introduce duplicates when unifying synonyms — merge into one concept with combined chunk_ids.

---

### Domain–story map sync (reuse)
*Scanner: `scan_domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept participates in at least one story after cross-module wiring.

**DO NOT** break sync when assigning cross-cutting concepts — update stories to reference the concept in its new home.

---

### Hierarchy sizing (reuse)
*Scanner: `scan_hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

**DO** keep child count in the 4–9 range. Subtype additions must not violate hierarchy sizing.

---

### Concepts must have owns (reuse)
*Scanner: `scan_concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept (including new subtypes) has an `owns` field.

---

### Stories must have trigger and response (reuse)
*Scanner: `scan_stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

**DO** ensure every story retains trigger and response after canonicalization.

---

### Subtypes and enums finalized (AI-only)
*(AI-only — no scanner)*

**DO** resolve all deferred subtype/enum decisions. Create subtype concepts or apply `EnumType {val1, val2}` consistently.

**DO NOT** leave `[defer]` for subtype/enum in the output. Step 5 produces the canonical scaffold — no deferred structural decisions.

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

```
python scripts/scan_cross_cutting_resolved.py --input map-model-spec.json
python scripts/scan_no_duplicates.py --input map-model-spec.json
python scripts/scan_domain_interaction_sync.py --input map-model-spec.json
python scripts/scan_hierarchy_sizing.py --input map-model-spec.json
python scripts/scan_concepts_have_owns.py --input map-model-spec.json
python scripts/scan_stories_have_trigger_response.py --input map-model-spec.json
```

Review each violation. Fix or document. Re-run until all scanners report PASS.

### Pass 2 — Build chunk index (code)

If structure changed:

```
python scripts/build_chunk_index.py --input map-model-spec.json --output mms-chunk-index.json
```

### Pass 3 — Adversarial validation (AI)

- Any cross-cutting item left unresolved?
- Any synonym unification that merged distinct concepts?
- Any subtype that should have been an enum (or vice versa)?
- Any cross-module relationship missing or incorrect?

---

## Output

- `map-model-spec.json` — updated with unified names, cross-module relationships, resolved cross-cutting items, finalized subtypes/enums
- `mms-chunk-index.json` — updated if structure changed (re-run `build_chunk_index.py`)
