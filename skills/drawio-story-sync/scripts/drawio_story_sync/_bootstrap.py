"""Ensure ``common/`` and **story-graph-ops** ``scripts`` are on ``sys.path``.

This skill assumes the standard ``agilebydesign-skills`` monorepo layout::

    agilebydesign-skills/
        common/                                <- diagram_story_sync package
        skills/story-graph-ops/scripts/        <- story_graph_ops package
        skills/drawio-story-sync/scripts/      <- this skill

When that layout is in place, importing ``drawio_story_sync`` is enough — both
sibling locations are auto-prepended. If your project differs, prepend
``common/`` and ``skills/story-graph-ops/scripts`` to ``PYTHONPATH`` yourself.
"""
from __future__ import annotations

import sys
from pathlib import Path


def ensure_common_and_story_graph_ops_on_path() -> None:
    here = Path(__file__).resolve().parent
    scripts = here.parent
    skill_root = scripts.parent
    skills_dir = skill_root.parent
    repo_root = skills_dir.parent

    common_dir = repo_root / "common"
    ops_scripts = skills_dir / "story-graph-ops" / "scripts"

    for p in (common_dir, ops_scripts):
        s = str(p)
        if p.is_dir() and s not in sys.path:
            sys.path.insert(0, s)


ensure_common_and_story_graph_ops_on_path()


def ensure_story_graph_ops_on_path() -> None:
    """Backward-compatible alias kept for any external caller importing this."""
    ensure_common_and_story_graph_ops_on_path()
