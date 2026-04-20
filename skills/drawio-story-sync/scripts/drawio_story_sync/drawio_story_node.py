from typing import List, Optional, Any, Set
from dataclasses import dataclass, field
from story_graph.nodes import StoryNode, Epic, SubEpic, Story, StoryGroup
from story_graph.domain import DomainConcept, StoryUser
from .diagram_story_node import (
    DiagramStoryNode, DiagramEpic, DiagramSubEpic, DiagramStory, DiagramIncrement
)
from .drawio_element import DrawIOElement, STYLE_DEFAULTS
from .story_io_position import Position, Boundary
from .update_report import UpdateReport


# ---------------------------------------------------------------------------
# Row-based layout constants (matching reference diagram)
# ---------------------------------------------------------------------------
CELL_SIZE = 50           # Stories and actors are 50x50 squares
CELL_SPACING = 10        # Horizontal gap between cells
EPIC_Y = 120             # Y position of epic row
EPIC_HEIGHT = 60         # Height of epic bar
SUB_EPIC_HEIGHT = 60     # Height of sub-epic bar
ROW_GAP = 15             # Gap between rows
ACTOR_GAP = 25           # Extra gap before actor row
BAR_PADDING = 5          # Internal horizontal padding for bars
SPACING = CELL_SPACING   # alias kept for backward compatibility
CONTAINER_PADDING = BAR_PADDING


def _slug(name: str) -> str:
    return name.lower().replace(' ', '-')


def _add_new_by_type(report, node, parent_name=''):
    """Report a new node using the correct method based on its type."""
    if isinstance(node, Epic):
        report.add_new_epic(node.name, parent=parent_name)
    elif isinstance(node, SubEpic):
        report.add_new_sub_epic(node.name, parent=parent_name)
    else:
        report.add_new_story(node.name, parent=parent_name)


def _add_removed_by_type(report, node, parent_name=''):
    """Report a removed node using the correct method based on its type."""
    if isinstance(node, Epic):
        report.add_removed_epic(node.name, parent=parent_name)
    elif isinstance(node, SubEpic):
        report.add_removed_sub_epic(node.name, parent=parent_name)
    else:
        report.add_removed_story(node.name, parent=parent_name)


def _report_all_descendants_as_new(node, report, parent_name=''):
    """When a node is entirely new, report all its descendants as new too."""
    sub_epics = list(node.get_sub_epics()) if hasattr(node, 'get_sub_epics') else []
    if sub_epics:
        # Has sub-epics: report them and recurse (stories will be reported by recursion)
        for se in sub_epics:
            report.add_new_sub_epic(se.name, parent=node.name)
            _report_all_descendants_as_new(se, report, parent_name=se.name)
    elif hasattr(node, 'get_stories'):
        # Leaf container: report direct stories only
        for story in node.get_stories():
            report.add_new_story(story.name, parent=node.name)


def _report_all_descendants_as_removed(node, report, parent_name=''):
    """When a node is removed, report all its descendants as removed too."""
    # Get sub-epics using whichever method/property is available
    sub_epics = []
    if hasattr(node, 'get_sub_epics'):
        sub_epics = list(node.get_sub_epics())
    elif hasattr(node, 'sub_epics'):
        sub_epics = list(node.sub_epics)
    
    if sub_epics:
        # Has sub-epics: report them and recurse (stories will be reported by recursion)
        for se in sub_epics:
            report.add_removed_sub_epic(se.name, parent=node.name)
            _report_all_descendants_as_removed(se, report, parent_name=se.name)
    
    # Report direct stories
    stories = []
    if hasattr(node, 'get_stories'):
        stories = list(node.get_stories())
    elif hasattr(node, 'all_stories'):
        stories = list(node.all_stories)
    
    for story in stories:
        report.add_removed_story(story.name, parent=node.name)


def _collect_all_names(nodes) -> Set[str]:
    """Recursively collect all names (epics, sub-epics, stories) from a tree."""
    names: Set[str] = set()
    for node in nodes:
        names.add(node.name)
        if hasattr(node, 'get_sub_epics'):
            names |= _collect_all_names(node.get_sub_epics())
        if hasattr(node, 'get_stories'):
            for story in node.get_stories():
                names.add(story.name)
        # For original domain nodes that use .children or .sub_epics
        if hasattr(node, 'sub_epics') and not hasattr(node, 'get_sub_epics'):
            names |= _collect_all_names(node.sub_epics)
        if hasattr(node, 'children'):
            for child in getattr(node, 'children', []):
                names.add(child.name)
    return names


