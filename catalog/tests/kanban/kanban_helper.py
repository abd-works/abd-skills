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
OTHER_FAMILY = "other"
KANBAN_FAMILY = "kanban"
ALL_PRACTICE_FAMILIES = [SDD_FAMILY, DDD_FAMILY, UXD_FAMILY, ARC_FAMILY]
SUPPORTING_CROSSCUT_GROUPS = [KANBAN_FAMILY, DDD_FAMILY, SDD_FAMILY]
KANBAN_SUPPORTING_SKILL_SLUGS = [
    "abd-kanban",
    "abd-kanban-planning",
    "abd-kanban-repo",
    "kanban-estimation",
    "abd-kanban-handoff",
]

_ROW_VISIBILITY_JS = """el => {
  const style = window.getComputedStyle(el);
  if (style.display === 'none' || style.visibility === 'hidden') return false;
  if (parseFloat(style.opacity) < 0.05) return false;
  const rect = el.getBoundingClientRect();
  return rect.width > 0 && rect.height > 0;
}"""

_INNER_HIDDEN_JS = """el => {
  const style = window.getComputedStyle(el);
  if (style.display === 'none' || style.visibility === 'hidden') return true;
  return parseFloat(style.opacity) < 0.05;
}"""

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
    page.wait_for_selector(".foundry-kanban-surface", state="visible")
    if page.locator(".foundry-family-toggle").count():
        page.wait_for_selector(".foundry-family-toggle", state="visible")

def given_supporting_only_skill_page_loaded(page: Page, skill_html: str = "abd-kanban.html") -> None:
    """Navigate to a supporting-section-only kanban practice skill page."""
    url = (CATALOG_ROOT / "skill" / skill_html).as_uri()
    page.goto(url)
    page.evaluate("() => sessionStorage.setItem('abd-foundry-skill-page-skills-expanded', '0')")
    page.reload()
    page.wait_for_selector(".foundry-kanban-surface--supporting-only", state="visible")

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
        page.wait_for_timeout(300)

# ============================================================================
# ACTION HELPERS
# ============================================================================

def when_family_header_chip_clicked(page: Page, family: str) -> None:
    """Click the Family Header Chip for the given family slug in the practice rail."""
    chip = page.locator(f".foundry-practice-col .foundry-family-toggle[data-family='{family}']").first
    chip.click()
    page.wait_for_timeout(200)

def when_other_practices_chip_clicked(page: Page) -> None:
    """Click the Other Practices chip at the bottom of the practice rail."""
    when_family_header_chip_clicked(page, OTHER_FAMILY)

def given_kanban_at_viewport_offset(page: Page, target_top: float = 80.0) -> None:
    """Scroll until the kanban surface sits at a stable offset from the viewport top."""
    page.evaluate(
        """(targetTop) => {
          const s = document.querySelector('.foundry-kanban-surface');
          if (!s) return;
          window.scrollBy(0, s.getBoundingClientRect().top - targetTop);
        }""",
        target_top,
    )
    page.wait_for_timeout(200)

def kanban_viewport_top(page: Page) -> float:
    """Distance from viewport top to the kanban surface top edge."""
    top = page.evaluate(
        """() => {
          const s = document.querySelector('.foundry-kanban-surface');
          return s ? s.getBoundingClientRect().top : null;
        }"""
    )
    assert top is not None, "Expected kanban surface on page"
    return float(top)

def then_kanban_viewport_top_near(page: Page, expected_top: float, tolerance: float = 12.0) -> None:
    """Kanban surface stays at roughly the same viewport offset after navigation."""
    page.wait_for_function(
        """(args) => {
          const s = document.querySelector('.foundry-kanban-surface');
          if (!s) return false;
          const top = s.getBoundingClientRect().top;
          return Math.abs(top - args.expected) <= args.tolerance;
        }""",
        arg={"expected": expected_top, "tolerance": tolerance},
        timeout=8000,
    )

