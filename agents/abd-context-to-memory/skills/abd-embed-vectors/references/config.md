# Configuration

## Topic root (where memory lives)

There is **no** persisted “workspace” object in the database sense. Scripts resolve a **topic root** (`ROOT` in `_config.py`) after loading **config files** into the process environment.

### Config files first (recommended)

**Policy** is defined in the **agent**: **[AGENTS.md](../../../AGENTS.md)** → *Workspace (topic root) — config first*.

Set a stable default corpus by copying **`conf/.secrets.example`** to **`conf/.secrets`** under **`agents/abd-context-to-memory/`** and adding lines such as:

```text
OPENAI_API_KEY=sk-...
CONTENT_MEMORY_ROOT=C:\path\to\your\corpus
```

Format: **`KEY=value`**, no spaces around `=`. `_config.py` loads these **before** resolving `ROOT`, so you normally **do not** rely on shell `export` for `CONTENT_MEMORY_ROOT`. The **name** of the setting remains **`CONTENT_MEMORY_ROOT`** (what the code reads); the **authoritative place** to set it for day-to-day use is **`conf/.secrets`** (or **`conf/.env`**), not “only an environment variable.”

Load order (see `_config.py`):

1. `<agent>/conf/.secrets`
2. `<agent>/conf/.env`
3. **Skill scripts:** `<that_skill>/.env`, then `cwd/.env`. **Orchestrator `scripts/`:** `<agent>/.env`, then `cwd/.env`.

### How `ROOT` is chosen (after load)

1. **`CONTENT_MEMORY_ROOT`** if set (typically from **`conf/.secrets`**)
2. **Current working directory** if unset

**Per-run override:** pass **`--path`** (or **`--rag`** / **`--memory`** where documented); that wins for that command.

If the user has **not** said where the corpus lives and **`CONTENT_MEMORY_ROOT`** is not in config, **ask** which folder holds the documents (or confirm **cwd**) **before** converting — do not silently treat an arbitrary shell cwd as the corpus.

**`index_memory.py`**, **`draft_chunking_spec.py`**, **`embed_and_index.py`**, and **`search_memory.py`** use `ROOT` when flags are omitted; embed/search use `<ROOT>/memory` and `<ROOT>/memory/rag` by default.

Markdown, `context_chunking_spec.yaml`, `memory/`, and `memory/rag/` are created **under that topic folder** — not inside the skill package.

## Where embeddings go

Embedding writes under **`<topic_folder>/memory/rag/`** when you pass `--path <topic_folder>` to `index_memory.py`, or under **`<ROOT>/memory/rag/`** when you rely on the defaults above. The skill package does not hold corpus data; each project keeps its own index beside its content.

## Required

Set `OPENAI_API_KEY` for embedding. Place it in **`conf/.secrets`** (preferred) or any file in the load order above. `_config.py` loads it automatically.
