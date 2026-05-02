#!/usr/bin/env python3
"""Scanner: every Core term from module-partition must appear as a ### heading in the DL."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).resolve().parent.parent
_REPO = _ROOT.parent.parent.parent.parent  # agents/abd-domain-driven-design/skills/<skill> -> repo root
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
_TERM_BULLET_RE = re.compile(r"^- (.+)$", re.MULTILINE)
_H3_RE = re.compile(r"^### (.+)$", re.MULTILINE)
_MODULE_RE = re.compile(r"^#+ Module:\s*\[(.+?)\]", re.MULTILINE)


def _extract_core_terms(partition_text: str) -> List[str]:
    m = _CORE_TERMS_RE.search(partition_text)
    if not m:
        return []
    after = partition_text[m.end():]
    terms: List[str] = []
    for line in after.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            terms.append(line[2:].strip())
        elif line == "" or line.startswith("---"):
            if terms:
                break
    return terms


def _extract_h3_headings(DL_text: str) -> List[str]:
    return [m.group(1).strip() for m in _H3_RE.finditer(DL_text)]


class AllCoreTermsPresentScanner(Scanner):

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        all_files = context.files.all_files
        if not all_files:
            return violations

        first_file = all_files[0]
        workspace = first_file.parent.parent

        DL_path = workspace / "abd-domain-driven-design" / "domain-language.md"
        modules_dir = workspace / "abd-domain-driven-design" / "modules"

        if not DL_path.exists():
            violations.append(
                Violation(
                    rule=self.rule,
                    violation_message="domain-language.md not found.",
                    location=str(workspace / "abd-domain-driven-design"),
                    severity="error",
                ).to_dict()
            )
            return violations

        DL_text = DL_path.read_text(encoding="utf-8")
        headings_lower = [h.lower() for h in _extract_h3_headings(DL_text)]

        DL_modules = {m.group(1).strip().lower() for m in _MODULE_RE.finditer(DL_text)}

        if not modules_dir.is_dir():
            return violations

        for mod_file in sorted(modules_dir.glob("*.md")):
            if mod_file.name in ("unallocated.md", "rejected.md"):
                continue
            partition_text = mod_file.read_text(encoding="utf-8")

            mod_match = _MODULE_RE.search(partition_text)
            if not mod_match:
                continue
            mod_name = mod_match.group(1).strip().lower()
            if mod_name not in DL_modules:
                continue

            core_terms = _extract_core_terms(partition_text)

            for term in core_terms:
                if term.lower() not in headings_lower:
                    violations.append(
                        Violation(
                            rule=self.rule,
                            violation_message=(
                                f'Core term "{term}" from {mod_file.name} '
                                f"has no matching ### heading in "
                                f"domain-language.md."
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
            AllCoreTermsPresentScanner,
            rule_md_name="all-core-terms-present",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
