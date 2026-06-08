#!/usr/bin/env python3
"""Scanner: modules must have 4-7 KAs; each KA must have 4-7 terms."""
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

_CORE_DOMAIN_RE = re.compile(r"^# Core Domain\s*$", re.MULTILINE)
_BOUNDARY_DOMAIN_RE = re.compile(r"^# Boundary Domain\s*$", re.MULTILINE)
_H2_RE = re.compile(r"^## (.+)$", re.MULTILINE)
_H3_RE = re.compile(r"^### (.+)$", re.MULTILINE)

_SKIP_H3 = {"decisions made", "references", "key abstractions"}

MIN_KA = 4
MAX_KA = 7
MIN_TERMS = 4
MAX_TERMS = 7


class KaTermCountScanner(Scanner):

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

        core_match = _CORE_DOMAIN_RE.search(text)
        if not core_match:
            return violations

        core_start = core_match.end()

        boundary_match = _BOUNDARY_DOMAIN_RE.search(text, core_start)
        core_end = boundary_match.start() if boundary_match else len(text)

        core_text = text[core_start:core_end]

        ka_matches = list(_H2_RE.finditer(core_text))

        if len(ka_matches) < MIN_KA:
            violations.append(
                Violation(
                    rule=self.rule,
                    violation_message=(
                        f"{file_path.name}: only {len(ka_matches)} KA(s) found "
                        f"(minimum {MIN_KA}). Consider merging this module with "
                        f"a neighbour if it is too narrow."
                    ),
                    location=str(file_path),
                    severity="warning",
                ).to_dict()
            )
        elif len(ka_matches) > MAX_KA:
            violations.append(
                Violation(
                    rule=self.rule,
                    violation_message=(
                        f"{file_path.name}: {len(ka_matches)} KAs found "
                        f"(maximum {MAX_KA}). Consider splitting this module."
                    ),
                    location=str(file_path),
                    severity="warning",
                ).to_dict()
            )

        for i, ka_m in enumerate(ka_matches):
            ka_name = ka_m.group(1).strip()
            ka_start = ka_m.end()
            ka_end = ka_matches[i + 1].start() if i + 1 < len(ka_matches) else len(core_text)
            ka_block = core_text[ka_start:ka_end]

            terms = [
                m.group(1).strip()
                for m in _H3_RE.finditer(ka_block)
                if m.group(1).strip().lower() not in _SKIP_H3
            ]

            if len(terms) < MIN_TERMS:
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=(
                            f'{file_path.name}: KA "{ka_name}" has only '
                            f"{len(terms)} term(s) (minimum {MIN_TERMS}). "
                            f"Consider folding terms into a neighbouring KA."
                        ),
                        location=str(file_path),
                        severity="warning",
                    ).to_dict()
                )
            elif len(terms) > MAX_TERMS:
                violations.append(
                    Violation(
                        rule=self.rule,
                        violation_message=(
                            f'{file_path.name}: KA "{ka_name}" has '
                            f"{len(terms)} terms (maximum {MAX_TERMS}). "
                            f"Consider splitting this KA."
                        ),
                        location=str(file_path),
                        severity="warning",
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
            KaTermCountScanner,
            rule_md_name="ka-term-count",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
