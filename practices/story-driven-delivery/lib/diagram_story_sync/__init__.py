"""Platform-agnostic diagram-story-sync primitives.

Shared by **drawio-story-sync**, **miro-story-sync**, and any future diagram
backend. Holds the geometry, layout, comparison, and abstract node types that
do not depend on a specific diagramming tool. Each backend skill plugs in its
own ``Element`` / ``Synchronizer`` / ``Serializer`` over these primitives.
"""
from . import bootstrap  # noqa: F401  (side-effect: extends sys.path)

from .position import Position, Boundary
from .layout_data import LayoutData
from .render_summary import RenderSummary
from .layout_constants import (
    CELL_SIZE,
    CELL_SPACING,
    EPIC_Y,
    EPIC_HEIGHT,
    SUB_EPIC_HEIGHT,
    ROW_GAP,
    ACTOR_GAP,
    BAR_PADDING,
    SPACING,
    CONTAINER_PADDING,
)
from .style_defaults import STYLE_DEFAULTS
from .diagram_story_node import (
    DiagramStoryNode,
    DiagramEpic,
    DiagramSubEpic,
    DiagramStory,
    DiagramIncrement,
)
from .node_comparison import (
    RowPositions,
    collect_all_names,
    compare_node_lists,
    max_sub_epic_depth,
    report_leaf_story_group_reorder_if_needed,
    report_sub_epic_sibling_reorder_if_needed,
    slug,
)
from .update_report import (
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
    'Position',
    'Boundary',
    'LayoutData',
    'RenderSummary',
    'CELL_SIZE',
    'CELL_SPACING',
    'EPIC_Y',
    'EPIC_HEIGHT',
    'SUB_EPIC_HEIGHT',
    'ROW_GAP',
    'ACTOR_GAP',
    'BAR_PADDING',
    'SPACING',
    'CONTAINER_PADDING',
    'STYLE_DEFAULTS',
    'DiagramStoryNode',
    'DiagramEpic',
    'DiagramSubEpic',
    'DiagramStory',
    'DiagramIncrement',
    'RowPositions',
    'collect_all_names',
    'compare_node_lists',
    'max_sub_epic_depth',
    'report_leaf_story_group_reorder_if_needed',
    'report_sub_epic_sibling_reorder_if_needed',
    'slug',
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
