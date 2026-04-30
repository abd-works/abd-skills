#!/usr/bin/env python3
"""Scanner: every extract must have Source, Locator, Extract type, and Part when partial."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).resolve().parent.parent
_SKILLS = _ROOT.parent
for _p in (
    _SKILLS / "execute_using_rules" / "scripts",
    _ROOT / "scanners",
):
    s = str(_p)
    if s not in sys.path:
        sys.path.insert(0, s)

from scanner_runner import execute_scan_with_workspace  # noqa: E402
from markdown_artifact_scanner import (  # noqa: E402
    MarkdownArtifactScanner,
    ParsedArtifact,
    ParsedKeyAbstraction,
    ParsedExtract,
    build_ka_context,
)


class ExtractFormatComplianceScanner(MarkdownArtifactScanner):

    VALID_TYPES = {"whole", "partial"}

    def check_artifact(self, parsed: ParsedArtifact) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        location = str(parsed.file_path or "key-abstractions.md")

        for ka in self._all_kas(parsed):
            for ext in ka.extracts:
                violations.extend(self._check_extract(ext, ka.name, location))

        return violations

    def _check_extract(self, ext: ParsedExtract, ka_name: str, location: str) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        prefix = f'Key Abstraction "{ka_name}", extract "{ext.title}"'

        if not ext.source_ref:
            violations.append(self._violation(
                f"{prefix}: missing Source: line.", location, ext.line_number
            ))

        if not ext.locator:
            violations.append(self._violation(
                f"{prefix}: missing Locator: line.", location, ext.line_number
            ))

        if not ext.extract_type:
            violations.append(self._violation(
                f"{prefix}: missing Extract: line (must be 'whole' or 'partial').",
                location, ext.line_number,
            ))
        elif ext.extract_type not in self.VALID_TYPES:
            violations.append(self._violation(
                f'{prefix}: Extract type "{ext.extract_type}" is invalid — must be "whole" or "partial".',
                location, ext.line_number,
            ))

        if ext.extract_type == "partial" and not ext.part:
            violations.append(self._violation(
                f"{prefix}: Extract: partial but no Part: line present.",
                location, ext.line_number,
            ))

        if ext.extract_type == "whole" and ext.part:
            violations.append(self._violation(
                f"{prefix}: Extract: whole should not have a Part: line (contradicts 'whole').",
                location, ext.line_number, severity="warning",
            ))

        return violations

    @staticmethod
    def _all_kas(parsed: ParsedArtifact) -> List[ParsedKeyAbstraction]:
        kas: List[ParsedKeyAbstraction] = []
        if parsed.has_modules:
            for mod in parsed.modules:
                kas.extend(mod.key_abstractions)
        else:
            kas.extend(parsed.flat_abstractions)
        return kas


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            ExtractFormatComplianceScanner,
            rule_md_name="extract-format-compliance",
            build_context=build_ka_context,
            skill_root=_ROOT,
        )
    )
