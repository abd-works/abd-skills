"""Plugin package discovery and catalog sections for the AI Garden."""
from __future__ import annotations

import html as html_mod
import re
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple
from urllib.parse import quote

# Repo-root plugin packages (deploy via deploy_family_package.py).
FAMILY_PACKAGES = (
    "delivery",
    "story-driven-delivery",
    "domain-driven-design",
    "architecture-centric-engineering",
    "user-experience-design",
    "context-to-memory",
    "idea-shaping",
    "skill-builder",
    "skill-helpers",
    "utilities",
)

FAMILY_CATALOG_ALIASES = {"idea-shaping": "Idea Shaping"}

FAMILY_SLOT_ORDER = (
    "agents",
    "skills",
    "content",
    "instructions",
    "prompts",
    "lib",
    "scripts",
)

PLUGIN_CARD_SLOTS = ("agents", "skills", "instructions", "prompts")

FAMILY_SLOT_LABELS: dict[str, str] = {
    "agents": "Agents — orchestrators (AGENT.md / AGENTS.md)",
    "skills": "Skills — practice packages (SKILL.md)",
    "content": "Content — shared prose merged on deploy",
    "instructions": "Instructions — .mdc / .instructions.md → Cursor rules",
    "prompts": "Prompts — .prompt.md → slash commands",
    "lib": "Lib — shared Python packages",
    "scripts": "Scripts — package-level automation",
}

PLUGIN_SLOT_SHORT_LABELS: dict[str, str] = {
    "agents": "Agents",
    "skills": "Skills",
    "instructions": "Instructions",
    "prompts": "Prompts",
}

PLUGIN_SLOT_CAPTIONS: dict[str, str] = {
    "agents": "Orchestrators shipped as agent packages.",
    "skills": "Practice skills with rules, templates, and scanners.",
    "instructions": "Always-on or scoped rules merged into .cursor/rules on deploy.",
    "prompts": "Slash commands merged into .cursor/commands on deploy.",
}

_SKIP_NAMES = frozenset({".git", "__pycache__", ".pytest_cache", "node_modules", ".cursor"})
_FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)


class FamilySlotEntry(NamedTuple):
    name: str
    rel_path: str
    entry_kind: str  # agent | skill | file | dir
    entry_file: str = ""
    summary: str = ""


class FamilyPackageEntry(NamedTuple):
    id: str
    label: str
    rel_path: str
    summary: str
    slots: dict[str, list[FamilySlotEntry]]
    skill_dir_names: tuple[str, ...]
    agent_dir_names: tuple[str, ...]


def family_label(family_id: str) -> str:
    return FAMILY_CATALOG_ALIASES.get(family_id, family_id.replace("-", " ").title())


def plugin_label(plugin_id: str) -> str:
    return family_label(plugin_id)


def artifact_stem(filename: str, slot: str) -> str:
    if slot == "prompts" and filename.endswith(".prompt.md"):
        return filename[: -len(".prompt.md")]
    if filename.endswith(".instructions.md"):
        return filename[: -len(".instructions.md")]
    if filename.endswith(".mdc"):
        return filename[: -len(".mdc")]
    return Path(filename).stem


def artifact_slug(plugin_id: str, slot: str, filename: str) -> str:
    """Unique slug per source file (handles .mdc + .instructions.md pairs)."""
    safe = re.sub(r"[^\w.-]+", "-", filename).strip("-").replace(".", "-")
    return f"{plugin_id}--{slot}--{safe}"


def _file_summary(path: Path, max_len: int = 240) -> str:
    try:
        raw = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""
    fm_desc = ""
    if raw.startswith("---"):
        m = _FRONTMATTER_RE.match(raw)
        if m:
            block = m.group(0)
            dm = re.search(r"^description:\s*>-?\s*\n((?:[ \t]+.*\n?)+)", block, re.MULTILINE)
            if dm:
                fm_desc = " ".join(
                    ln.strip() for ln in dm.group(1).splitlines() if ln.strip()
                )
            else:
                sm = re.search(
                    r'^description:\s*["\']?(.*?)["\']?\s*$',
                    block,
                    re.MULTILINE,
                )
                if sm:
                    fm_desc = sm.group(1).strip().strip('"').strip("'")
            raw = raw[m.end() :]
    if fm_desc:
        text = fm_desc
    else:
        text = ""
        for line in raw.splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            s = re.sub(r"^#+\s*", "", s)
            s = re.sub(r"\*\*|__|`", "", s)
            if len(s) >= 8:
                text = s
                break
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rsplit(" ", 1)[0] + " …"


