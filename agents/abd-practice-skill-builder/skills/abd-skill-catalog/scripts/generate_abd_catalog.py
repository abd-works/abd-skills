#!/usr/bin/env python3
"""Scan repo-root skills/ and agents/; emit outline.md + HTML under repo catalog/.

Lives under agents/abd-practice-skill-builder/skills/abd-skill-catalog/; repo root is
detected by walking up until both skills/ and agents/ exist.
"""

from __future__ import annotations

import argparse
import html as html_mod
import json
import re
import shutil
import sys
import textwrap
from pathlib import Path
from typing import NamedTuple
from urllib.parse import quote

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / "templates"


def _repo_root_from_skill_package(skill_pkg_dir: Path) -> Path:
    """Walk upward until a directory contains both top-level skills/ and agents/."""
    p = skill_pkg_dir.resolve()
    for _ in range(16):
        if (p / "skills").is_dir() and (p / "agents").is_dir():
            return p
        parent = p.parent
        if parent == p:
            break
        p = parent
    raise RuntimeError(
        f"Could not find repository root (folder with skills/ and agents/) starting from {skill_pkg_dir}"
    )


_REPO_ROOT_DEFAULT = _repo_root_from_skill_package(SKILL_DIR)
_EXECUTE_RULES_SCRIPTS = _REPO_ROOT_DEFAULT / "skills" / "execute_using_rules" / "scripts"
if str(_EXECUTE_RULES_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_EXECUTE_RULES_SCRIPTS))
import frontmatter_tags  # noqa: E402


def _catalog_cli_invocation(repo_root: Path) -> str:
    script = SCRIPT_DIR / "generate_abd_catalog.py"
    try:
        rel = script.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        rel = "agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py"
    return f"python {rel}"

# Subtitle in generated pages (repo output folder is <root>/catalog/).
CATALOG_BRAND_HTML = "<strong>Agile by Design</strong> &middot; catalog"

# GitHub slug for `npx skills add owner/repo@skill` (skills.sh / Open Agent Skills CLI).
NPX_SKILLS_REPO_SLUG = "agilebydesign/agilebydesign-skills"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
YAML_FIELD_RE = re.compile(r"^(\w[\w-]*):\s*(.+)", re.MULTILINE)
YAML_BLOCK_RE = re.compile(
    r"^(\w[\w-]*):\s*>-?\s*\n((?:[ \t]+.*\n?)+)", re.MULTILINE
)

KNOWN_DIR_SUMMARY: dict[str, str] = {
    "rules": "Practice rules (DO/DON'T) and constraints used with scanners.",
    "templates": "Authoring templates and structural skeletons.",
    "scripts": "Build, catalogue, validation, or packaging automation.",
    "docs": "Human-oriented documentation for the package.",
    "content": "Source parts merged into agent instructions or outputs.",
    "roles": "Persona playbooks for multi-role agents.",
    "test": "Automated tests for the agent or skill package.",
    "skills": "Nested skills shipped inside an agent package.",
    "context": "Optional engagement or corpus context.",
    "images": "Figures referenced by nearby HTML or markdown docs.",
}

# Open repo file/folder links in a new tab so the catalogue page (dark UI) stays open.
_REPO_LINK_NEW_TAB = ' target="_blank" rel="noopener noreferrer"'

# Max nesting depth for folder trees on detail pages (prevents huge trees).
_FILE_TREE_MAX_DEPTH = 8
# <details open> only when depth <= this value. -1 = all folders start collapsed (match skill doc sections).
_FILE_TREE_DEFAULT_EXPAND_DEPTH = -1


class SkillEntry(NamedTuple):
    name: str
    dir_name: str
    summary: str
    description: str
    rel_skill_md: str
    # Path from repo root to the skill package folder (e.g. skills/foo or agents/.../skills/foo).
    pkg_rel_posix: str
    # catalogue “Agile Garden” lists: practice | foundational | "" (omit)
    garden_tier: str
    garden_order: int


class AgentEntry(NamedTuple):
    name: str
    dir_name: str
    entry_file: str
    summary: str
    description: str
    rel_entry_md: str
    garden_include: bool
    garden_order: int


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
    tags_ordered = frontmatter_tags.ordered_tags_from_frontmatter_block(block)
    if tags_ordered:
        fields["tags"] = tags_ordered
    elif fields.get("tags"):
        fields["tags"] = frontmatter_tags.normalize_tags_scalar(fields["tags"])
    return fields


def _extract_section(body: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    m = pattern.search(body)
    if not m:
        return None
    return m.group(1).strip()


def _strip_md(text: str) -> str:
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def _truncate(text: str, limit: int = 200) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(".,;: ") + " …"


def _h1_title(body: str) -> str | None:
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return m.group(1).strip() if m else None


def _opening_blurb_after_h1(body: str, max_len: int = 260) -> str:
    lines = body.splitlines()
    i = 0
    if i < len(lines) and lines[i].lstrip().startswith("#"):
        i += 1
    parts: list[str] = []
    while i < len(lines):
        if lines[i].startswith("##"):
            break
        s = lines[i].strip()
        if s == "---":
            i += 1
            continue
        if not s:
            if parts:
                break
            i += 1
            continue
        parts.append(s)
        i += 1
    joined = _strip_md(" ".join(parts))
    return _truncate(joined, max_len) if joined else ""


def _intro_after_h1_until_section(body: str, max_len: int = 2000) -> str:
    """All prose after the title # line until the first ## heading (skips YAML --- only at block start).

    Used for catalogue detail pages when ## Purpose and YAML description are missing, so agent pages
    match skill pages (short multi-paragraph summary, not the full AGENT.md).
    """
    lines = body.splitlines()
    i = 0
    if i < len(lines) and lines[i].lstrip().startswith("#"):
        i += 1
    parts: list[str] = []
    blank_run = 0
    while i < len(lines):
        raw = lines[i]
        if raw.startswith("##"):
            break
        s = raw.strip()
        if s.startswith("```"):
            break
        if s == "---":
            i += 1
            continue
        if not s:
            blank_run += 1
            if blank_run >= 2 and parts:
                break
            i += 1
            continue
        blank_run = 0
        parts.append(s)
        i += 1
    joined = _strip_md(" ".join(parts))
    return _truncate(joined, max_len) if joined else ""


def _table_blurb(fm: dict[str, str], body: str, max_len: int = 300) -> str:
    """One paragraph for summary tables and HTML cards: short one-liner, else description, else Purpose, …"""
    one = (fm.get("catalogue_one_liner") or "").strip()
    if one and one != "---":
        flat = _strip_md(" ".join(one.split()))
        return _truncate(flat, max_len)
    desc = fm.get("description", "").strip()
    if desc and desc != "---":
        flat = _strip_md(" ".join(desc.split()))
        return _truncate(flat, max_len)
    purpose = _extract_section(body, "Purpose")
    if purpose:
        flat = _strip_md(re.sub(r"\s+", " ", purpose.replace("\n", " ")))
        return _truncate(flat, max_len)
    blurb = _opening_blurb_after_h1(body, max_len=700)
    if blurb:
        return _truncate(blurb, max_len)
    return _truncate(_strip_md(body), max_len)


def _description_skill(fm: dict[str, str], body: str) -> str:
    purpose = _extract_section(body, "Purpose")
    if purpose:
        return _truncate(_strip_md(purpose), 900)
    desc = fm.get("description", "")
    if desc:
        return _truncate(_strip_md(desc), 900)
    return _truncate(_strip_md(body), 500)


def _description_agent(fm: dict[str, str], body: str) -> str:
    purpose = _extract_section(body, "Purpose")
    if purpose:
        return _truncate(_strip_md(purpose), 1200)
    desc = fm.get("description", "")
    if desc:
        return _truncate(_strip_md(desc), 1200)
    return _truncate(_strip_md(body), 800)


def _norm_catalog_garden_tier(raw: str) -> str:
    v = (raw or "").strip().lower()
    return v if v in ("practice", "foundational") else ""


def _catalog_garden_order(fm: dict[str, str]) -> int:
    raw = (fm.get("catalog_garden_order") or "").strip()
    if raw.isdigit():
        return int(raw)
    return 999


def _catalog_listing_excluded(package_dir: Path, fm: dict[str, str]) -> bool:
    """True if this skill/agent package must not appear in hub, outline, grids, or detail pages."""
    raw = (fm.get("catalog_ready") or "").strip().lower()
    if raw in ("false", "no", "0", "draft", "not-ready", "not_ready"):
        return True
    for t in frontmatter_tags.parse_tags_list(fm.get("tags", "")):
        n = t.strip().lower().replace("_", "-")
        if n in ("not-ready", "wip", "draft", "hidden"):
            return True
    cfg_path = package_dir / "skill-config.json"
    if cfg_path.is_file():
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, TypeError):
            data = {}
        v = data.get("catalog_ready")
        if v is False:
            return True
        if isinstance(v, str) and v.strip().lower() in ("false", "no", "0", "draft", "not-ready", "not_ready"):
            return True
    return False


