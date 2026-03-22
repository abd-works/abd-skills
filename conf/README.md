# Content memory — workspace configuration

**Hub lists and RAG paths are workspace-specific.** They do **not** live in this skill repo.

## Where configuration goes

| File | Location | Purpose |
|------|----------|---------|
| **`content_memory_roots.json`** | **Your workspace**, e.g. `abd_content/conf/content_memory_roots.json` | List of junction hubs: `path`, `rag_path`, optional `junctions_dir`. |
| **`content_memory_workspace.json`** | Optional, **your workspace** `conf/` | Pointer: `{ "workspace_root": "C:/dev/abd_content" }` — used when scripts run from another directory and cannot find `content_memory_roots.json` by walking cwd. |
| **`content_memory_roots.example.json`** | **This repo** (`conf/`) | Template only — copy into your workspace and edit paths. |

## How the skill finds `content_memory_roots.json`

Resolution order (first match wins):

1. **`CONTENT_MEMORY_ROOTS_CONFIG`** — absolute path to the JSON file.
2. **`CONTENT_MEMORY_WORKSPACE`** — directory of the workspace; loads `conf/content_memory_roots.json` or `content_memory_roots.json` there.
3. **`CONTENT_MEMORY_ROOT`** — usually the hub root (e.g. `abd_content`); loads `conf/content_memory_roots.json` under it.
4. Walk **current working directory** upward for `conf/content_memory_roots.json` or `content_memory_roots.json`.
5. Walk cwd for **`conf/content_memory_workspace.json`**, then read **`workspace_root`** and load that workspace’s `conf/content_memory_roots.json`.

There is **no** default hub list in the skill package.

## Schema (`roots[]`)

| Field | Required | Meaning |
|-------|------------|---------|
| **`path`** | Yes | Absolute path to the **hub root** (local). Set **`CONTENT_MEMORY_ROOT`** to this when running embed/search for that hub. |
| **`rag_path`** | Yes* | Where the **combined** FAISS index is stored. *Use env overrides if omitted. |
| **`label`** | No | Short name for docs. |
| **`junctions_dir`** | No | Local subfolder under `path` for topic junctions (default **`assets`**). |

## Overrides (single run)

| Env | Effect |
|-----|--------|
| **`CONTENT_MEMORY_ROOTS_CONFIG`** | Explicit path to `content_memory_roots.json`. |
| **`CONTENT_MEMORY_WORKSPACE`** | Workspace directory containing `conf/content_memory_roots.json`. |
| **`CONTENT_MEMORY_JUNCTIONS_DIR`** | Overrides `junctions_dir` for the current **`CONTENT_MEMORY_ROOT`**. |
| **`CONTENT_MEMORY_RAG_PATH`** | Overrides aggregate RAG directory. |

**Example workspace:** `C:\dev\abd_content\conf\content_memory_roots.json`
