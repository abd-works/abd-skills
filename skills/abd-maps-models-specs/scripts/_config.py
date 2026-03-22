"""Path resolution for abd-maps-models-specs — layered config (no hardcoded handbook paths).

1. <skill_path>/conf/abd-config.json → active skill workspace root (directory containing solution.conf)
   Resolution order for the workspace path string: active_skill_workspace, then solution_workspace,
   then skill_space_path (deprecated aliases).
2. <skill_workspace>/solution.conf → output_dir, context_path, manifest_sources[], context_chunking_spec, …

Paths in solution.conf are relative to the skill workspace root. See abd-skill-builder/docs/workspace-config.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]

_SOLUTION_CONF_OVERRIDE: Path | None = None


def set_solution_conf_override(path: Path | None) -> None:
    """If set, must be an existing file under declared_workspace_root()."""
    global _SOLUTION_CONF_OVERRIDE
    _SOLUTION_CONF_OVERRIDE = path.resolve() if path else None


def _die(msg: str) -> None:
    print(f"abd-maps-models-specs: {msg}", file=sys.stderr)
    sys.exit(1)


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        _die(f"cannot read JSON {path}: {e}")


def skill_config() -> dict:
    return _load_json(SKILL_ROOT / "conf" / "abd-config.json")


def _workspace_path_string(data: dict) -> str | None:
    """First non-empty among canonical and deprecated install keys."""
    for key in ("active_skill_workspace", "solution_workspace", "skill_space_path"):
        v = data.get(key)
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s
    return None


def declared_workspace_root() -> Path:
    data = skill_config()
    ws = _workspace_path_string(data)
    if ws is None:
        _die(
            'conf/abd-config.json must set non-empty "active_skill_workspace" '
            '(or deprecated "solution_workspace" / "skill_space_path") — directory containing solution.conf.'
        )
    p = Path(ws)
    if not p.is_absolute():
        p = SKILL_ROOT / p
    p = p.resolve()
    if not p.is_dir():
        _die(f"solution_workspace is not a directory: {p}")
    return p


def solution_conf_path() -> Path:
    root = declared_workspace_root()
    if _SOLUTION_CONF_OVERRIDE is not None:
        p = _SOLUTION_CONF_OVERRIDE
        if not p.is_file():
            _die(f"solution config not found: {p}")
        if p.parent.resolve() != root.resolve():
            _die(f"--config must live under skill workspace ({root}); got {p}")
        return p
    p = root / "solution.conf"
    if not p.is_file():
        _die(f"missing solution.conf at {p}")
    return p


def workspace_root() -> Path:
    return declared_workspace_root()


def workspace_config() -> dict:
    return _load_json(solution_conf_path())


def output_dir() -> Path:
    ws = workspace_root()
    out = workspace_config().get("output_dir", "abd-maps-models-specs")
    return ws / out


def context_path() -> Path:
    ws = workspace_root()
    ctx = workspace_config().get("context_path", "context")
    return ws / ctx


def context_index_path() -> Path:
    return context_path() / "context_index.json"


def chunks_dir() -> Path:
    return context_path() / "chunks"


def source_path_dir() -> Path:
    """Directory named in solution.conf source_path (canonical markdown root)."""
    ws = workspace_root()
    sp = workspace_config().get("source_path", "docs")
    return ws / sp


def context_chunking_spec_path() -> Path:
    ws = workspace_root()
    name = workspace_config().get("context_chunking_spec", "context_chunking_spec.yaml")
    return ws / name


def manifest_sources_declared() -> list[dict]:
    """manifest_sources from solution.conf: [{ path, role }, ...]."""
    cfg = workspace_config()
    ms = cfg.get("manifest_sources")
    if not isinstance(ms, list):
        return []
    return [x for x in ms if isinstance(x, dict) and x.get("path")]


def resolved_manifest_sources() -> list[tuple[Path, str, str]]:
    """(absolute_path, role, path_relative_posix) for each declared source."""
    root = workspace_root()
    out: list[tuple[Path, str, str]] = []
    for item in manifest_sources_declared():
        rel = str(item["path"]).replace("\\", "/")
        p = (root / rel).resolve()
        role = str(item.get("role") or "source")
        out.append((p, role, rel))
    return out


# --- Phase output dirs (under output_dir) ---


def _phase_dirs() -> dict[str, Path]:
    o = output_dir()
    return {
        "OUT_ROOT": o,
        "PHASE0": o / "phase0",
        "PHASE1": o / "phase1",
        "PHASE2": o / "phase2",
        "PHASE3": o / "phase3",
        "PHASE4": o / "phase4",
        "PHASE5": o / "phase5",
        "PHASE6": o / "phase6",
        "PHASE7": o / "phase7",
        "PHASE8": o / "phase8",
        "MAPS_MODELS_SPECS": o / "maps-models-specs",
    }


def _init_module_paths() -> None:
    global OUT_ROOT, PHASE0, PHASE1, PHASE2, PHASE3, PHASE4, PHASE5, PHASE6, PHASE7, PHASE8, MAPS_MODELS_SPECS
    global CHUNKS_DIR, CONTEXT_INDEX, WORKSPACE_ROOT
    WORKSPACE_ROOT = workspace_root()
    d = _phase_dirs()
    OUT_ROOT = d["OUT_ROOT"]
    PHASE0 = d["PHASE0"]
    PHASE1 = d["PHASE1"]
    PHASE2 = d["PHASE2"]
    PHASE3 = d["PHASE3"]
    PHASE4 = d["PHASE4"]
    PHASE5 = d["PHASE5"]
    PHASE6 = d["PHASE6"]
    PHASE7 = d["PHASE7"]
    PHASE8 = d["PHASE8"]
    MAPS_MODELS_SPECS = d["MAPS_MODELS_SPECS"]
    CHUNKS_DIR = chunks_dir()
    CONTEXT_INDEX = context_index_path()


_init_module_paths()

_rms = resolved_manifest_sources()
# First declared canonical file (scripts that still expect one Path); use resolved_manifest_sources() for all.
HEROES_HANDBOOK = _rms[0][0] if _rms else source_path_dir() / "HeroesHandbook.md"
MM3_FIXTURE = WORKSPACE_ROOT


def map_model_spec_path() -> Path:
    """Published domain spec JSON under output_dir (Phases 4–7)."""
    return MAPS_MODELS_SPECS / "map-model-spec.json"


def default_map_model_spec_path() -> Path:
    """Alias for scanners imported from older skill scripts."""
    return map_model_spec_path()
