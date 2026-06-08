#!/usr/bin/env python3
"""Scanner: collaborator lines must appear before invariant lines under a method.

When a method has both collaborator references and invariant constraints,
collaborators must be listed first.  A collaborator line is tab-indented and
starts with an uppercase type name.  An invariant line starts with
tab + 'Invariant:'.
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
_METHOD_RE = re.compile(r"^[-]?\s*\w+\s*\(")
_COLLABORATOR_RE = re.compile(r"^\t[A-Z]\w+")
_INVARIANT_RE = re.compile(r"^\tInvariant:")


class CollaboratorsBeforeInvariantsScanner(Scanner):
    """Flag methods where an Invariant: line appears before a collaborator line."""

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
            method_m = _METHOD_RE.match(line)
            if not method_m:
                i += 1
                continue

            method_name = line.strip()
            method_line = i
            seen_invariant = False
            j = i + 1

            while j < len(lines):
                sub = lines[j]
                if not sub.startswith("\t"):
                    break
                if _INVARIANT_RE.match(sub):
                    seen_invariant = True
                elif _COLLABORATOR_RE.match(sub) and not _INVARIANT_RE.match(sub):
                    if seen_invariant:
                        violations.append(Violation(
                            rule=self.rule,
                            violation_message=(
                                f"Method '{method_name[:60]}': collaborator '{sub.strip()}' "
                                f"appears after an Invariant: line — collaborators must come first"
                            ),
                            location=str(file_path),
                            line_number=j + 1,
                            severity="error",
                        ).to_dict())
                j += 1

            i = j
        return violations


from domain_model_context import build_domain_model_context as _build_context  # noqa: E402


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            CollaboratorsBeforeInvariantsScanner,
            rule_md_name="collaborators-before-invariants",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
