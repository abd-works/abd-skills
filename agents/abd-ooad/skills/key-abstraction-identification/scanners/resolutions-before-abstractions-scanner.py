#!/usr/bin/env python3
"""Scanner: ### Resolutions must appear before the first ### Key Abstraction in each module."""
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
    ParsedModule,
    RESOLUTIONS_HEADING_RE,
    KA_HEADING_RE,
    build_ka_context,
)


class ResolutionsBeforeAbstractionScanner(MarkdownArtifactScanner):

    def check_artifact(self, parsed: ParsedArtifact) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        location = str(parsed.file_path or "key-abstractions.md")

        if parsed.has_modules:
            for mod in parsed.modules:
                violations.extend(self._check_module(mod, location))
        else:
            violations.extend(self._check_flat(parsed, location))

        return violations

    def _check_module(self, mod: ParsedModule, location: str) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []

        if not mod.key_abstractions:
            return violations

        if not mod.has_resolutions:
            violations.append(self._violation(
                f'Module "[{mod.name}]": missing ### Resolutions section. '
                f"Every module must document settle-pass outcomes before listing Key Abstractions.",
                location, mod.line_number,
            ))
        elif mod.resolutions_line > mod.first_ka_line and mod.first_ka_line > 0:
            violations.append(self._violation(
                f'Module "[{mod.name}]": ### Resolutions (line {mod.resolutions_line}) '
                f"appears after the first ### Key Abstraction (line {mod.first_ka_line}). "
                f"Resolutions must come first.",
                location, mod.resolutions_line,
            ))

        return violations

    def _check_flat(self, parsed: ParsedArtifact, location: str) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []

        if not parsed.flat_abstractions:
            return violations

        res_match = RESOLUTIONS_HEADING_RE.search(parsed.content)
        ka_match = KA_HEADING_RE.search(parsed.content)

        if not res_match:
            violations.append(self._violation(
                "Flat file: missing ### Resolutions section. "
                "Place it under the H1 / front matter, before the first ### Key Abstraction.",
                location,
            ))
        elif ka_match and res_match.start() > ka_match.start():
            res_line = parsed.content[:res_match.start()].count("\n") + 1
            violations.append(self._violation(
                f"Flat file: ### Resolutions (line {res_line}) appears after "
                f"the first ### Key Abstraction. Resolutions must come first.",
                location, res_line,
            ))

        return violations


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            ResolutionsBeforeAbstractionScanner,
            rule_md_name="resolutions-before-abstractions",
            build_context=build_ka_context,
            skill_root=_ROOT,
        )
    )
