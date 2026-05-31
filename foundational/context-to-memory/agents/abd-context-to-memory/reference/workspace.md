The **default corpus folder** (topic root: where `markdown/`, `memory/`, etc. live) is **not** a separate Open Agent Skill. It is **agent policy**, implemented by **`_config.py`** in this package.

**Primary setup:** copy **`conf/.secrets.example`** → **`conf/.secrets`** and set:

- **`OPENAI_API_KEY`** — required for embed/search
- **`CONTENT_MEMORY_ROOT`** — optional but recommended: absolute path to your topic/corpus folder

Use **`KEY=value`** lines (no spaces around `=`). Files are loaded **before** scripts resolve `ROOT`; you normally **do not** need shell `export`. The key name stays **`CONTENT_MEMORY_ROOT`** (same as in code); only the **storage** is the config file, not “set an env var by hand” as the default story.

**Overrides (per run):** pass **`--path`**, **`--memory`**, or **`--rag`** on the relevant script so a single command targets a different folder without editing `.secrets`.

**Fallback:** `cd` to the topic folder before running (scripts use `cwd` when `CONTENT_MEMORY_ROOT` is unset).

**Canonical detail for skills:** each stage skill’s **`SKILL.md`** points here and to **[config.md](../../skills/abd-context-to-memory/abd-embed-vectors/references/config.md)** so authors keep workspace behavior consistent with this agent.
