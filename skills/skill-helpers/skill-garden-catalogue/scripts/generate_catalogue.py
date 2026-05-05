#!/usr/bin/env python3
"""Scan the skills tree and generate a categorised Markdown inventory + HTML catalogue.

Categories are the top-level folders directly under skills/.  Every SKILL.md
found at any depth beneath a category folder becomes an entry in that category.
Skills sitting at the top level (no parent folder) land in an "Other" bucket.
"""

from __future__ import annotations

import argparse
import html as html_mod
import re
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Callable, NamedTuple
from urllib.parse import quote as _urlquote

SCRIPT_DIR   = Path(__file__).resolve().parent
SKILL_ROOT   = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_ROOT / "templates"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
YAML_FIELD_RE  = re.compile(r"^(\w[\w-]*):\s*(.+)", re.MULTILINE)
YAML_BLOCK_RE  = re.compile(r"^(\w[\w-]*):\s*>-?\s*\n((?:[ \t]+.*\n?)+)", re.MULTILINE)


class SkillEntry(NamedTuple):
    name:     str
    category: str        # top-level folder name, or "" for root-level skills
    rel_path: str        # path from skills_dir to skill folder  e.g. delivery/abd-delivery-planning
    challenge: str
    solution:  str


class AgentEntry(NamedTuple):
    name:    str
    folder:  str   # folder name under agents_dir
    summary: str


# ---------------------------------------------------------------------------
# Lightweight frontmatter parser
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    fields: dict[str, str] = {}
    for bm in YAML_BLOCK_RE.finditer(block):
        fields[bm.group(1)] = " ".join(bm.group(2).split())
    for lm in YAML_FIELD_RE.finditer(block):
        key = lm.group(1)
        if key not in fields:
            fields[key] = lm.group(2).strip().strip('"').strip("'")
    return fields


