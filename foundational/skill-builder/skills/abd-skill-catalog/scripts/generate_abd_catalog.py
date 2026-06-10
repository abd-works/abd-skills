#!/usr/bin/env python3
"""Scan family packages; emit outline.md + HTML under catalog/.

Lives under skill-builder/skills/abd-skill-catalog/; repo root is detected by walking
up until scripts/deploy_family_package.py is found.
"""

from __future__ import annotations

import argparse
import html as html_mod
import json
import os
import re
import shutil
import stat
import sys
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple
from urllib.parse import quote

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / "templates"


def _is_skills_repo_root(path: Path) -> bool:
    """Recognize agilebydesign-skills / abd-skills layout."""
    if (path / "scripts" / "deploy_family_package.py").is_file():
        return True
    if (path / "practices").is_dir() and (path / "foundational").is_dir():
        return True
    if (path / "practices").is_dir() and (path / "skill-config.json").is_file():
        return True
    return False


def _repo_root_from_skill_package(skill_pkg_dir: Path) -> Path:
    """Walk upward until the agilebydesign-skills repo root."""
    p = skill_pkg_dir.resolve()
    for _ in range(16):
        if _is_skills_repo_root(p):
            return p
        parent = p.parent
        if parent == p:
            break
        p = parent
    raise RuntimeError(
        f"Could not find repository root (practices/ + foundational/ or "
        f"scripts/deploy_family_package.py) starting from {skill_pkg_dir}"
    )


def _rmtree_output_dir(path: Path) -> None:
    """Remove a regenerated catalog subtree; chmod first so Windows AV/git indexers don't block deletes."""

    if not path.exists():
        return

    def onexc(_func: object, p: str, _exc: BaseException) -> None:
        try:
            os.chmod(p, stat.S_IWUSR | stat.S_IREAD | stat.S_IEXEC)
            _func(p)
        except OSError:
            pass

    import sys as _sys
    if _sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=onexc)
    else:
        shutil.rmtree(path, onerror=lambda f, p, e: onexc(f, p, e[1]))
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)


_REPO_ROOT_DEFAULT = _repo_root_from_skill_package(SKILL_DIR)
_EXECUTE_RULES_SCRIPTS = (
    _REPO_ROOT_DEFAULT / "skill-helpers" / "skills" / "execute-skill-using-skills-rules" / "scripts"
)
if str(_EXECUTE_RULES_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_EXECUTE_RULES_SCRIPTS))
import frontmatter_tags  # noqa: E402

from kanban_layout import (  # noqa: E402
    build_catalog_hub_kanban_embed_html,
    build_kanban_board_html,
    build_kanban_legend_html,
    load_catalog_embed_kanban_css,
    load_kanban_model,
    patch_bootcamp_slide_files,
    rewrite_bootcamp_catalog_links,
    skill_dir_map_from_entries,
    skill_purpose_map_from_entries,
    sync_bootcamp_part3_kanban,
    write_kanban_layout_pages,
)
from family_catalog import (  # noqa: E402
    FAMILY_CATALOG_ALIASES,
    FAMILY_PACKAGES,
    FAMILY_SLOT_LABELS,
    FAMILY_SLOT_ORDER,
    FamilyPackageEntry,
    artifact_slug,
    artifact_stem,
    card_block_families,
    card_block_plugins,
    discover_family_packages,
    html_family_slot_sections,
    html_plugin_slot_sections,
    outline_families_section,
    outline_plugins_section,
    plugin_label,
)


def _catalog_cli_invocation(repo_root: Path) -> str:
    script = SCRIPT_DIR / "generate_abd_catalog.py"
    try:
        rel = script.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        rel = "skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py"
    return f"python {rel}"

# Subtitle in generated pages (repo output folder is <root>/catalog/).
CATALOG_BRAND_HTML = "<strong>abd.works</strong> &middot; Foundry"

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

# Open repo file/folder links in a new tab so the AI Garden page (dark UI) stays open.
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
    # Optional override for catalog family (from catalog_garden_family frontmatter field).
    family_override: str = ""
    # Full ## Purpose (or YAML description) — not truncated; used for kanban tooltips.
    purpose: str = ""


class AgentEntry(NamedTuple):
    name: str
    dir_name: str
    entry_file: str
    summary: str
    description: str
    rel_entry_md: str
    pkg_rel_posix: str
    garden_include: bool
    garden_order: int


class PluginArtifactEntry(NamedTuple):
    plugin_id: str
    plugin_label: str
    slot: str  # instructions | prompts
    slug: str
    display_name: str
    filename: str
    rel_path: str
    summary: str


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
    purpose_full = _extract_section(body, "Purpose")
    if purpose_full:
        purpose_full = re.split(r"\n---+\s*(?:\n|$)", purpose_full, maxsplit=1)[0]
        purpose_full = _strip_md(purpose_full.strip())
    elif fm.get("description", "").strip():
        purpose_full = _strip_md(fm.get("description", ""))
    else:
        purpose_full = ""
    return SkillEntry(
        name=name,
        dir_name=child.name,
        summary=summary,
        description=_description_skill(fm, body),
        rel_skill_md=rel,
        pkg_rel_posix=pkg_rel,
        garden_tier=tier,
        garden_order=_catalog_garden_order(fm),
        family_override=fm.get("catalog_garden_family", ""),
        purpose=purpose_full,
    )


def discover_skills(repo_root: Path) -> list[SkillEntry]:
    """Practice skills under ``<family>/skills/`` plus stage-tier skills under ``stages/``."""
    by_dir: dict[str, SkillEntry] = {}

    def push(child: Path) -> None:
        ent = _skill_entry_from_package_dir(child, repo_root)
        if ent is None:
            return
        by_dir[ent.dir_name] = ent

    for _fam_id, fam_path in FAMILY_PACKAGES.items():
        family_skills = repo_root / fam_path / "skills"
        if not family_skills.is_dir():
            continue
        for skill_md in sorted(family_skills.rglob("SKILL.md")):
            child = skill_md.parent
            if any(part.startswith(".") for part in child.relative_to(family_skills).parts):
                continue
            push(child)

    stages_root = repo_root / "stages"
    if stages_root.is_dir():
        for skill_md in sorted(stages_root.rglob("SKILL.md")):
            child = skill_md.parent
            rel = child.relative_to(stages_root)
            if any(part.startswith(".") for part in rel.parts):
                continue
            if "test" in rel.parts[:-1]:
                continue
            push(child)

    return sorted(by_dir.values(), key=lambda e: (e.garden_order, e.dir_name))


def _agent_catalog_garden_include(fm: dict[str, str]) -> bool:
    v = (fm.get("catalog_garden") or "true").strip().lower()
    return v not in ("false", "no", "0")


def discover_agents(repo_root: Path) -> list[AgentEntry]:
    """Agents under ``<family>/agents/`` (family packages only)."""
    out: list[AgentEntry] = []
    seen: set[str] = set()

    def push_agent(child: Path) -> None:
        if child.name in seen:
            return
        entry_name: str | None = None
        text = ""
        for fname in ("AGENT.md", "AGENTS.md", "SKILL.md"):
            p = child / fname
            if p.exists():
                entry_name = fname
                text = p.read_text(encoding="utf-8-sig", errors="replace")
                break
        if not entry_name:
            return
        fm = _parse_frontmatter(text)
        body = FRONTMATTER_RE.sub("", text).strip()
        if _catalog_listing_excluded(child, fm):
            return
        name = child.name
        rel = (child / entry_name).relative_to(repo_root).as_posix()
        pkg_rel = child.relative_to(repo_root).as_posix()
        summary = _table_blurb(fm, body)
        summary = _readme_catalogue_card_summary(child / "README.md", summary, fm)
        seen.add(child.name)
        out.append(
            AgentEntry(
                name=name,
                dir_name=child.name,
                entry_file=entry_name,
                summary=summary,
                description=_description_agent(fm, body),
                rel_entry_md=rel,
                pkg_rel_posix=pkg_rel,
                garden_include=_agent_catalog_garden_include(fm),
                garden_order=_catalog_garden_order(fm),
            )
        )

    for _fam_id, fam_path in FAMILY_PACKAGES.items():
        family_agents = repo_root / fam_path / "agents"
        if not family_agents.is_dir():
            continue
        for child in sorted(family_agents.iterdir()):
            if child.is_dir():
                push_agent(child)

    return out


