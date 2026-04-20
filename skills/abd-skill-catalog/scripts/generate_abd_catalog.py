#!/usr/bin/env python3
"""Scan repo-root skills/ and agents/; emit outline.md + HTML under repo catalog/."""

from __future__ import annotations

import argparse
import html as html_mod
import re
import shutil
import textwrap
from pathlib import Path
from typing import NamedTuple
from urllib.parse import quote

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / "templates"

# Subtitle in generated pages (repo output folder is <root>/catalog/).
CATALOG_BRAND_HTML = "<strong>Agile by Design</strong> &middot; catalog"

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
# <details open> for folder depth 0..N so nested agent skills show files by default (still collapsible).
_FILE_TREE_DEFAULT_EXPAND_DEPTH = 2


class SkillEntry(NamedTuple):
    name: str
    dir_name: str
    summary: str
    description: str
    rel_skill_md: str


class AgentEntry(NamedTuple):
    name: str
    dir_name: str
    entry_file: str
    summary: str
    description: str
    rel_entry_md: str


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
    """One paragraph for summary tables and HTML cards: YAML description, else Purpose, else opening text."""
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


def _agent_display_name(fm: dict[str, str], body: str, dir_name: str) -> str:
    n = fm.get("name", "").strip()
    if n:
        return n
    h1 = _h1_title(body)
    if h1:
        h1 = re.sub(r"^AGENTS\s+—\s*", "", h1, flags=re.IGNORECASE).strip()
        return h1 or dir_name
    return dir_name


def _description_agent(fm: dict[str, str], body: str) -> str:
    purpose = _extract_section(body, "Purpose")
    if purpose:
        return _truncate(_strip_md(purpose), 1200)
    desc = fm.get("description", "")
    if desc:
        return _truncate(_strip_md(desc), 1200)
    return _truncate(_strip_md(body), 800)


