#!/usr/bin/env python3
"""Scanner: module file must contain a ## Domain logic section with at least one bullet.

After domain-sketch enrichment, the file must have a '## Domain logic' section
containing at least one prose bullet (line starting with '- '). The section without
any bullet content is as bad as missing the section entirely.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).resolve().parent.parent
_REPO = _ROOT.parent.parent.parent.parent
for _p in (
    _REPO / "skills" / "execute-skill-using-skills-rules" / "scripts",
    _ROOT / "scanners",
):
    s = str(_p)
    if s not in sys.path:
        sys.path.insert(0, s)

from scanner_runner import execute_scan_with_workspace  # noqa: E402
from scanner_bases import Scanner, Violation  # noqa: E402
from scanner_bases.resources.scan_context import (  # noqa: E402
    FileCollection,
    ScanFilesContext,
)

_DOMAIN_LOGIC_RE = re.compile(r"^## Domain logic\s*$", re.IGNORECASE | re.MULTILINE)
_NEXT_H2_RE = re.compile(r"^## ", re.MULTILINE)
_BULLET_RE = re.compile(r"^\s*-\s+\S")


class DomainLogicSectionPresentScanner(Scanner):
    """Flag files missing a ## Domain logic section or where the section has no bullet content."""

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        for fp in context.files.all_files:
            if fp and fp.is_file():
                violations.extend(self._scan_file(fp))
        return violations

    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        content = file_path.read_text(encoding="utf-8")
        m = _DOMAIN_LOGIC_RE.search(content)
        if not m:
            return [Violation(
                rule=self.rule,
                violation_message=(
                    "No '## Domain logic' section found — "
                    "add a Domain logic section with testable behavior bullets"
                ),
                location=str(file_path),
                line_number=1,
                severity="error",
            ).to_dict()]

        # Find the body of the section (until the next ## heading)
        section_start = m.end()
        next_h2 = _NEXT_H2_RE.search(content, section_start)
        section_body = content[section_start:next_h2.start() if next_h2 else len(content)]

        if not _BULLET_RE.search(section_body):
            line_num = content[:m.start()].count("\n") + 1
            return [Violation(
                rule=self.rule,
                violation_message=(
                    "'## Domain logic' section exists but contains no bullet points — "
                    "add at least one testable behavior observation"
                ),
                location=str(file_path),
                line_number=line_num,
                severity="error",
            ).to_dict()]
        return []


def _build_context(workspace: Path) -> ScanFilesContext:
    files: List[Path] = []
    for search_path in (
        workspace / "abd-domain-driven-design" / "modules",
        workspace / "modules",
    ):
        if search_path.is_dir():
            for md in sorted(search_path.glob("*.md")):
                text = md.read_text(encoding="utf-8")
                if "state: domain-sketch" in text[:300]:
                    files.append(md)
            if files:
                break
    return ScanFilesContext(files=FileCollection(code_files=files))


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            DomainLogicSectionPresentScanner,
            rule_md_name="domain-logic-section-present",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
