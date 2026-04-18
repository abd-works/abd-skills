# abd-diagrams

OOAD + Draw.io class/sequence diagram norms (`content/parts/`), `scripts/drawio_cli.py`, templates, and merged **`AGENTS.md`**.

## Cursor: deploy this skill (Windows)

Cursor loads skills from **`%USERPROFILE%\.cursor\skills\<name>\`**. This repo is the source of truth; use a **directory junction** so Cursor always sees the live skill tree:

```powershell
New-Item -ItemType Junction `
  -Path "$env:USERPROFILE\.cursor\skills\abd-diagrams" `
  -Target "c:\dev\agilebydesign-skills\skills\abd-diagrams" `
  -Force
```

Adjust the `-Target` path if your clone lives elsewhere. Remove the old junction before re-pointing: `Remove-Item $env:USERPROFILE\.cursor\skills\abd-diagrams` (junction only; does not delete the repo).

## Build

```bash
python scripts/build_instructions.py
```

Writes **`AGENTS.md`** at the skill root and `content/built/AGENTS.md`.
