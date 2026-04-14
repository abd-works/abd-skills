# `content/` — per-skill narrative (purpose, outline, role, principles)

These markdown files at **`content/*.md`** are **templates** created by **`scaffold_skill.py`**. Replace placeholders (`{{skill_name}}`, …) and extend the content so they describe **this** skill’s purpose, outline, role, and principles.

Frozen shared norms live under **`content/parts/library/base/`** (copied from **abd-skill-builder**). Additional cross-cutting docs can be added at **`content/parts/library/*.md`** and listed in **`skill-config.json` → `library_files`**.

Merge resolution for these filenames is documented in **`scripts/base/instructions.py`** → **`_resolve_library_md`**.