def then_page_scroll_y_near(page: Page, expected_y: float, tolerance: float = 20.0) -> None:
    """Window scroll position is preserved across skill navigation."""
    page.wait_for_function(
        """(args) => Math.abs(window.scrollY - args.expected) <= args.tolerance""",
        arg={"expected": expected_y, "tolerance": tolerance},
        timeout=8000,
    )
    assert page.evaluate("window.scrollY") > 50, "Expected page not jumped back to top"

def when_skill_ticket_clicked(page: Page, skill_slug: str) -> None:
    """Click a skill ticket link on the kanban board (not a family chip)."""
    link = page.locator(
        f".foundry-kanban-surface a.kb-ticket.aad-skill[href*='{skill_slug}']:not(.foundry-family-toggle)"
    ).first
    link.click()
    page.wait_for_load_state("load")
    page.wait_for_selector(".foundry-kanban-surface", state="visible")
    page.wait_for_timeout(500)

def when_skills_toggle_clicked(page: Page) -> None:
    """Click the Skills Toggle Button (+/-)."""
    page.locator("#foundry-skills-toggle").click()
    page.wait_for_timeout(500)

def when_stage_column_head_clicked(page: Page, stage: str) -> None:
    """Click the Stage Column Head for the given stage slug."""
    head = page.locator(
        f".foundry-board-grid .kb-col[data-stage='{stage}'] .kb-col-head[data-stage='{stage}']"
    ).first
    head.click()
    page.wait_for_timeout(200)

# ============================================================================
# ASSERTION HELPERS
# ============================================================================

def then_practice_rail_contains_all_families(page: Page) -> None:
    """All Family Header Chips are visible in the practice rail."""
    for family in ALL_PRACTICE_FAMILIES:
        chip = page.locator(f".foundry-practice-col .foundry-family-toggle[data-family='{family}']").first
        expect(chip).to_be_visible()

def then_practice_rail_shows_only_families(page: Page, families: list[str]) -> None:
    """Only the listed families are visible in the practice rail."""
    visible = set(families)
    for family in ALL_PRACTICE_FAMILIES:
        chip = page.locator(f".foundry-practice-col .foundry-family-toggle[data-family='{family}']").first
        if family in visible:
            expect(chip).to_be_visible()
        else:
            expect(chip).to_be_hidden()

def then_practice_rail_chip_fits_column(page: Page, family: str) -> None:
    """A practice-rail chip does not overflow the practice column width."""
    col = page.locator(".foundry-practice-col").first
    chip = page.locator(f".foundry-practice-col .foundry-family-toggle[data-family='{family}']").first
    col_box = col.bounding_box()
    chip_box = chip.bounding_box()
    assert col_box is not None and chip_box is not None
    assert chip_box["width"] <= col_box["width"] + 1, (
        f"Expected '{family}' chip width <= practice column "
        f"({chip_box['width']:.1f}px vs {col_box['width']:.1f}px)"
    )

def then_inactive_family_row_tracks_collapsed(page: Page, active_families: list[str]) -> None:
    """Collapsed filter mode zeroes grid tracks for unticked practice families."""
    rows = _board_grid_row_track_heights(page)
    assert len(rows) >= 5, f"Expected family row tracks, got {rows}"
    family_rows = {
        SDD_FAMILY: rows[1],
        DDD_FAMILY: rows[2],
        UXD_FAMILY: rows[3],
        ARC_FAMILY: rows[4],
    }
    active = set(active_families)
    for family, height in family_rows.items():
        if family in active:
            assert height >= 30, f"Expected active family '{family}' row open, got {height}px"
        else:
            assert height <= 2, f"Expected inactive family '{family}' row collapsed, got {height}px"

def then_family_chip_is_ticked(page: Page, family: str) -> None:
    """The given Family Header Chip has aria-pressed=true (is selected)."""
    chip = page.locator(f".foundry-practice-col .foundry-family-toggle[data-family='{family}']").first
    expect(chip).to_have_attribute("aria-pressed", "true")

def then_family_chip_is_unticked(page: Page, family: str) -> None:
    """The given Family Header Chip has aria-pressed=false."""
    chip = page.locator(f".foundry-practice-col .foundry-family-toggle[data-family='{family}']").first
    expect(chip).to_have_attribute("aria-pressed", "false")

