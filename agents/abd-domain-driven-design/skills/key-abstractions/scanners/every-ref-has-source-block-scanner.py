#!/usr/bin/env python3
"""Scanner: every **Ref —** entry must have a non-empty fenced source block."""
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
)


class EveryRefHasSourceBlockScanner(ModuleFileScanner):
    rule = "every-ref-has-source-block"

    def check_artifact(self, parsed: ParsedModuleFile) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        fname = str(parsed.file_path or "unknown")

        for term in parsed.terms:
            if not term.refs:
                continue
            for ref in term.refs:
                if not ref.has_source_block:
                    violations.append(self._violation(
                        f"Ref '{ref.title}' under term '{term.name}' has no "
                        f"```source block",
                        fname,
                        ref.line_number,
                    ))
                elif ref.source_block_body is not None and ref.source_block_body.strip() == "":
                    violations.append(self._violation(
                        f"Ref '{ref.title}' under term '{term.name}' has an "
                        f"empty ```source block",
                        fname,
                        ref.line_number,
                    ))
        return violations


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            EveryRefHasSourceBlockScanner,
            rule_md_name="every-ref-has-source-block",
            build_context=build_module_context,
            skill_root=_ROOT,
        )
    )