def discover_skills(skills_dir: Path, repo_root: Path) -> list[SkillEntry]:
    out: list[SkillEntry] = []
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir():
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.exists():
            continue
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        fm = _parse_frontmatter(text)
        body = FRONTMATTER_RE.sub("", text).strip()
        name = fm.get("name", child.name)
        rel = skill_md.relative_to(repo_root).as_posix()
        out.append(
            SkillEntry(
                name=name,
                dir_name=child.name,
                summary=_table_blurb(fm, body),
                description=_description_skill(fm, body),
                rel_skill_md=rel,
            )
        )
    return out


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
                text = p.read_text(encoding="utf-8", errors="replace")
                break
        if not entry_name:
            continue
        fm = _parse_frontmatter(text)
        body = FRONTMATTER_RE.sub("", text).strip()
        name = _agent_display_name(fm, body, child.name)
        rel = (child / entry_name).relative_to(repo_root).as_posix()
        out.append(
            AgentEntry(
                name=name,
                dir_name=child.name,
                entry_file=entry_name,
                summary=_table_blurb(fm, body),
                description=_description_agent(fm, body),
                rel_entry_md=rel,
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
        link = f"{md_prefix}{rel}"
        if p.is_dir():
            try:
                cnt = len([x for x in p.iterdir() if not x.name.startswith(".")])
            except OSError:
                cnt = 0
            summary = _folder_blurb_from_path(p, cnt)
            lines.append(f"- **[{p.name}/]({link})** — {summary}")
        else:
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


def _repo_href(href_to_repo: str, rel_posix: str) -> str:
    rel_posix = rel_posix.replace("\\", "/").strip("/")
    if not rel_posix:
        return href_to_repo
    parts = [quote(p, safe="") for p in rel_posix.split("/") if p]
    return href_to_repo + "/".join(parts)


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


def _ascii_package_diagram(repo_rel: str, entry_filename: str, package_dir: Path) -> str:
    """ASCII diagram (abd-skill-builder overview style): flow + top-level tree."""
    ef = entry_filename if len(entry_filename) <= 24 else entry_filename[:21] + "…"
    lines = [
        "       repository",
        "           │",
        "           ▼",
        "  ┌─────────────────────────┐",
        f"  │ {ef:<25} │",
        "  │ (entry document)        │",
        "  └────────────┬────────────┘",
        "               │",
        "  peers at package root:",
        "               │",
        "               ▼",
        "",
    ]
    if not package_dir.is_dir():
        lines.append("(could not read package directory)")
        return "\n".join(lines)
    try:
        kids = sorted(package_dir.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except OSError:
        lines.append("(could not read directory)")
        return "\n".join(lines)
    lines.append(f"{repo_rel}/")
    for i, p in enumerate(kids):
        branch = "└── " if i == len(kids) - 1 else "├── "
        label = p.name + ("/" if p.is_dir() else "")
        lines.append(branch + label)
    return "\n".join(lines)


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


def _html_file_row(repo_root: Path, file_path: Path, href_to_repo: str) -> str:
    rel = file_path.relative_to(repo_root).as_posix()
    blurb = _file_blurb(file_path, max_len=260)
    url = _repo_href(href_to_repo, rel)
    return (
        "<li class=\"file-tree__file\"><strong>"
        + _h(file_path.name)
        + "</strong><span class=\"file-meta\"> → "
        + _h(blurb)
        + '</span> <a href="'
        + _h(url)
        + '"'
        + _REPO_LINK_NEW_TAB
        + '>open file</a></li>'
    )


def _html_folder_branch(
    repo_root: Path,
    folder: Path,
    href_to_repo: str,
    *,
    depth: int,
    max_depth: int,
) -> str:
    """One directory as <details>: summary + recursive files/subfolders."""
    if not folder.is_dir():
        return ""
    rel = folder.relative_to(repo_root).as_posix()
    url = _repo_href(href_to_repo, rel) + "/"
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
            inner_parts.append(_html_file_row(repo_root, p, href_to_repo))
        elif p.is_dir():
            if depth + 1 > max_depth:
                crel = p.relative_to(repo_root).as_posix()
                curl = _repo_href(href_to_repo, crel) + "/"
                inner_parts.append(
                    "<li class=\"file-tree__dir file-tree__dir--truncated\"><strong>"
                    + _h(p.name)
                    + "/</strong> <span class=\"file-meta\">(deeper nesting omitted)</span> "
                    + '<a href="'
                    + _h(curl)
                    + '"'
                    + _REPO_LINK_NEW_TAB
                    + ">open folder</a></li>"
                )
            else:
                sub = _html_folder_branch(repo_root, p, href_to_repo, depth=depth + 1, max_depth=max_depth)
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
        + '</span> <a class="file-tree__folder-link" href="'
        + _h(url)
        + '"'
        + _REPO_LINK_NEW_TAB
        + ">open folder</a></summary><div class=\"file-tree__inner\">"
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
                    depth=0,
                    max_depth=_FILE_TREE_MAX_DEPTH,
                )
                + "</li>"
            )
        else:
            parts.append(_html_file_row(repo_root, p, href_to_repo))
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
        pkg = repo_root / "skills" / s.dir_name
        fm, body, entry_fn = _load_package_source(pkg, "skill")
        desc_plain = _full_purpose_plain(fm, body) if body or fm else s.summary
        desc_html = _h(desc_plain).replace("\n", "<br>\n")
        rel_posix = f"skills/{s.dir_name}"
        ascii_art = _ascii_package_diagram(rel_posix, entry_fn or "SKILL.md", pkg)
        file_list = _html_contents_list(repo_root, pkg, href_to_repo)
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
            .replace("{{ASCII_DIAGRAM}}", _h(ascii_art))
            .replace("{{FILE_LIST}}", file_list)
        )
        (skill_out / f"{s.dir_name}.html").write_text(html, encoding="utf-8")

    for a in agents:
        pkg = repo_root / "agents" / a.dir_name
        fm, body, entry_fn = _load_package_source(pkg, "agent")
        desc_plain = _full_purpose_plain(fm, body) if body or fm else a.summary
        desc_html = _h(desc_plain).replace("\n", "<br>\n")
        rel_posix = f"agents/{a.dir_name}"
        ascii_art = _ascii_package_diagram(rel_posix, entry_fn or a.entry_file, pkg)
        file_list = _html_contents_list(repo_root, pkg, href_to_repo)
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
            .replace("{{ASCII_DIAGRAM}}", _h(ascii_art))
            .replace("{{FILE_LIST}}", file_list)
        )
        (agent_out / f"{a.dir_name}.html").write_text(html, encoding="utf-8")

    return len(skills), len(agents)


