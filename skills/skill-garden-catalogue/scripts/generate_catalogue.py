#!/usr/bin/env python3
"""Scan a skills folder and generate a Markdown inventory + HTML catalogue."""

from __future__ import annotations

import argparse
import html as html_mod
import os
import re
import sys
import textwrap
from pathlib import Path
from typing import NamedTuple

_EXECUTE_RULES_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "execute-skill-using-skills-rules" / "scripts"
if str(_EXECUTE_RULES_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_EXECUTE_RULES_SCRIPTS))
import frontmatter_tags  # noqa: E402

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_ROOT / "templates"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
YAML_FIELD_RE = re.compile(r"^(\w[\w-]*):\s*(.+)", re.MULTILINE)
YAML_BLOCK_RE = re.compile(
    r"^(\w[\w-]*):\s*>-?\s*\n((?:[ \t]+.*\n?)+)", re.MULTILINE
)


class SkillEntry(NamedTuple):
    name: str
    dir_name: str
    challenge: str
    solution: str


# ---------------------------------------------------------------------------
# Lightweight YAML-ish frontmatter parser (avoids PyYAML dependency)
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
    text = re.sub(r"`[^`]+`", "", text)
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


def _first_meaningful_line(text: str) -> str:
    text = _strip_md(text)
    for line in text.splitlines():
        line = line.strip().lstrip("- ").strip()
        if len(line) < 15:
            continue
        if PREAMBLE_RE.match(line):
            continue
        sent = re.split(r"(?<=[.!?])\s", line, maxsplit=1)[0]
        return _truncate(sent)
    return _truncate(text.strip())


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
        clean = _strip_md(one)
        return _truncate(clean, 250)
    desc = fm.get("description", "")
    if desc:
        clean = _strip_md(desc)
        return _truncate(clean, 250)
    section = _extract_section(body, "Purpose")
    if section:
        return _first_meaningful_line(section)
    return "See SKILL.md for details."


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_skills(skills_dir: Path) -> list[SkillEntry]:
    entries: list[SkillEntry] = []
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
        challenge = _derive_challenge(body)
        solution = _derive_solution(fm, body)
        entries.append(SkillEntry(name=name, dir_name=child.name,
                                  challenge=challenge, solution=solution))
    return entries


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def generate_markdown(entries: list[SkillEntry]) -> str:
    lines = [
        "# Skill Garden — Inventory",
        "",
        f"> Auto-generated catalogue of **{len(entries)}** deployed skills.",
        "> Re-run `generate_catalogue.py` to refresh.",
        "",
        "| Skill | Challenge | Solution |",
        "| --- | --- | --- |",
    ]
    for e in entries:
        link = f"[{e.name}]({e.dir_name}/)"
        challenge = e.challenge.replace("|", "\\|")
        solution = e.solution.replace("|", "\\|")
        lines.append(f"| {link} | {challenge} | {solution} |")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

def _h(text: str) -> str:
    return html_mod.escape(text)


def generate_html(entries: list[SkillEntry]) -> str:
    cards: list[str] = []
    for e in entries:
        cards.append(textwrap.dedent(f"""\
  <a class="cap-card" href="../{_h(e.dir_name)}/">
    <p class="cap-card__title">
      <span class="cap-card__icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect width="24" height="24" rx="4" fill="#1a1a1e"/><path d="M7 8h10M7 12h7M7 16h10" stroke="#ff7a00" stroke-width="1.5" stroke-linecap="round"/></svg></span>
      {_h(e.name)}
    </p>
    <div class="cap-card__row">
      <div>
        <p class="cap-card__label">Challenge</p>
        <p class="cap-card__problem">{_h(e.challenge)}</p>
      </div>
      <hr class="cap-card__sep">
      <div>
        <p class="cap-card__label">Solution</p>
        <p class="cap-card__solution">{_h(e.solution)}</p>
      </div>
    </div>
    <p class="cap-card__more">Open skill →</p>
  </a>
"""))

    card_block = "\n".join(cards)
    template_path = TEMPLATE_DIR / "catalog-index.html"
    if template_path.exists():
        template = template_path.read_text(encoding="utf-8")
    else:
        template = _default_html_template()

    return (
        template
        .replace("{{SKILL_COUNT}}", str(len(entries)))
        .replace("{{SKILL_CARDS}}", card_block)
    )


def _default_html_template() -> str:
    """Minimal fallback if the template file is missing."""
    return textwrap.dedent("""\
        <!DOCTYPE html><html><head><meta charset="utf-8">
        <title>Skill Catalogue</title></head><body>
        <h1>Skill Catalogue ({{SKILL_COUNT}} skills)</h1>
        {{SKILL_CARDS}}
        </body></html>""")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate skill catalogue.")
    parser.add_argument(
        "--skills-dir", type=Path, required=True,
        help="Folder containing skill subdirectories (each with SKILL.md).",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=None,
        help="Where to write outputs. Defaults to --skills-dir.",
    )
    args = parser.parse_args()

    skills_dir: Path = args.skills_dir.resolve()
    output_dir: Path = (args.output_dir or skills_dir).resolve()

    if not skills_dir.is_dir():
        raise SystemExit(f"Skills directory not found: {skills_dir}")

    entries = discover_skills(skills_dir)
    if not entries:
        raise SystemExit(f"No SKILL.md files found under {skills_dir}")

    md_path = output_dir / "skill-inventory.md"
    md_path.write_text(generate_markdown(entries), encoding="utf-8")
    print(f"  wrote {md_path}  ({len(entries)} skills)")

    catalog_dir = output_dir / "catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)
    html_path = catalog_dir / "index.html"
    html_path.write_text(generate_html(entries), encoding="utf-8")
    print(f"  wrote {html_path}")


if __name__ == "__main__":
    main()
