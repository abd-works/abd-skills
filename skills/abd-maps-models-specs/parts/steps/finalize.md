# Finalize

## Purpose

AI steps: behavior, variation, consolidate, assess, finalize. Produce the validated map-model-spec.

---

## Inputs

- `map-model-spec.json` — structured output from **[Structure](../process.md)** (Stage 3)

---

## Activities

1. **Behavior** — Assign operations to concepts. Link behaviors to steps. Group steps into scenarios.

2. **Variation** — Split stories by subtype when mechanics differ. Add failure modes where evidenced.

3. **Consolidate** — Fix anti-patterns (anemia, over-centralization). Add examples where appropriate.

4. **Assess** — Produce assessment: consistency, coverage, completeness, type-field-vs-subtype. Flag gaps.

5. **Finalize** — Apply assessment fixes. Produce validated `map-model-spec.json`.

---

## Rules

These rules apply after finalization. All structural rules from earlier steps still apply. **Finalize** adds final-quality checks.

Full rule files: `rules/`

---

### No anemia (AI-only)
*(AI-only — no scanner)*

**DO** ensure concepts that own decisions have operations that enact those decisions. Avoid anemic concepts — data bags with no behavior.

**DO NOT** leave concepts with only properties and no operations when the domain clearly implies behavior.

---

### No over-centralization (AI-only)
*(AI-only — no scanner)*

**DO** distribute responsibility across concepts. Prefer composition over a single "manager" or "service" concept.

**DO NOT** create a central concept that does everything — spread operations to the concepts that own the decisions.

---

### Assessment complete (AI-only)
*(AI-only — no scanner)*

**DO** produce an assessment covering: consistency (naming, types), coverage (all concepts in stories), completeness (no [defer] left), type-field-vs-subtype (correct representation).

**DO NOT** skip assessment. Document gaps and apply fixes before declaring final.

---

### All structural rules (reuse)

Run the same scanners as **[Concept Classes and Stories](../process.md)** (and scaffold scanners as needed). The final output must pass all structural checks:

```
python scripts/scanners/no_duplicates.py --input map-model-spec.json
python scripts/scanners/domain_interaction_sync.py --input map-model-spec.json
python scripts/scanners/hierarchy_sizing.py --input map-model-spec.json
python scripts/scanners/concepts_have_owns.py --input map-model-spec.json
python scripts/scanners/stories_have_trigger_response.py --input map-model-spec.json
```

---

## After Generation — Quality Passes

### Pass 1 — Scanners (code)

Run all structural scanners. Fix violations.

### Pass 2 — Adversarial validation (AI)

- Any anemic concepts?
- Any over-centralized design?
- Assessment complete? All gaps documented and addressed?

---

## Output

- `map-model-spec.json` — final, validated
- `map-model-spec.md` — readable summary (optional)