def _extract_section(body: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    m = pattern.search(body)
    return m.group(1).strip() if m else None


def _strip_md(text: str) -> str:
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*",     r"\1", text)
    text = re.sub(r"`[^`]+`",         "",    text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def _truncate(text: str, limit: int = 200) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(".,;: ") + " …"


PREAMBLE_RE = re.compile(
    r"^(load this skill|use when|use this skill|any of the following)\b",
    re.IGNORECASE,
)


def _first_meaningful_line(text: str, max_chars: int = 200) -> str:
    text = _strip_md(text)
    for line in text.splitlines():
        line = line.strip().lstrip("- ").strip()
        if len(line) < 15:
            continue
        if PREAMBLE_RE.match(line):
            continue
        sent = re.split(r"(?<=[.!?])\s", line, maxsplit=1)[0]
        return _truncate(sent, max_chars)
    return _truncate(text.strip(), max_chars)


def _first_two_sentences(text: str, max_chars: int = 200) -> str:
    """Return up to two sentences from text, stripped of markdown."""
    text = _strip_md(text)
    combined = " ".join(line.strip().lstrip("- ").strip() for line in text.splitlines() if line.strip())
    sentences = re.split(r"(?<=[.!?])\s+", combined)
    result = ""
    for sent in sentences:
        sent = sent.strip()
        if not sent or len(sent) < 10 or PREAMBLE_RE.match(sent):
            continue
        if not result:
            result = sent
        elif len(result) + 1 + len(sent) <= max_chars:
            result += " " + sent
        else:
            break
    return _truncate(result, max_chars) if result else _truncate(combined, max_chars)


def _first_bullet(text: str) -> str:
    text = _strip_md(text)
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            content = stripped[2:].strip()
            if len(content) > 15:
                return _truncate(content)
    return ""


def _derive_challenge(body: str) -> str:
    purpose = _extract_section(body, "Purpose")
    if purpose:
        result = _first_meaningful_line(purpose)
        if result and not PREAMBLE_RE.match(result):
            return result
    for heading in ("When to use this skill", "When to use", "When to Apply"):
        section = _extract_section(body, heading)
        if section:
            bullet = _first_bullet(section)
            if bullet:
                return bullet
            result = _first_meaningful_line(section)
            if result and not PREAMBLE_RE.match(result):
                return result
    h1_match = re.search(r"^#\s+(.+)", body, re.MULTILINE)
    if h1_match:
        return _truncate(h1_match.group(1).strip())
    return "See SKILL.md for details."


def _derive_solution(fm: dict[str, str], body: str) -> str:
    one = (fm.get("catalogue_one_liner") or "").strip()
    if one and one != "---":
        return _truncate(_strip_md(one), 200)
    desc = fm.get("description", "")
    if desc:
        return _truncate(_strip_md(desc), 200)
    section = _extract_section(body, "Purpose")
    if section:
        return _first_two_sentences(section, 200)
    return "See SKILL.md for details."


# ---------------------------------------------------------------------------
# Catalogue overrides — move a skill to a different display category
# ---------------------------------------------------------------------------

# Maps skill folder name → display category override.
# The skill stays on disk where it is; only the catalogue column changes.
CATEGORY_OVERRIDES: dict[str, str] = {
    "abd-acceptance-test-driven-development": "engineering",
}

# Explicit display order within a category (by skill folder name).
# Skills not listed here sort alphabetically after the pinned ones.
CATEGORY_SORT_ORDER: dict[str, list[str]] = {
    "engineering": [
        "abd-acceptance-test-driven-development",
        "abd-clean-code",
        "mern-technical-architecture",
    ],
}


def _category_sort_key(cat: str) -> "Callable[[SkillEntry], tuple]":
    pinned = {name: i for i, name in enumerate(CATEGORY_SORT_ORDER.get(cat, []))}
    n = len(pinned)
    def key(e: SkillEntry) -> tuple:
        folder = e.rel_path.rstrip("/").rsplit("/", 1)[-1]
        idx = pinned.get(folder, n)
        return (idx, e.name.lower())
    return key


# ---------------------------------------------------------------------------
# Discovery  —  recursive, category = top-level folder
# ---------------------------------------------------------------------------

def discover_skills(skills_dir: Path) -> dict[str, list[SkillEntry]]:
    """Return {category: [SkillEntry, ...]} sorted by category then skill name."""
    by_category: dict[str, list[SkillEntry]] = defaultdict(list)

    for skill_md in sorted(skills_dir.rglob("SKILL.md")):
        skill_folder = skill_md.parent
        rel          = skill_folder.relative_to(skills_dir)
        parts        = rel.parts

        # category = top-level folder; "" for root-level skills
        folder_name = skill_folder.name
        category = CATEGORY_OVERRIDES.get(folder_name) or (parts[0] if len(parts) > 1 else "")

        text      = skill_md.read_text(encoding="utf-8", errors="replace")
        fm        = _parse_frontmatter(text)
        body      = FRONTMATTER_RE.sub("", text).strip()
        name      = fm.get("name", skill_folder.name)
        challenge = _derive_challenge(body)
        solution  = _derive_solution(fm, body)

        by_category[category].append(
            SkillEntry(
                name=name,
                category=category,
                rel_path=str(rel).replace("\\", "/"),
                challenge=challenge,
                solution=solution,
            )
        )

    # sort entries within each category (pinned order first, then alpha)
    for cat in by_category:
        by_category[cat].sort(key=_category_sort_key(cat))

    return dict(sorted(by_category.items(), key=lambda kv: kv[0].lower()))


# ---------------------------------------------------------------------------
# Agent discovery
# ---------------------------------------------------------------------------

def discover_agents(agents_dir: Path) -> list[AgentEntry]:
    """Scan agents_dir for AGENT.md files. Returns list sorted by name."""
    entries: list[AgentEntry] = []
    for agent_md in sorted(agents_dir.rglob("AGENT.md")):
        folder = agent_md.parent
        # only top-level agent folders (depth 1)
        try:
            rel = folder.relative_to(agents_dir)
        except ValueError:
            continue
        if len(rel.parts) != 1:
            continue
        text  = agent_md.read_text(encoding="utf-8", errors="replace")
        fm    = _parse_frontmatter(text)
        body  = FRONTMATTER_RE.sub("", text).strip()
        name  = fm.get("name") or folder.name
        # summary: first meaningful sentence from body
        summary = (fm.get("description") or fm.get("catalogue_one_liner") or
                   _first_meaningful_line(body, 200))
        entries.append(AgentEntry(name=name, folder=folder.name, summary=summary))
    return sorted(entries, key=lambda e: e.name.lower())


_AGENT_ICON = (
    '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
    ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<circle cx="8" cy="5" r="3"/><path d="M2 14c0-3.3 2.7-6 6-6s6 2.7 6 6"/>'
    '<path d="M8 9v2M6 11h4"/></svg>'
)


def _render_agents_section(agents: list[AgentEntry]) -> str:
    if not agents:
        return ""
    label_svg = (
        '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<circle cx="7" cy="4.5" r="2.5"/><path d="M1.5 13c0-3 2.2-5 5.5-5s5.5 2 5.5 5"/>'
        '<path d="M7 8.5v1.5M6 10h2"/></svg>'
    )
    rows = ""
    for a in agents:
        url = "/abd-skills-catalog/agents/" + _urlquote(a.folder, safe="/")
        rows += (
            f'      <div class="catalog-garden-row">'
            f'<span class="catalog-garden-name catalog-garden-name--foundational">'
            f'<a href="{url}/">{_h(a.name)}</a></span>'
            f'<span class="catalog-garden-desc">{_h(a.summary)}</span>'
            f'</div>\n'
        )
    return textwrap.dedent(f"""\
  <div class="catalog-section-label catalog-section-label--agents">
    {label_svg}
    Agents — Role-Based AI Collaborators
  </div>
  <div class="catalog-agents-grid">
    <div class="catalog-garden-col">
      <div class="catalog-garden-col-header catalog-garden-col-header--foundational">
        {_AGENT_ICON}
        <span>Agents</span>
      </div>
{rows}    </div>
  </div>
""")


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

_CATEGORY_LABELS: dict[str, str] = {
    "":                     "General",
    "delivery":             "Delivery",
    "domain-driven-design": "Domain Driven Design",
    "engineering":          "Engineering",
    "idea shaping":         "Idea Shaping",
    "skill-helpers":        "Skill Helpers",
    "story-analysis":       "Story Analysis",
    "utilities":            "Utilities",
}

# Categories that go in the top practice grid vs the lower foundational grid
PRACTICE_CATEGORIES = {"idea shaping", "domain-driven-design", "story-analysis", "engineering", "delivery"}
FOUNDATIONAL_CATEGORIES = {"skill-helpers", "utilities", ""}

_CATEGORY_ICONS: dict[str, str] = {
    "idea shaping": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<circle cx="8" cy="6" r="4"/><path d="M6 10v1.5h4V10"/><path d="M6.5 13h3"/></svg>'
    ),
    "domain-driven-design": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" aria-hidden="true">'
        '<circle cx="8" cy="8" r="5.5"/><circle cx="8" cy="8" r="2"/>'
        '<path d="M8 2.5V6M8 10v3.5M2.5 8H6M10 8h3.5"/></svg>'
    ),
    "story-analysis": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<rect x="2" y="2" width="12" height="12" rx="1.5"/>'
        '<path d="M5 6h6M5 9h4M5 12h2"/><path d="M11 9l2 2-2 2"/></svg>'
    ),
    "engineering": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M5 4L1 8l4 4M11 4l4 4-4 4M9.5 2.5l-3 11"/></svg>'
    ),
    "delivery": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M2 5h12v7a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V5z"/>'
        '<path d="M2 5l2-3h8l2 3M6 9h4"/></svg>'
    ),
    "utilities": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M2 4l6-2.5L14 4l-6 2.5L2 4z"/>'
        '<path d="M2 8l6 2.5L14 8"/><path d="M2 12l6 2.5L14 12"/></svg>'
    ),
    "skill-helpers": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M13.5 2.5a3.5 3.5 0 0 0-4.9 4.9L2 14a1 1 0 0 0 1.4 1.4l6.6-6.6'
        ' a3.5 3.5 0 0 0 3.5-6.3z"/><path d="M12 4l-2 2"/></svg>'
    ),
    "": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" aria-hidden="true">'
        '<circle cx="8" cy="8" r="6"/><path d="M8 5v6M5 8h6"/></svg>'
    ),
}


