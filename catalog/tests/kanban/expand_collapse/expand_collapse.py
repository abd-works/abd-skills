"""
Expand and Collapse Practice Skills

Story: User toggles individual skill visibility on the kanban surface.
Scenarios: toggle switches state; expanded reveals tickets and supporting section;
collapsed hides them; preference restores on reload.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from playwright.sync_api import Page, expect
from kanban_helper import (
    given_hub_kanban_loaded,
    given_skill_page_loaded,
    given_supporting_only_skill_page_loaded,
    given_skills_expanded,
    given_skills_collapsed,
    when_skills_toggle_clicked,
    when_family_header_chip_clicked,
    then_supporting_section_is_visible,
    then_supporting_section_body_is_hidden,
    then_stage_questions_row_is_visible,
    then_stage_questions_row_is_hidden,
    then_surface_has_class,
    then_skill_tickets_visible_in_row,
    then_skill_tickets_hidden_in_row,
    then_board_row_is_hidden,
    then_collapsed_idle_hides_board_skill_tickets,
    then_supporting_crosscut_skills_visible,
    then_practice_rail_chip_fits_column,
    ALL_PRACTICE_FAMILIES,
    SDD_FAMILY,
    DDD_FAMILY,
    KANBAN_SUPPORTING_SKILL_SLUGS,
)

# ============================================================================
# STORY: Expand and Collapse Practice Skills
# ============================================================================

class TestExpandAndCollapsePracticeSkills:
    """AC 1–4 from Expand and Collapse Practice Skills story."""

    def test_toggle_switches_between_expanded_and_collapsed(self, page: Page):
        # Given: hub loaded (starts collapsed by default)
        given_hub_kanban_loaded(page)
        given_skills_collapsed(page)
        # When: user clicks Skills Toggle Button
        when_skills_toggle_clicked(page)
        # Then: surface enters Expanded State
        then_surface_has_class(page, "foundry-skills-expanded")
        # And: toggle aria-expanded reflects the new state
        toggle = page.locator("#foundry-skills-toggle")
        expect(toggle).to_have_attribute("aria-expanded", "true")

    def test_expanded_state_shows_skill_tickets_and_supporting_section(self, page: Page):
        # Given: hub loaded; expand surface
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # Then: Supporting Section becomes visible
        then_supporting_section_is_visible(page)
        # And: Stage Questions Row is visible
        then_stage_questions_row_is_visible(page)

    def test_collapsed_idle_keeps_practice_rail_chips_inside_column(self, page: Page):
        # Given: hub loaded; collapsed idle
        given_hub_kanban_loaded(page)
        given_skills_collapsed(page)
        # Then: family chips stay within the practice column width (no blowout)
        for family in ALL_PRACTICE_FAMILIES:
            then_practice_rail_chip_fits_column(page, family)

    def test_collapsed_state_hides_skill_tickets_and_supporting_section(self, page: Page):
        # Given: hub loaded; expand then collapse
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_skills_toggle_clicked(page)
        # Then: surface enters Collapsed State
        then_surface_has_class(page, "foundry-skills-collapsed")
        # And: supporting crosscut content is hidden (section shell may keep the label)
        then_supporting_section_body_is_hidden(page)
        # And: idle collapse hides board skill tickets completely
        then_collapsed_idle_hides_board_skill_tickets(page)
        # And: Stage Questions Row is hidden
        then_stage_questions_row_is_hidden(page)

    def test_collapsed_filter_hides_stage_questions_row(self, page: Page):
        # Given: hub loaded; expanded then collapsed with a family filter active
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        then_stage_questions_row_is_visible(page)
        when_skills_toggle_clicked(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: Stage Questions Row stays hidden in collapsed focus mode
        then_stage_questions_row_is_hidden(page)
        then_skill_tickets_visible_in_row(page, SDD_FAMILY)

    def test_skills_expanded_preference_persists_across_reload(self, page: Page):
        # Given: hub loaded; user expands skills
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # When: user reloads the page
        page.reload()
        page.wait_for_selector(".foundry-kanban-surface", state="visible")
        # Then: surface restores Expanded State from sessionStorage preference
        then_surface_has_class(page, "foundry-skills-expanded")

    def test_collapsed_filter_shows_only_ticked_family_skills_on_hub(self, page: Page):
        # Given: hub loaded; collapsed; sdd ticked
        given_hub_kanban_loaded(page)
        given_skills_collapsed(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # Then: only sdd skill tickets are visible in stage columns
        then_skill_tickets_visible_in_row(page, SDD_FAMILY)
        for family in ALL_PRACTICE_FAMILIES:
            if family != SDD_FAMILY:
                then_skill_tickets_hidden_in_row(page, family)

    def test_expanded_shows_ticked_family_skills_on_skill_page(self, page: Page):
        # Given: skill page loaded with initial family; skills expanded
        given_skill_page_loaded(page, "abd-story-mapping.html")
        given_skills_expanded(page)
        # Then: pre-selected family skill tickets are visible (not hidden by skill-page-only CSS)
        then_skill_tickets_visible_in_row(page, SDD_FAMILY)

    def test_collapsed_filter_shows_only_ticked_family_skills_on_skill_page(self, page: Page):
        # Given: skill page loaded; collapsed; sdd pre-selected
        given_skill_page_loaded(page, "abd-story-mapping.html")
        given_skills_collapsed(page)
        # Then: sdd tickets visible; other families hidden
        then_skill_tickets_visible_in_row(page, SDD_FAMILY)
        then_skill_tickets_hidden_in_row(page, DDD_FAMILY)

    def test_expand_on_skill_page_does_not_hide_ticked_family_skills(self, page: Page):
        # Given: skill page loaded; collapsed with sdd selected
        given_skill_page_loaded(page, "abd-story-mapping.html")
        given_skills_collapsed(page)
        when_skills_toggle_clicked(page)
        # Then: expanding still shows the ticked family's skill tickets
        then_surface_has_class(page, "foundry-skills-expanded")
        then_skill_tickets_visible_in_row(page, SDD_FAMILY)
        then_board_row_is_hidden(page, DDD_FAMILY)

    def test_supporting_only_page_shows_crosscut_skills_when_session_collapsed(self, page: Page):
        # Given: kanban supporting-only page with collapsed preference in sessionStorage
        given_supporting_only_skill_page_loaded(page, "abd-kanban.html")
        # Then: surface stays expanded and supporting skill chips are visible
        then_surface_has_class(page, "foundry-skills-expanded")
        then_supporting_crosscut_skills_visible(page, KANBAN_SUPPORTING_SKILL_SLUGS[1])
