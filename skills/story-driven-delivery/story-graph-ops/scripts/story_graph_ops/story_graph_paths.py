"""Centralized path resolution for story graph and documentation outputs."""
from pathlib import Path
from typing import List, Optional


class StoryGraphPaths:
    """Centralized path resolution for story graph and documentation outputs.
    
    Provides a single source of truth for all documentation paths:
    - docs/story/ for story_bot outputs
    - docs/crc/ for crc_bot outputs
    - Behavior-specific subfolders (shape, exploration, scenarios, etc.)
    """
    
    def __init__(self, workspace_directory: Path, bot_name: str = 'story'):
        """Initialize path resolver.
        
        Args:
            workspace_directory: Root workspace directory
            bot_name: Bot name (e.g., 'story_bot' or 'story'). 
                      The '_bot' suffix is automatically stripped.
        """
        self._workspace_directory = workspace_directory
        # story_bot -> story, crc_bot -> crc
        self._bot_name = bot_name.replace('_bot', '')
    
    @property
    def workspace_directory(self) -> Path:
        """Root workspace directory."""
        return self._workspace_directory
    
    @property
    def bot_name(self) -> str:
        """Bot name without _bot suffix."""
        return self._bot_name
    
    @property
    def docs_root(self) -> Path:
        """Root docs folder for this bot: docs/story/ or docs/crc/"""
        return self._workspace_directory / 'docs' / self._bot_name
    
    @property
    def story_graph_path(self) -> Path:
        """Path to story-graph.json.
        
        Note: Only story_bot has a story-graph.json. Other bots share it.
        For non-story bots, this still points to docs/story/story-graph.json.
        """
        if self._bot_name == 'story':
            return self.docs_root / 'story-graph.json'
        # Other bots share the story_bot's story-graph.json
        return self._workspace_directory / 'docs' / 'story' / 'story-graph.json'
    
    @property
    def story_graph_cache_path(self) -> Path:
        """Path to story graph enriched cache file."""
        return self.story_graph_path.parent / '.story-graph-enriched-cache.json'
    
    def behavior_path(self, behavior: str) -> Path:
        """Path for behavior-specific outputs: docs/story/shape/
        
        Args:
            behavior: Behavior name (e.g., 'shape', 'exploration', 'scenarios')
        """
        return self.docs_root / behavior
    
    @property
    def bot_workspace_config_path(self) -> Path:
        """Path for bot workspace config: docs/<bot>/bot_workspace.json.
        Stores behavior/action configuration: execution mode, special instructions."""
        return self.docs_root / 'bot_workspace.json'

    @property
    def scenarios_path(self) -> Path:
        """Path for scenario markdown files.
        
        This is the folder containing the story scenario documentation
        organized by epic/subepic/story structure.
        """
        return self.behavior_path('scenarios')
    
    def ensure_folders(self, behaviors: Optional[List[str]] = None) -> None:
        """Create documentation folders for each behavior if missing.
        
        Args:
            behaviors: List of behavior names. If None, only creates docs_root.
        """
        self.docs_root.mkdir(parents=True, exist_ok=True)
        if behaviors:
            for behavior in behaviors:
                self.behavior_path(behavior).mkdir(parents=True, exist_ok=True)
