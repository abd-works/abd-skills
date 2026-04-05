# Tests (`abd-skill-builder`)

This **`test/`** folder **is part of the skill repo** — it is not missing. It holds **`test_build_smoke.py`** (asserts **`build.py`** syncs root and **`content/built/`**) and the **fixture** below.

- **`test_build_smoke.py`** — run after `pip install -r requirements-dev.txt`.
- **`fixture/toy-polite-dialogue/`** — minimal valid skill (polite multi-phase dialogue) used as the **canonical example** for standards and structural checks in this repo.

```bash
pip install -r requirements-dev.txt
python -m pytest test/
```
