#!/usr/bin/env python3
"""Scanner: every ### term heading must have at least one Ref entry."""
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

_H3_RE = re.compile(r"^### (.+)$", re.MULTILINE)
_REF_RE = re.compile(r"^\*\*Ref\s*\u2014\s*.+\*\*\s*$", re.MULTILINE)
_SKIP_HEADINGS = {
    "decisions made",
    "references",
    "key abstractions",
}


class RefsPerTermScanner(Scanner):

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
        h3_matches = list(_H3_RE.finditer(text))

        for i, m in enumerate(h3_matches):
            heading = m.group(1).strip()
            heading_lower = heading.lower()
            if any(skip in heading_lower for skip in _SKIP_HEADINGS):
                continue

            start = m.end()
            end = h3_matches[i + 1].start() if i + 1 < len(h3_matches) else len(text)
            block = text[start:end]

            if not _REF_RE.search(block):
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=(
                            f'Term "### {heading}" in {file_path.name} has no '
                            f"Ref entry. Every term must carry at least one "
                            f"**Ref \u2014 \u2026** with Source/Locator/Extract."
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
            RefsPerTermScanner,
            rule_md_name="refs-per-term",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