def then_family_chip_shows_tick_indicator(page: Page, family: str) -> None:
    """The selected Family Header Chip renders a visible tick (::after pseudo-element has opacity 1)."""
    chip = page.locator(f".foundry-practice-col .foundry-family-toggle[data-family='{family}']").first
    opacity = chip.evaluate(
        "el => parseFloat(window.getComputedStyle(el, '::after').opacity)"
    )
    assert opacity > 0.5, (
        f"Expected tick indicator visible on '{family}' chip (::after opacity > 0.5), got {opacity}"
    )

def then_family_chip_hides_tick_indicator(page: Page, family: str) -> None:
    """The unticked Family Header Chip has no visible tick (::after pseudo-element has opacity 0)."""
    chip = page.locator(f".foundry-practice-col .foundry-family-toggle[data-family='{family}']").first
    opacity = chip.evaluate(
        "el => parseFloat(window.getComputedStyle(el, '::after').opacity)"
    )
    assert opacity < 0.05, (
        f"Expected tick indicator hidden on '{family}' chip (::after opacity < 0.05), got {opacity}"
    )

def _board_row_any_visible(page: Page, family: str) -> bool:
    return page.evaluate(
        """family => {
          const rows = document.querySelectorAll(
            `.foundry-board-grid .kb-col > .aad-skill-row[data-family="${family}"]`
          );
          for (const el of rows) {
            const style = window.getComputedStyle(el);
            if (style.display === 'none' || style.visibility === 'hidden') continue;
            if (parseFloat(style.opacity) < 0.05) continue;
            const col = el.closest('.kb-col');
            if (col && window.getComputedStyle(col).display === 'none') continue;
            const rect = el.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) return true;
          }
          return false;
        }""",
        family,
    )

def then_board_row_is_visible(page: Page, family: str) -> None:
    """The Board Row for this family is visually shown in at least one stage column."""
    assert _board_row_any_visible(page, family), f"Expected board row for '{family}' to be visible"

def then_board_row_is_hidden(page: Page, family: str) -> None:
    """The Board Row for this family is hidden in every stage column."""
    assert not _board_row_any_visible(page, family), f"Expected board row for '{family}' to be hidden"

def then_all_board_rows_are_visible(page: Page) -> None:
    for family in ALL_PRACTICE_FAMILIES:
        then_board_row_is_visible(page, family)

def then_skill_tickets_visible_in_row(page: Page, family: str) -> None:
    """At least one individual skill ticket in this family's row is visible."""
    ticket = page.locator(
        f".foundry-board-grid .kb-col > .aad-skill-row[data-family='{family}'] .kb-ticket:not(.foundry-practice-col__card)"
    ).first
    expect(ticket).to_be_visible()

def then_skill_tickets_hidden_in_row(page: Page, family: str) -> None:
    """Individual skill ticket chips in this family's row are not visible."""
    row = page.locator(f".foundry-board-grid .kb-col > .aad-skill-row[data-family='{family}']").first
    tickets = row.locator(".kb-ticket:not(.foundry-practice-col__card)")
    count = tickets.count()
    for i in range(min(count, 3)):
        expect(tickets.nth(i)).to_be_hidden()

def then_collapsed_idle_hides_board_skill_tickets(page: Page) -> None:
    """Collapsed idle state hides every stage-column skill ticket."""
    hidden = page.evaluate("""() => {
      const tickets = document.querySelectorAll(
        '.foundry-board-grid .kb-col > .aad-skill-row .kb-ticket'
      );
      if (!tickets.length) return false;
      for (const ticket of tickets) {
        const row = ticket.closest('.aad-skill-row');
        if (!row) continue;
        const rowStyle = window.getComputedStyle(row);
        if (rowStyle.display === 'none' || rowStyle.visibility === 'hidden') continue;
        if (parseFloat(rowStyle.opacity) < 0.05) continue;
        const rect = ticket.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) return false;
      }
      return true;
    }""")
    assert hidden, "Expected no visible board skill tickets when collapsed idle"

