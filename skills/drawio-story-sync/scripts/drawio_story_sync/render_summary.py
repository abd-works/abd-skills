"""
RenderSummary - Typed return object for render operations.

Replaces Dict[str, Any] returns with a strongly-typed object.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class RenderSummary:
    """Summary of a diagram render operation.
    
    Attributes:
        epics: Number of epics rendered
        sub_epic_count: Number of sub-epics rendered
        story_count: Number of stories rendered
        diagram_generated: Whether the diagram was successfully generated
        increments: Optional number of increments rendered (for increment diagrams)
        ac_count: Optional number of acceptance criteria rendered (for AC diagrams)
    """
    epics: int
    sub_epic_count: int
    diagram_generated: bool
    story_count: int = 0
    increments: Optional[int] = None
    ac_count: Optional[int] = None
    exploration: bool = False
    
    def __getitem__(self, key: str):
        """Support dict-style access for backward compatibility."""
        if key == 'epics':
            return self.epics
        elif key == 'sub_epic_count':
            return self.sub_epic_count
        elif key == 'diagram_generated':
            return self.diagram_generated
        elif key == 'story_count':
            return self.story_count
        elif key == 'increments':
            return self.increments
        elif key == 'ac_count':
            return self.ac_count
        elif key == 'exploration':
            return self.exploration
        else:
            raise KeyError(f"'{key}' not found in RenderSummary")
    
    def __setitem__(self, key: str, value):
        """Support dict-style setting for backward compatibility."""
        if key == 'epics':
            self.epics = value
        elif key == 'sub_epic_count':
            self.sub_epic_count = value
        elif key == 'diagram_generated':
            self.diagram_generated = value
        elif key == 'story_count':
            self.story_count = value
        elif key == 'increments':
            self.increments = value
        elif key == 'ac_count':
            self.ac_count = value
        elif key == 'exploration':
            self.exploration = value
        else:
            raise KeyError(f"Cannot set '{key}' in RenderSummary")
    
    def get(self, key: str, default=None):
        """Support dict.get() for backward compatibility."""
        try:
            return self[key]
        except KeyError:
            return default
    
    def __contains__(self, key: str) -> bool:
        """Support 'in' operator for backward compatibility."""
        return key in ['epics', 'sub_epic_count', 'diagram_generated', 'story_count', 
                       'increments', 'ac_count', 'exploration']
    
    def __eq__(self, other) -> bool:
        """Support comparison with dict for backward compatibility."""
        if isinstance(other, dict):
            return self.to_dict() == other
        return super().__eq__(other)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for backward compatibility."""
        result = {
            'epics': self.epics,
            'sub_epic_count': self.sub_epic_count,
            'diagram_generated': self.diagram_generated
        }
        if self.story_count > 0:
            result['story_count'] = self.story_count
        if self.increments is not None:
            result['increments'] = self.increments
        if self.ac_count is not None:
            result['ac_count'] = self.ac_count
        if self.exploration:
            result['exploration'] = True
        return result
