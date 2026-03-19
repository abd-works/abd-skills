"""Shared config for abd-map-model-spec-synthesizer scripts.

Config is split across two files:
  conf/abd-config.json   — skill-level: solution_workspace only (points to workspace root)
  <workspace>/solution.conf — workspace-level: output_dir, context_path, chunk_index_path

When solution_workspace is set, all paths resolve relative to the workspace.
When not set, scripts fall back to skill_dir (flat layout at skill root).
"""
import json
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def skill_config() -> dict:
    return _load_json(_SKILL_DIR / "conf" / "abd-config.json")


def workspace_root() -> Path | None:
    ws = skill_config().get("solution_workspace")
    if ws:
        p = Path(ws)
        if not p.is_absolute():
            p = _SKILL_DIR / p
        return p.resolve()
    return None


def workspace_config() -> dict:
    ws = workspace_root()
    if ws:
        return _load_json(ws / "solution.conf")
    return {}


def output_dir() -> Path:
    """Resolve output directory: workspace/solution.conf → output_dir, relative to workspace root."""
    ws = workspace_root()
    if ws:
        out = workspace_config().get("output_dir", "solution")
        return ws / out
    return _SKILL_DIR


def context_path() -> Path | None:
    """Resolve context_path from workspace/solution.conf, relative to workspace root.
    Default: output_dir/context (e.g. maps-models-specs/context)."""
    ws = workspace_root()
    if ws:
        ctx = workspace_config().get("context_path")
        if ctx:
            return ws / ctx
        # Default: output_dir/context
        return output_dir() / "context"
    return None


def context_chunks_path() -> Path | None:
    """Path to context_chunks.json. None when no workspace."""
    ctx = context_path()
    return (ctx / "context_chunks.json") if ctx else None


def chunk_index_path() -> Path | None:
    """Resolve chunk_index_path from workspace/solution.conf. Default: output_dir/mms-chunk-index.json."""
    ws = workspace_root()
    if ws:
        p = workspace_config().get("chunk_index_path")
        if p:
            return ws / p
        return output_dir() / "mms-chunk-index.json"
    return None


def generated_dir() -> Path:
    """Root for generated outputs (junk_config.json, etc.)."""
    return output_dir() / "generated"


def evidence_dir() -> Path:
    """Evidence files: actions.json, decisions.json, states.json, relationships.json."""
    return output_dir() / "evidence"


def map_model_spec_path() -> Path:
    """map-model-spec.json path."""
    return output_dir() / "map-model-spec.json"


def junk_config_path() -> Path | None:
    """Junk config for no-junk-concepts scanner. Tries: generated/junk_config.json, mms-junk-config.json."""
    out = output_dir()
    # Prefer generated/junk_config.json (mm3 layout)
    p = generated_dir() / "junk_config.json"
    if p.exists():
        return p
    # Fallback: mms-junk-config.json next to map-model-spec
    p = out / "mms-junk-config.json"
    if p.exists():
        return p
    return None


def default_map_model_spec_path() -> Path:
    """Default input for scanners: workspace output_dir or skill_dir."""
    return map_model_spec_path() if workspace_root() else _SKILL_DIR / "map-model-spec.json"


def default_evidence_dir() -> Path:
    """Default evidence dir for scanners: workspace or skill_dir."""
    return evidence_dir() if workspace_root() else _SKILL_DIR / "evidence"


def default_chunk_index_path() -> Path:
    """Default chunk index path for build script."""
    return output_dir() / "mms-chunk-index.json" if workspace_root() else _SKILL_DIR / "mms-chunk-index.json"
