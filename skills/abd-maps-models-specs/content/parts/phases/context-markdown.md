# Context markdown

Produce **canonical Markdown** for each evidence source that is not already Markdown, then list those `.md` paths in `manifest_sources`. **Canonical context** assumes **Markdown** on disk.

**You will:**

1. Produce **canonical Markdown** for each source that is not already Markdown (fix encoding, strip or tag conversion artifacts you already know about, and land paths you can list in `manifest_sources`).
2. Keep conversion **repeatable**: use the same **Python** entry points below whenever you convert (dependency versions are fixed by a proper skill install). Run commands from the **abd-maps-models-specs skill package root** (the directory that contains `scripts/` and `conf/`). Paths you pass to `--file`, and paths in `manifest_sources[]`, are relative to the **skill workspace** (folder that contains `solution.conf`, from `conf/abd-config.json` → `active_skill_workspace`).

**Why two commands:** `--manifest` only works off a list that already exists in `solution.conf`. The **first** time you wire a workspace, that list is usually empty or not written yet—so you convert **named files** with `--file`, then **author** `manifest_sources[]` to point at the resulting `.md` files (and any sources that were already Markdown). Later, when the manifest is the source of truth and you add or swap non-Markdown paths there, `**--manifest`** is the point: one run converts every supported non-`.md` entry the manifest names (skips missing paths, already-`.md`, and unsupported extensions) without typing each path again.

**Exact commands (repeatable)**

Working directory: `skills/abd-maps-models-specs/` (repository path may vary; this folder must be current when you invoke Python).

**A — Greenfield or “not in the manifest yet”**  
**Point:** Convert a file you have on disk **before** `manifest_sources[]` describes it (or when you are landing files and will write the manifest afterward).

`python scripts/convert_sources_to_markdown.py --file <path>`

`<path>` is relative to the skill workspace unless it is absolute. Example: `python scripts/convert_sources_to_markdown.py --file docs/handbook.pdf`

Repeat for each non-Markdown source as needed. Then edit `solution.conf` and set `manifest_sources[]` to the **Markdown** paths canonical context should read.

**B — Manifest already lists the corpus**  
**Point:** Refresh conversion for **everything the manifest already points at**—typical after you add new `.pdf` / `.docx` / … paths to `manifest_sources[]` or re-run after upstream edits.

`python scripts/convert_sources_to_markdown.py --manifest`

Still **update** any `path` values to the `.md` files after conversion; the script does **not** rewrite `solution.conf`.

**Behavior:** writes `<stem>.md` beside each converted source and prefixes output with `<!-- Source: … -->` for provenance.

For SharePoint / OneDrive fetch, chunk-to-memory layout, or vector RAG, use **abd-context-to-memory** instead and record **its** exact commands the same way.

**What goes in `manifest_sources[]`:** After conversion (and for any sources that were already Markdown), **`solution.conf` → `manifest_sources[]`** is where you **record the corpus for downstream work**: each entry’s **`path`** is the **Markdown** file path (relative to the skill workspace—see [set-workspace.md](set-workspace.md)), and **`role`** is your provenance anchor for that source. That list is what **chunking** and **canonical context** read as “these are the files we cover”; it is the durable answer to **where** context came from and **where** canonical **`.md`** lives on disk.

## See also

- **[set-workspace.md](set-workspace.md)** — Skill workspace and **`solution.conf`** wiring (before you finalize paths here).
- **[context-chunking-approach.md](context-chunking-approach.md)** — Chunking spec after Markdown and **`manifest_sources`** exist.
- **[canonical-context.md](canonical-context.md)** — Context package (chunks, index, validate).

