#!/usr/bin/env python3
"""Scanner: every ### heading under ## Boundary terms must have an Owned by: field."""
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

_BOUNDARY_SECTION_RE = re.compile(r"^## Boundary terms\s*$", re.MULTILINE)
_H2_RE = re.compile(r"^## .+$", re.MULTILINE)
_H3_RE = re.compile(r"^### (.+)$", re.MULTILINE)
_OWNED_BY_RE = re.compile(r"^Owned by:\s*(.+)$", re.MULTILINE)


class BoundaryTermsHaveOwnerScanner(Scanner):

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        all_files = context.files.all_files
        if not all_files:
            return violations

        first_file = all_files[0]
        workspace = first_file.parent.parent

        DL_path = workspace / "abd-domain-driven-design" / "domain-language.md"
        if not DL_path.exists():
            return violations

        text = DL_path.read_text(encoding="utf-8")

        boundary_match = _BOUNDARY_SECTION_RE.search(text)
        if not boundary_match:
            return violations

        boundary_start = boundary_match.end()

        next_h2 = None
        for m in _H2_RE.finditer(text, boundary_start):
            next_h2 = m.start()
            break

        boundary_text = text[boundary_start:next_h2] if next_h2 else text[boundary_start:]

        h3_matches = list(_H3_RE.finditer(boundary_text))

        for i, m in enumerate(h3_matches):
            heading = m.group(1).strip()
            start = m.end()
            end = h3_matches[i + 1].start() if i + 1 < len(h3_matches) else len(boundary_text)
            block = boundary_text[start:end]

            owned_match = _OWNED_BY_RE.search(block)
            if not owned_match:
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=(
                            f'Boundary term "### {heading}" has no '
                            f'"Owned by:" field. Every boundary term must '
                            f"name the single module that owns the concept."
                        ),
                        location=str(DL_path),
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
                                f'Boundary term "### {heading}" lists multiple '
                                f'owners: "{owner}". A boundary term must have '
                                f"exactly one owner. Multiple owners means this "
                                f"is a base abstraction, not a boundary term."
                            ),
                            location=str(DL_path),
                            severity="error",
                        ).to_dict()
                    )

        return violations


def _build_context(workspace: Path) -> ScanFilesContext:
    files: List[Path] = []
    DL = workspace / "abd-domain-driven-design" / "domain-language.md"
    if DL.is_file():
        files.append(DL)
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
