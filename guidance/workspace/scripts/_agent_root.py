"""Resolve agent repo root for workspace CLI. See guidance/workspace/README.md."""
from __future__ import annotations

from pathlib import Path


def find_agent_root(start: Path) -> Path | None:
    """Walk upward from *start* (usually …/scripts); first dir with skill-config.json wins."""
    for d in [start] + list(start.parents):
        cfg = d / "skill-config.json"
        if cfg.is_file():
            return d
    return None


def find_skills_repo_root(start: Path) -> Path | None:
    """When skill-config.json does not exist yet: agilebydesign-skills repo root (scripts + skills/)."""
    for d in [start] + list(start.parents):
        if (d / "skills").is_dir() and (d / "scripts" / "deploy-skills.ps1").is_file():
            return d
    return None


def resolve_repo_root_for_workspace_cli(start: Path) -> Path | None:
    """Prefer explicit skill-config.json location; else bootstrap against known monorepo layout."""
    return find_agent_root(start) or find_skills_repo_root(start)