def _category_label(cat: str) -> str:
    return _CATEGORY_LABELS.get(cat, cat.replace("-", " ").title())


def _category_icon(cat: str) -> str:
    return _CATEGORY_ICONS.get(cat, _CATEGORY_ICONS[""])


def generate_markdown(by_category: dict[str, list[SkillEntry]]) -> str:
    total = sum(len(v) for v in by_category.values())
    lines = [
        "# Skill Garden — Inventory",
        "",
        f"> Auto-generated catalogue of **{total}** deployed skills.",
        "> Re-run `generate_catalogue.py` to refresh.",
        "",
    ]
    for cat, entries in by_category.items():
        lines += [f"## {_category_label(cat)}", "", "| Skill | Challenge | Solution |", "| --- | --- | --- |"]
        for e in entries:
            link      = f"[{e.name}]({e.rel_path}/)"
            challenge = e.challenge.replace("|", "\\|")
            solution  = e.solution.replace("|", "\\|")
            lines.append(f"| {link} | {challenge} | {solution} |")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

def _h(text: str) -> str:
    return html_mod.escape(text)


def _render_row(e: SkillEntry, *, foundational: bool = False) -> str:
    name_cls = "catalog-garden-name" + (" catalog-garden-name--foundational" if foundational else "")
    desc = e.solution
    url = "/abd-skills-catalog/" + _urlquote(e.rel_path.replace("\\", "/"), safe="/")
    return (
        f'      <div class="catalog-garden-row">'
        f'<span class="{name_cls}"><a href="{url}/">{_h(e.name)}</a></span>'
        f'<span class="catalog-garden-desc">{_h(desc)}</span>'
        f'</div>\n'
    )


