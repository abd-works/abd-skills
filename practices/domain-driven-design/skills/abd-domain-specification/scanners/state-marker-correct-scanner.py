#!/usr/bin/env python3
"""Scanner: front matter must contain state: domain-specification."""
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

_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
_STATE_RE = re.compile(r"^state:\s*(.+)$", re.MULTILINE)
_EXPECTED_STATE = "domain-model"


class StateMarkerCorrectScanner(Scanner):
    """Check that module files at domain-specification stage carry state: domain-specification."""

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        for fp in context.files.all_files:
            if fp and fp.is_file():
                violations.extend(self._scan_file(fp))
        return violations

    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        content = file_path.read_text(encoding="utf-8")
        fm = _FRONT_MATTER_RE.match(content)
        if not fm:
            return [Violation(
                rule=self.rule,
                violation_message="No YAML front matter found; expected state: domain-specification",
                location=str(file_path),
                line_number=1,
                severity="error",
            ).to_dict()]
        state_m = _STATE_RE.search(fm.group(1))
        if not state_m:
            return [Violation(
                rule=self.rule,
                violation_message="No state: key in front matter; expected state: domain-specification",
                location=str(file_path),
                line_number=1,
                severity="error",
            ).to_dict()]
        actual = state_m.group(1).strip()
        if actual != _EXPECTED_STATE:
            return [Violation(
                rule=self.rule,
                violation_message=f"state: '{actual}' — expected 'domain-model'",
                location=str(file_path),
                line_number=1,
                severity="error",
            ).to_dict()]
        return []


from object_model_context import build_object_model_context as _build_context  # noqa: E402


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            StateMarkerCorrectScanner,
            rule_md_name="state-marker-correct",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
