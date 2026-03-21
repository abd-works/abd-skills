# Integrate and Harmonize

## Purpose

Unify naming, wire cross-module relationships, resolve `[cross-cutting]` items, and finalize subtypes/enums. Produces a clean, consistent scaffold ready for evidence extraction.

### Domain + story map — relevant excerpts only (full specs: **`parts/domain.md`**, **`parts/story-map.md`**)

*Domain (integrate pass):*

- **Synonym merge:** one **`concepts[].name`**; **union** **`chunk_ids`** / **`chunk_evidence`**; if a merged concept had **`extends`**, ensure the parent **`name`** still exists or repoint **`extends`** after renames (**`parts/domain.md`** — naming + scaffold extensions).
- **Cross-module wiring:** **`depends_on`**, **`provides_concepts`**, and any **`relationships`** stay consistent with **`parts/domain.md`** module boundaries; new shared concepts get **`owns`** + evidence (**`concepts-must-have-owns`**).
- **Subtypes / enums:** align **`extends`** trees and **`EnumType {…}`** property types with finalized decisions (**`parts/domain.md`** — property types).

*Story map (integrate pass):*

- After **moving or renaming** a concept, scan epics/sub-epics/stories: every **`**Concept**`** reference must match a surviving **`concepts[].name`** in the right module (**`parts/story-map.md`** — *Domain Grounding*; scanner **`domain-interaction-sync`**).
- **Hierarchy 4–9** still holds after regrouping (**`parts/story-map.md`** — *Hierarchy* + **`hierarchy-approximately-4-to-9-children`**).

---

## Inputs

- `map-model-spec.json` — deepened output from **[Concept Classes and Stories](../process.md)** (Stage 2)
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
*Scanner: `scripts/scanners/cross_cutting_resolved.py` → Rule: `cross-cutting-resolved.md`*

**DO** resolve every item in `cross_cutting_notes` — assign to a primary module, create a shared module, or document in `open_questions` if human input is needed.

**DO NOT** leave unresolved `[cross-cutting]` items. The scaffold must be clean before evidence extraction.

---

### No duplicates (reuse)
*Scanner: `scripts/scanners/no_duplicates.py` → Rule: `no-duplicates.md`*

**DO** ensure concept names remain unique within their module after unification. **DO** ensure module names remain unique across the output.

**DO NOT** introduce duplicates when unifying synonyms — merge into one concept with combined chunk_ids.

---

### Domain–story map sync (reuse)
*Scanner: `scripts/scanners/domain_interaction_sync.py` → Rule: `domain-interaction-sync.md`*

**DO** ensure every concept participates in at least one story after cross-module wiring.

**DO NOT** break sync when assigning cross-cutting concepts — update stories to reference the concept in its new home.

---

### Hierarchy sizing (reuse)
*Scanner: `scripts/scanners/hierarchy_sizing.py` → Rule: `hierarchy-approximately-4-to-9-children.md`*

**DO** keep child count in the 4–9 range. Subtype additions must not violate hierarchy sizing.

---

### Concepts must have owns (reuse)
*Scanner: `scripts/scanners/concepts_have_owns.py` → Rule: `concepts-must-have-owns.md`*

**DO** ensure every concept (including new subtypes) has an `owns` field.

---

### Stories must have trigger and response (reuse)
*Scanner: `scripts/scanners/stories_have_trigger_response.py` → Rule: `stories-must-have-trigger-response.md`*

**DO** ensure every story retains trigger and response after canonicalization.

---

### Subtypes and enums finalized (AI-only)
*(AI-only — no scanner)*

**DO** resolve all deferred subtype/enum decisions. Create subtype concepts or apply `EnumType {val1, val2}` consistently.

**DO NOT** leave `[defer]` for subtype/enum in the output. **Integrate and Harmonize** must resolve them — no deferred structural decisions in the integrated scaffold.

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

```
python scripts/scanners/cross_cutting_resolved.py --input map-model-spec.json
python scripts/scanners/no_duplicates.py --input map-model-spec.json
python scripts/scanners/domain_interaction_sync.py --input map-model-spec.json
python scripts/scanners/hierarchy_sizing.py --input map-model-spec.json
python scripts/scanners/concepts_have_owns.py --input map-model-spec.json
python scripts/scanners/stories_have_trigger_response.py --input map-model-spec.json
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
