# Python environment (agentic-skill-builder)

## Standard layout for this repo

- **`pyproject.toml`** — project metadata and dependencies (PEP 621).
- **`.venv/`** — local virtual environment (create at repo root; **never commit**).
- **`requirements/`** — optional lock-style or layered requirement files if you want `pip install -r` without PEP 621 tools.

This project does **not** use a `lib/` or `bin/` folder for third-party packages. The conventional approach is:

1. Create a venv: `python -m venv .venv`
2. Activate (Windows PowerShell): `.venv\Scripts\Activate.ps1`
3. Install in editable mode: `pip install -e ".[dev]"`

Vendored wheels (rare) could live under `vendor/` if needed; prefer PyPI + lock files.

## Why not `lib/` for dependencies?

In Python, installed packages live **inside the active environment** (`site-packages`), not copied into the project tree. Keeping dependencies in `.venv` avoids duplicating “standard” layout with nonstandard `lib/python` trees unless you have a strong reason (offline airgap, etc.).
