"""Build delivery kanban HTML from practices/kanban/reference/stages/*.md practice-skill tables."""

from __future__ import annotations

import html as html_mod
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

from catalog_repo_urls import (
    GITHUB_BLOB_MAIN,
    GITHUB_REPO,
    GITHUB_REPO_URL,
    LEGACY_GITHUB_REPO_SLUGS,
)
from catalog_supporting_groups import (
    FOUNDATIONAL_CROSSCUT_PLUGINS,
    SKILL_TO_SUPPORTING_GROUP,
    SUPPORTING_CROSSCUT_GROUPS,
)
from family_catalog import FAMILY_PACKAGES

BOOTCAMP_CATALOG_PREFIX = "../abd-skills-catalog/"

# GitHub tree leaf folder → catalog skill dir_name
GITHUB_SKILL_ALIASES: dict[str, str] = {
    "abd-opportunity-canvas": "abd-opportunity-generation",
    "abd-acceptance-criteria": "abd-story-acceptance-criteria",
    "abd-acceptance-test-driven-development": "abd-story-acceptance-test",
    "abd-specification-by-example": "abd-story-specification",
    "abd-information-architecture": "abd-ux-information-architecture",
    "abd-impact-mapping": "abd-ux-user-impact-map",
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
    "story-driven-delivery",
    "domain-driven-design",
    "user-experience-design",
    "architecture-centric-engineering",
)

# Delivery-system practice — supporting crosscut only; never a board row or practice-rail chip.
SUPPORTING_ONLY_PLUGIN_IDS: frozenset[str] = frozenset({"kanban"})

# Stage-folder skills (stages/*/…) — filtered via the "other practices" rail toggle.
SKILL_PAGE_OTHER_FAMILY = "other"

PLUGIN_CSS_CLASS: dict[str, str] = {
    "domain-driven-design": "aad-fam-ddd",
    "user-experience-design": "aad-fam-uxd",
    "story-driven-delivery": "aad-fam-sdd",
    "architecture-centric-engineering": "aad-fam-arc",
    "idea-shaping": "aad-fam-idea",
    "kanban": "aad-fam-delivery",
}

PLUGIN_PERSPECTIVE_KEY: dict[str, str] = {
    "story-driven-delivery": "sdd",
    "domain-driven-design": "ddd",
    "user-experience-design": "uxd",
    "architecture-centric-engineering": "arc",
}

PLUGIN_LABEL: dict[str, str] = {
    "domain-driven-design": "Domain-driven design",
    "user-experience-design": "User experience design",
    "story-driven-delivery": "Story-driven delivery",
    "architecture-centric-engineering": "Architecture-centric engineering",
    "idea-shaping": "Idea shaping",
    "kanban": "Kanban",
}

PLUGIN_TOOLTIP: dict[str, str] = {
    "story-driven-delivery": "Given/When/Then scenarios with real example data",
    "domain-driven-design": "Typed terms + relationships (a schema), not prose definitions",
    "user-experience-design": "Component spec with named states & rules, not a static picture",
    "architecture-centric-engineering": "Interface contracts / templates the engine can follow",
}

