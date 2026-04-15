"""Shared config for abd-maps-models-specs scripts.

Config is split across two files:
  skill-config.json   — skill-level: **required** `solution_workspace` (path to workspace root)
  <workspace>/solution.conf — workspace-level: output_dir, context_path, chunk_index_path

There is **no** skill-root-only / flat layout. If `solution_workspace` is missing, invalid, or
`solution.conf` is absent, importing callers get a clear error when they first resolve paths.

Optional: call `set_solution_conf_override(Path)` before any path resolution so
`--config` points at a specific solution.conf under the same workspace root.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent

# Set by parse_and_curate / discover_context_structure when passing --config
_SOLUTION_CONF_OVERRIDE: Path | None = None


def set_solution_conf_override(path: Path | None) -> None:
    """If set, path must be an existing file whose parent equals declared_workspace_root()."""
    global _SOLUTION_CONF_OVERRIDE
    _SOLUTION_CONF_OVERRIDE = path.resolve() if path else None


def _die(msg: str) -> None:
    print(f"abd-maps-models-specs: {msg}", file=sys.stderr)
    sys.exit(1)


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def skill_config() -> dict:
    return _load_json(_SKILL_DIR / "conf" / "skill-config.json")


def declared_workspace_root() -> Path:
    """Path from skill-config.json — directory that contains solution.conf."""
    data = skill_config()
    ws = data.get("solution_workspace")
    if ws is None or (isinstance(ws, str) and not str(ws).strip()):
        _die(
            'skill-config.json must set non-empty "solution_workspace" '
            "(path to the workspace root directory that contains solution.conf)."
        )
    p = Path(ws)
    if not p.is_absolute():
        p = _SKILL_DIR / p
    p = p.resolve()
    if not p.is_dir():
        _die(f"solution_workspace is not a directory: {p}")
    return p


def solution_conf_path() -> Path:
    """Active solution.conf: override (if set) or <declared_workspace_root>/solution.conf."""
    root = declared_workspace_root()
    if _SOLUTION_CONF_OVERRIDE is not None:
        p = _SOLUTION_CONF_OVERRIDE
        if not p.is_file():
            _die(f"solution config file not found: {p}")
        if p.parent.resolve() != root.resolve():
            _die(
                f"--config must be under solution_workspace ({root}); got parent {p.parent}"
            )
        return p
    p = root / "solution.conf"
    if not p.is_file():
        _die(f"missing solution.conf at {p} (required under solution_workspace)")
    return p


def workspace_root() -> Path:
    """Same as declared_workspace_root — all paths in solution.conf are relative to this."""
    return declared_workspace_root()


def workspace_config() -> dict:
    return _load_json(solution_conf_path())


def output_dir() -> Path:
    """Resolve output directory from solution.conf → output_dir, relative to workspace root."""
    ws = workspace_root()
    out = workspace_config().get("output_dir", "solution")
    return ws / out


def context_path() -> Path:
    """Context dir: chunks/*.md and context_index.json."""
    ws = workspace_root()
    ctx = workspace_config().get("context_path")
    if ctx:
        return ws / ctx
    return output_dir() / "context"


def context_index_path() -> Path:
    """Path to context_index.json (manifest + indexes)."""
    return context_path() / "context_index.json"


def chunk_index_path() -> Path:
    """chunk_index_path from solution.conf, or default output_dir/mms-chunk-index.json."""
    ws = workspace_root()
    p = workspace_config().get("chunk_index_path")
    if p:
        return ws / p
    return output_dir() / "mms-chunk-index.json"


def generated_dir() -> Path:
    return output_dir() / "generated"


def evidence_dir() -> Path:
    return output_dir() / "evidence"


def map_model_spec_path() -> Path:
    return output_dir() / "map-model-spec.json"


def junk_config_path() -> Path | None:
    """Junk config for no-junk-concepts scanner."""
    out = output_dir()
    p = generated_dir() / "junk_config.json"
    if p.exists():
        return p
    p = out / "mms-junk-config.json"
    if p.exists():
        return p
    return None


def default_map_model_spec_path() -> Path:
    return map_model_spec_path()


def default_evidence_dir() -> Path:
    return evidence_dir()


def default_chunk_index_path() -> Path:
    return chunk_index_path()
