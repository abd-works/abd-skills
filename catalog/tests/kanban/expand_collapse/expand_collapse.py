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
    given_skills_expanded,
    given_skills_collapsed,
    when_skills_toggle_clicked,
    then_supporting_section_is_visible,
    then_supporting_section_is_hidden,
    then_surface_has_class,
    SDD_FAMILY,
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

    def test_collapsed_state_hides_skill_tickets_and_supporting_section(self, page: Page):
        # Given: hub loaded; expand then collapse
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_skills_toggle_clicked(page)
        # Then: surface enters Collapsed State
        then_surface_has_class(page, "foundry-skills-collapsed")
        # And: Supporting Section is hidden
        then_supporting_section_is_hidden(page)

    def test_skills_expanded_preference_persists_across_reload(self, page: Page):
        # Given: hub loaded; user expands skills
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        # When: user reloads the page
        page.reload()
        page.wait_for_selector(".foundry-kanban-surface", state="visible")
        # Then: surface restores Expanded State from sessionStorage preference
        then_surface_has_class(page, "foundry-skills-expanded")
