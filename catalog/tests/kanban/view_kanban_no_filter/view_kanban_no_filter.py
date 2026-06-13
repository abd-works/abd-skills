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
    given_skill_page_loaded,
    given_skills_expanded,
    given_skills_collapsed,
    when_family_header_chip_clicked,
    when_skills_toggle_clicked,
    then_practice_rail_contains_all_families,
    then_all_board_rows_are_visible,
    then_board_row_is_hidden,
    then_supporting_section_body_is_hidden,
    then_surface_is_idle,
    then_family_chip_is_ticked,
    then_family_chip_is_unticked,
    then_other_practices_chip_aligns_with_practice_rail,
    then_other_stage_tracks_collapsed,
    then_other_stage_tracks_expanded,
    then_other_stage_skill_hidden,
    then_other_stage_skill_visible,
    when_other_practices_chip_clicked,
    ALL_PRACTICE_FAMILIES,
    SDD_FAMILY,
    OTHER_FAMILY,
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
        # And: all Board Rows visible once skills are expanded (collapsed idle hides rows)
        given_skills_expanded(page)
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
        # Then: supporting crosscut content is not visible
        then_supporting_section_body_is_hidden(page)

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

    def test_other_practices_chip_aligns_with_practice_rail_families(self, page: Page):
        # Given: hub loaded; skills expanded
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # Then: Other Practices chip lines up with the four practice-family chips
        then_other_practices_chip_aligns_with_practice_rail(page)

    def test_other_practices_chip_is_clickable_and_selectable(self, page: Page):
        # Given: hub loaded; skills expanded
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # When: user clicks Other Practices
        when_other_practices_chip_clicked(page)
        # Then: chip becomes ticked
        then_family_chip_is_ticked(page, OTHER_FAMILY)

    def test_other_practices_chip_aligns_when_skills_collapsed(self, page: Page):
        # Given: hub loaded; skills collapsed (default)
        given_hub_kanban_loaded(page)
        given_skills_collapsed(page)
        # Then: Other Practices chip still lines up with practice-family chips
        then_other_practices_chip_aligns_with_practice_rail(page)
        # And: user can click it without overlap from other chips
        when_other_practices_chip_clicked(page)
        then_family_chip_is_ticked(page, OTHER_FAMILY)

    def test_idle_expanded_hides_other_stage_skills_until_other_ticked(self, page: Page):
        # Given: hub loaded; skills expanded; no filter
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # Then: other stage tracks collapsed — no gap above other practices chip
        then_other_stage_tracks_collapsed(page)
        # And: stage-folder skills hidden until other is ticked
        then_other_stage_skill_hidden(page, "abd-cost-of-delay")
        # When: user ticks other practices
        when_other_practices_chip_clicked(page)
        # Then: other tracks open and stage-folder skills appear
        then_other_stage_tracks_expanded(page)
        then_other_stage_skill_visible(page, "abd-cost-of-delay")

    def test_deactivating_other_practices_collapses_extra_board_rows(self, page: Page):
        # Given: hub loaded; skills expanded; other practices active
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_other_practices_chip_clicked(page)
        then_other_stage_tracks_expanded(page)
        # When: user deactivates other practices
        when_other_practices_chip_clicked(page)
        then_family_chip_is_unticked(page, OTHER_FAMILY)
        # Then: idle state collapses other tracks again
        then_other_stage_tracks_collapsed(page)
        then_other_stage_skill_hidden(page, "abd-cost-of-delay")

    def test_practice_family_filter_without_other_collapses_other_rows(self, page: Page):
        # Given: hub loaded; skills expanded; other practices active
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_other_practices_chip_clicked(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # When: user deactivates other practices while sdd remains selected
        when_other_practices_chip_clicked(page)
        then_family_chip_is_unticked(page, OTHER_FAMILY)
        then_family_chip_is_ticked(page, SDD_FAMILY)
        # Then: extra other-practice row tracks collapse
        then_other_stage_tracks_collapsed(page)

    def test_skill_page_other_practices_matches_hub_behavior(self, page: Page):
        # Given: skill page loaded; skills expanded
        given_skill_page_loaded(page, "abd-story-mapping.html")
        given_skills_expanded(page)
        # Then: other tracks collapsed until other is ticked (same as hub)
        then_other_stage_tracks_collapsed(page)
        when_other_practices_chip_clicked(page)
        then_other_stage_tracks_expanded(page)
