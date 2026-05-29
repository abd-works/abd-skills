"""Build delivery kanban HTML from delivery/content/stages/*.md practice-skill tables."""

from __future__ import annotations

import html as html_mod
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

BOOTCAMP_CATALOG_PREFIX = "../abd-skills-catalog/"

# GitHub tree leaf folder → catalog skill dir_name
GITHUB_SKILL_ALIASES: dict[str, str] = {
    "abd-opportunity-canvas": "abd-opportunity-generation",
}

STAGE_FILES: tuple[tuple[str, str, int], ...] = (
    ("shaping", "Shaping", 1),
    ("discovery", "Discovery", 2),
    ("exploration", "Exploration", 3),
    ("specification", "Specification", 4),
    ("engineering", "Engineering", 5),
)

FAMILY_DISPLAY_TO_PLUGIN: dict[str, str] = {
    "domain-driven design": "domain-driven-design",
    "story-driven delivery": "story-driven-delivery",
    "user experience design": "user-experience-design",
    "architecture-centric engineering": "architecture-centric-engineering",
    "idea shaping": "idea-shaping",
}

PLUGIN_ROW_ORDER: tuple[str, ...] = (
    "domain-driven-design",
    "user-experience-design",
    "story-driven-delivery",
    "architecture-centric-engineering",
)

PLUGIN_CSS_CLASS: dict[str, str] = {
    "domain-driven-design": "aad-fam-ddd",
    "user-experience-design": "aad-fam-uxd",
    "story-driven-delivery": "aad-fam-sdd",
    "architecture-centric-engineering": "aad-fam-arc",
    "idea-shaping": "aad-fam-idea",
    "delivery": "aad-fam-delivery",
}

PLUGIN_LABEL: dict[str, str] = {
    "domain-driven-design": "Domain-driven design",
    "user-experience-design": "User experience design",
    "story-driven-delivery": "Story-driven delivery",
    "architecture-centric-engineering": "Architecture-centric engineering",
    "idea-shaping": "Idea shaping",
    "delivery": "Delivery",
}

DELIVERY_CROSSCUT_SKILLS: tuple[str, ...] = (
    "abd-kanban-planning",
    "abd-kanban",
    "abd-kanban-repo",
    "kanban-estimation",
)

DELIVERY_AGENTS: tuple[str, ...] = (
    "delivery-lead",
    "product-owner",
    "product-owner-reviewer",
    "business-expert",
    "business-expert-reviewer",
    "ux-designer",
    "ux-designer-reviewer",
    "engineer",
    "engineer-reviewer",
)

# Infrastructure / diagram sync skills — omitted from kanban tiles (stage docs unchanged).
KANBAN_EXCLUDED_SKILLS: frozenset[str] = frozenset(
    {
        "drawio-domain-sync",
        "drawio-story-sync",
        "story-graph-ops",
        "miro-story-sync",
        "abd-bounded-context-map",
        "abd-opportunity-generation",
    }
)

# Hide specific skills on the kanban grid only (stage markdown unchanged).
KANBAN_STAGE_EXCLUDED_SKILLS: dict[str, frozenset[str]] = {
    "discovery": frozenset({"abd-ubiquitous-language"}),
}

# Kanban tile label overrides (stage_id, skill_id) → display text.
KANBAN_SKILL_LABEL_OVERRIDES: dict[tuple[str, str], str] = {
    ("shaping", "abd-story-mapping"): "story mapping outline",
}

STAGE_SPOTLIGHT_ORDER: tuple[str, ...] = (
    "shaping",
    "discovery",
    "exploration",
    "specification",
    "engineering",
)

STAGE_SPOTLIGHT_SLIDE_NUM: dict[str, int] = {
    "shaping": 2,
    "discovery": 3,
    "exploration": 4,
    "specification": 5,
    "engineering": 6,
}

# Vertical index inside the Reveal.js stack (0 = overview).
STAGE_VERTICAL_SLIDE_INDEX: dict[str, int] = {
    "shaping": 1,
    "discovery": 2,
    "exploration": 3,
    "specification": 4,
    "engineering": 5,
}


def _kanban_include_skill(skill_id: str, *, stage_id: str | None = None) -> bool:
    if skill_id in KANBAN_EXCLUDED_SKILLS:
        return False
    if stage_id and skill_id in KANBAN_STAGE_EXCLUDED_SKILLS.get(stage_id, frozenset()):
        return False
    if skill_id.endswith("-sync"):
        return False
    return skill_id != "story-graph-ops"

# Per-stage context-window depth — detail text appears under scale shapes (not duplicated below).
STAGE_CONTEXT: dict[str, tuple[str, str]] = {
    "shaping": ("wide / shallow", "Whole-solution view — outline map and boundaries."),
    "discovery": ("medium", "Full map, domain, UX IA, architecture blueprint."),
    "exploration": ("narrow / deeper", "Increment slice — AC, mockups, arch templates."),
    "specification": ("narrow / executable", "CRC, scenarios, interface spec, arch reference."),
    "engineering": ("narrowest / deep", "Tests first, then running production code."),
}

# Scale diagram steps → delivery stage (for depth label + detail under each shape).
SCALE_STEPS: tuple[tuple[str, str, str], ...] = (
    ("aad-scale-solution", "Whole Solution", "shaping"),
    ("aad-scale-increment", "Increment", "discovery"),
    ("aad-scale-sprint", "Sprint", "exploration"),
    ("aad-scale-story", "Story", "engineering"),
)