def _render_col(cat: str, entries: list[SkillEntry]) -> str:
    label = _category_label(cat)
    icon  = _category_icon(cat)
    is_foundational = cat in FOUNDATIONAL_CATEGORIES
    header_cls = "catalog-garden-col-header" + (" catalog-garden-col-header--foundational" if is_foundational else "")
    rows = "".join(_render_row(e, foundational=is_foundational) for e in entries)
    return (
        f'    <div class="catalog-garden-col">\n'
        f'      <div class="{header_cls}">\n'
        f'        {icon}\n'
        f'        <span>{_h(label)}</span>\n'
        f'      </div>\n'
        f'{rows}'
        f'    </div>\n'
    )


def generate_html(by_category: dict[str, list[SkillEntry]]) -> str:
    total = sum(len(v) for v in by_category.values())

    # Split into practice and foundational tiers
    practice_cols    = ""
    foundational_cols = ""

    # Preserve desired order for practice disciplines
    practice_order = ["idea shaping", "domain-driven-design", "story-analysis", "engineering", "delivery"]
    foundational_order = ["utilities", "skill-helpers", ""]

    for cat in practice_order:
        if cat in by_category:
            practice_cols += _render_col(cat, by_category[cat])

    # Any practice category not in the explicit order list
    for cat, entries in by_category.items():
        if cat in PRACTICE_CATEGORIES and cat not in practice_order:
            practice_cols += _render_col(cat, entries)

    for cat in foundational_order:
        if cat in by_category:
            foundational_cols += _render_col(cat, by_category[cat])

    for cat, entries in by_category.items():
        if cat in FOUNDATIONAL_CATEGORIES and cat not in foundational_order:
            foundational_cols += _render_col(cat, entries)

    # Section label SVG icons
    practice_label_svg = (
        '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" aria-hidden="true">'
        '<circle cx="7" cy="5" r="3.5"/><path d="M5 8.5V10h4V8.5"/><path d="M5.5 11.5h3"/></svg>'
    )
    foundational_label_svg = (
        '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M2 4.5l5-2 5 2-5 2-5-2z"/><path d="M2 8l5 2 5-2"/><path d="M2 11.5l5 2 5-2"/></svg>'
    )

    skill_sections = textwrap.dedent(f"""\
  <div class="catalog-section-label">
    {practice_label_svg}
    Practice Skills — What We Do
  </div>
  <div class="catalog-practice-grid">
{practice_cols}  </div>

  <div class="catalog-section-label catalog-section-label--foundational">
    {foundational_label_svg}
    Foundational Skills — Enhance the Way Skills Run
  </div>
  <div class="catalog-foundational-grid">
{foundational_cols}  </div>
""")

    template_path = TEMPLATE_DIR / "catalog-index.html"
    template = (
        template_path.read_text(encoding="utf-8")
        if template_path.exists()
        else _default_html_template()
    )

    return (
        template
        .replace("{{SKILL_COUNT}}", str(total))
        .replace("{{SKILL_SECTIONS}}", skill_sections)
        .replace("{{AGENT_SECTION}}", "")  # filled by generate_html_with_agents
    )


