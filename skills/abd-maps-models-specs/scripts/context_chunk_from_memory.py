"""
Chunking primitives ported from ``skills/abd-context-to-memory/scripts/chunk_markdown.py``,
extended with **1-based line ranges** in the source file for Phase 1 ``context-spec`` anchors.

Same strategy:
- PPTX / slide decks: split on ``<!-- Slide number: N -->``
- Large docs (>200 lines): ``#`` / ``##`` boundaries (min 5 lines before flush), or CHAPTER markers
- Small files: single chunk

This module has no I/O; ``build_context.py`` writes ``chunks/*.md`` + ``context_index.json``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# Match abd-context-to-memory ``chunk_markdown.MIN_CHUNK_LINES``
MIN_CHUNK_LINES = 5
LARGE_DOC_LINES = 200
# Subsections inside a chapter (flat PDF handbooks): min lines since last boundary
MIN_SUBSECTION_LINES = 2

_CHROME = re.compile(
    r"MUTANTS|DELUXE|HANDBOOK|GREEN\s+RONIN|OPEN\s+GAME|PRODUCT\s+IDENTITY|"
    r"PRINTED\s+IN|PLAYTESTERS|COPYRIGHT|ISBN",
    re.I,
)
# TOC dot leaders (6+); avoid matching prose ellipsis (… or "..." alone).
_TOC_DOT_LEADER = re.compile(r"\.{6,}")


def _classify_handbook_chunk(body: str) -> tuple[str, str]:
    """Per-chunk ``evidence_type`` / ``modeling_kind`` for flat handbook markdown."""
    head = body[:4000]
    low = head.lower()
    if "©" in head[:3000] or (
        "all rights reserved" in low and "open game license" in low[:2500]
    ):
        return ("metadata_noise", "noise")
    if "©" in head[:500] and "green ronin" in low[:800]:
        return ("metadata_noise", "noise")
    if len(_TOC_DOT_LEADER.findall(head)) >= 2 and len(body) < 20000:
        return ("mixed", "structural_only")
    if len(_TOC_DOT_LEADER.findall(head)) >= 1 and head.count("\n") < 80 and len(body) < 8000:
        return ("mixed", "structural_only")
    pipes = sum(1 for ln in body.split("\n") if ln.strip().startswith("|"))
    if pipes >= 4:
        return ("table", "rule")
    for ln in body.split("\n")[:25]:
        s = ln.strip()
        if s and s.upper().startswith("EXAMPLE") and s == s.upper():
            return ("example", "example")
    return ("rule", "rule")


@dataclass(frozen=True)
class Segment:
    """One chunk boundary in the original markdown file."""

    label: str
    line_start: int  # 1-based inclusive
    line_end: int  # 1-based inclusive
    body: str
    evidence_type: str | None = None
    modeling_kind: str | None = None
    handbook_chapter_line: str | None = None


def _is_slide_deck(text: str) -> bool:
    return bool(re.search(r"<!-- Slide number: \d+ -->", text))


def _has_markdown_headings(text: str) -> bool:
    return bool(re.search(r"^#{1,2}\s", text, re.MULTILINE))


def _chunk_by_slides_lines(lines: list[str]) -> list[Segment]:
    """Line-accurate slide split (same markers as ``chunk_markdown._chunk_by_slides``)."""
    chunks: list[tuple[str, list[str], int, int]] = []
    current: list[str] = []
    label = "preamble"
    chunk_start_line = 1

    for i, line in enumerate(lines):
        line_no = i + 1
        m = re.match(r"<!-- Slide number: (\d+) -->", line.strip())
        if m:
            if current and "".join(current).strip():
                chunks.append(
                    (label, current, chunk_start_line, line_no - 1)
                )
            label = f"slide_{int(m.group(1)):02d}"
            current = [line]
            chunk_start_line = line_no
        else:
            if not current:
                chunk_start_line = line_no
            current.append(line)

    if current and "".join(current).strip():
        chunks.append((label, current, chunk_start_line, len(lines)))

    out: list[Segment] = []
    for label, clines, ls, le in chunks:
        body = "\n".join(clines).strip()
        if body:
            out.append(Segment(label=label, line_start=ls, line_end=le, body=body))
    return out


def _chunk_by_headings_indexed(lines: list[str]) -> list[Segment]:
    boundaries: list[int] = []
    current_len = 0
    for i, line in enumerate(lines):
        if re.match(r"^#{1,2}\s", line) and current_len >= MIN_CHUNK_LINES:
            boundaries.append(i)
            current_len = 1
        else:
            current_len += 1

    starts = [0] + boundaries
    ends = boundaries + [len(lines)]
    out: list[Segment] = []
    for idx, (s, e) in enumerate(zip(starts, ends)):
        if s >= e:
            continue
        clines = lines[s:e]
        body = "\n".join(clines).strip()
        if not body:
            continue
        label = f"section_{idx:02d}"
        out.append(
            Segment(
                label=label,
                line_start=s + 1,
                line_end=e,
                body=body,
            )
        )
    return out


def _basic_subsection_title(stripped: str, *, prev_nonempty: str | None) -> bool:
    """ALL CAPS line that might start a handbook subsection (not running chrome)."""
    if not stripped or stripped == prev_nonempty:
        return False
    if len(stripped) < 4 or len(stripped) > 80:
        return False
    if _CHROME.search(stripped) or _TOC_DOT_LEADER.search(stripped):
        return False
    if stripped.isdigit():
        return False
    if stripped != stripped.upper():
        return False
    if sum(1 for c in stripped if c.isalpha()) < 2:
        return False
    return True


def _prose_or_stacked_header_follows(lines: list[str], i: int, current_title: str) -> bool:
    """True if line i looks like a real section break, not a stat-table cell."""
    j = i + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    if j >= len(lines):
        return True
    nxt = lines[j].strip()
    if not nxt:
        return True
    if re.match(r"^-?\d+$", nxt):
        return False
    if len(nxt) > 45 and any(c.islower() for c in nxt):
        return True
    if re.match(r"^[A-Z][a-z]", nxt):
        return True
    if nxt.startswith("•") or nxt.startswith("—") or nxt.startswith("–"):
        return True
    if any(q in nxt for q in ('"', "'", "’", "“")):
        return True
    if "http" in nxt.lower():
        return True
    # Stacked subsection titles (e.g. THE CORE MECHANIC then THE HEROES)
    if _basic_subsection_title(nxt, prev_nonempty=current_title):
        return True
    if nxt == nxt.title() and " " not in nxt and len(nxt) < 22:
        return False
    if nxt.upper() == nxt and len(nxt) <= 18 and " " not in nxt:
        return False
    return True


def _is_handbook_subsection_boundary(
    lines: list[str], i: int, prev_nonempty: str | None
) -> bool:
    stripped = lines[i].strip()
    if not _basic_subsection_title(stripped, prev_nonempty=prev_nonempty):
        return False
    if " " in stripped:
        return _prose_or_stacked_header_follows(lines, i, stripped)
    if len(stripped) < 6:
        return False
    return _prose_or_stacked_header_follows(lines, i, stripped)


def _chapter_line_before(lines: list[str], start_idx: int) -> str | None:
    """Most recent ``CHAPTER n: …`` line before this chunk (may be a running header)."""
    chapter_pat = re.compile(r"^CHAPTER\s+(\d+)\s*:", re.IGNORECASE)
    last: str | None = None
    for k in range(0, start_idx):
        s = lines[k].strip()
        m = chapter_pat.match(s) if s else None
        if not m:
            continue
        if "MUTANTS" in s.upper():
            continue
        last = s[:120]
    return last


def _chunk_by_chapter_and_caps_subsections(lines: list[str]) -> list[Segment]:
    """Chapter boundaries (``CHAPTER n:`` when *n* changes) + ALL CAPS subsection titles.

    Enabled per workspace via ``handbook_subsection_chunking: true`` in
    ``context_chunking_spec.yaml``. Tuned for PDF-derived RPG handbooks with
    running headers and no markdown ``#`` structure.
    """
    chapter_pat = re.compile(r"^CHAPTER\s+(\d+)\s*:", re.IGNORECASE)
    boundaries: list[int] = []
    current_len = 0
    last_chapter_num: int | None = None
    prev_nonempty: str | None = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        m_ch = chapter_pat.match(stripped) if stripped else None

        if m_ch:
            cn = int(m_ch.group(1))
            if last_chapter_num is not None and cn == last_chapter_num:
                current_len += 1
                if stripped:
                    prev_nonempty = stripped
                continue
            if current_len >= MIN_CHUNK_LINES:
                boundaries.append(i)
                current_len = 1
            else:
                current_len += 1
            last_chapter_num = cn
            if stripped:
                prev_nonempty = stripped
            continue

        if stripped and _is_handbook_subsection_boundary(lines, i, prev_nonempty):
            if current_len >= MIN_SUBSECTION_LINES:
                boundaries.append(i)
                current_len = 1
            else:
                current_len += 1
            prev_nonempty = stripped
            continue

        current_len += 1
        if stripped:
            prev_nonempty = stripped

    starts = [0] + boundaries
    ends = boundaries + [len(lines)]
    out: list[Segment] = []
    for idx, (s, e) in enumerate(zip(starts, ends)):
        if s >= e:
            continue
        clines = lines[s:e]
        body = "\n".join(clines).strip()
        if not body:
            continue
        label = f"section_{idx:02d}"
        et, mk = _classify_handbook_chunk(body)
        ch_line = _chapter_line_before(lines, s)
        out.append(
            Segment(
                label=label,
                line_start=s + 1,
                line_end=e,
                body=body,
                evidence_type=et,
                modeling_kind=mk,
                handbook_chapter_line=ch_line,
            )
        )
    return out


def _chunk_by_section_markers(lines: list[str]) -> list[Segment]:
    """Split on ``CHAPTER <n>`` lines when **n** changes.

    PDF-to-markdown often repeats the same chapter line on every page (running
    headers). Treating every match as a boundary shards the corpus; only start a
    new segment when the chapter **number** differs from the last one seen.
    """
    # Require ":" so "Chapter 5 and see …" (prose) does not split like a header.
    section_pat = re.compile(r"^CHAPTER\s+(\d+)\s*:", re.IGNORECASE)
    boundaries: list[int] = []
    current_len = 0
    last_chapter_num: int | None = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        m = section_pat.match(stripped) if stripped else None
        if m:
            chapter_num = int(m.group(1))
            if last_chapter_num is not None and chapter_num == last_chapter_num:
                # Running header / duplicate page chrome for same chapter
                current_len += 1
                continue
            # New chapter (or first chapter marker in doc)
            if current_len >= MIN_CHUNK_LINES:
                boundaries.append(i)
                current_len = 1
            else:
                current_len += 1
            last_chapter_num = chapter_num
        else:
            current_len += 1

    starts = [0] + boundaries
    ends = boundaries + [len(lines)]
    out: list[Segment] = []
    for idx, (s, e) in enumerate(zip(starts, ends)):
        if s >= e:
            continue
        clines = lines[s:e]
        body = "\n".join(clines).strip()
        if not body:
            continue
        label = f"section_{idx:02d}"
        out.append(Segment(label=label, line_start=s + 1, line_end=e, body=body))
    return out


def _extract_source_ref(text: str) -> tuple[str | None, str | None]:
    m = re.search(r"<!--\s*Source:\s*([^|]+)\s*\|\s*([^>]+)\s*-->", text)
    return (m.group(1).strip(), m.group(2).strip()) if m else (None, None)


def _add_chunk_source_ref(
    content: str, source_path: str | None, source_url: str | None, location: str
) -> str:
    if not source_path:
        return content
    loc = f", {location}" if location else ""
    url = f" | {source_url}" if source_url else ""
    return f"<!-- Source: {source_path}{loc}{url} -->\n\n" + content


def _loc_from_label(label: str) -> str:
    if label.startswith("slide_"):
        return f"slide {int(label.split('_')[1])}"
    if label.startswith("section_"):
        return f"section {int(label.split('_')[1]) + 1}"
    return ""


def segment_markdown(
    text: str, *, stem: str, handbook_subsection_chunking: bool = False
) -> list[Segment]:
    """
    Split ``text`` using the same rules as ``chunk_markdown.chunk_file`` (without image copy).
    ``stem`` is the source filename stem for single-chunk naming parity.

    When ``handbook_subsection_chunking`` is true (from workspace ``context_chunking_spec.yaml``),
    large flat handbooks also split on ALL CAPS subsection titles, not only on chapter changes.
    """
    lines = text.split("\n")
    line_count = len(lines)

    if _is_slide_deck(text):
        return _chunk_by_slides_lines(lines)

    if line_count > LARGE_DOC_LINES:
        if _has_markdown_headings(text):
            return _chunk_by_headings_indexed(lines)
        if handbook_subsection_chunking:
            return _chunk_by_chapter_and_caps_subsections(lines)
        return _chunk_by_section_markers(lines)

    body = text.strip()
    if not body:
        return []
    return [Segment(label=stem, line_start=1, line_end=line_count, body=body)]


def decorate_segment_body(seg: Segment, md_text: str) -> str:
    """Re-attach ``Source:`` banner when convert step left one in the file (memory pipeline)."""
    source_path, source_url = _extract_source_ref(md_text)
    loc = _loc_from_label(seg.label)
    return _add_chunk_source_ref(seg.body, source_path, source_url, loc)


def section_path_from_body(body: str, *, max_headings: int = 6) -> list[str]:
    """Breadcrumb from leading markdown headings in the chunk."""
    titles: list[str] = []
    for line in body.split("\n"):
        s = line.strip()
        m = re.match(r"^(#{1,3})\s+(.+)$", s)
        if not m:
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        titles = titles[: level - 1] + [title]
        if len(titles) >= max_headings:
            break
    return titles if titles else ["_body"]


def handbook_section_path_from_body(
    body: str, *, chapter_hint: str | None = None
) -> list[str]:
    """Breadcrumb from ``CHAPTER n:`` + first ALL CAPS subsection title in the chunk."""
    chapter: str | None = chapter_hint.strip()[:100] if chapter_hint else None
    subsection: str | None = None
    prev: str | None = None
    for line in body.split("\n")[:160]:
        s = line.strip()
        if not s:
            continue
        m = re.match(r"^(CHAPTER\s+\d+\s*:.+)$", s, re.IGNORECASE)
        if m and "MUTANTS" not in s.upper():
            chapter = m.group(1).strip()[:100]
            continue
        if _basic_subsection_title(s, prev_nonempty=prev):
            subsection = s[:100]
            break
        prev = s
    out: list[str] = []
    if chapter:
        out.append(chapter)
    if subsection:
        out.append(subsection)
    return out if out else ["_body"]
