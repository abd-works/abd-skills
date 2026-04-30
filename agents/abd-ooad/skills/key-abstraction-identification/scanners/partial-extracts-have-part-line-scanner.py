#!/usr/bin/env python3
"""Scanner: Extract: partial must have Part:; Extract: whole must not."""
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
    build_ka_context,
)


class PartialExtractsHavePartLineScanner(MarkdownArtifactScanner):

    def check_artifact(self, parsed: ParsedArtifact) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        location = str(parsed.file_path or "key-abstractions.md")

        for ka in self._all_kas(parsed):
            for ext in ka.extracts:
                if ext.extract_type == "partial" and not ext.part:
                    violations.append(self._violation(
                        f'Key Abstraction "{ka.name}", extract "{ext.title}": '
                        f"Extract: partial but no Part: line. "
                        f"Reviewers need Part: to identify which slice this is.",
                        location, ext.line_number,
                    ))
                elif ext.extract_type == "whole" and ext.part:
                    violations.append(self._violation(
                        f'Key Abstraction "{ka.name}", extract "{ext.title}": '
                        f"Extract: whole should not have a Part: line — "
                        f"if only part of the passage is here, use Extract: partial.",
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
            PartialExtractsHavePartLineScanner,
            rule_md_name="partial-extracts-have-part-line",
            build_context=build_ka_context,
            skill_root=_ROOT,
        )
    )