PRINCIPLES_HTML = """\
  <div class="aad-principles">
    <div class="aad-principle">
      <div class="aad-principle-tag">Agile foundation</div>
      <div class="aad-principle-body">Frequent feedback. Cross-functional <em>context</em>, not cross-functional teams. Test-driven and executable. Domain-oriented.</div>
    </div>
    <div class="aad-principle">
      <div class="aad-principle-tag">Layered context</div>
      <div class="aad-principle-body">Keep the window <em>small</em> — but reshape it as work progresses. Wide and shallow at the solution. Narrow and deep at the story.</div>
    </div>
    <div class="aad-principle">
      <div class="aad-principle-tag">Human-in-the-loop</div>
      <div class="aad-principle-body">Ask the agent <em>hard questions</em> through validating lenses. Humans review each lens to prevent known failure modes before work moves right.</div>
    </div>
  </div>"""

TABLE_SKILL_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*\*\*(.+?)\*\*\s*\|\s*`([^`]+)`",
    re.MULTILINE | re.IGNORECASE,
)


@dataclass
class StageSkill:
    plugin_id: str
    skill_id: str
    notes: str = ""


@dataclass
class KanbanModel:
    stages: list[tuple[str, str, int, str]] = field(default_factory=list)
    matrix: dict[str, dict[str, list[StageSkill]]] = field(default_factory=dict)
    stage_purpose: dict[str, str] = field(default_factory=dict)


def _h(text: str) -> str:
    return html_mod.escape(text, quote=True)


def build_scale_row_html() -> str:
    """Context-window scale: shape, name, depth label, and stage detail under each step."""
    lines = [
        '  <div class="aad-scale-row" role="img" '
        'aria-label="Context window narrows from Whole Solution to Story">',
    ]
    for index, (step_class, step_name, stage_id) in enumerate(SCALE_STEPS):
        if index:
            lines.append('    <div class="aad-scale-arrow"></div>')
        depth_label, detail = STAGE_CONTEXT.get(stage_id, ("", ""))
        lines.append(f'    <div class="aad-scale-step {step_class}">')
        lines.append('      <div class="aad-scale-shape"></div>')
        lines.append(f'      <div class="aad-scale-name">{_h(step_name)}</div>')
        if depth_label:
            lines.append(
                f'      <div class="aad-scale-shape-label">{_h(depth_label)}</div>'
            )
        if detail:
            lines.append(f'      <div class="aad-scale-detail">{_h(detail)}</div>')
        lines.append("    </div>")
    lines.append("  </div>")
    return "\n".join(lines)


CONTEXT_WINDOW_SPOTLIGHT_HTML = f"""\
<div class="kb-spotlight kanban-context-spotlight" data-id="context-window">
  <div class="kb-spotlight-head">
    <div class="kb-spotlight-title">Layered context — wide and shallow to narrow and deep</div>
  </div>
  <div class="kb-spotlight-body">
{PRINCIPLES_HTML}
{build_scale_row_html()}
  </div>
</div>"""


def _skill_label(skill_id: str, stage_id: str | None = None) -> str:
    if stage_id and (stage_id, skill_id) in KANBAN_SKILL_LABEL_OVERRIDES:
        return KANBAN_SKILL_LABEL_OVERRIDES[(stage_id, skill_id)]
    name = skill_id.removeprefix("abd-")
    return name.replace("-", " ")


def _normalize_family(raw: str) -> str:
    return re.sub(r"\s+", " ", raw.strip().lower())


def _parse_stage_markdown(path: Path) -> tuple[str, list[StageSkill]]:
    text = path.read_text(encoding="utf-8")
    purpose = ""
    m = re.search(r"^## Purpose\s*\n\n(.+?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    if m:
        purpose = re.sub(r"\s+", " ", m.group(1).strip())
    skills: list[StageSkill] = []
    for fam_raw, skill_raw in TABLE_SKILL_RE.findall(text):
        fam = _normalize_family(fam_raw)
        plugin_id = FAMILY_DISPLAY_TO_PLUGIN.get(fam)
        if not plugin_id:
            continue
        skill_id = skill_raw.strip().split()[0]
        if "**" in skill_id:
            skill_id = skill_id.split("**", 1)[0].strip()
        notes = ""
        if "(" in skill_raw and ")" in skill_raw:
            notes = skill_raw[skill_raw.find("(") + 1 : skill_raw.rfind(")")].strip()
        skills.append(StageSkill(plugin_id=plugin_id, skill_id=skill_id, notes=notes))
    return purpose, skills


def load_kanban_model(repo_root: Path) -> KanbanModel:
    stages_dir = repo_root / "delivery" / "content" / "stages"
    model = KanbanModel()
    for stage_id, title, num in STAGE_FILES:
        path = stages_dir / f"{stage_id}.md"
        if not path.is_file():
            continue
        purpose, skills = _parse_stage_markdown(path)
        model.stages.append((stage_id, title, num, purpose))
        model.stage_purpose[stage_id] = purpose
        model.matrix[stage_id] = {}
        for sk in skills:
            model.matrix[stage_id].setdefault(sk.plugin_id, []).append(sk)
    apply_kanban_display_model(model)
    return model


def apply_kanban_display_model(model: KanbanModel) -> None:
    """Kanban-only filters — does not alter stage source files."""
    for stage_id in model.matrix:
        stage_skip = KANBAN_STAGE_EXCLUDED_SKILLS.get(stage_id, frozenset())
        for plugin_id in list(model.matrix[stage_id].keys()):
            model.matrix[stage_id][plugin_id] = [
                sk
                for sk in model.matrix[stage_id][plugin_id]
                if _kanban_include_skill(sk.skill_id)
                and sk.skill_id not in stage_skip
            ]
            if not model.matrix[stage_id][plugin_id]:
                del model.matrix[stage_id][plugin_id]


def _skill_href(skill_id: str, skill_dir_by_name: dict[str, str], *, relative: str) -> str:
    dir_name = skill_dir_by_name.get(skill_id, skill_id)
    return f"{relative}skill/{quote(dir_name, safe='')}.html"


def _agent_href(agent_dir: str, *, relative: str) -> str:
    return f"{relative}agent/{quote(agent_dir, safe='')}.html"


def _plugin_href(plugin_id: str, *, relative: str) -> str:
    return f"{relative}plugin/{quote(plugin_id, safe='')}.html"


def build_kanban_legend_html(*, relative_href_prefix: str = "../", indent: str = "      ") -> str:
    """Practice plugin key cards (same style as skill tickets); delivery omitted — in crosscut."""
    cards: list[str] = []
    for plugin_id in PLUGIN_ROW_ORDER:
        css = PLUGIN_CSS_CLASS.get(plugin_id, "")
        href = _plugin_href(plugin_id, relative=relative_href_prefix)
        cards.append(
            f'<a class="kb-ticket aad-skill {css}" '
            f'href="{_h(href)}">{_h(plugin_id)}</a>'
        )
    block = (
        '<div class="kanban-legend-row">\n'
        '  <div class="kanban-legend-heading">Practice plugins</div>\n'
        '  <div class="kanban-legend-cards">\n'
        + "\n".join(f"    {c}" for c in cards)
        + "\n  </div>\n"
        "</div>"
    )
    if not indent:
        return block
    return textwrap.indent(block, indent)


def _stage_href(stage_id: str, *, same_page: bool, relative: str) -> str:
    anchor = f"#stage-{stage_id}"
    if same_page:
        return anchor
    return f"{relative}kanban-layout/index.html{anchor}"


def build_stage_context_spotlight() -> str:
    """Principles and scale diagram — below board + legend (matches bootcamp kb-spotlight)."""
    return CONTEXT_WINDOW_SPOTLIGHT_HTML


_SHAPING_STORY_MAP_OUTLINE = """\
        <div class="aad-artifact aad-fam-sdd">
          <div class="aad-artifact-head">
            <span class="aad-art-skill"><a href="{prefix}skill/abd-story-mapping.html">story-mapping</a></span>
            <a class="aad-art-path" href="{prefix}skill/abd-story-mapping.html">outline mode</a>
          </div>
<div class="aad-fac aad-fac-story-map aad-fac-story-map--outline" aria-label="Story map outline — epics and flows only">
  <div class="aad-fac-sm-persona">GM (Game Master)</div>
  <div class="aad-fac-sm-epic">Manage Crowds</div>
  <div class="aad-fac-sm-epic">Run Roster</div>
  <div class="aad-fac-sm-epic">Drive Combat</div>
  <div class="aad-fac-sm-stories"><div class="aad-fac-sm-story aad-fac-sm-story--outline-hint">epics &amp; journeys — not full story depth</div></div>
  <div class="aad-fac-sm-stories"><div class="aad-fac-sm-story aad-fac-sm-story--outline-hint">&nbsp;</div></div>
  <div class="aad-fac-sm-stories"><div class="aad-fac-sm-story aad-fac-sm-story--outline-hint">&nbsp;</div></div>
</div>
        </div>"""


def _bootcamp_slides_css_path(repo_root: Path) -> Path:
    return (
        repo_root.parent
        / "abd-works"
        / "abd-ai-augmented-bootcamp"
        / "slides.css"
    )


def _bootcamp_abd_works_css_path(repo_root: Path) -> Path:
    return (
        repo_root.parent
        / "abd-works"
        / "abd-ai-augmented-bootcamp"
        / "css"
        / "abd-works.css"
    )


def load_bootcamp_abd_works_css(repo_root: Path) -> str:
    """Full bootcamp abd-works.css — same stylesheet as index.html."""
    css_path = _bootcamp_abd_works_css_path(repo_root)
    if not css_path.is_file():
        return ""
    return (
        "/* Bootcamp abd-works.css (synced from abd-ai-augmented-bootcamp/css/abd-works.css) */\n"
        + css_path.read_text(encoding="utf-8")
    )


def load_bootcamp_kanban_base_css(repo_root: Path) -> str:
    """Kanban slide chrome from bootcamp slides.css (layout, tickets, crosscut, spotlight shell)."""
    css_path = _bootcamp_slides_css_path(repo_root)
    if not css_path.is_file():
        return ""
    raw = css_path.read_text(encoding="utf-8")
    start = raw.find("/* -- Story-Driven Kanban: layout")
    end = raw.find(".aad-spot-lead {")
    if start == -1 or end == -1:
        return ""
    return (
        "/* Bootcamp kanban base (synced from abd-ai-augmented-bootcamp/slides.css) */\n"
        + raw[start:end]
    )


def load_bootcamp_artifact_css(repo_root: Path) -> str:
    """Facsimile + spotlight styles from bootcamp slides.css (Part 3 artifact panels)."""
    css_path = _bootcamp_slides_css_path(repo_root)
    if not css_path.is_file():
        return ""
    raw = css_path.read_text(encoding="utf-8")
    start = raw.find(".aad-spot-lead {")
    # Include artifact-row + all aad-fac-* facsimiles (after .aad-fam-legend block).
    end = raw.find(".story-map {")
    if start == -1:
        return ""
    chunk = raw[start:end] if end != -1 else raw[start:]
    return (
        "/* Bootcamp Part 3 artifact facsimiles (synced from abd-ai-augmented-bootcamp/slides.css) */\n"
        + chunk
    )


def _repair_unclosed_divs(html: str) -> str:
    """Bootcamp part3 spotlight slides truncate before closing divs — balance them."""
    opens = len(re.findall(r"<div[\s>]", html, flags=re.I))
    closes = len(re.findall(r"</div>", html, flags=re.I))
    missing = opens - closes
    if missing > 0:
        html = html + "\n" + ("</div>\n" * missing)
    return html


def _kanban_spotlight_source_path(repo_root: Path) -> Path:
    """Spotlight/header source for catalog kanban regen (canonical generated deck)."""
    catalog = repo_root / "catalog" / "kanban-layout" / "index.html"
    if catalog.is_file():
        return catalog
    return _bootcamp_part3_path(repo_root)


def _read_kanban_spotlight_source(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp1252")


def _is_catalog_kanban_index(path: Path, repo_root: Path) -> bool:
    try:
        return path.resolve() == (repo_root / "catalog" / "kanban-layout" / "index.html").resolve()
    except OSError:
        return False


def _catalog_slide_id_for_num(slide_num: int) -> str:
    if slide_num == 1:
        return "overview"
    for stage_id, num in STAGE_SPOTLIGHT_SLIDE_NUM.items():
        if num == slide_num:
            return f"stage-{stage_id}"
    return ""


def _extract_catalog_kanban_slide(text: str, slide_id: str) -> str:
    pattern = re.compile(
        rf'<section class="kb-slide"[^>]*\sid="{re.escape(slide_id)}"[^>]*>([\s\S]*?)</section>',
        re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(0) if match else ""


def _split_kanban_spotlight_slides(source_text: str, source_path: Path, repo_root: Path) -> dict[int, str]:
    if _is_catalog_kanban_index(source_path, repo_root):
        out: dict[int, str] = {}
        for slide_num in range(1, 7):
            slide_id = _catalog_slide_id_for_num(slide_num)
            if slide_id:
                html = _extract_catalog_kanban_slide(source_text, slide_id)
                if html:
                    out[slide_num] = html
        return out
    return _split_bootcamp_stage_slides(source_text)


def _split_bootcamp_stage_slides(part3_text: str) -> dict[int, str]:
    parts = re.split(
        r"<!-- ===========================================================\s*\n\s*SLIDE (\d+)[^\n]*\n\s*={10,}",
        part3_text,
    )
    out: dict[int, str] = {}
    for idx in range(1, len(parts), 2):
        slide_num = int(parts[idx])
        out[slide_num] = parts[idx + 1] if idx + 1 < len(parts) else ""
    return out


def extract_bootcamp_stage_spotlights(repo_root: Path) -> dict[str, tuple[str, str]]:
    """Return stage_id → (spotlight_title, spotlight_body_inner_html) from kanban slides 2–6."""
    source_path = _kanban_spotlight_source_path(repo_root)
    if not source_path.is_file():
        return {}
    text = _read_kanban_spotlight_source(source_path)
    slides = _split_kanban_spotlight_slides(text, source_path, repo_root)
    out: dict[str, tuple[str, str]] = {}
    for stage_id in STAGE_SPOTLIGHT_ORDER:
        slide_num = STAGE_SPOTLIGHT_SLIDE_NUM[stage_id]
        slide_html = slides.get(slide_num, "")
        title = stage_id.replace("-", " ").title()
        title_m = re.search(
            r'<div class="kb-spotlight-title">([^<]+)',
            slide_html,
        )
        if title_m:
            title = html_mod.unescape(title_m.group(1).strip())
        body_m = re.search(
            r'<div class="kb-spotlight-body">([\s\S]*?)</section>',
            slide_html,
            re.DOTALL,
        )
        if body_m:
            body = _repair_unclosed_divs(body_m.group(1).strip())
            out[stage_id] = (title, body)
    return out


def _catalogize_spotlight_html(html: str, *, catalog_prefix: str = "../") -> str:
    text = html.replace(BOOTCAMP_CATALOG_PREFIX, catalog_prefix)
    text = text.replace("../../../../agilebydesign-skills/catalog/", catalog_prefix)
    text = text.replace('target="_blank" rel="noopener"', "")
    # Catalog kanban spotlights use ../skill/, ../plugin/, … (relative to catalog root).
    # Bootcamp deck resolves links from /abd-ai-augmented-bootcamp/ → ../abd-skills-catalog/…
    if catalog_prefix not in ("../", "./"):
        text = re.sub(
            r'href="\.\./(?!abd-skills-catalog/)',
            f'href="{catalog_prefix}',
            text,
        )
    text = re.sub(
        rf'href="{re.escape(catalog_prefix)}"\s+class="kb-skill-pill"',
        f'href="{catalog_prefix}index.html" class="kb-skill-pill"',
        text,
    )
    return text


def extract_bootcamp_slide_header(slide_html: str) -> str:
    match = re.search(
        r'(<div class="kb-header">[\s\S]*?</div>)\s*\n\s*(?:<div class="kb-board|<div class="kb-spotlight")',
        slide_html,
    )
    return match.group(1).strip() if match else ""


def extract_bootcamp_slide_headers(repo_root: Path) -> dict[int, str]:
    """Slide number → kb-header HTML from kanban deck (slides 1–6)."""
    source_path = _kanban_spotlight_source_path(repo_root)
    if not source_path.is_file():
        return {}
    text = _read_kanban_spotlight_source(source_path)
    slides = _split_kanban_spotlight_slides(text, source_path, repo_root)
    out: dict[int, str] = {}
    for slide_num in range(1, 7):
        header = extract_bootcamp_slide_header(slides.get(slide_num, ""))
        if header:
            out[slide_num] = header
    return out


def build_overview_spotlight_html() -> str:
    """Slide 1 spotlight — principles + context-window scale (bootcamp data-id=spot)."""
    return (
        '<div class="kb-spotlight" data-id="spot">\n'
        '  <div class="kb-spotlight-head" data-id="spot-head">\n'
        '    <div class="kb-spotlight-title">The Five Families &times; Five Stages</div>\n'
        "  </div>\n"
        '  <div class="kb-spotlight-body">\n'
        f"{PRINCIPLES_HTML}\n"
        f"{build_scale_row_html()}\n"
        "  </div>\n"
        "</div>"
    )


def build_stage_spotlight_html(title: str, body_inner: str) -> str:
    """One stage spotlight panel (bootcamp slide 2–6 shape)."""
    return (
        '<div class="kb-spotlight" data-id="spot">\n'
        '  <div class="kb-spotlight-head" data-id="spot-head">\n'
        f'    <div class="kb-spotlight-title">{_h(title)}</div>\n'
        "  </div>\n"
        '  <div class="kb-spotlight-body">\n'
        f"{body_inner}\n"
        "  </div>\n"
        "</div>"
    )


def build_kanban_slide_section(
    slide_id: str,
    header_html: str,
    board_html: str,
    legend_html: str,
    spotlight_html: str,
) -> str:
    return (
        f'<section class="kb-slide" data-auto-animate id="{slide_id}">\n'
        f"{textwrap.indent(header_html.strip(), '  ')}\n"
        f"{textwrap.indent(board_html.strip(), '  ')}\n"
        f"{textwrap.indent(legend_html.strip(), '  ')}\n"
        f"{textwrap.indent(spotlight_html.strip(), '  ')}\n"
        "</section>"
    )


def _inject_shaping_story_map_outline(body: str, *, catalog_prefix: str = "../") -> str:
    artifact = _SHAPING_STORY_MAP_OUTLINE.format(prefix=catalog_prefix)
    if "aad-fac-story-map--outline" in body:
        return body
    marker = '<div class="aad-artifact-row">'
    if marker in body:
        return body.replace(marker, marker + "\n" + artifact, 1)
    return body + "\n" + artifact


def build_catalog_stage_spotlight_bodies(
    repo_root: Path,
    *,
    catalog_prefix: str = "../",
) -> dict[str, tuple[str, str]]:
    """stage_id → (title, spotlight body inner HTML)."""
    spotlights = extract_bootcamp_stage_spotlights(repo_root)
    out: dict[str, tuple[str, str]] = {}
    for stage_id, entry in spotlights.items():
        title, body = entry
        body = _catalogize_spotlight_html(body, catalog_prefix=catalog_prefix)
        if stage_id == "shaping":
            body = _inject_shaping_story_map_outline(body, catalog_prefix=catalog_prefix)
        out[stage_id] = (title, body)
    return out


def build_kanban_slides_deck_html(
    model: KanbanModel,
    skill_dir_by_name: dict[str, str],
    repo_root: Path,
    *,
    relative_href_prefix: str = "../",
    same_page_stages: bool = True,
    link_column_heads: bool = True,
) -> str:
    """Vertical kb-slide stack (catalog kanban-layout or bootcamp part3 sync)."""
    headers = extract_bootcamp_slide_headers(repo_root)
    if relative_href_prefix != "../":
        headers = {
            n: _catalogize_spotlight_html(h, catalog_prefix=relative_href_prefix)
            for n, h in headers.items()
        }
    spotlight_bodies = build_catalog_stage_spotlight_bodies(
        repo_root, catalog_prefix=relative_href_prefix
    )
    legend = build_kanban_legend_html(relative_href_prefix=relative_href_prefix)
    slide_sections: list[str] = []

    overview_board = build_kanban_board_html(
        model,
        skill_dir_by_name,
        relative_href_prefix=relative_href_prefix,
        same_page_stages=same_page_stages,
        active_stage_id=None,
        include_delivery_crosscut=True,
        link_column_heads=link_column_heads,
    )
    slide_sections.append(
        build_kanban_slide_section(
            "overview",
            headers.get(1, ""),
            overview_board,
            legend,
            build_overview_spotlight_html(),
        )
    )

    for stage_id in STAGE_SPOTLIGHT_ORDER:
        slide_num = STAGE_SPOTLIGHT_SLIDE_NUM[stage_id]
        entry = spotlight_bodies.get(stage_id)
        if not entry:
            continue
        title, body = entry
        board = build_kanban_board_html(
            model,
            skill_dir_by_name,
            relative_href_prefix=relative_href_prefix,
            same_page_stages=same_page_stages,
            active_stage_id=stage_id,
            include_delivery_crosscut=True,
            link_column_heads=link_column_heads,
        )
        slide_sections.append(
            build_kanban_slide_section(
                f"stage-{stage_id}",
                headers.get(slide_num, ""),
                board,
                legend,
                build_stage_spotlight_html(title, body),
            )
        )

    return "\n".join(slide_sections)


def build_kanban_page_body(
    model: KanbanModel,
    skill_dir_by_name: dict[str, str],
    stages_html: str,
    *,
    repo_root: Path,
) -> str:
    """Reveal slide stack only (fullscreen page — no catalog chrome)."""
    return build_kanban_slides_deck_html(model, skill_dir_by_name, repo_root)


def build_kanban_board_html(
    model: KanbanModel,
    skill_dir_by_name: dict[str, str],
    *,
    relative_href_prefix: str = "../",
    same_page_stages: bool = False,
    board_class: str = "aad-board-grid",
    active_stage_id: str | None = None,
    include_delivery_crosscut: bool = True,
    link_column_heads: bool = True,
) -> str:
    rel = relative_href_prefix

    cols: list[str] = []
    for stage_id, title, num, _purpose in model.stages:
        stage_link = _stage_href(stage_id, same_page=same_page_stages, relative=rel)
        active_cls = " active" if active_stage_id == stage_id else ""
        col_rows: list[str] = []
        for plugin_id in PLUGIN_ROW_ORDER:
            skills = model.matrix.get(stage_id, {}).get(plugin_id, [])
            css = PLUGIN_CSS_CLASS.get(plugin_id, "")
            tickets: list[str] = []
            for sk in skills:
                if not _kanban_include_skill(sk.skill_id, stage_id=stage_id):
                    continue
                href = _skill_href(sk.skill_id, skill_dir_by_name, relative=rel)
                label = _skill_label(sk.skill_id, stage_id)
                title_attr = f' title="{_h(sk.notes)}"' if sk.notes else ""
                tickets.append(
                    f'        <a class="kb-ticket aad-skill {css}" '
                    f'data-id="tk-{plugin_id}-{stage_id}-{_h(sk.skill_id)}" '
                    f'href="{_h(href)}"{title_attr}>{_h(label)}</a>'
                )
            inner = "\n".join(tickets) if tickets else ""
            empty_cls = " aad-skill-row--empty" if not tickets else ""
            col_rows.append(
                f'      <div class="aad-skill-row {css}{empty_cls}" data-family="{plugin_id}">\n'
                f"{inner}\n      </div>"
            )
        if link_column_heads:
            col_head = (
                f'      <a class="kb-col-head kb-col-head--link" data-id="head-{stage_id}" '
                f'href="{_h(stage_link)}"><span>{_h(title)}</span>'
                f'<span class="kb-col-num">{num}</span></a>\n'
            )
        else:
            col_head = (
                f'      <div class="kb-col-head" data-id="head-{stage_id}">'
                f"<span>{_h(title)}</span>"
                f'<span class="kb-col-num">{num}</span></div>\n'
            )
        cols.append(
            f'    <div class="kb-col{active_cls}" data-id="col-{stage_id}">\n'
            f"{col_head}"
            f'      <div class="kb-col-tickets aad-tickets-grid">\n'
            + "\n".join(col_rows)
            + "\n      </div>\n    </div>"
        )

    crosscut = ""
    if include_delivery_crosscut:
        delivery_skills_html: list[str] = []
        for skill_id in DELIVERY_CROSSCUT_SKILLS:
            href = _skill_href(skill_id, skill_dir_by_name, relative=rel)
            delivery_skills_html.append(
                f'        <a class="kb-ticket aad-skill aad-fam-delivery" '
                f'href="{_h(href)}">{_h(_skill_label(skill_id))}</a>'
            )

        delivery_agents_html: list[str] = []
        for agent in DELIVERY_AGENTS:
            delivery_agents_html.append(
                f'        <a class="aad-delivery-leaf aad-row-agent aad-fam-delivery" '
                f'data-id="agent-{_h(agent)}" '
                f'href="{_h(_agent_href(agent, relative=rel))}">{_h(agent)}</a>'
            )

        crosscut = (
            '<div class="aad-delivery-crosscut aad-delivery-crosscut-grid" data-id="delivery-crosscut">\n'
            '  <div class="aad-delivery-crosscut-lane">\n'
            f'    <a class="aad-delivery-crosscut-label aad-fam-delivery" '
            f'data-id="row-label-delivery" '
            f'href="{_h(_plugin_href("delivery", relative=rel))}">'
            f"{_h(PLUGIN_LABEL['delivery'])}</a>\n"
            "  </div>\n"
            '  <div class="aad-delivery-crosscut-skills-band">\n'
            '    <div class="aad-delivery-crosscut-row aad-delivery-crosscut-row--inline">\n'
            '      <div class="aad-delivery-crosscut-sublabel">Agents</div>\n'
            '      <div class="aad-delivery-crosscut-agents">\n'
            + "\n".join(delivery_agents_html)
            + "\n      </div>\n"
            '      <div class="aad-delivery-crosscut-sublabel aad-delivery-crosscut-sublabel--skills">Skills</div>\n'
            '      <div class="aad-delivery-crosscut-skills">\n'
            + "\n".join(delivery_skills_html)
            + "\n      </div>\n"
            "    </div>\n"
            '    <div class="aad-delivery-crosscut-tracks" aria-hidden="true">\n'
            '      <span class="aad-delivery-arrow"></span>\n'
            '      <span class="aad-delivery-arrow"></span>\n'
            '      <span class="aad-delivery-arrow"></span>\n'
            '      <span class="aad-delivery-arrow"></span>\n'
            '      <span class="aad-delivery-arrow"></span>\n'
            "    </div>\n"
            "  </div>\n"
            "</div>"
        )

    return (
        f'<div class="kb-board {board_class}" data-id="board">\n'
        + "\n".join(cols)
        + "\n</div>\n"
        + crosscut
    )


def build_stage_sections_html(model: KanbanModel) -> str:
    parts: list[str] = ['<section class="kanban-stages" id="stages">', "<h2>Delivery stages</h2>"]
    planning_href = "../skill/abd-delivery-planning.html"
    parts.append(
        f'<p>Stage definitions are the source of truth for '
        f'<a href="{_h(planning_href)}">abd-delivery-planning</a> '
        f"and the delivery war room. Each column above links here.</p>"
    )
    for stage_id, title, num, purpose in model.stages:
        stage_src = (
            f"https://github.com/abd-works/agilebydesign-skills/blob/main/"
            f"delivery/content/stages/{stage_id}.md"
        )
        parts.append(f'<article class="kanban-stage" id="stage-{stage_id}-definition">')
        parts.append(
            f"<h3>{num}. {_h(title)}</h3>"
            f'<p class="kanban-stage-links">'
            f'<a href="{_h(planning_href)}">abd-delivery-planning</a> · '
            f'<a href="{_h(stage_src)}">stage definition (source)</a></p>'
        )
        if purpose:
            parts.append(f"<p>{_h(purpose)}</p>")
        skills = model.matrix.get(stage_id, {})
        if skills:
            parts.append("<ul>")
            for plugin_id in PLUGIN_ROW_ORDER:
                for sk in skills.get(plugin_id, []):
                    if not _kanban_include_skill(sk.skill_id, stage_id=stage_id):
                        continue
                    parts.append(
                        f"<li><strong>{_h(PLUGIN_LABEL.get(plugin_id, plugin_id))}</strong> — "
                        f"<code>{_h(sk.skill_id)}</code>"
                        + (f" ({_h(sk.notes)})" if sk.notes else "")
                        + "</li>"
                    )
            parts.append("</ul>")
        parts.append("</article>")
    parts.append("</section>")
    return "\n".join(parts)


def build_kanban_garden_link_html(*, relative_href_prefix: str = "../") -> str:
    """Short link to the catalog hub below board + legend."""
    return (
        f'<p class="kanban-garden-link">'
        f'<a href="{relative_href_prefix}index.html">The ABD AI Garden</a>'
        f" — browse plugins, skills, and agents</p>"
    )


def write_kanban_layout_pages(
    output_catalog_dir: Path,
    repo_root: Path,
    skill_dir_by_name: dict[str, str],
    css: str,
    brand: str,
    h1: str,
    tagline: str,
    *,
    template_dir: Path,
) -> Path:
    model = load_kanban_model(repo_root)
    out_dir = output_catalog_dir / "kanban-layout"
    out_dir.mkdir(parents=True, exist_ok=True)

    page_tpl = (template_dir / "kanban-layout.html").read_text(encoding="utf-8")
    kanban_css = (template_dir / "kanban-layout.css").read_text(encoding="utf-8")
    abd_works_css = load_bootcamp_abd_works_css(repo_root)
    kanban_base_css = load_bootcamp_kanban_base_css(repo_root)
    artifact_css = load_bootcamp_artifact_css(repo_root)
    full_css = abd_works_css + "\n" + kanban_base_css + "\n" + artifact_css + "\n" + kanban_css

    board_html = build_kanban_board_html(
        model,
        skill_dir_by_name,
        relative_href_prefix="../",
        same_page_stages=True,
    )
    stages_html = build_stage_sections_html(model)

    slides_html = build_kanban_page_body(
        model, skill_dir_by_name, stages_html, repo_root=repo_root
    )

    reveal_js_src = template_dir / "kanban-slides-init.js"
    reveal_init_js = (
        reveal_js_src.read_text(encoding="utf-8") if reveal_js_src.is_file() else ""
    )

    html = (
        page_tpl.replace("{{CSS}}", full_css)
        .replace("{{TITLE}}", "AI Garden — delivery kanban")
        .replace("{{SLIDES_INNER}}", slides_html)
        .replace("{{REVEAL_INIT_JS}}", reveal_init_js)
    )
    index_path = out_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")

    legacy_external = out_dir / "kanban-slides-init.js"
    if legacy_external.is_file():
        legacy_external.unlink()
    legacy_reveal = out_dir / "kanban-reveal-init.js"
    if legacy_reveal.is_file():
        legacy_reveal.unlink()

    fragment_path = out_dir / "board.fragment.html"
    fragment_path.write_text(
        "<!-- AUTO-GENERATED by generate_abd_catalog.py — do not edit by hand. -->\n"
        + build_kanban_board_html(
            model,
            skill_dir_by_name,
            relative_href_prefix="../",
            same_page_stages=True,
            board_class="aad-board-grid",
        ),
        encoding="utf-8",
    )
    return index_path


BOOTCAMP_KANBAN_SLIDES_START = "<!-- KANBAN_SLIDES -->"
BOOTCAMP_KANBAN_SLIDES_END = "<!-- /KANBAN_SLIDES -->"


def sync_bootcamp_part3_kanban(
    repo_root: Path,
    skill_dir_by_name: dict[str, str],
) -> bool:
    """Copy kanban kb-slides into bootcamp part3 — same pattern as part2 story board (vertical Reveal slides)."""
    bootcamp = _bootcamp_part3_path(repo_root)
    if not bootcamp.is_file():
        return False
    model = load_kanban_model(repo_root)
    prefix = BOOTCAMP_CATALOG_PREFIX
    slides_html = build_kanban_slides_deck_html(
        model,
        skill_dir_by_name,
        repo_root,
        relative_href_prefix=prefix,
        same_page_stages=True,
        link_column_heads=False,
    )
    slides_html = rewrite_bootcamp_catalog_links(slides_html, skill_dir_by_name)
    slides_html = slides_html.replace('href="../index.html"', f'href="{prefix}index.html"')
    slides_html = slides_html.replace(
        "../../../../agilebydesign-skills/catalog/", prefix
    )
    slides_html = slides_html.replace(
        '<section class="kb-slide" data-auto-animate',
        '<section class="kb-slide kb-slide--agentic-kanban" data-auto-animate',
    )
    text = _read_bootcamp_part3(bootcamp)
    start, end = BOOTCAMP_KANBAN_SLIDES_START, BOOTCAMP_KANBAN_SLIDES_END
    replacement = f"{start}\n{slides_html.rstrip()}\n{end}"
    if start in text and end in text:
        pattern = re.compile(re.escape(start) + r"[\s\S]*?" + re.escape(end))
        new_text, n = pattern.subn(replacement, text, count=1)
        if n == 0:
            return False
    else:
        iframe_block = re.compile(
            r"<!-- Delivery kanban:[\s\S]*?"
            r'<section class="kb-slide kb-slide--catalog-kanban"[\s\S]*?</section>\s*',
            re.MULTILINE,
        )
        new_text, n = iframe_block.subn(replacement + "\n\n", text, count=1)
        if n == 0:
            return False
    if new_text == text:
        return False
    bootcamp.write_text(new_text, encoding="utf-8")
    return True


def skill_dir_map_from_entries(skills: list) -> dict[str, str]:
    """Map YAML skill name and folder name → catalog skill dir_name."""
    out: dict[str, str] = {}
    for s in skills:
        out[s.name] = s.dir_name
        out[s.dir_name] = s.dir_name
    return out


def _bootcamp_part3_path(repo_root: Path) -> Path:
    return (
        repo_root.parent
        / "abd-works"
        / "abd-ai-augmented-bootcamp"
        / "slides"
        / "part3"
        / "part3.html"
    )


def _read_bootcamp_part3(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp1252")


def rewrite_bootcamp_catalog_links(text: str, skill_dir_by_name: dict[str, str]) -> str:
    """Replace localhost / legacy GitHub skill-tree URLs with catalog links."""
    prefix = BOOTCAMP_CATALOG_PREFIX
    text = text.replace("http://localhost:8787/abd-skills-catalog/", prefix)
    text = text.replace("http://localhost:8787/abd-skills-catalog", prefix.rstrip("/"))

    def _catalog_skill_href(leaf: str) -> str:
        leaf = GITHUB_SKILL_ALIASES.get(leaf, leaf)
        if leaf == "abd-skill-bulder":
            leaf = "abd-author-practice-skill"
        dir_name = skill_dir_by_name.get(leaf, leaf)
        return f"{prefix}skill/{quote(dir_name, safe='')}.html"

    text = re.sub(
        r'href="https://github\.com/abd-works/agilebydesign-skills/tree/main/skills(?:/[^/"]+)?/([^/"]+)"',
        lambda m: f'href="{_catalog_skill_href(m.group(1))}"',
        text,
    )
    text = text.replace("architecture-centric-delivery", "architecture-centric-engineering")
    text = text.replace("abd-clickable-prototype.html", "abd-interface-design.html")
    text = text.replace(">clickable-prototype</a>", ">interface-design</a>")
    text = text.replace("<!-- UXD: clickable-prototype -->", "<!-- UXD: interface-design (implementation pass) -->")
    return text


def patch_bootcamp_slide_files(repo_root: Path, skill_dir_by_name: dict[str, str]) -> list[str]:
    """Patch bootcamp slide HTML/MD (except part3 — catalog kanban iframe only)."""
    slides_root = (
        repo_root.parent / "abd-works" / "abd-ai-augmented-bootcamp" / "slides"
    )
    if not slides_root.is_dir():
        return []
    patched: list[str] = []
    part3 = _bootcamp_part3_path(repo_root)
    for path in sorted(slides_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".html", ".md"}:
            continue
        if path.resolve() == part3.resolve():
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            original = path.read_text(encoding="cp1252")
        updated = rewrite_bootcamp_catalog_links(original, skill_dir_by_name)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            patched.append(str(path.relative_to(slides_root)))
    return patched
