#!/usr/bin/env python3
"""Scanner: every class block must have a ------ separator.

The six-dash separator (------) divides the constructor line from the
properties block.  In domain-model format, class headers are ### **ClassName**
(triple-hash), members have no + prefix, and blocks run from one ### **
heading to the next.
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

_CLASS_HEADER_RE = re.compile(r"^### \*\*[^*]+\*\*")
_CTOR_SEPARATOR_RE = re.compile(r"^-{6,}\s*$")
_PROPERTY_RE = re.compile(r"^\w+\s*:")
_METHOD_RE = re.compile(r"^\w+\s*\(")
_PRIVATE_METHOD_RE = re.compile(r"^-\s+\w+\s*\(")


def _is_member_line(line: str) -> bool:
    """True if line looks like a property, method, or private method."""
    stripped = line.strip()
    if not stripped:
        return False
    if _PROPERTY_RE.match(stripped):
        return True
    if _METHOD_RE.match(stripped):
        return True
    if _PRIVATE_METHOD_RE.match(stripped):
        return True
    return False


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

        i = 0
        while i < len(lines):
            line = lines[i]
            if _CLASS_HEADER_RE.match(line):
                class_name = line.strip()
                j = i + 1
                block_lines: List[str] = []
                while j < len(lines):
                    bl = lines[j]
                    if _CLASS_HEADER_RE.match(bl):
                        break
                    block_lines.append(bl)
                    j += 1

                has_member = any(_is_member_line(bl) for bl in block_lines)
                if not has_member:
                    i = j
                    continue

                has_separator = any(_CTOR_SEPARATOR_RE.match(bl) for bl in block_lines)
                if not has_separator:
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=(
                            f"Class block '{class_name}' has no ------ separator between "
                            f"constructor and properties"
                        ),
                        location=str(file_path),
                        line_number=i + 1,
                        severity="error",
                    ).to_dict())
                i = j
            else:
                i += 1
        return violations


from domain_model_context import build_domain_model_context as _build_context  # noqa: E402


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            ClassBlockSeparatorScanner,
            rule_md_name="class-block-separator",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
