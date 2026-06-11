"""
Navigate From Kanban to Skill Page

Story: User navigates from hub to a skill detail page and back; filter state persists.
Scenarios: skill page pre-selects its family; user can add families; returning hub restores filter.
"""

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
    then_practice_rail_contains_all_families,
    then_family_chip_is_ticked,
    then_board_row_is_visible,
    then_board_row_is_hidden,
    then_crosscut_row_is_visible,
    then_surface_is_idle,
    ALL_PRACTICE_FAMILIES,
    SDD_FAMILY,
    DDD_FAMILY,
)

# ============================================================================
# STORY: Navigate From Kanban to Skill Page
# ============================================================================

class TestNavigateFromKanbanToSkillPage:
    """AC 1–3 from Navigate From Kanban to Skill Page story."""

    def test_skill_page_loads_with_its_family_pre_selected(self, page: Page):
        # Given: user navigates to a skill page (abd-story-mapping → sdd family)
        given_skill_page_loaded(page, "abd-story-mapping.html")
        given_skills_expanded(page)
        # Then: the skill's family (sdd) is pre-selected as the Initial Family
        then_family_chip_is_ticked(page, SDD_FAMILY)
        # And: the board shows only that family's rows
        then_board_row_is_visible(page, SDD_FAMILY)
        for family in ALL_PRACTICE_FAMILIES:
            if family != SDD_FAMILY:
                then_board_row_is_hidden(page, family)
        # And: all Family Header Chips remain visible in the practice rail
        then_practice_rail_contains_all_families(page)

    def test_skill_page_allows_adding_second_family(self, page: Page):
        # Given: skill page loaded with sdd pre-selected
        given_skill_page_loaded(page, "abd-story-mapping.html")
        given_skills_expanded(page)
        # When: user ticks a different Family Header Chip
        when_family_header_chip_clicked(page, DDD_FAMILY)
        # Then: both families' Board Rows become visible
        then_board_row_is_visible(page, SDD_FAMILY)
        then_board_row_is_visible(page, DDD_FAMILY)
        # And: both families' crosscut rows appear in the Supporting Section
        then_crosscut_row_is_visible(page, SDD_FAMILY)
        then_crosscut_row_is_visible(page, DDD_FAMILY)

    def test_navigating_back_to_hub_restores_persisted_filter(self, page: Page):
        # Given: hub loaded; user ticks a family
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        then_family_chip_is_ticked(page, SDD_FAMILY)
        # When: user navigates to a skill page and then back
        skill_url = (Path(__file__).parent.parent.parent.parent / "skill" / "abd-story-mapping.html").as_uri()
        page.click(f"a[href*='abd-story-mapping']") if page.locator("a[href*='abd-story-mapping']").count() > 0 \
            else page.goto(skill_url)
        page.go_back()
        page.wait_for_selector(".foundry-kanban-surface", state="visible")
        # Then: hub restores the Persisted Filter (sdd family still ticked)
        then_family_chip_is_ticked(page, SDD_FAMILY)
