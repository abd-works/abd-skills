#!/usr/bin/env python3
"""Scanner: operations with two or more Invariant: lines must have an Interaction: block."""
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
from scanner_bases.resources.scan_context import ScanFilesContext  # noqa: E402

_MEMBER_RE = re.compile(r"^[+\-]\s+\S")
_INVARIANT_RE = re.compile(r"^\t\s*Invariant\s*:", re.IGNORECASE)
_INTERACTION_RE = re.compile(r"^\t\s*Interaction\s*:", re.IGNORECASE)


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
        lines = file_path.read_text(encoding="utf-8").split("\n")
        scannable = domain_spec_scannable_line_indices(lines)
        if not scannable:
            return violations
        return self._scan_section(lines, 0, len(lines), file_path, scannable)

    def _scan_section(
        self,
        lines: List[str],
        sec_start: int,
        sec_end: int,
        file_path: Path,
        scannable: set[int],
    ) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        i = sec_start
        while i < sec_end:
            if i not in scannable:
                i += 1
                continue
            line = lines[i]
            if _MEMBER_RE.match(line) and "(" in line:
                op_line_num = i + 1
                op_text = line.strip()
                invariant_count = 0
                has_interaction = False
                j = i + 1
                while j < sec_end:
                    ann = lines[j]
                    if _INVARIANT_RE.match(ann):
                        invariant_count += 1
                    elif _INTERACTION_RE.match(ann):
                        has_interaction = True
                        j += 1
                        while j < sec_end and lines[j].startswith("\t"):
                            j += 1
                        break
                    elif ann.strip() == "" or ann.startswith("\t"):
                        pass
                    else:
                        break
                    j += 1
                if invariant_count >= 2 and not has_interaction:
                    violations.append(Violation(
                        rule=self.rule,
                        violation_message=(
                            f"Operation '{op_text}' has {invariant_count} Invariant: lines "
                            f"but no Interaction: block"
                        ),
                        location=str(file_path),
                        line_number=op_line_num,
                        severity="error",
                    ).to_dict())
            i += 1
        return violations


from object_model_context import (  # noqa: E402
    build_object_model_context as _build_context,
    domain_spec_scannable_line_indices,
)


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            InvariantsWithoutInteractionsScanner,
            rule_md_name="invariants-without-interactions",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
