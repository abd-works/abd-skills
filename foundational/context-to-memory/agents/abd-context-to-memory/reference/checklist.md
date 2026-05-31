**Agent orchestration only.** This checklist lives in **`agents/abd-context-to-memory/reference/`** with the other **agent** slices. It is **not** the **abd-skill-builder** pattern (`generate.py`, `phase_files`, `…/progress/` under `active_skill_workspace`).

Use it to track one **ingest run** over a **topic root** (`CONTENT_MEMORY_ROOT` or `--path`). Copy into chat or a run log under `<topic_root>/docs/` if you need persistence.

### Full pipeline (typical)

- [ ] **Config** — `conf/.secrets` has `OPENAI_API_KEY`; optional `CONTENT_MEMORY_ROOT` (see **Workspace** above).
- [ ] **Strategy** — User chose **strategy pass** vs **straight-through** (ask once if unclear).
- [ ] **Convert** — `markdown/` populated; structure acceptable or bespoke / preprocess loop applied.
- [ ] **Spec** — `memory/context_chunking_spec.yaml` drafted or reused; YAML reviewed if strategy pass.
- [ ] **Chunk** — `memory/` chunks sane (count, splits); run quality loop if not.
- [ ] **Embed** — FAISS index under `memory/rag/` built.
- [ ] **Search** — Optional smoke query if validating retrieval.

### Where things live (agent vs skills)

| Layer | Location |
| --- | --- |
| **Orchestration** (order, gates, this checklist) | **`reference/*.md`** here → merged **`AGENTS.md`** |
| **Stage how-to** (scripts, flags, YAML semantics) | **`skills/abd-context-to-memory/abd-*/SKILL.md`** and **`skills/abd-context-to-memory/abd-*/references/`** |

### Optional engagement artifacts

- **Corrections / run notes** — Under the **topic root** (e.g. `docs/corrections-log.md`), not inside this agent package.
