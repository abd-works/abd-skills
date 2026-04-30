"""Shared base for OOAD markdown-artifact scanners.

Parses key-abstractions.md (and similar structured markdown) into a tree of
modules, key abstractions, and extracts so each rule scanner only needs to
implement _check(parsed) -> violations.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import sys

_ROOT = Path(__file__).resolve().parent.parent
_SKILLS = _ROOT.parent
for _p in (
    _SKILLS / "execute_using_rules" / "scripts",
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
# Regex patterns for OOAD markdown artifacts
# ---------------------------------------------------------------------------

MODULE_HEADING_RE = re.compile(
    r"^##\s+Module:\s*\[(?P<name>[^\]]+)\]", re.MULTILINE
)
KA_HEADING_RE = re.compile(
    r"^###?\s+Key Abstraction:\s*(?P<name>.+)$", re.MULTILINE
)
RESOLUTIONS_HEADING_RE = re.compile(
    r"^###?\s+Resolutions\s*$", re.MULTILINE
)
DEFERRED_TENSIONS_HEADING_RE = re.compile(
    r"^###?\s+Deferred tensions\s*$", re.MULTILINE
)
EXTRACT_HEADER_RE = re.compile(
    r"^\*\*Extract\s*—\s*(?P<title>.+?)\*\*\s*$", re.MULTILINE
)
SOURCE_LINE_RE = re.compile(r"^Source:\s*(?P<ref>.+)$", re.MULTILINE)
LOCATOR_LINE_RE = re.compile(r"^Locator:\s*(?P<loc>.+)$", re.MULTILINE)
EXTRACT_TYPE_RE = re.compile(r"^Extract:\s*(?P<type>\w+)", re.MULTILINE)
PART_LINE_RE = re.compile(r"^Part:\s*(?P<part>.+)$", re.MULTILINE)
REASON_LINE_RE = re.compile(r"^Reason:\s*(?P<reason>.+)$", re.MULTILINE)
INTENT_LINE_RE = re.compile(r"^Intent:\s*(?P<intent>.+)$", re.MULTILINE)
SHAPE_HINT_LINE_RE = re.compile(r"^Shape hint:\s*(?P<hint>.+)$", re.MULTILINE)
TENSION_LINE_RE = re.compile(r"^Tension:\s*(?P<tension>.+)$", re.MULTILINE)
CORE_TERMS_HEADER_RE = re.compile(
    r"^Core terms.*?:\s*$", re.MULTILINE
)
SOURCE_BLOCK_RE = re.compile(r"```source\s*\n(?P<body>.*?)```", re.DOTALL)

STEREOTYPE_RE = re.compile(r"<<\s*\w+\s*>>")
TYPED_PROPERTY_RE = re.compile(r":\s*(String|Int|Float|Boolean|List|Set|Map|Date|UUID)\b", re.IGNORECASE)
METHOD_SIG_RE = re.compile(r"\w+\s*\([^)]*\)\s*(?:->|:)\s*\w+")
CARDINALITY_RE = re.compile(r"(?:1\.\.\*|0\.\.\*|\*\.\.\*|1\.\.1|0\.\.1)")


# ---------------------------------------------------------------------------
# Parsed data classes
# ---------------------------------------------------------------------------

@dataclass
class ParsedExtract:
    title: str
    source_ref: Optional[str] = None
    locator: Optional[str] = None
    extract_type: Optional[str] = None  # "whole" or "partial"
    part: Optional[str] = None
    reason: Optional[str] = None
    body: Optional[str] = None
    line_number: int = 0
    raw_block: str = ""


@dataclass
class ParsedKeyAbstraction:
    name: str
    intent: Optional[str] = None
    core_terms: List[str] = field(default_factory=list)
    shape_hint: Optional[str] = None
    tension: Optional[str] = None
    extracts: List[ParsedExtract] = field(default_factory=list)
    line_number: int = 0
    raw_block: str = ""


@dataclass
class ParsedModule:
    name: str
    has_resolutions: bool = False
    resolutions_line: int = 0
    first_ka_line: int = 0
    key_abstractions: List[ParsedKeyAbstraction] = field(default_factory=list)
    line_number: int = 0
    raw_block: str = ""


@dataclass
class ParsedArtifact:
    """Top-level parse result for a key-abstractions.md file."""
    front_matter: str = ""
    modules: List[ParsedModule] = field(default_factory=list)
    flat_abstractions: List[ParsedKeyAbstraction] = field(default_factory=list)
    has_modules: bool = False
    file_path: Optional[Path] = None
    content: str = ""


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_key_abstractions(content: str, file_path: Optional[Path] = None) -> ParsedArtifact:
    """Parse key-abstractions.md into structured data."""
    artifact = ParsedArtifact(content=content, file_path=file_path)

    module_matches = list(MODULE_HEADING_RE.finditer(content))
    artifact.has_modules = len(module_matches) > 0

    if artifact.has_modules:
        for i, m_match in enumerate(module_matches):
            end = module_matches[i + 1].start() if i + 1 < len(module_matches) else len(content)
            module_block = content[m_match.start():end]
            module = _parse_module(m_match.group("name"), module_block, content, m_match.start())
            artifact.modules.append(module)
        artifact.front_matter = content[:module_matches[0].start()] if module_matches else ""
    else:
        ka_matches = list(KA_HEADING_RE.finditer(content))
        if ka_matches:
            artifact.front_matter = content[:ka_matches[0].start()]
        for i, ka_match in enumerate(ka_matches):
            end = ka_matches[i + 1].start() if i + 1 < len(ka_matches) else len(content)
            ka_block = content[ka_match.start():end]
            ka = _parse_key_abstraction(ka_match.group("name"), ka_block, content, ka_match.start())
            artifact.flat_abstractions.append(ka)

    return artifact


def _parse_module(name: str, block: str, full_content: str, offset: int) -> ParsedModule:
    module = ParsedModule(
        name=name,
        line_number=full_content[:offset].count("\n") + 1,
        raw_block=block,
    )

    res_match = RESOLUTIONS_HEADING_RE.search(block)
    if res_match:
        module.has_resolutions = True
        module.resolutions_line = full_content[:offset + res_match.start()].count("\n") + 1

    ka_matches = list(KA_HEADING_RE.finditer(block))
    if ka_matches:
        module.first_ka_line = full_content[:offset + ka_matches[0].start()].count("\n") + 1

    for i, ka_match in enumerate(ka_matches):
        end = ka_matches[i + 1].start() if i + 1 < len(ka_matches) else len(block)
        ka_block = block[ka_match.start():end]
        ka = _parse_key_abstraction(
            ka_match.group("name"), ka_block, full_content, offset + ka_match.start()
        )
        module.key_abstractions.append(ka)

    return module


def _parse_key_abstraction(name: str, block: str, full_content: str, offset: int) -> ParsedKeyAbstraction:
    ka = ParsedKeyAbstraction(
        name=name,
        line_number=full_content[:offset].count("\n") + 1,
        raw_block=block,
    )

    intent_m = INTENT_LINE_RE.search(block)
    if intent_m:
        ka.intent = intent_m.group("intent").strip()

    shape_m = SHAPE_HINT_LINE_RE.search(block)
    if shape_m:
        ka.shape_hint = shape_m.group("hint").strip()

    tension_m = TENSION_LINE_RE.search(block)
    if tension_m:
        ka.tension = tension_m.group("tension").strip()

    core_m = CORE_TERMS_HEADER_RE.search(block)
    if core_m:
        terms_start = core_m.end()
        terms_end = len(block)
        for stopper in (INTENT_LINE_RE, SHAPE_HINT_LINE_RE, TENSION_LINE_RE, EXTRACT_HEADER_RE):
            s = stopper.search(block, terms_start)
            if s and s.start() < terms_end:
                terms_end = s.start()
        terms_block = block[terms_start:terms_end]
        for line in terms_block.splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                ka.core_terms.append(stripped[2:].strip())

    extract_matches = list(EXTRACT_HEADER_RE.finditer(block))
    for i, ex_match in enumerate(extract_matches):
        ex_end = extract_matches[i + 1].start() if i + 1 < len(extract_matches) else len(block)
        ex_block = block[ex_match.start():ex_end]
        ext = _parse_extract(ex_match.group("title"), ex_block, full_content, offset + ex_match.start())
        ka.extracts.append(ext)

    return ka


def _parse_extract(title: str, block: str, full_content: str, offset: int) -> ParsedExtract:
    ext = ParsedExtract(
        title=title,
        line_number=full_content[:offset].count("\n") + 1,
        raw_block=block,
    )

    source_m = SOURCE_LINE_RE.search(block)
    if source_m:
        ext.source_ref = source_m.group("ref").strip()

    loc_m = LOCATOR_LINE_RE.search(block)
    if loc_m:
        ext.locator = loc_m.group("loc").strip()

    type_m = EXTRACT_TYPE_RE.search(block)
    if type_m:
        ext.extract_type = type_m.group("type").strip().lower()

    part_m = PART_LINE_RE.search(block)
    if part_m:
        ext.part = part_m.group("part").strip()

    reason_m = REASON_LINE_RE.search(block)
    if reason_m:
        ext.reason = reason_m.group("reason").strip()

    body_m = SOURCE_BLOCK_RE.search(block)
    if body_m:
        ext.body = body_m.group("body")

    return ext


# ---------------------------------------------------------------------------
# Base scanner class
# ---------------------------------------------------------------------------

class MarkdownArtifactScanner(Scanner):
    """Base class for scanners that validate a parsed OOAD markdown artifact.

    Subclasses override `check_artifact(parsed)` to return violations.
    """

    ARTIFACT_FILENAME = "key-abstractions.md"
    ARTIFACT_SUBDIR = "abd-ooad"

    def scan_with_context(self, context: ScanFilesContext) -> List[Dict[str, Any]]:
        violations: List[Dict[str, Any]] = []
        all_files = context.files.all_files
        for fp in all_files:
            if fp and fp.exists() and fp.is_file():
                violations.extend(self._scan_file(fp))
        return violations

    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        content = file_path.read_text(encoding="utf-8")
        parsed = parse_key_abstractions(content, file_path)
        return self.check_artifact(parsed)

    def check_artifact(self, parsed: ParsedArtifact) -> List[Dict[str, Any]]:
        """Override in subclass to implement rule-specific checks."""
        return []

    def _violation(self, message: str, location: str, line: int = 0, severity: str = "error") -> Dict[str, Any]:
        return Violation(
            rule=self.rule,
            violation_message=message,
            location=location,
            line_number=line,
            severity=severity,
        ).to_dict()


def build_ka_context(workspace: Path) -> ScanFilesContext:
    """Standard context builder for key-abstractions.md scanners."""
    ka = workspace / "abd-ooad" / "key-abstractions.md"
    files = FileCollection(code_files=[ka] if ka.is_file() else [])
    return ScanFilesContext(files=files)
