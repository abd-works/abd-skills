# `content/built/` — generated merge outputs

All **built** artifacts for this skill live under this directory (do not edit by hand; run **`python scripts/build.py`** or **`python scripts/build.py --merge-only`**).

| Path | Role |
| --- | --- |
| **`agents-staged.md`** | Intermediate merge: `process.md` + source phase bodies (same body as root **`AGENTS.md`** below its title) |
| **`phases/<slug>.md`** | Per-phase static prompt bundle (role → phase → library → rules → principles for Stage 2+; Stage 1 ends after rules) |
| **`phases/README.md`** | Describes phase bundle layout |
