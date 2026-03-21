# Phase 0 / Phase 1 stub — iteration log

**Orchestrator:** main agent (Cursor). **Builder:** scripts + reports in-repo. **Critics:** independent readonly subagents (rounds 1–3); **round 4** = orchestrator synthesis + validator hardening from critic feedback.

**Repro (exact commands):**

```text
python scripts/phase0_audit.py
python scripts/apply_modeling_kind_heuristics.py
python scripts/validate_modeling_kind_sidecar.py --golden
python scripts/generate_context_bundle_manifest.py
python scripts/sample_domain_rule_review.py
python scripts/orchestrator_loop.py --min-iterations 10 --max-iterations 20
```

**Fingerprints (run-time):** see `phase0_audit_metrics.json` → `handbook_sha256`, `generated_at`.

---

## Iteration 1 — Phase 0 metrics + audit report

- **Built:** `scripts/phase0_audit.py` → `test/mm3/context/phase0_audit_metrics.json`
- **Built:** `test/mm3/context/phase0_audit_report.md` (§0.1–0.4)
- **Result:** 725/725 index↔chunk; handbook SHA-256; **0** `modeling_kind` on index; gate **Adopt + extend**
- **Critic:** `critic_round_01_phase0_audit.md` — plumbing solid; metadata still insufficient; demands `reason` on units, generator id, `blk` join, reconcile `domain-rule` paths

## Iteration 2 — `modeling_kind` sidecar (heuristic v1)

- **Built:** `scripts/apply_modeling_kind_heuristics.py` → `test/mm3/context/modeling_kind_sidecar.json`
- **Distribution:** definition_candidate 328, domain_rule_candidate 266, narrative_example 83, toc_or_nav_noise 15, variation_rule 19, mechanic_rule 8, behavioral_interaction 5, editorial_or_credit 1, ambiguous_review 0
- **Critic:** `critic_round_02_modeling_kind_heuristics.md` — OK as **non-authoritative** stub; TOC brittle; do not treat `domain_rule_candidate` as promotion approval

## Iteration 3 — Validation

- **Built:** `scripts/validate_modeling_kind_sidecar.py` — key parity + non-empty kind
- **Critic:** `critic_round_03_validation_handoff.md` — validator narrow but real; log needs fingerprints + decisions for “serious” handoff

## Iteration 4 — Docs + enum enforcement

- **Built:** `docs/modeling_kind_sidecar_v1.md`; `docs/README.md` row
- **Changed:** `validate_modeling_kind_sidecar.py` — **`ALLOWED_KINDS`** whitelist (critic recommendation)
- **Changed:** `apply_modeling_kind_heuristics.py` — `missing evidence_type` → `ambiguous_review`

## Iteration 5 — Critic artifacts inlined

- **Built:** `critic_round_01_phase0_audit.md`, `critic_round_02_modeling_kind_heuristics.md`, `critic_round_03_validation_handoff.md` (summaries of subagent output)

## Iteration 6 — Residual risks / next session

| Risk | Mitigation (next) |
| ---- | ------------------- |
| **266** `domain_rule_candidate` includes TOC false negatives | Sample 20; add body/line-pattern TOC signals |
| **`reason` missing on forward units** | Phase 1 index schema or sidecar |
| **No generator version in index** | Next index build |
| **Promotion gates must not read sidecar as truth** | Document in scanners / Phase 4 gate text |

**Phase 1 merge preconditions (not yet met):** schema doc + optional JSON Schema file + spot-check error rate on `domain_rule_candidate` vs gold.

## Iteration 7 — Heuristic v2 (body TOC) + golden + schema + manifest

- **Changed:** `scripts/apply_modeling_kind_heuristics.py` — `read_chunk_body`, `toc_nav_body_score`, `BODY_TOC_THRESHOLD`; `definition`/`domain-rule` can flip to `toc_or_nav_noise` from body signals; payload `heuristic_version: v2`.
- **Built:** `test/mm3/context/modeling_kind_heuristic_golden.json` — regression snapshot of `kinds_distribution`.
- **Changed:** `scripts/validate_modeling_kind_sidecar.py` — `--golden` compares distribution (+ optional `heuristic_version`).
- **Built:** `docs/schemas/modeling_kind_sidecar.schema.json`.
- **Built:** `scripts/sample_domain_rule_review.py` — quick human spot-check list.
- **Built:** `scripts/generate_context_bundle_manifest.py` → `test/mm3/context/context_bundle_manifest.json` (SHA-256 of index, sidecar, phase0 metrics).
- **Updated:** `docs/modeling_kind_sidecar_v1.md` — v2 behavior, golden path, schema link.
- **Result (725 units):** `toc_or_nav_noise` **215**, `domain_rule_candidate` **229**, `definition_candidate` **165** (remaining kinds unchanged vs v1 counts where applicable).
- **Residual risk:** dense **table / measure** lines (e.g. MASS ladder) can score as TOC-like — tune in v3 or require LLM for `domain_rule_candidate` promotion.

