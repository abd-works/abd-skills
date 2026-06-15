#!/usr/bin/env python3
"""Scanner: slash terms (A / B) must be resolved before CRC — none may appear in headings.

Any concept named A / B in the Ubiquitous Language must be resolved to one canonical name before
writing CRC blocks. This scanner finds #### **A / B** heading lines anywhere in the
module file and flags them as unresolved slash terms.

Also checks: collaborator column entries that use slash notation (e.g. "Check / Graded Check")
inside CRC table rows.
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

# Heading with slash: #### **A / B** or #### **A/B**
_SLASH_HEADING_RE = re.compile(r"^#{2,6}\s+\*\*[^*]+\s*/\s*[^*]+\*\*")
# CRC row with slash in collaborator column
_CRC_ROW_RE = re.compile(r"^(.+?)\s*\|\s*(.+)$")
_SLASH_IN_COLLABORATOR_RE = re.compile(r"\b\w[\w\s]+\s*/\s*\w[\w\s]+")

# CRC section header
_CRC_SECTION_RE = re.compile(r"^### Class Responsibility Collaborator\s*$", re.IGNORECASE)


def _find_crc_sections(lines: List[str]) -> List[tuple[int, int]]:
    sections = []
    start = None
    for i, line in enumerate(lines):
        if _CRC_SECTION_RE.match(line):
            start = i
        elif start is not None and re.match(r"^#{2,3}\s", line) and not _CRC_SECTION_RE.match(line):
            sections.append((start, i))
            start = None
    if start is not None:
        sections.append((start, len(lines)))
    return sections


class SlashTermsResolvedScanner(Scanner):
    """Flag A/B slash notation in headings and CRC collaborator columns."""

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        for fp in context.files.all_files:
            if fp and fp.is_file():
                violations.extend(self._scan_file(fp))
        return violations

    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        crc_sections = _find_crc_sections(lines)
        crc_set: set[int] = set()
        for s, e in crc_sections:
            crc_set.update(range(s, e))

        for i, line in enumerate(lines):
            # Check headings anywhere in the file
            if _SLASH_HEADING_RE.match(line):
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"Heading '{line.strip()}' uses slash notation — "
                        f"resolve to one canonical name before CRC"
                    ),
                    location=str(file_path),
                    line_number=i + 1,
                    severity="error",
                ).to_dict())
                continue

            # Check collaborator columns in CRC sections
            if i in crc_set:
                m = _CRC_ROW_RE.match(line)
                if m:
                    collaborators = m.group(2).strip()
                    # Skip invariant lines
                    if collaborators.lower().startswith("invariant"):
                        continue
                    if _SLASH_IN_COLLABORATOR_RE.search(collaborators):
                        violations.append(Violation(
                            rule=self.rule,
                            violation_message=(
                                f"CRC collaborator column contains slash notation "
                                f"'{collaborators[:60]}' — use one canonical name"
                            ),
                            location=str(file_path),
                            line_number=i + 1,
                            severity="error",
                        ).to_dict())
        return violations


def _build_context(workspace: Path) -> ScanFilesContext:
    files: List[Path] = []
    for search_path in (
        workspace / "abd-domain-driven-design" / "modules",
        workspace / "modules",
    ):
        if search_path.is_dir():
            for md in sorted(search_path.glob("*.md")):
                text = md.read_text(encoding="utf-8")
                if "state: crc" in text[:300]:
                    files.append(md)
            if files:
                break
    return ScanFilesContext(files=FileCollection(code_files=files))


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            SlashTermsResolvedScanner,
            rule_md_name="slash-terms-resolved-before-crc",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
