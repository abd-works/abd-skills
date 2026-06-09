"""Ensure ``lib/`` and **story-graph-ops** ``scripts`` are on ``sys.path``.

Family package layout::

    story-driven-delivery/
        lib/diagram_story_sync/
        skills/supporting/story-graph-ops/scripts/
        skills/supporting/drawio-story-sync/scripts/   <- this skill
"""
from __future__ import annotations

import sys
from pathlib import Path


def ensure_common_and_story_graph_ops_on_path() -> None:
    here = Path(__file__).resolve().parent
    skill_root = here.parent.parent
    skills_dir = skill_root.parent
    package_root = skills_dir.parent

    lib_dir = package_root / "lib"
    legacy_common = skills_dir / "common"
    ops_scripts = skills_dir / "story-graph-ops" / "scripts"

    for p in (lib_dir, legacy_common, ops_scripts):
        s = str(p)
        if p.is_dir() and s not in sys.path:
            sys.path.insert(0, s)


ensure_common_and_story_graph_ops_on_path()


def ensure_story_graph_ops_on_path() -> None:
    """Backward-compatible alias."""
    ensure_common_and_story_graph_ops_on_path()
