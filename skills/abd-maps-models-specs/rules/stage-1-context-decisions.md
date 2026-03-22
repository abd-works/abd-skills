---
rule_id: stage-1-context-decisions
phase_files:
  - context-readiness.md
  - canonical-context.md
---

## Stage 1 — context readiness and frozen package

**Process phases:** Phase **0** (readiness) and Phase **1** (canonical context build) in [`content/parts/process.md`](../content/parts/process.md).

**Readiness is a real decision.** Phase 0 produces metrics, samples, and an honest **adopt / extend-and-freeze / rebuild** position. If the corpus or chunk/index plumbing fails the principles in [`principles-and-rules.md`](../content/parts/library/principles-and-rules.md), you **record that** and fix upstream—not downstream modeling.

**Phase 1 delivers a single enforceable contract.** Chunk files and `context_index.json` (plus manifest and chunking spec) must match [`context-package.md`](../content/parts/library/context-package.md). `validate_context_contract.py` is the **hard gate** when the index exists.

**No vocabulary or types here.** Stage 1 does not introduce inheritance, `concepts[]`, or behavioral story text. You only **package and pin** evidence that later stages will cite by stable `chunk_id`.

Older pipelines mixed evidence layout with **map-model-spec** shapes. This skill **separates** Stage 1 from Stage 2 (terms, mechanisms, story map). Do not import checklists that assume a full module/epic tree exists before `context_index.json` exists.

**DO**

- Exit Phase 0 with an explicit readiness position and honest gaps.
- Make Phase 1 outputs consistent enough that **`validate_context_contract.py`** passes when the index is present.

```json
{
  "index_path": "context_index.json",
  "chunk_count": 120,
  "manifest_sha256": "…"
}
```

(Representative: index + manifest aligned with chunk files.)

**DON'T**

- Declare Phase 1 “done” while chunk hashes and `context_index.json` disagree, or start **`concepts[]`** / behavioral story work before the index is stable.

```json
{
  "context_index.json": "stale — chunk file modified after index build"
}
```

Treat as **not ready** for Phase 2 until rebuilt or reconciled.