def discover_plugin_artifacts(
    repo_root: Path, plugins: list[FamilyPackageEntry]
) -> tuple[list[PluginArtifactEntry], list[PluginArtifactEntry]]:
    """Instructions and prompts across all plugin packages."""
    instructions: list[PluginArtifactEntry] = []
    prompts: list[PluginArtifactEntry] = []
    for plugin in plugins:
        for slot, bucket in (("instructions", instructions), ("prompts", prompts)):
            for it in plugin.slots.get(slot, []):
                path = repo_root / it.rel_path
                summary = it.summary or _file_blurb(path, max_len=240)
                entry = PluginArtifactEntry(
                    plugin_id=plugin.id,
                    plugin_label=plugin.label,
                    slot=slot,
                    slug=artifact_slug(plugin.id, slot, it.name),
                    display_name=artifact_stem(it.name, slot),
                    filename=it.name,
                    rel_path=it.rel_path,
                    summary=summary,
                )
                bucket.append(entry)
    instructions.sort(key=lambda e: (e.plugin_id, e.display_name.lower()))
    prompts.sort(key=lambda e: (e.plugin_id, e.display_name.lower()))
    return instructions, prompts


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
            link = _outline_href_for_rules_folder(repo_root, package_dir, p)
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


def _resolve_website_assets(repo_root: Path) -> Path | None:
    """Locate abd-works-website (site.css, nav pattern, brand wordmarks)."""
    for candidate in (
        repo_root.parent / "abd-works-website",
        repo_root / "abd-works-website",
    ):
        if (candidate / "css" / "site.css").is_file() and (candidate / "js" / "nav.js").is_file():
            return candidate
    return None


def _commons_prefix(page_dir: Path, catalog_root: Path) -> str:
    """Relative URL prefix from page_dir to catalog_root/commons/."""
    commons_dir = catalog_root.resolve() / "commons"
    page_dir = page_dir.resolve()
    rel = os.path.relpath(commons_dir, page_dir).replace("\\", "/")
    if rel in (".", ""):
        return "commons/"
    return f"{rel}/"


def _site_base_prefix(page_dir: Path, website_root: Path | None) -> str:
    """Relative or absolute URL prefix from a catalog page to abd.works marketing site root."""
    if website_root is None or not (website_root / "index.html").is_file():
        return "https://abd.works/"
    rel = os.path.relpath(website_root.resolve(), page_dir.resolve()).replace("\\", "/")
    if rel in (".", ""):
        return ""
    return rel.rstrip("/") + "/"


def _vendor_catalog_site_assets(catalog_root: Path, website_root: Path) -> None:
    """Copy marketing-site nav/CSS/brand beside catalog HTML for file:// and static deploy."""
    dest = catalog_root / "commons"
    if dest.exists():
        _rmtree_output_dir(dest)
    dest.mkdir(parents=True)
    (dest / "brand").mkdir()
    shutil.copy2(website_root / "css" / "site.css", dest / "site.css")
    shutil.copy2(TEMPLATE_DIR / "catalog-nav.js", dest / "catalog-nav.js")
    shutil.copy2(TEMPLATE_DIR / "catalog-foundry-tour.js", dest / "catalog-foundry-tour.js")
    brand_src = website_root / "commons" / "brand"
    for name in ("abd.works.wordmark.white.svg", "abd.works.wordmark.black.svg"):
        src = brand_src / name
        if src.is_file():
            shutil.copy2(src, dest / "brand" / name)


def _h(text: str) -> str:
    return html_mod.escape(text)


def _html_attr(text: str) -> str:
    """Escape trusted HTML for double-quoted attribute values (keeps tags)."""
    return text.replace("&", "&amp;").replace('"', "&quot;")


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
    # Must match write_package_markdown_pages: doc/<kind>/<package_dir.name>/…
    pkg = package_dir.name
    rel_html = rel_under_pkg.with_suffix(".html").as_posix()
    segs = [quote(s, safe="") for s in rel_html.split("/") if s]
    return f"../doc/{kind}/{quote(pkg, safe='')}/" + "/".join(segs)


def _outline_href_for_package_md(
    repo_root: Path, package_dir: Path, file_path: Path
) -> str | None:
    """outline.md: doc/<skill|agent>/<package_dir.name>/file.html (mirrors write_package_markdown_pages)."""
    if file_path.suffix.lower() != ".md" or file_path.parent != package_dir:
        return None
    try:
        rel_pkg = package_dir.relative_to(repo_root)
    except ValueError:
        return None
    if len(rel_pkg.parts) < 2 or rel_pkg.parts[0] not in ("skills", "agents"):
        return None
    kind = "skill" if rel_pkg.parts[0] == "skills" else "agent"
    pkg = package_dir.name
    rel_html = file_path.relative_to(package_dir).with_suffix(".html").as_posix()
    segs = [quote(s, safe="") for s in rel_html.split("/") if s]
    return f"doc/{kind}/{quote(pkg, safe='')}/" + "/".join(segs)


