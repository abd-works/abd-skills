# parts/phases/built/ — derived per-phase prompts

Files here are **generated** by **`scripts/build.py`**. Sources of truth: **`skill-config.json`**
(`PHASE_LIBRARY_SLICES`, `phase_rules`, `every_phase_rules`, `phase_bundle`, …) and **`parts/`** / **`rules/`**.

Regenerate:

```bash
python scripts/build.py
```

**Runtime:** `python scripts/generate_prompt.py --phase <slug> --mode static` reads these files when present; otherwise assembles from sources (`dynamic`).
