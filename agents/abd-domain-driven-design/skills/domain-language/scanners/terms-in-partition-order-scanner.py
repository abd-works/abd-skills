#!/usr/bin/env python3
"""Scanner: Core terms in DL must appear in the same order as the module partition."""
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

_CORE_TERMS_RE = re.compile(r"^\*\*Core terms\*\*:", re.MULTILINE)
_H3_RE = re.compile(r"^### (.+)$", re.MULTILINE)
_BOUNDARY_RE = re.compile(r"^## Boundary terms", re.MULTILINE)


def _extract_core_terms(partition_text: str) -> List[str]:
    m = _CORE_TERMS_RE.search(partition_text)
    if not m:
        return []
    after = partition_text[m.end():]
    terms: List[str] = []
    for line in after.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            terms.append(line[2:].strip().lower())
        elif line == "" or line.startswith("---"):
            if terms:
                break
    return terms


def _extract_h3_before_boundary(DL_text: str) -> List[str]:
    boundary = _BOUNDARY_RE.search(DL_text)
    region = DL_text[:boundary.start()] if boundary else DL_text
    return [m.group(1).strip().lower() for m in _H3_RE.finditer(region)]


class TermsInPartitionOrderScanner(Scanner):

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        all_files = context.files.all_files
        if not all_files:
            return violations

        first_file = all_files[0]
        workspace = first_file.parent.parent

        DL_path = workspace / "abd-domain-driven-design" / "domain-language.md"
        modules_dir = workspace / "abd-domain-driven-design" / "modules"

        if not DL_path.exists() or not modules_dir.is_dir():
            return violations

        DL_text = DL_path.read_text(encoding="utf-8")
        DL_headings = _extract_h3_before_boundary(DL_text)

        module_re = re.compile(r"^#+ Module:\s*\[(.+?)\]", re.MULTILINE)
        DL_modules = {m.group(1).strip().lower() for m in module_re.finditer(DL_text)}

        for mod_file in sorted(modules_dir.glob("*.md")):
            if mod_file.name in ("unallocated.md", "rejected.md"):
                continue

            partition_text = mod_file.read_text(encoding="utf-8")

            mod_match = module_re.search(partition_text)
            if not mod_match:
                continue
            mod_name = mod_match.group(1).strip().lower()
            if mod_name not in DL_modules:
                continue

            core_terms = _extract_core_terms(partition_text)

            if not core_terms:
                continue

            core_in_DL = [h for h in DL_headings if h in core_terms]

            expected_order = [t for t in core_terms if t in core_in_DL]

            if core_in_DL != expected_order:
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=(
                            f"Core terms from {mod_file.name} appear out of "
                            f"partition order in domain-language.md. "
                            f"Expected order: {expected_order[:5]}... "
                            f"Found order: {core_in_DL[:5]}..."
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
    modules_dir = workspace / "abd-domain-driven-design" / "modules"
    if modules_dir.is_dir():
        for f in sorted(modules_dir.glob("*.md")):
            if f.is_file():
                files.append(f)
    return ScanFilesContext(files=FileCollection(code_files=files))


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            TermsInPartitionOrderScanner,
            rule_md_name="terms-in-partition-order",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
