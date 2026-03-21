# Step 6 — Deepen AI-only (no merge scripts)



**Binding process rule.** Violating this is a process failure, not a style preference.



## Required (pick one path)



- **Path A — Chat / agent session:** Read the pair’s chunks and `map-model-spec.json`, run Pass 1–4 reasoning, and **edit** `map-model-spec.json` and `map-model-spec.md` directly (patch sections, or equivalent).

- **Path B — Listed chat API driver:** Run **`scripts/deepen_pair_chat_api.py`** (same class of tool as `classify_chunks.py`). It batches this pair’s chunks using the **same token budgeting as Step 5** (~8k tokens of chunk text per batch, oversize chunks alone). **Context model:** each **observation** call includes the **full** current shard: always the **entire** `module` for the pair plus the **epic slice** for that run (whole pair when under size limit; otherwise a **sub_epic** subtree, or a **story batch** under a node if still too large — `--split-threshold-chars`, default 120000 compact JSON chars; `0` disables splitting). **Synthesis** returns **one** JSON object per shard with **complete** `module` and `epic` for that scope. **Single shard:** replace the stored pair from synthesis. **Multiple shards:** each run is **pinned** to a **sub_epic** path; the driver **nests** that synthesis **`module`** under **`sub_modules`** mirroring that path (story batches → parent sub_epic chain), then **merges** by **`sub_modules`** / **concept** name; pair **`chunk_ids`** are **unioned**; **`epic`** is **grafted** by scope. **`deepen_pair_chat_api_run`** records **`run_boundary`**: **`single_run`** vs **`isolated_runs`**, **`module_merge_policy`**, **`isolated_runs[]`** with per-shard **`run_boundary_tag`** (**`single_run`** / **`isolated_run`**) and **`run_boundary_index`**, **`epic_root_name`**, **`scope_hierarchy`** (ordered **epic → sub_epic → … → stories_batch**), **`hierarchy_display`** (same chain as one string), plus **`reconciliation_hint`** and **`module_merge_note`** when multiple shards ran so a later **Integrate/Harmonize** (or dedicated reconciliation) step knows how much cross-run stitching may be needed. The JSON shard payload’s **`deepen_shard_scope`** mirrors that hierarchy. Use **`--dry-run`** to print the planned shards without calling the API. Re-run a deepen by running the script again or Path A again — not ad-hoc merge helpers.



## Forbidden



- **Any unofficial** one-off **script** whose **purpose** is to programmatically **merge, splice, bulk-inject, or regenerate** Step 6 content **without** going through the chat API for authoring (e.g. `step6_pairs_*.py` replay merges, idempotent JSON splices that **fabricate** domain text in code).

- **Path B is not optional glue:** If you use code for Step 6, it must be **`deepen_pair_chat_api.py`** (or future listed equivalents in `AGENTS.md`), not a new private merge script.



## Allowed code



- **`classify_chunks.py`** (Step 5) — chat API + deterministic merge of **model-returned** chunk evidence.

- **`deepen_pair_chat_api.py`** (Step 6, optional) — chat API + apply **model-returned** `module`/`epic` (single shard: replace pair; multi-shard: **sub_module** shells per sub_epic pin, merge, union `chunk_ids`, graft `epic`).

- **`build_chunk_index.py`**, **scanners** — indexes and validation after the spec is updated.



## Rationale



Step 6 is defined as an **AI pass** over evidence and the spec. Merge scripts hide reasoning, rot when the schema shifts, and train agents to be lazy. **Do the fucking work** every time.

