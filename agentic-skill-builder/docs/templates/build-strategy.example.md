# `build-strategy.json` (strategize payload)

Copy **`build-strategy.example.json`** to **`<skill-path>/conf/build-strategy.json`** (or pass **`--strategy-file`**).

- **`skill_purpose`** — Required for **`strategy_complete`** in the delivery graph (non-empty string). This is the **minimum** to mark strategize complete.
- **All other keys** — Same JSON object, **sibling fields**. They enrich the **`strategy`** passed to **`builder_manifest`**; they are **not** part of the **`skill_purpose`** text.

See **`../../README.md`** (Status → Strategizer) for the full convention.
