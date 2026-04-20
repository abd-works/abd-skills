"""
DiagramStoryNode - Platform-agnostic diagram node hierarchy.

This module provides the middle tier between domain nodes (StoryNode) and 
platform-specific diagram nodes (DrawIOStoryNode). It contains positioning,
containment, and formatting rules that are independent of any specific
diagramming tool.
"""
from abc import abstractmethod
from typing import List, Optional, TYPE_CHECKING
from dataclasses import dataclass, field

from story_graph.nodes import StoryNode, Epic, SubEpic, Story
from .story_io_position import Position, Boundary

if TYPE_CHECKING:
    from story_graph.nodes import Increment


# ---------------------------------------------------------------------------
# Layout constants (platform-agnostic)
# ---------------------------------------------------------------------------
CELL_SIZE = 50           # Stories and actors are 50x50 squares
CELL_SPACING = 10        # Horizontal gap between cells
EPIC_Y = 120             # Y position of epic row
EPIC_HEIGHT = 60         # Height of epic bar
SUB_EPIC_HEIGHT = 60     # Height of sub-epic bar
ROW_GAP = 15             # Gap between rows
ACTOR_GAP = 25           # Extra gap before actor row
BAR_PADDING = 5          # Internal horizontal padding for bars
SPACING = CELL_SPACING
CONTAINER_PADDING = BAR_PADDING


@dataclass
class DiagramStoryNode(StoryNode):
    """Platform-agnostic diagram node with positioning and formatting rules.
    
    Inherits from StoryNode and adds diagram-specific properties and methods
    for positioning, containment, and formatting. Subclasses implement
    specific rules for epics, sub-epics, stories, and increments.
    
    Platform-specific implementations (like DrawIO) inherit from the concrete
    subclasses and add XML read/write capabilities.
    """
    
    @property
    @abstractmethod
    def position(self) -> Position:
        """Get the node's position in the diagram."""
        pass
    
    @property
    @abstractmethod
    def boundary(self) -> Boundary:
        """Get the node's boundary (position + size)."""
        pass
    
    @abstractmethod
    def containment_rules(self) -> dict:
        """Return containment rules for this node type.
        
        Returns dict with:
        - allowed_parents: List of parent node types that can contain this node
        - contains_check: Function to determine if a point is inside this node
        """
        pass
    
    @abstractmethod
    def placement_rules(self) -> dict:
        """Return placement rules for this node type.
        
        Returns dict with positioning rules like:
        - x_calculation: How to calculate X position
        - y_calculation: How to calculate Y position
        - spacing: Spacing from siblings
        """
        pass
    
    @abstractmethod
    def formatting_rules(self) -> dict:
        """Return formatting rules for this node type.
        
        Returns dict with visual styling:
        - fill: Fill color
        - stroke: Border color
        - font_color: Text color
        - shape: Shape type (rounded, rectangle, etc.)
        """
        pass
    
    def compute_container_dimensions_from_children(self, spacing: float = SPACING) -> Boundary:
        """Compute container boundary from children positions.
        
        Default implementation returns current boundary. Subclasses override
        to calculate from children.
        
        Args:
            spacing: Space between children
            
        Returns:
            Boundary for the container
        """
        return self.boundary
    
    @classmethod
    @abstractmethod
    def create(cls, domain_node: StoryNode, parent: Optional['DiagramStoryNode'] = None):
        """Create a diagram node from a domain node.
        
        This mirrors the pattern in StoryNode.create(). Each subclass implements
        to create the correct diagram node type from the domain node.
        
        Args:
            domain_node: The domain node (Epic, SubEpic, Story, etc.)
            parent: Optional parent diagram node
            
        Returns:
            Instance of the appropriate DiagramStoryNode subclass
        """
        pass
    
    def add_child(self, child: 'DiagramStoryNode'):
        """Add a child node and apply placement rules.
        
        Args:
            child: Child node to add
        """
        child._parent = self
        self._children.append(child)
    
    def move_to(self, new_parent: 'DiagramStoryNode'):
        """Move this node to a new parent.
        
        Applies containment and placement rules for the new location.
        
        Args:
            new_parent: The new parent node
        """
        # Remove from current parent
        if self._parent:
            self._parent._children.remove(self)
        
        # Add to new parent
        new_parent.add_child(self)
    
    def delete(self):
        """Remove this node from its parent."""
        if self._parent:
            self._parent._children.remove(self)
            self._parent = None
    
    def rename(self, new_name: str):
        """Rename this node.
        
        Args:
            new_name: The new name for the node
        """
        self.name = new_name
    
    @classmethod
    @abstractmethod
    def recognizes(cls, element: any) -> bool:
        """Determine if this node type recognizes the given element.
        
        Used for classification during diagram loading. Each subclass decides
        internally how to recognize its type from diagram elements.
        
        Args:
            element: The element to check (platform-specific, e.g. DrawIOElement)
            
        Returns:
            True if this node type should handle the element
        """
        pass


