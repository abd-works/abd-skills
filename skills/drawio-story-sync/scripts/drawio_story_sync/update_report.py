"""Re-export ``UpdateReport`` and related types from **story_graph_ops** (single source of truth)."""

from __future__ import annotations

import sys
from pathlib import Path

_ops_scripts = Path(__file__).resolve().parents[2] / 'story-graph-ops' / 'scripts'
if _ops_scripts.is_dir():
    _p = str(_ops_scripts)
    if _p not in sys.path:
        sys.path.insert(0, _p)

from story_graph_ops.update_report import (  # noqa: E402
    ACChange,
    ACMove,
    IncrementChange,
    IncrementMove,
    LargeDeletions,
    MatchEntry,
    StoryEntry,
    StoryGroupReorder,
    StoryMove,
    StoryUsersChange,
    SubEpicMove,
    SubEpicSiblingReorder,
    UpdateReport,
)

__all__ = [
    'ACChange',
    'ACMove',
    'IncrementChange',
    'IncrementMove',
    'LargeDeletions',
    'MatchEntry',
    'StoryEntry',
    'StoryGroupReorder',
    'StoryMove',
    'StoryUsersChange',
    'SubEpicMove',
    'SubEpicSiblingReorder',
    'UpdateReport',
]
