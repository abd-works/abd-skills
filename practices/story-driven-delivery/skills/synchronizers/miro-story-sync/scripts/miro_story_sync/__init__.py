"""Miro backend for the diagram-story-sync ecosystem.

Mirrors **drawio-story-sync** but materialises rendered nodes through a
pluggable ``MiroTransport`` (REST API v2 in production; in-memory fake in
tests). All shared geometry, layout, comparison, and abstract diagram nodes
come from the **common** ``diagram_story_sync`` package.
"""
from . import _bootstrap  # noqa: F401

from diagram_story_sync.position import Position, Boundary
from diagram_story_sync.layout_data import LayoutData
from diagram_story_sync.render_summary import RenderSummary
from diagram_story_sync.update_report import UpdateReport

from .miro_element import MiroElement, MIRO_SHAPE_BY_TYPE
from .miro_transport import (
    MiroTransport,
    InMemoryMiroTransport,
    RestMiroTransport,
    MiroItem,
)
from .miro_story_node import (
    MiroStoryNode,
    MiroEpic,
    MiroSubEpic,
    MiroStory,
)
from .miro_story_node_serializer import MiroStoryNodeSerializer
from .miro_story_map import MiroStoryMap, MiroOutlineMap
from .miro_story_synchronizer import MiroSynchronizer, load_story_graph_json

__all__ = [
    'Boundary',
    'Position',
    'LayoutData',
    'RenderSummary',
    'UpdateReport',
    'MiroElement',
    'MIRO_SHAPE_BY_TYPE',
    'MiroTransport',
    'InMemoryMiroTransport',
    'RestMiroTransport',
    'MiroItem',
    'MiroStoryNode',
    'MiroEpic',
    'MiroSubEpic',
    'MiroStory',
    'MiroStoryNodeSerializer',
    'MiroStoryMap',
    'MiroOutlineMap',
    'MiroSynchronizer',
    'load_story_graph_json',
]