def _outline_href_for_rules_folder(
    repo_root: Path, package_dir: Path, rules_dir: Path
) -> str | None:
    """Point rules/ folder entry at the skill or agent detail page #entry-contents."""
    if rules_dir.name != "rules" or not rules_dir.is_dir():
        return None
    try:
        rel = package_dir.relative_to(repo_root)
    except ValueError:
        return None
    if not rel.parts:
        return None
    top = rel.parts[0]
    if top == "skills":
        return f"skill/{quote(package_dir.name, safe='')}.html#entry-contents"
    if top == "agents":
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
    *,
    website_root: Path | None = None,
) -> int:
    """Emit catalog/doc/<skill|agent>/<pkg>/…/*.html for every package .md (mirrors subfolders). Returns page count."""
    tpl = _load_template("page-markdown-doc.html")
    brand = CATALOG_BRAND_HTML
    doc_root = output_catalog_dir / "doc"
    if doc_root.exists():
        _rmtree_output_dir(doc_root)
    legacy_rule = output_catalog_dir / "rule"
    if legacy_rule.exists():
        _rmtree_output_dir(legacy_rule)
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
            commons_prefix = _commons_prefix(dest.parent, output_catalog_dir)
            back = f"{nav_prefix}{'skill' if kind == 'skill' else 'agent'}/{quote(pkg, safe='')}.html"
            relpos = rel_under_pkg.as_posix()
            title = f"Foundry — {display_name} · {relpos}"
            h1 = relpos
            tagline = _file_blurb(md, max_len=400)
            nav_current = "skills" if kind == "skill" else "agents"
            html = _apply_catalog_nav(
                tpl.replace("{{CSS}}", css)
                .replace("{{TITLE}}", _h(title))
                .replace("{{BRAND}}", brand)
                .replace("{{BACK_HREF}}", back)
                .replace("{{BACK_LABEL}}", "← " + _h(display_name))
                .replace("{{BADGE}}", badge_for(rel_under_pkg))
                .replace("{{H1}}", _h(h1))
                .replace("{{TAGLINE}}", _h(tagline))
                .replace("{{DOC_BODY}}", body_html),
                nav_prefix=nav_prefix,
                commons_prefix=commons_prefix,
                current=nav_current,
                nav_site_base=_site_base_prefix(dest.parent, website_root),
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
        pkg = repo_root / a.pkg_rel_posix
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


def write_entry_detail_pages(
    output_catalog_dir: Path,
    repo_root: Path,
    skills: list[SkillEntry],
    agents: list[AgentEntry],
    detail_css: str,
    detail_tpl: str,
    *,
    website_root: Path | None = None,
) -> tuple[int, int]:
    """Write catalog/skill/<dir>.html and catalog/agent/<dir>.html. Returns counts."""
    href_to_repo = _path_up_to_ancestor(output_catalog_dir / "skill", repo_root)
    if not href_to_repo:
        href_to_repo = "./"
    nav_prefix = "../"
    detail_commons = _commons_prefix(output_catalog_dir / "skill", output_catalog_dir)
    brand = CATALOG_BRAND_HTML

    skill_out = output_catalog_dir / "skill"
    agent_out = output_catalog_dir / "agent"
    if skill_out.exists():
        _rmtree_output_dir(skill_out)
    if agent_out.exists():
        _rmtree_output_dir(agent_out)
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
        skill_plugin_id = _plugin_id_for_pkg_rel(s.pkg_rel_posix)
        if skill_plugin_id:
            skill_back_href = _plugin_detail_href(nav_prefix, skill_plugin_id)
            skill_back_label = f"← {plugin_label(skill_plugin_id)}"
        else:
            skill_back_href = _foundry_home_href(nav_prefix)
            skill_back_label = "← Foundry home"
        html = _apply_catalog_nav(
            detail_tpl.replace("{{CSS}}", detail_css)
            .replace("{{TITLE}}", _h(f"Foundry — skill · {s.name}"))
            .replace("{{BRAND}}", brand)
            .replace("{{BACK_HREF}}", skill_back_href)
            .replace("{{BACK_LABEL}}", skill_back_label)
            .replace("{{BADGE}}", "Skill")
            .replace("{{H1}}", _h(s.name))
            .replace("{{TAGLINE}}", _h(s.summary))
            .replace("{{DESCRIPTION}}", desc_html)
            .replace("{{INSTALL_BLOCK}}", install_block)
            .replace("{{HOW_IT_FITS_BLOCK}}", how_block)
            .replace("{{ENTRY_MD_COLLAPSIBLE}}", entry_md)
            .replace("{{FILE_LIST}}", file_list),
            nav_prefix=nav_prefix,
            commons_prefix=detail_commons,
            current="skills",
            nav_site_base=_site_base_prefix(skill_out, website_root),
        )
        (skill_out / f"{s.dir_name}.html").write_text(html, encoding="utf-8")

    for a in agents:
        pkg = repo_root / a.pkg_rel_posix
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
        html = _apply_catalog_nav(
            detail_tpl.replace("{{CSS}}", detail_css)
            .replace("{{TITLE}}", _h(f"Foundry — agent · {a.name}"))
            .replace("{{BRAND}}", brand)
            .replace("{{BACK_HREF}}", _foundry_home_href(nav_prefix))
            .replace("{{BACK_LABEL}}", "← Foundry home")
            .replace("{{BADGE}}", "Agent")
            .replace("{{H1}}", _h(a.name))
            .replace("{{TAGLINE}}", _h(a.summary))
            .replace("{{DESCRIPTION}}", desc_html)
            .replace("{{INSTALL_BLOCK}}", "")
            .replace("{{HOW_IT_FITS_BLOCK}}", how_block)
            .replace("{{ENTRY_MD_COLLAPSIBLE}}", entry_md)
            .replace("{{FILE_LIST}}", file_list),
            nav_prefix=nav_prefix,
            commons_prefix=detail_commons,
            current="agents",
            nav_site_base=_site_base_prefix(agent_out, website_root),
        )
        (agent_out / f"{a.dir_name}.html").write_text(html, encoding="utf-8")

    return len(skills), len(agents)


def write_plugin_artifact_detail_pages(
    output_catalog_dir: Path,
    repo_root: Path,
    instructions: list[PluginArtifactEntry],
    prompts: list[PluginArtifactEntry],
    detail_css: str,
    detail_tpl: str,
    *,
    website_root: Path | None = None,
) -> tuple[int, int]:
    """Write catalog/instruction/<slug>.html and catalog/prompt/<slug>.html."""
    brand = CATALOG_BRAND_HTML
    nav_prefix = "../"
    artifact_commons = _commons_prefix(output_catalog_dir / "instruction", output_catalog_dir)
    href_to_repo = _path_up_to_ancestor(output_catalog_dir / "instruction", repo_root) or "./"

    def write_bucket(entries: list[PluginArtifactEntry], folder: str, badge: str, back_page: str) -> int:
        out_dir = output_catalog_dir / folder
        if out_dir.exists():
            _rmtree_output_dir(out_dir)
        out_dir.mkdir(parents=True)
        folder_commons = _commons_prefix(out_dir, output_catalog_dir)
        count = 0
        for e in entries:
            src = repo_root / e.rel_path
            if not src.is_file():
                continue
            raw = src.read_text(encoding="utf-8", errors="replace")
            fm = _parse_frontmatter(raw)
            body = FRONTMATTER_RE.sub("", raw).strip()
            desc_plain = fm.get("description") or e.summary
            desc_html = _plain_overview_to_html(desc_plain) if desc_plain else _h(e.summary)
            if not desc_html.strip():
                desc_html = f"<p>{_h(e.summary)}</p>"
            entry_md = (
                _html_package_md_collapsible_sections(body)
                if body.strip()
                else f'<p class="entry-caption">(empty file)</p>'
            )
            plugin_href = f"{nav_prefix}plugin/{quote(e.plugin_id, safe='')}.html"
            nav_current = "instructions" if folder == "instruction" else "hub"
            html = _apply_catalog_nav(
                detail_tpl.replace("{{CSS}}", detail_css)
                .replace("{{TITLE}}", _h(f"Foundry — {badge.lower()} · {e.display_name}"))
                .replace("{{BRAND}}", brand)
                .replace("{{BACK_HREF}}", plugin_href)
                .replace("{{BACK_LABEL}}", f"← {e.plugin_label}")
                .replace("{{BADGE}}", badge)
                .replace("{{H1}}", _h(e.display_name))
                .replace("{{TAGLINE}}", _h(f"{e.plugin_id}/{e.slot}/{e.filename}"))
                .replace("{{DESCRIPTION}}", desc_html)
                .replace("{{INSTALL_BLOCK}}", "")
                .replace("{{HOW_IT_FITS_BLOCK}}", "")
                .replace("{{ENTRY_MD_COLLAPSIBLE}}", entry_md)
                .replace(
                    "{{FILE_LIST}}",
                    f'<p><a href="{_h(href_to_repo + e.rel_path)}" target="_blank" rel="noopener noreferrer">'
                    f"Open source file</a></p>",
                ),
                nav_prefix=nav_prefix,
                commons_prefix=folder_commons,
                current=nav_current,
                nav_site_base=_site_base_prefix(out_dir, website_root),
            )
            (out_dir / f"{e.slug}.html").write_text(html, encoding="utf-8")
            count += 1
        return count

    n_inst = write_bucket(instructions, "instruction", "Instruction", "instructions.html")
    n_prompt = write_bucket(prompts, "prompt", "Prompt", "prompts.html")
    return n_inst, n_prompt


def write_family_detail_pages(
    output_catalog_dir: Path,
    repo_root: Path,
    families: list[FamilyPackageEntry],
    detail_css: str,
    detail_tpl: str,
    skills: list[SkillEntry] | None = None,
    agents: list[AgentEntry] | None = None,
) -> int:
    """Write catalog/plugin/<id>.html. Returns plugin page count."""
    return write_plugin_detail_pages(
        output_catalog_dir,
        repo_root,
        families,
        detail_css,
        detail_tpl,
        skills=skills,
        agents=agents,
    )


def write_plugin_detail_pages(
    output_catalog_dir: Path,
    repo_root: Path,
    plugins: list[FamilyPackageEntry],
    detail_css: str,
    detail_tpl: str,
    skills: list[SkillEntry] | None = None,
    agents: list[AgentEntry] | None = None,
    *,
    website_root: Path | None = None,
) -> int:
    """Write catalog/plugin/<id>.html. Removes legacy catalog/family/."""
    plugin_out = output_catalog_dir / "plugin"
    legacy = output_catalog_dir / "family"
    if legacy.exists():
        _rmtree_output_dir(legacy)
    if plugin_out.exists():
        _rmtree_output_dir(plugin_out)
    plugin_out.mkdir(parents=True)
    href_to_repo = _path_up_to_ancestor(plugin_out, repo_root) or "./"
    nav_prefix = "../"
    plugin_commons = _commons_prefix(plugin_out, output_catalog_dir)
    brand = CATALOG_BRAND_HTML
    skill_by_dir = {s.dir_name: s for s in (skills or [])}
    agent_by_dir = {a.dir_name: a for a in (agents or [])}

    def skill_href(dir_name: str) -> str:
        return f"{nav_prefix}skill/{quote(dir_name, safe='')}.html"

    def agent_href(dir_name: str) -> str:
        return f"{nav_prefix}agent/{quote(dir_name, safe='')}.html"

    def instruction_href(_filename: str, slug: str) -> str:
        return f"{nav_prefix}instruction/{quote(slug, safe='')}.html"

    def prompt_href(_filename: str, slug: str) -> str:
        return f"{nav_prefix}prompt/{quote(slug, safe='')}.html"

    for plugin in plugins:
        pkg_dir = repo_root / plugin.id
        slot_html = html_plugin_slot_sections(
            plugin,
            href_to_repo=href_to_repo,
            skill_href=skill_href,
            agent_href=agent_href,
            instruction_href=instruction_href,
            prompt_href=prompt_href,
            skill_summary=lambda n: skill_by_dir[n].summary if n in skill_by_dir else "",
            agent_summary=lambda n: agent_by_dir[n].summary if n in agent_by_dir else "",
        )
        file_list = _html_contents_list(repo_root, pkg_dir, href_to_repo)
        readme = pkg_dir / "README.md"
        desc = _h(plugin.summary).replace("\n", "<br>\n")
        if readme.is_file():
            desc += (
                f'<p><a href="{_h(href_to_repo + plugin.rel_path + "/README.md")}"'
                f' target="_blank" rel="noopener noreferrer">README.md</a></p>'
            )
        deploy_cmd = (
            f"python scripts/deploy_family_package.py --package {plugin.id} --to &lt;workspace&gt;"
        )
        desc += f"<p class=\"entry-caption\">Deploy: <code>{deploy_cmd}</code></p>"
        html = _apply_catalog_nav(
            detail_tpl.replace("{{CSS}}", detail_css)
            .replace("{{TITLE}}", _h(f"Foundry — plugin · {plugin.label}"))
            .replace("{{BRAND}}", brand)
            .replace("{{BACK_HREF}}", _foundry_home_href(nav_prefix))
            .replace("{{BACK_LABEL}}", "← Foundry home")
            .replace("{{BADGE}}", "Plugin")
            .replace("{{H1}}", _h(plugin.label))
            .replace("{{TAGLINE}}", _h(f"{plugin.id}/ — {plugin.summary}"))
            .replace("{{DESCRIPTION}}", desc)
            .replace("{{INSTALL_BLOCK}}", "")
            .replace("{{HOW_IT_FITS_BLOCK}}", "")
            .replace(
                "{{ENTRY_MD_COLLAPSIBLE}}",
                f'<div class="plugin-slots">{slot_html}</div>',
            )
            .replace("{{FILE_LIST}}", file_list),
            nav_prefix=nav_prefix,
            commons_prefix=plugin_commons,
            current="hub",
            nav_site_base=_site_base_prefix(plugin_out, website_root),
        )
        (plugin_out / f"{plugin.id}.html").write_text(html, encoding="utf-8")

    return len(plugins)


def generate_outline_md(
    repo_root: Path,
    families: list[FamilyPackageEntry],
    skills: list[SkillEntry],
    agents: list[AgentEntry],
    md_link_prefix: str,
    catalog_cli_hint: str,
) -> str:
    lines: list[str] = [
        "# Foundry — plugins, skills & agents",
        "",
        "> Auto-generated from repository **plugins** (`<plugin>/agents|skills|content|instructions|prompts|lib|scripts/`).",
        f"> Run `{catalog_cli_hint}` to refresh.",
        "",
        "Each row gives a **short description** and where to open the source.",
        "",
    ]
    lines.extend(outline_plugins_section(families, md_link_prefix))
    lines += [
        "## Summary — Skills",
        "",
        "| Skill | Plugin | Description | Open |",
        "| --- | --- | --- | --- |",
    ]
    for s in skills:
        link = f"{md_link_prefix}{s.rel_skill_md}"
        desc = s.summary.replace("|", "\\|")
        fam = s.pkg_rel_posix.split("/")[0] if "/" in s.pkg_rel_posix else ""
        lines.append(f"| **{s.name}** | `{fam}` | {desc} | [SKILL.md]({link}) |")
    lines += [
        "",
        "## Summary — Agents",
        "",
        "| Agent | Plugin | Description | Open |",
        "| --- | --- | --- | --- |",
    ]
    for a in agents:
        link = f"{md_link_prefix}{a.rel_entry_md}"
        desc = a.summary.replace("|", "\\|")
        fam = a.pkg_rel_posix.split("/")[0] if "/" in a.pkg_rel_posix else ""
        lines.append(f"| **{a.name}** | `{fam}` | {desc} | [{a.entry_file}]({link}) |")

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
    for a in agents:
        d = repo_root / a.pkg_rel_posix
        lines += [
            f"### {a.name}",
            "",
            f"- **Directory:** [`{a.pkg_rel_posix}/`]({md_link_prefix}{a.pkg_rel_posix}/)",
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
          <p class="cap-card__title"><span class="cap-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect width="24" height="24" rx="4" fill="#1a1a1e"/><path d="M7 8h10M7 12h7M7 16h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></span>{_h(e.name)}</p>
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
          <p class="cap-card__title"><span class="cap-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect width="24" height="24" rx="4" fill="#1a1a1e"/><path d="M6 9h12v10H6z" stroke="currentColor" stroke-width="1.5"/><path d="M9 7V5h6v2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></span>{_h(e.name)}</p>
          <p class="cap-card__label">Description</p>
          <p class="cap-card__summary">{_h(e.summary)}</p>
          <p class="cap-card__more">Open agent page →</p>
        </a>"""
            )
        )
    return "\n".join(parts)


def _card_block_plugin_artifacts(entries: list[PluginArtifactEntry], kind: str) -> str:
    """kind: instruction | prompt (URL folder name)."""
    parts: list[str] = []
    for e in entries:
        href = f"{kind}/{quote(e.slug, safe='')}.html"
        parts.append(
            textwrap.dedent(
                f"""\
        <a class="cap-card" href="{_h(href)}">
          <p class="cap-card__title">{_h(e.display_name)}</p>
          <p class="cap-card__label">{_h(e.plugin_label)} · {_h(e.filename)}</p>
          <p class="cap-card__summary">{_h(e.summary)}</p>
          <p class="cap-card__more">Open {kind} page →</p>
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
        # try one level up if this is being run from the git submodule inside abd-works
        p = repo_root.parent / "commons" / "agile-garden-fragment.css"
        if not p.is_file():
            return ""
    return p.read_text(encoding="utf-8").strip() + "\n\n"


def _catalog_page_stylesheet(repo_root: Path, catalog_css: str) -> str:
    """Prepend fragment after leading @import so the combined sheet is valid and cascade order is stable."""
    frag = _abd_works_agile_garden_fragment_css(repo_root)
    text = catalog_css.strip()
    if text.startswith("@import"):
        newline = text.find("\n")
        if newline != -1:
            import_line = text[:newline].strip()
            remainder = text[newline + 1 :].lstrip("\n")
            return f"{import_line}\n\n{frag}{remainder}\n"
    return frag + catalog_css.strip() + "\n"


GARDENER_ROLE_PAGE_HREF = "/abd-ai-usage-journey/ai-users/Gardener.html"


def garden_prelude_tagline_html() -> str:
    """Trusted HTML for hub tagline + prelude paragraph."""

    return (
        "The ABD Foundry — thirty years of product engineering experience "
        "shared as agents, skills, and tools that anyone can use. "
        'Grab the repo <a href="https://github.com/abd-works/agilebydesign-skills" target="_blank" rel="noopener noreferrer">here</a>.'
    )


CATALOG_GARDEN_H1 = "The ABD Foundry"
CATALOG_PAGE_LABEL = "abd.works · Forge"
CATALOG_PAGE_TITLE_HTML = 'The ABD <span class="accent">Foundry</span>'
SKILLS_PAGE = "skills.html"
AGENTS_PAGE = "agents.html"
INSTRUCTIONS_PAGE = "instructions.html"


def _apply_catalog_nav(
    html: str, *, nav_prefix: str = "", commons_prefix: str = "commons/", current: str, nav_site_base: str = "https://abd.works/"
) -> str:
    def nav_cls(which: str) -> str:
        base = "nav__link nav__link--current" if which == current else "nav__link"
        if which == "kanban":
            base += " nav__link--kanban"
        return base

    return (
        html.replace("{{NAV_PREFIX}}", nav_prefix)
        .replace("{{NAV_CURRENT}}", current)
        .replace("{{NAV_SITE_BASE}}", nav_site_base)
        .replace("{{COMMONS_PREFIX}}", commons_prefix)
        .replace("{{NAV_HUB}}", nav_cls("hub"))
        .replace("{{NAV_SKILLS}}", nav_cls("skills"))
        .replace("{{NAV_AGENTS}}", nav_cls("agents"))
        .replace("{{NAV_INSTRUCTIONS}}", nav_cls("instructions"))
        .replace("{{NAV_KANBAN}}", nav_cls("kanban"))
    )


def catalog_garden_page_header() -> tuple[str, str, str, str]:
    """Shared brand page header for catalog listing pages."""
    return (
        CATALOG_PAGE_LABEL,
        CATALOG_PAGE_TITLE_HTML,
        garden_prelude_tagline_html(),
        CATALOG_GARDEN_H1,
    )


# Practice-tier placeholders (no skill package yet); listed after real practice entries.
GARDEN_PRACTICE_STUB_ROWS: tuple[tuple[str, str], ...] = (
    ("· cost-of-delay", "Coming soon"),
    ("· relative-sizing", "Coming soon"),
)

# Practice columns = family package ids (fixed order).
_CATALOG_SKILL_FAMILY_PRACTICE_ORDER: tuple[str, ...] = (
    "idea-shaping",
    "domain-driven-design",
    "story-driven-delivery",
    "user-experience-design",
    "architecture-centric-engineering",
    "kanban",
)
_CATALOG_SKILL_FAMILY_FOUNDATIONAL_ORDER: tuple[str, ...] = (
    "context-to-memory",
    "skill-builder",
    "utilities",
    "skill-helpers",
    "__agent_skills__",
    "",
)
_CATALOG_FAMILY_PRACTICE_FOLDERS: frozenset[str] = frozenset(_CATALOG_SKILL_FAMILY_PRACTICE_ORDER)
_CATALOG_FAMILY_FOUNDATIONAL_FOLDERS: frozenset[str] = frozenset(
    {
        "context-to-memory",
        "skill-builder",
        "utilities",
        "skill-helpers",
        "",
        "__agent_skills__",
    }
)

# Omit these catalogue families from the Agile Garden prelude (column layout only).
# Skill entries remain in outline.md, flat card grids, and detail pages.
# IDs are _skill_catalog_family() values (e.g. utilities, skill-helpers, delivery, __agent_skills__).
_CATALOG_GARDEN_PRELUDE_OMIT_FAMILIES: frozenset[str] = frozenset()

_CATALOG_FAMILY_LABELS: dict[str, str] = {
    "": "General",
    "context-to-memory": "Context to Memory",
    "kanban": "Kanban",
    "domain-driven-design": "Domain-Driven Design",
    "idea-shaping": "Idea Shaping",
    "skill-builder": "Skill Builder",
    "skill-helpers": "Skill Helpers",
    "story-driven-delivery": "Story-Driven Delivery",
    "user-experience-design": "User Experience Design",
    "architecture-centric-engineering": "Architecture-Centric Engineering",
    "utilities": "Utilities",
    "__agent_skills__": "Bundled with agents",
}

_CATALOG_FAMILY_ICONS: dict[str, str] = {
    "idea-shaping": (
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
    "story-driven-delivery": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<rect x="2" y="2" width="12" height="12" rx="1.5"/>'
        '<path d="M5 6h6M5 9h4M5 12h2"/><path d="M11 9l2 2-2 2"/></svg>'
    ),
    "user-experience-design": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<rect x="2" y="2" width="12" height="12" rx="1.5"/>'
        '<path d="M5 5h6M5 8h4M5 11h2"/></svg>'
    ),
    "architecture-centric-engineering": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M2 5l6-3 6 3-6 3-6-3z"/>'
        '<path d="M2 9l6 3 6-3"/><path d="M2 12l6 3 6-3"/></svg>'
    ),
    "kanban": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<rect x="1" y="2" width="14" height="12" rx="1.5"/>'
        '<path d="M5.5 2v12M10.5 2v12"/>'
        '<rect x="2.5" y="4" width="2" height="3" rx=".5"/>'
        '<rect x="7" y="4" width="2" height="5" rx=".5"/>'
        '<rect x="12" y="4" width="2" height="2" rx=".5"/></svg>'
    ),
    "context-to-memory": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M3 4.5h10v9H3z"/><path d="M5 7h6M5 10h6M5 13h4"/>'
        '<path d="M5 2.5h6v2H5z"/></svg>'
    ),
    "skill-builder": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M10.5 2.5l2 2-6.5 6.5-2.5.5.5-2.5L10.5 2.5z"/>'
        '<path d="M9 4l3 3"/></svg>'
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
    "__agent_skills__": (
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
        ' stroke-width="1.5" stroke-linecap="round" aria-hidden="true">'
        '<circle cx="8" cy="5" r="3"/><path d="M2 14c0-3.3 2.7-6 6-6s6 2.7 6 6"/>'
        '<path d="M8 9v2M6 11h4"/></svg>'
    ),
}

