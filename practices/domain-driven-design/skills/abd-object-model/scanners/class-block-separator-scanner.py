#!/usr/bin/env python3
"""Scanner: every class block in Object Model sections must have a ------ separator.

The six-dash separator (------) divides the constructor/initialisation block from the
properties block. Its absence signals that properties and constructors are merged without
the required structural boundary.

Classes that have only an Initialisation: note (no explicit constructor) are exempt
from requiring the separator on the constructor side, but they must still have the
------  line before their properties.
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

# Class block header inside Object Model: #### **ClassName** or #### **ClassName : Parent**
_CLASS_HEADER_RE = re.compile(r"^#### \*\*[^*]+\*\*", re.IGNORECASE)
# Constructor/property separator: 6 or more dashes (exactly this usage in object-model)
_CTOR_SEPARATOR_RE = re.compile(r"^-{6,}\s*$")
# Block-level separator (5 dashes): marks end of a class block
_BLOCK_SEPARATOR_RE = re.compile(r"^-{5}\s*$")
# Property line: + name: Type (has colon after name)
_PROPERTY_LINE_RE = re.compile(r"^[+\-]\s+(?:<<[^>]+>>\s*)?\S+\s*:")
# Object Model section
_OM_SECTION_RE = re.compile(r"^### Object Model\s*$")


def _find_object_model_sections(lines: List[str]) -> List[tuple[int, int]]:
    sections = []
    start = None
    for i, line in enumerate(lines):
        if _OM_SECTION_RE.match(line):
            start = i
        elif start is not None and re.match(r"^#{2,3}\s", line) and not _OM_SECTION_RE.match(line):
            sections.append((start, i))
            start = None
    if start is not None:
        sections.append((start, len(lines)))
    return sections


def _lines_in_om(lines: List[str], sections: List[tuple[int, int]]) -> set[int]:
    result: set[int] = set()
    for s, e in sections:
        result.update(range(s, e))
    return result


class ClassBlockSeparatorScanner(Scanner):
    """Flag class blocks missing the ------ constructor/property separator."""

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
        om_set = _lines_in_om(lines, om_sections)

        i = 0
        while i < len(lines):
            if i not in om_set:
                i += 1
                continue
            line = lines[i]
            if _CLASS_HEADER_RE.match(line):
                class_name = line.strip()
                class_start = i + 1
                # Collect the class body until the next #### header or -----
                j = i + 1
                block_lines: List[str] = []
                while j < len(lines) and j in om_set:
                    bl = lines[j]
                    if _CLASS_HEADER_RE.match(bl):
                        break
                    # A stand-alone -----  (5-dash) separator closes the block
                    if re.match(r"^-{5}\s*$", bl) and not re.match(r"^-{6}", bl):
                        break
                    block_lines.append(bl)
                    j += 1

                # Check if the block has any members (properties or operations)
                has_member = any(
                    re.match(r"^[+\-]\s+", bl) for bl in block_lines
                )
                if not has_member:
                    i = j
                    continue

                # Check if there's a ------ separator (6+ dashes)
                has_separator = any(_CTOR_SEPARATOR_RE.match(bl) for bl in block_lines)
                if not has_separator:
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=(
                            f"Class block '{class_name}' has no ------ separator between "
                            f"constructor/initialisation and properties"
                        ),
                        location=str(file_path),
                        line_number=i + 1,
                        severity="error",
                    ).to_dict())
                i = j
            else:
                i += 1
        return violations


from object_model_context import build_object_model_context as _build_context  # noqa: E402


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            ClassBlockSeparatorScanner,
            rule_md_name="operations-have-signatures",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
