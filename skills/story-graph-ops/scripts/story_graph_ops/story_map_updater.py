"""
StoryMapUpdater - Owns comparison and merge logic between two story maps.

This module extracts update/merge logic from StoryMap.apply_update_report()
into a dedicated updater class.
"""
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from story_graph_ops.nodes import StoryMap
    from story_graph_ops.update_report import UpdateReport


class StoryMapUpdater:
    """Owns comparison and merge logic between two story maps.
    
    Instantiated with the target map. Can generate reports from source maps
    and apply changes to the target.
    """
    
    def __init__(self, target_map: 'StoryMap'):
        """Initialize with the target story map that will be updated.
        
        Args:
            target_map: The StoryMap that will receive updates
        """
        self._target_map = target_map
        self._last_source = None
        self._last_report = None
    
    def generate_report_from(self, source_map: 'StoryMap') -> 'UpdateReport':
        """Generate an update report by comparing source against target.
        
        Stores the source map and report for later use with update_from_report().
        
        Args:
            source_map: The source StoryMap to compare against target
            
        Returns:
            UpdateReport containing the differences
        """
        # story-graph-ops has no DrawIO dependency; report generation lives in drawio-story-sync.
        raise NotImplementedError(
            "generate_report_from is not available in story-graph-ops. "
            "Produce an UpdateReport in drawio-story-sync (or agile_bots synchronizers), "
            "then call update_from_report(report=...)."
        )
    
    def update_from_report(
        self, 
        source: Optional['StoryMap'] = None, 
        report: Optional['UpdateReport'] = None
    ) -> None:
        """Apply changes from an update report to the target map.
        
        If source and report are not provided, uses the stored values from
        the last generate_report_from() call.
        
        Args:
            source: Optional source map (not currently used, for future features)
            report: Optional update report. If None, uses last generated report.
            
        Raises:
            ValueError: If no report is provided and no stored report exists
        """
        # Use stored report if not provided
        if report is None:
            if self._last_report is None:
                raise ValueError(
                    "No report provided and no stored report from generate_report_from()"
                )
            report = self._last_report
        
        # Apply the report using existing logic (extracted from StoryMap)
        self._apply_renames(report)
        self._apply_new_nodes(report)
        self._apply_moves(report)
        self._apply_sub_epic_moves(report)
        self._apply_increment_changes(report)
    
    def _apply_renames(self, report: 'UpdateReport') -> None:
        """Apply rename changes from report."""
        for rename in report.renames:
            node = self._target_map.find_node(rename.original_name)
            if node:
                node.name = rename.extracted_name
    
    def _apply_new_nodes(self, report: 'UpdateReport') -> None:
        """Apply new node creations from report."""
        for new_story in report.new_stories:
            parent = self._target_map.find_node(new_story.parent) if new_story.parent else None
            if parent and hasattr(parent, 'create_story'):
                parent.create_story(name=new_story.name)
        
        for new_se in report.new_sub_epics:
            parent = self._target_map.find_node(new_se.parent) if new_se.parent else None
            if parent and hasattr(parent, 'create_sub_epic'):
                parent.create_sub_epic(name=new_se.name)
    
    def _apply_moves(self, report: 'UpdateReport') -> None:
        """Apply node moves from report."""
        for moved in report.moved_stories:
            story = self._target_map.find_story_by_name(moved.name)
            target = self._target_map.find_node(moved.to_parent) if moved.to_parent else None
            if story and target and hasattr(story, 'move_to'):
                try:
                    story.move_to(target)
                except ValueError as e:
                    # Skip moves that violate hierarchy rules (e.g., moving to non-leaf sub-epic)
                    print(f"Warning: Skipping move of '{moved.name}' to '{moved.to_parent}': {e}")

    def _apply_sub_epic_moves(self, report: 'UpdateReport') -> None:
        """Apply sub-epic moves from report (re-parent sub-epics)."""
        from story_graph_ops.nodes import SubEpic
        for moved in report.moved_sub_epics:
            node = self._target_map.find_node(moved.name)
            to_parent = self._target_map.find_node(moved.to_parent) if moved.to_parent else None
            if not isinstance(node, SubEpic) or not to_parent:
                continue
            if not hasattr(to_parent, '_children') or not hasattr(to_parent, 'create_sub_epic'):
                continue
            old_parent = getattr(node, '_parent', None)
            if not old_parent or old_parent is to_parent:
                continue
            try:
                # Remove from old parent
                if hasattr(old_parent, '_children') and node in old_parent._children:
                    old_parent._children.remove(node)
                # Add to new parent
                to_parent._children.append(node)
                node._parent = to_parent
                if hasattr(node, 'save'):
                    node.save()
            except (ValueError, AttributeError) as e:
                print(f"Warning: Skipping sub-epic move '{moved.name}' to '{moved.to_parent}': {e}")

    def _apply_increment_changes(self, report: 'UpdateReport') -> None:
        """Apply increment changes from report."""
        from story_graph_ops.nodes import IncrementCollection
        
        increments = self._target_map._increments.to_list()
        
        if report.increment_order:
            # Update increment order/priorities and add new increments
            existing_by_name = {inc.get('name', ''): inc for inc in increments}
            new_increments = []
            for inc_order in report.increment_order:
                inc_name = inc_order['name']
                if inc_name in existing_by_name:
                    # Update existing increment priority
                    existing_by_name[inc_name]['priority'] = inc_order['priority']
                    new_increments.append(existing_by_name[inc_name])
                else:
                    # Create new increment
                    new_increments.append({
                        'name': inc_name,
                        'priority': inc_order['priority'],
                        'stories': []
                    })
            increments = new_increments
        
        # Apply increment story assignments
        if report.increment_moves:
            for move in report.increment_moves:
                # Remove from old increment
                if move.from_increment:
                    for inc in increments:
                        if inc.get('name') == move.from_increment:
                            stories = inc.get('stories', [])
                            inc['stories'] = [s for s in stories 
                                            if (s.get('name', '') if isinstance(s, dict) else str(s)) != move.story]
                # Add to new increment
                if move.to_increment:
                    for inc in increments:
                        if inc.get('name') == move.to_increment:
                            stories = inc.get('stories', [])
                            if move.story not in [s.get('name', '') if isinstance(s, dict) else str(s) for s in stories]:
                                stories.append({'name': move.story})
        
        # Remove increments
        if report.removed_increments:
            increments = [
                inc for inc in increments 
                if inc.get('name', '') not in report.removed_increments
            ]
        
        # Update the IncrementCollection with modified increments
        self._target_map._increments = IncrementCollection.from_list(increments, story_map=self._target_map)
        # Keep story_graph dict in sync for serialization and legacy access
        self._target_map.story_graph['increments'] = increments
    
    def reconcile_moves(self, original_map: 'StoryMap') -> None:
        """Reclassify new+removed pairs as moved nodes.
        
        This is a future enhancement mentioned in the plan. For now, it's a stub.
        
        Args:
            original_map: The original map to compare against
        """
        # TODO: Implement move reconciliation logic
        # This would look for nodes marked as both new in one parent and removed
        # from another parent, and reclassify them as moves.
        raise NotImplementedError("Move reconciliation not yet implemented")
    
    def reconcile_ac_moves(self) -> None:
        """Reclassify AC adds+removes as AC moves.
        
        This is a future enhancement mentioned in the plan. For now, it's a stub.
        """
        # TODO: Implement AC move reconciliation logic
        raise NotImplementedError("AC move reconciliation not yet implemented")