def generate_html_with_agents(
    by_category: dict[str, list[SkillEntry]],
    agents: list[AgentEntry],
) -> str:
    total = sum(len(v) for v in by_category.values())

    # reuse generate_html for skill sections
    html = generate_html(by_category)

    agent_section = _render_agents_section(agents)
    # inject agent section before closing </div>\n</body>
    return html.replace("</div>\n\n</body>", f"{agent_section}\n</div>\n\n</body>")


def _default_html_template() -> str:
    return textwrap.dedent("""\
        <!DOCTYPE html><html><head><meta charset="utf-8">
        <title>Skill Catalogue</title></head><body>
        <h1>Skill Catalogue ({{SKILL_COUNT}} skills)</h1>
        {{SKILL_SECTIONS}}
        </body></html>""")


# ---------------------------------------------------------------------------
# Markdown → HTML renderer (no external deps)
# ---------------------------------------------------------------------------

def _md_inline(text: str) -> str:
    """Convert inline markdown (bold, italic, code, links) to HTML."""
    text = re.sub(r"```[^`]*```", lambda m: "<code>" + html_mod.escape(m.group(0)[3:-3]) + "</code>", text)
    text = re.sub(r"`([^`]+)`", lambda m: "<code>" + html_mod.escape(m.group(1)) + "</code>", text)
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*",     r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*",         r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def _md_to_html(md: str) -> str:
    """Convert a SKILL.md body (frontmatter already stripped) to HTML."""
    lines = md.splitlines()
    out: list[str] = []
    in_code = False
    code_lang = ""
    code_lines: list[str] = []
    in_list: str | None = None   # "ul" or "ol"
    pending_para: list[str] = []

    def flush_para() -> None:
        if pending_para:
            content = " ".join(pending_para).strip()
            if content:
                out.append(f"<p>{_md_inline(html_mod.escape(content))}</p>")
            pending_para.clear()

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append(f"</{in_list}>")
            in_list = None

    for raw in lines:
        # fenced code block
        if raw.startswith("```"):
            if not in_code:
                flush_para()
                close_list()
                in_code = True
                code_lang = raw[3:].strip()
                code_lines = []
            else:
                lang_cls = f' class="language-{html_mod.escape(code_lang)}"' if code_lang else ""
                out.append(f"<pre><code{lang_cls}>{html_mod.escape(chr(10).join(code_lines))}</code></pre>")
                in_code = False
            continue

        if in_code:
            code_lines.append(raw)
            continue

        # headings
        hm = re.match(r"^(#{1,4})\s+(.*)", raw)
        if hm:
            flush_para()
            close_list()
            level = len(hm.group(1))
            out.append(f"<h{level}>{_md_inline(html_mod.escape(hm.group(2).strip()))}</h{level}>")
            continue

        # horizontal rule
        if re.match(r"^[-*_]{3,}\s*$", raw):
            flush_para()
            close_list()
            out.append("<hr>")
            continue

        # blockquote
        if raw.startswith("> "):
            flush_para()
            close_list()
            out.append(f"<blockquote><p>{_md_inline(html_mod.escape(raw[2:]))}</p></blockquote>")
            continue

        # unordered list
        ul_m = re.match(r"^[-*+]\s+(.*)", raw)
        if ul_m:
            flush_para()
            if in_list != "ul":
                close_list()
                out.append("<ul>")
                in_list = "ul"
            out.append(f"<li>{_md_inline(html_mod.escape(ul_m.group(1)))}</li>")
            continue

        # ordered list
        ol_m = re.match(r"^\d+\.\s+(.*)", raw)
        if ol_m:
            flush_para()
            if in_list != "ol":
                close_list()
                out.append("<ol>")
                in_list = "ol"
            out.append(f"<li>{_md_inline(html_mod.escape(ol_m.group(1)))}</li>")
            continue

        # blank line
        if not raw.strip():
            flush_para()
            close_list()
            continue

        pending_para.append(raw)

    flush_para()
    close_list()
    if in_code and code_lines:
        out.append(f"<pre><code>{html_mod.escape(chr(10).join(code_lines))}</code></pre>")

    return "\n".join(out)


