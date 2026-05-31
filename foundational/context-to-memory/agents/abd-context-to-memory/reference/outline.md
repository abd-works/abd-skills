**How it works** (each step is distinct; order matters):

- **Convert** supported sources to Markdown (under `markdown/` in the source tree) — skill **abd-convert-to-markdown**.
- **Draft** a structure-aware chunking spec: `context_chunking_spec.yaml` — **abd-chunk-markdown**.
- **Strategy pass (optional):** review or edit that YAML *before* chunking and embedding.
- **Chunk** Markdown into `memory/` with front matter when a spec applies — **abd-chunk-markdown**.
- **Embed** chunk vectors into a **local FAISS** index under `<source_folder>/memory/rag/` — **abd-embed-vectors**.
- **Search** semantically over the index — **abd-search-memory**.

**Skills (route here by stage):**

| Skill | `SKILL.md` |
| --- | --- |
| Convert | [skills/abd-convert-to-markdown/SKILL.md](../../skills/abd-context-to-memory/abd-convert-to-markdown/SKILL.md) |
| Chunk | [skills/abd-chunk-markdown/SKILL.md](../../skills/abd-context-to-memory/abd-chunk-markdown/SKILL.md) |
| Embed | [skills/abd-embed-vectors/SKILL.md](../../skills/abd-context-to-memory/abd-embed-vectors/SKILL.md) |
| Search | [skills/abd-search-memory/SKILL.md](../../skills/abd-context-to-memory/abd-search-memory/SKILL.md) |

**Where to read more:** each skill's **`SKILL.md`** documents its scripts and flags. Stage references: **`skills/abd-context-to-memory/<skill-name>/references/`**.