def then_supporting_crosscut_skills_visible(page: Page, skill_slug: str) -> None:
    """A supporting crosscut skill chip is visible (supporting-only pages)."""
    ticket = page.locator(
        f".aad-delivery-crosscut-skills .kb-ticket[href*='{skill_slug}']"
    ).first
    expect(ticket).to_be_visible()

def then_stage_questions_row_is_visible(page: Page) -> None:
    """Stage perspective questions row is visible under the board grid."""
    row = page.locator(".foundry-kanban-surface .kanban-stage-questions").first
    expect(row).to_be_visible()

def then_stage_questions_row_is_hidden(page: Page) -> None:
    """Stage perspective questions row is hidden when skills are collapsed."""
    row = page.locator(".foundry-kanban-surface .kanban-stage-questions").first
    expect(row).to_be_hidden()

def then_supporting_section_is_visible(page: Page) -> None:
    """Supporting crosscut content is visible when skills are expanded."""
    section = page.locator(".aad-delivery-crosscut-section--supporting").first
    expect(section).to_be_visible()
    inner = page.locator(".foundry-skills-extra__inner").first
    hidden = inner.evaluate(_INNER_HIDDEN_JS)
    assert not hidden, "Expected supporting section body to be visible"

def then_supporting_section_body_is_hidden(page: Page) -> None:
    """Supporting crosscut content is hidden; the section shell may still reserve space."""
    page.wait_for_function(
        """() => {
          const section = document.querySelector('.aad-delivery-crosscut-section--supporting');
          if (section && section.hidden) return true;
          const inner = document.querySelector('.foundry-skills-extra__inner');
          if (!inner) return true;
          const style = window.getComputedStyle(inner);
          return parseFloat(style.opacity) < 0.05 || style.visibility === 'hidden';
        }""",
        timeout=3000,
    )

def then_supporting_section_is_hidden(page: Page) -> None:
    """Alias for collapsed supporting content checks."""
    then_supporting_section_body_is_hidden(page)

def then_crosscut_row_is_visible(page: Page, group: str) -> None:
    """The Crosscut Row for this group is present and visible in the Supporting Section."""
    row = page.locator(f".aad-delivery-crosscut-row[data-crosscut-group='{group}']").first
    expect(row).to_be_visible()

def then_crosscut_row_is_hidden(page: Page, group: str) -> None:
    """The Crosscut Row for this group is hidden (filter or collapse logic)."""
    row = page.locator(f".aad-delivery-crosscut-row[data-crosscut-group='{group}']").first
    expect(row).to_be_hidden()

def then_crosscut_row_matches_hub_layout(page: Page, group: str) -> None:
    """Crosscut row uses hub layout: anchor header + inline visible skill chips in a horizontal row."""
    row = page.locator(f".aad-delivery-crosscut-row[data-crosscut-group='{group}']").first
    expect(row).to_be_visible()
    expect(row.locator("button.aad-crosscut-row-toggle")).to_have_count(0)
    expect(row.locator("a.aad-crosscut-row-title")).to_have_count(1)
    flex_dir = row.evaluate("el => window.getComputedStyle(el).flexDirection")
    assert flex_dir == "row", f"Expected crosscut row flex-direction row, got {flex_dir}"
    skills = row.locator(".aad-delivery-crosscut-skills").first
    expect(skills).to_be_visible()
    skills_flex = skills.evaluate("el => window.getComputedStyle(el).flexDirection")
    assert skills_flex in ("row", "row-reverse"), (
        f"Expected crosscut skills inline (row), got {skills_flex}"
    )
    expect(skills.locator(".kb-ticket.aad-skill").first).to_be_visible()

def then_surface_has_class(page: Page, css_class: str) -> None:
    surface = page.locator(".foundry-kanban-surface")
    assert surface.evaluate(f"el => el.classList.contains('{css_class}')"), (
        f"Expected kanban surface to have class '{css_class}'"
    )

STAGE_COLUMN_STAGES = ["shaping", "discovery", "exploration", "specification", "engineering"]