_DETAIL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
:root {
  --orange: #E5531A; --orange-hover: #C64514;
  --bg: #0B0B0B; --surface: #111113; --raised: #1B1B20;
  --border: #2A2A2A; --text: #F4F4F5; --muted: #9B9BA8;
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;
}
*, *::before, *::after { box-sizing: border-box; }
body { background: var(--bg); color: var(--text); margin: 0;
  font-family: var(--font-sans); font-size: 15px; line-height: 1.7;
  -webkit-font-smoothing: antialiased; }
a { color: var(--orange); text-decoration: none; }
a:hover { color: var(--orange-hover); }
.page-wrap { max-width: 860px; margin: 0 auto; padding: 48px clamp(16px,4vw,48px) 96px; }
.back-link { display: inline-flex; align-items: center; gap: 6px;
  font-family: var(--font-mono); font-size: 11px; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted);
  margin-bottom: 40px; }
.back-link:hover { color: var(--text); }
h1 { font-size: clamp(24px,4vw,36px); font-weight: 800; letter-spacing: -0.03em;
  line-height: 1.1; margin: 0 0 8px; color: var(--text); }
.skill-category { font-family: var(--font-mono); font-size: 11px; font-weight: 600;
  letter-spacing: 0.1em; text-transform: uppercase; color: var(--orange);
  margin-bottom: 32px; display: block; }
