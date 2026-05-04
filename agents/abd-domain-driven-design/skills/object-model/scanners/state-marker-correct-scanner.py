#!/usr/bin/env python3
"""Scanner: front matter must contain state: domain-model."""
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
    """Check that module files at object-model stage carry state: domain-model."""

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
                violation_message="No YAML front matter found; expected state: domain-model",
                location=str(file_path),
                line_number=1,
                severity="error",
            ).to_dict()]
        state_m = _STATE_RE.search(fm.group(1))
        if not state_m:
            return [Violation(
                rule=self.rule,
                violation_message="No state: key in front matter; expected state: domain-model",
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
            StateMarkerCorrectScanner,
            rule_md_name="state-marker-correct",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