def then_filtered_family_tickets_align_across_stage_columns(page: Page, family: str) -> None:
    """Visible skill tickets for a filtered family share one horizontal band across stage columns."""
    ys: list[float] = []
    for stage in STAGE_COLUMN_STAGES:
        ticket = page.locator(
            f".kb-col[data-stage='{stage}'] .aad-skill-row[data-family='{family}'] .kb-ticket"
        ).first
        if not ticket.count():
            continue
        if not ticket.evaluate(_ROW_VISIBILITY_JS):
            continue
        box = ticket.bounding_box()
        assert box is not None, f"Expected visible ticket in stage '{stage}'"
        ys.append(box["y"])
    assert len(ys) >= 2, f"Expected at least two visible tickets for '{family}', got {len(ys)}"
    spread = max(ys) - min(ys)
    assert spread <= 2, f"Expected stage columns aligned (spread <= 2px), got {spread:.1f}px: {ys}"

def then_filtered_family_tickets_align_with_practice_rail(page: Page, family: str) -> None:
    """Filtered family tickets share the same horizontal band as the practice-rail chip."""
    chip = page.locator(
        f".foundry-practice-col .foundry-family-toggle[data-family='{family}']"
    ).first
    chip_box = chip.bounding_box()
    assert chip_box is not None, f"Expected practice-rail chip for '{family}'"
    chip_center_y = chip_box["y"] + chip_box["height"] / 2
    matched = 0
    for stage in STAGE_COLUMN_STAGES:
        ticket = page.locator(
            f".kb-col[data-stage='{stage}'] .aad-skill-row[data-family='{family}'] .kb-ticket"
        ).first
        if not ticket.count() or not ticket.evaluate(_ROW_VISIBILITY_JS):
            continue
        ticket_box = ticket.bounding_box()
        assert ticket_box is not None, f"Expected visible ticket in '{stage}' for '{family}'"
        ticket_center_y = ticket_box["y"] + ticket_box["height"] / 2
        assert abs(ticket_center_y - chip_center_y) <= 4, (
            f"Expected '{family}' ticket in '{stage}' aligned with practice rail "
            f"(chip_y={chip_center_y:.1f}, ticket_y={ticket_center_y:.1f})"
        )
        matched += 1
    assert matched >= 1, f"Expected at least one visible ticket for '{family}'"

def _board_grid_row_track_heights(page: Page) -> list[float]:
    return page.evaluate("""() => {
      const grid = document.querySelector('.foundry-board-grid');
      if (!grid) return [];
      return window.getComputedStyle(grid).gridTemplateRows
        .split(' ')
        .map(v => parseFloat(v) || 0);
    }""")

def then_other_stage_tracks_collapsed(page: Page) -> None:
    """Gap + extra other-practice row tracks are zero-height; practice-rail other chip track remains."""
    rows = _board_grid_row_track_heights(page)
    assert len(rows) >= 9, f"Expected 9 grid row tracks, got {len(rows)}: {rows}"
    assert rows[5] <= 1, f"Expected stage-skills gap track collapsed, got {rows[5]}px"
    assert rows[6] >= 30, f"Expected other-practices rail track reserved, got {rows[6]}px"
    assert rows[7] <= 1, f"Expected second other row track collapsed, got {rows[7]}px"
    assert rows[8] <= 1, f"Expected third other row track collapsed, got {rows[8]}px"

def then_other_stage_skill_hidden(page: Page, skill_slug: str) -> None:
    """Stage-folder (other) skill ticket is not visible until other practices is ticked."""
    ticket = page.locator(
        f".aad-skill-row--stage-other .kb-ticket[href*='{skill_slug}'], "
        f".aad-skill-row--stage-other .kb-ticket[data-skill-href*='{skill_slug}']"
    ).first
    if ticket.count() == 0:
        return
    expect(ticket).to_be_hidden()

def then_other_stage_skill_visible(page: Page, skill_slug: str) -> None:
    """Stage-folder (other) skill ticket is visible after other practices is ticked."""
    ticket = page.locator(
        f".aad-skill-row--stage-other .kb-ticket[href*='{skill_slug}'], "
        f".aad-skill-row--stage-other .kb-ticket[data-skill-href*='{skill_slug}']"
    ).first
    expect(ticket).to_be_visible()

