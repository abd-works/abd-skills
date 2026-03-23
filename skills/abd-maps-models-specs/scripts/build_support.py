"""
Shared markdown utilities for abd-maps-models-specs build (rules, links, headings).
Used by maps_instructions.py and maps_assembler.py.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def slug_to_phase_fname(slug: str) -> str:
    """Phase markdown basename under `content/parts/phases/`. Slugs come from `skill-config.json` → `phase_files`."""
    return slug if slug.endswith(".md") else f"{slug}.md"


def phase_fnames_from_skill_config(skill_config: dict[str, Any]) -> list[str]:
    """Ordered phase filenames (`*.md`) matching `skill-config.json` → `phase_files`."""
    return [slug_to_phase_fname(s) for s in skill_config.get("phase_files", [])]


def parse_rule_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter (subset: rule_id, every_phase, phase_files list). Returns (meta, body)."""
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    fm = raw[3:end]
    body = raw[end + 4 :].lstrip("\n")
    meta: dict[str, Any] = {}
    phase_files: list[str] = []
    in_phase_list = False
    for line in fm.splitlines():
        s = line.strip()
        if s.startswith("rule_id:"):
            in_phase_list = False
            meta["rule_id"] = s[8:].strip()
        elif s.startswith("every_phase:"):
            in_phase_list = False
            meta["every_phase"] = s[12:].strip().lower() in ("true", "yes", "1")
        elif s.startswith("phase_files:"):
            rest = line.split(":", 1)[1].strip()
            if rest:
                for part in rest.split(","):
                    p = part.strip()
                    if p:
                        phase_files.append(p)
                in_phase_list = False
            else:
                in_phase_list = True
        elif in_phase_list and s.startswith("- "):
            phase_files.append(s[2:].strip())
    if phase_files:
        meta["phase_files"] = phase_files
    return meta, body


def rule_applies_to_phase(meta: dict[str, Any], phase_fname: str) -> bool:
    if meta.get("every_phase"):
        return True
    phases = meta.get("phase_files") or []
    return phase_fname in phases


def load_rule_files_for_phase(rules_dir: Path, phase_fname: str) -> list[tuple[str, str]]:
    """Rule filename + body (frontmatter stripped) for this phase bundle only."""
    out: list[tuple[str, str]] = []
    if not rules_dir.is_dir():
        return out
    for rp in sorted(rules_dir.glob("*.md")):
        if rp.name.lower() == "readme.md":
            continue
        raw = rp.read_text(encoding="utf-8")
        meta, body = parse_rule_frontmatter(raw)
        if not rule_applies_to_phase(meta, phase_fname):
            continue
        if not meta.get("phase_files") and not meta.get("every_phase"):
            print(
                f"Warning: rules/{rp.name} has no phase_files / every_phase — skipped. "
                "Set YAML frontmatter (see rules/README.md).",
                flush=True,
            )
            continue
        body = body.strip() + "\n"
        if not body.strip():
            continue
        out.append((rp.name, body))
    return out


def demote_all_headings(md: str, extra_levels: int = 2) -> str:
    """Prefix each markdown heading line with extra # so inlined docs nest under section headers."""
    prefix = "#" * extra_levels
    lines: list[str] = []
    for line in md.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            idx = len(line) - len(stripped)
            lines.append(line[:idx] + prefix + stripped)
        else:
            lines.append(line)
    return "".join(lines)


def rewrite_links_for_agents_md(md: str, phase_files: list[str]) -> str:
    """Paths relative to skill root (AGENTS.md and agents-staged.md location)."""
    md = md.replace("](../content/parts/library/", "](content/parts/library/")
    md = md.replace("../../../docs/", "docs/")
    md = md.replace("../../docs/", "docs/")
    md = md.replace("](../process.md)", "](content/parts/process.md)")
    md = md.replace("](solution-analyst-role.md)", "](content/parts/solution-analyst-role.md)")
    md = md.replace("](../solution-analyst-role.md)", "](content/parts/solution-analyst-role.md)")
    md = md.replace("](solution-role.md)", "](content/parts/solution-analyst-role.md)")
    md = md.replace("](../solution-role.md)", "](content/parts/solution-analyst-role.md)")
    md = md.replace("](operator-role.md)", "](content/parts/solution-analyst-role.md)")
    md = md.replace("](../operator-role.md)", "](content/parts/solution-analyst-role.md)")
    md = md.replace("](phases/", "](content/parts/phases/")
    # Phase files use ../library/ relative to phases/ — resolve to skill-root path for AGENTS.md.
    md = md.replace("](../library/", "](content/parts/library/")
    for fname in phase_files:
        md = md.replace(f"]({fname})", f"](content/parts/phases/{fname})")
    return md


def rewrite_links_for_phase_bundle(md: str, phase_files: list[str]) -> str:
    """Links in bundle files live under content/built/phases/ or parts/phases/built/ — adjust skill-root paths."""
    md = rewrite_links_for_agents_md(md, phase_files)
    # ``../content/parts/library/`` in rules → ``content/parts/library/`` in agents_md; then:
    # Must run before blanket ``content/parts/`` → ``../../parts/`` (library lives under ``parts/library/``).
    md = md.replace("](content/parts/library/", "](../../library/")
    md = md.replace("](content/parts/", "](../../parts/")
    md = md.replace("](../content/parts/", "](../../parts/")
    md = md.replace("](docs/", "](../../../docs/")
    return md


def demote_first_h1_to_h2(md: str) -> str:
    """Demote the first # heading to ## so content nests under # AGENTS — …"""
    lines = md.splitlines(keepends=True)
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            indent = line[: len(line) - len(stripped)]
            lines[i] = indent + "## " + stripped[2:]
            break
    return "".join(lines)


def strip_solution_role_block_for_agents(text: str) -> str:
    """Remove role preamble (markers + body) when merging phase sources into AGENTS.md / agents-staged."""
    for pat in (
        r"<!-- solution-analyst-role:start -->.*?<!-- solution-analyst-role:end -->\s*",
        r"<!-- solution-role:start -->.*?<!-- solution-role:end -->\s*",
        r"<!-- operator-role:start -->.*?<!-- operator-role:end -->\s*",
    ):
        text = re.sub(pat, "", text, flags=re.DOTALL)
    return text


# Backward compatibility for imports
strip_operator_block_for_agents = strip_solution_role_block_for_agents