def _compare_node_lists(extracted, original, report, parent_name='',
                        recurse=False,
                        all_extracted_names: Set[str] = None,
                        all_original_names: Set[str] = None,
                        extracted_story_to_inc: dict = None,
                        original_story_to_inc: dict = None):
    # Phase 1: Match by exact name first
    orig_by_name = {}
    for n in original:
        orig_by_name[n.name] = n

    matched_ext = []       # (ext_node, orig_node) pairs
    unmatched_ext = []     # extracted nodes with no name match
    used_orig = set()      # names already matched

    for ext_node in extracted:
        orig_node = orig_by_name.get(ext_node.name)
        if orig_node and ext_node.name not in used_orig:
            matched_ext.append((ext_node, orig_node))
            used_orig.add(ext_node.name)
        else:
            unmatched_ext.append(ext_node)

    unmatched_orig = [n for n in original if n.name not in used_orig]

    # Phase 2: Report exact matches and recurse
    for ext_node, orig_node in matched_ext:
        report.add_exact_match(ext_node.name, orig_node.name, parent=parent_name)
        if recurse and hasattr(ext_node, '_compare_children'):
            ext_node._compare_children(orig_node, report,
                                       all_extracted_names=all_extracted_names,
                                       all_original_names=all_original_names,
                                       extracted_story_to_inc=extracted_story_to_inc,
                                       original_story_to_inc=original_story_to_inc)

    # Phase 3: Detect renames by story-graph order.
    # Sort unmatched originals by their story-graph sequential_order so
    # the positional pairing reflects the original graph ordering.
    unmatched_ext_sorted = sorted(unmatched_ext, key=lambda n: n.sequential_order or 0)
    unmatched_orig_sorted = sorted(unmatched_orig, key=lambda n: getattr(n, 'sequential_order', 0) or 0)

    # A pair (ext, orig) is a rename ONLY if:
    #   - ext.name does NOT exist anywhere in the original story graph
    #     (otherwise it was moved here from another parent)
    #   - orig.name does NOT exist anywhere in the extracted diagram
    #     (otherwise it moved to a different parent)
    ext_names_global = all_extracted_names or set()
    orig_names_global = all_original_names or set()

    still_unmatched_ext = []
    still_unmatched_orig = []

    rename_pairs = []
    used_ext_idx = set()
    used_orig_idx = set()

    for i, ext_node in enumerate(unmatched_ext_sorted):
        if ext_node.name in orig_names_global:
            # This name exists in the original tree → it's a move, not a rename
            still_unmatched_ext.append(ext_node)
            continue
        # Sub-epics/epics with non-hierarchical cell IDs (e.g. "3", "18")
        # were created manually by the user in DrawIO.  They are genuinely
        # new structural elements, not renames.  Only nodes whose cell_id
        # contains '/' (generated by our rendering code from the hierarchy
        # path) are candidates for rename pairing.  Stories are excluded
        # from this check because test helpers and simplified diagrams
        # may use simple IDs for stories that are still valid renames.
        cell_id = getattr(ext_node, 'cell_id', '') or ''
        if (cell_id and '/' not in cell_id
                and isinstance(ext_node, (DrawIOEpic, DrawIOSubEpic))):
            still_unmatched_ext.append(ext_node)
            continue
        # Find the first available original that is also not present elsewhere
        for j, orig_node in enumerate(unmatched_orig_sorted):
            if j in used_orig_idx:
                continue
            if orig_node.name in ext_names_global:
                # This original name still exists in the diagram → it moved away
                continue
            # Check if both are stories with increment information.
            # Only pair as rename if they're in the same increment (or both unassigned).
            # This prevents stories in different increments but same horizontal position
            # from being incorrectly treated as renames.
            if hasattr(ext_node, 'story_type') and extracted_story_to_inc and original_story_to_inc:
                ext_inc = extracted_story_to_inc.get(ext_node.name)
                orig_inc = original_story_to_inc.get(orig_node.name)
                # If either has an increment assignment and they differ, skip this pairing
                if (ext_inc or orig_inc) and ext_inc != orig_inc:
                    continue
            # Neither name exists elsewhere → genuine rename
            rename_pairs.append((ext_node, orig_node))
            used_ext_idx.add(i)
            used_orig_idx.add(j)
            break
        else:
            still_unmatched_ext.append(ext_node)

    for j, orig_node in enumerate(unmatched_orig_sorted):
        if j not in used_orig_idx:
            still_unmatched_orig.append(orig_node)

    for ext_node, orig_node in rename_pairs:
        report.add_rename(ext_node.name, orig_node.name, confidence=1.0, parent=parent_name)
        if recurse and hasattr(ext_node, '_compare_children'):
            ext_node._compare_children(orig_node, report,
                                       all_extracted_names=all_extracted_names,
                                       all_original_names=all_original_names,
                                       extracted_story_to_inc=extracted_story_to_inc,
                                       original_story_to_inc=original_story_to_inc)

    # Phase 4: Remaining extracted = new, remaining original = removed
    # Use type-aware reporting so epics/sub-epics are not misclassified as stories
    for ext_node in still_unmatched_ext:
        _add_new_by_type(report, ext_node, parent_name=parent_name)
        _report_all_descendants_as_new(ext_node, report)

    for orig_node in still_unmatched_orig:
        _add_removed_by_type(report, orig_node, parent_name=parent_name)
        _report_all_descendants_as_removed(orig_node, report)


