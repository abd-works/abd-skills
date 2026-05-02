#!/usr/bin/env python3
"""Scanner: no identification-model jargon (Intent, Shape hint, Tension, etc.)."""
from __future__ import annotations

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
from markdown_artifact_scanner import (  # noqa: E402
    ModuleFileScanner,
    ParsedModuleFile,
    build_module_context,
    INTENT_LINE_RE,
    SHAPE_HINT_LINE_RE,
    TENSION_LINE_RE,
    CORE_TERMS_ABSORBED_RE,
    KA_HEADING_RE,
)


class NoJargonScanner(ModuleFileScanner):
    rule = "no-jargon-added"

    JARGON_PATTERNS = [
        (INTENT_LINE_RE, "Intent:"),
        (SHAPE_HINT_LINE_RE, "Shape hint:"),
        (TENSION_LINE_RE, "Tension:"),
        (CORE_TERMS_ABSORBED_RE, "Core terms (absorbed..."),
        (KA_HEADING_RE, "## Key Abstraction: (old format)"),
    ]

    def check_artifact(self, parsed: ParsedModuleFile) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        fname = str(parsed.file_path or "unknown")
        content = parsed.content

        for pattern, label in self.JARGON_PATTERNS:
            for m in pattern.finditer(content):
                line_num = content[:m.start()].count("\n") + 1
                violations.append(self._violation(
                    f"Old-model jargon found: '{label}' at line {line_num}",
                    fname,
                    line_num,
                ))

        return violations


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            NoJargonScanner,
            rule_md_name="no-jargon-added",
            build_context=build_module_context,
            skill_root=_ROOT,
        )
    )
