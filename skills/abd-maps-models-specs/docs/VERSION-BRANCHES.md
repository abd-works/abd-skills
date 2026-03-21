# Version branches (`abd-maps-models-specs`)

Git branches in repo **`agilebydesign-skills`** use the prefix **`abd-maps-models-specs/`** so you can see **which milestone** a line of work came from.

| Branch | Commit | What it is |
| ------ | ------ | ---------- |
| `abd-maps-models-specs/v0-skill-scaffold-pre-mm3` | `08b148d` | Early skill layout (“skill v1”) before the current MM3 fixture shape. |
| `abd-maps-models-specs/v0-phase4-map-model-spec` | `351759d` | Phase 4 **map-model-spec** JSON/MD focus for MM3 test workspace. |
| `abd-maps-models-specs/v1-heuristic-v2-mm3` | `7414129` | Full **`test/mm3/context`** fixture + **`modeling_kind` v2** (body TOC), golden validator, schema, bundle manifest. |
| `abd-maps-models-specs/v2-orchestrator` | `cfd2bfa` | Adds **orchestrator loop**, **MM3 domain critic**, `rules/mm3_domain_critic.json`, stub `map-model-spec.md`, API hook for planner. |
| `abd-maps-models-specs/v3-candidate-near-reference` | `85d78f2` | **Corpus-first** critic (public score); optional **gold map** → `private_gap_analysis` only; **reference docs** under `docs/reference/`; **full** `map-model-spec.md` candidate; orchestrator strips private fields from planner; typical run **overall_score ≈ 0.967**, **private gap empty** vs reference when candidate includes invariant terms. |

**Current development** is usually on branch `solution_run_two` (or your main line) at **`v3-candidate-near-reference`** until the next tagged milestone.

## Commands

```bash
# List version branches
git branch --list "abd-maps-models-specs/*"

# Compare two versions (example)
git diff abd-maps-models-specs/v1-heuristic-v2-mm3..abd-maps-models-specs/v2-orchestrator -- skills/abd-maps-models-specs/

# Checkout a frozen snapshot (detached OK for inspection)
git checkout abd-maps-models-specs/v1-heuristic-v2-mm3
```

## Push to remote

Branches are local until pushed:

```bash
git push -u origin "abd-maps-models-specs/v0-phase4-map-model-spec"
git push -u origin "abd-maps-models-specs/v1-heuristic-v2-mm3"
git push -u origin "abd-maps-models-specs/v2-orchestrator"
# …etc.
```

After pushing, anyone can **`git fetch`** and **`git checkout`** the branch name to get that exact tree under `skills/abd-maps-models-specs/`.
