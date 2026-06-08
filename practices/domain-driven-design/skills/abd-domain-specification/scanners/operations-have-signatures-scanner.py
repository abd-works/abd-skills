#!/usr/bin/env python3
"""Scanner: every operation in Class Model blocks must have a typed signature with parentheses.

Finds lines in ### Class Model sections that start with + or - and appear to name an
operation (no colon = not a property, no parentheses = missing signature) and flags them
as prose-only operation lines that violate the typed-signature rule.
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

# Matches public/private member lines: + or - at start of line (possibly indented by a tab)
_MEMBER_LINE_RE = re.compile(r"^(\t?)([+\-])\s+(.+)$")
# Class Model section header
_OBJECT_MODEL_SECTION_RE = re.compile(r"^### Class Model\s*$", re.MULTILINE)
# Class block header (marks boundary of sections)
_CLASS_BLOCK_RE = re.compile(r"^#{2,3}\s", re.MULTILINE)
# Stereotype annotation prefix — properties like + << composition >> name: Type are valid
_STEREOTYPE_RE = re.compile(r"^<<\s*\w+")
# Initialisation note (not a member)
_INIT_RE = re.compile(r"^Initialisation\s*:")

# A line is an "operation" (must have parens) vs a property (has a colon-type after the name)
# Property pattern:  name: Type  or  << stereotype >> name: Type
# Operation pattern: name(...)   or  ClassName(...)  (constructors count)
# Constructor: starts with uppercase letter
_HAS_PAREN = re.compile(r"\(")
_HAS_COLON_TYPE = re.compile(r"^\S+\s*:")  # name: after stripping <<...>>
_IS_STEREOTYPE = re.compile(r"^<<")
_ENUM_VALUE_RE = re.compile(r"^[A-Z][A-Z0-9_]+$")  # ALL_CAPS enum constant


def _extract_object_model_ranges(content: str) -> List[tuple[int, int]]:
    """Return (start, end) byte ranges for each ### Class Model section."""
    ranges = []
    lines = content.split("\n")
    in_om = False
    start = 0
    pos = 0
    for i, line in enumerate(lines):
        if re.match(r"^### Class Model\s*$", line):
            in_om = True
            start = pos
        elif in_om and re.match(r"^#{2,3}\s", line) and not re.match(r"^### Class Model", line):
            ranges.append((start, pos))
            in_om = False
        pos += len(line) + 1  # +1 for newline
    if in_om:
        ranges.append((start, len(content)))
    return ranges


def _member_name_and_rest(member_text: str) -> tuple[str, str]:
    """Strip stereotype prefix and return (name_part, rest)."""
    text = member_text.strip()
    # Remove << stereotype >> prefix
    st = re.match(r"^<<[^>]+>>\s*", text)
    if st:
        text = text[st.end():]
    # name is first token
    parts = text.split(None, 1)
    name = parts[0] if parts else ""
    rest = parts[1] if len(parts) > 1 else ""
    return name, rest


class OperationsHaveSignaturesScanner(Scanner):
    """Flag operation lines in Class Model sections that lack typed signatures."""

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
        om_ranges = _extract_object_model_ranges(content)
        if not om_ranges:
            return violations

        # Build set of line indices that fall inside Class Model sections
        om_line_indices: set[int] = set()
        pos = 0
        for i, line in enumerate(lines):
            for start, end in om_ranges:
                if start <= pos < end:
                    om_line_indices.add(i)
                    break
            pos += len(line) + 1

        for i, line in enumerate(lines):
            if i not in om_line_indices:
                continue
            m = _MEMBER_LINE_RE.match(line)
            if not m:
                continue
            indent, sign, member_text = m.groups()
            # Skip Invariant/Interaction annotations (they're indented under a member)
            if indent:
                continue
            text = member_text.strip()
            # Skip Initialisation: notes
            if _INIT_RE.match(text):
                continue
            # Remove stereotype prefix for analysis
            st = re.match(r"^<<[^>]+>>\s*", text)
            if st:
                text_inner = text[st.end():]
            else:
                text_inner = text
            # Skip enum constants (ALL_CAPS with no space)
            first_token = text_inner.split()[0] if text_inner.split() else ""
            if _ENUM_VALUE_RE.match(first_token):
                continue
            # If it has `(`, it's a constructor or operation — fine
            if "(" in text_inner:
                continue
            # If it has `name: Type` pattern — it's a property — fine
            if re.match(r"^\S+\s*:", text_inner):
                continue
            # Remaining: a name with no parens and no colon = prose description
            line_num = i + 1
            violations.append(Violation(
                rule=self.rule,
                violation_message=(
                    f"Operation-like member '{text}' has no typed signature "
                    f"(missing parentheses and return type)"
                ),
                location=str(file_path),
                line_number=line_num,
                severity="error",
            ).to_dict())
        return violations


from object_model_context import build_object_model_context as _build_context  # noqa: E402


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            OperationsHaveSignaturesScanner,
            rule_md_name="operations-have-signatures",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
