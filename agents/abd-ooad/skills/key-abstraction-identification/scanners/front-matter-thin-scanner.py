#!/usr/bin/env python3
"""Scanner: front matter must be thin — only source pointer(s) and counts."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).resolve().parent.parent
_SKILLS = _ROOT.parent
for _p in (
    _SKILLS / "execute_using_rules" / "scripts",
    _ROOT / "scanners",
):
    s = str(_p)
    if s not in sys.path:
        sys.path.insert(0, s)

from scanner_runner import execute_scan_with_workspace  # noqa: E402
from markdown_artifact_scanner import (  # noqa: E402
    MarkdownArtifactScanner,
    ParsedArtifact,
    build_ka_context,
)

_ALLOWED_PATTERNS = [
    re.compile(r"^#\s+"),                          # H1 title
    re.compile(r"^Source:\s+"),                     # Source pointer
    re.compile(r"^Modules:\s+"),                    # Module count
    re.compile(r"^Key Abstractions:\s+"),           # KA count
    re.compile(r"^Settled Key Abstractions:\s+"),   # After settlement
    re.compile(r"^---\s*$"),                        # Horizontal rule
    re.compile(r"^\s*$"),                           # Blank line
    re.compile(r"^<!--"),                           # Comment
]

_SUSPICIOUS_PATTERNS = [
    re.compile(r"^-\s+\*?\*?[\w\s]+\*?\*?\s*:", re.IGNORECASE),  # Bullet list with label
    re.compile(r"^Intent:", re.IGNORECASE),
    re.compile(r"^Core terms", re.IGNORECASE),
    re.compile(r"^Shape hint:", re.IGNORECASE),
    re.compile(r"^Tension:", re.IGNORECASE),
]

MAX_FRONT_MATTER_LINES = 12


class FrontMatterThinScanner(MarkdownArtifactScanner):

    def check_artifact(self, parsed: ParsedArtifact) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        location = str(parsed.file_path or "key-abstractions.md")
        fm = parsed.front_matter.strip()

        if not fm:
            return violations

        lines = fm.splitlines()
        content_lines = [l for l in lines if l.strip() and not l.strip().startswith("<!--")]

        if len(content_lines) > MAX_FRONT_MATTER_LINES:
            violations.append(self._violation(
                f"Front matter has {len(content_lines)} content lines "
                f"(max {MAX_FRONT_MATTER_LINES}). "
                f"Keep it to source pointer(s) and counts only.",
                location, severity="warning",
            ))

        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            if any(p.match(stripped) for p in _ALLOWED_PATTERNS):
                continue
            if any(p.match(stripped) for p in _SUSPICIOUS_PATTERNS):
                violations.append(self._violation(
                    f"Front matter line {i}: abstraction-level content found in front matter: "
                    f'"{stripped[:80]}". Move this under the appropriate heading.',
                    location, i,
                ))

        return violations


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            FrontMatterThinScanner,
            rule_md_name="front-matter-thin",
            build_context=build_ka_context,
            skill_root=_ROOT,
        )
    )
