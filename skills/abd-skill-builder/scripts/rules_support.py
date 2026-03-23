"""
Rule file helpers — YAML frontmatter strip + phase stem lists from ``skill-config.json``.

``Instructions`` uses this so ``rules/*.md`` may keep a short ``---`` / ``rule_id`` block while
phase attachment stays in **skill-config.json** (``phase_rules``, ``every_phase_rules``), not duplicated
per rule file.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def parse_rule_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter (subset). Returns ``(meta, body)``."""
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    fm = raw[3:end]
    body = raw[end + 4 :].lstrip("\n")
    meta: dict[str, Any] = {}
    for line in fm.splitlines():
        s = line.strip()
        if s.startswith("rule_id:"):
            meta["rule_id"] = s[8:].strip()
    return meta, body


def rule_body_text(raw: str) -> str:
    """Return markdown body with optional frontmatter removed."""
    _meta, body = parse_rule_frontmatter(raw)
    return body.strip()


def stems_for_phase_rules(skill_config: dict[str, Any], phase_slug: str) -> list[str]:
    """``every_phase_rules`` then ``phase_rules[slug]``, deduplicated in order."""
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


def read_rule_body(rules_dir: Path, stem: str) -> str:
    """Load ``rules/<stem>.md`` and return body (frontmatter stripped)."""
    p = rules_dir / f"{stem}.md"
    if not p.is_file():
        return ""
    return rule_body_text(p.read_text(encoding="utf-8"))