def _skill_entry_from_package_dir(child: Path, repo_root: Path) -> SkillEntry | None:
    skill_md = child / "SKILL.md"
    if not skill_md.is_file():
        return None
    text = skill_md.read_text(encoding="utf-8-sig", errors="replace")
    fm = _parse_frontmatter(text)
    body = FRONTMATTER_RE.sub("", text).strip()
    if _catalog_listing_excluded(child, fm):
        return None
    name = fm.get("name", child.name)
    rel = skill_md.relative_to(repo_root).as_posix()
    pkg_rel = child.relative_to(repo_root).as_posix()
    summary = _table_blurb(fm, body)
    summary = _readme_catalogue_card_summary(child / "README.md", summary, fm)
    tier = _norm_catalog_garden_tier(fm.get("catalog_garden_tier", ""))
    return SkillEntry(
        name=name,
        dir_name=child.name,
        summary=summary,
        description=_description_skill(fm, body),
        rel_skill_md=rel,
        pkg_rel_posix=pkg_rel,
        garden_tier=tier,
        garden_order=_catalog_garden_order(fm),
    )


def discover_skills(skills_dir: Path, repo_root: Path) -> list[SkillEntry]:
    """Top-level repo skills/ plus agents/*/skills/ packages with SKILL.md."""
    seen: set[str] = set()
    out: list[SkillEntry] = []

    def push(child: Path) -> None:
        ent = _skill_entry_from_package_dir(child, repo_root)
        if ent is None:
            return
        if ent.dir_name in seen:
            raise SystemExit(
                f"Duplicate skill package folder name {ent.dir_name!r} (second at {child}). "
                "Rename one package so catalogue detail page ids stay unique."
            )
        seen.add(ent.dir_name)
        out.append(ent)

    for child in sorted(skills_dir.iterdir()):
        if child.is_dir():
            push(child)

    # Nested packages under agents/<agent>/skills/ are not top-level `npx` skills by default.
    # Include only those that opt in with YAML `catalog_garden_tier: practice|foundational`
    # (same signal as Agile Garden), so agent-local pipeline skills stay off the grid.
    agents_root = repo_root / "agents"
    if agents_root.is_dir():
        for agent_dir in sorted(agents_root.iterdir()):
            if not agent_dir.is_dir():
                continue
            nested = agent_dir / "skills"
            if not nested.is_dir():
                continue
            for child in sorted(nested.iterdir()):
                if not child.is_dir():
                    continue
                skill_md = child / "SKILL.md"
                if not skill_md.is_file():
                    continue
                peek = skill_md.read_text(encoding="utf-8-sig", errors="replace")
                fm_peek = _parse_frontmatter(peek)
                if not _norm_catalog_garden_tier(fm_peek.get("catalog_garden_tier", "")):
                    continue
                push(child)

    return out


def _agent_catalog_garden_include(fm: dict[str, str]) -> bool:
    v = (fm.get("catalog_garden") or "true").strip().lower()
    return v not in ("false", "no", "0")


def discover_agents(agents_dir: Path, repo_root: Path) -> list[AgentEntry]:
    out: list[AgentEntry] = []
    for child in sorted(agents_dir.iterdir()):
        if not child.is_dir():
            continue
        entry_name: str | None = None
        for fname in ("AGENT.md", "AGENTS.md", "SKILL.md"):
            p = child / fname
            if p.exists():
                entry_name = fname
                text = p.read_text(encoding="utf-8-sig", errors="replace")
                break
        if not entry_name:
            continue
        fm = _parse_frontmatter(text)
        body = FRONTMATTER_RE.sub("", text).strip()
        if _catalog_listing_excluded(child, fm):
            continue
        # Catalogue titles use package id (kebab-case folder name), not H1 display names.
        name = child.name
        rel = (child / entry_name).relative_to(repo_root).as_posix()
        summary = _table_blurb(fm, body)
        summary = _readme_catalogue_card_summary(child / "README.md", summary, fm)
        out.append(
            AgentEntry(
                name=name,
                dir_name=child.name,
                entry_file=entry_name,
                summary=summary,
                description=_description_agent(fm, body),
                rel_entry_md=rel,
                garden_include=_agent_catalog_garden_include(fm),
                garden_order=_catalog_garden_order(fm),
            )
        )
    return out


def _file_blurb(path: Path, max_len: int = 180) -> str:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "Unreadable file."
    for line in raw.splitlines():
        s = line.strip()
        if not s or s == "---":
            continue
        s = re.sub(r"^#+\s*", "", s)
        s = _strip_md(s)
        if len(s) < 8:
            continue
        return _truncate(s, max_len)
    return "No preview available."


def layout_lines(repo_root: Path, package_dir: Path, md_prefix: str) -> list[str]:
    """Markdown bullets: files with blurb+link; directories one summary line."""
    lines: list[str] = []
    if not package_dir.is_dir():
        return lines
    try:
        kids = sorted(package_dir.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except OSError:
        return ["- (could not read directory)"]
    for p in kids:
        rel = p.relative_to(repo_root).as_posix()
        if p.is_dir():
            link = _outline_href_for_rules_folder(package_dir, p)
            if link is None:
                link = f"{md_prefix}{rel}"
            try:
                cnt = len([x for x in p.iterdir() if not x.name.startswith(".")])
            except OSError:
                cnt = 0
            summary = _folder_blurb_from_path(p, cnt)
            lines.append(f"- **[{p.name}/]({link})** — {summary}")
        else:
            doc_link = _outline_href_for_package_md(repo_root, package_dir, p)
            link = doc_link if doc_link is not None else f"{md_prefix}{rel}"
            blurb = _file_blurb(p)
            lines.append(f"- [{p.name}]({link}) — {blurb}")
    return lines


def _path_up_to_ancestor(from_dir: Path, ancestor: Path) -> str:
    """Return a relative URL prefix like ../../ to ascend from from_dir to ancestor."""
    from_dir = from_dir.resolve()
    ancestor = ancestor.resolve()
    try:
        rel = from_dir.relative_to(ancestor)
    except ValueError:
        return ""
    n = len(rel.parts)
    if n == 0:
        return ""
    return "../" * n


def _h(text: str) -> str:
    return html_mod.escape(text)


def _npx_skills_install_block(skill_package_name: str) -> str:
    """HTML: copy-paste `npx skills add` line using @skill (matches `npx skills` discover names)."""
    name = skill_package_name.strip()
    cmd = f"npx skills add {NPX_SKILLS_REPO_SLUG}@{name} -y"
    return (
        '<section class="install-block" aria-labelledby="install-npx-heading">\n'
        '  <h2 id="install-npx-heading">Install with npx</h2>\n'
        '  <p class="install-hint">Install this package from GitHub into your project or global agent '
        'skills directory (see <a href="https://skills.sh/">skills.sh</a> / Open Agent Skills).</p>\n'
        '  <pre class="install-snippet"><code>'
        + _h(cmd)
        + "</code></pre>\n"
        "</section>\n"
    )


def _repo_href(href_to_repo: str, rel_posix: str) -> str:
    rel_posix = rel_posix.replace("\\", "/").strip("/")
    if not rel_posix:
        return href_to_repo
    parts = [quote(p, safe="") for p in rel_posix.split("/") if p]
    return href_to_repo + "/".join(parts)


def _should_skip_catalog_md(rel_parts: tuple[str, ...]) -> bool:
    """Skip dot-directories and hidden path segments when mirroring .md into catalog/doc/."""
    return any(part.startswith(".") for part in rel_parts)


def _package_markdown_catalog_href_from_detail_page(
    repo_root: Path, file_path: Path, package_dir: Path
) -> str | None:
    """Any <pkg>/**/*.md or *.txt → ../doc/<skill|agent>/<pkg>/…/file.html from catalog/skill|agent/<pkg>.html."""
    if file_path.suffix.lower() not in {".md", ".txt"}:
        return None
    try:
        rel_under_pkg = file_path.relative_to(package_dir)
    except ValueError:
        return None
    if _should_skip_catalog_md(rel_under_pkg.parts):
        return None
    try:
        rel_pkg = package_dir.relative_to(repo_root)
    except ValueError:
        return None
    if len(rel_pkg.parts) < 2 or rel_pkg.parts[0] not in ("skills", "agents"):
        return None
    kind = "skill" if rel_pkg.parts[0] == "skills" else "agent"
    pkg = rel_pkg.parts[1]
    rel_html = rel_under_pkg.with_suffix(".html").as_posix()
    segs = [quote(s, safe="") for s in rel_html.split("/") if s]
    return f"../doc/{kind}/{quote(pkg, safe='')}/" + "/".join(segs)


def _outline_href_for_package_md(
    repo_root: Path, package_dir: Path, file_path: Path
) -> str | None:
    """outline.md lives in catalog/: doc/<skill|agent>/<pkg>/….html for top-level .md only."""
    if file_path.suffix.lower() != ".md" or file_path.parent != package_dir:
        return None
    try:
        rel_pkg = package_dir.relative_to(repo_root)
    except ValueError:
        return None
    if len(rel_pkg.parts) < 2 or rel_pkg.parts[0] not in ("skills", "agents"):
        return None
    kind = "skill" if rel_pkg.parts[0] == "skills" else "agent"
    pkg = rel_pkg.parts[1]
    rel_html = file_path.relative_to(package_dir).with_suffix(".html").as_posix()
    segs = [quote(s, safe="") for s in rel_html.split("/") if s]
    return f"doc/{kind}/{quote(pkg, safe='')}/" + "/".join(segs)


def _outline_href_for_rules_folder(package_dir: Path, rules_dir: Path) -> str | None:
    """Point rules/ folder entry at the skill or agent detail page #entry-contents."""
    if rules_dir.name != "rules" or not rules_dir.is_dir():
        return None
    root = package_dir.parent.name
    if root == "skills":
        return f"skill/{quote(package_dir.name, safe='')}.html#entry-contents"
    if root == "agents":
        return f"agent/{quote(package_dir.name, safe='')}.html#entry-contents"
    return None


_TABLE_SEPARATOR_CELL_RE = re.compile(r"^:?-{3,}:?$")


def _catalog_href_from_md(href: str) -> str:
    """Relative *.md links in mirrored docs → *.html for static catalog."""
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "http://", "https://")):
        return href
    if href.endswith(".md"):
        return href[:-3] + ".html"
    return href


