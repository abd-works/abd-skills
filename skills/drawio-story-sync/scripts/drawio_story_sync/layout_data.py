"""
LayoutData - Stores position and size per node for diagram re-rendering.

Persisted as JSON alongside the diagram file. Used to preserve positions
when re-rendering after story graph changes.
"""
import json
from pathlib import Path
from typing import Optional, Dict, Any
from .story_io_position import Position, Boundary


class LayoutData:

    def __init__(self, entries: Dict[str, Dict[str, float]] = None):
        self._entries = entries or {}

    @property
    def entries(self) -> Dict[str, Dict[str, float]]:
        return dict(self._entries)

    def position_for(self, node_key: str) -> Optional[Position]:
        entry = self._entries.get(node_key)
        if entry and 'x' in entry and 'y' in entry:
            return Position(entry['x'], entry['y'])
        return None

    def boundary_for(self, node_key: str) -> Optional[Boundary]:
        entry = self._entries.get(node_key)
        if entry and all(k in entry for k in ('x', 'y', 'width', 'height')):
            return Boundary(entry['x'], entry['y'], entry['width'], entry['height'])
        return None

    def has_entry(self, node_key: str) -> bool:
        return node_key in self._entries

    def set_entry(self, node_key: str, x: float, y: float, width: float, height: float):
        self._entries[node_key] = {'x': x, 'y': y, 'width': width, 'height': height}

    def save(self, file_path: Path):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(self._entries, indent=2), encoding='utf-8')

    @classmethod
    def load(cls, file_path: Path) -> Optional['LayoutData']:
        if not file_path.exists():
            return None
        content = file_path.read_text(encoding='utf-8')
        entries = json.loads(content)
        return cls(entries)
