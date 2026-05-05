"""Resolve sibling skill ``scripts`` directories onto ``sys.path``.

The diagram-story-sync ecosystem assumes a monorepo layout::

    agilebydesign-skills/
        common/
            diagram_story_sync/         <- this package
        skills/
            story-graph-ops/scripts/    <- canonical story_graph_ops
            drawio-story-sync/scripts/
            miro-story-sync/scripts/

Backend skills (drawio-story-sync, miro-story-sync) import this package and
``story_graph_ops`` together. We auto-prepend both locations so that scripts and
tests do not need to set ``PYTHONPATH`` manually when the layout is the
default. Callers in non-default layouts should set ``PYTHONPATH`` themselves.
"""
from __future__ import annotations

import sys
from pathlib import Path


def _common_root() -> Path:
    """Path of the ``common`` directory holding this package."""
    return Path(__file__).resolve().parents[1]


def _repo_root() -> Path:
    """Path of the ``agilebydesign-skills`` repo root, parent of ``common``."""
    return _common_root().parent


def ensure_common_on_path() -> None:
    """Insert ``common/`` so ``import diagram_story_sync`` works from any caller."""
    p = str(_common_root())
    if p not in sys.path:
        sys.path.insert(0, p)


def ensure_story_graph_ops_on_path() -> None:
    """Insert sibling ``skills/story-graph-ops/scripts`` if present."""
    ops_scripts = _repo_root() / "skills" / "story-graph-ops" / "scripts"
    p = str(ops_scripts)
    if ops_scripts.is_dir() and p not in sys.path:
        sys.path.insert(0, p)


def ensure_backend_paths(backend_skill_dir: Path) -> None:
    """Insert ``common/`` plus a backend skill's ``scripts/`` and ``story-graph-ops``.

    ``backend_skill_dir`` is expected to be the skill folder
    (e.g. ``.../skills/drawio-story-sync``); we add its ``scripts/`` subdirectory.
    """
    ensure_common_on_path()
    ensure_story_graph_ops_on_path()
    scripts = backend_skill_dir / "scripts"
    p = str(scripts)
    if scripts.is_dir() and p not in sys.path:
        sys.path.insert(0, p)


ensure_common_on_path()
ensure_story_graph_ops_on_path()