DELIVERY_AGENTS: tuple[str, ...] = (
    "kanban-lead",
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

# Optional skills — omitted from kanban catalog (still in stage docs when deferred).
KANBAN_OPTIONAL_SKILLS: frozenset[str] = frozenset(
    {
        "abd-thin-slicing",
    }
)

# Hide specific skills on the kanban grid only (stage markdown unchanged).
KANBAN_STAGE_EXCLUDED_SKILLS: dict[str, frozenset[str]] = {
    "discovery": frozenset({"abd-ubiquitous-language"}),
}

# Kanban tile label overrides (stage_id, skill_id) → display text.
KANBAN_SKILL_LABEL_OVERRIDES: dict[tuple[str, str], str] = {
    ("shaping", "abd-ux-user-impact-map"): "user impact map",
    ("shaping", "abd-story-mapping"): "story mapping outline",
    ("exploration", "abd-architecture-specification"): "architecture specification document",
    ("specification", "abd-architecture-specification"): "architecture specification template",
    ("engineering", "abd-ux-specification"): "UI code",
    ("engineering", "abd-architecture-code"): "architecture code",
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

# Repo ``stages/<folder>/`` → kanban column id (see ``abd-skills/stages/``).
STAGE_FOLDER_TO_KANBAN: dict[str, str] = {
    "shaping": "shaping",
    "idea-shaping": "shaping",
    "discovery": "discovery",
    "exploration": "exploration",
    "specification": "specification",
    "engineering": "engineering",
}

STAGE_SCOPE_META: dict[str, tuple[str, str, str, str]] = {
    "shaping": (
        "solution",
        "Whole solution",
        "wide / shallow",
        "outcomes · scope · boundaries",
    ),
    "discovery": (
        "increment",
        "Increment",
        "medium",
        "interactions · experience · structure",
    ),
    "exploration": (
        "sprint",
        "Sprint",
        "narrow / deeper",
        "behaviour · design · logic",
    ),
    "specification": (
        "story",
        "Story",
        "narrow / executable",
        "examples · design · templates",
    ),
    "engineering": (
        "story",
        "Story",
        "narrowest / deep",
        "tests · code · interface",
    ),
}

PERSPECTIVE_ROW_LABELS: tuple[tuple[str, str], ...] = (
    ("ddd", "Domain"),
    ("sdd", "Stories"),
    ("uxd", "UX"),
    ("arc", "Architecture"),
)

# Bottom outcome bullets → perspective color (domain, stories, UX, architecture).
OUTCOME_PERSPECTIVE_KEYS: tuple[str, ...] = ("ddd", "sdd", "uxd", "arc")

_CATALOG_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

STAGE_SKILL_FAMILY_CLASS = "aad-fam-stage"
FOUNDRY_HUB_STAGE_SKILL_ROWS = 3

_SKILL_NAME_FM_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)
_CATALOG_READY_FALSE_RE = re.compile(
    r"^catalog_ready:\s*(false|no|0|draft|not-ready|not_ready)\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def _kanban_include_skill(skill_id: str, *, stage_id: str | None = None, notes: str = "") -> bool:
    if skill_id in SKILL_TO_SUPPORTING_GROUP:
        return False
    if skill_id in KANBAN_EXCLUDED_SKILLS or skill_id in KANBAN_OPTIONAL_SKILLS:
        return False
    if "optional" in notes.lower():
        return False
    if stage_id and skill_id in KANBAN_STAGE_EXCLUDED_SKILLS.get(stage_id, frozenset()):
        return False
    if skill_id.endswith("-sync"):
        return False
    return skill_id != "story-graph-ops"

# Per-stage context-window depth — detail text appears under scale shapes (not duplicated below).
STAGE_CONTEXT: dict[str, tuple[str, str]] = {
    "shaping": ("wide / shallow", "Whole-solution view — outline map and boundaries."),
    "discovery": ("medium", "Full map, UX IA, architecture blueprint, thin slices."),
    "exploration": ("narrow / deeper", "Increment slice — AC, mockups, arch templates."),
    "specification": ("narrow / executable", "Domain model, scenarios, interface spec."),
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
    r"^\|\s*\d+[a-z]?\s*\|\s*\*\*(.+?)\*\*\s*\|\s*`([^`]+)`",
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
    stage_questions: dict[str, tuple[str, list[str]]] = field(default_factory=dict)
    stage_folder_skills: dict[str, list[str]] = field(default_factory=dict)


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


def _parse_stage_outcomes(text: str) -> tuple[str, list[str]]:
    """Return (headline, outcome bullets) from ## Outcomes section."""
    m = re.search(r"^## Outcomes\s*\n\n(.+?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not m:
        return "", []
    headline = ""
    bullets: list[str] = []
    for raw_line in m.group(1).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            bullets.append(line[2:].strip())
            continue
        if not bullets:
            headline = re.sub(r"\*\*(.+?)\*\*", r"\1", line).strip()
    if not bullets and headline and "·" in headline:
        parts = [p.strip() for p in headline.split("·") if p.strip()]
        if len(parts) > 1:
            return "", parts
    return headline, bullets


def _parse_stage_markdown(path: Path) -> tuple[str, list[StageSkill], tuple[str, list[str]]]:
    text = path.read_text(encoding="utf-8")
    purpose = ""
    m = re.search(r"^## Purpose\s*\n\n(.+?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    if m:
        purpose = re.sub(r"\s+", " ", m.group(1).strip())
    outcomes = _parse_stage_outcomes(text)
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
    return purpose, skills, outcomes


def _skill_id_from_skill_md(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8-sig", errors="replace")
    if _CATALOG_READY_FALSE_RE.search(text):
        return ""
    m = _SKILL_NAME_FM_RE.search(text)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return skill_md.parent.name


def _skill_ids_in_stage_folder(stage_folder: Path) -> list[str]:
    """Skill ids from ``stages/<folder>/`` packages (flat or ``skills/<name>/``)."""
    ids: list[str] = []
    seen: set[str] = set()
    for skill_md in sorted(stage_folder.rglob("SKILL.md")):
        rel = skill_md.relative_to(stage_folder)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if "test" in rel.parts[:-1]:
            continue
        skill_id = _skill_id_from_skill_md(skill_md)
        if not skill_id or skill_id in seen:
            continue
        seen.add(skill_id)
        ids.append(skill_id)
    return ids


def discover_stage_folder_skills(repo_root: Path) -> dict[str, list[str]]:
    """Map kanban stage id → skill ids under ``repo_root/stages/<folder>/``."""
    stages_root = repo_root / "stages"
    if not stages_root.is_dir():
        return {}
    by_stage: dict[str, list[str]] = {}
    for folder in sorted(stages_root.iterdir()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        kanban_stage = STAGE_FOLDER_TO_KANBAN.get(folder.name)
        if not kanban_stage:
            continue
        skill_ids = _skill_ids_in_stage_folder(folder)
        if not skill_ids:
            continue
        bucket = by_stage.setdefault(kanban_stage, [])
        for skill_id in skill_ids:
            if skill_id not in bucket:
                bucket.append(skill_id)
    return by_stage


def load_kanban_model(repo_root: Path) -> KanbanModel:
    stages_dir = repo_root / "practices" / "kanban" / "reference" / "stages"
    model = KanbanModel()
    for stage_id, title, num in STAGE_FILES:
        path = stages_dir / f"{stage_id}.md"
        if not path.is_file():
            continue
        purpose, skills, outcomes = _parse_stage_markdown(path)
        model.stages.append((stage_id, title, num, purpose))
        model.stage_purpose[stage_id] = purpose
        if outcomes[0] or outcomes[1]:
            model.stage_questions[stage_id] = outcomes
        model.matrix[stage_id] = {}
        for sk in skills:
            model.matrix[stage_id].setdefault(sk.plugin_id, []).append(sk)
    model.stage_folder_skills = discover_stage_folder_skills(repo_root)
    apply_kanban_display_model(model)
    return model


def apply_kanban_display_model(model: KanbanModel) -> None:
    """Kanban-only filters — does not alter stage source files."""
    for stage_id in model.matrix:
        for plugin_id in list(model.matrix[stage_id].keys()):
            model.matrix[stage_id][plugin_id] = [
                sk
                for sk in model.matrix[stage_id][plugin_id]
                if _kanban_include_skill(sk.skill_id, stage_id=stage_id, notes=sk.notes)
            ]
            if not model.matrix[stage_id][plugin_id]:
                del model.matrix[stage_id][plugin_id]


def _skill_href(
    skill_id: str,
    skill_dir_by_name: dict[str, str],
    *,
    relative: str,
    sibling_pages: bool = False,
    stage_id: str | None = None,
) -> str:
    dir_name = skill_dir_by_name.get(skill_id, skill_id)
    if sibling_pages:
        base = f"{quote(dir_name, safe='')}.html"
        if stage_id:
            return f"{base}?stage={quote(stage_id, safe='')}"
        return base
    return f"{relative}skill/{quote(dir_name, safe='')}.html"


def _agent_href(agent_dir: str, *, relative: str) -> str:
    return f"{relative}agent/{quote(agent_dir, safe='')}.html"


def _plugin_href(plugin_id: str, *, relative: str) -> str:
    return f"{relative}plugin/{quote(plugin_id, safe='')}.html"


def _plugin_id_for_pkg_rel(pkg_rel_posix: str) -> str:
    norm = pkg_rel_posix.replace("\\", "/").strip("/")
    if not norm:
        return ""
    for fam_id, fam_path in FAMILY_PACKAGES.items():
        fp = fam_path.rstrip("/")
        if norm == fp or norm.startswith(fp + "/"):
            return fam_id
    return ""


def plugin_first_skill_href_map(
    skills: list,
    skill_dir_by_name: dict[str, str],
    *,
    relative: str = "",
    sibling_pages: bool = False,
) -> dict[str, str]:
    """Map plugin id → first practice-tier skill detail page (same target as skills listing)."""
    by_plugin: dict[str, list] = {}
    for s in skills:
        if getattr(s, "garden_tier", "") != "practice":
            continue
        pid = _plugin_id_for_pkg_rel(getattr(s, "pkg_rel_posix", ""))
        if pid:
            by_plugin.setdefault(pid, []).append(s)
    out: dict[str, str] = {}
    for pid, entries in by_plugin.items():
        first = min(
            entries,
            key=lambda e: (getattr(e, "garden_order", 9999), getattr(e, "dir_name", e.name)),
        )
        if sibling_pages:
            out[pid] = _skill_page_sibling_href(first.name, skill_dir_by_name)
        else:
            out[pid] = _skill_href(first.name, skill_dir_by_name, relative=relative)
    return out


def _family_nav_href(
    plugin_id: str,
    *,
    relative: str,
    plugin_first_skill_hrefs: dict[str, str] | None,
) -> str:
    """Family/plugin label → first skill page when available (matches skills grid), else plugin page."""
    if plugin_first_skill_hrefs and plugin_id in plugin_first_skill_hrefs:
        return plugin_first_skill_hrefs[plugin_id]
    return _plugin_href(plugin_id, relative=relative)


def _skill_page_sibling_href(skill_id: str, skill_dir_by_name: dict[str, str]) -> str:
    """Href between skill detail pages in catalog/skill/."""
    dir_name = skill_dir_by_name.get(skill_id) or GITHUB_SKILL_ALIASES.get(
        skill_id, skill_id
    )
    return f"{quote(dir_name, safe='')}.html"


def _catalog_skill_href_as_sibling(href: str) -> str:
    """Turn catalog-root skill/foo.html into sibling foo.html for skill detail pages."""
    if href.startswith("skill/"):
        return href[6:]
    return href


def plugin_stage_skill_href_map(
    model: KanbanModel,
    skill_dir_by_name: dict[str, str],
    *,
    sibling_pages: bool = False,
    relative: str = "",
) -> dict[str, dict[str, str]]:
    """Map each practice family to the first kanban skill href per delivery stage."""
    out: dict[str, dict[str, str]] = {}
    for stage_id, _title, _num, _purpose in model.stages:
        for plugin_id in PLUGIN_ROW_ORDER:
            if stage_id in out.get(plugin_id, {}):
                continue
            for sk in model.matrix.get(stage_id, {}).get(plugin_id, []):
                if not _kanban_include_skill(
                    sk.skill_id, stage_id=stage_id, notes=sk.notes
                ):
                    continue
                href = (
                    _skill_page_sibling_href(sk.skill_id, skill_dir_by_name)
                    if sibling_pages
                    else _skill_href(sk.skill_id, skill_dir_by_name, relative=relative)
                )
                out.setdefault(plugin_id, {})[stage_id] = href
                break
    return out


def other_practices_first_skill_href(
    model: KanbanModel,
    skill_dir_by_name: dict[str, str],
    *,
    relative: str = "",
    sibling_pages: bool = False,
) -> str:
    """First stage-folder skill page — hub other-practices label target."""
    for stage_id, _title, _num, _purpose in model.stages:
        for skill_id in model.stage_folder_skills.get(stage_id, []):
            if not _kanban_include_skill(skill_id, stage_id=stage_id):
                continue
            if sibling_pages:
                return _skill_page_sibling_href(skill_id, skill_dir_by_name)
            return _skill_href(skill_id, skill_dir_by_name, relative=relative)
    return "#"


def skill_in_stage_folder(
    model: KanbanModel,
    *,
    current_skill_id: str,
    current_dir_name: str = "",
    skill_dir_by_name: dict[str, str],
) -> bool:
    """True when the skill lives under stages/*/ (other-practices row on the board)."""

    def matches(skill_id: str) -> bool:
        dir_name = skill_dir_by_name.get(skill_id) or GITHUB_SKILL_ALIASES.get(
            skill_id, skill_id
        )
        return skill_id == current_skill_id or dir_name == current_dir_name

    for skill_ids in model.stage_folder_skills.values():
        for skill_id in skill_ids:
            if matches(skill_id):
                return True
    return False


def resolve_skill_page_kanban_family(
    model: KanbanModel,
    *,
    current_skill_id: str,
    current_dir_name: str = "",
    skill_dir_by_name: dict[str, str],
    plugin_id_from_path: str,
) -> str:
    """Family filter id for a skill page kanban embed — core practice or other."""
    if skill_in_stage_folder(
        model,
        current_skill_id=current_skill_id,
        current_dir_name=current_dir_name,
        skill_dir_by_name=skill_dir_by_name,
    ):
        return SKILL_PAGE_OTHER_FAMILY
    if (
        plugin_id_from_path in SUPPORTING_ONLY_PLUGIN_IDS
        or SKILL_TO_SUPPORTING_GROUP.get(current_skill_id) in SUPPORTING_ONLY_PLUGIN_IDS
    ):
        return "kanban"
    if plugin_id_from_path in PLUGIN_ROW_ORDER:
        return plugin_id_from_path
    return ""


def resolve_skill_stage_id(
    model: KanbanModel,
    plugin_id: str,
    *,
    current_skill_id: str,
    current_dir_name: str,
    skill_dir_by_name: dict[str, str],
) -> str:
    """Delivery stage for the open skill — first kanban column that contains it."""

    def matches(skill_id: str) -> bool:
        dir_name = skill_dir_by_name.get(skill_id) or GITHUB_SKILL_ALIASES.get(
            skill_id, skill_id
        )
        return skill_id == current_skill_id or dir_name == current_dir_name

    if plugin_id == SKILL_PAGE_OTHER_FAMILY:
        for stage_id, _title, _num, _purpose in model.stages:
            for skill_id in model.stage_folder_skills.get(stage_id, []):
                if matches(skill_id):
                    return stage_id
        return model.stages[0][0]

    for stage_id, _title, _num, _purpose in model.stages:
        for sk in model.matrix.get(stage_id, {}).get(plugin_id, []):
            if matches(sk.skill_id):
                return stage_id
    return model.stages[0][0]


def _family_nav_href_at_stage(
    plugin_id: str,
    stage_id: str,
    *,
    plugin_stage_skill_hrefs: dict[str, dict[str, str]] | None,
    plugin_first_skill_hrefs: dict[str, str] | None,
    relative: str = "",
    sibling_pages: bool = False,
) -> str:
    """Family link at a specific delivery stage, with first-skill fallback."""
    if plugin_stage_skill_hrefs:
        per_stage = plugin_stage_skill_hrefs.get(plugin_id, {})
        if stage_id in per_stage:
            return per_stage[stage_id]
    if plugin_first_skill_hrefs and plugin_id in plugin_first_skill_hrefs:
        href = plugin_first_skill_hrefs[plugin_id]
        return _catalog_skill_href_as_sibling(href) if sibling_pages else href
    return _plugin_href(plugin_id, relative=relative)


def build_skill_page_practice_sidebar_html(
    *,
    current_plugin_id: str,
    current_stage_id: str,
    plugin_stage_skill_hrefs: dict[str, dict[str, str]] | None = None,
    plugin_first_skill_hrefs: dict[str, str] | None = None,
    relative_href_prefix: str = "",
    sibling_pages: bool = False,
) -> str:
    """Left practice-family rail (hub style) — each link keeps the current delivery stage."""
    cards: list[str] = []
    for plugin_id in PLUGIN_ROW_ORDER:
        css = PLUGIN_CSS_CLASS.get(plugin_id, "")
        key = PLUGIN_PERSPECTIVE_KEY.get(plugin_id, "")
        tooltip = PLUGIN_TOOLTIP.get(plugin_id, "")
        href = _family_nav_href_at_stage(
            plugin_id,
            current_stage_id,
            plugin_stage_skill_hrefs=plugin_stage_skill_hrefs,
            plugin_first_skill_hrefs=plugin_first_skill_hrefs,
            relative=relative_href_prefix,
            sibling_pages=sibling_pages,
        )
        inner = _skill_ticket_inner_html(plugin_id, tooltip)
        current_cls = " kb-ticket--current" if plugin_id == current_plugin_id else ""
        tooltip_cls = " has-skill-tooltip" if tooltip else ""
        cards.append(
            f'      <a class="foundry-practice-col__card foundry-perspective-label--{key} '
            f"aad-skill {css}{current_cls}{tooltip_cls}\" href=\"{_h(href)}\">{inner}</a>"
        )
    return (
        '    <div class="skill-kanban-nav__practice-col" aria-label="Practice families">\n'
        + "\n".join(cards)
        + "\n    </div>"
    )


def build_kanban_legend_html(
    *,
    relative_href_prefix: str = "../",
    indent: str = "      ",
    plugin_first_skill_hrefs: dict[str, str] | None = None,
) -> str:
    """Practice plugin key cards (same style as skill tickets); delivery omitted — in crosscut."""
    cards: list[str] = []
    for plugin_id in PLUGIN_ROW_ORDER:
        css = PLUGIN_CSS_CLASS.get(plugin_id, "")
        href = _family_nav_href(
            plugin_id,
            relative=relative_href_prefix,
            plugin_first_skill_hrefs=plugin_first_skill_hrefs,
        )
        cards.append(
            f'<a class="kb-ticket aad-skill {css}" '
            f'href="{_h(href)}">{_h(plugin_id)}</a>'
        )
    block = (
        '<div class="kanban-legend-row">\n'
        '  <div class="kanban-legend-heading">Practice</div>\n'
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
    return f"{relative}index.html{anchor}"


def load_catalog_embed_kanban_css(repo_root: Path, template_dir: Path) -> str:
    """CSS for the delivery kanban embedded on catalog/index.html."""
    embed_css = (template_dir / "catalog-kanban-embed.css").read_text(encoding="utf-8")
    return (
        load_bootcamp_abd_works_css(repo_root)
        + "\n"
        + load_bootcamp_kanban_base_css(repo_root)
        + "\n"
        + (template_dir / "kanban-layout.css").read_text(encoding="utf-8")
        + "\n"
        + embed_css
        + "\n"
        + (template_dir / "catalog-foundry-interface.css").read_text(encoding="utf-8")
    )


def _load_foundry_cdd_panel_html() -> str:
    return (_CATALOG_TEMPLATE_DIR / "catalog-foundry-cdd-panel.html").read_text(
        encoding="utf-8"
    )


def _foundry_col_head_html(stage_id: str, title: str, num: str | int, href: str) -> str:
    shape_key, scope_name, width_label, bullets = STAGE_SCOPE_META[stage_id]
    scope_detail = f"{width_label} · {bullets}"
    tooltip_label = f"{scope_name}. {width_label}. {bullets.replace(' · ', ', ')}"
    return (
        f'      <button type="button" class="kb-col-head kb-col-head--toggle foundry-stage-toggle" '
        f'data-stage="{stage_id}" data-id="head-{stage_id}" aria-pressed="false">\n'
        f'        <div class="kb-col-head-row">\n'
        f'          <span class="kb-col-scope-shape-wrap">\n'
        f'            <span class="kb-col-scope-shape kb-col-scope-shape--{shape_key}" '
        f'title="{_h(scope_name + " — " + width_label + " — " + bullets)}" '
        f'aria-label="{_h(tooltip_label)}"></span>\n'
        f'            <span class="kb-col-shape-tooltip" role="tooltip">\n'
        f'              <span class="kb-col-shape-tooltip__name">{_h(scope_name)}</span>\n'
        f'              <span class="kb-col-shape-tooltip__width">{_h(width_label)}</span>\n'
        f'              <span class="kb-col-shape-tooltip__bullets">{_h(bullets)}</span>\n'
        f"            </span>\n"
        f"          </span>\n"
        f'          <span class="kb-col-head-title"><span>{_h(title)}</span>'
        f'<span class="kb-col-num">{num}</span></span>\n'
        f"        </div>\n"
        f"      </button>\n"
    )


def _skill_nav_col_head_html(
    stage_id: str,
    title: str,
    num: str | int,
    *,
    href: str = "",
    is_active: bool = False,
) -> str:
    """Kanban column head for skill detail nav — links to the stage skill when href is set."""
    shape_key, scope_name, width_label, bullets = STAGE_SCOPE_META[stage_id]
    tooltip_label = f"{scope_name}. {width_label}. {bullets.replace(' · ', ', ')}"
    active_cls = " kb-col-head--current" if is_active else ""
    inner = (
        f'          <div class="kb-col-head-row">\n'
        f'            <span class="kb-col-scope-shape kb-col-scope-shape--{shape_key}" '
        f'aria-hidden="true"></span>\n'
        f'            <span class="kb-col-head-title"><span>{_h(title)}</span>'
        f'<span class="kb-col-num">{num}</span></span>\n'
        f"          </div>\n"
    )
    if href:
        return (
            f'        <a class="kb-col-head kb-col-head--link foundry-stage-toggle{active_cls}" '
            f'data-stage="{stage_id}" href="{_h(href)}" title="{_h(tooltip_label)}" '
            f'aria-pressed="false">\n'
            f"{inner}"
            f"        </a>\n"
        )
    return (
        f'        <div class="kb-col-head kb-col-head--static" data-stage="{stage_id}" '
        f'title="{_h(tooltip_label)}">\n'
        f"{inner}"
        f"        </div>\n"
    )


def _skill_in_family(
    skill_id: str,
    family_skill_ids: frozenset[str],
    skill_dir_by_name: dict[str, str],
) -> bool:
    if skill_id in family_skill_ids:
        return True
    dir_name = skill_dir_by_name.get(skill_id)
    if dir_name and dir_name in family_skill_ids:
        return True
    alias = GITHUB_SKILL_ALIASES.get(skill_id)
    if alias and alias in family_skill_ids:
        return True
    return bool(alias and skill_dir_by_name.get(alias, "") in family_skill_ids)


def _skill_nav_ticket_html(
    *,
    skill_id: str,
    stage_id: str,
    skill_dir_by_name: dict[str, str],
    family_css: str,
    is_active: bool = False,
    notes: str = "",
    skill_purpose_by_name: dict[str, str] | None = None,
) -> str:
    dir_name = skill_dir_by_name.get(skill_id) or GITHUB_SKILL_ALIASES.get(skill_id, skill_id)
    href = f"{quote(dir_name, safe='')}.html"
    label = _skill_label(skill_id, stage_id)
    purpose = _skill_purpose_text(skill_id, skill_purpose_by_name, notes=notes)
    title_attr = f' title="{_h(purpose)}"' if purpose else ""
    active_cls = " kb-ticket--current" if is_active else ""
    return (
        f'          <a class="kb-ticket aad-skill {family_css}{active_cls}" '
        f'href="{_h(href)}"{title_attr}>{_h(label)}</a>'
    )


def build_skill_family_kanban_nav_html(
    model: KanbanModel,
    plugin_id: str,
    *,
    family_skill_ids: frozenset[str],
    skill_dir_by_name: dict[str, str],
    current_skill_id: str,
    current_dir_name: str = "",
    skill_purpose_by_name: dict[str, str] | None = None,
    plugin_stage_skill_hrefs: dict[str, dict[str, str]] | None = None,
    plugin_first_skill_hrefs: dict[str, str] | None = None,
) -> str:
    """Kanban column nav for skill pages — practice sidebar + stage headings."""
    if not plugin_id or plugin_id not in PLUGIN_ROW_ORDER:
        return ""

    family_css = PLUGIN_CSS_CLASS.get(plugin_id, STAGE_SKILL_FAMILY_CLASS)
    cols: list[str] = []
    current_marked = False

    def append_ticket(
        *,
        skill_id: str,
        stage_id: str,
        notes: str = "",
    ) -> None:
        nonlocal current_marked, first_href, col_is_active
        dir_name = skill_dir_by_name.get(skill_id) or GITHUB_SKILL_ALIASES.get(
            skill_id, skill_id
        )
        if not first_href:
            first_href = f"{quote(dir_name, safe='')}.html"
        matches_current = (
            skill_id == current_skill_id or dir_name == current_dir_name
        )
        is_active = matches_current and not current_marked
        if is_active:
            current_marked = True
            col_is_active = True
        tickets.append(
            _skill_nav_ticket_html(
                skill_id=skill_id,
                stage_id=stage_id,
                skill_dir_by_name=skill_dir_by_name,
                family_css=family_css,
                is_active=is_active,
                notes=notes,
                skill_purpose_by_name=skill_purpose_by_name,
            )
        )

    for stage_id, title, num, _purpose in model.stages:
        tickets: list[str] = []
        seen_in_col: set[str] = set()
        first_href = ""
        col_is_active = False

        for sk in model.matrix.get(stage_id, {}).get(plugin_id, []):
            if not _kanban_include_skill(sk.skill_id, stage_id=stage_id, notes=sk.notes):
                continue
            if not _skill_in_family(sk.skill_id, family_skill_ids, skill_dir_by_name):
                continue
            if sk.skill_id in seen_in_col:
                continue
            seen_in_col.add(sk.skill_id)
            append_ticket(skill_id=sk.skill_id, stage_id=stage_id, notes=sk.notes)

        if plugin_id == "idea-shaping" and stage_id == "shaping":
            for skill_id in model.stage_folder_skills.get(stage_id, []):
                if skill_id in seen_in_col:
                    continue
                if not _kanban_include_skill(skill_id, stage_id=stage_id):
                    continue
                if not _skill_in_family(skill_id, family_skill_ids, skill_dir_by_name):
                    continue
                seen_in_col.add(skill_id)
                append_ticket(skill_id=skill_id, stage_id=stage_id)

        if not tickets:
            continue

        col_head = _skill_nav_col_head_html(
            stage_id, title, num, href=first_href, is_active=col_is_active
        )
        cols.append(
            f'      <div class="skill-kanban-nav__col" data-stage="{stage_id}">\n'
            f"{col_head}"
            f'        <div class="skill-kanban-nav__tickets">\n'
            + "\n".join(tickets)
            + "\n        </div>\n      </div>"
        )

    if not cols:
        return ""

    current_stage_id = resolve_skill_stage_id(
        model,
        plugin_id,
        current_skill_id=current_skill_id,
        current_dir_name=current_dir_name,
        skill_dir_by_name=skill_dir_by_name,
    )
    sidebar = build_skill_page_practice_sidebar_html(
        current_plugin_id=plugin_id,
        current_stage_id=current_stage_id,
        plugin_stage_skill_hrefs=plugin_stage_skill_hrefs,
        plugin_first_skill_hrefs=plugin_first_skill_hrefs,
        sibling_pages=True,
    )
    col_count = len(cols)
    return (
        '<div class="skill-kanban-nav">\n'
        '<div class="wrap">\n'
        '<div class="skill-kanban-nav__board">\n'
        f"{sidebar}\n"
        f'<nav class="skill-kanban-nav__stages" style="--skill-kanban-cols: {col_count}" '
        'aria-label="Practice stages">\n'
        + "\n".join(cols)
        + "\n</nav>\n</div>\n</div>\n</div>\n"
    )


def _foundry_skills_toggle_html() -> str:
    return (
        '      <button type="button" class="foundry-skills-toggle" id="foundry-skills-toggle" '
        'aria-expanded="false" aria-label="Show or hide practice skills across columns">'
        '<span class="foundry-skills-toggle__label">Skills</span>'
        '<span class="foundry-skills-toggle__icon" aria-hidden="true">'
        '<span class="foundry-skills-toggle__bar foundry-skills-toggle__bar--h"></span>'
        '<span class="foundry-skills-toggle__bar foundry-skills-toggle__bar--v"></span>'
        '</span>'
        "</button>\n"
    )


def _foundry_other_practices_col_html(
    *, skill_page_mode: bool = False, href: str = "", selected: bool = False
) -> str:
    """Left-rail toggle for stage-folder skills + foundations. Always a button."""
    inner = '<span class="kb-skill-tooltip-wrap">other practices</span>'
    selected_cls = " is-selected" if selected else ""
    pressed = "true" if selected else "false"
    return (
        '      <div class="foundry-practice-col__other-practices" aria-label="Other practices">\n'
        f'        <button type="button" class="kb-ticket aad-skill aad-fam-other '
        f"foundry-practice-col__card foundry-perspective-label foundry-family-toggle "
        f"foundry-perspective-label--other{selected_cls}\" data-family=\"other\" "
        f'data-perspective="other" aria-pressed="{pressed}">{inner}</button>\n'
        "      </div>\n"
    )


def build_foundry_practice_col_html(
    *,
    relative_href_prefix: str = "",
    plugin_first_skill_hrefs: dict[str, str] | None = None,
    current_plugin_id: str | None = None,
    skill_page_active_family: str | None = None,
    plugin_filter: str | None = None,
    include_stage_spacer: bool = True,
    skill_page_mode: bool = False,
    other_practices_href: str = "",
) -> str:
    """Practice rail — always buttons with data-family so the same JS filter works on hub and skill pages."""
    active_family = skill_page_active_family if skill_page_active_family is not None else current_plugin_id
    cards: list[str] = []
    for plugin_id in PLUGIN_ROW_ORDER:
        if plugin_filter and plugin_id != plugin_filter:
            continue
        css = PLUGIN_CSS_CLASS.get(plugin_id, "")
        key = PLUGIN_PERSPECTIVE_KEY[plugin_id]
        tooltip = PLUGIN_TOOLTIP.get(plugin_id, "")
        tooltip_cls = " has-skill-tooltip" if tooltip else ""
        current_cls = " kb-ticket--current" if plugin_id == current_plugin_id else ""
        selected_cls = " is-selected" if plugin_id == active_family else ""
        pressed = "true" if plugin_id == active_family else "false"
        inner = _skill_ticket_inner_html(plugin_id, tooltip)
        cards.append(
            f'      <button type="button" class="kb-ticket aad-skill {css} '
            f"foundry-practice-col__card foundry-perspective-label foundry-family-toggle "
            f"foundry-perspective-label--{key}{tooltip_cls}{current_cls}{selected_cls}\" "
            f'data-family="{_h(plugin_id)}" data-perspective="{key}" '
            f'aria-pressed="{pressed}">{inner}</button>'
        )
    toggle = _foundry_skills_toggle_html()
    stage_gap_html = (
        '      <div class="foundry-practice-col__stage-spacer aad-stage-skills-gap" '
        'aria-hidden="true"></div>\n'
        if include_stage_spacer
        else ""
    )
    return (
        '    <div class="foundry-practice-col" aria-label="Practice plugins">\n'
        f"{toggle}"
        + "\n".join(cards)
        + "\n"
        + stage_gap_html
        + _foundry_other_practices_col_html(
            selected=active_family == SKILL_PAGE_OTHER_FAMILY,
        )
        + "    </div>"
    )


def build_catalog_foundry_kanban_embed_html(
    model: KanbanModel,
    skill_dir_by_name: dict[str, str],
    *,
    relative_href_prefix: str = "",
    sibling_skill_pages: bool = False,
    same_page_stages: bool = True,
    active_stage_id: str | None = None,
    current_skill_id: str | None = None,
    current_dir_name: str = "",
    current_plugin_id: str | None = None,
    initial_family: str | None = None,
    skill_page_active_family: str | None = None,
    skill_purpose_by_name: dict[str, str] | None = None,
    plugin_first_skill_hrefs: dict[str, str] | None = None,
    include_stage_folder_skills: bool = False,
    initial_visible_family: str | None = None,
    settling_class: bool = False,
) -> str:
    """Foundry kanban embed — shared generator for hub and skill pages."""
    cols = build_kanban_board_html(
        model,
        skill_dir_by_name,
        relative_href_prefix=relative_href_prefix,
        same_page_stages=same_page_stages,
        active_stage_id=active_stage_id,
        link_column_heads=True,
        board_class="aad-board-grid aad-board-grid--catalog",
        foundry_hub=True,
        skill_purpose_by_name=skill_purpose_by_name,
        sibling_skill_pages=sibling_skill_pages,
        current_skill_id=current_skill_id,
        current_dir_name=current_dir_name,
        include_stage_folder_skills=include_stage_folder_skills,
        initial_visible_family=initial_visible_family,
    )
    practice_col = build_foundry_practice_col_html(
        relative_href_prefix=relative_href_prefix,
        plugin_first_skill_hrefs=plugin_first_skill_hrefs,
        current_plugin_id=current_plugin_id,
        skill_page_active_family=skill_page_active_family,
        other_practices_href=other_practices_first_skill_href(
            model,
            skill_dir_by_name,
            relative=relative_href_prefix,
            sibling_pages=sibling_skill_pages,
        ),
    )
    cdd = textwrap.indent(_load_foundry_cdd_panel_html().strip(), "    ")
    questions = build_stage_questions_row_html(
        model,
        active_stage_id=active_stage_id,
        foundry_grid=True,
    )
    crosscut = build_crosscut_html(
        skill_dir_by_name,
        relative_href_prefix=relative_href_prefix,
        skill_purpose_by_name=skill_purpose_by_name,
        plugin_first_skill_hrefs=plugin_first_skill_hrefs,
        sibling_skill_pages=sibling_skill_pages,
        foundry_ticket=True,
    )
    after_parts: list[str] = []
    if questions.strip():
        after_parts.append(questions.strip())
    if crosscut.strip():
        after_parts.append(
            '<div class="foundry-skills-extra">\n'
            '  <div class="foundry-skills-extra__inner">\n'
            + textwrap.indent(crosscut.strip(), "    ")
            + "\n  </div>\n"
            "</div>"
        )
    after_board = "\n".join(after_parts)
    body = (
        '  <div class="foundry-travel-ring" id="travel-ring" aria-hidden="true"></div>\n'
        f"{cdd}\n"
        '  <div class="foundry-board-grid" id="board">\n'
        f"{practice_col}\n"
        f"{textwrap.indent(cols.strip(), '    ')}\n"
        "  </div>"
    )
    if after_board:
        body += "\n" + textwrap.indent(after_board, "    ")
    data_attrs: list[str] = []
    if initial_family:
        data_attrs.append(f'data-initial-family="{_h(initial_family)}"')
    if active_stage_id:
        data_attrs.append(f'data-initial-stage="{_h(active_stage_id)}"')
    data_attr_str = (" " + " ".join(data_attrs)) if data_attrs else ""
    surface_classes = "foundry-kanban-surface foundry-skills-collapsed catalog-kanban-embed"
    if settling_class:
        surface_classes += " foundry-skill-nav-settling"
    return (
        '<div class="wrap">\n'
        '<div class="foundry-kanban-shell" id="kanban-shell">\n'
        f'<section class="{surface_classes}" id="catalog-kanban"{data_attr_str} '
        'aria-label="Delivery kanban">\n'
        f"{body}\n"
        "</section>\n"
        "</div>\n"
        "</div>"
    )


def build_catalog_hub_kanban_embed_html(
    model: KanbanModel,
    skill_dir_by_name: dict[str, str],
    *,
    relative_href_prefix: str = "",
    sibling_skill_pages: bool = False,
    same_page_stages: bool = True,
    active_stage_id: str | None = None,
    current_skill_id: str | None = None,
    current_dir_name: str = "",
    current_plugin_id: str | None = None,
    skill_purpose_by_name: dict[str, str] | None = None,
    plugin_first_skill_hrefs: dict[str, str] | None = None,
) -> str:
    """Foundry hub kanban — delegates to shared foundry embed generator."""
    return build_catalog_foundry_kanban_embed_html(
        model,
        skill_dir_by_name,
        relative_href_prefix=relative_href_prefix,
        sibling_skill_pages=sibling_skill_pages,
        same_page_stages=same_page_stages,
        active_stage_id=active_stage_id,
        current_skill_id=current_skill_id,
        current_dir_name=current_dir_name,
        current_plugin_id=current_plugin_id,
        skill_purpose_by_name=skill_purpose_by_name,
        plugin_first_skill_hrefs=plugin_first_skill_hrefs,
        include_stage_folder_skills=True,
    )


def build_catalog_supporting_only_kanban_embed_html(
    skill_dir_by_name: dict[str, str],
    *,
    current_skill_id: str,
    skill_purpose_by_name: dict[str, str] | None = None,
    plugin_first_skill_hrefs: dict[str, str] | None = None,
) -> str:
    """Supporting-section-only embed for delivery-system (kanban) practice skills."""
    crosscut = build_crosscut_html(
        skill_dir_by_name,
        relative_href_prefix="../",
        skill_purpose_by_name=skill_purpose_by_name,
        plugin_first_skill_hrefs=plugin_first_skill_hrefs,
        sibling_skill_pages=True,
        foundry_ticket=True,
    )
    if not crosscut.strip():
        return ""
    body = (
        '<div class="foundry-skills-extra foundry-skills-extra--always">\n'
        '  <div class="foundry-skills-extra__inner">\n'
        + textwrap.indent(crosscut.strip(), "    ")
        + "\n  </div>\n"
        "</div>"
    )
    return (
        '<div class="wrap">\n'
        '<div class="foundry-kanban-shell" id="kanban-shell">\n'
        '<section class="foundry-kanban-surface foundry-kanban-surface--supporting-only '
        'foundry-skills-expanded catalog-kanban-embed" '
        'id="catalog-kanban" '
        'data-initial-family="kanban" '
        'aria-label="Delivery kanban supporting skills">\n'
        f"{body}\n"
        "</section>\n"
        "</div>\n"
        "</div>"
    )


def build_catalog_skill_page_kanban_embed_html(
    model: KanbanModel,
    skill_dir_by_name: dict[str, str],
    *,
    plugin_id: str,
    current_skill_id: str,
    current_dir_name: str = "",
    skill_purpose_by_name: dict[str, str] | None = None,
    plugin_first_skill_hrefs: dict[str, str] | None = None,
) -> str:
    """Foundry kanban on skill pages — full board; tickets filtered via family/column toggles."""
    if not plugin_id:
        return ""
    if plugin_id in SUPPORTING_ONLY_PLUGIN_IDS:
        return build_catalog_supporting_only_kanban_embed_html(
            skill_dir_by_name,
            current_skill_id=current_skill_id,
            skill_purpose_by_name=skill_purpose_by_name,
            plugin_first_skill_hrefs=plugin_first_skill_hrefs,
        )
    if plugin_id not in PLUGIN_ROW_ORDER and plugin_id != SKILL_PAGE_OTHER_FAMILY:
        return ""

    active_stage_id = resolve_skill_stage_id(
        model,
        plugin_id,
        current_skill_id=current_skill_id,
        current_dir_name=current_dir_name,
        skill_dir_by_name=skill_dir_by_name,
    )
    return build_catalog_foundry_kanban_embed_html(
        model,
        skill_dir_by_name,
        relative_href_prefix="../",
        sibling_skill_pages=True,
        same_page_stages=False,
        active_stage_id=active_stage_id,
        current_skill_id=current_skill_id,
        current_dir_name=current_dir_name,
        current_plugin_id=plugin_id if plugin_id in PLUGIN_ROW_ORDER else None,
        initial_family=plugin_id,
        skill_page_active_family=plugin_id,
        skill_purpose_by_name=skill_purpose_by_name,
        plugin_first_skill_hrefs=plugin_first_skill_hrefs,
        include_stage_folder_skills=True,
        initial_visible_family=plugin_id,
        settling_class=True,
    )


def build_overview_header_html(*, relative_href_prefix: str = "../") -> str:
    """Overview slide header — matches bootcamp Context Perspectives kanban."""
    rel = relative_href_prefix
    return (
        '<div class="kb-header">\n'
        "  <div>\n"
        "    <h2>Context can be refined to greater degrees of fidelity "
        "across each perspective</h2>\n"
        "  </div>\n"
        '  <div class="kb-header-right">\n'
        '    <div class="kb-skill-links">\n'
        f'      <a href="{_h(rel)}index.html" class="kb-skill-pill">skill library</a>\n'
        f'      <a href="{GITHUB_REPO_URL}" '
        'class="kb-skill-gh">GitHub</a>\n'
        "    </div>\n"
        "  </div>\n"
        "</div>"
    )


def build_stage_questions_row_html(
    model: KanbanModel,
    *,
    active_stage_id: str | None = None,
    foundry_grid: bool = False,
) -> str:
    """Five-column question grid aligned under kanban stage columns (bootcamp part3)."""
    cells: list[str] = []
    if foundry_grid:
        cells.append('  <div class="kanban-stage-questions__spacer" aria-hidden="true"></div>')
    for stage_id, _title, _num, _purpose in model.stages:
        headline, bullets = model.stage_questions.get(stage_id, ("", []))
        active_cls = " is-active" if active_stage_id == stage_id else ""
        if foundry_grid:
            rows = bullets if bullets else ([headline] if headline else [])
            bullet_html = "".join(
                f'      <li class="kanban-stage-questions__item">{_h(q)}</li>\n'
                for q in rows
            )
        else:
            bullet_html = "".join(
                f'      <li class="kanban-stage-questions__item '
                f'kanban-stage-questions__item--{_h(key)}">{_h(q)}</li>\n'
                for key, q in zip(OUTCOME_PERSPECTIVE_KEYS, bullets, strict=False)
            )
        headline_html = (
            f'    <div class="kanban-stage-questions__headline">'
            f"<strong>{_h(headline)}</strong></div>\n"
            if headline and not foundry_grid
            else ""
        )
        cells.append(
            f'  <div class="kanban-stage-questions__cell{active_cls}" '
            f'data-stage="{stage_id}">\n'
            f"{headline_html}"
            f'    <ul class="kanban-stage-questions__list">\n'
            f"{bullet_html}"
            f"    </ul>\n"
            f"  </div>"
        )
    if not any(model.stage_questions.values()):
        return ""
    grid_class = " kanban-stage-questions--foundry" if foundry_grid else ""
    return (
        f'<div class="kanban-stage-questions{grid_class}" data-id="stage-questions">\n'
        + "\n".join(cells)
        + "\n</div>"
    )


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


_CATALOG_FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Inter:wght@400;500;600;700;800&"
    "family=JetBrains+Mono:wght@400;500;600;700&display=swap');"
)


def load_bootcamp_abd_works_css(repo_root: Path) -> str:
    """Full bootcamp abd-works.css — same stylesheet as index.html."""
    css_path = _bootcamp_abd_works_css_path(repo_root)
    if not css_path.is_file():
        return ""
    raw = css_path.read_text(encoding="utf-8")
    raw = re.sub(
        r"@import\s+url\(['\"]?/commons/abd-fonts\.css['\"]?\)\s*;",
        _CATALOG_FONT_IMPORT,
        raw,
    )
    raw = re.sub(
        r"@import\s+url\(['\"]?\.\./\.\./commons/abd-fonts\.css['\"]?\)\s*;",
        _CATALOG_FONT_IMPORT,
        raw,
    )
    return (
        "/* Bootcamp abd-works.css (synced from abd-ai-augmented-bootcamp/css/abd-works.css) */\n"
        + raw
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
    """Spotlight/header source for kanban regen (bootcamp part3 deck)."""
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


def _legacy_catalog_path_prefixes() -> tuple[str, ...]:
    slugs = (*LEGACY_GITHUB_REPO_SLUGS, GITHUB_REPO)
    return tuple(f"../../../../{slug}/catalog/" for slug in slugs)


def _rewrite_github_repo_urls(text: str) -> str:
    slugs = (*LEGACY_GITHUB_REPO_SLUGS, GITHUB_REPO)
    legacy = "|".join(re.escape(slug) for slug in slugs)
    return re.sub(
        rf"https://github\.com/abd-works/(?:{legacy})",
        GITHUB_REPO_URL,
        text,
    )


def _rewrite_legacy_catalog_paths(text: str, catalog_prefix: str) -> str:
    for legacy in _legacy_catalog_path_prefixes():
        text = text.replace(legacy, catalog_prefix)
    return text


def _catalogize_spotlight_html(html: str, *, catalog_prefix: str = "../") -> str:
    text = html.replace(BOOTCAMP_CATALOG_PREFIX, catalog_prefix)
    text = _rewrite_legacy_catalog_paths(text, catalog_prefix)
    text = _rewrite_github_repo_urls(text)
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
    spotlight_html: str = "",
    *,
    questions_html: str = "",
    crosscut_html: str = "",
) -> str:
    parts = [
        f'<section class="kb-slide" data-auto-animate id="{slide_id}">\n',
        f"{textwrap.indent(header_html.strip(), '  ')}\n",
        f"{textwrap.indent(board_html.strip(), '  ')}\n",
    ]
    if questions_html.strip():
        parts.append(f"{textwrap.indent(questions_html.strip(), '  ')}\n")
    if crosscut_html.strip():
        parts.append(f"{textwrap.indent(crosscut_html.strip(), '  ')}\n")
    parts.append(f"{textwrap.indent(legend_html.strip(), '  ')}\n")
    if spotlight_html.strip():
        parts.append(f"{textwrap.indent(spotlight_html.strip(), '  ')}\n")
    parts.append("</section>")
    return "".join(parts)


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
    skill_purpose_by_name: dict[str, str] | None = None,
) -> str:
    """Vertical kb-slide stack (catalog kanban-layout or bootcamp part3 sync)."""
    headers = extract_bootcamp_slide_headers(repo_root)
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
        link_column_heads=link_column_heads,
        board_class="aad-board-grid aad-board-grid--catalog",
        skill_purpose_by_name=skill_purpose_by_name,
    )
    questions_row = build_stage_questions_row_html(model)
    crosscut_row = build_crosscut_html(
        skill_dir_by_name,
        relative_href_prefix=relative_href_prefix,
        skill_purpose_by_name=skill_purpose_by_name,
    )
    slide_sections.append(
        build_kanban_slide_section(
            "overview",
            build_overview_header_html(relative_href_prefix=relative_href_prefix),
            overview_board,
            legend,
            questions_html=questions_row,
            crosscut_html=crosscut_row,
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
            link_column_heads=link_column_heads,
            board_class="aad-board-grid aad-board-grid--catalog",
            skill_purpose_by_name=skill_purpose_by_name,
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
    skill_purpose_by_name: dict[str, str] | None = None,
) -> str:
    """Reveal slide stack only (fullscreen page — no catalog chrome)."""
    return build_kanban_slides_deck_html(
        model,
        skill_dir_by_name,
        repo_root,
        skill_purpose_by_name=skill_purpose_by_name,
    )


def _is_md_list_line(line: str) -> bool:
    s = line.strip()
    return bool(re.match(r"^[-*•]\s+", s) or re.match(r"^\d+[.)]\s+", s))


def _normalize_list_line(line: str) -> str:
    s = line.strip()
    m = re.match(r"^[-*•]\s+(.*)$", s)
    if m:
        return "— " + m.group(1).strip()
    m = re.match(r"^\d+[.)]\s+(.*)$", s)
    if m:
        return "— " + m.group(1).strip()
    return s


def _format_purpose_for_tooltip(text: str) -> str:
    """Keep prose paragraphs; put markdown list items on separate lines."""
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return ""

    blocks: list[str] = []
    prose_buf: list[str] = []
    list_buf: list[str] = []

    def flush_prose() -> None:
        nonlocal prose_buf
        if prose_buf:
            blocks.append(re.sub(r"[ \t]+", " ", " ".join(prose_buf)).strip())
            prose_buf = []

    def flush_list() -> None:
        nonlocal list_buf
        if list_buf:
            blocks.append("\n".join(_normalize_list_line(ln) for ln in list_buf))
            list_buf = []

    for raw in text.split("\n"):
        stripped = raw.strip()
        if not stripped:
            flush_list()
            flush_prose()
            continue
        if _is_md_list_line(stripped):
            flush_prose()
            list_buf.append(stripped)
        else:
            flush_list()
            prose_buf.append(stripped)

    flush_list()
    flush_prose()
    return "\n\n".join(b for b in blocks if b)


def _skill_purpose_text(
    skill_id: str,
    skill_purpose_by_name: dict[str, str] | None,
    *,
    notes: str = "",
) -> str:
    text = ""
    if skill_purpose_by_name:
        text = skill_purpose_by_name.get(skill_id, "").strip()
    if not text and notes:
        text = notes.strip()
    if not text:
        return ""
    return _format_purpose_for_tooltip(text)


def _skill_ticket_inner_html(label: str, purpose: str) -> str:
    if not purpose:
        return _h(label)
    return (
        f'<span class="kb-skill-tooltip-wrap">{_h(label)}'
        f'<span class="kb-col-shape-tooltip kb-skill-tooltip" role="tooltip">'
        f'<span class="kb-col-shape-tooltip__name">{_h(label)}</span>'
        f'<span class="kb-col-shape-tooltip__bullets">{_h(purpose)}</span>'
        f"</span></span>"
    )


def _crosscut_skill_tickets(
    skill_ids: tuple[str, ...],
    skill_dir_by_name: dict[str, str],
    *,
    relative: str,
    css_class: str = "aad-fam-supporting",
    skill_purpose_by_name: dict[str, str] | None = None,
    sibling_pages: bool = False,
) -> list[str]:
    tickets: list[str] = []
    for skill_id in skill_ids:
        href = _skill_href(
            skill_id, skill_dir_by_name, relative=relative, sibling_pages=sibling_pages
        )
        label = _skill_label(skill_id)
        purpose = _skill_purpose_text(skill_id, skill_purpose_by_name)
        tooltip_cls = " has-skill-tooltip" if purpose else ""
        inner = _skill_ticket_inner_html(label, purpose)
        tickets.append(
            f'        <a class="kb-ticket aad-skill {css_class}{tooltip_cls}" '
            f'href="{_h(href)}">{inner}</a>'
        )
    return tickets


def _crosscut_row_label(
    label: str,
    *,
    href: str | None,
    css_class: str,
    spacer: bool = False,
    foundry_ticket: bool = False,
    crosscut_group: str | None = None,
    skill_page_toggle: bool = False,
) -> str:
    if spacer:
        return '      <div class="aad-delivery-crosscut-row-label aad-delivery-crosscut-row-label--spacer"></div>\n'
    if foundry_ticket and skill_page_toggle and crosscut_group:
        ticket_cls = (
            f"kb-ticket aad-skill aad-crosscut-row-title aad-crosscut-row-toggle {css_class}"
        )
        return (
            f'      <button type="button" class="{ticket_cls}" '
            f'data-crosscut-group="{_h(crosscut_group)}" aria-pressed="false">'
            f"{_h(label)}</button>\n"
        )
    if foundry_ticket:
        ticket_cls = f"kb-ticket aad-skill aad-crosscut-row-title {css_class}"
        if href:
            return (
                f'      <a class="{ticket_cls}" href="{_h(href)}">{_h(label)}</a>\n'
            )
        return f'      <span class="{ticket_cls}">{_h(label)}</span>\n'
    if href:
        return (
            f'      <a class="aad-delivery-crosscut-row-label aad-row-label {css_class}" '
            f'href="{_h(href)}">{_h(label)}</a>\n'
        )
    return (
        f'      <div class="aad-delivery-crosscut-row-label aad-row-label {css_class}">'
        f"{_h(label)}</div>\n"
    )


def _crosscut_group_rows(
    label: str,
    skill_ids: tuple[str, ...],
    skill_dir_by_name: dict[str, str],
    *,
    relative: str,
    group_href: str | None = None,
    family_css: str = "aad-fam-supporting",
    tier: str = "practice",
    row_class: str = "",
    skill_purpose_by_name: dict[str, str] | None = None,
    sibling_pages: bool = False,
    filter_family: str | None = None,
    crosscut_group: str | None = None,
    foundry_ticket: bool = False,
    skill_page_toggle: bool = False,
) -> list[str]:
    tier_cls = f"aad-crosscut-tier--{tier}"
    extra_cls = f" {row_class}" if row_class else ""
    group_id = crosscut_group or filter_family or ""
    data_attr = ""
    if group_id:
        data_attr = f' data-crosscut-group="{_h(group_id)}"'
    if filter_family:
        if tier == "foundational" or filter_family == "other":
            data_attr += ' data-filter-family="other"'
        else:
            data_attr += f' data-family="{_h(filter_family)}"'
    skill_tickets = _crosscut_skill_tickets(
        skill_ids,
        skill_dir_by_name,
        relative=relative,
        css_class=family_css,
        skill_purpose_by_name=skill_purpose_by_name,
        sibling_pages=sibling_pages,
    )
    if foundry_ticket:
        row_title = filter_family if filter_family and tier == "practice" else label
        return [
            f'    <div class="aad-delivery-crosscut-row {tier_cls}{extra_cls}"{data_attr}>\n'
            + _crosscut_row_label(
                row_title,
                href=group_href,
                css_class=family_css,
                foundry_ticket=True,
                crosscut_group=group_id,
                skill_page_toggle=skill_page_toggle,
            )
            + '      <div class="aad-delivery-crosscut-skills aad-delivery-crosscut-skills--collapsed">\n'
            + "\n".join(skill_tickets)
            + "\n      </div>\n    </div>"
        ]
    return [
        f'    <div class="aad-delivery-crosscut-row {tier_cls}{extra_cls}"{data_attr}>\n'
        + _crosscut_row_label(label, href=group_href, css_class=family_css)
        + '      <div class="aad-delivery-crosscut-row-body">\n'
        + '        <div class="aad-delivery-crosscut-skills">\n'
        + "\n".join(skill_tickets)
        + "\n        </div>\n      </div>\n    </div>"
    ]


def build_crosscut_html(
    skill_dir_by_name: dict[str, str],
    *,
    relative_href_prefix: str = "../",
    skill_purpose_by_name: dict[str, str] | None = None,
    plugin_first_skill_hrefs: dict[str, str] | None = None,
    sibling_skill_pages: bool = False,
    foundry_ticket: bool = False,
    skill_page_toggle: bool = False,
) -> str:
    """Cross-plugin skill rows below stage question bullets."""
    rel = relative_href_prefix
    practice_rows_list: list[str] = []
    foundational_rows_list: list[str] = []

    for group_id, label, plugin_id, skill_ids in SUPPORTING_CROSSCUT_GROUPS:
        family_css = PLUGIN_CSS_CLASS.get(plugin_id, "aad-fam-supporting")
        group_href = _family_nav_href(
            plugin_id,
            relative=rel,
            plugin_first_skill_hrefs=plugin_first_skill_hrefs,
        )
        practice_rows_list.extend(
            _crosscut_group_rows(
                label,
                skill_ids,
                skill_dir_by_name,
                relative=rel,
                group_href=group_href,
                family_css=family_css,
                tier="practice",
                skill_purpose_by_name=skill_purpose_by_name,
                sibling_pages=sibling_skill_pages,
                filter_family=plugin_id,
                crosscut_group=group_id,
                foundry_ticket=foundry_ticket,
                skill_page_toggle=skill_page_toggle,
            )
        )

    for plugin_id, label, skill_ids in FOUNDATIONAL_CROSSCUT_PLUGINS:
        foundational_rows_list.extend(
            _crosscut_group_rows(
                label,
                skill_ids,
                skill_dir_by_name,
                relative=rel,
                group_href=_family_nav_href(
                    plugin_id,
                    relative=rel,
                    plugin_first_skill_hrefs=plugin_first_skill_hrefs,
                ),
                family_css="aad-fam-foundational",
                tier="foundational",
                skill_purpose_by_name=skill_purpose_by_name,
                sibling_pages=sibling_skill_pages,
                filter_family="other",
                crosscut_group=plugin_id,
                foundry_ticket=foundry_ticket,
                skill_page_toggle=skill_page_toggle,
            )
        )

    return (
        '<div class="aad-delivery-crosscut-stack" data-id="crosscut">\n'
        '  <section class="aad-delivery-crosscut-section aad-delivery-crosscut-section--supporting">\n'
        '    <h3 class="aad-delivery-crosscut-section-title">Supporting</h3>\n'
        '    <div class="aad-delivery-crosscut-section-body">\n'
        + "\n".join(practice_rows_list)
        + "\n    </div>\n  </section>\n"
        '  <section class="aad-delivery-crosscut-section aad-delivery-crosscut-section--foundational">\n'
        '    <h3 class="aad-delivery-crosscut-section-title">Foundations</h3>\n'
        '    <div class="aad-delivery-crosscut-section-body">\n'
        + "\n".join(foundational_rows_list)
        + "\n    </div>\n  </section>\n"
        "</div>"
    )


def build_kanban_board_html(
    model: KanbanModel,
    skill_dir_by_name: dict[str, str],
    *,
    relative_href_prefix: str = "../",
    same_page_stages: bool = False,
    board_class: str = "aad-board-grid",
    active_stage_id: str | None = None,
    link_column_heads: bool = True,
    foundry_hub: bool = False,
    skill_purpose_by_name: dict[str, str] | None = None,
    sibling_skill_pages: bool = False,
    current_skill_id: str | None = None,
    current_dir_name: str = "",
    plugin_filter: str | None = None,
    include_stage_folder_skills: bool = True,
    initial_visible_family: str | None = None,
) -> str:
    rel = relative_href_prefix

    def ticket_is_current(skill_id: str, stage_id: str) -> bool:
        if not current_skill_id:
            return False
        dir_name = skill_dir_by_name.get(skill_id) or GITHUB_SKILL_ALIASES.get(
            skill_id, skill_id
        )
        if skill_id != current_skill_id and dir_name != current_dir_name:
            return False
        if active_stage_id:
            return stage_id == active_stage_id
        return True

    def render_skill_ticket(
        *,
        skill_id: str,
        stage_id: str,
        plugin_id: str,
        css: str,
        label: str,
        purpose: str,
        data_id: str,
        extra_class: str = "",
    ) -> str:
        href = _skill_href(
            skill_id,
            skill_dir_by_name,
            relative=rel,
            sibling_pages=sibling_skill_pages,
            stage_id=stage_id if sibling_skill_pages else None,
        )
        tooltip_cls = " has-skill-tooltip" if purpose else ""
        is_current = ticket_is_current(skill_id, stage_id)
        current_cls = " kb-ticket--current" if is_current else ""
        inner = _skill_ticket_inner_html(label, purpose)
        perspective_attr = (
            f' data-perspective="{PLUGIN_PERSPECTIVE_KEY[plugin_id]}"'
            if foundry_hub and plugin_id in PLUGIN_PERSPECTIVE_KEY
            else ""
        )
        stage_attr = f' data-stage="{stage_id}"'
        skill_href_attr = ""
        if sibling_skill_pages:
            base_href = _skill_href(
                skill_id,
                skill_dir_by_name,
                relative=rel,
                sibling_pages=True,
            )
            skill_href_attr = f' data-skill-href="{_h(base_href)}"'
        ticket_cls = f"kb-ticket aad-skill {css}{extra_class}{tooltip_cls}{current_cls}"
        if sibling_skill_pages and is_current:
            return (
                f'        <span class="{ticket_cls}" '
                f'data-id="{data_id}"{perspective_attr}{stage_attr}{skill_href_attr} '
                f'aria-current="page">{inner}</span>'
            )
        return (
            f'        <a class="{ticket_cls}" '
            f'data-id="{data_id}"{perspective_attr}{stage_attr}{skill_href_attr} '
            f'href="{_h(href)}">{inner}</a>'
        )

    cols: list[str] = []
    for stage_id, title, num, _purpose in model.stages:
        stage_link = _stage_href(stage_id, same_page=same_page_stages, relative=rel)
        active_cls = " active" if active_stage_id == stage_id else ""
        col_rows: list[str] = []
        practice_skill_ids: set[str] = set()
        practice_rows: list[str] = []
        for plugin_id in PLUGIN_ROW_ORDER:
            if plugin_filter and plugin_id != plugin_filter:
                continue
            skills = model.matrix.get(stage_id, {}).get(plugin_id, [])
            css = PLUGIN_CSS_CLASS.get(plugin_id, "")
            tickets: list[str] = []
            for sk in skills:
                if not _kanban_include_skill(sk.skill_id, stage_id=stage_id, notes=sk.notes):
                    continue
                practice_skill_ids.add(sk.skill_id)
                label = _skill_label(sk.skill_id, stage_id)
                purpose = _skill_purpose_text(
                    sk.skill_id, skill_purpose_by_name, notes=sk.notes or ""
                )
                tickets.append(
                    render_skill_ticket(
                        skill_id=sk.skill_id,
                        stage_id=stage_id,
                        plugin_id=plugin_id,
                        css=css,
                        label=label,
                        purpose=purpose,
                        data_id=f"tk-{plugin_id}-{stage_id}-{_h(sk.skill_id)}",
                    )
                )
            inner = "\n".join(tickets) if tickets else ""
            empty_cls = " aad-skill-row--empty" if not tickets else ""
            visible_cls = (
                " is-filter-visible"
                if initial_visible_family and plugin_id == initial_visible_family
                else ""
            )
            practice_rows.append(
                f'      <div class="aad-skill-row {css}{empty_cls}{visible_cls}" '
                f'data-family="{plugin_id}">\n'
                f"{inner}\n      </div>"
            )

        col_rows.extend(practice_rows)

        if include_stage_folder_skills:
            stage_folder_ids = model.stage_folder_skills.get(stage_id, [])
            stage_tickets: list[str] = []
            for skill_id in stage_folder_ids:
                if skill_id in practice_skill_ids:
                    continue
                if not _kanban_include_skill(skill_id, stage_id=stage_id):
                    continue
                label = _skill_label(skill_id, stage_id)
                purpose = _skill_purpose_text(skill_id, skill_purpose_by_name)
                stage_tickets.append(
                    render_skill_ticket(
                        skill_id=skill_id,
                        stage_id=stage_id,
                        plugin_id="",
                        css="aad-fam-other",
                        label=label,
                        purpose=purpose,
                        data_id=f"tk-stage-{stage_id}-{_h(skill_id)}",
                        extra_class=f" aad-stage-skill {STAGE_SKILL_FAMILY_CLASS}",
                    )
                )
            if foundry_hub:
                col_rows.append(
                    '      <div class="aad-stage-skills-gap" aria-hidden="true"></div>'
                )
                for slot in range(FOUNDRY_HUB_STAGE_SKILL_ROWS):
                    if slot < len(stage_tickets):
                        col_rows.append(
                            '      <div class="aad-skill-row aad-skill-row--stage-other" '
                            'data-family="other">\n'
                            f"{stage_tickets[slot]}\n      </div>"
                        )
                    else:
                        col_rows.append(
                            '      <div class="aad-skill-row aad-skill-row--stage-other '
                            'aad-skill-row--empty" data-family="other" aria-hidden="true"></div>'
                        )
            elif stage_tickets:
                col_rows.append('      <div class="aad-stage-skills-gap" aria-hidden="true"></div>')
                col_rows.append(
                    '      <div class="aad-stage-skills-block">\n'
                    + "\n".join(stage_tickets)
                    + "\n      </div>"
                )
        if link_column_heads:
            if foundry_hub:
                col_head = _foundry_col_head_html(
                    stage_id, title, num, _stage_href(stage_id, same_page=same_page_stages, relative=rel)
                )
            else:
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
        stage_attr = f' data-stage="{stage_id}"' if foundry_hub else ""
        if foundry_hub:
            cols.append(
                f'    <div class="kb-col{active_cls}" data-id="col-{stage_id}"{stage_attr}>\n'
                f"{col_head}"
                + "\n".join(col_rows)
                + "\n    </div>"
            )
        else:
            cols.append(
                f'    <div class="kb-col{active_cls}" data-id="col-{stage_id}"{stage_attr}>\n'
                f"{col_head}"
                f'      <div class="kb-col-tickets aad-tickets-grid">\n'
                + "\n".join(col_rows)
                + "\n      </div>\n    </div>"
            )

    if foundry_hub:
        return "\n".join(cols) + "\n"

    return (
        f'<div class="kb-board {board_class}" data-id="board">\n'
        + "\n".join(cols)
        + "\n</div>\n"
    )


def build_stage_sections_html(model: KanbanModel) -> str:
    parts: list[str] = ['<section class="kanban-stages" id="stages">', "<h2>Delivery stages</h2>"]
    planning_href = "../skill/abd-kanban-planning.html"
    parts.append(
        f'<p>Stage definitions are the source of truth for '
        f'<a href="{_h(planning_href)}">abd-kanban-planning</a> '
        f"and the delivery war room. Each column above links here.</p>"
    )
    for stage_id, title, num, purpose in model.stages:
        stage_src = f"{GITHUB_BLOB_MAIN}practices/kanban/reference/stages/{stage_id}.md"
        parts.append(f'<article class="kanban-stage" id="stage-{stage_id}-definition">')
        parts.append(
            f"<h3>{num}. {_h(title)}</h3>"
            f'<p class="kanban-stage-links">'
            f'<a href="{_h(planning_href)}">abd-kanban-planning</a> · '
            f'<a href="{_h(stage_src)}">stage definition (source)</a></p>'
        )
        if purpose:
            parts.append(f"<p>{_h(purpose)}</p>")
        skills = model.matrix.get(stage_id, {})
        if skills:
            parts.append("<ul>")
            for plugin_id in PLUGIN_ROW_ORDER:
                for sk in skills.get(plugin_id, []):
                    if not _kanban_include_skill(sk.skill_id, stage_id=stage_id, notes=sk.notes):
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
        f'<a href="{relative_href_prefix}index.html">The ABD Foundry</a>'
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
    skill_purpose_by_name: dict[str, str] | None = None,
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
        skill_purpose_by_name=skill_purpose_by_name,
    )
    stages_html = build_stage_sections_html(model)

    slides_html = build_kanban_page_body(
        model,
        skill_dir_by_name,
        stages_html,
        repo_root=repo_root,
        skill_purpose_by_name=skill_purpose_by_name,
    )

    reveal_js_src = template_dir / "kanban-slides-init.js"
    reveal_init_js = (
        reveal_js_src.read_text(encoding="utf-8") if reveal_js_src.is_file() else ""
    )

    html = (
        page_tpl.replace("{{CSS}}", full_css)
        .replace("{{TITLE}}", "Foundry — delivery kanban")
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
            skill_purpose_by_name=skill_purpose_by_name,
        ),
        encoding="utf-8",
    )
    return index_path


BOOTCAMP_KANBAN_SLIDES_START = "<!-- KANBAN_SLIDES -->"
BOOTCAMP_KANBAN_SLIDES_END = "<!-- /KANBAN_SLIDES -->"


def sync_bootcamp_part3_kanban(
    repo_root: Path,
    skill_dir_by_name: dict[str, str],
    *,
    skill_purpose_by_name: dict[str, str] | None = None,
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
        skill_purpose_by_name=skill_purpose_by_name,
    )
    slides_html = rewrite_bootcamp_catalog_links(slides_html, skill_dir_by_name)
    slides_html = slides_html.replace('href="../index.html"', f'href="{prefix}index.html"')
    slides_html = _rewrite_legacy_catalog_paths(slides_html, prefix)
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


def skill_purpose_map_from_entries(skills: list) -> dict[str, str]:
    """Map YAML skill name and folder name → full SKILL.md Purpose (no truncation)."""
    out: dict[str, str] = {}
    for s in skills:
        purpose = (
            getattr(s, "purpose", None)
            or getattr(s, "description", None)
            or getattr(s, "summary", None)
            or ""
        ).strip()
        if purpose:
            out[s.name] = purpose
            out[s.dir_name] = purpose
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

    legacy_tree = "|".join(re.escape(slug) for slug in (*LEGACY_GITHUB_REPO_SLUGS, GITHUB_REPO))
    text = re.sub(
        rf'href="https://github\.com/abd-works/(?:{legacy_tree})/tree/main/skills(?:/[^/"]+)?/([^/"]+)"',
        lambda m: f'href="{_catalog_skill_href(m.group(1))}"',
        text,
    )
    text = text.replace("architecture-centric-delivery", "architecture-centric-engineering")
    text = text.replace("abd-clickable-prototype.html", "abd-ux-specification.html")
    text = text.replace(">clickable-prototype</a>", ">interface-design</a>")
    text = text.replace("<!-- UXD: clickable-prototype -->", "<!-- UXD: interface-design (implementation pass) -->")
    text = _rewrite_github_repo_urls(text)
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
