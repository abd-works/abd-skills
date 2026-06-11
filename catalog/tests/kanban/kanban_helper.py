"""
Kanban Test Helpers

Shared Given/When/Then helpers for kanban acceptance tests.
All helpers operate on a Playwright Page that has already loaded a kanban surface.
"""

from pathlib import Path
from playwright.sync_api import Page, expect

CATALOG_ROOT = Path(__file__).parent.parent.parent.resolve()
HUB_URL = CATALOG_ROOT / "index.html"
SKILL_PAGE_URL = CATALOG_ROOT / "skill" / "abd-story-mapping.html"

SDD_FAMILY = "story-driven-delivery"
DDD_FAMILY = "domain-driven-design"
UXD_FAMILY = "user-experience-design"
ARC_FAMILY = "architecture-centric-engineering"
ALL_PRACTICE_FAMILIES = [SDD_FAMILY, DDD_FAMILY, UXD_FAMILY, ARC_FAMILY]

# ============================================================================
# SETUP HELPERS
# ============================================================================

def given_hub_kanban_loaded(page: Page) -> None:
    """Navigate to the hub with a clean session — no saved filter or preference."""
    page.goto(HUB_URL.as_uri())
    page.evaluate("() => sessionStorage.clear()")
    page.reload()
    page.wait_for_selector(".foundry-kanban-surface", state="visible")
    page.wait_for_selector(".foundry-family-toggle", state="visible")

def given_skill_page_loaded(page: Page, skill_html: str = "abd-story-mapping.html") -> None:
    """Navigate to a skill detail page."""
    url = (CATALOG_ROOT / "skill" / skill_html).as_uri()
    page.goto(url)
    page.wait_for_selector(".foundry-kanban-surface--skill-page", state="visible")
    page.wait_for_selector(".foundry-family-toggle", state="visible")

def given_skills_expanded(page: Page) -> None:
    """Ensure the kanban is in Expanded State — click toggle if needed.
    Waits for the CSS grid-template-rows transition to complete.
    """
    surface = page.locator(".foundry-kanban-surface")
    if surface.evaluate("el => el.classList.contains('foundry-skills-collapsed')"):
        page.locator("#foundry-skills-toggle").click()
        page.wait_for_selector(".foundry-kanban-surface.foundry-skills-expanded", timeout=3000)
        page.wait_for_timeout(500)

def given_skills_collapsed(page: Page) -> None:
    """Ensure the kanban is in Collapsed State."""
    surface = page.locator(".foundry-kanban-surface")
    if surface.evaluate("el => el.classList.contains('foundry-skills-expanded')"):
        page.locator("#foundry-skills-toggle").click()
        surface.wait_for(has_class="foundry-skills-collapsed", timeout=2000)

# ============================================================================
# ACTION HELPERS
# ============================================================================

def when_family_header_chip_clicked(page: Page, family: str) -> None:
    """Click the Family Header Chip for the given family slug in the practice rail."""
    page.locator(f".foundry-family-toggle[data-family='{family}']").first.click()
    page.wait_for_timeout(150)

def when_skills_toggle_clicked(page: Page) -> None:
    """Click the Skills Toggle Button (+/-)."""
    page.locator("#foundry-skills-toggle").click()
    page.wait_for_timeout(150)

# ============================================================================
# ASSERTION HELPERS
# ============================================================================

def then_practice_rail_contains_all_families(page: Page) -> None:
    """All Family Header Chips are visible in the practice rail."""
    for family in ALL_PRACTICE_FAMILIES:
        chip = page.locator(f".foundry-family-toggle[data-family='{family}']").first
        expect(chip).to_be_visible()

def then_family_chip_is_ticked(page: Page, family: str) -> None:
    """The given Family Header Chip has aria-pressed=true (is selected)."""
    chip = page.locator(f".foundry-family-toggle[data-family='{family}']").first
    expect(chip).to_have_attribute("aria-pressed", "true")

def then_family_chip_is_unticked(page: Page, family: str) -> None:
    """The given Family Header Chip has aria-pressed=false."""
    chip = page.locator(f".foundry-family-toggle[data-family='{family}']").first
    expect(chip).to_have_attribute("aria-pressed", "false")