_CATALOG_AGENTS_SECTION_LABEL_SVG = (
    '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor"'
    ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<circle cx="7" cy="4.5" r="2.5"/><path d="M1.5 13c0-3 2.2-5 5.5-5s5.5 2 5.5 5"/>'
    '<path d="M7 8.5v1.5M6 10h2"/></svg>'
)
_CATALOG_AGENTS_COLUMN_ICON_SVG = (
    '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
    ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<circle cx="8" cy="5" r="3"/><path d="M2 14c0-3.3 2.7-6 6-6s6 2.7 6 6"/>'
    '<path d="M8 9v2M6 11h4"/></svg>'
)


def _skill_catalog_family(pkg_rel_posix: str) -> str:
    """Primary training area: family package (possibly nested), or agent bundle."""
    norm = pkg_rel_posix.replace("\\", "/").strip("/")
    if not norm:
        return ""
    if norm.split("/")[0] == "agents":
        return "__agent_skills__"
    for fam_id, fam_path in FAMILY_PACKAGES.items():
        prefix = fam_path.rstrip("/") + "/skills/"
        if norm.startswith(prefix):
            return fam_id
    return ""


def _plugin_id_for_pkg_rel(pkg_rel_posix: str) -> str:
    """Plugin id owning a skill or agent package path."""
    norm = pkg_rel_posix.replace("\\", "/").strip("/")
    if not norm:
        return ""
    for fam_id, fam_path in FAMILY_PACKAGES.items():
        fp = fam_path.rstrip("/")
        if norm == fp or norm.startswith(fp + "/"):
            return fam_id
    return ""