def _max_sub_epic_depth(node) -> int:
    """Max nesting depth of sub-epics under a domain node.

    Returns 0 if node has no sub-epics, 1 for flat sub-epics,
    2 for one level of nesting, etc.
    """
    sub_epics = []
    if hasattr(node, 'sub_epics'):
        sub_epics = list(node.sub_epics)
    elif hasattr(node, 'children'):
        sub_epics = [c for c in node.children if isinstance(c, SubEpic)]
    if not sub_epics:
        return 0
    return 1 + max(_max_sub_epic_depth(se) for se in sub_epics)


class _RowPositions:
    """Computes absolute Y positions for every row in the story map.

    All epics share the same row layout so stories across different
    epics line up horizontally.
    """

    def __init__(self, max_depth: int):
        self.max_depth = max(max_depth, 1)

    def sub_epic_y(self, depth: int) -> float:
        return EPIC_Y + EPIC_HEIGHT + ROW_GAP + depth * (SUB_EPIC_HEIGHT + ROW_GAP)

    @property
    def actor_y(self) -> float:
        deepest = self.sub_epic_y(self.max_depth - 1)
        return deepest + SUB_EPIC_HEIGHT + ACTOR_GAP

    @property
    def story_y(self) -> float:
        return self.actor_y + CELL_SIZE + ROW_GAP


# ---------------------------------------------------------------------------
# DrawIO Story Nodes
# ---------------------------------------------------------------------------

@dataclass
class DrawIOStoryNode(DiagramStoryNode):
    """DrawIO-specific node handling XML read/write.
    
    Inherits from DiagramStoryNode (platform-agnostic positioning/formatting)
    and adds DrawIO XML serialization via DrawIOElement.
    """
    _element: DrawIOElement = field(default=None, repr=False)

    def __post_init__(self):
        super().__post_init__()
        if self._element is None:
            self._element = DrawIOElement(cell_id=_slug(self.name), value=self.name)

    @property
    def children(self) -> List['StoryNode']:
        return list(self._children)

    @property
    def element(self) -> DrawIOElement:
        return self._element

    @property
    def position(self) -> Position:
        """Position from DrawIO XML element."""
        return self._element.position

    @property
    def boundary(self) -> Boundary:
        """Boundary from DrawIO XML element."""
        return self._element.boundary

    @property
    def fill(self) -> Optional[str]:
        return self._element.fill

    @property
    def stroke(self) -> Optional[str]:
        return self._element.stroke

    @property
    def font_color(self) -> Optional[str]:
        return self._element.font_color

    @property
    def shape(self) -> Optional[str]:
        return self._element.shape

    @property
    def cell_id(self) -> str:
        return self._element.cell_id

    def set_position(self, x: float, y: float):
        """Set position in DrawIO XML element."""
        self._element.set_position(x, y)

    def set_size(self, width: float, height: float):
        """Set size in DrawIO XML element."""
        self._element.set_size(width, height)

    def add_child(self, child: 'DrawIOStoryNode'):
        """Add child node (from DiagramStoryNode)."""
        child._parent = self
        self._children.append(child)

    def compute_container_dimensions_from_children(self, spacing: float = SPACING) -> Boundary:
        """Kept for backward compatibility but not used in row-based layout."""
        return self._element.boundary
    
    def containment_rules(self) -> dict:
        """Default containment rules. Subclasses override."""
        return {}
    
    def placement_rules(self) -> dict:
        """Default placement rules. Subclasses override."""
        return {}
    
    def formatting_rules(self) -> dict:
        """Default formatting rules. Subclasses override."""
        return {}
    
    @classmethod
    def create(cls, domain_node: StoryNode, parent: Optional['DiagramStoryNode'] = None):
        """Create DrawIO node from domain node. Subclasses implement."""
        raise NotImplementedError("Subclass must implement create()")
    
    @classmethod
    def recognizes(cls, element: any) -> bool:
        """Recognition logic. Subclasses implement."""
        raise NotImplementedError("Subclass must implement recognizes()")

    def _saved_position_for(self, key: str, layout_data) -> Optional[Position]:
        if layout_data:
            return layout_data.position_for(key)
        return None

    def collect_all_nodes(self) -> list:
        """Collect self and all descendant nodes for serialization."""
        nodes = [self]
        for child in self._children:
            if hasattr(child, 'collect_all_nodes'):
                nodes.extend(child.collect_all_nodes())
            else:
                nodes.append(child)
        return nodes


