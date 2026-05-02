#!/usr/bin/env python3
"""Scanner: no class-level commitments (stereotypes, typed props, method sigs, cardinality)."""
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
    STEREOTYPE_RE,
    TYPED_PROPERTY_RE,
    METHOD_SIG_RE,
    CARDINALITY_RE,
    SOURCE_BLOCK_RE,
)


class NoClassLevelCommitmentsScanner(ModuleFileScanner):
    rule = "no-class-level-commitments"

    PATTERNS = [
        (STEREOTYPE_RE, "UML stereotype tag"),
        (TYPED_PROPERTY_RE, "Typed property"),
        (METHOD_SIG_RE, "Method signature"),
        (CARDINALITY_RE, "Cardinality notation"),
    ]

    def check_artifact(self, parsed: ParsedModuleFile) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        fname = str(parsed.file_path or "unknown")

        content_no_source = SOURCE_BLOCK_RE.sub("", parsed.content)

        for pattern, label in self.PATTERNS:
            for m in pattern.finditer(content_no_source):
                line_num = content_no_source[:m.start()].count("\n") + 1
                violations.append(self._violation(
                    f"{label} found: '{m.group()}'",
                    fname,
                    line_num,
                ))

        return violations


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            NoClassLevelCommitmentsScanner,
            rule_md_name="no-class-level-commitments",
            build_context=build_module_context,
            skill_root=_ROOT,
        )
    )