def _foundry_home_href(nav_prefix: str) -> str:
    return f"{nav_prefix}index.html"


def _plugin_detail_href(nav_prefix: str, plugin_id: str) -> str:
    return f"{nav_prefix}plugin/{quote(plugin_id, safe='')}.html"


def _catalog_family_icon(cat: str) -> str:
    return _CATALOG_FAMILY_ICONS.get(cat, _CATALOG_FAMILY_ICONS[""])


def _catalog_family_label(cat: str) -> str:
    return _CATALOG_FAMILY_LABELS.get(cat, cat.replace("-", " ").title())


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


def _html_agile_garden_agent_col(a: AgentEntry) -> str:
    """Each agent gets its own column so agents sit side by side in the prelude grid."""
    href = _agile_garden_agent_href(a.dir_name)
    return (
        f'    <div class="catalog-garden-col">\n'
        f'      <div class="catalog-garden-col-header catalog-garden-col-header--foundational">\n'
        f"        {_CATALOG_AGENTS_COLUMN_ICON_SVG}\n"
        f'        <span><a href="{href}" style="color:inherit;text-decoration:none;">{_h(a.name)}</a></span>\n'
        f"      </div>\n"
        f'      <div class="catalog-garden-row">'
        f'<span class="catalog-garden-desc">{_h(a.summary)}</span></div>\n'
        f"    </div>\n"
    )


