"""Shared base for key-abstractions enrichment scanners.

Parses a module file (e.g. check-resolution.md) that has been enriched with
verbatim source blocks. Extracts the state marker, term headings, ref entries,
and source blocks so each rule scanner only needs to implement
check_artifact(parsed) -> violations.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import sys

_ROOT = Path(__file__).resolve().parent.parent
_REPO = _ROOT.parent.parent.parent.parent  # agents/abd-domain-driven-design/skills/<skill> -> repo root
for _p in (
    _REPO / "skills" / "execute-skill-using-skills-rules" / "scripts",
    _ROOT / "scanners",
):
    s = str(_p)
    if s not in sys.path:
        sys.path.insert(0, s)

from scanner_bases import Scanner, Violation  # noqa: E402
from scanner_bases.resources.scan_context import (  # noqa: E402
    FileCollection,
    ScanFilesContext,
)

# ---------------------------------------------------------------------------
# Regex patterns for enrichment-model module files
# ---------------------------------------------------------------------------

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
STATE_LINE_RE = re.compile(r"^state:\s*(.+)$", re.MULTILINE)

CORE_TERMS_SECTION_RE = re.compile(r"^## Core terms\s*$", re.MULTILINE)
BOUNDARY_TERMS_SECTION_RE = re.compile(r"^## Boundary terms\s*$", re.MULTILINE)

H3_HEADING_RE = re.compile(r"^### (.+)$", re.MULTILINE)
H4_HEADING_RE = re.compile(r"^#### (.+)$", re.MULTILINE)
KA_SECTION_RE = re.compile(r"^## Key Abstractions\s*$", re.MULTILINE)

REF_HEADER_RE = re.compile(
    r"^\*\*Ref\s*—\s*(?P<title>.+?)\*\*\s*$", re.MULTILINE
)
SOURCE_LINE_RE = re.compile(r"^Source:\s*(?P<ref>.+)$", re.MULTILINE)
LOCATOR_LINE_RE = re.compile(r"^Locator:\s*(?P<loc>.+)$", re.MULTILINE)
EXTRACT_TYPE_RE = re.compile(r"^Extract:\s*(?P<type>\w+)", re.MULTILINE)
PART_LINE_RE = re.compile(r"^Part:\s*(?P<part>.+)$", re.MULTILINE)

SOURCE_BLOCK_RE = re.compile(r"```source\s*\n(?P<body>.*?)```", re.DOTALL)

OWNED_BY_RE = re.compile(r"^Owned by:\s*(?P<owner>.+)$", re.MULTILINE)

# Jargon patterns from old identification model
INTENT_LINE_RE = re.compile(r"^Intent:\s*", re.MULTILINE)
SHAPE_HINT_LINE_RE = re.compile(r"^Shape hint:\s*", re.MULTILINE)
TENSION_LINE_RE = re.compile(r"^Tension:\s*", re.MULTILINE)
CORE_TERMS_ABSORBED_RE = re.compile(r"^Core terms \(absorbed", re.MULTILINE)
KA_HEADING_RE = re.compile(r"^###?\s+Key Abstraction:\s*", re.MULTILINE)

# Class-level commitment patterns
STEREOTYPE_RE = re.compile(r"<<\s*\w+\s*>>")
TYPED_PROPERTY_RE = re.compile(
    r":\s*(String|Int|Float|Boolean|List|Set|Map|Date|UUID)\b", re.IGNORECASE
)
METHOD_SIG_RE = re.compile(r"[a-z]\w*\s*\([^)]*\)\s*->\s*\w+")
CARDINALITY_RE = re.compile(r"(?:1\.\.\*|0\.\.\*|\*\.\.\*|1\.\.1|0\.\.1)")


# ---------------------------------------------------------------------------
# Parsed data classes
# ---------------------------------------------------------------------------

@dataclass
class ParsedRef:
    title: str
    source_ref: Optional[str] = None
    locator: Optional[str] = None
    extract_type: Optional[str] = None
    part: Optional[str] = None
    has_source_block: bool = False
    source_block_body: Optional[str] = None
    line_number: int = 0
    raw_block: str = ""


@dataclass
class ParsedTerm:
    name: str
    behavioral_lines: List[str] = field(default_factory=list)
    refs: List[ParsedRef] = field(default_factory=list)
    owned_by: Optional[str] = None
    is_boundary: bool = False
    line_number: int = 0
    raw_block: str = ""


@dataclass
class ParsedModuleFile:
    state: Optional[str] = None
    terms: List[ParsedTerm] = field(default_factory=list)
    file_path: Optional[Path] = None
    content: str = ""


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_module_file(content: str, file_path: Optional[Path] = None) -> ParsedModuleFile:
    parsed = ParsedModuleFile(content=content, file_path=file_path)

    fm = FRONT_MATTER_RE.match(content)
    if fm:
        state_m = STATE_LINE_RE.search(fm.group(1))
        if state_m:
            parsed.state = state_m.group(1).strip()

    boundary_start = None
    boundary_m = BOUNDARY_TERMS_SECTION_RE.search(content)
    if boundary_m:
        boundary_start = boundary_m.start()

    ka_section_start = None
    ka_m = KA_SECTION_RE.search(content)
    if ka_m:
        ka_section_start = ka_m.start()

    term_headings: List[re.Match] = []

    if ka_section_start is not None:
        ka_end = boundary_start if boundary_start is not None else len(content)
        for m in H4_HEADING_RE.finditer(content):
            if ka_section_start < m.start() < ka_end:
                term_headings.append(m)

    if boundary_start is not None:
        for m in H3_HEADING_RE.finditer(content):
            if m.start() > boundary_start:
                term_headings.append(m)

    term_headings.sort(key=lambda m: m.start())

    for i, h in enumerate(term_headings):
        end = term_headings[i + 1].start() if i + 1 < len(term_headings) else len(content)
        block = content[h.start():end]
        line_num = content[:h.start()].count("\n") + 1

        term = ParsedTerm(
            name=h.group(1).strip(),
            line_number=line_num,
            raw_block=block,
        )

        if boundary_start is not None and h.start() > boundary_start:
            term.is_boundary = True
            owned_m = OWNED_BY_RE.search(block)
            if owned_m:
                term.owned_by = owned_m.group("owner").strip()

        for line in block.splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                term.behavioral_lines.append(stripped)

        ref_matches = list(REF_HEADER_RE.finditer(block))
        for j, ref_m in enumerate(ref_matches):
            ref_end = ref_matches[j + 1].start() if j + 1 < len(ref_matches) else len(block)
            ref_block = block[ref_m.start():ref_end]
            ref_line = content[:h.start() + ref_m.start()].count("\n") + 1

            ref = ParsedRef(
                title=ref_m.group("title").strip(),
                line_number=ref_line,
                raw_block=ref_block,
            )

            src_m = SOURCE_LINE_RE.search(ref_block)
            if src_m:
                ref.source_ref = src_m.group("ref").strip()

            loc_m = LOCATOR_LINE_RE.search(ref_block)
            if loc_m:
                ref.locator = loc_m.group("loc").strip()

            type_m = EXTRACT_TYPE_RE.search(ref_block)
            if type_m:
                ref.extract_type = type_m.group("type").strip().lower()

            part_m = PART_LINE_RE.search(ref_block)
            if part_m:
                ref.part = part_m.group("part").strip()

            body_m = SOURCE_BLOCK_RE.search(ref_block)
            if body_m:
                ref.has_source_block = True
                ref.source_block_body = body_m.group("body")

            term.refs.append(ref)

        parsed.terms.append(term)

    return parsed


# ---------------------------------------------------------------------------
# Base scanner class
# ---------------------------------------------------------------------------

class ModuleFileScanner(Scanner):
    """Base class for scanners that validate an enriched module file."""

    def __init__(self, rule=None):
        super().__init__(rule or self.__class__.__name__)

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        all_files = context.files.all_files
        for fp in all_files:
            if fp and fp.exists() and fp.is_file():
                violations.extend(self._scan_file(fp))
        return violations

    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        content = file_path.read_text(encoding="utf-8")
        parsed = parse_module_file(content, file_path)
        return self.check_artifact(parsed)

    def check_artifact(self, parsed: ParsedModuleFile) -> List[Dict[str, Any]]:
        return []

    def _violation(self, message: str, location: str, line: int = 0, severity: str = "error") -> Dict[str, Any]:
        return Violation(
            rule=self.rule,
            violation_message=message,
            location=location,
            line_number=line,
            severity=severity,
        ).to_dict()


def build_module_context(workspace: Path, module_dir: str = "abd-domain-driven-design/modules") -> ScanFilesContext:
    """Build context from all module files that are at state: key-abstractions."""
    modules_path = workspace / module_dir
    files: List[Path] = []
    if modules_path.is_dir():
        for md in modules_path.glob("*.md"):
            text = md.read_text(encoding="utf-8")
            if "state: key-abstractions" in text[:200]:
                files.append(md)
    return ScanFilesContext(files=FileCollection(code_files=files))
