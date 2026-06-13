"""
Catalog top navigation — single forge link back to catalog hub.

Story: User sees one Foundry nav item (Forge) instead of Complete/Skills/Agents/etc.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

CATALOG_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
HUB_URL = CATALOG_ROOT / "index.html"
SKILL_URL = CATALOG_ROOT / "skill" / "abd-story-mapping.html"

REMOVED_LABELS = ("Complete", "Skills", "Agents", "Instructions", "Delivery kanban")
FOUNDRY_LINK = ".nav-links .nav-links__foundry"


def given_catalog_page_loaded(page: Page, url: Path) -> None:
    page.goto(url.as_uri())
    page.wait_for_selector(".site-nav", state="visible")
    page.wait_for_selector(FOUNDRY_LINK, state="visible")


class TestForgeCatalogNavigation:
    """AC from Return to Catalog Hub via Forge Nav story."""

    def test_hub_shows_only_forge_foundry_link(self, page: Page):
        given_catalog_page_loaded(page, HUB_URL)
        expect(page.locator(FOUNDRY_LINK)).to_have_count(1)
        expect(page.locator(FOUNDRY_LINK)).to_have_text("forge")
        for label in REMOVED_LABELS:
            expect(page.locator(".nav-links").get_by_role("link", name=label)).to_have_count(0)

    def test_hub_marks_forge_as_current_page(self, page: Page):
        given_catalog_page_loaded(page, HUB_URL)
        expect(page.locator(FOUNDRY_LINK)).to_have_attribute("aria-current", "page")

    def test_skill_page_shows_only_forge_foundry_link(self, page: Page):
        given_catalog_page_loaded(page, SKILL_URL)
        expect(page.locator(FOUNDRY_LINK)).to_have_count(1)
        expect(page.locator(FOUNDRY_LINK)).to_have_text("forge")
        for label in REMOVED_LABELS:
            expect(page.locator(".nav-links").get_by_role("link", name=label)).to_have_count(0)

    def test_skill_page_forge_links_to_catalog_hub(self, page: Page):
        given_catalog_page_loaded(page, SKILL_URL)
        href = page.locator(FOUNDRY_LINK).get_attribute("href") or ""
        assert href.endswith("index.html")
        page.click(FOUNDRY_LINK)
        page.wait_for_selector(".foundry-kanban-surface", state="visible")
        assert page.url.endswith("/index.html") or page.url.endswith("/index.html/")

    def test_skill_page_forge_is_not_current(self, page: Page):
        given_catalog_page_loaded(page, SKILL_URL)
        expect(page.locator(FOUNDRY_LINK)).not_to_have_attribute("aria-current", "page")
