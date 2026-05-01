#!/usr/bin/env python3
"""Scanner: Core terms phrases must be disjoint within each module/flat scope."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

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
    ParsedModule,
    build_ka_context,
)


class CoreTermsDisjointScanner(MarkdownArtifactScanner):

    def check_artifact(self, parsed: ParsedArtifact) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        location = str(parsed.file_path or "key-abstractions.md")

        if parsed.has_modules:
            for mod in parsed.modules:
                violations.extend(
                    self._check_scope(mod.key_abstractions, f'Module "[{mod.name}]"', location)
                )
        else:
            violations.extend(
                self._check_scope(parsed.flat_abstractions, "File", location)
            )

        return violations

    def _check_scope(
        self, kas: List[ParsedKeyAbstraction], scope_label: str, location: str
    ) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        seen: Dict[str, str] = {}  # normalised phrase -> first KA name

        for ka in kas:
            for term in ka.core_terms:
                normalised = term.strip().lower()
                if not normalised:
                    continue
                if normalised in seen:
                    violations.append(self._violation(
                        f'{scope_label}: Core term "{term}" appears under both '
                        f'"{seen[normalised]}" and "{ka.name}". '
                        f"Each phrase must belong to exactly one Key Abstraction within the same scope.",
                        location, ka.line_number,
                    ))
                else:
                    seen[normalised] = ka.name

        return violations


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            CoreTermsDisjointScanner,
            rule_md_name="core-terms-disjoint",
            build_context=build_ka_context,
            skill_root=_ROOT,
        )
    )
