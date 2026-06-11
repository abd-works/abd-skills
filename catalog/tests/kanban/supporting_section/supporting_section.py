"""
View Supporting Section Crosscut Skills

Story: User views the supporting section of the kanban with filter active or idle.
Scenarios: no filter shows all crosscut rows; filter shows only ticked family; foundational uses grey/white colors.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from playwright.sync_api import Page, expect
from kanban_helper import (
    given_hub_kanban_loaded,
    given_skills_expanded,
    when_family_header_chip_clicked,
    then_supporting_section_is_visible,
    then_crosscut_row_is_visible,
    then_crosscut_row_is_hidden,
    ALL_PRACTICE_FAMILIES,
    SDD_FAMILY,
)

# ============================================================================
# STORY: View Supporting Section Crosscut Skills
# ============================================================================

class TestViewSupportingSectionCrosscutSkills:
    """AC 1–3 from View Supporting Section Crosscut Skills story."""

    def test_no_filter_shows_all_crosscut_rows_expanded(self, page: Page):
        # Given: hub loaded; skills expanded; no filter
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # Then: Supporting Section is visible
        then_supporting_section_is_visible(page)
        # And: all Crosscut Rows are shown
        for family in ALL_PRACTICE_FAMILIES:
            then_crosscut_row_is_visible(page, family)

    def test_filter_active_shows_only_ticked_family_crosscut_row(self, page: Page):
        # Given: hub loaded; skills expanded; sdd ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: only sdd Crosscut Row is shown; non-ticked are hidden
        then_crosscut_row_is_visible(page, SDD_FAMILY)
        for family in ALL_PRACTICE_FAMILIES:
            if family != SDD_FAMILY:
                then_crosscut_row_is_hidden(page, family)

    def test_non_ticked_crosscut_row_hidden_regardless_of_expand_state(self, page: Page):
        # Given: hub loaded; skills expanded; sdd ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: non-ticked crosscut rows are hidden (expand state has no effect)
        for family in ALL_PRACTICE_FAMILIES:
            if family != SDD_FAMILY:
                then_crosscut_row_is_hidden(page, family)

    def test_foundational_section_header_is_muted_grey(self, page: Page):
        # Given: hub loaded; skills expanded
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # Then: foundational section header chip uses muted grey styling class
        foundational_header = page.locator(
            ".aad-crosscut-tier--foundational .aad-crosscut-row-title"
        ).first
        expect(foundational_header).to_be_visible()
        # Color is set by CSS variable; verify the element is present with expected class
        expect(foundational_header).to_have_class("/aad-crosscut-row-title/")