@dataclass
class DrawIOEpic(DiagramEpic, DrawIOStoryNode):
    """DrawIO representation of an Epic with XML serialization."""
    _parent: Optional[StoryNode] = field(default=None, repr=False)
    _element: DrawIOElement = field(default=None, repr=False)

    # Kept as class-level references for tests
    Y_DEFAULT = EPIC_Y
    X_START = 20
    SUB_EPIC_Y_OFFSET = ROW_GAP + EPIC_HEIGHT   # not used directly anymore

    def __post_init__(self):
        if self.domain_concepts is None:
            self.domain_concepts = []
        DiagramStoryNode.__post_init__(self)
        if self._element is None:
            self._element = DrawIOElement(cell_id=_slug(self.name), value=self.name)
        self._element.apply_style_for_type('epic')

    @property
    def children(self) -> List['StoryNode']:
        return list(self._children)

    def get_sub_epics(self) -> List['DrawIOSubEpic']:
        return [c for c in self._children if isinstance(c, DrawIOSubEpic)]

    @property
    def sub_epics(self) -> List['DrawIOSubEpic']:
        return self.get_sub_epics()

    def get_stories(self) -> List['DrawIOStory']:
        stories = []
        for sub_epic in self.get_sub_epics():
            stories.extend(sub_epic.get_all_stories_recursive())
        return stories

    @property
    def all_stories(self) -> List['DrawIOStory']:
        return self.get_stories()

    def render_from_domain(self, epic: Epic, x_pos: float,
                            rows: _RowPositions = None,
                            layout_data=None,
                            skip_stories: bool = False,
                            story_widths: dict = None,
                            render_ac: bool = False) -> 'DrawIOEpic':
        """Render epic as a flat horizontal bar spanning its sub-epics.

        The epic does NOT visually contain its sub-epics; it sits on
        its own row and its width spans from the first to the last
        sub-epic underneath it.

        When *skip_stories* is True sub-epics are rendered without
        story cells (used by increments view).

        When *story_widths* is provided (exploration view), stories are
        spaced apart based on their widest AC box width.
        """
        from .drawio_story_node_serializer import DrawIOStoryNodeSerializer

        if rows is None:
            depth = _max_sub_epic_depth(epic)
            rows = _RowPositions(depth)

        epic_slug = _slug(self.name)
        self._element._cell_id = epic_slug

        cursor_x = x_pos + BAR_PADDING
        for sub_epic in epic.sub_epics:
            drawio_se = DrawIOStoryNodeSerializer.create_sub_epic(
                sub_epic.name, getattr(sub_epic, 'sequential_order', 0) or 0)
            cursor_x = drawio_se.render_from_domain(
                sub_epic, cursor_x, depth=0, rows=rows,
                layout_data=layout_data, path_prefix=epic_slug,
                skip_stories=skip_stories,
                story_widths=story_widths,
                render_ac=render_ac)
            self.add_child(drawio_se)
            cursor_x += CELL_SPACING

        # Remove trailing spacing
        if epic.sub_epics:
            cursor_x -= CELL_SPACING

        saved = self._saved_position_for(f'EPIC|{self.name}', layout_data)
        epic_x = saved.x if saved else x_pos
        epic_y = saved.y if saved else EPIC_Y
        self.set_position(epic_x, epic_y)
        self.set_size(max(cursor_x - x_pos + BAR_PADDING, 100), EPIC_HEIGHT)
        return self

    def collect_all_nodes(self) -> list:
        nodes = [self]
        for se in self.get_sub_epics():
            nodes.extend(se.collect_all_nodes())
        return nodes

    def _compare_children(self, original_epic, report: UpdateReport, *,
                          all_extracted_names: Set[str] = None,
                          all_original_names: Set[str] = None,
                          extracted_story_to_inc: dict = None,
                          original_story_to_inc: dict = None):
        _compare_node_lists(self.get_sub_epics(), original_epic.sub_epics,
                            report, parent_name=self.name, recurse=True,
                            all_extracted_names=all_extracted_names,
                            all_original_names=all_original_names,
                            extracted_story_to_inc=extracted_story_to_inc,
                            original_story_to_inc=original_story_to_inc)


