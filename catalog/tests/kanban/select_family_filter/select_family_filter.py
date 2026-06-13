"""
Select Practice Family Filter

Story: User ticks and unticks Family Header Chips to filter the kanban board and supporting section.
Scenarios: tick shows filtered rows; untick restores idle; collapse hides non-ticked; expand shows all headers;
supporting section follows tick state only.
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
    then_practice_rail_contains_all_families,
    then_family_chip_is_ticked,
    then_family_chip_is_unticked,
    then_board_row_is_visible,
    then_board_row_is_hidden,
    then_all_board_rows_are_visible,
    then_skill_tickets_visible_in_row,
    then_skill_tickets_hidden_in_row,
    then_crosscut_row_is_visible,
    then_crosscut_row_is_hidden,
    then_surface_is_idle,
    then_supporting_section_is_visible,
    ALL_PRACTICE_FAMILIES,
    SUPPORTING_CROSSCUT_GROUPS,
    then_filtered_family_tickets_align_across_stage_columns,
    then_filtered_family_tickets_align_with_practice_rail,
    then_practice_rail_shows_only_families,
    then_practice_rail_chip_fits_column,
    then_inactive_family_row_tracks_collapsed,
    SDD_FAMILY,
    DDD_FAMILY,
    UXD_FAMILY,
    ARC_FAMILY,
    KANBAN_FAMILY,
    then_family_chip_shows_tick_indicator,
    then_family_chip_hides_tick_indicator,
)

# ============================================================================
# STORY: Select Practice Family Filter
# ============================================================================

class TestSelectPracticeFamilyFilter:
    """AC 1–6 from Select Practice Family Filter story."""

    def test_clicking_unticked_chip_selects_it_without_hiding_others(self, page: Page):
        # Given: hub loaded, skills expanded
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # When: user clicks an unticked Family Header Chip
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: chip becomes ticked
        then_family_chip_is_ticked(page, SDD_FAMILY)
        # And: all other Family Header Chips remain visible in the practice rail
        then_practice_rail_contains_all_families(page)

    def test_selected_hub_chip_shows_tick_indicator(self, page: Page):
        # Given: hub loaded; skills expanded
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # When: user selects a family chip
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: tick indicator is visible on the selected chip
        then_family_chip_shows_tick_indicator(page, SDD_FAMILY)
        # And: unticked chips do not show a tick
        for family in ALL_PRACTICE_FAMILIES:
            if family != SDD_FAMILY:
                then_family_chip_hides_tick_indicator(page, family)

    def test_deselecting_hub_chip_hides_tick_indicator(self, page: Page):
        # Given: hub loaded; sdd ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        then_family_chip_shows_tick_indicator(page, SDD_FAMILY)
        # When: user clicks the ticked chip again
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: tick indicator disappears
        then_family_chip_hides_tick_indicator(page, SDD_FAMILY)

    def test_clicking_ticked_chip_deselects_and_restores_idle_state(self, page: Page):
        # Given: hub loaded; sdd family ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        then_family_chip_is_ticked(page, SDD_FAMILY)
        # When: user clicks the already ticked chip
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: chip becomes unticked and surface returns to Idle State
        then_family_chip_is_unticked(page, SDD_FAMILY)
        then_surface_is_idle(page)
        # And: all Board Rows reappear
        then_all_board_rows_are_visible(page)

    def test_collapsed_filter_active_shows_only_ticked_family_header_chip(self, page: Page):
        # Given: hub loaded; skills collapsed; sdd ticked
        given_hub_kanban_loaded(page)
        given_skills_collapsed(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: only the ticked family board row chip is visible
        then_board_row_is_visible(page, SDD_FAMILY)
        # And: non-matching board rows are hidden
        for family in ALL_PRACTICE_FAMILIES:
            if family != SDD_FAMILY:
                then_board_row_is_hidden(page, family)
        # And: practice rail hides inactive families and keeps chip inside the column
        then_practice_rail_shows_only_families(page, [SDD_FAMILY])
        then_practice_rail_chip_fits_column(page, SDD_FAMILY)
        then_inactive_family_row_tracks_collapsed(page, [SDD_FAMILY])

    def test_expanded_filter_active_shows_all_headers_but_only_ticked_tickets(self, page: Page):
        # Given: hub loaded; skills expanded; sdd ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: ALL Family Header Chips visible as row headers in the board
        then_practice_rail_contains_all_families(page)
        # And: ticked family shows its skill tickets
        then_skill_tickets_visible_in_row(page, SDD_FAMILY)
        # And: non-matching board rows are hidden (family headers stay in the practice rail)
        for family in ALL_PRACTICE_FAMILIES:
            if family != SDD_FAMILY:
                then_board_row_is_hidden(page, family)

    def test_ticked_family_shows_its_crosscut_row_non_ticked_hidden(self, page: Page):
        # Given: hub loaded; skills expanded; sdd ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: supporting section is visible
        then_supporting_section_is_visible(page)
        # And: ticked family crosscut row is shown auto-expanded
        then_crosscut_row_is_visible(page, SDD_FAMILY)
        # But: crosscut rows for non-ticked families are never shown (except kanban — always supporting)
        for group in SUPPORTING_CROSSCUT_GROUPS:
            if group not in (SDD_FAMILY, KANBAN_FAMILY):
                then_crosscut_row_is_hidden(page, group)
        then_crosscut_row_is_visible(page, KANBAN_FAMILY)

    def test_single_family_filter_aligns_tickets_across_stage_columns(self, page: Page):
        # Given: hub loaded; skills expanded; uxd ticked (AC 4 / observed defect)
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, UXD_FAMILY)
        # Then: UX tickets align horizontally across all stage columns
        then_filtered_family_tickets_align_across_stage_columns(page, UXD_FAMILY)
        # And: tickets stay on the UX practice-rail row (not snapped to story row)
        then_filtered_family_tickets_align_with_practice_rail(page, UXD_FAMILY)

    @pytest.mark.parametrize("family", [DDD_FAMILY, UXD_FAMILY, ARC_FAMILY])
    def test_single_non_sdd_family_stays_on_practice_rail_row(self, page: Page, family: str):
        # Given: hub loaded; skills expanded; one non-SDD family ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, family)
        # Then: tickets align with that family's practice-rail chip, not the top board row
        then_filtered_family_tickets_align_with_practice_rail(page, family)

    def test_ticking_second_family_adds_both_rows(self, page: Page):
        # Given: hub loaded; skills expanded; sdd ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # When: a second family is ticked
        when_family_header_chip_clicked(page, DDD_FAMILY)
        # Then: both families' Board Rows are visible
        then_board_row_is_visible(page, SDD_FAMILY)
        then_board_row_is_visible(page, DDD_FAMILY)
        # And: both families' crosscut rows appear in the Supporting Section
        then_crosscut_row_is_visible(page, SDD_FAMILY)
        then_crosscut_row_is_visible(page, DDD_FAMILY)