h2 { font-size: 1.15rem !important; font-weight: 700 !important; margin: 36px 0 12px !important;
  padding-bottom: 8px !important; border-bottom: 1px solid var(--border) !important; color: #E5531A !important; }
h3 { font-size: 1rem !important; font-weight: 700 !important; margin: 24px 0 8px !important; color: var(--text) !important; }
h4 { font-size: 0.9rem !important; font-weight: 700 !important; margin: 20px 0 6px !important; color: var(--muted) !important; text-transform: uppercase !important; letter-spacing: 0.06em !important; }
p { margin: 0 0 14px; }
ul, ol { margin: 0 0 16px; padding-left: 1.4rem; }
li { margin-bottom: 6px; }
code { font-family: var(--font-mono); font-size: 0.855em;
  background: rgba(255,255,255,0.07); padding: 2px 6px; border-radius: 3px; color: #F2A07A; }
pre { background: var(--surface); border: 1px solid var(--border); border-radius: 6px;
  padding: 20px 24px; overflow-x: auto; margin: 0 0 20px; }
pre code { background: none; padding: 0; color: var(--text); font-size: 0.85rem; }
blockquote { border-left: 3px solid var(--orange); margin: 0 0 16px;
  padding: 10px 18px; background: var(--surface); border-radius: 0 4px 4px 0; }
blockquote p { margin: 0; color: var(--muted); }
hr { border: none; border-top: 1px solid var(--border); margin: 32px 0; }
strong { font-weight: 600; }
"""


def generate_detail_page(e: SkillEntry, skills_dir: Path) -> str | None:
    """Render a SKILL.md as a branded HTML page. Returns HTML string or None if file missing."""
    skill_md = skills_dir / e.rel_path / "SKILL.md"
    if not skill_md.exists():
        return None
    raw = skill_md.read_text(encoding="utf-8", errors="replace")
    body = FRONTMATTER_RE.sub("", raw).strip()
    # strip metadata lines before the first heading (e.g. "Manual: [...]")
    body = re.sub(r"^[A-Za-z][A-Za-z\s]+:\s*\[.+\]\(.+\)\s*\n?", "", body, flags=re.MULTILINE)
    # strip the H1 title (we render it separately in the page header)
    body = re.sub(r"^#\s+.+\n?", "", body, count=1, flags=re.MULTILINE).strip()
    content_html = _md_to_html(body)
    category_label = _category_label(e.category)
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="engineering">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_mod.escape(e.name)} — abd.works</title>
<script src="/commons/brand-nav.js"></script>
<style>{_DETAIL_CSS}</style>
</head>
<body>
<div class="page-wrap">
  <a class="back-link" href="/abd-skills-catalog/">← Skill Catalog</a>
  <h1>{html_mod.escape(e.name)}</h1>
  <span class="skill-category">{html_mod.escape(category_label)}</span>
  {content_html}
</div>
</body>
</html>"""


def generate_detail_pages(
    by_category: dict[str, list[SkillEntry]],
    skills_dir: Path,
    output_dir: Path,
) -> int:
    count = 0
    for entries in by_category.values():
        for e in entries:
            html = generate_detail_page(e, skills_dir)
            if html is None:
                continue
            page_dir = output_dir / e.rel_path
            page_dir.mkdir(parents=True, exist_ok=True)
            (page_dir / "index.html").write_text(html, encoding="utf-8")
            count += 1
    return count


def generate_agent_detail_page(a: AgentEntry, agents_dir: Path) -> str | None:
    agent_md = agents_dir / a.folder / "AGENT.md"
    if not agent_md.exists():
        return None
    raw = agent_md.read_text(encoding="utf-8", errors="replace")
    body = FRONTMATTER_RE.sub("", raw).strip()
    body = re.sub(r"^#\s+.+\n?", "", body, count=1, flags=re.MULTILINE).strip()
    content_html = _md_to_html(body)
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="engineering">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_mod.escape(a.name)} — abd.works</title>
<script src="/commons/brand-nav.js"></script>
<style>{_DETAIL_CSS}</style>
</head>
<body>
<div class="page-wrap">
  <a class="back-link" href="/abd-skills-catalog/">← Skill Catalog</a>
  <h1>{html_mod.escape(a.name)}</h1>
  <span class="skill-category">Agent</span>
  {content_html}
</div>
</body>
</html>"""


def generate_agent_detail_pages(
    agents: list[AgentEntry],
    agents_dir: Path,
    output_dir: Path,
) -> int:
    count = 0
    for a in agents:
        html = generate_agent_detail_page(a, agents_dir)
        if html is None:
            continue
        page_dir = output_dir / "agents" / a.folder
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(html, encoding="utf-8")
        count += 1
    return count


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate categorised skill catalogue.")
    parser.add_argument("--skills-dir", type=Path, required=True,
                        help="Root skills folder.")
    parser.add_argument("--agents-dir", type=Path, default=None,
                        help="Root agents folder (optional).")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Where to write outputs. Defaults to --skills-dir.")
    args = parser.parse_args()

    skills_dir: Path = args.skills_dir.resolve()
    output_dir: Path = (args.output_dir or skills_dir).resolve()

    if not skills_dir.is_dir():
        raise SystemExit(f"Skills directory not found: {skills_dir}")

    by_category = discover_skills(skills_dir)
    total = sum(len(v) for v in by_category.values())
    if not total:
        raise SystemExit(f"No SKILL.md files found under {skills_dir}")

    # agents (optional)
    agents: list[AgentEntry] = []
    agents_dir: Path | None = args.agents_dir.resolve() if args.agents_dir else None
    if agents_dir and agents_dir.is_dir():
        agents = discover_agents(agents_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / "skill-inventory.md"
    md_path.write_text(generate_markdown(by_category), encoding="utf-8")
    print(f"  wrote {md_path}  ({total} skills across {len(by_category)} categories)")

    html_path = output_dir / "index.html"
    html_path.write_text(generate_html_with_agents(by_category, agents), encoding="utf-8")
    print(f"  wrote {html_path}")

    detail_count = generate_detail_pages(by_category, skills_dir, output_dir)
    print(f"  wrote {detail_count} skill detail pages")

    if agents and agents_dir:
        agent_detail_count = generate_agent_detail_pages(agents, agents_dir, output_dir)
        print(f"  wrote {agent_detail_count} agent detail pages")


if __name__ == "__main__":
    main()
