#!/usr/bin/env python3
"""Scanner: every variable assignment inside an Interaction: block must carry a type annotation."""
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

_INTERACTION_RE = re.compile(r"^\t\s*Interaction\s*:\s*$", re.IGNORECASE)
_ASSIGNMENT_RE = re.compile(r"^(\t{2,})(\w[\w.]*)(\s*)=\s*.+$")
_TYPED_ASSIGNMENT_RE = re.compile(r"^(\t{2,})(\w[\w.]*)\s*:\s*\S+.*=\s*.+$")
_CONTROL_FLOW_RE = re.compile(
    r"^\t{2,}\s*(return|if|else|for|while|super|switch|break|continue)\b",
    re.IGNORECASE,
)


class InteractionVariableTypesScanner(Scanner):
    """Flag Interaction: variable lines that lack type annotations."""

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

        i = 0
        while i < len(lines):
            if i not in scannable:
                i += 1
                continue
            line = lines[i]
            if _INTERACTION_RE.match(line):
                i += 1
                while i < len(lines) and i in scannable:
                    inner = lines[i]
                    if not inner.startswith("\t\t") and inner.strip() != "":
                        break
                    if _CONTROL_FLOW_RE.match(inner):
                        i += 1
                        continue
                    if _ASSIGNMENT_RE.match(inner) and not _TYPED_ASSIGNMENT_RE.match(inner):
                        m = _ASSIGNMENT_RE.match(inner)
                        var_name = m.group(2) if m else "?"
                        violations.append(Violation(
                            rule=self.rule,
                            violation_message=(
                                f"Interaction variable '{var_name}' has no type annotation"
                            ),
                            location=str(file_path),
                            line_number=i + 1,
                            severity="error",
                        ).to_dict())
                    i += 1
            else:
                i += 1
        return violations


from object_model_context import (  # noqa: E402
    build_object_model_context as _build_context,
    domain_spec_scannable_line_indices,
)


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            InteractionVariableTypesScanner,
            rule_md_name="interaction-uses-domain-language",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