def then_other_stage_tracks_expanded(page: Page) -> None:
    """Other-practice section row tracks are open when other filter is active."""
    rows = _board_grid_row_track_heights(page)
    assert len(rows) >= 9, f"Expected 9 grid row tracks, got {len(rows)}: {rows}"
    assert rows[5] >= 30, f"Expected stage-skills gap track open, got {rows[5]}px"
    assert rows[6] >= 30, f"Expected first other row track open, got {rows[6]}px"

def then_other_practices_chip_aligns_with_practice_rail(page: Page) -> None:
    """Other Practices chip shares the same left edge and width as practice-family chips."""
    ref = page.locator(
        ".foundry-practice-col > .foundry-family-toggle[data-family='story-driven-delivery']"
    ).first
    other = page.locator(
        ".foundry-practice-col__other-practices .foundry-family-toggle[data-family='other']"
    ).first
    ref_box = ref.bounding_box()
    other_box = other.bounding_box()
    assert ref_box is not None and other_box is not None, "Expected both practice-rail chips to have layout boxes"
    assert abs(ref_box["x"] - other_box["x"]) <= 1, (
        f"Expected matching left edges, got ref={ref_box['x']} other={other_box['x']}"
    )
    assert abs(ref_box["width"] - other_box["width"]) <= 1, (
        f"Expected matching widths, got ref={ref_box['width']} other={other_box['width']}"
    )
    assert abs(ref_box["height"] - other_box["height"]) <= 1, (
        f"Expected matching heights, got ref={ref_box['height']} other={other_box['height']}"
    )

def then_surface_is_idle(page: Page) -> None:
    """No filter is active on the kanban surface."""
    surface = page.locator(".foundry-kanban-surface")
    assert not surface.evaluate("el => el.classList.contains('foundry-skill-filter-active')"), (
        "Expected kanban surface to be in Idle State (no foundry-skill-filter-active class)"
    )

def then_stage_filter_is_idle(page: Page) -> None:
    """No stage column filter is active."""
    surface = page.locator(".foundry-kanban-surface")
    assert not surface.evaluate("el => el.classList.contains('foundry-stage-filter-active')"), (
        "Expected kanban surface to have no stage filter active"
    )

def then_only_stage_column_visible(page: Page, stage: str) -> None:
    """All stage columns remain visible; only the focused column has skill tickets."""
    then_all_stage_columns_visible(page)
    for s in STAGE_COLUMN_STAGES:
        has_ticket = page.evaluate(
            """(stage) => {
              const col = document.querySelector(
                `.foundry-board-grid > .kb-col[data-stage="${stage}"]`
              );
              if (!col) return false;
              const rows = col.querySelectorAll('.aad-skill-row.is-filter-visible');
              for (const row of rows) {
                const style = window.getComputedStyle(row);
                if (style.display === 'none' || style.visibility === 'hidden') continue;
                if (parseFloat(style.opacity) < 0.05) continue;
                if (row.querySelector('.kb-ticket')) return true;
              }
              return false;
            }""",
            s,
        )
        if s == stage:
            assert has_ticket, f"Expected skill tickets in focused stage column '{stage}'"
        else:
            assert not has_ticket, (
                f"Expected empty stage column '{s}' when filtering '{stage}'"
            )

def then_all_stage_columns_visible(page: Page) -> None:
    """All five Stage Columns are visible."""
    for s in STAGE_COLUMN_STAGES:
        col = page.locator(f".foundry-board-grid > .kb-col[data-stage='{s}']").first
        hidden = col.evaluate("""el => window.getComputedStyle(el).display === 'none'""")
        assert not hidden, f"Expected stage column '{s}' to be visible"

def then_stage_column_head_is_current(page: Page, stage: str) -> None:
    """The Stage Column Head for this stage has the current indicator."""
    head = page.locator(f".kb-col-head[data-stage='{stage}']").first
    assert head.evaluate("el => el.classList.contains('kb-col-head--current')"), (
        f"Expected stage column head '{stage}' to be current"
    )

