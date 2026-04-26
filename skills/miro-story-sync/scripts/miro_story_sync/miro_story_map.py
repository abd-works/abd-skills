"""``MiroStoryMap`` orchestrator.

Mirrors ``DrawIOStoryMap`` for Miro: walks the canonical ``StoryMap``,
materialises ``MiroEpic`` / ``MiroSubEpic`` / ``MiroStory`` nodes via
``MiroStoryNodeSerializer``, and flushes every node to a Miro board through
``MiroTransport``.

For now only the **outline** mode is implemented end-to-end; exploration
(AC boxes) and increments (lanes) follow the same pattern as DrawIO and are
straight-line additions on top of this module — they can reuse common's
``RowPositions`` and ``compare_node_lists`` exactly the way
``DrawIOStoryMap`` does.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from . import _bootstrap  # noqa: F401

from story_graph_ops.nodes import StoryMap

from diagram_story_sync.layout_constants import CELL_SPACING
from diagram_story_sync.layout_data import LayoutData
from diagram_story_sync.node_comparison import (
    RowPositions,
    max_sub_epic_depth,
)
from diagram_story_sync.render_summary import RenderSummary

from .miro_story_node import MiroEpic, MiroStory, MiroSubEpic
from .miro_story_node_serializer import MiroStoryNodeSerializer
from .miro_transport import MiroItem, MiroTransport


__all__ = ['MiroStoryMap', 'MiroOutlineMap']


class MiroStoryMap(StoryMap):
    """Coordinates render → transport flush for Miro story maps."""

    def __init__(self, transport: MiroTransport,
                 diagram_type: str = 'outline',
                 story_graph: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(story_graph or {'epics': []})
        self._transport = transport
        self._diagram_type = diagram_type
        self._miro_epics: List[MiroEpic] = []
        self._created_items: List[MiroItem] = []
        self._layout_data: Optional[LayoutData] = None

    @property
    def transport(self) -> MiroTransport:
        return self._transport

    @property
    def diagram_type(self) -> str:
        return self._diagram_type

    @property
    def created_items(self) -> List[MiroItem]:
        """Items created by the most recent ``flush`` (newest last)."""
        return list(self._created_items)

    # ------------------------------------------------------------------
    # Queries (same shape as DrawIOStoryMap)
    # ------------------------------------------------------------------

    def get_epics(self) -> List[MiroEpic]:
        return list(self._miro_epics)

    def get_sub_epics(self) -> List[MiroSubEpic]:
        result: List[MiroSubEpic] = []
        for epic in self._miro_epics:
            result.extend(epic.get_sub_epics())
        return result

    def get_stories(self) -> List[MiroStory]:
        result: List[MiroStory] = []
        for epic in self._miro_epics:
            result.extend(epic.get_stories())
        return result

    def get_total_width(self) -> float:
        if not self._miro_epics:
            return 0.0
        return max(e.boundary.right for e in self._miro_epics)

    def get_bottom_y(self) -> float:
        bottom = 0.0
        for story in self.get_stories():
            b = story.position.y + story.boundary.height
            if b > bottom:
                bottom = b
        for se in self.get_sub_epics():
            b = se.position.y + se.boundary.height
            if b > bottom:
                bottom = b
        return bottom

    # ------------------------------------------------------------------
    # Render — outline
    # ------------------------------------------------------------------

    def render_from_story_map(self, story_map: StoryMap,
                               layout_data: Optional[LayoutData] = None) -> RenderSummary:
        """Build the in-memory ``MiroStoryNode`` tree for the outline.

        No items are pushed to Miro yet — call ``flush`` after rendering.
        Splitting ``render`` from ``flush`` lets tests inspect what would be
        sent without creating any board items.
        """
        self._layout_data = layout_data
        self._miro_epics = []

        epics = list(story_map.epics)
        if not epics:
            return RenderSummary(epics=0, sub_epic_count=0, diagram_generated=True)

        max_depth = max(max_sub_epic_depth(epic) for epic in epics)
        rows = RowPositions(max_depth)

        x_pos = MiroEpic.X_START
        for epic in epics:
            miro_epic = MiroStoryNodeSerializer.create_epic(
                epic.name, getattr(epic, 'sequential_order', 0) or 0)
            miro_epic.render_from_domain(epic, x_pos, rows, layout_data)
            self._miro_epics.append(miro_epic)
            x_pos = miro_epic.boundary.right + CELL_SPACING

        return RenderSummary(
            epics=len(self._miro_epics),
            sub_epic_count=len(self.get_sub_epics()),
            story_count=len(self.get_stories()),
            diagram_generated=True,
        )

    # ------------------------------------------------------------------
    # Persistence — Miro board flush via transport
    # ------------------------------------------------------------------

    def flush(self) -> List[MiroItem]:
        """Replace every item on the configured board with the rendered tree.

        Mirrors ``DrawIOStoryMap.save``: collect every node in render order
        and hand the specs to the transport. Returns the created items in
        the order they were sent (use ``created_items`` to retrieve later).
        """
        nodes = self._collect_all_nodes()
        specs = MiroStoryNodeSerializer.to_item_specs(nodes)
        self._created_items = self._transport.replace_all(specs)
        return list(self._created_items)

    # ------------------------------------------------------------------
    # Layout — extract / save
    # ------------------------------------------------------------------

    def extract_layout(self) -> LayoutData:
        """Persist current node positions for re-rendering.

        Same key shape as the DrawIO skill (``EPIC|name`` / ``SUB_EPIC|name``
        / ``STORY|epic|sub_epic|story``) so the JSON sidecar is
        cross-compatible: a layout produced from DrawIO loads cleanly into
        Miro and vice versa.
        """
        layout = LayoutData()
        for epic in self._miro_epics:
            layout.set_entry(f'EPIC|{epic.name}',
                             epic.position.x, epic.position.y,
                             epic.boundary.width, epic.boundary.height)
            layout.set_entry(epic.cell_id,
                             epic.position.x, epic.position.y,
                             epic.boundary.width, epic.boundary.height)
            for se in epic.get_sub_epics():
                self._extract_layout_for_sub_epic(layout, epic.name, se)
        return layout

    def _extract_layout_for_sub_epic(self, layout: LayoutData,
                                      epic_name: str,
                                      se: MiroSubEpic) -> None:
        layout.set_entry(f'SUB_EPIC|{se.name}',
                         se.position.x, se.position.y,
                         se.boundary.width, se.boundary.height)
        layout.set_entry(se.cell_id,
                         se.position.x, se.position.y,
                         se.boundary.width, se.boundary.height)
        for nested in se.get_sub_epics():
            self._extract_layout_for_sub_epic(layout, epic_name, nested)
        for story in se.get_stories():
            layout.set_entry(
                f'STORY|{epic_name}|{se.name}|{story.name}',
                story.position.x, story.position.y,
                story.boundary.width, story.boundary.height,
            )
            layout.set_entry(story.cell_id,
                             story.position.x, story.position.y,
                             story.boundary.width, story.boundary.height)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _collect_all_nodes(self) -> list:
        nodes: List[Any] = []
        for epic in self._miro_epics:
            nodes.extend(epic.collect_all_nodes())
        return nodes


class MiroOutlineMap(MiroStoryMap):
    """Convenience subclass keeping naming parity with ``DrawIOOutlineMap``."""

    def __init__(self, transport: MiroTransport,
                 story_graph: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(transport, diagram_type='outline', story_graph=story_graph)

    def render(self, story_map: StoryMap,
               layout_data: Optional[LayoutData] = None) -> Union[Dict[str, Any], RenderSummary]:
        return self.render_from_story_map(story_map, layout_data)