def _inline_format(s: str) -> str:
    """Inline: **bold**, *italic*, [label](href). Escapes plain text; href normalized for sibling .md."""
    if not s:
        return ""
    parts: list[str] = []
    i = 0
    n = len(s)
    while i < n:
        if s.startswith("**", i):
            j = s.find("**", i + 2)
            if j == -1:
                parts.append(_h(s[i:]))
                break
            inner = s[i + 2 : j]
            parts.append("<strong>" + _inline_format(inner) + "</strong>")
            i = j + 2
            continue
        if s[i] == "[":
            close_lb = s.find("]", i + 1)
            if (
                close_lb != -1
                and close_lb + 1 < n
                and s[close_lb + 1] == "("
            ):
                close_paren = s.find(")", close_lb + 2)
                if close_paren != -1:
                    label = s[i + 1 : close_lb]
                    href_raw = s[close_lb + 2 : close_paren]
                    href = _catalog_href_from_md(href_raw)
                    plain = label.strip()
                    if plain.endswith(".md") and href == _catalog_href_from_md(plain):
                        link_inner = _h(plain[:-3])
                    else:
                        link_inner = _inline_format(label)
                    parts.append('<a href="' + _h(href) + '">' + link_inner + "</a>")
                    i = close_paren + 1
                    continue
        if s[i] == "*" and (i + 1 >= n or s[i + 1] != "*"):
            j = s.find("*", i + 1)
            if j != -1 and j > i + 1:
                inner = s[i + 1 : j]
                parts.append("<em>" + _inline_format(inner) + "</em>")
                i = j + 1
                continue
        parts.append(_h(s[i]))
        i += 1
    return "".join(parts)


def _is_markdown_table_row(stripped: str) -> bool:
    return stripped.startswith("|") and stripped.count("|") >= 2


def _split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _is_table_separator_row(cells: list[str]) -> bool:
    if not cells:
        return False
    for c in cells:
        t = c.strip()
        if not t:
            continue
        if not _TABLE_SEPARATOR_CELL_RE.match(t):
            return False
    return True


def _markdown_table_to_html(table_lines: list[str]) -> str:
    rows = [_split_table_row(line) for line in table_lines]
    if not rows:
        return ""
    max_cols = max(len(r) for r in rows)
    rows = [r + [""] * (max_cols - len(r)) for r in rows]
    parts: list[str] = ['<table class="md-table">']
    start_body = 0
    if len(rows) >= 2 and _is_table_separator_row(rows[1]):
        parts.append("<thead><tr>")
        for c in rows[0]:
            parts.append("<th>" + _inline_format(c) + "</th>")
        parts.append("</tr></thead>")
        start_body = 2
    parts.append("<tbody>")
    for r in rows[start_body:]:
        parts.append("<tr>")
        for c in r:
            parts.append("<td>" + _inline_format(c) + "</td>")
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return '<div class="md-table-wrap">' + "".join(parts) + "</div>"


