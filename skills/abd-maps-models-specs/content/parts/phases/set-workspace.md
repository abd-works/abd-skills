# Set workspace

**You will** decide **where** the solution lives on disk and land **`solution.conf`** so every later step resolves paths the same way.

**You must not** finalize the full list of evidence files here—that happens when you finish **context markdown** and record `**manifest_sources[]`** there (see [context-markdown.md](context-markdown.md)).

**You will:**

1. **Choose the active skill workspace** — One folder that will contain `**solution.conf**`. The skill package points at it with `**conf/abd-config.json**` → `**active_skill_workspace**` (or the deprecated aliases documented in `scripts/_config.py`). **You must** treat that folder as the root for every relative path in `**solution.conf**`.
2. **Create or edit `solution.conf` in that workspace.** **You must** wire at minimum:
   - `**context_path**` and output conventions (where context artifacts like chunks and the index will live).
   - `**context_chunking_spec**` — pointer to the chunking YAML (default basename `**context_chunking_spec.yaml**` beside `**solution.conf**`). The YAML **contents** are drafted and reviewed in [context-chunking-approach.md](context-chunking-approach.md); in this phase **you should** only ensure the **pointer** exists so tooling knows where to read it.
   - `**manifest_sources[]`** — **You may** start **empty** or as a stub. The **authoritative list of which Markdown files are your corpus** (and each `**role**`) is finalized when you complete **context markdown**: that is where **you will** record **where** sources came from and **where** canonical `**.md**` landed (see end of [context-markdown.md](context-markdown.md)).

**Command line:** From the **skill package root** (the folder that contains `**scripts/**` and `**conf/**`):

- `python scripts/set_workspace.py` — **You will** use this to print the configured workspace path string (first non-empty among `**active_skill_workspace**`, then deprecated `**solution_workspace**` / `**skill_space_path**`).
- `python scripts/set_workspace.py <path>` — **You will** use this to set `**active_skill_workspace**` in `**conf/abd-config.json**` to `**<path>**` (resolved; stored **relative to the skill package** when that keeps the value portable, otherwise absolute). The script also writes the same string to `**solution_workspace**` for tools that still read the legacy key. **You must** pass an existing directory for `**<path>**` (the folder that will contain or already contains `**solution.conf**`).

This entry point matches the idea of `**skills/abd-solution-modeler/scripts/workspace.py**`; there is no separate “storage synchronizer” script in this repository.

**You should** treat **`scripts/_config.py`** (skill package root — the directory that contains `**scripts/**` and `**conf/**`) as how emitters and validators resolve paths consistently. [canonical-context.md](canonical-context.md) assumes this workspace and `**solution.conf**` already exist.

## See also

- **[context-markdown.md](context-markdown.md)** — Conversion and `**manifest_sources**` (evidence locations).
- **[context-chunking-approach.md](context-chunking-approach.md)** — Structural inventory and `**context_chunking_spec**` contents.
- **[canonical-context.md](canonical-context.md)** — Context package (chunks, index, validate).
