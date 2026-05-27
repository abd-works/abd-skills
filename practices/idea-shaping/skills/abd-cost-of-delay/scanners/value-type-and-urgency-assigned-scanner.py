#!/usr/bin/env python3
"""Scanner: value-type-and-urgency-assigned.

Checks every cost-of-delay canvas in --workspace for:
  1. Value Type is filled and is one of the four valid types
  2. Urgency Profile is filled and is one of the four valid profiles
  3. Rationale is present (not blank)
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent
_EXECUTE_RULES_SCRIPTS = _SKILL_ROOT.parent / "execute_using_rules" / "scripts"
if str(_EXECUTE_RULES_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_EXECUTE_RULES_SCRIPTS))
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from scanner_bases import Scanner, Violation, SimpleRule, ScanFilesContext, FileCollection  # noqa: E402
from scanner_runner import execute_scan_with_workspace  # noqa: E402
from md_tables import find_markdown_files, field_value  # noqa: E402

RULE_NAME = "value-type-and-urgency-assigned"
CANVAS_GLOB = "*canvas*.md"

VALID_VALUE_TYPES = {
    "increase revenue",
    "protect revenue",
    "reduce cost",
    "avoid cost",
}
VALID_URGENCY_PROFILES = {
    "expedite",
    "fixed date",
    "standard",
    "intangible",
}


def _is_option_placeholder(value: str, valid_set: set[str]) -> bool:
    """True if value is a slash-separated list of all valid options (template placeholder)."""
    parts = [p.strip().lower() for p in value.split("/")]
    return len(parts) > 1 and all(p in valid_set for p in parts)


class ValueTypeUrgencyScanner(Scanner):
    def scan_with_context(self, context: ScanFilesContext) -> list:
        violations: list[Violation] = []
        for fp in context.files.all_files:
            violations.extend(self._check_canvas(fp))
        return violations

    def _check_canvas(self, path: Path) -> list[Violation]:
        violations: list[Violation] = []
        lines = path.read_text(encoding="utf-8").splitlines()

        vt = field_value(lines, "Value Type")
        if not vt or vt.lower() == "tbd":
            violations.append(Violation(
                self.rule,
                f"Value Type is missing or TBD in {path.name}. "
                "Must be one of: Increase Revenue, Protect Revenue, Reduce Cost, Avoid Cost.",
                location=str(path),
            ))
        elif _is_option_placeholder(vt, VALID_VALUE_TYPES):
            pass  # template placeholder listing all options
        elif vt.lower() not in VALID_VALUE_TYPES:
            violations.append(Violation(
                self.rule,
                f"Value Type '{vt}' in {path.name} is not a recognized type. "
                "Must be one of: Increase Revenue, Protect Revenue, Reduce Cost, Avoid Cost.",
                location=str(path),
            ))

        up = field_value(lines, "Urgency Profile")
        if not up or up.lower() == "tbd":
            violations.append(Violation(
                self.rule,
                f"Urgency Profile is missing or TBD in {path.name}. "
                "Must be one of: Expedite, Fixed Date, Standard, Intangible.",
                location=str(path),
            ))
        elif _is_option_placeholder(up, VALID_URGENCY_PROFILES):
            pass  # template placeholder listing all options
        elif up.lower() not in VALID_URGENCY_PROFILES:
            violations.append(Violation(
                self.rule,
                f"Urgency Profile '{up}' in {path.name} is not a recognized profile. "
                "Must be one of: Expedite, Fixed Date, Standard, Intangible.",
                location=str(path),
            ))

        rationale = field_value(lines, "Rationale")
        if not rationale:
            has_filled_example = any("## example" in l.lower() for l in lines)
            if not has_filled_example:
                violations.append(Violation(
                    self.rule,
                    f"Rationale is blank in {path.name}. "
                    "Explain why this value type and urgency profile were chosen.",
                    location=str(path),
                ))

        return violations


def _build_context(workspace: Path) -> ScanFilesContext:
    canvases = find_markdown_files(workspace, CANVAS_GLOB)
    return ScanFilesContext(files=FileCollection(code_files=canvases))


if __name__ == "__main__":
    sys.exit(execute_scan_with_workspace(
        ValueTypeUrgencyScanner,
        RULE_NAME,
        _build_context,
        skill_root=_SKILL_ROOT,
    ))
