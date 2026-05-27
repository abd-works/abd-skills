#!/usr/bin/env python3
"""Scanner: operations with two or more Invariant: lines must have an Interaction: block.

Multiple invariants signal that the operation performs real internal work. That work must
be made explicit via an Interaction: block showing the steps that satisfy the invariants.
A single invariant on a simple setter or guard is fine without an Interaction block.
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

# A non-indented member line: + or - at column 0
_MEMBER_RE = re.compile(r"^[+\-]\s+\S")
# Invariant annotation (tab-indented)
_INVARIANT_RE = re.compile(r"^\t\s*Invariant\s*:", re.IGNORECASE)
# Interaction annotation (tab-indented)
_INTERACTION_RE = re.compile(r"^\t\s*Interaction\s*:", re.IGNORECASE)
# Object Model section
_OM_SECTION_RE = re.compile(r"^### Object Model\s*$", re.MULTILINE)
# Class separator (5+ dashes on a line)
_SEPARATOR_RE = re.compile(r"^-{4,}\s*$")


def _find_object_model_sections(lines: List[str]) -> List[tuple[int, int]]:
    """Return (start_line, end_line) for each ### Object Model section."""
    sections = []
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^### Object Model\s*$", line):
            start = i
        elif start is not None and re.match(r"^#{2,3}\s", line) and not re.match(r"^### Object Model", line):
            sections.append((start, i))
            start = None
    if start is not None:
        sections.append((start, len(lines)))
    return sections


class InvariantsWithoutInteractionsScanner(Scanner):
    """Flag operations that have 2+ Invariant: lines but no Interaction: block."""

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
        om_sections = _find_object_model_sections(lines)

        for sec_start, sec_end in om_sections:
            violations.extend(
                self._scan_section(lines, sec_start, sec_end, file_path)
            )
        return violations

    def _scan_section(
        self,
        lines: List[str],
        sec_start: int,
        sec_end: int,
        file_path: Path,
    ) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        i = sec_start
        while i < sec_end:
            line = lines[i]
            if _MEMBER_RE.match(line) and "(" in line:
                # This is an operation (has parentheses)
                op_line_num = i + 1
                op_text = line.strip()
                # Collect annotation lines (tab-indented) that follow
                invariant_count = 0
                has_interaction = False
                j = i + 1
                while j < sec_end:
                    ann = lines[j]
                    if _INVARIANT_RE.match(ann):
                        invariant_count += 1
                    elif _INTERACTION_RE.match(ann):
                        has_interaction = True
                        # skip into interaction block
                        j += 1
                        while j < sec_end and lines[j].startswith("\t"):
                            j += 1
                        break
                    elif ann.strip() == "" or ann.startswith("\t"):
                        pass  # blank or indented continuation
                    else:
                        break  # next top-level member
                    j += 1
                if invariant_count >= 2 and not has_interaction:
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=(
                            f"Operation '{op_text}' has {invariant_count} Invariant: lines "
                            f"but no Interaction: block — add an Interaction: block to show "
                            f"how the invariants are satisfied"
                        ),
                        location=str(file_path),
                        line_number=op_line_num,
                        severity="error",
                    ).to_dict())
            i += 1
        return violations


from object_model_context import build_object_model_context as _build_context  # noqa: E402


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            InvariantsWithoutInteractionsScanner,
            rule_md_name="invariants-without-interactions",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
