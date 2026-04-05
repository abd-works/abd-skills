# `library/required/` — extend for each skill

Files here are **scaffolded for every new skill** (see **`templates/skill-scaffold/content/parts/library/required/`**). They are **not** frozen copies: authors (or the AI) **fill and maintain** them for **this** skill’s story—purpose, outline, role, principles, and similar.

| Contrast | Role |
| --- | --- |
| **`library/base/`** | Copied verbatim from **abd-skill-builder** when you scaffold. **Do not** fork for one-off skills—refresh from the builder repo when shared norms change. |
| **`library/required/`** | **Start here** for skill-specific narrative. Same paths in every skill so tooling and **`skill-config.json`** stay predictable (`purpose.md`, `outline.md`, `role.md`, `principles.md`, …). |
| **`library/*.md` (root)** | Optional **extra** shards per skill (`library_files` / `phase_library`). Use when you add norms that are not in **base** or **required**. |

Resolution order for a filename (e.g. `outline.md`): **`library/<file>`** (override) → **`library/required/<file>`** → **`library/base/<file>`**. See **`scripts/base/instructions.py`** (`_resolve_library_md`).
