"""
rules — load rules/*.md + scanners.json; frontmatter helpers; phase stem resolution.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Frontmatter helpers
# ---------------------------------------------------------------------------

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


def read_rule_body(rules_dir: Path, stem: str) -> str:
    """Load ``rules/<stem>.md`` and return body (frontmatter stripped)."""
    p = rules_dir / f"{stem}.md"
    if not p.is_file():
        return ""
    return rule_body_text(p.read_text(encoding="utf-8"))


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


# ---------------------------------------------------------------------------
# RuleSet — unified rule set per skill
# ---------------------------------------------------------------------------

class RuleSet:
    """Loads rules/*.md and scanners.json for a skill."""

    def __init__(self, skill_path: Path):
        self.skill_path = Path(skill_path).resolve()
        self.markdown_paths: list[Path] = []
        self.scanner_rules: dict = {}
        self.merged_content: str = ""

    def load(self) -> "RuleSet":
        rules_dir = self.skill_path / "rules"
        parts: list[str] = []

        scanners_path = rules_dir / "scanners.json"
        if scanners_path.exists():
            self.scanner_rules = json.loads(scanners_path.read_text(encoding="utf-8"))

        for md in sorted(rules_dir.glob("*.md")):
            self.markdown_paths.append(md)
            parts.append(md.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")

        self.merged_content = "".join(parts).rstrip()
        return self