def _scan_slot(repo_root: Path, family_id: str, slot: str) -> list[FamilySlotEntry]:
    slot_dir = repo_root / family_id / slot
    if not slot_dir.is_dir():
        return []
    out: list[FamilySlotEntry] = []

    if slot == "agents":
        for child in sorted(slot_dir.iterdir(), key=lambda p: p.name.lower()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            entry = next(
                (f for f in ("AGENT.md", "AGENTS.md") if (child / f).is_file()),
                "",
            )
            if not entry:
                continue
            out.append(
                FamilySlotEntry(
                    name=child.name,
                    rel_path=child.relative_to(repo_root).as_posix(),
                    entry_kind="agent",
                    entry_file=entry,
                )
            )
        return out

    if slot == "skills":
        for child in sorted(slot_dir.iterdir(), key=lambda p: p.name.lower()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            if not (child / "SKILL.md").is_file():
                continue
            out.append(
                FamilySlotEntry(
                    name=child.name,
                    rel_path=child.relative_to(repo_root).as_posix(),
                    entry_kind="skill",
                    entry_file="SKILL.md",
                )
            )
        return out

    for path in sorted(slot_dir.rglob("*"), key=lambda p: p.as_posix().lower()):
        if not path.is_file():
            continue
        if any(part.startswith(".") or part in _SKIP_NAMES for part in path.parts):
            continue
        rel = path.relative_to(repo_root).as_posix()
        summary = ""
        if slot in ("instructions", "prompts"):
            summary = _file_summary(path)
        out.append(
            FamilySlotEntry(
                name=path.name,
                rel_path=rel,
                entry_kind="file",
                entry_file=path.name,
                summary=summary,
            )
        )
    return out


def discover_family_packages(repo_root: Path) -> list[FamilyPackageEntry]:
    """One entry per repo-root plugin package with full slot inventory."""
    out: list[FamilyPackageEntry] = []
    for family_id in FAMILY_PACKAGES:
        pkg = repo_root / family_id
        if not pkg.is_dir():
            continue
        slots: dict[str, list[FamilySlotEntry]] = {}
        for slot in FAMILY_SLOT_ORDER:
            slots[slot] = _scan_slot(repo_root, family_id, slot)
        readme = pkg / "README.md"
        summary = _read_readme_blurb(readme) if readme.is_file() else ""
        if not summary:
            counts = ", ".join(
                f"{len(slots[s])} {s}" for s in FAMILY_SLOT_ORDER if slots[s]
            )
            summary = counts or "Capability plugin package."
        out.append(
            FamilyPackageEntry(
                id=family_id,
                label=family_label(family_id),
                rel_path=family_id,
                summary=summary,
                slots=slots,
                skill_dir_names=tuple(x.name for x in slots.get("skills", [])),
                agent_dir_names=tuple(x.name for x in slots.get("agents", [])),
            )
        )
    return out


def discover_plugin_packages(repo_root: Path) -> list[FamilyPackageEntry]:
    """Alias for discover_family_packages (user-facing name: plugin)."""
    return discover_family_packages(repo_root)


def _read_readme_blurb(readme: Path, max_len: int = 320) -> str:
    if not readme.is_file():
        return ""
    text = readme.read_text(encoding="utf-8-sig", errors="replace")
    m = re.search(r"^##\s+Overview\s*\n(.*?)(?=\n##\s|\Z)", text, re.DOTALL | re.MULTILINE)
    block = m.group(1).strip() if m else ""
    if not block:
        for line in text.splitlines():
            s = line.strip()
            if s and not s.startswith("#") and s != "---":
                block = s
                break
    block = re.sub(r"\s+", " ", block)
    if len(block) <= max_len:
        return block
    return block[: max_len - 1].rsplit(" ", 1)[0] + " …"


def family_counts_line(fam: FamilyPackageEntry) -> str:
    parts: list[str] = []
    if fam.agent_dir_names:
        parts.append(f"{len(fam.agent_dir_names)} agent{'s' if len(fam.agent_dir_names) != 1 else ''}")
    if fam.skill_dir_names:
        parts.append(f"{len(fam.skill_dir_names)} skill{'s' if len(fam.skill_dir_names) != 1 else ''}")
    for slot in ("instructions", "prompts", "content", "lib", "scripts"):
        n = len(fam.slots.get(slot, []))
        if n:
            parts.append(f"{n} {slot}")
    return " · ".join(parts) if parts else "plugin slots"


def plugin_counts_line(fam: FamilyPackageEntry) -> str:
    return family_counts_line(fam)


def outline_families_section(
    families: list[FamilyPackageEntry], md_prefix: str
) -> list[str]:
    lines = [
        "## Plugins",
        "",
        "Repo-root capability plugins (`<plugin>/agents|skills|content|instructions|prompts|lib|scripts/`).",
        "",
        "| Plugin | Summary | Open |",
        "| --- | --- | --- |",
    ]
    for fam in families:
        link = f"{md_prefix}{fam.rel_path}/README.md"
        desc = fam.summary.replace("|", "\\|")
        lines.append(f"| **{fam.label}** (`{fam.id}/`) | {desc} | [README.md]({link}) |")
    lines += ["", "### Plugin layout (detail)", ""]
    for fam in families:
        lines += [
            f"#### {fam.label} — `{fam.id}/`",
            "",
            fam.summary,
            "",
        ]
        for slot in FAMILY_SLOT_ORDER:
            items = fam.slots.get(slot, [])
            lines.append(f"**{FAMILY_SLOT_LABELS[slot]}**")
            lines.append("")
            if not items:
                lines.append(f"- _(empty `{fam.id}/{slot}/`)_")
            elif slot in ("agents", "skills"):
                for it in items:
                    entry = it.entry_file or "—"
                    lines.append(
                        f"- **{it.name}** — [{entry}]({md_prefix}{it.rel_path}/{entry})"
                    )
            elif slot in ("instructions", "prompts"):
                for it in items:
                    slug = artifact_slug(fam.id, slot, it.name)
                    lines.append(
                        f"- **{artifact_stem(it.name, slot)}** — "
                        f"[{it.name}]({md_prefix}{it.rel_path}) "
                        f"(catalog: `{slot}/{slug}.html`)"
                    )
            else:
                for it in items:
                    lines.append(f"- [{it.rel_path}]({md_prefix}{it.rel_path})")
            lines.append("")
        lines.append("---")
        lines.append("")
    return lines


outline_plugins_section = outline_families_section


def card_block_families(families: list[FamilyPackageEntry]) -> str:
    return card_block_plugins(families)


def card_block_plugins(families: list[FamilyPackageEntry]) -> str:
    parts: list[str] = []
    for fam in families:
        href = f"plugin/{quote(fam.id, safe='')}.html"
        counts = plugin_counts_line(fam)
        parts.append(
            f"""        <a class="cap-card" href="{html_mod.escape(href)}">
          <p class="cap-card__title"><span class="cap-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect width="24" height="24" rx="4" fill="#1a1a1e"/><path d="M4 6h16v12H4z" stroke="currentColor" stroke-width="1.5"/><path d="M4 10h16" stroke="currentColor" stroke-width="1.5"/></svg></span>{html_mod.escape(fam.label)}</p>
          <p class="cap-card__label">{html_mod.escape(fam.id)}/</p>
          <p class="cap-card__summary">{html_mod.escape(fam.summary)}</p>
          <p class="cap-card__meta">{html_mod.escape(counts)}</p>
          <p class="cap-card__more">Open plugin page →</p>
        </a>"""
        )
    return "\n".join(parts)


def _artifact_card(
    *,
    href: str,
    title: str,
    summary: str,
    meta: str,
    more: str,
) -> str:
    return f"""        <a class="cap-card" href="{html_mod.escape(href)}">
          <p class="cap-card__title">{html_mod.escape(title)}</p>
          <p class="cap-card__label">{html_mod.escape(meta)}</p>
          <p class="cap-card__summary">{html_mod.escape(summary or "Open for full text.")}</p>
          <p class="cap-card__more">{html_mod.escape(more)}</p>
        </a>"""


def html_family_slot_sections(
    fam: FamilyPackageEntry,
    *,
    href_to_repo: str,
    skill_href: Callable[[str], str],
    agent_href: Callable[[str], str],
    instruction_href: Callable[[str, str], str] | None = None,
    prompt_href: Callable[[str, str], str] | None = None,
    skill_summary: Callable[[str], str] | None = None,
    agent_summary: Callable[[str], str] | None = None,
) -> str:
    """HTML blocks listing each standard slot — card grids for primary artifact types."""
    return html_plugin_slot_sections(
        fam,
        href_to_repo=href_to_repo,
        skill_href=skill_href,
        agent_href=agent_href,
        instruction_href=instruction_href,
        prompt_href=prompt_href,
        skill_summary=skill_summary,
        agent_summary=agent_summary,
    )


def html_plugin_slot_sections(
    fam: FamilyPackageEntry,
    *,
    href_to_repo: str,
    skill_href: Callable[[str], str],
    agent_href: Callable[[str], str],
    instruction_href: Callable[[str, str], str] | None = None,
    prompt_href: Callable[[str, str], str] | None = None,
    skill_summary: Callable[[str], str] | None = None,
    agent_summary: Callable[[str], str] | None = None,
) -> str:
    sections: list[str] = []
    instruction_href = instruction_href or (lambda _f, slug: f"../instruction/{quote(slug, safe='')}.html")
    prompt_href = prompt_href or (lambda _f, slug: f"../prompt/{quote(slug, safe='')}.html")

    for slot in FAMILY_SLOT_ORDER:
        items = fam.slots.get(slot, [])
        label = FAMILY_SLOT_LABELS[slot]
        sections.append(
            f'<h3 id="slot-{html_mod.escape(slot)}">{html_mod.escape(label)}</h3>'
        )
        if slot in PLUGIN_SLOT_CAPTIONS:
            sections.append(
                f'<p class="entry-caption">{html_mod.escape(PLUGIN_SLOT_CAPTIONS[slot])}</p>'
            )
        if not items:
            sections.append(
                f'<p class="entry-caption">_(empty <code>{html_mod.escape(fam.id)}/{html_mod.escape(slot)}/</code>)_</p>'
            )
            continue

        if slot in PLUGIN_CARD_SLOTS:
            cards: list[str] = ['<div class="cap-grid cap-grid--plugin-slot">']
            for it in items:
                if slot == "skills":
                    detail = skill_href(it.name)
                    summary = (skill_summary(it.name) if skill_summary else "") or it.name
                    cards.append(
                        _artifact_card(
                            href=detail,
                            title=it.name,
                            summary=summary,
                            meta="Skill",
                            more="Open skill page →",
                        )
                    )
                elif slot == "agents":
                    detail = agent_href(it.name)
                    summary = (agent_summary(it.name) if agent_summary else "") or it.name
                    cards.append(
                        _artifact_card(
                            href=detail,
                            title=it.name,
                            summary=summary,
                            meta="Agent",
                            more="Open agent page →",
                        )
                    )
                elif slot == "instructions":
                    stem = artifact_stem(it.name, slot)
                    slug = artifact_slug(fam.id, slot, it.name)
                    detail = instruction_href(it.name, slug)
                    cards.append(
                        _artifact_card(
                            href=detail,
                            title=stem,
                            summary=it.summary or stem,
                            meta=it.name,
                            more="Open instruction page →",
                        )
                    )
                elif slot == "prompts":
                    stem = artifact_stem(it.name, slot)
                    slug = artifact_slug(fam.id, slot, it.name)
                    detail = prompt_href(it.name, slug)
                    cards.append(
                        _artifact_card(
                            href=detail,
                            title=stem,
                            summary=it.summary or stem,
                            meta=it.name,
                            more="Open prompt page →",
                        )
                    )
            cards.append("</div>")
            sections.append("\n".join(cards))
            continue

        rows: list[str] = ['<ul class="file-list file-list--root">']
        for it in items:
            rows.append(
                f'<li><a href="{html_mod.escape(href_to_repo + it.rel_path)}" target="_blank" rel="noopener noreferrer">{html_mod.escape(it.rel_path)}</a></li>'
            )
        rows.append("</ul>")
        sections.append("\n".join(rows))
    return "\n".join(sections)