def then_board_row_is_visible(page: Page, family: str) -> None:
    """The Board Row for this family renders with non-zero height (grid row is open)."""
    row = page.locator(f".foundry-board-grid .aad-skill-row[data-family='{family}']").first
    box = row.bounding_box()
    assert box is not None and box["height"] > 0, (
        f"Expected board row for '{family}' to be visible (height > 0), got: {box}"
    )

def then_board_row_is_hidden(page: Page, family: str) -> None:
    """The Board Row for this family is clipped to zero height (grid-template-rows: 0px)."""
    row = page.locator(f".foundry-board-grid .aad-skill-row[data-family='{family}']").first
    box = row.bounding_box()
    assert box is None or box["height"] == 0, (
        f"Expected board row for '{family}' to be hidden (height == 0), got: {box}"
    )

def then_all_board_rows_are_visible(page: Page) -> None:
    for family in ALL_PRACTICE_FAMILIES:
        then_board_row_is_visible(page, family)

def then_skill_tickets_visible_in_row(page: Page, family: str) -> None:
    """At least one individual skill ticket in this family's row has non-zero height."""
    ticket = page.locator(
        f".foundry-board-grid .aad-skill-row[data-family='{family}'] .kb-ticket:not(.foundry-practice-col__card)"
    ).first
    box = ticket.bounding_box()
    assert box is not None and box["height"] > 0, (
        f"Expected skill tickets in '{family}' row to be visible, got: {box}"
    )

def then_skill_tickets_hidden_in_row(page: Page, family: str) -> None:
    """All individual skill ticket chips in this family's row have zero height (grid-clipped)."""
    row = page.locator(f".foundry-board-grid .aad-skill-row[data-family='{family}']").first
    tickets = row.locator(".kb-ticket:not(.foundry-practice-col__card)")
    count = tickets.count()
    for i in range(min(count, 3)):
        box = tickets.nth(i).bounding_box()
        assert box is None or box["height"] == 0, (
            f"Expected skill ticket {i} in '{family}' row to be hidden, got: {box}"
        )

def then_supporting_section_is_visible(page: Page) -> None:
    """The foundry-skills-extra wrapper has non-zero height (expanded)."""
    extra = page.locator(".foundry-skills-extra").first
    box = extra.bounding_box()
    assert box is not None and box["height"] > 0, (
        f"Expected supporting section to be visible (height > 0), got: {box}"
    )

def then_supporting_section_is_hidden(page: Page) -> None:
    """The foundry-skills-extra wrapper is clipped to zero height (collapsed)."""
    extra = page.locator(".foundry-skills-extra").first
    box = extra.bounding_box()
    assert box is None or box["height"] == 0, (
        f"Expected supporting section to be hidden (height == 0), got: {box}"
    )

def then_crosscut_row_is_visible(page: Page, family: str) -> None:
    """The Crosscut Row for this family is present and visible in the Supporting Section."""
    row = page.locator(f".aad-delivery-crosscut-row[data-crosscut-group='{family}']").first
    expect(row).to_be_visible()

def then_crosscut_row_is_hidden(page: Page, family: str) -> None:
    """The Crosscut Row for this family is hidden (display:none via is-filter-visible logic)."""
    row = page.locator(f".aad-delivery-crosscut-row[data-crosscut-group='{family}']").first
    expect(row).to_be_hidden()

def then_surface_has_class(page: Page, css_class: str) -> None:
    surface = page.locator(".foundry-kanban-surface")
    assert surface.evaluate(f"el => el.classList.contains('{css_class}')"), (
        f"Expected kanban surface to have class '{css_class}'"
    )

def then_surface_is_idle(page: Page) -> None:
    """No filter is active on the kanban surface."""
    surface = page.locator(".foundry-kanban-surface")
    assert not surface.evaluate("el => el.classList.contains('foundry-skill-filter-active')"), (
        "Expected kanban surface to be in Idle State (no foundry-skill-filter-active class)"
    )

