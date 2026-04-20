"""Ensure **story-graph-ops** ``scripts`` is on ``sys.path`` so ``story_graph_ops`` imports work."""
from __future__ import annotations

import sys
from pathlib import Path


def ensure_story_graph_ops_on_path() -> None:
    """Insert sibling ``skills/story-graph-ops/scripts`` if present (standard monorepo layout)."""
    here = Path(__file__).resolve().parent
    scripts = here.parent
    skill_root = scripts.parent
    ops_scripts = skill_root.parent / "story-graph-ops" / "scripts"
    p = str(ops_scripts)
    if ops_scripts.is_dir() and p not in sys.path:
        sys.path.insert(0, p)


ensure_story_graph_ops_on_path()
