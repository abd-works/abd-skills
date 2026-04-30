#!/usr/bin/env python3
"""Scanner: every Key Abstraction must have Intent, Core terms, Shape hint, and ≥1 extract."""
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


class RequiredFieldsPerAbstractionScanner(MarkdownArtifactScanner):

    def check_artifact(self, parsed: ParsedArtifact) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        all_kas = self._collect_all_kas(parsed)
        location = str(parsed.file_path or "key-abstractions.md")

        for ka in all_kas:
            if not ka.intent:
                violations.append(self._violation(
                    f'Key Abstraction "{ka.name}": missing Intent line.',
                    location, ka.line_number,
                ))
            if not ka.core_terms:
                violations.append(self._violation(
                    f'Key Abstraction "{ka.name}": missing or empty Core terms list.',
                    location, ka.line_number,
                ))
            if not ka.shape_hint:
                violations.append(self._violation(
                    f'Key Abstraction "{ka.name}": missing Shape hint line.',
                    location, ka.line_number,
                ))
            if not ka.extracts:
                violations.append(self._violation(
                    f'Key Abstraction "{ka.name}": no Extract blocks found (at least one required).',
                    location, ka.line_number,
                ))

        return violations

    @staticmethod
    def _collect_all_kas(parsed: ParsedArtifact) -> List[ParsedKeyAbstraction]:
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
            RequiredFieldsPerAbstractionScanner,
            rule_md_name="required-fields-per-abstraction",
            build_context=build_ka_context,
            skill_root=_ROOT,
        )
    )
