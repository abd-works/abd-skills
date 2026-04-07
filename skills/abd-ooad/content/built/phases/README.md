# content/built/phases/ — derived per-phase prompts

Files here are **generated** by **`scripts/base/build.py`**. Sources of truth: **`skill-config.json`**
(`library_files`, `phase_library`, `phase_rules`, `every_phase_rules`, `phase_bundle`, …) and **`parts/`** / **`rules/`**.

Phase bodies under **`parts/phases/`** may link to library shards with ``../library/…``; the build rewrites those to
``../../parts/library/…`` in this folder so links resolve from **`content/built/phases/<slug>.md`**.

Regenerate:

```bash
python scripts/base/build.py
```

**Runtime:** `python scripts/base/generate.py --phase <slug> --mode static` reads these files when present; otherwise assembles from sources (`dynamic`).
