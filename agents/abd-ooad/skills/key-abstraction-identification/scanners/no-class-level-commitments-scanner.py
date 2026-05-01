#!/usr/bin/env python3
"""Scanner: no stereotype tags, typed properties, method sigs, or cardinality arrows."""
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
    STEREOTYPE_RE,
    TYPED_PROPERTY_RE,
    METHOD_SIG_RE,
    CARDINALITY_RE,
    SOURCE_BLOCK_RE,
    build_ka_context,
)


class NoClassLevelCommitmentsScanner(MarkdownArtifactScanner):

    def check_artifact(self, parsed: ParsedArtifact) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        location = str(parsed.file_path or "key-abstractions.md")

        content_to_check = self._non_source_content(parsed.content)

        for i, line in enumerate(content_to_check.splitlines(), start=1):
            if STEREOTYPE_RE.search(line):
                violations.append(self._violation(
                    f'Line {i}: UML stereotype tag found: "{line.strip()}". '
                    f"Stereotypes (<<Entity>>, <<ValueObject>>, etc.) belong to later skills.",
                    location, i,
                ))

            if TYPED_PROPERTY_RE.search(line):
                violations.append(self._violation(
                    f'Line {i}: typed property found: "{line.strip()}". '
                    f"Typed properties belong to later class-level skills.",
                    location, i, severity="warning",
                ))

            if METHOD_SIG_RE.search(line):
                violations.append(self._violation(
                    f'Line {i}: method signature found: "{line.strip()}". '
                    f"Method signatures belong to later class-level skills.",
                    location, i, severity="warning",
                ))

            if CARDINALITY_RE.search(line):
                violations.append(self._violation(
                    f'Line {i}: cardinality notation found: "{line.strip()}". '
                    f"Cardinality arrows belong to later relationship skills.",
                    location, i, severity="warning",
                ))

        return violations

    @staticmethod
    def _non_source_content(content: str) -> str:
        """Remove ```source blocks so we don't flag verbatim source text."""
        return SOURCE_BLOCK_RE.sub("", content)

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
            NoClassLevelCommitmentsScanner,
            rule_md_name="no-class-level-commitments",
            build_context=build_ka_context,
            skill_root=_ROOT,
        )
    )