@dataclass
class DrawIOSubEpic(DiagramSubEpic, DrawIOStoryNode):
    """DrawIO representation of a SubEpic with XML serialization."""
    _parent: Optional[StoryNode] = field(default=None, repr=False)
    _element: DrawIOElement = field(default=None, repr=False)

    # Kept for backward-compat references
    Y_OFFSET_FROM_PARENT = SUB_EPIC_HEIGHT + ROW_GAP
    STORY_Y_OFFSET = 0   # not used in row-based layout

    def __post_init__(self):
        if self.domain_concepts is None:
            self.domain_concepts = []
        DiagramStoryNode.__post_init__(self)
        if self._element is None:
            self._element = DrawIOElement(cell_id=_slug(self.name), value=self.name)
        self._element.apply_style_for_type('sub_epic')
        if not hasattr(self, 'test_file'):
            self.test_file = None

    @property
    def children(self) -> List['StoryNode']:
        return list(self._children)

    def get_sub_epics(self) -> List['DrawIOSubEpic']:
        return [c for c in self._children if isinstance(c, DrawIOSubEpic)]

    def get_stories(self) -> List['DrawIOStory']:
        return sorted([c for c in self._children if isinstance(c, DrawIOStory)],
                       key=lambda s: s.sequential_order or 0)

    def get_all_stories_recursive(self) -> List['DrawIOStory']:
        stories = list(self.get_stories())
        for nested_se in self.get_sub_epics():
            stories.extend(nested_se.get_all_stories_recursive())
        return stories

    @property
    def all_stories(self) -> List['DrawIOStory']:
        return self.get_stories()

    def render_from_domain(self, sub_epic, x_cursor: float, depth: int,
                            rows: _RowPositions,
                            layout_data=None,
                            path_prefix: str = '',
                            skip_stories: bool = False,
                            story_widths: dict = None,
                            render_ac: bool = False) -> float:
        """Render sub-epic as a flat horizontal bar.

        Returns the x position of the right edge of this sub-epic's
        content (so the caller knows where to place the next sibling).

        When *skip_stories* is True the sub-epic computes its width
        from the number of domain stories but does not create story
        cells (used by increments view).

        When *story_widths* is provided (exploration view), the
        horizontal spacing between stories is determined by each
        story's widest AC box, so acceptance criteria don't overlap.
        """
        from .drawio_story_node_serializer import DrawIOStoryNodeSerializer

        se_path = f'{path_prefix}/{_slug(self.name)}' if path_prefix else _slug(self.name)
        self._element._cell_id = se_path

        nested = [c for c in sub_epic.children if isinstance(c, SubEpic)]
        start_x = x_cursor

        if nested:
            inner_x = x_cursor + BAR_PADDING
            for n in nested:
                drawio_n = DrawIOStoryNodeSerializer.create_sub_epic(
                    n.name, getattr(n, 'sequential_order', 0) or 0)
                inner_x = drawio_n.render_from_domain(
                    n, inner_x, depth + 1, rows, layout_data,
                    path_prefix=se_path,
                    skip_stories=skip_stories,
                    story_widths=story_widths,
                    render_ac=render_ac)
                self.add_child(drawio_n)
                inner_x += CELL_SPACING
            inner_x -= CELL_SPACING  # remove trailing
            end_x = inner_x + BAR_PADDING
        else:
            stories = [c for c in sub_epic.children if isinstance(c, Story)]
            stories.sort(key=lambda s: getattr(s, 'sequential_order', 0) or 0)

            # Disambiguate duplicate story names to ensure unique cell_ids
            slug_counts: dict = {}
            for s in stories:
                slug = _slug(s.name)
                slug_counts[slug] = slug_counts.get(slug, 0) + 1

            if skip_stories:
                story_count = len(stories)
                if story_count:
                    content_width = story_count * CELL_SIZE + (story_count - 1) * CELL_SPACING
                else:
                    content_width = CELL_SIZE
                end_x = x_cursor + BAR_PADDING + content_width + BAR_PADDING
            else:
                se_saved = self._saved_position_for(f'SUB_EPIC|{self.name}', layout_data)
                se_right = (se_saved.x + layout_data.boundary_for(f'SUB_EPIC|{self.name}').width) if (se_saved and layout_data and layout_data.boundary_for(f'SUB_EPIC|{self.name}')) else None
                se_left = x_cursor + BAR_PADDING

                story_x = se_left
                story_y = rows.story_y
                seen_actors: set = set()
                seen_slugs: dict = {}
                for story in stories:
                    story_type = getattr(story, 'story_type', 'user') or 'user'
                    drawio_story = DrawIOStoryNodeSerializer.create_story(
                        story.name, getattr(story, 'sequential_order', 0) or 0, story_type)
                    slug = _slug(drawio_story.name)
                    if slug_counts.get(slug, 0) > 1:
                        seen_slugs[slug] = seen_slugs.get(slug, 0) + 1
                        base = f'{slug}-{seen_slugs[slug]}'
                    else:
                        base = slug
                    story_path = f'{se_path}/{base}' if se_path else base
                    has_saved = layout_data and layout_data.position_for(story_path)
                    if has_saved:
                        drawio_story.render_from_domain(
                            story, story_x, story_y, rows.actor_y,
                            path_prefix=se_path, seen_actors=seen_actors,
                            layout_data=layout_data, render_ac=render_ac,
                            cell_id_override=story_path)
                    else:
                        if se_right and story_x + CELL_SIZE > se_right:
                            story_x = se_left
                            story_y += CELL_SIZE + CELL_SPACING
                        drawio_story.render_from_domain(
                            story, story_x, story_y, rows.actor_y,
                            path_prefix=se_path, seen_actors=seen_actors,
                            layout_data=None, render_ac=render_ac,
                            cell_id_override=story_path)
                    self.add_child(drawio_story)
                    # Advance X by the AC width if in exploration mode,
                    # otherwise by the standard cell size.
                    ac_w = story_widths.get(story.name, CELL_SIZE) if story_widths else CELL_SIZE
                    story_x += max(CELL_SIZE, ac_w) + CELL_SPACING
                if stories:
                    story_x -= CELL_SPACING
                end_x = story_x + BAR_PADDING

        se_y = rows.sub_epic_y(depth)
        self.set_position(start_x, se_y)
        self.set_size(max(end_x - start_x, CELL_SIZE + 2 * BAR_PADDING),
                       SUB_EPIC_HEIGHT)
        return end_x

    def collect_all_nodes(self) -> list:
        nodes = [self]
        for se in self.get_sub_epics():
            nodes.extend(se.collect_all_nodes())
        for story in self.get_stories():
            nodes.extend(story.collect_all_nodes())
        return nodes

    def _compare_children(self, original_sub_epic, report: UpdateReport, *,
                          all_extracted_names: Set[str] = None,
                          all_original_names: Set[str] = None,
                          extracted_story_to_inc: dict = None,
                          original_story_to_inc: dict = None):
        orig_nested = [c for c in original_sub_epic._children if isinstance(c, SubEpic)]
        _compare_node_lists(self.get_sub_epics(), orig_nested,
                            report, parent_name=self.name, recurse=True,
                            all_extracted_names=all_extracted_names,
                            all_original_names=all_original_names,
                            extracted_story_to_inc=extracted_story_to_inc,
                            original_story_to_inc=original_story_to_inc)

        # Deduplicate extracted stories by name.  The same story can
        # appear multiple times in the tree when it lives in several
        # increment lanes (each lane copy is assigned to the same
        # sub-epic by X-position).  Keep the first occurrence.
        seen_names: set = set()
        unique_stories: list = []
        for s in self.get_stories():
            if s.name not in seen_names:
                seen_names.add(s.name)
                unique_stories.append(s)

        orig_stories = [c for c in original_sub_epic.children if isinstance(c, Story)]
        _compare_node_lists(unique_stories, orig_stories,
                            report, parent_name=self.name, recurse=False,
                            all_extracted_names=all_extracted_names,
                            all_original_names=all_original_names,
                            extracted_story_to_inc=extracted_story_to_inc,
                            original_story_to_inc=original_story_to_inc)