def then_stage_column_head_is_filtered(page: Page, stage: str) -> None:
    """Stage column head is toggled on like a family chip (selected + pressed + tick)."""
    head = page.locator(f".kb-col-head[data-stage='{stage}']").first
    expect(head).to_have_attribute("aria-pressed", "true")
    assert head.evaluate("el => el.classList.contains('is-selected')"), (
        f"Expected stage column head '{stage}' to be selected"
    )
    opacity = head.evaluate(
        "el => parseFloat(window.getComputedStyle(el, '::after').opacity)"
    )
    assert opacity > 0.5, (
        f"Expected tick on stage column head '{stage}' (::after opacity > 0.5), got {opacity}"
    )

def then_stage_column_head_is_unfiltered(page: Page, stage: str) -> None:
    """Stage column head is toggled off with no filter highlight."""
    head = page.locator(f".kb-col-head[data-stage='{stage}']").first
    expect(head).to_have_attribute("aria-pressed", "false")
    assert not head.evaluate("el => el.classList.contains('is-selected')"), (
        f"Expected stage column head '{stage}' to be unselected"
    )
    assert not head.evaluate("el => el.classList.contains('kb-col-head--current')"), (
        f"Expected stage column head '{stage}' to lose current indicator when filter clears"
    )
    opacity = head.evaluate(
        "el => parseFloat(window.getComputedStyle(el, '::after').opacity)"
    )
    assert opacity < 0.05, (
        f"Expected no tick on stage column head '{stage}' (::after opacity < 0.05), got {opacity}"
    )

def then_stage_questions_cell_is_inactive(page: Page, stage: str) -> None:
    """The Stage Questions Cell for this stage is not marked active."""
    cell = page.locator(f".kanban-stage-questions__cell[data-stage='{stage}']").first
    assert not cell.evaluate("el => el.classList.contains('is-active')"), (
        f"Expected stage questions cell '{stage}' to be inactive"
    )

def then_stage_columns_with_tickets(page: Page, stages: list[str]) -> None:
    """Given stages show skill tickets; all other stage columns are empty."""
    then_all_stage_columns_visible(page)
    stage_set = set(stages)
    for s in STAGE_COLUMN_STAGES:
        has_ticket = page.evaluate(
            """(stage) => {
              const col = document.querySelector(
                `.foundry-board-grid > .kb-col[data-stage="${stage}"]`
              );
              if (!col) return false;
              const rows = col.querySelectorAll('.aad-skill-row.is-filter-visible');
              for (const row of rows) {
                const style = window.getComputedStyle(row);
                if (style.display === 'none' || style.visibility === 'hidden') continue;
                if (parseFloat(style.opacity) < 0.05) continue;
                if (row.querySelector('.kb-ticket')) return true;
              }
              return false;
            }""",
            s,
        )
        if s in stage_set:
            assert has_ticket, f"Expected skill tickets in filtered stage column '{s}'"
        else:
            assert not has_ticket, (
                f"Expected empty stage column '{s}' when filtering {sorted(stage_set)}"
            )

def then_stage_questions_cell_is_active(page: Page, stage: str) -> None:
    """The Stage Questions Cell for this stage is marked active."""
    cell = page.locator(f".kanban-stage-questions__cell[data-stage='{stage}']").first
    assert cell.evaluate("el => el.classList.contains('is-active')"), (
        f"Expected stage questions cell '{stage}' to be active"
    )

def then_skill_absent_from_board_grid(page: Page, skill_slug: str) -> None:
    """A skill ticket does not appear in the stage-column board grid."""
    links = page.locator(f".foundry-board-grid a[href*='{skill_slug}']")
    assert links.count() == 0, f"Expected '{skill_slug}' absent from board grid, found {links.count()}"

def then_kanban_supporting_skills_only_in_supporting_section(page: Page) -> None:
    """Kanban practice skills live in the supporting crosscut area, not on the board."""
    for slug in KANBAN_SUPPORTING_SKILL_SLUGS:
        then_skill_absent_from_board_grid(page, slug)
        link = page.locator(
            f".aad-delivery-crosscut-section--supporting a[href*='{slug}']"
        ).first
        expect(link).to_be_attached()
