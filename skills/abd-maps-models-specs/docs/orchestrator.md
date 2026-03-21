# Autonomous orchestrator (builder / runner / critic)

## Roles

| Role | Script responsibility | What it does |
| ---- | ---------------------- | ------------ |
| **1 — Planner (builder)** | `orchestrator_loop.py` | Writes `test/mm3/orchestration/plans/plan_NNN.md` — next steps from **deterministic** templates, or from your HTTP API if configured. |
| **2 — Runner** | same | Runs `phase0_audit.py` → `apply_modeling_kind_heuristics.py` → `validate_modeling_kind_sidecar.py --golden` → `generate_context_bundle_manifest.py`. Logs under `orchestration/runner/`. |
| **3 — Critic (evaluator)** | `critic_mm3_domain.py` | Scores pipeline health + **optional** `map-model-spec` text against `rules/mm3_domain_critic.json` and `mm3_target_ontology.json`. |

## One-command loop

```bash
cd skills/abd-maps-models-specs
python scripts/orchestrator_loop.py --min-iterations 10 --max-iterations 20 --stop-on-score 0.92
```

- Runs **at least** `--min-iterations` (default 10), **at most** `--max-iterations` (default 20).
- Stops early when **critic `overall_score` ≥ `--stop-on-score`** and the pipeline is green (unless `--no-early-stop`).

## Optional HTTP API (you are the orchestrator host)

Set **`ORCHESTRATOR_AGENT_URL`** to a server you control. Each iteration POSTs JSON:

```json
{
  "role": "planner",
  "iteration": 3,
  "critic": { "overall_score": 0.71, "invariants": [], "recommendations": [] },
  "runner_log": [{ "cmd": ["python", "scripts/phase0_audit.py"], "exit": 0, "tail": "..." }]
}
```

Return:

```json
{ "plan_markdown": "## Custom plan\n..." }
```

If the request fails or the variable is unset, the loop prepends a short failure note and uses the **built-in deterministic plan** (never blocks).

## Domain heuristics (critic “cheat sheet”)

Edit **`rules/mm3_domain_critic.json`** — checks/traits, powers vs effects, damage/affliction, modifiers. The critic uses **keyword presence** in:

- `test/mm3/maps-models-specs/map-model-spec.md` (and optional `.json`), and  
- `test/mm3/docs/HeroesHandbook.md` (fallback: `context_index.json`) for corpus coverage.

## Artifacts

| Path | Purpose |
| ---- | ------- |
| `test/mm3/orchestration/state.json` | Last iteration + stop reason |
| `test/mm3/orchestration/run_summary.json` | Per-iteration scores |
| `test/mm3/orchestration/plans/plan_NNN.md` | Planner output |
| `test/mm3/orchestration/critic/critic_NNN.json` | Full critic payload |

## See also

- `plan/PROCESS-PLAN.md`
- `docs/modeling_kind_sidecar_v1.md`