@dataclass
class DrawIOStory(DiagramStory, DrawIOStoryNode):
    """DrawIO representation of a Story with XML serialization."""
    _parent: Optional[StoryNode] = field(default=None, repr=False)
    _element: DrawIOElement = field(default=None, repr=False)

    # Stories are 50x50 sticky-note squares
    WIDTH = CELL_SIZE
    HEIGHT = CELL_SIZE
    ACTOR_HEIGHT = CELL_SIZE
    ACTOR_SPACING = 2
    AC_MIN_WIDTH = 250
    AC_HEIGHT = 60
    AC_SPACING_Y = 10
    AC_CHAR_WIDTH = 6
    AC_PADDING = 10

    STORY_TYPE_STYLES = {
        'user': 'story_user',
        None: 'story_user',
        '': 'story_user',
        'system': 'story_system',
        'technical': 'story_technical',
    }

    def __post_init__(self):
        if self.users is None:
            self.users = []
        DiagramStoryNode.__post_init__(self)
        if self._element is None:
            self._element = DrawIOElement(cell_id=_slug(self.name), value=self.name)
        style_key = self.STORY_TYPE_STYLES.get(self.story_type, 'story_user')
        self._element.apply_style_for_type(style_key)
        self._actor_elements: List[DrawIOElement] = []
        self._ac_elements: List[DrawIOElement] = []

    @property
    def children(self) -> List['StoryNode']:
        return list(self._children)

    def render_from_domain(self, story, x_pos: float, story_y: float,
                            actor_y: float = 0,
                            path_prefix: str = '',
                            seen_actors: set = None,
                            layout_data=None,
                            render_ac: bool = False,
                            cell_id_override: str = None) -> 'DrawIOStory':
        story_path = cell_id_override if cell_id_override else (
            f'{path_prefix}/{_slug(self.name)}' if path_prefix else _slug(self.name))
        self._element._cell_id = story_path

        saved = self._saved_position_for(story_path, layout_data)
        final_x = saved.x if saved else x_pos
        final_y = saved.y if saved else story_y
        self.set_position(final_x, final_y)
        self.set_size(CELL_SIZE, CELL_SIZE)

        # Actors placed directly above this story (deduplicated within sub-epic)
        users = getattr(story, 'users', []) or []
        for user in users:
            user_name = user.name if hasattr(user, 'name') else str(user)
            if seen_actors is not None:
                if user_name in seen_actors:
                    continue
                seen_actors.add(user_name)
            actor = DrawIOElement(
                cell_id=f'{story_path}/actor-{_slug(user_name)}',
                value=user_name)
            actor.apply_style_for_type('actor')
            actor.set_position(x_pos, actor_y)
            actor.set_size(CELL_SIZE, CELL_SIZE)
            self._actor_elements.append(actor)
        
        # Render AC boxes if requested (acceptance_criteria diagram type)
        if render_ac:
            self.render_ac_boxes(story)
        
        return self

    @staticmethod
    def compute_ac_width(domain_story) -> float:
        """Return the width needed for AC boxes of this story.

        All AC boxes use a consistent fixed width (AC_MIN_WIDTH) since
        the text wraps inside the box.  Returns CELL_SIZE if no AC.
        """
        ac_list = getattr(domain_story, 'acceptance_criteria', []) or []
        if not ac_list:
            return CELL_SIZE
        return DrawIOStory.AC_MIN_WIDTH

    @staticmethod
    def _format_ac_text_static(ac) -> str:
        if hasattr(ac, 'name') and ac.name:
            return ac.name
        if isinstance(ac, str):
            return ac
        if isinstance(ac, dict):
            return ac.get('name', ac.get('description', ''))
        return str(ac) if ac else ''

    def render_ac_boxes(self, domain_story) -> List[DrawIOElement]:
        """Create acceptance criteria DrawIOElements below this story."""
        ac_list = getattr(domain_story, 'acceptance_criteria', []) or []
        if not ac_list:
            return []

        elements = []
        ac_y = self.position.y + self.HEIGHT + self.AC_SPACING_Y

        for idx, ac in enumerate(ac_list):
            text = self._format_ac_text(ac)
            if not text:
                continue
            ac_elem = DrawIOElement(
                cell_id=f'{self.cell_id}/ac-{idx}',
                value=text)
            ac_elem.apply_style_for_type('acceptance_criteria')
            ac_elem.set_position(self.position.x, ac_y)
            ac_elem.set_size(self.AC_MIN_WIDTH, self.AC_HEIGHT)
            elements.append(ac_elem)
            ac_y += self.AC_HEIGHT + self.AC_SPACING_Y

        self._ac_elements = elements
        return elements

    def _format_ac_text(self, ac) -> str:
        if hasattr(ac, 'name') and ac.name:
            return ac.name
        if isinstance(ac, str):
            return ac
        if isinstance(ac, dict):
            return ac.get('name', ac.get('description', ''))
        return str(ac) if ac else ''

    def collect_all_nodes(self) -> list:
        nodes = [self]
        nodes.extend(self._actor_elements)
        nodes.extend(self._ac_elements)
        return nodes



