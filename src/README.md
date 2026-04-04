# Shared source (`src/`)

Canonical implementations that are **copied into one or more skills** under `skills/*/scripts/` live here. Per-skill installs (for example via `npx skills add … --skill <name>`) only include that skill’s folder, so shared code is **vendored** into the skill at build time.

## Layout

| Path | Role |
|------|------|
| `src/drawio/` | DrawIO class-diagram helpers (`drawio_tools`, `model_to_drawio`, `drawio_class_cli`) used by **abd-story-synthesizer** (and optionally more skills later). |

## Workflow

1. **Edit only** the files under `src/` (see the “CANONICAL SOURCE” docstring in each module).
2. **Regenerate** copies and commit both canonical and vendored files:
   ```bash
   python scripts/sync_drawio_vendor.py
   ```
   Or from the repo root:
   ```bash
   python build.py
   ```
3. **Verify** before pushing (CI runs this too):
   ```bash
   python scripts/sync_drawio_vendor.py --check
   ```
   Or:
   ```bash
   python build.py check
   ```

Vendored files get a **generated** header (timestamp, regenerate command). Do not edit those files by hand.

## Adding a new consumer skill

1. Add a row to `VENDOR_FILES` in `scripts/sync_drawio_vendor.py` (`src/...` → `skills/.../scripts/...`).
2. Run `python scripts/sync_drawio_vendor.py` and commit.
