#!/usr/bin/env python3
"""Scanner: every ### term heading must have at least one Ref entry."""
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

_H3_RE = re.compile(r"^### (.+)$", re.MULTILINE)

_DT_CANDIDATES = [
    "docs/domain/domain-terms.md",
    "domain/domain-terms.md",
    "abd-domain-driven-design/domain-terms.md",
]


def _find_domain_terms(workspace: Path) -> Path | None:
    for rel in _DT_CANDIDATES:
        p = workspace / rel
        if p.exists():
            return p
    return None
_REF_RE = re.compile(r"^\*\*Ref\s*—\s*.+\*\*\s*$", re.MULTILINE)
_SKIP_HEADINGS = {
    "trait — base abstraction owned by this module",
    "boundary objects — concepts this module depends on but does not own",
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

        first_file = all_files[0]
        workspace = context.workspace if hasattr(context, "workspace") else first_file.parent.parent

        DL_path = _find_domain_terms(workspace)
        if DL_path is None:
            return violations

        text = DL_path.read_text(encoding="utf-8")
        h3_matches = list(_H3_RE.finditer(text))

        for i, m in enumerate(h3_matches):
            heading = m.group(1).strip()
            if heading.lower() in _SKIP_HEADINGS:
                continue

            start = m.end()
            end = h3_matches[i + 1].start() if i + 1 < len(h3_matches) else len(text)
            block = text[start:end]

            if not _REF_RE.search(block):
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=(
                            f'Term "### {heading}" has no Ref entry. '
                            f"Every term must carry at least one "
                            f"**Ref — …** with Source/Locator/Extract."
                        ),
                        location=str(DL_path),
                        severity="error",
                    ).to_dict()
                )

        return violations


def _build_context(workspace: Path, story_graph=None) -> ScanFilesContext:
    files: List[Path] = []
    DL = _find_domain_terms(workspace)
    if DL is not None:
        files.append(DL)
    ctx = ScanFilesContext(files=FileCollection(code_files=files))
    if hasattr(ctx, "workspace"):
        ctx.workspace = workspace
    return ctx


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            RefsPerTermScanner,
            rule_md_name="refs-per-term",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