def _markdown_rule_to_html(text: str) -> str:
    """Markdown → HTML for bundled .md pages: headings, lists, tables, HR, fences, paragraphs, inline marks."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if FRONTMATTER_RE.match(text):
        text = FRONTMATTER_RE.sub("", text).strip()
    lines = text.split("\n")
    out: list[str] = []
    in_code = False
    code_buf: list[str] = []
    para: list[str] = []
    in_ul = False

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def flush_para() -> None:
        nonlocal para
        if not para:
            return
        close_ul()
        out.append("<p>" + _inline_format(" ".join(para)) + "</p>")
        para = []

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                out.append("<pre><code>" + _h("\n".join(code_buf)) + "</code></pre>")
                code_buf = []
                in_code = False
            else:
                flush_para()
                close_ul()
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue
        if stripped == "":
            flush_para()
            close_ul()
            i += 1
            continue
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):
            flush_para()
            close_ul()
            out.append("<hr>")
            i += 1
            continue
        if _is_markdown_table_row(stripped):
            flush_para()
            close_ul()
            tbl: list[str] = []
            while i < len(lines):
                st = lines[i].rstrip("\n").strip()
                if st == "":
                    break
                if not _is_markdown_table_row(st):
                    break
                tbl.append(st)
                i += 1
            out.append(_markdown_table_to_html(tbl))
            continue
        if stripped.startswith("#"):
            flush_para()
            close_ul()
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped.lstrip("#").strip()
            tag = min(max(level, 1), 6)
            out.append(f"<h{tag}>{_inline_format(title)}</h{tag}>")
            i += 1
            continue
        m = re.match(r"^[-*]\s+(.*)", stripped)
        if m:
            flush_para()
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append("<li>" + _inline_format(m.group(1)) + "</li>")
            i += 1
            continue
        para.append(stripped)
        i += 1
    if in_code and code_buf:
        out.append("<pre><code>" + _h("\n".join(code_buf)) + "</code></pre>")
    flush_para()
    close_ul()
    return "\n".join(out) if out else "<p>(empty)</p>"


def _split_markdown_at_h2(body: str) -> list[tuple[str | None, str]]:
    """Split Markdown into (h2 title or None for preamble, section text without the ## line)."""
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    lines = body.split("\n")
    out: list[tuple[str | None, str]] = []
    cur_title: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal cur_title, buf
        text = "\n".join(buf).strip()
        if cur_title is not None:
            out.append((cur_title, text))
        elif text:
            out.append((None, text))
        cur_title = None
        buf.clear()

    for line in lines:
        if line.startswith("## ") and not line.startswith("###"):
            flush()
            cur_title = line[3:].strip()
        else:
            buf.append(line)
    flush()
    return out


def _chunk_is_only_solitary_h1(chunk: str) -> bool:
    lines = [ln.strip() for ln in chunk.strip().split("\n") if ln.strip()]
    return len(lines) == 1 and lines[0].startswith("# ") and not lines[0].startswith("##")


def _heading_slug_for_id(title: str, used: dict[str, int]) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", _strip_md(title).lower()).strip("-") or "section"
    c = used.get(base, 0) + 1
    used[base] = c
    return base if c == 1 else f"{base}-{c}"


def _html_package_md_collapsible_sections(body: str) -> str:
    """Each top-level ## section (plus optional preamble) → <details> closed by default."""
    if not body.strip():
        return '<p class="entry-caption">(empty document)</p>'
    sections = _split_markdown_at_h2(body)
    parts: list[str] = []
    used_slugs: dict[str, int] = {}
    overview_used = False
    for title, chunk in sections:
        if title is not None and not chunk.strip():
            continue
        if title is None and _chunk_is_only_solitary_h1(chunk):
            continue
        if title is None:
            summary_plain = "Overview"
            sid = "md-overview" if not overview_used else "md-overview-2"
            overview_used = True
        else:
            summary_plain = _strip_md(title)
            sid = _heading_slug_for_id(title, used_slugs)
        inner = _markdown_rule_to_html(chunk)
        parts.append(
            f'<details class="entry-md-section" id="{_h(sid)}">'
            f'<summary class="entry-md-section__summary">{_h(summary_plain)}</summary>'
            f'<div class="entry-md-section__body">{inner}</div>'
            f"</details>"
        )
    return "\n".join(parts) if parts else '<p class="entry-caption">(no sections)</p>'


def write_package_markdown_pages(
    output_catalog_dir: Path,
    repo_root: Path,
    skills: list[SkillEntry],
    agents: list[AgentEntry],
    css: str,
) -> int:
    """Emit catalog/doc/<skill|agent>/<pkg>/…/*.html for every package .md (mirrors subfolders). Returns page count."""
    tpl = _load_template("page-markdown-doc.html")
    brand = CATALOG_BRAND_HTML
    doc_root = output_catalog_dir / "doc"
    if doc_root.exists():
        shutil.rmtree(doc_root)
    legacy_rule = output_catalog_dir / "rule"
    if legacy_rule.exists():
        shutil.rmtree(legacy_rule)
    doc_root.mkdir(parents=True)
    count = 0

    def badge_for(rel_under_pkg: Path) -> str:
        if rel_under_pkg.parts and rel_under_pkg.parts[0] == "rules":
            return "Rule"
        if rel_under_pkg.suffix.lower() == ".txt":
            return "Plain text"
        return "Markdown"

    def write_pkg_md(pkg_dir: Path, kind: str, display_name: str) -> None:
        nonlocal count
        if not pkg_dir.is_dir():
            return
        pkg = pkg_dir.name
        source_files = sorted(
            list(pkg_dir.rglob("*.md")) + list(pkg_dir.rglob("*.txt"))
        )
        for md in source_files:
            if not md.is_file():
                continue
            try:
                rel_under_pkg = md.relative_to(pkg_dir)
            except ValueError:
                continue
            if _should_skip_catalog_md(rel_under_pkg.parts):
                continue
            dest = doc_root / kind / pkg / rel_under_pkg.with_suffix(".html")
            dest.parent.mkdir(parents=True, exist_ok=True)
            raw = md.read_text(encoding="utf-8", errors="replace")
            if md.suffix.lower() == ".txt":
                body_html = "<pre>" + _h(raw) + "</pre>"
            else:
                body_html = _markdown_rule_to_html(raw)
            rel_to_cat = dest.relative_to(output_catalog_dir)
            nav_prefix = "../" * len(rel_to_cat.parent.parts)
            back = f"{nav_prefix}{'skill' if kind == 'skill' else 'agent'}/{quote(pkg, safe='')}.html"
            relpos = rel_under_pkg.as_posix()
            title = f"ABD catalogue — {display_name} · {relpos}"
            h1 = relpos
            tagline = _file_blurb(md, max_len=400)
            if kind == "skill":
                nav_hub = _nav_cls("hub", "skills")
                nav_skills = _nav_cls("skills", "skills")
                nav_agents = _nav_cls("agents", "skills")
            else:
                nav_hub = _nav_cls("hub", "agents")
                nav_skills = _nav_cls("skills", "agents")
                nav_agents = _nav_cls("agents", "agents")
            html = (
                tpl.replace("{{CSS}}", css)
                .replace("{{TITLE}}", _h(title))
                .replace("{{BRAND}}", brand)
                .replace("{{BACK_HREF}}", back)
                .replace("{{BACK_LABEL}}", "← " + _h(display_name))
                .replace("{{BADGE}}", badge_for(rel_under_pkg))
                .replace("{{H1}}", _h(h1))
                .replace("{{TAGLINE}}", _h(tagline))
                .replace("{{NAV_PREFIX}}", nav_prefix)
                .replace("{{NAV_HUB}}", nav_hub)
                .replace("{{NAV_SKILLS}}", nav_skills)
                .replace("{{NAV_AGENTS}}", nav_agents)
                .replace("{{DOC_BODY}}", body_html)
            )
            dest.write_text(html, encoding="utf-8")
            count += 1

    for s in skills:
        write_pkg_md(repo_root / s.pkg_rel_posix, "skill", s.name)
    for a in agents:
        write_pkg_md(repo_root / "agents" / a.dir_name, "agent", a.name)

    return count


def _full_purpose_plain(fm: dict[str, str], body: str) -> str:
    """Detail-page description: ## Purpose, else YAML description, else intro after H1 (until next ##), else truncated body.

    Agents often omit ## Purpose; dumping the full AGENT.md breaks the same layout as skills (short prose, then diagram, then contents).
    """
    purpose = _extract_section(body, "Purpose")
    if purpose:
        return _strip_md(purpose)
    desc = fm.get("description", "")
    if desc.strip():
        return _strip_md(desc)
    intro = _intro_after_h1_until_section(body, max_len=2000)
    if intro.strip():
        return intro
    return _truncate(_strip_md(body), 1600)


def _load_package_source(package_dir: Path, kind: str) -> tuple[dict[str, str], str, str]:
    """kind is 'skill' or 'agent'. Returns (frontmatter, body, entry_filename)."""
    if kind == "skill":
        path = package_dir / "SKILL.md"
        if not path.is_file():
            return {}, "", ""
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = _parse_frontmatter(text)
        body = FRONTMATTER_RE.sub("", text).strip()
        return fm, body, "SKILL.md"
    for fname in ("AGENT.md", "AGENTS.md", "SKILL.md"):
        path = package_dir / fname
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            fm = _parse_frontmatter(text)
            body = FRONTMATTER_RE.sub("", text).strip()
            return fm, body, fname
    return {}, "", ""


def _load_readme_markdown(path: Path) -> tuple[dict[str, str], str]:
    """README.md body after optional YAML frontmatter."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    fm = _parse_frontmatter(raw)
    body = FRONTMATTER_RE.sub("", raw).strip() if FRONTMATTER_RE.match(raw) else raw.strip()
    return fm, body


def _escape_yaml_double_quoted_scalar(s: str) -> str:
    one = " ".join(s.split())
    return one.replace("\\", "\\\\").replace('"', '\\"')


def _readme_catalogue_card_summary(
    readme_path: Path, fallback: str, skill_fm: dict[str, str] | None = None
) -> str:
    """Card one-liner: SKILL ``catalogue_one_liner`` wins; else README summary / Overview; else fallback."""
    if skill_fm is not None:
        one = (skill_fm.get("catalogue_one_liner") or "").strip()
        if one and one != "---":
            return fallback
    if not readme_path.is_file():
        return fallback
    fm, body = _load_readme_markdown(readme_path)
    cs = fm.get("catalogue_summary", "").strip()
    if cs:
        return _truncate(_strip_md(cs), 300)
    ov = _extract_section(body, "Overview")
    if ov:
        flat = _strip_md(re.sub(r"\s+", " ", ov.replace("\n", " ")))
        return _truncate(flat, 300)
    return fallback


def _extract_first_fence_body(section: str) -> str:
    """First fenced ``` / ```ascii / ```text block in section; inner body only."""
    if not section:
        return ""
    text = section.replace("\r\n", "\n").replace("\r", "\n")
    for pat in (
        r"(?m)^```(?:ascii|text)\s*\n(.*?)^```\s*$",
        r"(?m)^```\s*\n(.*?)^```\s*$",
    ):
        m = re.search(pat, text, flags=re.DOTALL)
        if m:
            return m.group(1).strip()
    return ""


def _parse_catalog_readme_detail(readme_path: Path) -> tuple[str, str] | None:
    """Return (overview_markdown, ascii_diagram) from README; None if file missing."""
    if not readme_path.is_file():
        return None
    _, body = _load_readme_markdown(readme_path)
    overview = (_extract_section(body, "Overview") or "").strip()
    how = (_extract_section(body, "How it fits together") or "").strip()
    # Only fenced blocks become the diagram — never dump italic / prose into <pre>.
    ascii_block = _extract_first_fence_body(how)
    return overview, ascii_block


def _strip_catalog_maintainer_notes(overview_md: str) -> str:
    """Remove italic maintainer hints from catalogue README overviews."""
    lines = [ln for ln in overview_md.splitlines() if not ln.strip().startswith("_Maintainer")]
    return "\n".join(lines).strip()


_LIST_LINE_RE = re.compile(r"^( *)- (.*)$")


def _inline_markdown_spans(s: str) -> str:
    """Convert `` `code` `` and **bold** to HTML; escape all other characters."""
    out: list[str] = []
    i = 0
    n = len(s)
    while i < n:
        if s.startswith("**", i):
            j = s.find("**", i + 2)
            if j != -1:
                out.append("<strong>")
                out.append(html_mod.escape(s[i + 2 : j]))
                out.append("</strong>")
                i = j + 2
                continue
        if s[i] == "`":
            j = s.find("`", i + 1)
            if j != -1:
                out.append("<code>")
                out.append(html_mod.escape(s[i + 1 : j]))
                out.append("</code>")
                i = j + 1
                continue
        out.append(html_mod.escape(s[i]))
        i += 1
    return "".join(out)


class _LiNode:
    __slots__ = ("level", "html", "children")

    def __init__(self, level: int, html: str) -> None:
        self.level = level
        self.html = html
        self.children: list[_LiNode] = []


def _md_nested_list_to_html(lines: list[str]) -> str:
    """Markdown-style nested lists (2 spaces per level); inline ** and ` in item text."""
    dummy = _LiNode(-1, "")
    stack: list[_LiNode] = [dummy]
    for line in lines:
        m = _LIST_LINE_RE.match(line.rstrip("\n"))
        if not m:
            joined = "\n".join(lines)
            return f"<p>{_h(joined).replace(chr(10), '<br>')}</p>"
        indent, raw = m.group(1), m.group(2)
        level = len(indent) // 2
        html = _inline_markdown_spans(raw)
        node = _LiNode(level, html)
        while len(stack) > 1 and stack[-1].level >= level:
            stack.pop()
        stack[-1].children.append(node)
        stack.append(node)

    def li_inner(n: _LiNode) -> str:
        parts = [n.html]
        if n.children:
            parts.append("<ul>")
            for c in n.children:
                parts.append("<li>")
                parts.append(li_inner(c))
                parts.append("</li>")
            parts.append("</ul>")
        return "".join(parts)

    return "<ul>" + "".join(f"<li>{li_inner(c)}</li>" for c in dummy.children) + "</ul>"


def _collapse_blank_lines_between_list_items(text: str) -> str:
    """So `- a`\\n\\n`- b` becomes one markdown list (one HTML <ul>) for catalogue overviews."""
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        if not ln.strip():
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and out:
                prev_raw = out[-1]
                next_raw = lines[j]
                if _LIST_LINE_RE.match(prev_raw.rstrip("\n")) and _LIST_LINE_RE.match(
                    next_raw.rstrip("\n")
                ):
                    i = j
                    continue
        out.append(ln)
        i += 1
    return "\n".join(out)


def _split_overview_blocks(text: str) -> list[tuple[str, list[str]]]:
    """Split overview into alternating list blocks and paragraph blocks (blank line separates)."""
    blocks: list[tuple[str, list[str]]] = []
    cur_kind: str | None = None
    cur_lines: list[str] = []

    def flush() -> None:
        nonlocal cur_kind, cur_lines
        if not cur_lines or cur_kind is None:
            cur_lines = []
            cur_kind = None
            return
        blocks.append((cur_kind, cur_lines[:]))
        cur_lines = []
        cur_kind = None

    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped:
            flush()
            continue
        is_list = _LIST_LINE_RE.match(raw.rstrip("\n")) is not None
        kind = "list" if is_list else "para"
        if cur_kind is not None and kind != cur_kind:
            flush()
        cur_kind = kind
        cur_lines.append(raw.rstrip("\n"))
    flush()
    return blocks


def _para_block_to_html(lines: list[str]) -> str:
    parts = [_inline_markdown_spans(ln.strip()) for ln in lines if ln.strip()]
    if not parts:
        return ""
    inner = "<br>\n".join(parts) if len(parts) > 1 else parts[0]
    return f"<p>{inner}</p>"


def _plain_overview_to_html(text: str) -> str:
    """Turn README ## Overview into HTML: paragraphs, nested - lists, **bold**, `` `code` ``."""
    text = _collapse_blank_lines_between_list_items(
        _strip_catalog_maintainer_notes(text).strip()
    )
    if not text:
        return ""
    blocks = _split_overview_blocks(text)
    if not blocks:
        return ""
    out: list[str] = []
    for kind, lines in blocks:
        if kind == "list":
            out.append(_md_nested_list_to_html(lines))
        else:
            h = _para_block_to_html(lines)
            if h:
                out.append(h)
    return "\n".join(out)


def _ascii_placeholder_no_fence() -> str:
    return ""


def _ascii_placeholder_no_readme() -> str:
    return ""


def _ascii_catalog_ready(raw: str) -> str:
    """Drop scaffold TODO lines; keep only real diagram text for the HTML <pre>."""
    t = raw.strip()
    if not t:
        return ""
    low = t.lower()
    if "todo" in low and "replace" in low:
        return ""
    return t


def _html_how_it_fits_block(ascii_art: str) -> str:
    """Heading + <pre> when there is diagram text; nothing when empty."""
    t = _ascii_catalog_ready(ascii_art)
    if not t:
        return ""
    return (
        '<h2>How it fits together</h2>\n<pre class="ascii-diagram" role="img" '
        'aria-label="How it fits together">'
        + _h(t)
        + "</pre>\n"
    )


def scaffold_catalog_readmes(
    repo_root: Path,
    skills: list[SkillEntry],
    agents: list[AgentEntry],
) -> int:
    """Write skills/<dir>/README.md and agents/<dir>/README.md from templates only when missing.

    Never overwrites an existing README.md — improve weak READMEs in the editor
    or via an assistant; see abd-skill-catalog SKILL.md.
    """
    skill_tpl = (TEMPLATE_DIR / "catalog-readme-skill.md").read_text(encoding="utf-8", errors="replace")
    agent_tpl = (TEMPLATE_DIR / "catalog-readme-agent.md").read_text(encoding="utf-8", errors="replace")
    written = 0
    for s in skills:
        pkg = repo_root / s.pkg_rel_posix
        dest = pkg / "README.md"
        if dest.exists():
            continue
        fm, body, _ = _load_package_source(pkg, "skill")
        stub = _truncate(_full_purpose_plain(fm, body), 1200) if body or fm else s.summary
        text = (
            skill_tpl.replace("{{NAME}}", s.name)
            .replace("{{CATALOGUE_SUMMARY}}", _escape_yaml_double_quoted_scalar(s.summary))
            .replace("{{OVERVIEW_STUB}}", stub)
        )
        dest.write_text(text, encoding="utf-8", newline="\n")
        written += 1
    for a in agents:
        pkg = repo_root / "agents" / a.dir_name
        dest = pkg / "README.md"
        if dest.exists():
            continue
        fm, body, _ = _load_package_source(pkg, "agent")
        stub = _truncate(_full_purpose_plain(fm, body), 1200) if body or fm else a.summary
        text = (
            agent_tpl.replace("{{NAME}}", a.name)
            .replace("{{CATALOGUE_SUMMARY}}", _escape_yaml_double_quoted_scalar(a.summary))
            .replace("{{OVERVIEW_STUB}}", stub)
            .replace("{{ENTRY_FILE}}", a.entry_file)
        )
        dest.write_text(text, encoding="utf-8", newline="\n")
        written += 1
    return written


def _folder_blurb(dir_name: str, child_count: int) -> str:
    if dir_name in KNOWN_DIR_SUMMARY:
        return KNOWN_DIR_SUMMARY[dir_name]
    return f"Folder ({child_count} items)."


def _folder_blurb_from_path(folder: Path, child_count: int) -> str:
    """Known directory roles, else SKILL.md-based summary for embedded/nested skills, else generic count."""
    name = folder.name
    if name in KNOWN_DIR_SUMMARY:
        return KNOWN_DIR_SUMMARY[name]
    skill_md = folder / "SKILL.md"
    if skill_md.is_file():
        fm, body, _ = _load_package_source(folder, "skill")
        if body or fm:
            return _table_blurb(fm, body, max_len=260)
    return _folder_blurb(name, child_count)


def _html_file_row(
    repo_root: Path,
    file_path: Path,
    href_to_repo: str,
    package_dir: Path | None,
) -> str:
    rel = file_path.relative_to(repo_root).as_posix()
    blurb = _file_blurb(file_path, max_len=260)
    url = _repo_href(href_to_repo, rel)
    link_attrs = _REPO_LINK_NEW_TAB
    if package_dir is not None:
        cat = _package_markdown_catalog_href_from_detail_page(repo_root, file_path, package_dir)
        if cat:
            url = cat
            link_attrs = ""
    return (
        '<li class="file-tree__file"><a class="file-tree__file-link" href="'
        + _h(url)
        + '"'
        + link_attrs
        + "><strong>"
        + _h(file_path.name)
        + "</strong></a><span class=\"file-meta\"> → "
        + _h(blurb)
        + "</span></li>"
    )


def _html_folder_branch(
    repo_root: Path,
    folder: Path,
    href_to_repo: str,
    package_dir: Path | None,
    *,
    depth: int,
    max_depth: int,
) -> str:
    """One directory as <details>: summary + recursive files/subfolders."""
    if not folder.is_dir():
        return ""
    try:
        kids = sorted(folder.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        kids = [p for p in kids if not p.name.startswith(".")]
    except OSError:
        return (
            '<details class="file-tree__details"><summary class="file-tree__summary">'
            + _h(folder.name)
            + "/ <span class=\"file-meta\">(unreadable)</span></summary></details>"
        )
    n = len(kids)
    summary = _folder_blurb_from_path(folder, n)
    open_attr = ' open' if depth <= _FILE_TREE_DEFAULT_EXPAND_DEPTH else ""

    inner_parts: list[str] = []
    for p in kids:
        if p.is_file():
            inner_parts.append(_html_file_row(repo_root, p, href_to_repo, package_dir))
        elif p.is_dir():
            if depth + 1 > max_depth:
                inner_parts.append(
                    "<li class=\"file-tree__dir file-tree__dir--truncated\"><strong>"
                    + _h(p.name)
                    + "/</strong> <span class=\"file-meta\">(deeper nesting omitted)</span></li>"
                )
            else:
                sub = _html_folder_branch(
                    repo_root,
                    p,
                    href_to_repo,
                    package_dir,
                    depth=depth + 1,
                    max_depth=max_depth,
                )
                inner_parts.append('<li class="file-tree__dir">' + sub + "</li>")

    if not inner_parts:
        inner_body = '<p class="file-list__nested-note">Empty folder.</p>'
    else:
        inner_body = (
            '<ul class="file-list file-list--nested file-tree__ul">\n'
            + "\n".join(inner_parts)
            + "\n</ul>"
        )

    return (
        '<details class="file-tree__details"'
        + open_attr
        + "><summary class=\"file-tree__summary\"><strong>"
        + _h(folder.name)
        + "/</strong><span class=\"file-meta\"> → "
        + _h(summary)
        + '</span></summary><div class=\"file-tree__inner\">'
        + inner_body
        + "</div></details>"
    )


def _html_contents_list(repo_root: Path, package_dir: Path, href_to_repo: str) -> str:
    """HTML list: files; dirs as expandable <details> with recursive subfolders and files."""
    if not package_dir.is_dir():
        return '<p class="entry-caption">(missing directory)</p>'
    try:
        kids = sorted(package_dir.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        kids = [p for p in kids if not p.name.startswith(".")]
    except OSError:
        return '<p class="entry-caption">(could not read directory)</p>'
    parts: list[str] = []
    for p in kids:
        if p.is_dir():
            parts.append(
                '<li class="file-list__folder">'
                + _html_folder_branch(
                    repo_root,
                    p,
                    href_to_repo,
                    package_dir,
                    depth=0,
                    max_depth=_FILE_TREE_MAX_DEPTH,
                )
                + "</li>"
            )
        else:
            parts.append(_html_file_row(repo_root, p, href_to_repo, package_dir))
    if not parts:
        return '<p class="entry-caption">(no top-level files)</p>'
    return '<ul class="file-list file-list--root">\n' + "\n".join(parts) + "\n</ul>"


def _nav_cls(which: str, current: str) -> str:
    return "nav__link nav__link--current" if which == current else "nav__link"


def write_entry_detail_pages(
    output_catalog_dir: Path,
    repo_root: Path,
    skills: list[SkillEntry],
    agents: list[AgentEntry],
    detail_css: str,
    detail_tpl: str,
) -> tuple[int, int]:
    """Write catalog/skill/<dir>.html and catalog/agent/<dir>.html. Returns counts."""
    href_to_repo = _path_up_to_ancestor(output_catalog_dir / "skill", repo_root)
    if not href_to_repo:
        href_to_repo = "./"
    nav_prefix = "../"
    brand = CATALOG_BRAND_HTML

    skill_out = output_catalog_dir / "skill"
    agent_out = output_catalog_dir / "agent"
    if skill_out.exists():
        shutil.rmtree(skill_out)
    if agent_out.exists():
        shutil.rmtree(agent_out)
    skill_out.mkdir(parents=True)
    agent_out.mkdir(parents=True)

    for s in skills:
        pkg = repo_root / s.pkg_rel_posix
        fm, body, src_fname = _load_package_source(pkg, "skill")
        readme_path = pkg / "README.md"
        parsed = _parse_catalog_readme_detail(readme_path)
        if parsed:
            overview_r, ascii_r = parsed
            if overview_r:
                desc_html = _plain_overview_to_html(overview_r)
            else:
                desc_plain = _full_purpose_plain(fm, body) if body or fm else s.summary
                desc_html = _h(desc_plain).replace("\n", "<br>\n")
            ascii_art = _ascii_catalog_ready(ascii_r) if ascii_r.strip() else _ascii_placeholder_no_fence()
        else:
            desc_plain = _full_purpose_plain(fm, body) if body or fm else s.summary
            desc_html = _h(desc_plain).replace("\n", "<br>\n")
            ascii_art = _ascii_placeholder_no_readme()
        how_block = _html_how_it_fits_block(ascii_art)
        file_list = _html_contents_list(repo_root, pkg, href_to_repo)
        install_block = _npx_skills_install_block(s.name)
        entry_md = (
            _html_package_md_collapsible_sections(body)
            if body.strip()
            else f'<p class="entry-caption">(no body in {_h(src_fname)})</p>'
        )
        html = (
            detail_tpl.replace("{{CSS}}", detail_css)
            .replace("{{TITLE}}", _h(f"ABD catalogue — skill · {s.name}"))
            .replace("{{BRAND}}", brand)
            .replace("{{BACK_HREF}}", f"{nav_prefix}skills.html")
            .replace("{{BACK_LABEL}}", "← All skills")
            .replace("{{BADGE}}", "Skill")
            .replace("{{H1}}", _h(s.name))
            .replace("{{TAGLINE}}", _h(s.summary))
            .replace("{{NAV_PREFIX}}", nav_prefix)
            .replace("{{NAV_HUB}}", _nav_cls("hub", "skills"))
            .replace("{{NAV_SKILLS}}", _nav_cls("skills", "skills"))
            .replace("{{NAV_AGENTS}}", _nav_cls("agents", "skills"))
            .replace("{{DESCRIPTION}}", desc_html)
            .replace("{{INSTALL_BLOCK}}", install_block)
            .replace("{{HOW_IT_FITS_BLOCK}}", how_block)
            .replace("{{ENTRY_MD_COLLAPSIBLE}}", entry_md)
            .replace("{{FILE_LIST}}", file_list)
        )
        (skill_out / f"{s.dir_name}.html").write_text(html, encoding="utf-8")

    for a in agents:
        pkg = repo_root / "agents" / a.dir_name
        fm, body, src_fname = _load_package_source(pkg, "agent")
        readme_path = pkg / "README.md"
        parsed = _parse_catalog_readme_detail(readme_path)
        if parsed:
            overview_r, ascii_r = parsed
            if overview_r:
                desc_html = _plain_overview_to_html(overview_r)
            else:
                desc_plain = _full_purpose_plain(fm, body) if body or fm else a.summary
                desc_html = _h(desc_plain).replace("\n", "<br>\n")
            ascii_art = _ascii_catalog_ready(ascii_r) if ascii_r.strip() else _ascii_placeholder_no_fence()
        else:
            desc_plain = _full_purpose_plain(fm, body) if body or fm else a.summary
            desc_html = _h(desc_plain).replace("\n", "<br>\n")
            ascii_art = _ascii_placeholder_no_readme()
        how_block = _html_how_it_fits_block(ascii_art)
        file_list = _html_contents_list(repo_root, pkg, href_to_repo)
        entry_md = (
            _html_package_md_collapsible_sections(body)
            if body.strip()
            else f'<p class="entry-caption">(no body in {_h(src_fname)})</p>'
        )
        html = (
            detail_tpl.replace("{{CSS}}", detail_css)
            .replace("{{TITLE}}", _h(f"ABD catalogue — agent · {a.name}"))
            .replace("{{BRAND}}", brand)
            .replace("{{BACK_HREF}}", f"{nav_prefix}agents.html")
            .replace("{{BACK_LABEL}}", "← All agents")
            .replace("{{BADGE}}", "Agent")
            .replace("{{H1}}", _h(a.name))
            .replace("{{TAGLINE}}", _h(a.summary))
            .replace("{{NAV_PREFIX}}", nav_prefix)
            .replace("{{NAV_HUB}}", _nav_cls("hub", "agents"))
            .replace("{{NAV_SKILLS}}", _nav_cls("skills", "agents"))
            .replace("{{NAV_AGENTS}}", _nav_cls("agents", "agents"))
            .replace("{{DESCRIPTION}}", desc_html)
            .replace("{{INSTALL_BLOCK}}", "")
            .replace("{{HOW_IT_FITS_BLOCK}}", how_block)
            .replace("{{ENTRY_MD_COLLAPSIBLE}}", entry_md)
            .replace("{{FILE_LIST}}", file_list)
        )
        (agent_out / f"{a.dir_name}.html").write_text(html, encoding="utf-8")

    return len(skills), len(agents)


def generate_outline_md(
    repo_root: Path,
    skills: list[SkillEntry],
    agents: list[AgentEntry],
    md_link_prefix: str,
    catalog_cli_hint: str,
) -> str:
    lines: list[str] = [
        "# ABD Skills & Agents — Catalogue Outline",
        "",
        "> Auto-generated from repository `skills/` and `agents/`.",
        f"> Run `{catalog_cli_hint}` to refresh.",
        "",
        "This outline mirrors the reader-facing style of `process-outline.md`:",
        "each row gives a **short description** and where to open the source.",
        "",
        "## Summary — Skills",
        "",
        "| Skill | Description | Open |",
        "| --- | --- | --- |",
    ]
    for s in skills:
        link = f"{md_link_prefix}{s.rel_skill_md}"
        desc = s.summary.replace("|", "\\|")
        lines.append(f"| **{s.name}** | {desc} | [SKILL.md]({link}) |")
    lines += [
        "",
        "## Summary — Agents",
        "",
        "| Agent | Description | Open |",
        "| --- | --- | --- |",
    ]
    for a in agents:
        link = f"{md_link_prefix}{a.rel_entry_md}"
        desc = a.summary.replace("|", "\\|")
        lines.append(f"| **{a.name}** | {desc} | [{a.entry_file}]({link}) |")

    lines += ["", "---", "", "## Skills (detail)", ""]
    for s in skills:
        d = repo_root / s.pkg_rel_posix
        lines += [
            f"### {s.name}",
            "",
            f"- **Directory:** [`{s.pkg_rel_posix}/`]({md_link_prefix}{s.pkg_rel_posix}/)",
            "",
            "**Summary:**",
            "",
            s.summary,
            "",
            "**Description (from Purpose / body):**",
            "",
            s.description,
            "",
            "**Repository layout:**",
            "",
            *layout_lines(repo_root, d, md_link_prefix),
            "",
        ]

    lines += ["---", "", "## Agents (detail)", ""]
    agents_root = repo_root / "agents"
    for a in agents:
        d = agents_root / a.dir_name
        lines += [
            f"### {a.name}",
            "",
            f"- **Directory:** [`agents/{a.dir_name}/`]({md_link_prefix}agents/{a.dir_name}/)",
            f"- **Entry:** [`{a.rel_entry_md}`]({md_link_prefix}{a.rel_entry_md})",
            "",
            "**Summary:**",
            "",
            a.summary,
            "",
            "**Description:**",
            "",
            a.description,
            "",
            "**Repository layout:**",
            "",
            *layout_lines(repo_root, d, md_link_prefix),
            "",
        ]
    return "\n".join(lines)


def _card_block_skills(entries: list[SkillEntry], up_to_repo: str) -> str:
    parts: list[str] = []
    for e in entries:
        href = f"skill/{quote(e.dir_name, safe='')}.html"
        parts.append(
            textwrap.dedent(
                f"""\
        <a class="cap-card" href="{_h(href)}">
          <p class="cap-card__title"><span class="cap-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect width="24" height="24" rx="4" fill="#1a1a1e"/><path d="M7 8h10M7 12h7M7 16h10" stroke="#ff7a00" stroke-width="1.5" stroke-linecap="round"/></svg></span>{_h(e.name)}</p>
          <p class="cap-card__label">Description</p>
          <p class="cap-card__summary">{_h(e.summary)}</p>
          <p class="cap-card__more">Open skill page →</p>
        </a>"""
            )
        )
    return "\n".join(parts)


def _card_block_agents(entries: list[AgentEntry], up_to_repo: str) -> str:
    parts: list[str] = []
    for e in entries:
        href = f"agent/{quote(e.dir_name, safe='')}.html"
        parts.append(
            textwrap.dedent(
                f"""\
        <a class="cap-card" href="{_h(href)}">
          <p class="cap-card__title"><span class="cap-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect width="24" height="24" rx="4" fill="#1a1a1e"/><path d="M6 9h12v10H6z" stroke="#ff7a00" stroke-width="1.5"/><path d="M9 7V5h6v2" stroke="#ff7a00" stroke-width="1.5" stroke-linecap="round"/></svg></span>{_h(e.name)}</p>
          <p class="cap-card__label">Description</p>
          <p class="cap-card__summary">{_h(e.summary)}</p>
          <p class="cap-card__more">Open agent page →</p>
        </a>"""
            )
        )
    return "\n".join(parts)


def _load_template(name: str) -> str:
    p = TEMPLATE_DIR / name
    if not p.exists():
        raise FileNotFoundError(f"Missing template: {p}")
    return p.read_text(encoding="utf-8")


def _load_intro_fragment(filename: str, default: str) -> str:
    """HTML intro for hub/skills/agents pages. Prefer templates/intros/ (AI-reviewed copy)."""
    p = TEMPLATE_DIR / "intros" / filename
    if p.is_file():
        return p.read_text(encoding="utf-8").strip()
    return default


def _abd_works_agile_garden_fragment_css(repo_root: Path) -> str:
    """Shared CSS for prelude block (same file linked from gardener lesson). Prepended to catalog.css."""
    p = repo_root.parent / "abd-works" / "commons" / "agile-garden-fragment.css"
    if not p.is_file():
        return ""
    return p.read_text(encoding="utf-8").strip() + "\n\n"


GARDEN_PRELUDE_TAGLINE = (
    "The ABD AI Garden is ABD's area to share agents and skills that remove toil from our work and "
    "our clients' work. Browse it like a curriculum—each entry is a skill you can run with an agent."
)

# Practice-tier placeholders (no skill package yet); listed after real practice entries.
GARDEN_PRACTICE_STUB_ROWS: tuple[tuple[str, str], ...] = (
    ("· cost-of-delay", "Coming soon"),
    ("· relative-sizing", "Coming soon"),
)


def _agile_garden_skill_href(dir_name: str) -> str:
    return f"skill/{quote(dir_name, safe='')}.html"


def _agile_garden_agent_href(dir_name: str) -> str:
    return f"agent/{quote(dir_name, safe='')}.html"


def _html_agile_garden_mission_block() -> str:
    return (
        '  <h2 class="catalog-prelude-heading" id="mission">Mission</h2>\n'
        '  <div class="catalog-mission">\n'
        '    <div class="catalog-mission-card catalog-mission-card--teal">\n'
        "      <h3>Agents, Skills &amp; Apps</h3>\n"
        "      <p>Build specialised agents backed by ABD practice skills. Automate the toil, amplify "
        "the thinking. Each skill encodes years of practice knowledge.</p>\n"
        "    </div>\n"
        '    <div class="catalog-mission-card catalog-mission-card--amber">\n'
        "      <h3>Learning Internally</h3>\n"
        "      <p>Every skill we build is a lesson. Every lesson becomes a skill. Recursive learning by "
        "design — the curriculum IS the skill garden.</p>\n"
        "    </div>\n"
        '    <div class="catalog-mission-card catalog-mission-card--purple">\n'
        "      <h3>Eminence by Showcasing</h3>\n"
        "      <p>We want our thought leadership to be ready for anyone to use, living in agentic "
        "capability — not just slide decks.</p>\n"
        "    </div>\n"
        "  </div>\n"
    )


def _html_agile_garden_skill_row(s: SkillEntry, *, foundational: bool = False) -> str:
    href = _agile_garden_skill_href(s.dir_name)
    name_cls = (
        "catalog-garden-name catalog-garden-name--foundational"
        if foundational
        else "catalog-garden-name"
    )
    return (
        f'      <div class="catalog-garden-row"><span class="{name_cls}">'
        f'<a href="{href}">{_h(s.name)}</a></span>'
        f'<span class="catalog-garden-desc">{_h(s.summary)}</span></div>\n'
    )


def _html_agile_garden_agent_row(a: AgentEntry) -> str:
    href = _agile_garden_agent_href(a.dir_name)
    return (
        f'      <div class="catalog-garden-row"><span class="catalog-garden-name catalog-garden-name--agent">'
        f'<a href="{href}">{_h(a.name)}</a></span>'
        f'<span class="catalog-garden-desc">{_h(a.summary)}</span></div>\n'
    )


def _html_agile_garden_stub_row(label: str, desc: str) -> str:
    return (
        f'      <div class="catalog-garden-row"><span class="catalog-garden-name catalog-garden-name--dim">'
        f"{_h(label)}</span>"
        f'<span class="catalog-garden-desc catalog-garden-desc--muted">{_h(desc)}</span></div>\n'
    )


def build_agile_garden_prelude_html(
    skills: list[SkillEntry],
    agents: list[AgentEntry],
    *,
    include_title_block: bool = True,
) -> str:
    practice = sorted(
        [s for s in skills if s.garden_tier == "practice"],
        key=lambda s: (s.garden_order, s.name.lower()),
    )
    foundational = sorted(
        [s for s in skills if s.garden_tier == "foundational"],
        key=lambda s: (s.garden_order, s.name.lower()),
    )
    agents_show = sorted(
        [a for a in agents if a.garden_include],
        key=lambda a: (a.garden_order, a.name.lower()),
    )

    rows_p = "".join(_html_agile_garden_skill_row(s) for s in practice)
    for label, desc in GARDEN_PRACTICE_STUB_ROWS:
        rows_p += _html_agile_garden_stub_row(label, desc)
    rows_f = "".join(_html_agile_garden_skill_row(s, foundational=True) for s in foundational)
    rows_a = "".join(_html_agile_garden_agent_row(a) for a in agents_show)

    mission = _html_agile_garden_mission_block()
    if include_title_block:
        aria = ' aria-labelledby="catalog-agile-garden-h2"'
        title_block = (
            '  <h2 class="catalog-prelude-heading" id="catalog-agile-garden-h2">'
            "The ABD AI Garden</h2>\n"
            f'  <p class="catalog-prelude-tagline">{_h(GARDEN_PRELUDE_TAGLINE)}</p>\n'
        )
    else:
        aria = ' aria-label="The ABD AI Garden"'
        title_block = ""
    return (
        f'<section class="catalog-prelude" id="agile-garden"{aria}>\n'
        f"{title_block}"
        f"{mission}"
        '  <div class="catalog-garden-lists">\n'
        '  <div class="catalog-garden-grid">\n'
        '    <div class="catalog-garden-col">\n'
        '      <div class="catalog-garden-col-header catalog-garden-col-header--practice">\n'
        '        <img class="catalog-garden-ico" src="../commons/images/icon-garden-practice.svg" width="22" '
        'height="22" alt="" aria-hidden="true" />\n'
        "        <span>Practice Skills — What We Do</span>\n"
        "      </div>\n"
        f"{rows_p}"
        "    </div>\n"
        '    <div class="catalog-garden-col">\n'
        '      <div class="catalog-garden-col-header catalog-garden-col-header--foundational">\n'
        '        <img class="catalog-garden-ico" src="../commons/images/icon-garden-foundational.svg" width="22" '
        'height="22" alt="" aria-hidden="true" />\n'
        "        <span>Foundational Skills — Enhance the Way Skills Run</span>\n"
        "      </div>\n"
        f"{rows_f}"
        "    </div>\n"
        "  </div>\n"
        '  <div class="catalog-garden-agents-wrap">\n'
        '    <div class="catalog-garden-col catalog-garden-col--agents">\n'
        '      <div class="catalog-garden-col-header catalog-garden-col-header--agents">\n'
        "        <span>Agents — Teammates &amp; specialists</span>\n"
        "      </div>\n"
        f"{rows_a}"
        "    </div>\n"
        "  </div>\n"
        "  </div>\n"
        "</section>\n"
    )


def _abd_works_agile_garden_prelude_write_path(repo_root: Path) -> Path:
    return (
        repo_root.parent
        / "abd-works"
        / "abd-ai-gardener-training"
        / "context"
        / "fragments"
        / "agile-garden-catalog-prelude.html"
    )


def write_agile_garden_prelude_fragment(repo_root: Path, section_html: str) -> None:
    """Emit fragment for gardener lesson (see abd-works/scripts/sync-agile-garden-into-lesson.py)."""
    p = _abd_works_agile_garden_prelude_write_path(repo_root)
    header = (
        "<!--\n"
        "  AUTO-GENERATED by generate_abd_catalog.py — do not edit by hand.\n"
        "  Skills: catalog_garden_tier: practice | foundational in skills/*/SKILL.md\n"
        "  Optional: catalog_garden_order: <int> for sort order within a column.\n"
        "  Agents: catalog_garden: false to omit from this list (default: include).\n"
        "-->\n"
    )
    try:
        if p.parent.is_dir():
            p.write_text(header + section_html, encoding="utf-8")
    except OSError:
        pass


def _hub_intro_for_single_page_index(hub_intro: str) -> str:
    """Same copy as multi-page hub, but jump to in-page sections instead of skills.html / agents.html."""
    return (
        hub_intro.replace('href="skills.html"', 'href="#catalog-skills"')
        .replace("href='skills.html'", "href='#catalog-skills'")
        .replace('href="agents.html"', 'href="#catalog-agents"')
        .replace("href='agents.html'", "href='#catalog-agents'")
    )


def _html_catalog_section(
    section_id: str,
    title: str,
    count_label: str,
    body_inner: str,
    *,
    open_default: bool = False,
) -> str:
    """One collapsible block for the single-page index (matches abd-works catalogue layout)."""
    open_attr = " open" if open_default else ""
    body = textwrap.indent(body_inner.strip(), "    ")
    return (
        f'<details class="catalog-section" id="{_h(section_id)}"{open_attr}>\n'
        f"  <summary>{_h(title)} <span class=\"count\">{_h(count_label)}</span></summary>\n"
        f"  <div class=\"section-body\">\n{body}\n  </div>\n</details>"
    )


def write_html_pages(
    output_catalog_dir: Path,
    repo_root: Path,
    skills: list[SkillEntry],
    agents: list[AgentEntry],
) -> tuple[int, int, int]:
    """Write index.html (single-page hub + collapsible skills/agents), skills.html, agents.html, detail pages.

    Returns (skill_detail_count, agent_detail_count, markdown_doc_page_count).
    """
    up_to_repo = _path_up_to_ancestor(output_catalog_dir, repo_root)
    if not up_to_repo:
        up_to_repo = "./"
    idx_tpl = _load_template("page-catalog.html")
    idx_single_tpl = _load_template("page-catalog-index.html")
    css = _abd_works_agile_garden_fragment_css(repo_root) + _load_template("catalog.css")
    detail_tpl = _load_template("page-entry-detail.html")

    def fill(
        tpl: str,
        *,
        title: str,
        brand: str,
        h1: str,
        tagline: str,
        intro: str,
        nav_current: str,
        body_inner: str,
    ) -> str:
        def nav_cls(which: str) -> str:
            return "nav__link nav__link--current" if nav_current == which else "nav__link"

        return (
            tpl.replace("{{CSS}}", css)
            .replace("{{TITLE}}", title)
            .replace("{{BRAND}}", brand)
            .replace("{{H1}}", h1)
            .replace("{{TAGLINE}}", tagline)
            .replace("{{INTRO}}", intro)
            .replace("{{NAV_HUB}}", nav_cls("hub"))
            .replace("{{NAV_SKILLS}}", nav_cls("skills"))
            .replace("{{NAV_AGENTS}}", nav_cls("agents"))
            .replace("{{BODY_INNER}}", body_inner)
        )

    brand = CATALOG_BRAND_HTML

    outline_href = "outline.md"
    hub_intro = _load_intro_fragment(
        "catalog-hub-intro.html",
        (
            "<p>Browse <a href=\"skills.html\">skills</a> and "
            "<a href=\"agents.html\">agents</a>. "
            f"<a href=\"{outline_href}\">outline.md</a> lists the same entries in one file.</p>"
        ),
    ).replace("{{OUTLINE_HREF}}", outline_href)
    # Single-page index: hub + skills + agents as collapsible sections (same UX as abd-works catalogue).
    hub_for_index = _hub_intro_for_single_page_index(hub_intro)
    hub_index_extra = (
        "<p>Cards open full detail pages under <code>skill/</code> and <code>agent/</code>.</p>\n"
        f"<p>{len(skills)} skills and {len(agents)} agents are indexed in this catalogue.</p>"
    )
    skills_intro = _load_intro_fragment(
        "catalog-skills-intro.html",
        "<p>Open a card for a full page on that skill.</p>",
    )
    agents_intro = _load_intro_fragment(
        "catalog-agents-intro.html",
        "<p>Open a card for a full page on that agent.</p>",
    )
    skills_grid = _card_block_skills(skills, up_to_repo)
    agents_grid = _card_block_agents(agents, up_to_repo)
    index_sections = "\n\n".join(
        [
            _html_catalog_section(
                "catalog-hub",
                "About this catalogue",
                "(hub)",
                f"{hub_for_index}\n{hub_index_extra}",
                open_default=True,
            ),
            _html_catalog_section(
                "catalog-skills",
                "Skills",
                f"({len(skills)})",
                f"{skills_intro}\n<div class=\"cap-grid\">\n{skills_grid}\n</div>",
            ),
            _html_catalog_section(
                "catalog-agents",
                "Agents",
                f"({len(agents)})",
                f"{agents_intro}\n<div class=\"cap-grid\">\n{agents_grid}\n</div>",
            ),
        ]
    )
    write_agile_garden_prelude_fragment(
        repo_root,
        build_agile_garden_prelude_html(skills, agents, include_title_block=True),
    )
    garden_for_index = build_agile_garden_prelude_html(
        skills, agents, include_title_block=False
    )
    index_sections = f"{garden_for_index}\n\n{index_sections}"
    index_html = (
        idx_single_tpl.replace("{{CSS}}", css)
        .replace("{{TITLE}}", "ABD catalogue — The ABD AI Garden")
        .replace("{{BRAND}}", brand)
        .replace("{{H1}}", "The ABD AI Garden")
        .replace("{{TAGLINE}}", _h(GARDEN_PRELUDE_TAGLINE))
        .replace("{{BODY_INNER}}", index_sections)
    )
    (output_catalog_dir / "index.html").write_text(index_html, encoding="utf-8")

    skills_body = f'<h2>Skills ({len(skills)})</h2><div class="cap-grid">{skills_grid}</div>'
    (output_catalog_dir / "skills.html").write_text(
        fill(
            idx_tpl,
            title="ABD catalogue — Skills",
            brand=brand,
            h1="Skills",
            tagline=f"{len(skills)} entries.",
            intro=skills_intro,
            nav_current="skills",
            body_inner=skills_body,
        ),
        encoding="utf-8",
    )

    agents_body = f'<h2>Agents ({len(agents)})</h2><div class="cap-grid">{agents_grid}</div>'
    (output_catalog_dir / "agents.html").write_text(
        fill(
            idx_tpl,
            title="ABD catalogue — Agents",
            brand=brand,
            h1="Agents",
            tagline=f"{len(agents)} entries.",
            intro=agents_intro,
            nav_current="agents",
            body_inner=agents_body,
        ),
        encoding="utf-8",
    )

    n_md_pages = write_package_markdown_pages(output_catalog_dir, repo_root, skills, agents, css)
    n_skill_pages, n_agent_pages = write_entry_detail_pages(
        output_catalog_dir, repo_root, skills, agents, css, detail_tpl
    )
    return n_skill_pages, n_agent_pages, n_md_pages


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ABD skill + agent catalogue.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (contains skills/ and agents/). "
        "Defaults to discovery from this script location (agilebydesign-skills root).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for outline.md and all HTML (default: <repo-root>/catalog).",
    )
    parser.add_argument(
        "--scaffold-readmes",
        action="store_true",
        help="Create skills/<pkg>/README.md and agents/<pkg>/README.md from templates only where missing, then generate.",
    )
    args = parser.parse_args()

    repo_root = (args.repo_root or _repo_root_from_skill_package(SKILL_DIR)).resolve()
    skills_dir = repo_root / "skills"
    agents_dir = repo_root / "agents"
    output_dir = (args.output_dir or (repo_root / "catalog")).resolve()

    if not skills_dir.is_dir():
        raise SystemExit(f"skills/ not found: {skills_dir}")
    if not agents_dir.is_dir():
        raise SystemExit(f"agents/ not found: {agents_dir}")

    skills = discover_skills(skills_dir, repo_root)
    agents = discover_agents(agents_dir, repo_root)
    if args.scaffold_readmes:
        n = scaffold_catalog_readmes(repo_root, skills, agents)
        print(f"  scaffolded {n} catalogue README.md file(s)")
        skills = discover_skills(skills_dir, repo_root)
        agents = discover_agents(agents_dir, repo_root)
    if not skills and not agents:
        raise SystemExit("No skills or agents discovered.")

    output_dir.mkdir(parents=True, exist_ok=True)

    # outline.md, index/skills/agents, skill/, agent/ all live directly under catalog/
    outline_path = output_dir / "outline.md"
    md_prefix = _path_up_to_ancestor(output_dir, repo_root)
    catalog_cli_hint = _catalog_cli_invocation(repo_root)
    outline_path.write_text(
        generate_outline_md(repo_root, skills, agents, md_prefix, catalog_cli_hint),
        encoding="utf-8",
    )
    print(f"  wrote {outline_path}")

    n_sk_detail, n_ag_detail, n_md_pages = write_html_pages(
        output_dir,
        repo_root,
        skills,
        agents,
    )
    print(f"  wrote {output_dir / 'index.html'}")
    print(f"  wrote {output_dir / 'skills.html'}")
    print(f"  wrote {output_dir / 'agents.html'}")
    print(f"  wrote {n_md_pages} markdown pages under catalog/doc/")
    print(f"  wrote {n_sk_detail} skill detail pages under catalog/skill/")
    print(f"  wrote {n_ag_detail} agent detail pages under catalog/agent/")
    print(f"  ({len(skills)} skills, {len(agents)} agents)")


if __name__ == "__main__":
    main()
