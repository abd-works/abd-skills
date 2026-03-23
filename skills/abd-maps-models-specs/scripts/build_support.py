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


def stems_for_phase_rules(skill_config: dict[str, Any], phase_slug: str) -> list[str]:
    """Ordered rule stems (basename without ``.md``) for a phase: ``every_phase_rules`` then ``phase_rules[slug]``."""
    every: list[str] = list(skill_config.get("every_phase_rules") or [])
    per: list[str] = list((skill_config.get("phase_rules") or {}).get(phase_slug, []))
    seen: set[str] = set()
    out: list[str] = []
    for s in every + per:
        stem = str(s).strip()
        if not stem or stem in seen:
            continue
        seen.add(stem)
        out.append(stem)
    return out


def configured_rule_stems(skill_config: dict[str, Any]) -> set[str]:
    """All stems referenced by ``every_phase_rules`` and ``phase_rules``."""
    stems: set[str] = set(skill_config.get("every_phase_rules") or [])
    for slist in (skill_config.get("phase_rules") or {}).values():
        for s in slist or []:
            if str(s).strip():
                stems.add(str(s).strip())
    return stems


def warn_orphan_rule_files(rules_dir: Path, skill_config: dict[str, Any]) -> None:
    """Print a warning for each ``rules/*.md`` (except README) whose stem is not listed in skill-config rule lists."""
    if not rules_dir.is_dir():
        return
    configured = configured_rule_stems(skill_config)
    for rp in sorted(rules_dir.glob("*.md")):
        if rp.name.lower() == "readme.md":
            continue
        stem = rp.stem
        if stem not in configured:
            print(
                f"Warning: rules/{rp.name} is not listed in every_phase_rules or any phase_rules entry "
                f"in skill-config.json — it will never be inlined into a phase bundle.",
                flush=True,
            )


def warn_unknown_phase_rule_keys(skill_config: dict[str, Any]) -> None:
    """Print a warning if ``phase_rules`` contains keys not present in ``phase_files``."""
    phases = set(skill_config.get("phase_files") or [])
    pr_keys = set(skill_config.get("phase_rules") or {})
    extra = pr_keys - phases
    if extra:
        print(
            f"Warning: phase_rules has keys not in phase_files: {sorted(extra)}",
            flush=True,
        )


def load_rules_by_stems(rules_dir: Path, stems: list[str]) -> list[tuple[str, str]]:
    """Load ``rules/<stem>.md`` in order; return ``(filename, body)`` with YAML frontmatter stripped from body."""
    out: list[tuple[str, str]] = []
    if not rules_dir.is_dir():
        return out
    for stem in stems:
        rp = rules_dir / f"{stem}.md"
        if not rp.is_file():
            print(f"Warning: phase_rules references missing rules/{stem}.md — skipped.", flush=True)
            continue
        raw = rp.read_text(encoding="utf-8")
        _meta, body = parse_rule_frontmatter(raw)
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
    # process.md lives under content/parts/ — ``../built/`` works there; AGENTS.md lives at skill root.
    md = md.replace("](../built/", "](content/built/")
    # process.md lives under content/parts/ — links to ../../scripts/ must work from skill root in AGENTS.md
    md = md.replace("](../../scripts/", "](scripts/")
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
    """Rewrite links for per-phase bundles under ``content/built/phases/`` (relative to that folder)."""
    md = rewrite_links_for_agents_md(md, phase_files)
    # From ``content/built/phases/<slug>.md``: ``../..`` = ``content/``; targets live under ``content/parts/``.
    md = md.replace("](content/parts/library/", "](../../parts/library/")
    md = md.replace("](content/parts/phases/", "](../../parts/phases/")
    md = md.replace("](content/parts/", "](../../parts/")
    md = md.replace("](../content/parts/", "](../../../content/parts/")
    md = md.replace("](../phases/", "](../../parts/phases/")
    md = md.replace("](../library/", "](../../parts/library/")
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
