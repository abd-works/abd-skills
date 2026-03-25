# About this folder

This directory is **documentation and small examples** (`parallel-layout-example/`). **`index_memory`** still creates junctions under **`<hub>\assets\`** (see below), but this folder can also hold a **manual** junction so the topic memory is visible next to the skill:

- **`Agile Thinking`** — directory junction → `…\01 Agile Practices\Agile Thinking\memory` (OneDrive topic memory). Recreate with:  
  `cmd /c mklink /J "skills\abd-context-to-memory\assets\Agile Thinking" "<absolute path to …\Agile Thinking\memory>"`
- **`Canadian Banking Engineering`** — directory junction → `…\Scotiabank\Canadian Banking Engineering\memory`. Recreate with:  
  `cmd /c mklink /J "skills\abd-context-to-memory\assets\Canadian Banking Engineering" "<absolute path to …\Canadian Banking Engineering\memory>"`
- **`GTB`** — directory junction → `…\Scotiabank\GTB\memory`. Recreate with:  
  `cmd /c mklink /J "skills\abd-context-to-memory\assets\GTB" "<absolute path to …\GTB\memory>"`

## One aggregate RAG (not per topic)

Per-topic **`memory\rag`** under a topic folder is optional. For **one** FAISS index over **all** topic junctions under this skill’s `assets\`, `skill-config.json` sets **`content_memory_rag_path`** to **`assets\rag`** here. Build or refresh:

```powershell
cd C:\dev\agilebydesign-skills\skills\abd-context-to-memory
$env:CONTENT_MEMORY_ROOT = (Get-Location).Path
python scripts/embed_and_index.py --replace
```

`search_memory.py` resolves the index via **`aggregate_rag_dir_for_root`** (same config). Ingest topics with **`index_memory.py --path <topic> --no-junction`** (embedding is off by default; add **`--embed`** only if you want per-topic `memory\rag`).

## Where the junction actually appears

After `index_memory.py --path <topic>`, the script creates:

**`<hub>\assets\<topic_folder_name>`** → junction → **`<topic>\memory`**

- **`<hub>`** is **`--memory-root`**, else **`ABD_CONTENT_ROOT`**, else **current working directory** when you run Python.
- Example: `--memory-root C:\dev\agilebydesign-skills` →  
  **`C:\dev\agilebydesign-skills\assets\Agile Thinking`** → `…\Agile Thinking\memory`

**Default ingest:** `index_memory` does **not** put junctions under **`skills\abd-context-to-memory\assets\`** unless **`--memory-root`** includes this skill path. The repo’s **`agilebydesign-skills\assets\`** (next to `skills\`) is the usual hub `assets` folder. A **`skills\abd-context-to-memory\assets\Agile Thinking`** junction is optional and maintained separately for convenience in this workspace.

If a junction failed before, common causes were: resolving paths through an **`assets`** junction into OneDrive (fixed in `scripts/memory_junction.py`), **OneDrive lock**, or **access denied** on the target folder.

`junctions_dir` defaults to **`assets`** (see `conf/content_memory_roots.json`); override with **`CONTENT_MEMORY_JUNCTIONS_DIR`** if needed.

---

## Example: OneDrive topic “Agile Thinking”, markdown already done

**Topic root** (originals + converted markdown under **`markdown/`** at the topic root, parallel to **`memory/`**, and/or sibling `.md` — chunker picks one per stem):

`C:\Users\thoma\OneDrive - Agile by Design\Shared Documents\Assets\01 Agile Practices\Agile Thinking`

**Local hub** (clone or workspace root that should contain the junction folder — often the same repo you use as `path` in `content_memory_roots.json`):

`C:\path\to\your\hub` → contains `assets\` (junctions) and `conf\content_memory_roots.json`.

After a successful run, the skill creates:

- **Chunks + per-topic RAG:**  
  `...\Agile Thinking\memory\` (under the topic folder on OneDrive)
- **First junction (default):**  
  `<hub>\assets\Agile Thinking` → junction → `...\Agile Thinking\memory`

**PowerShell — chunk + index only (skip slow re-convert):**

```powershell
$repo  = "C:\dev\agilebydesign-skills"
$topic = "C:\Users\thoma\OneDrive - Agile by Design\Shared Documents\Assets\01 Agile Practices\Agile Thinking"
$hub   = "C:\path\to\your\hub"   # folder whose child is assets\

python "$repo\skills\abd-context-to-memory\scripts\index_memory.py" `
  --path $topic `
  --memory-root $hub `
  --skip-convert
```

If your **current directory** is already the hub, you can omit `--memory-root` and run from `$hub`.

**Optional:** `--no-junction` if you only want `memory\` on OneDrive and no link under `<hub>\assets\` yet.

**Requirements:** RAG deps and `OPENAI_API_KEY` for the embed step (see repo `conf/` and `requirements-rag.txt`). SharePoint links in chunks assume `sharepoint_mapping.json` is set up for that OneDrive prefix.
