#!/usr/bin/env python3
"""Scanner: boundary terms under # Boundary Domain must name their owning module."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).resolve().parent.parent
_SKILLS = _ROOT.parent
for _p in (
    _SKILLS / "execute-skill-using-skills-rules" / "scripts",
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

_BOUNDARY_SECTION_RE = re.compile(r"^# Boundary Domain\s*$", re.MULTILINE)
_H1_RE = re.compile(r"^# .+$", re.MULTILINE)
_H3_RE = re.compile(r"^### (.+)$", re.MULTILINE)
_OWNED_BY_RE = re.compile(r"\*\(owned by:\s*(.+?)\)\*")


class BoundaryTermsHaveOwnerScanner(Scanner):

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        all_files = context.files.all_files
        if not all_files:
            return violations

        for fp in all_files:
            if not fp.exists() or not fp.is_file():
                continue
            if fp.name in ("rejected.md", "unallocated.md"):
                continue
            violations.extend(self._scan_file(fp))

        return violations

    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        text = file_path.read_text(encoding="utf-8")

        boundary_match = _BOUNDARY_SECTION_RE.search(text)
        if not boundary_match:
            return violations

        boundary_start = boundary_match.end()

        next_h1 = None
        for m in _H1_RE.finditer(text, boundary_start):
            next_h1 = m.start()
            break

        boundary_text = text[boundary_start:next_h1] if next_h1 else text[boundary_start:]

        h3_matches = list(_H3_RE.finditer(boundary_text))

        for i, m in enumerate(h3_matches):
            heading = m.group(1).strip()
            heading_lower = heading.lower()
            if "decisions made" in heading_lower or "references" in heading_lower:
                continue

            owned_match = _OWNED_BY_RE.search(heading)
            if not owned_match:
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=(
                            f'Boundary term "### {heading}" in {file_path.name} '
                            f"has no ownership annotation. Use "
                            f"### term *(owned by: Module)* format."
                        ),
                        location=str(file_path),
                        severity="error",
                    ).to_dict()
                )
            else:
                owner = owned_match.group(1).strip()
                if "," in owner:
                    violations.append(
                        Violation(
                            rule=self.rule,
                            violation_message=(
                                f'Boundary term "### {heading}" in {file_path.name} '
                                f'lists multiple owners: "{owner}". A boundary term '
                                f"must have exactly one owner."
                            ),
                            location=str(file_path),
                            severity="error",
                        ).to_dict()
                    )

        return violations


def _build_context(workspace: Path) -> ScanFilesContext:
    modules_dir = workspace / "domain" / "modules"
    files: List[Path] = []
    if modules_dir.is_dir():
        for f in sorted(modules_dir.glob("*.md")):
            if f.is_file():
                files.append(f)
    return ScanFilesContext(files=FileCollection(code_files=files))


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            BoundaryTermsHaveOwnerScanner,
            rule_md_name="boundary-terms-have-owner",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
