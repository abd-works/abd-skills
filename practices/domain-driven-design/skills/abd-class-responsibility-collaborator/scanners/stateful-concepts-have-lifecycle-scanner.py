#!/usr/bin/env python3
"""Scanner: every CRC concept block must have a lifecycle: field.

After CRC enrichment, every #### **ConceptName** block must contain either a populated
lifecycle: block (with states, transitions, etc.) or the explicit marker 'lifecycle: (stateless)'.
Blocks that end after collaborators: with no lifecycle: field at all are a violation.

The lifecycle: field signals that lifecycle coverage was considered — not that the concept
is always stateful.
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

# CRC section header
_CRC_SECTION_RE = re.compile(r"^### Class Responsibility Collaborator\s*$", re.IGNORECASE)
# Concept block heading in CRC: #### **ConceptName** or #### **Sub : Base**
_CONCEPT_HEADING_RE = re.compile(r"^#### \*\*[^*]+\*\*\s*$")
# lifecycle: field (any form)
_LIFECYCLE_RE = re.compile(r"^\s*lifecycle\s*:", re.IGNORECASE)
# Collaborators field (marks that we're past the responsibility table into the metadata block)
_COLLABORATORS_RE = re.compile(r"^\s*collaborators\s*:", re.IGNORECASE)
# Alternately, CRC table rows use | — detect the end of a concept's entries
_TABLE_ROW_RE = re.compile(r"^.+\s*\|")


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


def _extract_concept_blocks(
    lines: List[str], crc_start: int, crc_end: int
) -> List[tuple[str, int, int]]:
    """Return list of (heading_text, start_line, end_line) for concept blocks in this CRC section."""
    blocks = []
    current_name = None
    current_start = None
    for i in range(crc_start, crc_end):
        line = lines[i]
        if _CONCEPT_HEADING_RE.match(line):
            if current_name is not None:
                blocks.append((current_name, current_start, i))
            current_name = line.strip()
            current_start = i
    if current_name is not None:
        blocks.append((current_name, current_start, crc_end))
    return blocks


class StatefulConceptsHaveLifecycleScanner(Scanner):
    """Flag CRC concept blocks that are missing the lifecycle: field entirely."""

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
        if not crc_sections:
            return violations

        for crc_start, crc_end in crc_sections:
            concept_blocks = _extract_concept_blocks(lines, crc_start, crc_end)
            for heading, blk_start, blk_end in concept_blocks:
                block_lines = lines[blk_start:blk_end]
                has_lifecycle = any(_LIFECYCLE_RE.match(bl) for bl in block_lines)
                # Only flag if the block has some content (table rows or collaborators)
                has_content = any(
                    _TABLE_ROW_RE.match(bl) or _COLLABORATORS_RE.match(bl)
                    for bl in block_lines
                )
                if has_content and not has_lifecycle:
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=(
                            f"CRC block '{heading}' has no lifecycle: field — "
                            f"add 'lifecycle: (stateless)' or a populated lifecycle block"
                        ),
                        location=str(file_path),
                        line_number=blk_start + 1,
                        severity="warning",
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
            StatefulConceptsHaveLifecycleScanner,
            rule_md_name="stateful-concepts-have-lifecycle",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
