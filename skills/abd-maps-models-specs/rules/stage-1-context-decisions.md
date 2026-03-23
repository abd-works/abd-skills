---
rule_id: stage-1-context-decisions
phase_files:
  - context-chunking-approach.md
  - canonical-context.md
---

## Stage 1 — source structure (Phase 0) and Phase 1 context package

**Process phases:** Phase **0** (scan Markdown, **chunking rules**) and Phase **1** (build chunks + index) in [`content/parts/process.md`](../content/parts/process.md).

**Phase 0** is **structural**: understand large sources and **encode `context_chunking_spec`**—not a pass/fail “readiness” gate. **Phase 1** **materializes** the contract: chunk files and `context_index.json` (plus manifest) must match [`context-spec.md`](../content/parts/library/context-spec.md). **`scripts/scanners/context_index_contract.py`** (legacy wrapper: `validate_context_contract.py`) is the **hard gate** when the index exists — see **`rules/scanners.json`**.

**No vocabulary or types here.** Stage 1 does not introduce inheritance, `concepts[]`, or behavioral story text. You only **package and pin** evidence that later stages will cite by stable `chunk_id`.

Older pipelines mixed evidence layout with **map-model-spec** shapes. This skill **separates** Stage 1 from Stage 2 (terms, mechanisms, story map). Do not import checklists that assume a full module/epic tree exists before `context_index.json` exists.

**DO**

- Complete Phase 0 **chunking approach** (spec aligned with source structure) before or alongside first Phase 1 build.
- Make Phase 1 outputs consistent enough that **`context_index_contract.py`** passes when the index is present.

```json
{
  "index_path": "context_index.json",
  "chunk_count": 120,
  "manifest_sha256": "…"
}
```

(Representative: index + manifest aligned with chunk files.)

**DON'T**

- Declare Phase 1 “done” while chunk hashes and `context_index.json` disagree, or start **`concepts[]`** / shaped story map work before the index is stable.

```json
{
  "context_index.json": "stale — chunk file modified after index build"
}
```

Do not start Phase 2 vocabulary work until the index and chunks are **reconciled** and **`context_index_contract.py`** passes.
