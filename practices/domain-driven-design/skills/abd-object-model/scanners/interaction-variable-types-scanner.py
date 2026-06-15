#!/usr/bin/env python3
"""Scanner: every variable assignment inside an Interaction: block must carry a type annotation.

Inside an Interaction: block, variable lines must follow the form:
    varName: Type = expression
Lines that use a plain assignment (varName = expression) without a type are a violation.
Lines that are control-flow keywords (if, return, super, for, while) are skipped.
"""
from __future__ import annotations

import re
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
from scanner_bases import Scanner, Violation  # noqa: E402
from scanner_bases.resources.scan_context import (  # noqa: E402
    FileCollection,
    ScanFilesContext,
)

# Interaction: block start (tab-indented under an operation)
_INTERACTION_RE = re.compile(r"^\t\s*Interaction\s*:\s*$", re.IGNORECASE)
# Assignment line inside an interaction block (double-tab indented)
# Has = but split to detect whether it has `: Type` before the =
_ASSIGNMENT_RE = re.compile(r"^(\t{2,})(\w[\w.]*)(\s*)=\s*.+$")
# Typed assignment: varName: Type = ...  (has colon before the =)
_TYPED_ASSIGNMENT_RE = re.compile(r"^(\t{2,})(\w[\w.]*)\s*:\s*\S+.*=\s*.+$")
# Control-flow prefixes to skip
_CONTROL_FLOW_RE = re.compile(
    r"^\t{2,}\s*(return|if|else|for|while|super|switch|break|continue)\b",
    re.IGNORECASE,
)
# Object Model section
_MEMBER_RE = re.compile(r"^[+\-]\s+\S")


def _find_object_model_sections(lines: List[str]) -> List[tuple[int, int]]:
    sections = []
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^### Object Model\s*$", line):
            start = i
        elif start is not None and re.match(r"^#{2,3}\s", line) and not re.match(r"^### Object Model", line):
            sections.append((start, i))
            start = None
    if start is not None:
        sections.append((start, len(lines)))
    return sections


class InteractionVariableTypesScanner(Scanner):
    """Flag Interaction: variable lines that lack type annotations (varName = expr instead of varName: Type = expr)."""

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        for fp in context.files.all_files:
            if fp and fp.is_file():
                violations.extend(self._scan_file(fp))
        return violations

    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        om_sections = _find_object_model_sections(lines)

        om_set: set[int] = set()
        for start, end in om_sections:
            om_set.update(range(start, end))

        i = 0
        while i < len(lines):
            if i not in om_set:
                i += 1
                continue
            line = lines[i]
            if _INTERACTION_RE.match(line):
                # Scan the interaction block
                i += 1
                while i < len(lines) and i in om_set:
                    inner = lines[i]
                    # Interaction block ends when indentation drops
                    if not inner.startswith("\t\t") and inner.strip() != "":
                        break
                    if _CONTROL_FLOW_RE.match(inner):
                        i += 1
                        continue
                    if _ASSIGNMENT_RE.match(inner) and not _TYPED_ASSIGNMENT_RE.match(inner):
                        m = _ASSIGNMENT_RE.match(inner)
                        var_name = m.group(2) if m else "?"
                        violations.append(Violation(
                            rule=self.rule,
                            violation_message=(
                                f"Interaction variable '{var_name}' has no type annotation "
                                f"(write '{var_name}: Type = ...' not '{var_name} = ...')"
                            ),
                            location=str(file_path),
                            line_number=i + 1,
                            severity="error",
                        ).to_dict())
                    i += 1
            else:
                i += 1
        return violations


from object_model_context import build_object_model_context as _build_context  # noqa: E402


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            InteractionVariableTypesScanner,
            rule_md_name="interaction-uses-domain-language",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
