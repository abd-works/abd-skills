# Set workspace

**You will** decide **where** the solution lives on disk and land **`solution.conf`** so every later step resolves paths the same way.

**You must not** finalize the full list of evidence files here—that happens when you finish **context markdown** and record `**manifest_sources[]`** there (see [context-markdown.md](context-markdown.md)).

**You will:**

1. **Choose the project workspace** — One folder that will contain `**solution.conf**`. This is **not** the skill install directory; it is the repo or folder where your spec and `solution.conf` live. The skill package records **only** that absolute path in `**conf/abd-config.json**` → `**active_skill_workspace**`. There is no fallback or inference—if it is unset, tooling fails. **You must** treat that folder as the root for every relative path in `**solution.conf**`.
2. **Create or edit `solution.conf` in that workspace.** **You must** wire at minimum:
   - `**context_path**` and output conventions (where context artifacts like chunks and the index will live).
   - `**context_chunking_spec**` — pointer to the chunking YAML (default basename `**context_chunking_spec.yaml**` beside `**solution.conf**`). The YAML **contents** are drafted and reviewed in [context-chunking-approach.md](context-chunking-approach.md); in this phase **you should** only ensure the **pointer** exists so tooling knows where to read it.
   - `**manifest_sources[]`** — **You may** start **empty** or as a stub. The **authoritative list of which Markdown files are your corpus** (and each `**role**`) is finalized when you complete **context markdown**: that is where **you will** record **where** sources came from and **where** canonical `**.md**` landed (see end of [context-markdown.md](context-markdown.md)).

**Command line:** From the **skill package root** (the folder that contains `**scripts/**` and `**conf/**`):

- `python scripts/set_workspace.py` — **You will** use this to print the configured workspace path. Exits **non-zero** if `**active_skill_workspace**` is missing or empty.
- `python scripts/set_workspace.py <path>` — **You will** use this to set `**active_skill_workspace**` in `**conf/abd-config.json**` to the **resolved absolute** path of `**<path>**`. **You must** pass an existing directory (the folder that will contain or already contains `**solution.conf**`). Legacy keys (`solution_workspace`, `skill_space_path`) are removed on save.

This entry point matches the idea of `**skills/abd-solution-modeler/scripts/workspace.py**`; there is no separate “storage synchronizer” script in this repository.

**You should** treat **`scripts/_config.py`** (skill package root — the directory that contains `**scripts/**` and `**conf/**`) as how emitters and validators resolve paths consistently. [canonical-context.md](canonical-context.md) assumes this workspace and `**solution.conf**` already exist.

## See also

- **[context-markdown.md](context-markdown.md)** — Conversion and `**manifest_sources**` (evidence locations).
- **[context-chunking-approach.md](context-chunking-approach.md)** — Structural inventory and `**context_chunking_spec**` contents.
- **[canonical-context.md](canonical-context.md)** — Context package (chunks, index, validate).
