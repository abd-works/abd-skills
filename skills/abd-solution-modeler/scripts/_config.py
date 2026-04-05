"""Shared config for abd-solution-modeler scripts.

Config is split across two files:
  skill-config.json → workspace — skill-level: solution_workspace only
  <workspace>/solution.conf — workspace-level: output_dir, chunk_index_path, context_path
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
    raw = _load_json(_SKILL_DIR / "skill-config.json")
    ws = raw.get("workspace")
    if isinstance(ws, dict):
        return ws
    return {}


def workspace_root() -> Path | None:
    ws = skill_config().get("solution_workspace")
    return Path(ws).resolve() if ws else None


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
    return Path.cwd() / "solution"


def context_path() -> Path | None:
    """Resolve context_path from workspace/solution.conf, relative to workspace root."""
    ws = workspace_root()
    if ws:
        ctx = workspace_config().get("context_path")
        if ctx:
            return ws / ctx
    return None


def chunk_index_path() -> Path | None:
    """Resolve chunk_index_path from workspace/solution.conf."""
    ws = workspace_root()
    if ws:
        p = workspace_config().get("chunk_index_path")
        if p:
            return ws / p
    return None


def context_dir() -> Path:
    """Chunks and context_chunks.json. workspace/context/ per recommendations."""
    out = output_dir()
    return out / "context"


def generated_dir() -> Path:
    """Root for generated outputs."""
    return output_dir() / "generated"


def domain_dir() -> Path:
    """Domain outputs: concept_guidance.md, concept_guidance.json, concept_model.md, etc."""
    return generated_dir() / "domain"


def interaction_model_dir() -> Path:
    """Interaction tree outputs: interaction_tree.md."""
    return generated_dir() / "interaction_model"


def evidence_dir() -> Path:
    """Evidence files: terms.json, actions.json, evidence_index.json, etc."""
    return output_dir() / "evidence"


def concept_signals_dir() -> Path:
    """Concept signal outputs from Phase 3: concept_signals.json (combined)."""
    return output_dir() / "concept_signals"


def hypothesis_path() -> Path:
    """hypothesis.json from Phase 4 (concept synthesis)."""
    return generated_dir() / "hypothesis.json"


def extraction_config_path() -> Path:
    """extraction_config.json from Phase 2 (configure extraction)."""
    return generated_dir() / "extraction_config.json"


def evidence_index_path() -> Path:
    """evidence_index.json from Phase 6 (index)."""
    return evidence_dir() / "evidence_index.json"


def solution_model_path() -> Path:
    """solution_model.json from Phases 7-12 (single artifact from Structure onward)."""
    return generated_dir() / "solution_model.json"


def assessment_path() -> Path:
    """assessment.json from Phase 11 (Assess)."""
    return generated_dir() / "assessment.json"


def no_tree() -> bool:
    """When True, interaction tree generation, rules, and validation are disabled."""
    return bool(workspace_config().get("no_tree", False))
