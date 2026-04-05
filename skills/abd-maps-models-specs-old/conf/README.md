# Skill config

## `skill-config.json` (required)

| Key | Required | Description |
|-----|----------|-------------|
| `solution_workspace` | **Yes** | Path to the **workspace root**: a directory that **must** contain `solution.conf`. Relative paths are resolved from the skill root (`abd-maps-models-specs/`). |

If `solution_workspace` is missing, empty, not a directory, or `solution.conf` is missing there, scripts exit with a clear error. There is no “run without a workspace” mode.

Optional script flag `--config` may point at a specific `solution.conf` file; it **must** still live under `solution_workspace` (same directory as the default `solution.conf` or a path whose parent is that workspace root — see `scripts/_config.py`).

## Workspace `solution.conf`

Paths inside `solution.conf` (`output_dir`, `context_path`, `chunk_index_path`, etc.) are relative to `solution_workspace`.

Typical outputs under `output_dir`:

- `context/chunks/*.md`, `context/context_index.json`
- `map-model-spec.json`, `map-model-spec.md`, `mms-chunk-index.json`
- `evidence/*.json`
