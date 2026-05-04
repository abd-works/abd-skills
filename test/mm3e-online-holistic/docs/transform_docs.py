"""
Transform DDD module documentation files to match new template format.

Handles three file types per module:
  - *-domain-language.md  (DL)
  - *-key-abstractions.md (KA)
  - *-domain-sketch.md    (DS)

Usage: python transform_docs.py [--dry-run] [module ...]
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

DOCS_ROOT = Path(__file__).parent
MODULES = [
    "advantage",
    "character-construction",
    "combat",
    "equipment",
    "power",
    "skill",
]

# ============================================================
# Source-block tracking
# ============================================================

def track_source_blocks(lines: List[str]) -> List[bool]:
    """Return True for each line that is inside a fenced code block."""
    inside = []
    in_src = False
    for line in lines:
        if line.strip().startswith("```"):
            in_src = not in_src
            inside.append(True)   # fence line treated as "inside"
        else:
            inside.append(in_src)
    return inside


# ============================================================
# Domain Language transformation
# ============================================================

def transform_domain_language(text: str) -> str:
    lines = text.split("\n")
    src = track_source_blocks(lines)
    out: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if src[i]:
            out.append(line)
            i += 1
            continue

        # ## Module: → # Module:
        if re.match(r"^## Module:", line):
            out.append("# " + line[3:])
            i += 1
            continue

        # ### term_name → #### **term_name** (if followed by #### Domain language)
        if re.match(r"^### ", line):
            term_name = line[4:].strip()
            j = i + 1
            while j < len(lines) and not src[j] and lines[j].strip() == "":
                j += 1
            if j < len(lines) and not src[j] and re.match(r"^#### Domain [Ll]anguage\s*$", lines[j]):
                out.append(f"#### **{term_name}**")
                i = j + 1  # skip ### line + blanks + #### Domain language
                continue
            out.append(line)
            i += 1
            continue

        # ## boundary_term + Owned by: → #### **term** *(owned by: Module)*
        if re.match(r"^## ", line):
            heading = line[3:].strip()
            if heading in ("Core Domain", "Boundary Domain", "Domain logic"):
                out.append(line)
                i += 1
                continue
            j = i + 1
            while j < len(lines) and not src[j] and lines[j].strip() == "":
                j += 1
            if j < len(lines) and not src[j] and re.match(r"^Owned by:", lines[j].strip()):
                module_name = lines[j].strip()[len("Owned by:"):].strip()
                out.append(f"#### **{heading}** *(owned by: {module_name})*")
                i = j + 1
                continue
            out.append(line)
            i += 1
            continue

        # Drop any #### Domain Language heading not already consumed (e.g., in Boundary Domain)
        if re.match(r"^#### Domain [Ll]anguage\s*$", line):
            i += 1
            continue

        out.append(line)
        i += 1

    result = "\n".join(out)
    result = remove_intra_section_separators_dl(result)
    return result


def remove_intra_section_separators_dl(text: str) -> str:
    """Keep only structural --- separators (before # Boundary Domain)."""
    lines = text.split("\n")
    src = track_source_blocks(lines)
    out: List[str] = []
    i = 0
    fm_count = 0
    fm_done = False

    while i < len(lines):
        line = lines[i]

        if src[i]:
            out.append(line)
            i += 1
            continue

        if line.strip() == "---" and not fm_done:
            fm_count += 1
            out.append(line)
            if fm_count == 2:
                fm_done = True
            i += 1
            continue

        if line.strip() == "---" and fm_done:
            j = i + 1
            while j < len(lines) and not src[j] and lines[j].strip() == "":
                j += 1
            next_line = lines[j].strip() if j < len(lines) else ""
            if re.match(r"^# (Boundary|Core) Domain", next_line):
                out.append(line)
            # else: drop (inter-term separator)
            i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


# ============================================================
# Key Abstractions transformation
# ============================================================

def transform_key_abstractions(text: str) -> str:
    lines = text.split("\n")
    src = track_source_blocks(lines)
    has_ka_header = any(
        not src[i] and re.match(r"^## Key Abstractions\s*$", lines[i])
        for i in range(len(lines))
    )
    if has_ka_header:
        return transform_ka_advantage_style(text)
    return transform_ka_ability_style(text)


def transform_ka_ability_style(text: str) -> str:
    """KAs at ##, terms at ### with #### Domain language."""
    lines = text.split("\n")
    src = track_source_blocks(lines)
    out: List[str] = []
    i = 0
    fm_count = 0
    fm_done = False

    while i < len(lines):
        line = lines[i]

        if src[i]:
            out.append(line)
            i += 1
            continue

        if line.strip() == "---" and not fm_done:
            fm_count += 1
            out.append(line)
            if fm_count == 2:
                fm_done = True
            i += 1
            continue

        if re.match(r"^## Module:", line):
            out.append("# " + line[3:])
            i += 1
            continue

        if re.match(r"^## ", line) and fm_done:
            heading = line[3:].strip()
            if heading in ("Core Domain", "Boundary Domain", "Domain logic"):
                out.append(line)
                i += 1
                continue
            j = i + 1
            while j < len(lines) and not src[j] and lines[j].strip() == "":
                j += 1
            if j < len(lines) and not src[j] and re.match(r"^Owned by:", lines[j].strip()):
                module_name = lines[j].strip()[len("Owned by:"):].strip()
                clean = heading.strip("*")
                out.append(f"#### **{clean}** *(owned by: {module_name})*")
                i = j + 1
                continue
            # Always strip existing bold markers and re-add exactly one pair (idempotent)
            clean = heading.strip("*")
            out.append(f"## **{clean}**")
            i += 1
            continue

        if re.match(r"^### ", line) and fm_done:
            term_name = line[4:].strip()
            j = i + 1
            while j < len(lines) and not src[j] and lines[j].strip() == "":
                j += 1
            if j < len(lines) and not src[j] and re.match(r"^#### Domain [Ll]anguage\s*$", lines[j]):
                clean = term_name.strip("*")
                out.append(f"#### **{clean}**")
                i = j + 1
                continue
            out.append(line)
            i += 1
            continue

        if re.match(r"^#### Decisions made\s*$", line) and fm_done:
            out.append("### Decisions made")
            i += 1
            continue

        # Drop any #### Domain Language heading not already consumed (e.g., in Boundary Domain)
        if re.match(r"^#### Domain [Ll]anguage\s*$", line) and fm_done:
            i += 1
            continue

        out.append(line)
        i += 1

    result = "\n".join(out)
    result = _fix_double_bold(result)
    result = _deduplicate_ul_headings(result)
    result = _insert_ul_after_ka_prose(result)
    result = _move_ka_decisions_after_terms(result)
    result = _remove_intra_ka_separators(result)
    result = _ensure_boundary_ul(result)
    return result


def transform_ka_advantage_style(text: str) -> str:
    """## Key Abstractions grouper, KAs at ###, terms at ####."""
    lines = text.split("\n")
    src = track_source_blocks(lines)
    out: List[str] = []
    i = 0
    fm_count = 0
    fm_done = False
    in_ka = False
    ul_inserted = False

    while i < len(lines):
        line = lines[i]

        if src[i]:
            out.append(line)
            i += 1
            continue

        if line.strip() == "---" and not fm_done:
            fm_count += 1
            out.append(line)
            if fm_count == 2:
                fm_done = True
            i += 1
            continue

        if re.match(r"^## Module:", line):
            out.append("# " + line[3:])
            i += 1
            continue

        if re.match(r"^## Key Abstractions\s*$", line):
            i += 1
            continue

        if re.match(r"^### ", line) and fm_done:
            ka_name = line[4:].strip()
            out.append(f"## **{ka_name}**")
            in_ka = True
            ul_inserted = False
            i += 1
            continue

        if re.match(r"^## ", line) and fm_done:
            heading = line[3:].strip()
            # Treat any boundary section marker as a section break (disable in_ka)
            heading_clean = heading.strip("*")
            if heading_clean in ("Core Domain", "Boundary Domain", "Domain logic") or \
               re.search(r"\bBoundary\b", heading_clean, re.IGNORECASE):
                out.append(line)
                in_ka = False
                i += 1
                continue
            j = i + 1
            while j < len(lines) and not src[j] and lines[j].strip() == "":
                j += 1
            if j < len(lines) and not src[j] and re.match(r"^Owned by:", lines[j].strip()):
                module_name = lines[j].strip()[len("Owned by:"):].strip()
                clean = heading.strip("*")
                out.append(f"#### **{clean}** *(owned by: {module_name})*")
                i = j + 1
                continue
            out.append(line)
            i += 1
            continue

        if re.match(r"^#### Decisions made", line) and fm_done:
            out.append("### Decisions made")
            i += 1
            continue

        if re.match(r"^#### ", line) and fm_done and in_ka:
            term_name = line[5:].strip()
            if term_name in ("Domain Sketch", "References"):
                out.append(line)
                i += 1
                continue
            if not ul_inserted:
                out.append("")
                out.append("### Ubiquitous Language")
                out.append("")
                ul_inserted = True
            # Idempotent: strip existing bold before adding
            clean = term_name.strip("*")
            out.append(f"#### **{clean}**")
            i += 1
            continue

        # Skip already-present ### Ubiquitous Language (idempotent)
        if re.match(r"^### Ubiquitous Language\s*$", line) and fm_done and in_ka:
            ul_inserted = True
            out.append(line)
            i += 1
            continue

        # Insert #### References before inline **Ref blocks (advantage-style KA files)
        if (not src[i] and line.strip().startswith("**Ref") and fm_done and in_ka and ul_inserted):
            # Check if previous non-blank output was #### References
            j = len(out) - 1
            while j >= 0 and out[j].strip() == "":
                j -= 1
            prev = out[j].strip() if j >= 0 else ""
            if not re.match(r"^#### References\s*$", prev):
                out.append("")
                out.append("#### References")
                out.append("")

        out.append(line)
        i += 1

    result = "\n".join(out)
    result = _fix_double_bold(result)
    result = _deduplicate_ul_headings(result)
    result = _move_ka_decisions_after_terms(result)
    result = _remove_intra_ka_separators(result)
    result = _ensure_boundary_ul(result)
    return result


def _fix_double_bold(text: str) -> str:
    """Fix any triple-or-more asterisk bold markers in heading lines (idempotency cleanup)."""
    lines = text.split("\n")
    src = track_source_blocks(lines)
    out: List[str] = []
    for i, line in enumerate(lines):
        if not src[i] and re.match(r"^#{1,6} ", line):
            # Replace any ***...*** or more with **...**
            fixed = re.sub(r"\*{3,}(.+?)\*{3,}", r"**\1**", line)
            out.append(fixed)
        else:
            out.append(line)
    return "\n".join(out)


def _deduplicate_ul_headings(text: str) -> str:
    """Remove consecutive duplicate ### Ubiquitous Language headings (idempotency fix)."""
    lines = text.split("\n")
    src = track_source_blocks(lines)
    out: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if not src[i] and re.match(r"^### Ubiquitous Language\s*$", line):
            out.append(line)
            i += 1
            # Absorb trailing blanks
            while i < len(lines) and not src[i] and lines[i].strip() == "":
                out.append(lines[i])
                i += 1
            # Skip any immediately following duplicate ### Ubiquitous Language + blanks
            while i < len(lines) and not src[i] and re.match(r"^### Ubiquitous Language\s*$", lines[i]):
                i += 1
                while i < len(lines) and not src[i] and lines[i].strip() == "":
                    i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def _insert_ul_after_ka_prose(text: str) -> str:
    """Insert ### Ubiquitous Language before first #### **term** after each ## **KA**."""
    lines = text.split("\n")
    src = track_source_blocks(lines)
    out: List[str] = []
    i = 0
    after_ka = False

    while i < len(lines):
        line = lines[i]

        if src[i]:
            out.append(line)
            i += 1
            continue

        if re.match(r"^## \*\*.+\*\*\s*$", line):
            out.append(line)
            after_ka = True
            i += 1
            continue

        if after_ka and re.match(r"^### Ubiquitous Language\s*$", line):
            # Already has UL heading — don't insert another
            after_ka = False
            out.append(line)
            i += 1
            continue

        if after_ka and re.match(r"^#### \*\*.+\*\*", line):
            out.append("")
            out.append("### Ubiquitous Language")
            out.append("")
            after_ka = False
            out.append(line)
            i += 1
            continue

        if after_ka and not src[i] and re.match(r"^(## |# )", line):
            after_ka = False

        out.append(line)
        i += 1

    return "\n".join(out)


def _move_ka_decisions_after_terms(text: str) -> str:
    """
    Move ### Decisions made that appears BEFORE any #### **term** in a KA to
    AFTER the last #### References in that KA.
    """
    lines = text.split("\n")
    src = track_source_blocks(lines)
    out: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if src[i] or not re.match(r"^## \*\*.+\*\*\s*$", line):
            out.append(line)
            i += 1
            continue

        # Collect entire KA block
        ka_start = i
        ka_end = len(lines)
        for j in range(i + 1, len(lines)):
            if not src[j] and (re.match(r"^## \*\*", lines[j]) or
                               re.match(r"^# (Core|Boundary) Domain", lines[j])):
                ka_end = j
                break

        ka_lines = lines[ka_start:ka_end]
        ka_src = src[ka_start:ka_end]

        # Find ### Decisions made before first #### **term**
        dec_start = None
        first_term = None
        for k, kl in enumerate(ka_lines):
            if not ka_src[k]:
                if dec_start is None and re.match(r"^### Decisions made\s*$", kl):
                    dec_start = k
                if first_term is None and re.match(r"^#### \*\*.+\*\*", kl):
                    first_term = k

        if dec_start is None or first_term is None or dec_start >= first_term:
            out.extend(ka_lines)
            i = ka_end
            continue

        # Extract decisions block
        dec_end = dec_start + 1
        while dec_end < len(ka_lines):
            if not ka_src[dec_end] and (
                re.match(r"^(###|####|##|# )", ka_lines[dec_end]) or
                ka_lines[dec_end].strip() == "---"
            ):
                break
            dec_end += 1

        decisions_block = ka_lines[dec_start:dec_end]
        new_ka = ka_lines[:dec_start] + ka_lines[dec_end:]
        new_ka_src = ka_src[:dec_start] + ka_src[dec_end:]

        # Find insertion point after last #### References
        insert_at = len(new_ka)
        for k in range(len(new_ka) - 1, -1, -1):
            if not new_ka_src[k] and re.match(r"^#### References\s*$", new_ka[k]):
                ref_end = k + 1
                while ref_end < len(new_ka):
                    if not new_ka_src[ref_end] and (
                        re.match(r"^(###|####|##|# )", new_ka[ref_end]) or
                        new_ka[ref_end].strip() == "---"
                    ):
                        break
                    ref_end += 1
                insert_at = ref_end
                break

        # Trim trailing blanks before insertion point
        while insert_at > 0 and new_ka[insert_at - 1].strip() == "":
            insert_at -= 1

        final_ka = (new_ka[:insert_at] + ["", "---", ""] +
                    decisions_block + new_ka[insert_at:])
        out.extend(final_ka)
        i = ka_end

    return "\n".join(out)


def _remove_intra_ka_separators(text: str) -> str:
    """Remove --- between terms within the same KA; keep structural ones."""
    lines = text.split("\n")
    src = track_source_blocks(lines)
    out: List[str] = []
    i = 0
    fm_count = 0
    fm_done = False

    while i < len(lines):
        line = lines[i]

        if src[i]:
            out.append(line)
            i += 1
            continue

        if line.strip() == "---" and not fm_done:
            fm_count += 1
            out.append(line)
            if fm_count == 2:
                fm_done = True
            i += 1
            continue

        if line.strip() == "---" and fm_done:
            j = i + 1
            while j < len(lines) and not src[j] and lines[j].strip() == "":
                j += 1
            next_line = lines[j].strip() if j < len(lines) else ""

            keep = (
                re.match(r"^## \*\*", next_line) or
                re.match(r"^# (Core|Boundary) Domain", next_line) or
                re.match(r"^### (Decisions made|Domain Sketch|Ubiquitous Language|References)", next_line)
            )
            if keep:
                out.append(line)
            i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def _ensure_boundary_ul(text: str) -> str:
    """Add ### Ubiquitous Language before first #### **term** in Boundary Domain (idempotent)."""
    lines = text.split("\n")
    src = track_source_blocks(lines)
    out: List[str] = []
    i = 0
    in_boundary = False
    ul_done = False

    while i < len(lines):
        line = lines[i]

        if not src[i] and re.match(r"^# Boundary Domain", line):
            out.append(line)
            in_boundary = True
            ul_done = False
            i += 1
            continue

        # If ### Ubiquitous Language already present in boundary, mark done
        if in_boundary and not src[i] and re.match(r"^### Ubiquitous Language\s*$", line):
            ul_done = True
            out.append(line)
            i += 1
            continue

        if in_boundary and not ul_done and not src[i] and re.match(r"^#### \*\*", line):
            out.append("")
            out.append("### Ubiquitous Language")
            out.append("")
            ul_done = True
            out.append(line)
            i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


# ============================================================
# Domain Sketch: data model
# ============================================================

@dataclass
class RefBlock:
    lines: List[str]

    def key(self) -> str:
        non_empty = [l for l in self.lines if l.strip()]
        return "\n".join(non_empty[:2])


@dataclass
class TermData:
    name: str
    dl_content: List[str] = field(default_factory=list)
    ds_content: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    refs: List[RefBlock] = field(default_factory=list)


@dataclass
class KAData:
    name: str
    prose: List[str] = field(default_factory=list)
    ka_decisions: List[str] = field(default_factory=list)
    terms: List[TermData] = field(default_factory=list)


@dataclass
class BoundaryTermData:
    name: str
    owned_by: str
    dl_content: List[str] = field(default_factory=list)
    ds_content: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    refs: List[RefBlock] = field(default_factory=list)


def _strip_blanks(lines: List[str]) -> List[str]:
    result = list(lines)
    while result and result[0].strip() == "":
        result.pop(0)
    while result and result[-1].strip() == "":
        result.pop()
    return result


# ============================================================
# Domain Sketch: parsing helpers
# ============================================================

def _parse_term_ability(term_name: str, term_lines: List[str], term_src: List[bool]) -> TermData:
    """
    Parse one ability-style term block.
    Handles both explicit #### References sections and inline **Ref blocks.
    Sections: #### Domain Language, #### Domain Sketch, #### References, #### Decisions made
    """
    dl: List[str] = []
    ds: List[str] = []
    decisions: List[str] = []
    refs: List[RefBlock] = []
    current_ref: List[str] = []
    section = None
    in_ref = False  # True when accumulating an inline ref block

    def flush_ref():
        nonlocal in_ref
        if current_ref:
            while current_ref and current_ref[-1].strip() == "":
                current_ref.pop()
            refs.append(RefBlock(lines=list(current_ref)))
            current_ref.clear()
        in_ref = False

    for i, line in enumerate(term_lines):
        stripped = line.strip()

        if term_src[i]:
            # Inside source block - route to current collector
            if in_ref or section == "refs":
                current_ref.append(line)
            elif section == "dl":
                dl.append(line)
            elif section == "ds":
                ds.append(line)
            elif section == "decisions":
                decisions.append(line)
            continue

        if re.match(r"^#### Domain [Ll]anguage\s*$", line):
            flush_ref()
            section = "dl"
            continue
        if re.match(r"^#### Domain Sketch\s*$", line):
            flush_ref()
            section = "ds"
            continue
        if re.match(r"^#### Decisions made", line):
            flush_ref()
            section = "decisions"
            continue
        if re.match(r"^#### References\s*$", line):
            flush_ref()
            section = "refs"
            in_ref = False
            continue
        if stripped == "---":
            continue

        if section == "dl":
            if stripped.startswith("**Ref"):
                # Inline ref within DL section
                flush_ref()
                in_ref = True
                current_ref.append(line)
            elif in_ref:
                # Continuation of inline ref (Source:, Locator:, Extract:, blank)
                current_ref.append(line)
            else:
                dl.append(line)
        elif section == "ds":
            ds.append(line)
        elif section == "decisions":
            decisions.append(line)
        elif section == "refs":
            if stripped.startswith("**Ref"):
                flush_ref()
                current_ref.append(line)
            else:
                current_ref.append(line)

    flush_ref()
    return TermData(name=term_name, dl_content=dl, ds_content=ds,
                    decisions=decisions, refs=refs)


def _parse_term_advantage(term_name: str, term_lines: List[str], term_src: List[bool]) -> TermData:
    """
    Parse one advantage-style term block.
    DL bullets and inline refs come before #### Domain Sketch.
    """
    dl: List[str] = []
    ds: List[str] = []
    decisions: List[str] = []
    refs: List[RefBlock] = []
    current_ref: List[str] = []
    section = "dl"
    in_ref = False

    def flush_ref():
        nonlocal in_ref
        if current_ref:
            # Trim trailing blanks
            while current_ref and current_ref[-1].strip() == "":
                current_ref.pop()
            refs.append(RefBlock(lines=list(current_ref)))
            current_ref.clear()
        in_ref = False

    for i, line in enumerate(term_lines):
        stripped = line.strip()

        if term_src[i]:
            if in_ref:
                current_ref.append(line)
            elif section == "ds":
                ds.append(line)
            elif section == "decisions":
                decisions.append(line)
            else:
                dl.append(line)
            continue

        if re.match(r"^#### Domain Sketch\s*$", line):
            flush_ref()
            section = "ds"
            continue
        if re.match(r"^#### Decisions made", line):
            flush_ref()
            section = "decisions"
            continue
        if stripped == "---":
            continue

        if section == "dl":
            if stripped.startswith("**Ref"):
                # Start new ref block
                flush_ref()
                in_ref = True
                current_ref.append(line)
            elif in_ref:
                # Continuation of ref (Source:, Locator:, blank lines, etc.)
                current_ref.append(line)
            else:
                dl.append(line)
        elif section == "ds":
            ds.append(line)
        elif section == "decisions":
            decisions.append(line)

    flush_ref()
    return TermData(name=term_name, dl_content=dl, ds_content=ds,
                    decisions=decisions, refs=refs)


def _parse_boundary_term_ability(lines: List[str], src: List[bool]) -> Optional[BoundaryTermData]:
    """Parse heading + Owned by: for a boundary term in ability-style."""
    # lines[0] should be ## term_name (may already be #### **term** if idempotent re-run)
    if re.match(r"^#### \*\*", lines[0]):
        # Already transformed — parse name and owned_by from transformed heading
        m = re.match(r"^#### \*\*(.+?)\*\* \*\(owned by: (.+?)\)\*", lines[0])
        if m:
            name = m.group(1).strip()
            owned_by = m.group(2).strip()
            td = _parse_term_ability(name, lines[1:], src[1:])
            return BoundaryTermData(name=name, owned_by=owned_by,
                                    dl_content=td.dl_content, ds_content=td.ds_content,
                                    decisions=td.decisions, refs=td.refs)
        return None
    if not re.match(r"^## ", lines[0]):
        return None
    name = lines[0][3:].strip().strip("*")
    owned_by = ""
    content_start = 1

    for j in range(1, len(lines)):
        if not src[j] and re.match(r"^Owned by:", lines[j].strip()):
            owned_by = lines[j].strip()[len("Owned by:"):].strip()
            content_start = j + 1
            break

    rest = lines[content_start:]
    rest_src = src[content_start:]
    td = _parse_term_ability(name, rest, rest_src)
    return BoundaryTermData(name=name, owned_by=owned_by,
                            dl_content=td.dl_content, ds_content=td.ds_content,
                            decisions=td.decisions, refs=td.refs)


def _parse_boundary_term_advantage(lines: List[str], src: List[bool]) -> Optional[BoundaryTermData]:
    """Parse boundary term in advantage-style (same structure)."""
    return _parse_boundary_term_ability(lines, src)


# ============================================================
# Domain Sketch: file-level parsers
# ============================================================

def _split_major_sections(lines: List[str], src: List[bool]):
    """Split into pre_content, core_lines, boundary_lines."""
    core_start = None
    boundary_start = None
    for i, line in enumerate(lines):
        if not src[i]:
            if re.match(r"^# Core Domain\s*$", line) and core_start is None:
                core_start = i
            elif re.match(r"^# Boundary Domain\s*$", line):
                boundary_start = i

    if core_start is None:
        return lines, [], []

    core_end = boundary_start if boundary_start is not None else len(lines)
    pre = lines[:core_start]
    core = lines[core_start:core_end]
    boundary = lines[boundary_start:] if boundary_start is not None else []
    return pre, core, boundary


def _parse_core_ability(core_lines: List[str], core_src: List[bool]):
    """Parse core domain lines (ability-style) into list of KAData."""
    ka_list: List[KAData] = []

    # Find KA start positions (## KA Name, not Core/Boundary Domain)
    ka_starts = []
    for i, line in enumerate(core_lines):
        if not core_src[i] and re.match(r"^## ", line):
            heading = line[3:].strip()
            if heading not in ("Core Domain", "Boundary Domain", "Domain logic"):
                ka_starts.append(i)

    for idx, start in enumerate(ka_starts):
        end = ka_starts[idx + 1] if idx + 1 < len(ka_starts) else len(core_lines)
        ka_block = core_lines[start:end]
        ka_src = core_src[start:end]
        ka = _parse_ka_ability(ka_block, ka_src)
        ka_list.append(ka)

    return ka_list


def _parse_ka_ability(ka_lines: List[str], ka_src: List[bool]) -> KAData:
    """Parse one KA block (ability-style)."""
    ka_name = ka_lines[0][3:].strip().strip("*")
    prose: List[str] = []
    ka_decisions: List[str] = []
    terms: List[TermData] = []

    # Find term start positions (### term_name) and KA-level decisions
    # KA-level = #### Decisions made before the first ### term
    term_starts = []
    for i, line in enumerate(ka_lines[1:], start=1):
        if not ka_src[i] and re.match(r"^### ", line):
            term_starts.append(i)

    # Find KA-level decisions (between start and first term)
    first_term = term_starts[0] if term_starts else len(ka_lines)
    in_ka_decisions = False
    for i, line in enumerate(ka_lines[1:first_term], start=1):
        if ka_src[i]:
            prose.append(line)
            continue
        if re.match(r"^#### Decisions made\s*$", line):
            in_ka_decisions = True
            continue
        if in_ka_decisions and re.match(r"^(###|##|# )", line):
            in_ka_decisions = False
        if in_ka_decisions:
            ka_decisions.append(line)
        elif line.strip() != "---":
            prose.append(line)

    # Parse each term
    for idx, start in enumerate(term_starts):
        end = term_starts[idx + 1] if idx + 1 < len(term_starts) else len(ka_lines)
        term_lines = ka_lines[start + 1:end]
        term_src = ka_src[start + 1:end]
        term_name = ka_lines[start][4:].strip().strip("*")
        term = _parse_term_ability(term_name, term_lines, term_src)
        terms.append(term)

    return KAData(name=ka_name, prose=prose, ka_decisions=ka_decisions, terms=terms)


def _parse_boundary_ability(boundary_lines: List[str], boundary_src: List[bool]):
    """Parse boundary domain (ability-style) into list of BoundaryTermData."""
    boundary_terms: List[BoundaryTermData] = []

    # Find ## term_name positions
    term_starts = []
    for i, line in enumerate(boundary_lines):
        if not boundary_src[i] and re.match(r"^## ", line):
            heading = line[3:].strip()
            if heading not in ("Core Domain", "Boundary Domain", "Domain logic"):
                term_starts.append(i)

    for idx, start in enumerate(term_starts):
        end = term_starts[idx + 1] if idx + 1 < len(term_starts) else len(boundary_lines)
        block = boundary_lines[start:end]
        block_src = boundary_src[start:end]
        bt = _parse_boundary_term_ability(block, block_src)
        if bt:
            boundary_terms.append(bt)

    return boundary_terms


def _parse_core_advantage(core_lines: List[str], core_src: List[bool]):
    """Parse core domain lines (advantage-style: ## Key Abstractions → ### KA → #### term)."""
    ka_list: List[KAData] = []

    # Find KA start positions (### KA Name)
    ka_starts = []
    for i, line in enumerate(core_lines):
        if not core_src[i] and re.match(r"^### ", line):
            # Make sure it's not inside source block
            ka_starts.append(i)

    for idx, start in enumerate(ka_starts):
        end = ka_starts[idx + 1] if idx + 1 < len(ka_starts) else len(core_lines)
        ka_block = core_lines[start:end]
        ka_src = core_src[start:end]
        ka = _parse_ka_advantage(ka_block, ka_src)
        ka_list.append(ka)

    return ka_list


def _parse_ka_advantage(ka_lines: List[str], ka_src: List[bool]) -> KAData:
    """Parse one KA block (advantage-style)."""
    ka_name = ka_lines[0][4:].strip().strip("*")
    prose: List[str] = []
    ka_decisions: List[str] = []
    terms: List[TermData] = []

    # Find term start positions (#### term_name, NOT #### Decisions made, Domain Sketch, References)
    term_starts = []
    for i, line in enumerate(ka_lines[1:], start=1):
        if not ka_src[i] and re.match(r"^#### ", line):
            heading = line[5:].strip()
            if (not re.match(r"^Decisions made", heading) and
                    heading not in ("Domain Sketch", "References")):
                term_starts.append(i)

    first_term = term_starts[0] if term_starts else len(ka_lines)
    in_ka_decisions = False

    for i, line in enumerate(ka_lines[1:first_term], start=1):
        if ka_src[i]:
            prose.append(line)
            continue
        if re.match(r"^#### Decisions made\s*$", line):
            in_ka_decisions = True
            continue
        if in_ka_decisions and re.match(r"^(####|###|##|# )", line):
            in_ka_decisions = False
        if in_ka_decisions:
            ka_decisions.append(line)
        elif line.strip() not in ("---", ""):
            prose.append(line)
        else:
            prose.append(line)

    for idx, start in enumerate(term_starts):
        end = term_starts[idx + 1] if idx + 1 < len(term_starts) else len(ka_lines)
        term_lines = ka_lines[start + 1:end]
        term_src = ka_src[start + 1:end]
        term_name = ka_lines[start][5:].strip().strip("*")
        term = _parse_term_advantage(term_name, term_lines, term_src)
        terms.append(term)

    return KAData(name=ka_name, prose=prose, ka_decisions=ka_decisions, terms=terms)


def _parse_boundary_advantage(boundary_lines: List[str], boundary_src: List[bool]):
    """Parse boundary domain (advantage-style)."""
    return _parse_boundary_ability(boundary_lines, boundary_src)


# ============================================================
# Domain Sketch: rendering
# ============================================================

def _render_ka(ka: KAData) -> List[str]:
    out: List[str] = []
    clean_name = ka.name.strip("*")
    out.append(f"## **{clean_name}**")
    out.append("")

    prose = _strip_blanks(ka.prose)
    if prose:
        out.extend(prose)
        out.append("")

    out.append("### Ubiquitous Language")
    out.append("")
    for term in ka.terms:
        clean = term.name.strip("*")
        out.append(f"#### **{clean}**")
        dl = _strip_blanks(term.dl_content)
        if dl:
            out.extend(dl)
        out.append("")

    out.append("---")
    out.append("")
    out.append("### Domain Sketch")
    out.append("")
    for term in ka.terms:
        clean = term.name.strip("*")
        out.append(f"#### **{clean}**")
        ds = _strip_blanks(term.ds_content)
        if ds:
            out.extend(ds)
        out.append("")

    out.append("---")
    out.append("")
    out.append("### Decisions made")
    out.append("")

    ka_dec = _strip_blanks(ka.ka_decisions)
    if ka_dec:
        out.extend(ka_dec)
        out.append("")

    for term in ka.terms:
        term_dec = _strip_blanks(term.decisions)
        if term_dec:
            out.extend(term_dec)
            out.append("")

    out.append("### References")
    out.append("")

    seen: set = set()
    for term in ka.terms:
        for ref in term.refs:
            k = ref.key()
            if k not in seen:
                seen.add(k)
                out.extend(ref.lines)
                out.append("")

    return out


def _render_boundary(boundary_terms: List[BoundaryTermData]) -> List[str]:
    if not boundary_terms:
        return []

    out: List[str] = []
    out.append("")
    out.append("# Boundary Domain")
    out.append("")
    out.append("### Ubiquitous Language")
    out.append("")

    for bt in boundary_terms:
        clean = bt.name.strip("*")
        out.append(f"#### **{clean}** *(owned by: {bt.owned_by})*")
        dl = _strip_blanks(bt.dl_content)
        if dl:
            out.extend(dl)
        out.append("")

    out.append("---")
    out.append("")
    out.append("### Domain Sketch")
    out.append("")

    for bt in boundary_terms:
        clean = bt.name.strip("*")
        out.append(f"#### **{clean}**")
        ds = _strip_blanks(bt.ds_content)
        if ds:
            out.extend(ds)
        out.append("")

    out.append("---")
    out.append("")
    out.append("### Decisions made")
    out.append("")

    for bt in boundary_terms:
        dec = _strip_blanks(bt.decisions)
        if dec:
            out.extend(dec)
            out.append("")

    out.append("### References")
    out.append("")

    seen: set = set()
    for bt in boundary_terms:
        for ref in bt.refs:
            k = ref.key()
            if k not in seen:
                seen.add(k)
                out.extend(ref.lines)
                out.append("")

    return out


# ============================================================
# Domain Sketch: top-level transform
# ============================================================

def remove_domain_logic_section(text: str) -> str:
    """Remove ## Domain logic section and its trailing --- separator."""
    lines = text.split("\n")
    src = track_source_blocks(lines)
    out: List[str] = []
    i = 0
    skip = False

    while i < len(lines):
        line = lines[i]

        if src[i]:
            if not skip:
                out.append(line)
            i += 1
            continue

        if re.match(r"^## Domain logic\s*$", line):
            skip = True
            i += 1
            continue

        if skip:
            if line.strip() == "---":
                skip = False
                i += 1
                continue
            elif re.match(r"^# ", line) or re.match(r"^## ", line):
                skip = False
                out.append(line)
                i += 1
                continue
            i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def _ds_already_transformed(lines: List[str], src: List[bool]) -> bool:
    """Return True if the DS file is already in new format (has ### Ubiquitous Language + ### Domain Sketch)."""
    has_ul = any(not src[i] and re.match(r"^### Ubiquitous Language\s*$", lines[i]) for i in range(len(lines)))
    has_ds = any(not src[i] and re.match(r"^### Domain Sketch\s*$", lines[i]) for i in range(len(lines)))
    return has_ul and has_ds


def transform_domain_sketch(text: str) -> str:
    """Full content restructuring of domain-sketch files."""
    # Quick idempotency guard: already in new format
    lines0 = text.split("\n")
    src0 = track_source_blocks(lines0)
    if _ds_already_transformed(lines0, src0):
        return text

    text = remove_domain_logic_section(text)
    lines = text.split("\n")
    src = track_source_blocks(lines)

    has_ka_header = any(
        not src[i] and re.match(r"^## Key Abstractions\s*$", lines[i])
        for i in range(len(lines))
    )

    pre, core, boundary = _split_major_sections(lines, src)
    pre_src = src[:len(pre)]
    core_src = src[len(pre):len(pre) + len(core)]
    boundary_src = src[len(pre) + len(core):]

    if has_ka_header:
        ka_list = _parse_core_advantage(core, core_src)
        boundary_terms = _parse_boundary_advantage(boundary, boundary_src) if boundary else []
    else:
        ka_list = _parse_core_ability(core, core_src)
        boundary_terms = _parse_boundary_ability(boundary, boundary_src) if boundary else []

    # Reconstruct
    out_lines: List[str] = []

    # Pre-content (fix ## Module: → # Module:)
    for line in pre:
        if re.match(r"^## Module:", line):
            out_lines.append("# " + line[3:])
        else:
            out_lines.append(line)

    # Remove trailing blanks from pre
    while out_lines and out_lines[-1].strip() == "":
        out_lines.pop()
    out_lines.append("")

    out_lines.append("# Core Domain")
    out_lines.append("")

    for ka in ka_list:
        out_lines.extend(_render_ka(ka))
        out_lines.append("---")
        out_lines.append("")

    if boundary_terms:
        out_lines.extend(_render_boundary(boundary_terms))
        out_lines.append("")

    # Ensure single trailing newline
    result = "\n".join(out_lines)
    result = _deduplicate_ul_headings(result)
    result = result.rstrip("\n") + "\n"
    return result


# ============================================================
# File dispatch
# ============================================================

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str, dry_run: bool = False):
    if dry_run:
        print(f"[DRY-RUN] Would write {path}")
    else:
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path}")


def transform_file(path: Path, dry_run: bool = False):
    name = path.name
    text = read(path)

    if name.endswith("-domain-language.md"):
        result = transform_domain_language(text)
    elif name.endswith("-key-abstractions.md"):
        result = transform_key_abstractions(text)
    elif name.endswith("-domain-sketch.md"):
        result = transform_domain_sketch(text)
    else:
        print(f"Skipping {path} (unknown type)")
        return

    if result != text:
        write(path, result, dry_run)
    else:
        print(f"No changes: {path}")


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    modules = args if args else MODULES

    for module in modules:
        module_dir = DOCS_ROOT / module
        if not module_dir.exists():
            print(f"Module dir not found: {module_dir}")
            continue
        for suffix in ["-domain-language.md", "-key-abstractions.md", "-domain-sketch.md"]:
            path = module_dir / f"{module}{suffix}"
            if path.exists():
                transform_file(path, dry_run)
            else:
                print(f"Not found: {path}")


if __name__ == "__main__":
    main()
