"""
Select Stage Column Filter

Story: User clicks a Stage Column Head to focus one delivery stage; click again to restore all columns.
Scenarios: single column visible; toggle off; combined with practice family filter.
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
    when_stage_column_head_clicked,
    when_family_header_chip_clicked,
    then_only_stage_column_visible,
    then_all_stage_columns_visible,
    then_stage_column_head_is_current,
    then_stage_column_head_is_filtered,
    then_stage_column_head_is_unfiltered,
    then_stage_questions_cell_is_active,
    then_stage_questions_cell_is_inactive,
    then_stage_columns_with_tickets,
    then_stage_filter_is_idle,
    then_practice_rail_contains_all_families,
    then_board_row_is_visible,
    then_board_row_is_hidden,
    UXD_FAMILY,
    DDD_FAMILY,
    ALL_PRACTICE_FAMILIES,
)

# ============================================================================
# STORY: Select Stage Column Filter
# ============================================================================

class TestSelectStageColumnFilter:
    """AC 1–6 from Select Stage Column Filter story."""

    def test_clicking_stage_column_shows_only_that_column(self, page: Page):
        # Given: hub loaded; skills expanded
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # When: user clicks the Discovery Stage Column Head
        when_stage_column_head_clicked(page, "discovery")
        # Then: only the Discovery Stage Column is visible
        then_only_stage_column_visible(page, "discovery")
        # And: the column head toggles on like a family chip
        then_stage_column_head_is_filtered(page, "discovery")
        then_stage_column_head_is_current(page, "discovery")
        then_stage_questions_cell_is_active(page, "discovery")

    def test_clicking_same_stage_column_restores_all_columns(self, page: Page):
        # Given: hub loaded; discovery stage filtered
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_stage_column_head_clicked(page, "discovery")
        then_only_stage_column_visible(page, "discovery")
        # When: user clicks the same Stage Column Head again
        when_stage_column_head_clicked(page, "discovery")
        # Then: surface returns to Stage Filter Idle State
        then_stage_filter_is_idle(page)
        # And: all Stage Columns are visible again
        then_all_stage_columns_visible(page)
        # And: column head clears selected/current state like an unticked family chip
        then_stage_column_head_is_unfiltered(page, "discovery")
        then_stage_questions_cell_is_inactive(page, "discovery")

    def test_multiple_stage_columns_can_be_filtered_together(self, page: Page):
        # Given: hub loaded; skills expanded
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # When: user toggles discovery and exploration stage columns on
        when_stage_column_head_clicked(page, "discovery")
        when_stage_column_head_clicked(page, "exploration")
        # Then: both columns show tickets; others are empty
        then_stage_columns_with_tickets(page, ["discovery", "exploration"])
        then_stage_column_head_is_filtered(page, "discovery")
        then_stage_column_head_is_filtered(page, "exploration")
        # When: user toggles discovery off
        when_stage_column_head_clicked(page, "discovery")
        # Then: exploration stays filtered; discovery returns to idle
        then_stage_columns_with_tickets(page, ["exploration"])
        then_stage_column_head_is_unfiltered(page, "discovery")
        then_stage_column_head_is_filtered(page, "exploration")

    def test_stage_filter_does_not_hide_practice_rail_families(self, page: Page):
        # Given: hub loaded; exploration stage filtered
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_stage_column_head_clicked(page, "exploration")
        # Then: all Family Header Chips remain visible in the practice rail
        then_practice_rail_contains_all_families(page)

    def test_stage_filter_combined_with_family_filter(self, page: Page):
        # Given: hub loaded; skills expanded; uxd family ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, UXD_FAMILY)
        # When: user filters to specification stage
        when_stage_column_head_clicked(page, "specification")
        # Then: only specification column is visible
        then_only_stage_column_visible(page, "specification")
        # And: only the ticked family row is visible in that column
        then_board_row_is_visible(page, UXD_FAMILY)
        for family in ALL_PRACTICE_FAMILIES:
            if family != UXD_FAMILY:
                then_board_row_is_hidden(page, family)
        # And: family filter remains active (practice rail unchanged)
        then_practice_rail_contains_all_families(page)

    def test_family_filter_persists_when_stage_filter_toggled_off(self, page: Page):
        # Given: hub loaded; ddd family ticked; shaping stage filtered
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, DDD_FAMILY)
        when_stage_column_head_clicked(page, "shaping")
        # When: user clears the stage filter
        when_stage_column_head_clicked(page, "shaping")
        then_stage_filter_is_idle(page)
        then_all_stage_columns_visible(page)
        # Then: family filter is still active
        then_board_row_is_visible(page, DDD_FAMILY)
        for family in ALL_PRACTICE_FAMILIES:
            if family != DDD_FAMILY:
                then_board_row_is_hidden(page, family)

    def test_family_chip_click_does_not_activate_stage_filter(self, page: Page):
        # Given: hub loaded; skills expanded
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # When: user ticks a practice family
        when_family_header_chip_clicked(page, UXD_FAMILY)
        # Then: stage filter stays idle and filtered family rows appear in multiple columns
        then_stage_filter_is_idle(page)
        then_all_stage_columns_visible(page)
        then_board_row_is_visible(page, UXD_FAMILY)

    def test_skill_page_initial_stage_highlights_without_column_filter(self, page: Page):
        # Given: skill page loads with data-initial-stage (story mapping outline → shaping)
        given_skill_page_loaded(page, "abd-story-mapping.html")
        given_skills_expanded(page)
        # Then: stage filter is idle — all columns remain populated
        then_stage_filter_is_idle(page)
        then_all_stage_columns_visible(page)
        then_stage_column_head_is_current(page, "shaping")
