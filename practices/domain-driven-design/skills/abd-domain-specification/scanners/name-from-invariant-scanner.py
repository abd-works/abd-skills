#!/usr/bin/env python3
"""Scanner: private operations must not use generic verb names.

When the right name for a private operation is unclear, it should be named after its
invariant — not invented with a vague process verb. This scanner flags private
operations (lines starting with - methodName() in domain specification class blocks) whose names
begin with generic verbs like handle, apply, process, manage, check, do, or execute.
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

# Private operation: starts with - and has parentheses
_PRIVATE_OP_RE = re.compile(r"^-\s+(\w+)\s*\(")
# Generic verbs that indicate the operation name was not derived from its invariant.
_GENERIC_VERBS = frozenset([
    "handle", "apply", "process", "manage", "check",
    "do", "execute",
])


def _first_verb(method_name: str) -> str:
    """Extract the leading verb from a camelCase method name."""
    parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)", method_name)
    return parts[0].lower() if parts else method_name.lower()


class NameFromInvariantScanner(Scanner):
    """Flag private operations whose names use generic verbs instead of domain invariant terms."""

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
        scannable = domain_spec_scannable_line_indices(lines)

        for i, line in enumerate(lines):
            if i not in scannable:
                continue
            m = _PRIVATE_OP_RE.match(line)
            if not m:
                continue
            method_name = m.group(1)
            verb = _first_verb(method_name)
            if verb in _GENERIC_VERBS:
                violations.append(Violation(
                    rule=self.rule,
                    violation_message=(
                        f"Private operation '{method_name}' starts with generic verb '{verb}' — "
                        f"name should come from the invariant, not a vague process word"
                    ),
                    location=str(file_path),
                    line_number=i + 1,
                    severity="warning",
                ).to_dict())
        return violations


from object_model_context import (  # noqa: E402
    build_object_model_context as _build_context,
    domain_spec_scannable_line_indices,
)


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            NameFromInvariantScanner,
            rule_md_name="name-from-invariant",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
