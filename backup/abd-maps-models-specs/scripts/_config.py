"""Path resolution for abd-maps-models-specs — layered config (no hardcoded handbook paths).

1. <skill_path>/skill-config.json → **workspace.active_skill_workspace** only (absolute path to the directory
   containing solution.conf). No other keys are read for workspace; no relative resolution.
2. <active_skill_workspace>/solution.conf → output_dir, context_path, manifest_sources[], …

Paths in solution.conf are relative to that workspace root.

**Spec layout (canonical):** Under ``output_dir`` (usually ``spec/``):

- **Files at the root of ``output_dir``** — domain and pipeline JSON (e.g. ``map-model-spec.json``,
  ``terms_layer.json``, ``shaped_story_map.json``, ``scenario_walkthroughs.json``, manifests).
- **Exactly two subfolders:** ``context/`` (``context_index.json`` + chunk ``*.md`` files in that folder — no ``chunks/`` subfolder) and ``walkthroughs/``
  (narrative ``*.md``). No ``phase*``, ``maps-models-specs``, or other extra directories under ``spec/``.

If ``context_path`` is omitted in ``solution.conf``, it defaults to ``<output_dir>/context`` (so context
lives under ``spec`` with walkthroughs as the only sibling folder).
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
    """Workspace routing keys from ``skill-config.json`` → ``workspace`` object."""
    p = SKILL_ROOT / "skill-config.json"
    if not p.exists():
        return {}
    raw = _load_json(p)
    ws = raw.get("workspace")
    if isinstance(ws, dict):
        return ws
    return {}


def _active_skill_workspace_string(data: dict) -> str | None:
    v = data.get("active_skill_workspace")
    if v is None:
        return None
    s = str(v).strip()
    return s if s else None


def declared_workspace_root() -> Path:
    data = skill_config()
    ws = _active_skill_workspace_string(data)
    if ws is None:
        _die(
            'skill-config.json → workspace must set non-empty string "active_skill_workspace" '
            "(absolute path to the directory that contains solution.conf). "
            "Set it with: python scripts/set_workspace.py <path>"
        )
    p = Path(ws)
    if not p.is_absolute():
        _die(
            f'"active_skill_workspace" must be an absolute path (got relative: {ws!r}). '
            "Use python scripts/set_workspace.py <path> with an absolute or resolvable path."
        )
    p = p.resolve()
    if not p.is_dir():
        _die(f"active_skill_workspace is not a directory: {p}")
    return p


def solution_conf_path() -> Path:
    root = declared_workspace_root()
    if _SOLUTION_CONF_OVERRIDE is not None:
        p = _SOLUTION_CONF_OVERRIDE
        if not p.is_file():
            _die(f"solution config not found: {p}")
        if p.parent.resolve() != root.resolve():
            _die(f"--config must live under workspace root ({root}); got {p}")
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
    out = workspace_config().get("output_dir", "spec")
    return ws / out


def context_path() -> Path:
    """Directory for ``context_index.json`` and ``chunks/`` — default ``<output_dir>/context``."""
    ws = workspace_root()
    cfg = workspace_config()
    cp = cfg.get("context_path")
    if cp is not None and str(cp).strip():
        return (ws / str(cp).replace("\\", "/")).resolve()
    return output_dir() / "context"


def context_index_path() -> Path:
    return context_path() / "context_index.json"


def chunks_dir() -> Path:
    """Where chunk markdown lives: same directory as ``context_index.json`` (flat ``*.md``, no ``chunks/`` subfolder)."""
    return context_path()


def walkthroughs_dir() -> Path:
    """Narrative walkthrough markdown under ``output_dir`` (``spec/walkthroughs`` when output_dir is ``spec``)."""
    return output_dir() / "walkthroughs"


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


# --- Artifact basenames (under output_dir / OUT_ROOT) ---

TERMS_LAYER_JSON = "terms_layer.json"
MECHANISMS_JSON = "mechanisms.json"
CANDIDATE_QUEUE_JSON = "candidate_queue.json"
SHAPED_STORY_MAP_JSON = "shaped_story_map.json"

# Emitted in those three JSON files' "schema" field by build_terms_mechanisms_scaffold.py
TERMS_MECHANISMS_QUEUE_SCHEMA = "terms_mechanisms_queue/v1"


def _phase_dirs() -> dict[str, Path]:
    """Legacy aliases: all pipeline outputs live at OUT_ROOT (flat under output_dir)."""
    o = output_dir()
    return {
        "OUT_ROOT": o,
        "PHASE0": o,
        "PHASE1": o,
        "PHASE2": o,
        "PHASE3": o,
        "PHASE4": o,
        "PHASE5": o,
        "PHASE6": o,
        "PHASE7": o,
        "PHASE8": o,
        "MAPS_MODELS_SPECS": o,
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


def map_model_spec_path() -> Path:
    """Published domain spec JSON at the root of output_dir."""
    return OUT_ROOT / "map-model-spec.json"


CLASS_DIAGRAM_LAYOUT_PLAN_JSON = "class-diagram-layout-plan.json"


def class_diagram_layout_plan_path() -> Path:
    """Optional logical layout JSON beside the spec (same directory as ``map_model_spec_path``)."""
    return OUT_ROOT / CLASS_DIAGRAM_LAYOUT_PLAN_JSON


def default_map_model_spec_path() -> Path:
    """Alias for scanners imported from older skill scripts."""
    return map_model_spec_path()
