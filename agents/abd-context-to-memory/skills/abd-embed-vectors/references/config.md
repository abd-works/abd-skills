# Configuration

## Topic root (where memory lives)

There is **no** persisted “workspace” in this skill. Scripts resolve a **topic root** (`ROOT` in `_config.py`) in this order:

1. **`CONTENT_MEMORY_ROOT`** — environment variable (automation / CI / one place to point all commands at a corpus).
2. **Current working directory** — if the env var is unset.

**Per-run override:** pass **`--path`** (or `--rag` / `--memory` where documented) so the corpus folder is explicit; that wins over defaults.

If the user has **not** said where the corpus lives and **has not** set `CONTENT_MEMORY_ROOT`, **ask** which folder holds the documents (or confirm **cwd**) **before** converting—do not silently treat an arbitrary shell cwd as the corpus. Same rule applies whenever generic “workspace” instructions would have applied: substitute this **topic root** guidance instead.

**`index_memory.py`**, **`draft_chunking_spec.py`**, **`embed_and_index.py`**, and **`search_memory.py`** use `ROOT` when flags are omitted; embed/search use `<ROOT>/memory` and `<ROOT>/memory/rag` by default.

Markdown, `context_chunking_spec.yaml`, `memory/`, and `memory/rag/` are created **under that topic folder**—not inside the skill package.

## Where embeddings go

Embedding writes under **`<topic_folder>/memory/rag/`** when you pass `--path <topic_folder>` to `index_memory.py`, or under **`<ROOT>/memory/rag/`** when you rely on the defaults above. The skill package does not hold corpus data; each project keeps its own index beside its content.

## Required

Set `OPENAI_API_KEY` for embedding. Place it in any of:

- `<repo>/conf/.secrets`
- `<repo>/conf/.env`
- `<skill_root>/.env`
- `cwd/.env`

`_config.py` loads it automatically.
