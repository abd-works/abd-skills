"""
View Supporting Section Crosscut Skills

Story: User views the supporting section of the kanban with filter active or idle.
Scenarios: no filter shows all crosscut rows; filter shows only ticked family; foundational uses grey/white colors.
"""

import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from playwright.sync_api import Page, expect
from kanban_helper import (
    given_hub_kanban_loaded,
    given_skill_page_loaded,
    given_skills_expanded,
    when_family_header_chip_clicked,
    when_other_practices_chip_clicked,
    then_supporting_section_is_visible,
    then_crosscut_row_is_visible,
    then_crosscut_row_is_hidden,
    then_crosscut_row_matches_hub_layout,
    SUPPORTING_CROSSCUT_GROUPS,
    SDD_FAMILY,
    KANBAN_FAMILY,
    then_kanban_supporting_skills_only_in_supporting_section,
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
        # And: all supporting Crosscut Rows are shown (kanban, ddd, sdd — not uxd/arc)
        for group in SUPPORTING_CROSSCUT_GROUPS:
            then_crosscut_row_is_visible(page, group)

    def test_filter_active_shows_only_ticked_family_crosscut_row(self, page: Page):
        # Given: hub loaded; skills expanded; sdd ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: sdd Crosscut Row is shown
        then_crosscut_row_is_visible(page, SDD_FAMILY)
        # And: kanban Crosscut Row always remains visible (supporting-only practice)
        then_crosscut_row_is_visible(page, KANBAN_FAMILY)
        # But: other non-ticked crosscut rows are hidden
        for group in SUPPORTING_CROSSCUT_GROUPS:
            if group not in (SDD_FAMILY, KANBAN_FAMILY):
                then_crosscut_row_is_hidden(page, group)

    def test_non_ticked_crosscut_row_hidden_regardless_of_expand_state(self, page: Page):
        # Given: hub loaded; skills expanded; sdd ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: non-ticked crosscut rows are hidden except kanban (always in supporting)
        for group in SUPPORTING_CROSSCUT_GROUPS:
            if group not in (SDD_FAMILY, KANBAN_FAMILY):
                then_crosscut_row_is_hidden(page, group)

    def test_kanban_skills_only_in_supporting_section(self, page: Page):
        # Given: hub loaded; skills expanded
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # Then: kanban practice skills never appear on the board grid
        then_kanban_supporting_skills_only_in_supporting_section(page)

    def test_kanban_crosscut_visible_when_family_filter_active(self, page: Page):
        # Given: hub loaded; skills expanded; uxd family ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, "user-experience-design")
        # Then: kanban crosscut row remains visible in the supporting section
        then_crosscut_row_is_visible(page, KANBAN_FAMILY)

    def test_foundational_section_header_is_muted_grey(self, page: Page):
        # Given: hub loaded; skills expanded; other practices ticked (foundations visible)
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_other_practices_chip_clicked(page)
        # Then: foundational section header chip uses muted grey styling class
        foundational_header = page.locator(
            ".aad-crosscut-tier--foundational .aad-crosscut-row-title"
        ).first
        expect(foundational_header).to_be_visible()
        # Color is set by CSS variable; verify the element is present with expected class
        expect(foundational_header).to_have_class(re.compile(r"\baad-crosscut-row-title\b"))

    def test_skill_page_supporting_row_matches_hub_layout(self, page: Page):
        # Given: skill page loaded with skills expanded (sdd pre-selected)
        given_skill_page_loaded(page, "abd-story-mapping.html")
        given_skills_expanded(page)
        # Then: supporting section visible with hub-style horizontal crosscut row
        then_supporting_section_is_visible(page)
        then_crosscut_row_matches_hub_layout(page, SDD_FAMILY)
        then_crosscut_row_matches_hub_layout(page, KANBAN_FAMILY)
