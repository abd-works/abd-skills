"""
Collapse and Expand Stage Column

Story: User narrows a stage column to save horizontal space.
Scenarios: collapse button present; clicking narrows column; clicking again restores;
preference persists across reload; collapse is independent of family and stage filters.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from playwright.sync_api import Page
from kanban_helper import (
    given_hub_kanban_loaded,
    given_skills_expanded,
    when_col_collapse_btn_clicked,
    then_col_collapse_btn_visible,
    then_col_is_collapsed,
    then_col_is_expanded,
    then_col_is_narrow,
    then_col_is_full_width,
    when_family_header_chip_clicked,
    when_stage_column_head_clicked,
    then_surface_has_class,
    SDD_FAMILY,
    STAGE_COLUMN_STAGES,
    CONTEXT_STAGE,
    ALL_STAGES,
)

# ============================================================================
# STORY: Collapse and Expand Stage Column
# ============================================================================

class TestCollapseAndExpandStageColumn:
    """AC 1–5 from Collapse and Expand Stage Column story."""

    def test_collapse_button_visible_on_each_stage_column(self, page: Page):
        # Given: hub loaded
        given_hub_kanban_loaded(page)
        # Then: every stage column (including context) has a visible Collapse Button
        for stage in ALL_STAGES:
            then_col_collapse_btn_visible(page, stage)

    def test_clicking_collapse_btn_narrows_column(self, page: Page):
        # Given: hub loaded; shaping column is expanded
        given_hub_kanban_loaded(page)
        then_col_is_expanded(page, "shaping")
        # When: user clicks Collapse Button on the shaping column
        when_col_collapse_btn_clicked(page, "shaping")
        # Then: column is collapsed and visually narrow
        then_col_is_collapsed(page, "shaping")
        then_col_is_narrow(page, "shaping")
        # And: other columns remain expanded
        then_col_is_expanded(page, "discovery")

    def test_clicking_collapse_btn_again_restores_column(self, page: Page):
        # Given: hub loaded; collapse the discovery column
        given_hub_kanban_loaded(page)
        when_col_collapse_btn_clicked(page, "discovery")
        then_col_is_collapsed(page, "discovery")
        # When: user clicks the button again
        when_col_collapse_btn_clicked(page, "discovery")
        # Then: column returns to full width
        then_col_is_expanded(page, "discovery")
        then_col_is_full_width(page, "discovery")

    def test_collapse_btn_aria_label_reflects_state(self, page: Page):
        # Given: hub loaded
        given_hub_kanban_loaded(page)
        btn = page.locator(
            ".foundry-board-grid > .kb-col[data-stage='exploration'] .kb-col-collapse-btn"
        ).first
        # Initially aria-expanded = true
        assert btn.get_attribute("aria-expanded") == "true"
        assert btn.get_attribute("aria-label") == "Collapse column"
        # After collapse
        when_col_collapse_btn_clicked(page, "exploration")
        assert btn.get_attribute("aria-expanded") == "false"
        assert btn.get_attribute("aria-label") == "Expand column"

    def test_collapsed_preference_persists_across_reload(self, page: Page):
        # Given: hub loaded; collapse the specification column
        given_hub_kanban_loaded(page)
        when_col_collapse_btn_clicked(page, "specification")
        then_col_is_collapsed(page, "specification")
        # When: user reloads the page
        page.reload()
        page.wait_for_selector(".foundry-kanban-surface", state="visible")
        page.wait_for_timeout(300)
        # Then: specification column is still collapsed
        then_col_is_collapsed(page, "specification")

    def test_collapse_is_independent_of_family_filter(self, page: Page):
        # Given: hub loaded; skills expanded; SDD family ticked
        given_hub_kanban_loaded(page)
        given_skills_expanded(page)
        when_family_header_chip_clicked(page, SDD_FAMILY)
        # When: user collapses the engineering column
        when_col_collapse_btn_clicked(page, "engineering")
        # Then: engineering column is collapsed
        then_col_is_collapsed(page, "engineering")
        # And: the family filter state is unchanged (SDD still selected)
        surface = page.locator(".foundry-kanban-surface")
        assert surface.evaluate("el => el.classList.contains('foundry-skill-filter-active')"), (
            "Expected family filter to remain active after collapsing a column"
        )

    def test_collapse_is_independent_of_stage_filter(self, page: Page):
        # Given: hub loaded; shaping stage filter toggled on
        given_hub_kanban_loaded(page)
        when_stage_column_head_clicked(page, "shaping")
        # When: user collapses the context column
        when_col_collapse_btn_clicked(page, CONTEXT_STAGE)
        # Then: context column is collapsed
        then_col_is_collapsed(page, CONTEXT_STAGE)
        # And: stage filter state is unchanged (shaping still filtered)
        surface = page.locator(".foundry-kanban-surface")
        assert surface.evaluate("el => el.classList.contains('foundry-stage-filter-active')"), (
            "Expected stage filter to remain active after collapsing a column"
        )

    def test_context_column_can_be_collapsed(self, page: Page):
        # Given: hub loaded
        given_hub_kanban_loaded(page)
        then_col_is_expanded(page, CONTEXT_STAGE)
        # When: user collapses the context column
        when_col_collapse_btn_clicked(page, CONTEXT_STAGE)
        # Then: context column is narrow and collapsed
        then_col_is_collapsed(page, CONTEXT_STAGE)
        then_col_is_narrow(page, CONTEXT_STAGE)