def _html_agile_garden_stub_row(label: str, desc: str) -> str:
    return (
        f'      <div class="catalog-garden-row"><span class="catalog-garden-name catalog-garden-name--dim">'
        f"{_h(label)}</span>"
        f'<span class="catalog-garden-desc catalog-garden-desc--muted">{_h(desc)}</span></div>\n'
    )


def _html_catalog_skill_family_column_entries(
    cat: str,
    entries: list[SkillEntry],
    *,
    foundational: bool,
    extra_rows: str = "",
) -> str:
    icon = _catalog_family_icon(cat)
    label = _catalog_family_label(cat)
    header_cls = "catalog-garden-col-header"
    if foundational:
        header_cls += " catalog-garden-col-header--foundational"
    rows = "".join(
        _html_agile_garden_skill_row(s, foundational=foundational) for s in entries
    )
    rows += extra_rows
    return (
        f'    <div class="catalog-garden-col">\n'
        f'      <div class="{header_cls}">\n'
        f"        {icon}\n"
        f"        <span>{_h(label)}</span>\n"
        f"      </div>\n"
        f"{rows}"
        f"    </div>\n"
    )


def build_agile_garden_prelude_html(
    skills: list[SkillEntry],
    agents: list[AgentEntry],
    *,
    include_title_block: bool = True,
    include_garden_lists: bool = True,
    include_mission: bool = False,
    omit_garden_families: frozenset[str] = frozenset(),
) -> str:
    """Practice families = top-level folder under ``skills/`` (multi-column grid + icons); foundational below."""
    by_cat: dict[str, list[SkillEntry]] = defaultdict(list)
    for s in skills:
        fam = s.family_override if s.family_override else _skill_catalog_family(s.pkg_rel_posix)
        if fam in omit_garden_families:
            continue
        by_cat[fam].append(s)
    for cat in by_cat:
        by_cat[cat].sort(key=lambda s: (s.garden_order, s.name.lower()))

    placed: set[str] = set()
    practice_fragments: list[str] = []

    for cat in _CATALOG_SKILL_FAMILY_PRACTICE_ORDER:
        ents = by_cat.get(cat)
        if not ents:
            continue
        placed.add(cat)
        stubs = ""
        if cat == "idea-shaping":
            stubs = "".join(
                _html_agile_garden_stub_row(label, desc)
                for label, desc in GARDEN_PRACTICE_STUB_ROWS
            )
        practice_fragments.append(
            _html_catalog_skill_family_column_entries(
                cat, ents, foundational=False, extra_rows=stubs
            )
        )

    extras_practice: list[str] = []
    extras_foundational: list[str] = []

    for cat, ents in sorted(by_cat.items(), key=lambda kv: kv[0].lower()):
        if not ents or cat in placed:
            continue
        if cat in _CATALOG_FAMILY_PRACTICE_FOLDERS:
            extras_practice.append(
                _html_catalog_skill_family_column_entries(cat, ents, foundational=False)
            )
            placed.add(cat)
        elif cat not in _CATALOG_FAMILY_FOUNDATIONAL_FOLDERS:
            extras_foundational.append(
                _html_catalog_skill_family_column_entries(cat, ents, foundational=True)
            )
            placed.add(cat)

    practice_cols = "".join(practice_fragments) + "".join(extras_practice)

    foundational_fragments: list[str] = []
    for cat in _CATALOG_SKILL_FAMILY_FOUNDATIONAL_ORDER:
        if cat in placed:
            continue
        ents = by_cat.get(cat)
        if not ents:
            continue
        placed.add(cat)
        foundational_fragments.append(
            _html_catalog_skill_family_column_entries(cat, ents, foundational=True)
        )

    for frag in extras_foundational:
        foundational_fragments.append(frag)

    foundational_cols = "".join(foundational_fragments)

    n_practice_cols = practice_cols.count('<div class="catalog-garden-col">')
    practice_grid_style = ""
    if n_practice_cols:
        practice_grid_style = (
            f' style="grid-template-columns: repeat({n_practice_cols}, minmax(0, 1fr));"'
        )

    n_found_cols = foundational_cols.count('<div class="catalog-garden-col">')
    foundational_grid_style = ""
    if n_found_cols:
        foundational_grid_style = (
            f' style="grid-template-columns: repeat({n_found_cols}, minmax(0, 1fr));"'
        )

    agents_show = sorted(
        [a for a in agents if a.garden_include],
        key=lambda a: (a.garden_order, a.name.lower()),
    )
    agents_section = ""
    if agents_show:
        n_agent_cols = len(agents_show)
        agent_grid_style = f' style="grid-template-columns: repeat({n_agent_cols}, minmax(0, 1fr));"'
        agent_cols_html = "".join(_html_agile_garden_agent_col(a) for a in agents_show)
        agents_section = (
            '\n  <div class="catalog-section-label catalog-section-label--agents">\n'
            f"    {_CATALOG_AGENTS_SECTION_LABEL_SVG}\n"
            "    Agents — Role-Based AI Collaborators\n"
            "  </div>\n"
            f'  <div class="catalog-agents-grid"{agent_grid_style}>\n'
            f"{agent_cols_html}"
            "  </div>\n"
        )

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

    lists_inner = ""

    mission = _html_agile_garden_mission_block() if include_mission else ""
    if include_title_block:
        aria = ' aria-labelledby="catalog-agile-garden-h2"'
        title_block = (
            f'  <h2 class="catalog-prelude-heading" id="catalog-agile-garden-h2">'
            f"{CATALOG_GARDEN_H1}</h2>\n"
            f'  <p class="catalog-prelude-tagline">{garden_prelude_tagline_html()}</p>\n'
        )
    else:
        aria = f' aria-label="{CATALOG_GARDEN_H1}"'
        title_block = ""

    if include_garden_lists:
        lists_inner += '  <div class="catalog-garden-lists">\n'
        if practice_cols.strip():
            lists_inner += '    <div class="catalog-section-label">\n'
            lists_inner += f"      {practice_label_svg}\n"
            lists_inner += "      Practice Skills — What We Do\n"
            lists_inner += "    </div>\n"
            lists_inner += f'    <div class="catalog-practice-grid"{practice_grid_style}>\n'
            lists_inner += practice_cols
            lists_inner += "    </div>\n"
        if foundational_cols.strip():
            lists_inner += (
                '    <div class="catalog-section-label catalog-section-label--foundational">\n'
            )
            lists_inner += f"      {foundational_label_svg}\n"
            lists_inner += "      Foundational Skills — Enhance the Way Skills Run\n"
            lists_inner += "    </div>\n"
            lists_inner += f'    <div class="catalog-foundational-grid"{foundational_grid_style}>\n'
            lists_inner += foundational_cols
            lists_inner += "    </div>\n"
        lists_inner += agents_section
        lists_inner += "  </div>\n"

    return (
        f'<section class="catalog-prelude" id="agile-garden"{aria}>\n'
        f"{title_block}"
        f"{mission}"
        f"{lists_inner}"
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
        "  Columns = first path segment under skills/; delivery/context-to-memory is its own column.\n"
        "  Agent-bundled skills use __agent_skills__.\n"
        "  Optional: catalog_garden_order: <int> for sort order within a column.\n"
        "  Agents: catalog_garden: false to omit from this list (default: include).\n"
        "-->\n"
    )
    try:
        if p.parent.is_dir():
            p.write_text(header + section_html, encoding="utf-8")
    except OSError:
        pass


