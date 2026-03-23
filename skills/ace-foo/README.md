# ace-foo

Generic **example** skill in the **abd-skill-builder** layout (`content/parts/`, **`skill-config.json`**, **`scripts/build.py`**, **`conf/`**).

## Delivery and merge order

**`scripts/build.py`** assembles **`AGENTS.md`** in this order:

1. **`content/parts/process.md`**
2. **`content/parts/phases/<slug>.md`** for each slug in **`PHASE_FILES`** inside **`scripts/build.py`** (currently **`workspace-and-config`** only)
3. **`content/parts/library/*.md`** in **`LIBRARY_FILES`** order inside **`scripts/build.py`**

After editing sources under **`content/parts/`**, run:

```bash
python scripts/build.py
```

**`delivery.mode`** in **`skill-config.json`** is **`static_built`**. This skill does not check in a separate **`content/built/`** tree; the merge output is **`AGENTS.md`** at the skill root.

## AI-chat phase prompt

```bash
python scripts/generate.py --phase workspace-and-config
```

## Operator

Configured for **`agentic-skill-builder`**-style checks: Python compile on **`scripts/`**, **`build.py`**, then **`scripts/scanner_smoke.py`**.
