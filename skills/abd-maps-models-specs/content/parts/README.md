# Normative content (`content/parts/`)

**`process.md`** is the process summary table (one row per **phase**); **`phases/*.md`** hold **steps** inside each phase. **Filenames and H1 titles** use **descriptive slugs**; pipeline order lives in **`process.md`** and in **`scripts/build.py`** (`PHASE_FILES`).

**Build output:** `python scripts/build.py` produces **`../built/agents-staged.md`**, **`../../AGENTS.md`**, and **`../built/phases/*.md`** (per-phase bundles: operator role + `rules/*.md` filtered by YAML `phase_files` + library + phase steps + **`library/critical-quality-steps.md`** and per-phase focus — see `../built/phases/README.md` and `../../rules/README.md`). Operator blocks are **removed** from the **merged** agent output only; each **`../built/phases/<phase>.md`** still includes the role text explicitly (see `../built/README.md`).

**Link resolution:** In-repo links use **`library/...`** or **`../../docs/...`** depending on file; **`AGENTS.md`** rewrites paths for the skill root. For navigation from the skill root, open **`AGENTS.md`** or a single **`content/built/phases/<phase>.md`** when you need one phase only.