def _html_catalog_section(
    section_id: str,
    title: str,
    count_label: str,
    body_inner: str,
    *,
    open_default: bool = False,
) -> str:
    """One collapsible block for the single-page index (matches abd-works AI Garden layout)."""
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
    families: list[FamilyPackageEntry],
    skills: list[SkillEntry],
    agents: list[AgentEntry],
    *,
    omit_garden_families: frozenset[str] = frozenset(),
    website_root: Path | None = None,
) -> tuple[int, int, int, int, int, int]:
    """Write index, plugins, skills, agents pages and detail pages.

    Returns (plugin_detail_count, skill_detail_count, agent_detail_count,
    markdown_doc_page_count, instruction_detail_count, prompt_detail_count).
    """
    up_to_repo = _path_up_to_ancestor(output_catalog_dir, repo_root)
    if not up_to_repo:
        up_to_repo = "./"
    idx_tpl = _load_template("page-catalog.html")
    idx_single_tpl = _load_template("page-catalog-index.html")
    css = _catalog_page_stylesheet(repo_root, _load_template("catalog.css"))
    detail_tpl = _load_template("page-entry-detail.html")
    hub_commons = _commons_prefix(output_catalog_dir, output_catalog_dir)

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
        kanban_embed: str = "",
        extra_css: str = "",
        page_title_html: str = "",
        page_tagline_html: str = "",
        commons_prefix: str = "commons/",
        nav_prefix: str = "",
        page_dir: Path | None = None,
        hero_practice_legend: str = "",
    ) -> str:
        css_block = css + extra_css if extra_css else css
        if not page_title_html:
            page_title_html = CATALOG_PAGE_TITLE_HTML
        if not page_tagline_html:
            page_tagline_html = tagline or garden_prelude_tagline_html()
        pd = page_dir or output_catalog_dir
        return _apply_catalog_nav(
            tpl.replace("{{CSS}}", css_block)
            .replace("{{TITLE}}", title)
            .replace("{{BRAND}}", brand)
            .replace("{{H1}}", h1)
            .replace("{{TAGLINE}}", tagline)
            .replace("{{PAGE_TITLE_HTML}}", page_title_html)
            .replace("{{PAGE_TAGLINE_HTML}}", page_tagline_html)
            .replace("{{HERO_PRACTICE_LEGEND}}", hero_practice_legend)
            .replace("{{INTRO}}", intro)
            .replace("{{KANBAN_EMBED}}", kanban_embed)
            .replace("{{BODY_INNER}}", body_inner),
            nav_prefix=nav_prefix,
            commons_prefix=commons_prefix,
            current=nav_current,
            nav_site_base=_site_base_prefix(pd, website_root),
        )

    brand = CATALOG_BRAND_HTML
    instructions, prompts = discover_plugin_artifacts(repo_root, families)

    plugins_intro = (
        "<p>Repo-root capability plugins deploy with "
        "<code>scripts/deploy_family_package.py</code>. "
        "Each plugin bundles agents, skills, instructions, prompts, and shared assets.</p>"
    )
    plugins_grid = card_block_plugins(families)
    skills_intro = _load_intro_fragment(
        "catalog-skills-intro.html",
        "<p>Open a card for a full page on that skill.</p>",
    )
    agents_intro = _load_intro_fragment(
        "catalog-agents-intro.html",
        "<p>Open a card for a full page on that agent.</p>",
    )
    instructions_intro = (
        "<p>Cursor rules and instruction files shipped inside plugins "
        "(<code>.mdc</code>, <code>.instructions.md</code>).</p>"
    )
    prompts_intro = (
        "<p>Slash commands shipped inside plugins (<code>.prompt.md</code>).</p>"
    )
    skills_grid = _card_block_skills(skills, up_to_repo)
    agents_grid = _card_block_agents(agents, up_to_repo)
    instructions_grid = _card_block_plugin_artifacts(instructions, "instruction")
    prompts_grid = _card_block_plugin_artifacts(prompts, "prompt")
    index_sections = "\n\n".join(
        [
            _html_catalog_section(
                "catalog-plugins",
                "Plugins",
                f"({len(families)})",
                f"{plugins_intro}\n<p><a href=\"plugins.html\">Open plugins grid →</a></p>\n<div class=\"cap-grid\">\n{plugins_grid}\n</div>",
                open_default=True,
            ),
            _html_catalog_section(
                "catalog-skills",
                "Skills",
                f"({len(skills)})",
                (
                    f"{skills_intro}\n"
                    f'<p><a href="{SKILLS_PAGE}">Open skills grid →</a></p>'
                ),
            ),
            _html_catalog_section(
                "catalog-agents",
                "Agents",
                f"({len(agents)})",
                (
                    f"{agents_intro}\n"
                    f'<p><a href="{AGENTS_PAGE}">Open agents grid →</a></p>'
                ),
            ),
            _html_catalog_section(
                "catalog-instructions",
                "Instructions",
                f"({len(instructions)})",
                f"{instructions_intro}\n<p><a href=\"instructions.html\">Open instructions grid →</a></p>",
            ),
            _html_catalog_section(
                "catalog-prompts",
                "Prompts",
                f"({len(prompts)})",
                f"{prompts_intro}\n<p><a href=\"prompts.html\">Open prompts grid →</a></p>",
            ),
        ]
    )
    write_agile_garden_prelude_fragment(
        repo_root,
        build_agile_garden_prelude_html(
            skills,
            agents,
            include_title_block=True,
            include_mission=True,
            omit_garden_families=omit_garden_families,
        ),
    )
    index_body = ""
    page_label, page_title_html, page_tagline_html, garden_h1 = catalog_garden_page_header()
    skill_map = skill_dir_map_from_entries(skills)
    purpose_map = skill_purpose_map_from_entries(skills)
    kanban_model = load_kanban_model(repo_root)
    kanban_embed = build_catalog_hub_kanban_embed_html(
        kanban_model, skill_map, skill_purpose_by_name=purpose_map
    )
    hero_practice_legend = ""
    index_kanban_css = load_catalog_embed_kanban_css(repo_root, TEMPLATE_DIR)
    index_html = fill(
        idx_single_tpl,
        title="Foundry — hub",
        brand=brand,
        h1=garden_h1,
        tagline=page_tagline_html,
        intro="",
        nav_current="hub",
        body_inner=index_body,
        kanban_embed=kanban_embed,
        extra_css=index_kanban_css,
        page_title_html=page_title_html,
        page_tagline_html=page_tagline_html,
        commons_prefix=hub_commons,
        hero_practice_legend=hero_practice_legend,
    )
    (output_catalog_dir / "index.html").write_text(index_html, encoding="utf-8")

    plugins_body = (
        f"<h2>Plugins ({len(families)})</h2>"
        f"<p>Each plugin is a deployable package: <code>agents/</code> · <code>skills/</code> · "
        f"<code>content/</code> · <code>instructions/</code> · <code>prompts/</code> · "
        f"<code>lib/</code> · <code>scripts/</code></p>"
        f'<div class="cap-grid">{plugins_grid}</div>'
    )
    (output_catalog_dir / "plugins.html").write_text(
        fill(
            idx_tpl,
            title="Foundry — hub",
            brand=brand,
            h1=garden_h1,
            tagline=page_tagline_html,
            intro=plugins_intro,
            nav_current="hub",
            body_inner=plugins_body,
        ),
        encoding="utf-8",
    )
    legacy_families = output_catalog_dir / "families.html"
    if legacy_families.is_file():
        legacy_families.unlink()

    skills_body = (
        f"<h2>Skills ({len(skills)})</h2>"
        f"{skills_intro}"
        f'<div class="cap-grid">{skills_grid}</div>'
    )
    (output_catalog_dir / SKILLS_PAGE).write_text(
        fill(
            idx_tpl,
            title="Foundry — skills",
            brand=brand,
            h1=garden_h1,
            tagline=page_tagline_html,
            intro="",
            nav_current="skills",
            body_inner=skills_body,
        ),
        encoding="utf-8",
    )
    agents_body = (
        f"<h2>Agents ({len(agents)})</h2>"
        f"{agents_intro}"
        f'<div class="cap-grid">{agents_grid}</div>'
    )
    (output_catalog_dir / AGENTS_PAGE).write_text(
        fill(
            idx_tpl,
            title="Foundry — agents",
            brand=brand,
            h1=garden_h1,
            tagline=page_tagline_html,
            intro="",
            nav_current="agents",
            body_inner=agents_body,
        ),
        encoding="utf-8",
    )

    instructions_body = (
        f"<h2>All indexed instructions ({len(instructions)})</h2>"
        f'<div class="cap-grid">{instructions_grid}</div>'
    )
    (output_catalog_dir / "instructions.html").write_text(
        fill(
            idx_tpl,
            title="Foundry — instructions",
            brand=brand,
            h1=garden_h1,
            tagline=page_tagline_html,
            intro=instructions_intro,
            nav_current="instructions",
            body_inner=instructions_body,
        ),
        encoding="utf-8",
    )

    prompts_body = (
        f"<h2>All indexed prompts ({len(prompts)})</h2>"
        f'<div class="cap-grid">{prompts_grid}</div>'
    )
    (output_catalog_dir / "prompts.html").write_text(
        fill(
            idx_tpl,
            title="Foundry — prompts",
            brand=brand,
            h1=garden_h1,
            tagline=page_tagline_html,
            intro=prompts_intro,
            nav_current="hub",
            body_inner=prompts_body,
        ),
        encoding="utf-8",
    )

    n_md_pages = write_package_markdown_pages(output_catalog_dir, repo_root, skills, agents, css, website_root=website_root)
    n_plugin_pages = write_plugin_detail_pages(
        output_catalog_dir, repo_root, families, css, detail_tpl, skills=skills, agents=agents, website_root=website_root
    )
    n_inst_pages, n_prompt_pages = write_plugin_artifact_detail_pages(
        output_catalog_dir, repo_root, instructions, prompts, css, detail_tpl, website_root=website_root
    )
    n_skill_pages, n_agent_pages = write_entry_detail_pages(
        output_catalog_dir, repo_root, skills, agents, css, detail_tpl, website_root=website_root
    )
    return n_plugin_pages, n_skill_pages, n_agent_pages, n_md_pages, n_inst_pages, n_prompt_pages


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the ABD Foundry (HTML + outline.md under catalog/).")
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
    parser.add_argument(
        "--omit-garden-families",
        type=str,
        default="",
        metavar="IDS",
        help="Comma-separated prelude column family ids to omit (e.g. utilities,skill-helpers). "
        "Same ids as path buckets from _skill_catalog_family. Adds to "
        "_CATALOG_GARDEN_PRELUDE_OMIT_FAMILIES.",
    )
    args = parser.parse_args()

    cli_omit = frozenset(
        x.strip()
        for x in (args.omit_garden_families or "").split(",")
        if x.strip()
    )
    omit_garden_families = _CATALOG_GARDEN_PRELUDE_OMIT_FAMILIES | cli_omit

    repo_root = (args.repo_root or _repo_root_from_skill_package(SKILL_DIR)).resolve()
    output_dir = (args.output_dir or (repo_root / "catalog")).resolve()

    if not any((repo_root / p).is_dir() for p in FAMILY_PACKAGES.values()):
        raise SystemExit(f"No family packages found under {repo_root}")

    families = discover_family_packages(repo_root)
    skills = discover_skills(repo_root)
    agents = discover_agents(repo_root)
    if args.scaffold_readmes:
        n = scaffold_catalog_readmes(repo_root, skills, agents)
        print(f"  scaffolded {n} README.md file(s) for the AI Garden")
        families = discover_family_packages(repo_root)
        skills = discover_skills(repo_root)
        agents = discover_agents(repo_root)
    if not families and not skills and not agents:
        raise SystemExit("No family packages, skills, or agents discovered.")

    # Sort skills by canonical family order, then by garden_order within each family,
    # then alphabetically — so outline.md and the flat skills grid respect the same
    # sequence as the Agile Garden prelude columns.
    _all_family_order = list(_CATALOG_SKILL_FAMILY_PRACTICE_ORDER) + [
        f for f in _CATALOG_SKILL_FAMILY_FOUNDATIONAL_ORDER
        if f not in _CATALOG_SKILL_FAMILY_PRACTICE_ORDER
    ]
    _family_idx: dict[str, int] = {f: i for i, f in enumerate(_all_family_order)}
    skills.sort(
        key=lambda s: (
            _family_idx.get(s.family_override if s.family_override else _skill_catalog_family(s.pkg_rel_posix), 999),
            s.garden_order,
            s.name.lower(),
        )
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    website_root = _resolve_website_assets(repo_root)
    if website_root:
        _vendor_catalog_site_assets(output_dir, website_root)
        print(f"  vendored site nav/CSS to {output_dir / 'commons'}")
    else:
        print(
            "  warning: abd-works-website not found (expected sibling abd-works-website/) — "
            "site nav will not work until you regenerate with abd-works-website present"
        )

    # outline.md, index/skills/agents, skill/, agent/ all live directly under catalog/
    outline_path = output_dir / "outline.md"
    md_prefix = _path_up_to_ancestor(output_dir, repo_root)
    catalog_cli_hint = _catalog_cli_invocation(repo_root)
    outline_path.write_text(
        generate_outline_md(repo_root, families, skills, agents, md_prefix, catalog_cli_hint),
        encoding="utf-8",
    )
    print(f"  wrote {outline_path}")

    n_plugin_detail, n_sk_detail, n_ag_detail, n_md_pages, n_inst_detail, n_prompt_detail = write_html_pages(
        output_dir,
        repo_root,
        families,
        skills,
        agents,
        omit_garden_families=omit_garden_families,
        website_root=website_root,
    )
    catalog_css = _catalog_page_stylesheet(repo_root, _load_template("catalog.css"))
    _, _, kanban_tagline, kanban_h1 = catalog_garden_page_header()
    skill_map = skill_dir_map_from_entries(skills)
    purpose_map = skill_purpose_map_from_entries(skills)
    kanban_path = write_kanban_layout_pages(
        output_dir,
        repo_root,
        skill_map,
        catalog_css,
        brand=CATALOG_BRAND_HTML,
        h1=kanban_h1,
        tagline=kanban_tagline,
        template_dir=TEMPLATE_DIR,
        skill_purpose_by_name=purpose_map,
    )
    print(f"  wrote {kanban_path}")
    if sync_bootcamp_part3_kanban(repo_root, skill_map, skill_purpose_by_name=purpose_map):
        print("  synced abd-ai-augmented-bootcamp slides/part3/part3.html (kanban kb-slides)")
    other = patch_bootcamp_slide_files(repo_root, skill_map)
    for rel in other:
        print(f"  patched bootcamp slides/{rel}")
    print(f"  wrote {output_dir / 'index.html'}")
    print(f"  wrote {output_dir / 'plugins.html'}")
    print(f"  wrote {output_dir / SKILLS_PAGE}")
    print(f"  wrote {output_dir / AGENTS_PAGE}")
    print(f"  wrote {output_dir / 'instructions.html'}")
    print(f"  wrote {output_dir / 'prompts.html'}")
    print(f"  wrote {n_md_pages} markdown pages under catalog/doc/")
    print(f"  wrote {n_plugin_detail} plugin detail pages under catalog/plugin/")
    print(f"  wrote {n_sk_detail} skill detail pages under catalog/skill/")
    print(f"  wrote {n_ag_detail} agent detail pages under catalog/agent/")
    print(f"  wrote {n_inst_detail} instruction detail pages under catalog/instruction/")
    print(f"  wrote {n_prompt_detail} prompt detail pages under catalog/prompt/")
    print(f"  ({len(families)} plugins, {len(skills)} skills, {len(agents)} agents)")


if __name__ == "__main__":
    main()
