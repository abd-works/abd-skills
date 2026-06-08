#!/usr/bin/env python3
"""Scanner: CRC responsibility lines must use plain English — no typed signatures.

Responsibility names and collaborator names in a domain model table must be written in plain
domain language. Lines that contain code-style notation (typed parameters, return types,
or arrow notation) violate this rule. Checked patterns:
  - word(param: Type)  → typed parameters
  - ) -> Type           → return type with arrow
  - ): Type             → return type with colon
  - DifficultyClass 1..1  → cardinality in collaborator column
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

# CRC table rows use | as a separator. The format is:
#   responsibility name   | CollaboratorType
#                         |   invariant: ...
# We check the responsibility column (before |) for code-style notation.
_CRC_ROW_RE = re.compile(r"^(.+?)\s*\|\s*(.*)$")

# Code-style patterns in a responsibility name (before the pipe):
_TYPED_PARAMS_RE = re.compile(r"\w+\s*\(\s*\w+\s*:\s*\w+")  # word(param: Type
_RETURN_ARROW_RE = re.compile(r"\)\s*->\s*\w+")              # ) -> Type
_RETURN_COLON_RE = re.compile(r"\)\s*:\s*\w+")               # ): Type
_CARDINALITY_RE = re.compile(r"\b\d\.\.[*\d]\b")             # 1..1, 0..*, 1..*

# CRC section header
_CRC_SECTION_RE = re.compile(r"^### Class Responsibility Collaborator\s*$", re.IGNORECASE)
# Section end markers
_NEXT_SECTION_RE = re.compile(r"^#{2,3}\s", re.MULTILINE)


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


class EnglishOnlyNoSignaturesScanner(Scanner):
    """Flag CRC table rows containing typed signatures or cardinality notation."""

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

        crc_set: set[int] = set()
        for s, e in crc_sections:
            crc_set.update(range(s, e))

        for i, line in enumerate(lines):
            if i not in crc_set:
                continue
            m = _CRC_ROW_RE.match(line)
            if not m:
                continue
            responsibility = m.group(1).strip()
            if not responsibility or responsibility.startswith("#") or responsibility.startswith("*"):
                continue

            bad_patterns = []
            if _TYPED_PARAMS_RE.search(responsibility):
                bad_patterns.append("typed parameter (word(param: Type))")
            if _RETURN_ARROW_RE.search(responsibility):
                bad_patterns.append("return type arrow () -> Type)")
            if _RETURN_COLON_RE.search(responsibility):
                bad_patterns.append("return type colon ((): Type)")
            if _CARDINALITY_RE.search(responsibility):
                bad_patterns.append("cardinality notation (1..1 / 0..*)")

            if bad_patterns:
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"CRC row '{responsibility[:60]}' contains code-style notation: "
                        + ", ".join(bad_patterns)
                        + " — use plain English prose"
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
                if "state: domain-model" in text[:300]:
                    files.append(md)
            if files:
                break
    return ScanFilesContext(files=FileCollection(code_files=files))


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            EnglishOnlyNoSignaturesScanner,
            rule_md_name="english-only-no-signatures",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