def generate_outline_md(
    repo_root: Path,
    skills: list[SkillEntry],
    agents: list[AgentEntry],
    md_link_prefix: str,
) -> str:
    lines: list[str] = [
        "# ABD Skills & Agents — Catalogue Outline",
        "",
        "> Auto-generated from repository `skills/` and `agents/`.",
        "> Run `python skills/abd-skill-catalog/scripts/generate_abd_catalog.py` to refresh.",
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
    skills_root = repo_root / "skills"
    for s in skills:
        d = skills_root / s.dir_name
        lines += [
            f"### {s.name}",
            "",
            f"- **Directory:** [`skills/{s.dir_name}/`]({md_link_prefix}skills/{s.dir_name}/)",
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


def write_html_pages(
    output_catalog_dir: Path,
    repo_root: Path,
    skills: list[SkillEntry],
    agents: list[AgentEntry],
) -> tuple[int, int]:
    """Write index.html, skills.html, agents.html and per-entry detail pages.

    Returns (skill_detail_count, agent_detail_count).
    """
    up_to_repo = _path_up_to_ancestor(output_catalog_dir, repo_root)
    if not up_to_repo:
        up_to_repo = "./"
    idx_tpl = _load_template("page-catalog.html")
    css = _load_template("catalog.css")
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
            "<a href=\"agents.html\">agents</a> in this repository. "
            "For a single diffable document, open "
            f"<a href=\"{outline_href}\">outline.md</a>.</p>"
        ),
    ).replace("{{OUTLINE_HREF}}", outline_href)
    hub_body = (
        "<h2>Quick links</h2><ul>"
        '<li><a href="skills.html">All skills — card grid</a></li>'
        '<li><a href="agents.html">All agents — card grid</a></li>'
        "</ul>"
        f"<p>{len(skills)} skills, {len(agents)} agents indexed.</p>"
    )
    index_html = fill(
        idx_tpl,
        title="ABD catalogue — Hub",
        brand=brand,
        h1="Skills &amp; agents catalogue",
        tagline="Repository-wide index; outputs live at the repository root.",
        intro=hub_intro,
        nav_current="hub",
        body_inner=hub_body,
    )
    (output_catalog_dir / "index.html").write_text(index_html, encoding="utf-8")

    skills_intro = _load_intro_fragment(
        "catalog-skills-intro.html",
        (
            "<p>Each card opens a <strong>skill detail page</strong> (description, ASCII package layout in a "
            "<code>&lt;pre&gt;</code>, and a contents list with links into the repo). Summaries come from "
            "<code>SKILL.md</code> (YAML <code>description</code>, <code>## Purpose</code>, or opening text).</p>"
        ),
    )
    skills_body = f'<h2>Skills ({len(skills)})</h2><div class="cap-grid">{_card_block_skills(skills, up_to_repo)}</div>'
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

    agents_intro = _load_intro_fragment(
        "catalog-agents-intro.html",
        (
            "<p>Each card opens an <strong>agent detail page</strong> (same layout as skills: description, "
            "ASCII layout diagram, contents). Entry file is <code>AGENT.md</code>, then "
            "<code>AGENTS.md</code>, then <code>SKILL.md</code>.</p>"
        ),
    )
    agents_body = f'<h2>Agents ({len(agents)})</h2><div class="cap-grid">{_card_block_agents(agents, up_to_repo)}</div>'
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

    n_skill_pages, n_agent_pages = write_entry_detail_pages(
        output_catalog_dir, repo_root, skills, agents, css, detail_tpl
    )
    return n_skill_pages, n_agent_pages


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ABD skill + agent catalogue.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (contains skills/ and agents/). "
        "Defaults to ../../../.. from this script (agilebydesign-skills root).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for outline.md and all HTML (default: <repo-root>/catalog).",
    )
    args = parser.parse_args()

    repo_root = (args.repo_root or SKILL_DIR.parent.parent).resolve()
    skills_dir = repo_root / "skills"
    agents_dir = repo_root / "agents"
    output_dir = (args.output_dir or (repo_root / "catalog")).resolve()

    if not skills_dir.is_dir():
        raise SystemExit(f"skills/ not found: {skills_dir}")
    if not agents_dir.is_dir():
        raise SystemExit(f"agents/ not found: {agents_dir}")

    skills = discover_skills(skills_dir, repo_root)
    agents = discover_agents(agents_dir, repo_root)
    if not skills and not agents:
        raise SystemExit("No skills or agents discovered.")

    output_dir.mkdir(parents=True, exist_ok=True)

    # outline.md, index/skills/agents, skill/, agent/ all live directly under catalog/
    outline_path = output_dir / "outline.md"
    md_prefix = _path_up_to_ancestor(output_dir, repo_root)
    outline_path.write_text(
        generate_outline_md(repo_root, skills, agents, md_prefix),
        encoding="utf-8",
    )
    print(f"  wrote {outline_path}")

    n_sk_detail, n_ag_detail = write_html_pages(output_dir, repo_root, skills, agents)
    print(f"  wrote {output_dir / 'index.html'}")
    print(f"  wrote {output_dir / 'skills.html'}")
    print(f"  wrote {output_dir / 'agents.html'}")
    print(f"  wrote {n_sk_detail} skill detail pages under catalog/skill/")
    print(f"  wrote {n_ag_detail} agent detail pages under catalog/agent/")
    print(f"  ({len(skills)} skills, {len(agents)} agents)")


if __name__ == "__main__":
    main()
