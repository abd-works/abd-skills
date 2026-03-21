# MM3 test workspace — map-model-spec (Phase 4)

**Status:** Phase 4 foundational spine complete. **Human checkpoint** before Phase 5 (K ≈ 218 full chunk reads at 30% of N=725).

## Spine summary

Six foundational **module + epic** pairs, `module.foundational: true`, concepts at `evidence_stage: "hypothesis"`, each concept has `owns`, `owns_chunk`, and `chunk_ids`.

| Module | Epic | Core concepts |
|--------|------|----------------|
| Ranks and measures | Translate measurements | Rank, MeasurementTable |
| Abilities | Express abilities | Ability, AbilityRank |
| Checks and tasks | Resolve checks | Check, DifficultyClass |
| Skills | Apply skills | Skill, SkillCheck |
| Powers | Acquire powers | PowerEffect, PowerPoints |
| Combat resolution | Track combat state | Condition, ResistanceCheck |

## Artifacts

- `map-model-spec.json` — canonical scaffold (Phase 4).
- `context/context_index.json` — N=725 chunks; Phase 5 uses this for K-read and chunk index build.

## Scanners (run from skill root)

```text
python scripts/scanners/chunks_must_be_referenced.py --input test/mm3/maps-models-specs/map-model-spec.json
python scripts/scanners/concepts_have_owns.py --input test/mm3/maps-models-specs/map-model-spec.json
python scripts/scanners/no_duplicates.py --input test/mm3/maps-models-specs/map-model-spec.json
python scripts/scanners/epic_requires_confirming_stories.py --input test/mm3/maps-models-specs/map-model-spec.json
python scripts/scanners/no_junk_concepts.py --input test/mm3/maps-models-specs/map-model-spec.json
```

Last run: **PASS** on all of the above.

## Next

1. Human review / approve foundational spine.
2. Phase 5: deepen with `build_chunk_index.py` and full-read pass per process.