## Iteration 8 — Orchestrator API loop (planner / runner / critic)

- **Built:** `scripts/orchestrator_loop.py` — runs pipeline each tick; writes `test/mm3/orchestration/plans/`, `runner/`, `critic/`; optional **`ORCHESTRATOR_AGENT_URL`** POST for custom planner markdown.
- **Built:** `scripts/critic_mm3_domain.py` + `rules/mm3_domain_critic.json` — MM3 OO invariants (checks, traits, powers/effects, damage+affliction, modifiers); scores `map-model-spec.md` + corpus.
- **Built:** `test/mm3/maps-models-specs/mm3_target_ontology.json`, `map-model-spec.md` (stub for critic keyword alignment).
- **Docs:** `docs/orchestrator.md`

---

## Orchestrator synthesis (`critic_round_04_orchestrator_synthesis.md`)

Short cross-cut: three critics agree the **corpus is worth keeping** and **`modeling_kind` is mandatory**; v1 heuristics are **honest scaffolding**—extend with content signals, enum validation (done), and **explicit non-promotion** semantics for `domain_rule_candidate` (doc updated).

## Iteration 10 — Critic may read gold map; private gap never shared with builder/planner

- **Scoring:** `critic_mm3_domain.py` **overall_score** = invariants vs **corpus** (`corpus_keywords` only) — first principles; **not** vs gold map.
- **Optional:** `--gold-map` + `--model` (candidate) → `private_gap_analysis` in full JSON (reference terms missing in candidate). **Stripped** before `deterministic_plan` and `ORCHESTRATOR_AGENT_URL` payload (`_public_critic_view`).
- **Orchestrator:** `--gold-map`, `--critic-model`; default gold `docs/reference/mm3-map-model-solution-reference.md`.
- **Docs:** `docs/orchestrator.md`, `docs/reference/README.md`.

## Iteration 11 — Process continuation (morning run, 2026-03-22)

Per [`plan/PROCESS-PLAN.md`](../../../plan/PROCESS-PLAN.md) **Execution order** §1–3: re-ran the **green path** on current `test/mm3/context/` (Phase 0 gate remains **Adopt + extend**; sidecar v2 unchanged this run).

| Step | Command | Result |
| ---- | ------- | ------ |
| Phase 0 metrics | `python scripts/phase0_audit.py` | 725/725 index↔chunk; `handbook_sha256` refreshed in `phase0_audit_metrics.json` |
| Heuristics v2 | `python scripts/apply_modeling_kind_heuristics.py` | Distribution unchanged vs golden (165 / 215 / 229 / …) |
| Validator | `python scripts/validate_modeling_kind_sidecar.py --golden` | **OK** |
| Bundle | `python scripts/generate_context_bundle_manifest.py` | `context_bundle_manifest.json` updated |
| Spot-check | `python scripts/sample_domain_rule_review.py` | First-12 samples for `domain_rule_candidate` + `toc_or_nav_noise` |
| Orchestrator | `orchestrator_loop.py` `--stop-on-score 0.96` `--critic-model` … `--run-prefix process-20260322-am` | **overall_score 0.967**, `pipeline_ok` true (iteration 1 stop) |

**Next (process):** Phase 1 **merge preconditions** from iteration 6 — optional **JSON Schema** for forward-index rows with `reason` populated; or proceed to **Phase 2** (terms & mechanisms queue) once you want narrative artifacts beyond the MM3 critic + `map-model-spec.md`.

## Iteration 9 — OO analysis & design foundation (map/model/spec)

- **Replaced stub:** `test/mm3/maps-models-specs/map-model-spec.md` — bounded context, **Check** specialization family, **Trait** vs **Power**, composition **Power → Effect**, **AttackEffect** ← **Damage** / **Affliction**, **Modifier** family, collaboration diagram, anti-patterns (TOC ≠ types, Power does not extend Effect).
- **Updated:** `mm3_target_ontology.json` (v0.2) — `core_types` includes check specializations, **AttackEffect**, **Stamina**, **ResistanceCheck**; `expected_relationships` and `anti_patterns` expanded.
- **Critic:** `critic_mm3_domain.py` **overall_score ≥ 0.98** with pipeline green; all five invariants **pass**.
- **Orchestrator:** one run under `test/mm3/orchestration/oo-foundation-20260321/` (early stop on score threshold).