@dataclass
class DiagramEpic(Epic, DiagramStoryNode):
    """Diagram representation of an Epic with positioning and formatting."""
    
    _parent: Optional[StoryNode] = field(default=None, repr=False)
    
    def containment_rules(self) -> dict:
        """Epics are top-level containers."""
        return {
            'allowed_parents': [],  # Top-level, no parents
            'contains_sub_epics': True,
            'contains_stories': False  # Stories go in sub-epics
        }
    
    def placement_rules(self) -> dict:
        """Epics are positioned at EPIC_Y, spanning sub-epics."""
        return {
            'y': EPIC_Y,
            'height': EPIC_HEIGHT,
            'span_children': True
        }
    
    def formatting_rules(self) -> dict:
        """Epic visual style."""
        return {
            'fill': '#e1d5e7',
            'stroke': '#9673a6',
            'font_color': 'black',
            'shape': 'rounded'
        }
    
    @classmethod
    def create(cls, domain_node: Epic, parent: Optional['DiagramStoryNode'] = None):
        """Create DiagramEpic from domain Epic.
        
        Subclasses (like DrawIOEpic) will override to add platform-specific initialization.
        """
        raise NotImplementedError("Subclass must implement create()")
    
    @classmethod
    def recognizes(cls, element: any) -> bool:
        """Subclass implements recognition logic."""
        raise NotImplementedError("Subclass must implement recognizes()")


@dataclass
class DiagramSubEpic(SubEpic, DiagramStoryNode):
    """Diagram representation of a SubEpic with positioning and formatting."""
    
    _parent: Optional[StoryNode] = field(default=None, repr=False)
    
    def containment_rules(self) -> dict:
        """Sub-epics are contained in epics or other sub-epics."""
        return {
            'allowed_parents': [DiagramEpic, DiagramSubEpic],
            'contains_sub_epics': True,
            'contains_stories': True
        }
    
    def placement_rules(self) -> dict:
        """Sub-epics positioned below parent with offset."""
        return {
            'y_offset': 75,  # Below parent
            'height': SUB_EPIC_HEIGHT,
            'span_children': True
        }
    
    def formatting_rules(self) -> dict:
        """Sub-epic visual style."""
        return {
            'fill': '#d5e8d4',
            'stroke': '#82b366',
            'font_color': 'black',
            'shape': 'rounded'
        }
    
    @classmethod
    def create(cls, domain_node: SubEpic, parent: Optional['DiagramStoryNode'] = None):
        """Create DiagramSubEpic from domain SubEpic."""
        raise NotImplementedError("Subclass must implement create()")
    
    @classmethod
    def recognizes(cls, element: any) -> bool:
        """Subclass implements recognition logic."""
        raise NotImplementedError("Subclass must implement recognizes()")


@dataclass  
class DiagramStory(Story, DiagramStoryNode):
    """Diagram representation of a Story with positioning and formatting."""
    
    _parent: Optional[StoryNode] = field(default=None, repr=False)
    
    def containment_rules(self) -> dict:
        """Stories are contained in sub-epics."""
        return {
            'allowed_parents': [DiagramSubEpic],
            'contains_sub_epics': False,
            'contains_stories': False
        }
    
    def placement_rules(self) -> dict:
        """Stories positioned as cells in a row."""
        return {
            'size': CELL_SIZE,
            'spacing': CELL_SPACING,
            'layout': 'left-to-right'
        }
    
    def formatting_rules(self) -> dict:
        """Story visual style varies by story_type."""
        story_type = getattr(self, 'story_type', 'user')
        
        if story_type == 'user':
            return {
                'fill': '#fff2cc',
                'stroke': '#d6b656',
                'font_color': 'black',
                'shape': 'rectangle'
            }
        elif story_type == 'system':
            return {
                'fill': '#1a237e',
                'stroke': '#0d47a1',
                'font_color': 'white',
                'shape': 'rectangle'
            }
        elif story_type == 'technical':
            return {
                'fill': '#000000',
                'stroke': '#333333',
                'font_color': 'white',
                'shape': 'rectangle'
            }
        else:
            # Default
            return {
                'fill': '#fff2cc',
                'stroke': '#d6b656',
                'font_color': 'black',
                'shape': 'rectangle'
            }
    
    @classmethod
    def create(cls, domain_node: Story, parent: Optional['DiagramStoryNode'] = None):
        """Create DiagramStory from domain Story."""
        raise NotImplementedError("Subclass must implement create()")
    
    @classmethod
    def recognizes(cls, element: any) -> bool:
        """Subclass implements recognition logic."""
        raise NotImplementedError("Subclass must implement recognizes()")


@dataclass
class DiagramIncrement(DiagramStoryNode):
    """Diagram representation of an Increment with positioning and formatting.
    
    Note: Increment is not yet a full StoryNode in the domain model,
    so this doesn't inherit from a domain Increment class yet.
    """
    
    _parent: Optional[StoryNode] = field(default=None, repr=False)
    priority: int = 1
    stories: List = field(default_factory=list)
    
    @property
    def children(self) -> List[StoryNode]:
        """Increments don't have hierarchical children."""
        return []
    
    def containment_rules(self) -> dict:
        """Increments are independent lanes."""
        return {
            'allowed_parents': [],  # Top-level
            'contains_sub_epics': False,
            'contains_stories': False  # References stories, doesn't contain them
        }
    
    def placement_rules(self) -> dict:
        """Increments positioned as horizontal lanes."""
        return {
            'layout': 'horizontal-lane',
            'ordered_by': 'priority',
            'fixed_height': True
        }
    
    def formatting_rules(self) -> dict:
        """Increment visual style."""
        return {
            'fill': '#f5f5f5',
            'stroke': '#666666',
            'font_color': 'black',
            'font_weight': 'bold',
            'shape': 'rectangle'
        }
    
    @classmethod
    def create(cls, domain_node: 'Increment', parent: Optional['DiagramStoryNode'] = None):
        """Create DiagramIncrement from domain Increment."""
        raise NotImplementedError("Subclass must implement create()")
    
    @classmethod
    def recognizes(cls, element: any) -> bool:
        """Subclass implements recognition logic."""
        raise NotImplementedError("Subclass must implement recognizes()")
