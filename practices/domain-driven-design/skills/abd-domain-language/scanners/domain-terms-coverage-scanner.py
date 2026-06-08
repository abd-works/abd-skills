#!/usr/bin/env python3
"""Scanner: every term in the **Terms** list must have a ### concept heading in Core Domain.

Also flags obvious un-italicized domain term occurrences by checking that terms
extracted from the Terms list are italicized whenever they appear in bullet lines.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

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
from scanner_bases.resources.scan_context import FileCollection, ScanFilesContext  # noqa: E402

_TERMS_HEADING_RE = re.compile(r"^\*\*Terms\*\*\s*:", re.IGNORECASE)
_CORE_DOMAIN_RE = re.compile(r"^# Core Domain\s*$")
_BOUNDARY_DOMAIN_RE = re.compile(r"^# Boundary Domain\s*$")
_MODULE_RE = re.compile(r"^# Module")
# Indented term bullet: "  - **term_name**"
_TERM_BULLET_RE = re.compile(r"^ {2,}- \*\*([^*]+)\*\*")
# Concept / subtype / property heading: ### anything
_CONCEPT_HEADING_RE = re.compile(r"^### (.+)$")
# Bullet line
_BULLET_RE = re.compile(r"^ *- ")
# Italicized term: *term*
_ITALIC_RE = re.compile(r"\*([^*]+)\*")


def _extract_terms(lines: List[str], terms_start: int, core_start: int) -> List[tuple[str, int]]:
    """Return (term_name, line_number) for every indented term bullet in the Terms block."""
    terms = []
    for i in range(terms_start + 1, core_start):
        m = _TERM_BULLET_RE.match(lines[i])
        if m:
            raw = m.group(1).strip().lower()
            # Strip parenthetical suffixes like *(property of check)*
            raw = re.sub(r"\s*\*\(.*?\)\*", "", raw).strip()
            terms.append((raw, i + 1))
    return terms


def _extract_concept_headings(lines: List[str], core_start: int, end: int) -> Set[str]:
    """Return normalised set of all ### headings under Core Domain."""
    headings: Set[str] = set()
    for i in range(core_start, end):
        m = _CONCEPT_HEADING_RE.match(lines[i])
        if m:
            raw = m.group(1).strip().lower()
            # Strip subtype suffix: "opposed check *is a type of* check" → "opposed check"
            raw = re.split(r"\s+\*is a type of\*", raw)[0].strip()
            # Strip *(boundary)* suffix
            raw = re.sub(r"\s*\*(boundary|owned by[^)]*)\*", "", raw).strip()
            headings.add(raw)
    return headings


class DomainTermsCoverageScanner(Scanner):

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        for fp in context.files.all_files:
            if fp and fp.is_file():
                violations.extend(self._scan_file(fp))
        return violations

    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        lines = file_path.read_text(encoding="utf-8").split("\n")

        module_starts = [i for i, l in enumerate(lines) if _MODULE_RE.match(l)]
        if not module_starts:
            module_starts = [0]

        for mod_idx, mod_start in enumerate(module_starts):
            next_module = module_starts[mod_idx + 1] if mod_idx + 1 < len(module_starts) else len(lines)

            terms_start = -1
            core_start = -1
            boundary_start = -1

            for i in range(mod_start, next_module):
                if _TERMS_HEADING_RE.match(lines[i]) and terms_start == -1:
                    terms_start = i
                if _CORE_DOMAIN_RE.match(lines[i]) and core_start == -1:
                    core_start = i
                if _BOUNDARY_DOMAIN_RE.match(lines[i]) and boundary_start == -1:
                    boundary_start = i

            if terms_start == -1 or core_start == -1:
                continue

            core_end = boundary_start if boundary_start != -1 else next_module
            terms = _extract_terms(lines, terms_start, core_start)
            headings = _extract_concept_headings(lines, core_start, core_end)

            for term_name, line_num in terms:
                if term_name not in headings:
                    # Allow partial match (e.g. "difficulty class (dc)" matches "difficulty class (dc)")
                    base = re.sub(r"\s*\([^)]*\)", "", term_name).strip()
                    matched = any(
                        h == term_name or h.startswith(base) or base in h
                        for h in headings
                    )
                    if not matched:
                        violations.append(Violation(
                            rule=self.rule,
                            violation_message=(
                                f"Term '{term_name}' is in the Terms list but has no "
                                f"### concept block in Core Domain"
                            ),
                            location=str(file_path),
                            line_number=line_num,
                            severity="error",
                        ).to_dict())

            # Check italicization: for each term, flag bullet lines where the plain
            # (non-italicized) term appears but the italicized form does not
            for term_name, _ in terms:
                base = re.sub(r"\s*\([^)]*\)", "", term_name).strip()
                if len(base) < 4:
                    continue  # skip very short terms (too noisy)
                for i in range(core_start, core_end):
                    line = lines[i]
                    if not _BULLET_RE.match(line):
                        continue
                    italicized = {m.group(1).lower() for m in _ITALIC_RE.finditer(line)}
                    plain = line.lower()
                    if base in plain and base not in italicized:
                        violations.append(Violation(
                            rule=self.rule,
                            violation_message=(
                                f"Term '{base}' appears un-italicized in bullet: "
                                f"'{line.strip()[:80]}'"
                            ),
                            location=str(file_path),
                            line_number=i + 1,
                            severity="warning",
                        ).to_dict())

        return violations


def _build_context(workspace: Path) -> ScanFilesContext:
    files: List[Path] = []
    for search_path in (workspace / "modules", workspace):
        if search_path.is_dir():
            for md in sorted(search_path.glob("*domain-language.md")):
                text = md.read_text(encoding="utf-8")
                if "state: domain-language" in text[:300]:
                    files.append(md)
            if files:
                break
    return ScanFilesContext(files=FileCollection(code_files=files))


if __name__ == "__main__":
    sys.exit(
        execute_scan_with_workspace(
            DomainTermsCoverageScanner,
            rule_md_name="domain-terms-italicized-in-prose-and-bullets",
            build_context=_build_context,
            skill_root=_ROOT,
        )
    )
