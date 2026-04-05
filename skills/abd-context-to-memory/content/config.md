# Configuration

**File:** `skill-config.json` (skill root)

## Paths (shareable config)

| Key | Purpose |
|-----|---------|
| `content_memory_root` | Local path to Assets folder. Use `~/OneDrive - Agile by Design/Shared Documents/Assets` so `~` expands to each user's home — config is shareable. |
| `content_memory_sharepoint_url` | SharePoint URL for the same folder. For documentation: sync from this URL; the portable path above will work if OneDrive is in the default location. |
| `content_memory_rag_path` | Optional. **Aggregate** hub RAG directory (FAISS + `metadata.json`). If set, the integrated index is written here instead of `{content_memory_root}/assets/rag`, so teams share one synced copy (OneDrive/SharePoint). |
| `skill_space_path` | Project/skill-space root. When set and no folder is specified for `index_memory.py`, the skill automatically runs on `{skill_space_path}/context`. Falls back to `abd-story-synthesizer/skill-config.json` when both skills are deployed. |

**Per-hub RAG** (multiple content hubs): **`conf/content_memory_roots.json` in the workspace** (e.g. `abd_content/conf/`), not in the skill package. Template: `agilebydesign-skills/conf/content_memory_roots.example.json`. Resolution order: `CONTENT_MEMORY_ROOTS_CONFIG` → `CONTENT_MEMORY_WORKSPACE` → `CONTENT_MEMORY_ROOT` (hub) → walk cwd for `conf/content_memory_roots.json` → optional `conf/content_memory_workspace.json` with `workspace_root`. Each root may include `rag_path` for that hub’s aggregate index; optional `junctions_dir` (default `assets`).

**RAG data** (aggregate): `index.faiss`, `embeddings.npy`, `metadata.json` under the resolved aggregate folder (see above). Per-topic `--memory` indexes still use `{root}/memory/rag/`.

**Overrides:**
- `CONTENT_MEMORY_ROOT` — overrides `content_memory_root`
- `CONTENT_MEMORY_RAG_PATH` — overrides aggregate RAG directory (highest priority)
- `CONTENT_MEMORY_ROOTS_CONFIG` — absolute path to a workspace `content_memory_roots.json`
- `CONTENT_MEMORY_WORKSPACE` — directory of the workspace (loads `conf/content_memory_roots.json` there)
- `SKILL_SPACE_PATH` — overrides `skill_space_path`
