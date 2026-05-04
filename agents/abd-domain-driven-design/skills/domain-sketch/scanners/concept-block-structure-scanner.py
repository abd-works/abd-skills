#!/usr/bin/env python3
"""Scanner: every ### Concept block must have a ---- behavior separator and a Decisions section.

Each domain-sketch concept block (and subtype block) must follow the prescribed structure:
  - intent paragraph
  - ---- separator before behaviors
  - ----- separator before collaborations (one dash longer)
  - #### Decisions made section

This scanner checks that:
1. Every #### concept heading inside a Domain Sketch section has at least one ---- separator
2. Every #### concept heading has a '#### Decisions made' subsection

Subtype blocks (### X *is a type of* Y) follow the same structural rules.
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

# Domain Sketch section
_DOMAIN_SKETCH_SECTION_RE = re.compile(r"^### Domain Sketch\s*$", re.IGNORECASE)
# Concept heading: #### **ConceptName** or ### ConceptName *is a type of* Base
_CONCEPT_H4_RE = re.compile(r"^#### \*\*[^*]+\*\*\s*$")
_SUBTYPE_H3_RE = re.compile(r"^### .+\*is a type of\*", re.IGNORECASE)
# Any #### heading (subheadings within a concept block)
_H4_RE = re.compile(r"^#### ")
# Behavior separator (4+ dashes, not part of a longer sequence)
_BEHAVIOR_SEP_RE = re.compile(r"^-{4,}\s*$")
# Decisions made section
_DECISIONS_RE = re.compile(r"^#### Decisions made\s*$", re.IGNORECASE)
# Core terms section
_CORE_TERMS_RE = re.compile(r"^#### Core terms\s*$", re.IGNORECASE)


def _find_domain_sketch_sections(lines: List[str]) -> List[tuple[int, int]]:
    sections = []
    start = None
    for i, line in enumerate(lines):
        if _DOMAIN_SKETCH_SECTION_RE.match(line):
            start = i
        elif start is not None and re.match(r"^#{2,3}\s", line) and not _DOMAIN_SKETCH_SECTION_RE.match(line):
            sections.append((start, i))
            start = None
    if start is not None:
        sections.append((start, len(lines)))
    return sections


def _extract_concept_blocks(
    lines: List[str], sec_start: int, sec_end: int
) -> List[tuple[str, int, int]]:
    """Return (heading, start_line, end_line) for each concept block."""
    blocks = []
    current = None
    current_start = None
    for i in range(sec_start, sec_end):
        line = lines[i]
        is_concept = _CONCEPT_H4_RE.match(line) or _SUBTYPE_H3_RE.match(line)
        if is_concept:
            if current is not None:
                blocks.append((current, current_start, i))
            current = line.strip()
            current_start = i
    if current is not None:
        blocks.append((current, current_start, sec_end))
    return blocks


class ConceptBlockStructureScanner(Scanner):
    """Flag concept blocks missing the ---- separator or the Decisions made subsection."""

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
        sketch_sections = _find_domain_sketch_sections(lines)

        for sec_start, sec_end in sketch_sections:
            concept_blocks = _extract_concept_blocks(lines, sec_start, sec_end)
            for heading, blk_start, blk_end in concept_blocks:
                block_lines = lines[blk_start:blk_end]

                # Count non-empty, non-heading content lines to know if block has real content
                content_lines = [
                    bl for bl in block_lines[1:]
                    if bl.strip() and not re.match(r"^#+\s", bl)
                ]
                if not content_lines:
                    continue  # skip empty/stub blocks

                has_separator = any(_BEHAVIOR_SEP_RE.match(bl) for bl in block_lines)
                has_decisions = any(_DECISIONS_RE.match(bl) for bl in block_lines)

                if not has_separator:
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=(
                            f"Concept block '{heading}' has no ---- behavior separator — "
                            f"add '----' before the behavior bullets and '-----' before collaborations"
                        ),
                        location=str(file_path),
                        line_number=blk_start + 1,
                        severity="error",
                    ).to_dict())

                if not has_decisions:
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=(
                            f"Concept block '{heading}' has no '#### Decisions made' section — "
                            f"document the modeling choices that shaped this concept"
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
                if "state: domain-sketch" in text[:300]:
                    files.append(md)
            if files:
                break
    return ScanFilesContext(files=FileCollection(code_files=files))


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            ConceptBlockStructureScanner,
            rule_md_name="concept-block-structure",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