class DrawIOIncrementLane:
    """An increment lane (horizontal band) in the story map diagram."""

    LABEL_Y_OFFSET = 5       # label starts 5px below lane top
    LABEL_HEIGHT = 30
    LABEL_WIDTH = 150
    ACTOR_Y_OFFSET = 40      # actor starts below label (5+30+5)
    ACTOR_SIZE = CELL_SIZE    # 50x50 – consistent with outline actors
    STORY_Y_OFFSET = 95      # story starts below actor (40+50+5)
    LANE_HEIGHT = 155         # label(30) + gap + actor(50) + gap + story(50) + pad

    def __init__(self, name: str, priority: int, story_names: list):
        self.name = name
        self.priority = priority
        self.story_names = set(story_names)
        self._lane_element: Optional[DrawIOElement] = None
        self._label_element: Optional[DrawIOElement] = None
        self._story_copies: List[DrawIOElement] = []
        self._actor_elements: List[DrawIOElement] = []

    def render(self, index: int, y_start: float, total_width: float,
               stories: List['DrawIOStory'],
               domain_stories: Optional[list] = None) -> float:
        """Render an increment lane with stories and actor labels.

        Args:
            stories: DrawIOStory objects from the outline render (used for
                     position and style info).
            domain_stories: Original domain Story objects (used for user
                           info to render actor labels).
        """
        lane_y = y_start + index * self.LANE_HEIGHT

        lane_slug = _slug(self.name)
        self._lane_element = DrawIOElement(cell_id=f'inc-lane/{lane_slug}', value='')
        self._lane_element.apply_style_for_type('increment_lane')
        self._lane_element.set_position(0, lane_y)
        self._lane_element.set_size(total_width + 40, self.LANE_HEIGHT)

        self._label_element = DrawIOElement(cell_id=f'inc-label/{lane_slug}', value=self.name)
        self._label_element.apply_style_for_type('increment_lane')
        self._label_element.set_position(5, lane_y + self.LABEL_Y_OFFSET)
        self._label_element.set_size(self.LABEL_WIDTH, self.LABEL_HEIGHT)

        # Build lookup from story name to domain story for user info
        domain_by_name = {}
        if domain_stories:
            for ds in domain_stories:
                ds_name = ds.name if hasattr(ds, 'name') else str(ds)
                domain_by_name[ds_name] = ds

        self._story_copies = []
        self._actor_elements = []
        seen_actors: set = set()
        for story in stories:
            if story.name in self.story_names:
                copy = DrawIOElement(
                    cell_id=f'inc-lane/{lane_slug}/{story.cell_id}',
                    value=story.name)
                style_key = DrawIOStory.STORY_TYPE_STYLES.get(story.story_type, 'story_user')
                copy.apply_style_for_type(style_key)
                copy.set_position(story.position.x, lane_y + self.STORY_Y_OFFSET)
                copy.set_size(CELL_SIZE, CELL_SIZE)
                self._story_copies.append(copy)

                # Actor labels above stories (deduplicated per lane)
                domain_story = domain_by_name.get(story.name)
                if domain_story:
                    users = getattr(domain_story, 'users', []) or []
                    for user in users:
                        user_name = user.name if hasattr(user, 'name') else str(user)
                        if user_name in seen_actors:
                            continue
                        seen_actors.add(user_name)
                        actor = DrawIOElement(
                            cell_id=f'inc-lane/{lane_slug}/actor-{_slug(user_name)}',
                            value=user_name)
                        actor.apply_style_for_type('actor')
                        actor.set_position(story.position.x, lane_y + self.ACTOR_Y_OFFSET)
                        actor.set_size(self.ACTOR_SIZE, self.ACTOR_SIZE)
                        self._actor_elements.append(actor)

        return self.LANE_HEIGHT

    def collect_all_elements(self) -> list:
        elements = []
        if self._lane_element:
            elements.append(self._lane_element)
        if self._label_element:
            elements.append(self._label_element)
        elements.extend(self._actor_elements)
        elements.extend(self._story_copies)
        return elements
