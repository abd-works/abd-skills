"""
View Kanban With No Filter Selected

Story: User opens the hub kanban with no saved filter.
Scenarios: idle state shows all families; collapsed idle shows nothing; expanded shows all chips and tickets.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from playwright.sync_api import Page
from kanban_helper import (
    given_hub_kanban_loaded,
    given_skills_expanded,
    given_skills_collapsed,
    when_family_header_chip_clicked,
    when_skills_toggle_clicked,
    then_practice_rail_contains_all_families,
    then_all_board_rows_are_visible,
    then_board_row_is_hidden,
    then_supporting_section_is_hidden,
    then_surface_is_idle,
    then_family_chip_is_ticked,
    ALL_PRACTICE_FAMILIES,
    SDD_FAMILY,
)

# ============================================================================
# STORY: View Kanban With No Filter Selected
# ============================================================================

class TestViewKanbanWithNoFilterSelected:
    """AC 1–4 from View Kanban With No Filter Selected story."""

    def test_idle_state_shows_all_family_chips_and_board_rows(self, page: Page):
        # Given: hub loads with no saved filter
        given_hub_kanban_loaded(page)
        # Then: all Family Header Chips visible in practice rail
        then_practice_rail_contains_all_families(page)
        # And: surface is in Idle State (no filter active)
        then_surface_is_idle(page)
        # And: all Board Rows visible
        then_all_board_rows_are_visible(page)

    def test_collapsed_idle_state_shows_no_board_rows(self, page: Page):
        # Given: hub loads with no saved filter; skills collapsed (default)
        given_hub_kanban_loaded(page)
        given_skills_collapsed(page)
        # Then: no Board Rows visible in the board area
        for family in ALL_PRACTICE_FAMILIES:
            then_board_row_is_hidden(page, family)

    def test_collapsed_idle_hides_supporting_section(self, page: Page):
        # Given: hub loads; skills collapsed
        given_hub_kanban_loaded(page)
        given_skills_collapsed(page)
        # Then: Supporting Section is not visible
        then_supporting_section_is_hidden(page)

    def test_expanded_shows_all_family_chips_regardless_of_filter(self, page: Page):
        # Given: hub loaded; skills expanded
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # When: a family is ticked
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: ALL Family Header Chips still visible in practice rail
        then_practice_rail_contains_all_families(page)
        # And: the ticked family chip shows selection indicator
        then_family_chip_is_ticked(page, SDD_FAMILY)
