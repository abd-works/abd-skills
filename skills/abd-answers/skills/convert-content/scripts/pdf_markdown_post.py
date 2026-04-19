"""
Generic cleanup for PDF-extracted markdown (MarkItDown / pdfminer, etc.).

**This module rewrites markdown during convert**—the right place for structural composition
(findable headings, less noise) before chunking. The chunker and chunking-spec drafter only
read what is already on disk.

**Belongs here (convert pipeline):** patterns caused by the PDF format itself—running
headers/footers repeated on every page, duplicate banner lines, obvious extraction noise;
**conservative** regex-based heading promotion (``CHAPTER n``, ``APPENDIX``, ``PART …``);
**dotted-leader lines** (``Title ........ page``) → ``### Title {page}`` before chapter promotion;
optional **PDF outline → headings** via ``pdf_outline_headings`` when PyMuPDF is installed.

**Does not belong here:** book-specific tuning, corpus-only rules—use a topic script or YAML.

Kept in sync with ``agilebydesign-skills/.../scripts/pdf_markdown_post.py``.
See ``convert_to_markdown.convert_one`` which applies this to ``.pdf`` sources after
extraction and before writing the mirror ``.md``.

**Leading table of contents:** If the extract contains a ``TABLE OF CONTENTS`` block before
real body text, that region is **replaced** with a short ``## Table of contents`` stub so
dot-leader / regex passes do not turn the TOC into hundreds of fake ``###`` lines at the
front. End of the removed region is the first ``WELCOME TO`` line after the TOC, or the first
long mixed-case prose line. ``PDF_KEEP_LEADING_TOC=1`` disables this.

**Env:** ``PDF_SKIP_REGEX_HEADINGS=1``, ``PDF_SKIP_DOTTED_LEADER_HEADINGS=1``,
``PDF_SKIP_OUTLINE_HEADINGS=1`` (see ``pdf_outline_headings.py``). ``PDF_KEEP_LEADING_TOC=1``
keeps the raw leading PDF table of contents.
``PDF_SKIP_DEDUPE_CHAPTER_H2=1`` — skip dropping repeated identical ``## CHAPTER …`` / ``## APPENDIX …``.
``PDF_SKIP_ALL_CAPS_HEADINGS=1`` — skip ALL CAPS → ``###`` promotion (e.g. ``ADVANTAGES``).
``PDF_SKIP_DEMOTE_NON_CHAPTER_H2=1`` — skip demoting ``##`` to ``###`` after the first
``## CHAPTER n`` / ``## APPENDIX`` (keeps MarkItDown ``##`` as top-level everywhere).
``PDF_SKIP_STACKED_H2_TABLES=1`` — skip stacked column blocks → pipe table merge.
``PDF_STACKED_TABLE_MIN_ROWS``, ``PDF_STACKED_TABLE_MIN_COLS`` (optional).
``PDF_SKIP_REMOVE_STANDALONE_PAGE=1`` — keep lines that are only ``Page`` (PDF column spacers).
"""

from __future__ import annotations

import os
import re
from pathlib import Path


def _is_probable_running_header_or_footer_line(stripped: str) -> bool:
    """
    Heuristic: short standalone line that looks like a repeated title strip (no body text).

    Not book-specific—many PDFs emit ALL CAPS book title + chapter name in margins.
    """
    if not stripped or len(stripped) > 140:
        return False
    if stripped.startswith(("#", "|", "-", "•", "*")):
        return False
    letters = [c for c in stripped if c.isalpha()]
    if len(letters) < 4:
        return False
    if not all(c.isupper() for c in letters):
        return False
    # Avoid dropping duplicate sentences (rarely identical consecutive in prose)
    if ". " in stripped and len(stripped) > 50:
        return False
    return True


def collapse_consecutive_duplicate_banner_lines(text: str) -> str:
    """
    Drop the second of two consecutive identical lines when both look like PDF margin
    banners (ALL CAPS strips). Typical pattern::

        MUTANTS & MASTERMINDS
        MUTANTS & MASTERMINDS

        DELUXE HERO'S HANDBOOK
        DELUXE HERO'S HANDBOOK

    becomes one copy of each block with no handbook-specific strings hardcoded.
    """
    lines = text.splitlines()
    out: list[str] = []
    prev: str | None = None
    for line in lines:
        stripped = line.strip()
        if (
            prev is not None
            and stripped
            and stripped == prev
            and _is_probable_running_header_or_footer_line(stripped)
        ):
            continue
        out.append(line)
        if stripped:
            prev = stripped
        # keep prev from previous non-empty for duplicate check across blank lines?
        # Headers are usually adjacent; if blank between, second copy still follows blank sometimes.
        elif not stripped:
            pass
    joined = "\n".join(out)
    if text.endswith("\n") and not joined.endswith("\n"):
        joined += "\n"
    return joined


def _regex_promotion_disabled() -> bool:
    v = os.environ.get("PDF_SKIP_REGEX_HEADINGS", "").strip().lower()
    return v in ("1", "true", "yes")


def _dotted_leader_promotion_disabled() -> bool:
    v = os.environ.get("PDF_SKIP_DOTTED_LEADER_HEADINGS", "").strip().lower()
    return v in ("1", "true", "yes")


def _leading_toc_replacement_disabled() -> bool:
    v = os.environ.get("PDF_KEEP_LEADING_TOC", "").strip().lower()
    return v in ("1", "true", "yes")


def _dedupe_chapter_h2_disabled() -> bool:
    v = os.environ.get("PDF_SKIP_DEDUPE_CHAPTER_H2", "").strip().lower()
    return v in ("1", "true", "yes")


def _all_caps_headings_disabled() -> bool:
    v = os.environ.get("PDF_SKIP_ALL_CAPS_HEADINGS", "").strip().lower()
    return v in ("1", "true", "yes")


def _stacked_h2_tables_disabled() -> bool:
    v = os.environ.get("PDF_SKIP_STACKED_H2_TABLES", "").strip().lower()
    return v in ("1", "true", "yes")


def _remove_standalone_page_disabled() -> bool:
    v = os.environ.get("PDF_SKIP_REMOVE_STANDALONE_PAGE", "").strip().lower()
    return v in ("1", "true", "yes")


def _demote_non_chapter_h2_disabled() -> bool:
    v = os.environ.get("PDF_SKIP_DEMOTE_NON_CHAPTER_H2", "").strip().lower()
    return v in ("1", "true", "yes")


_WELCOME_BODY_START = re.compile(r"(?im)^WELCOME TO\b")


def _fallback_first_long_prose_line_start(text: str, search_from: int) -> int | None:
    tail = text[search_from:]
    offset = 0
    for line in tail.splitlines(keepends=True):
        s = line.strip()
        if not s:
            offset += len(line)
            continue
        if len(s) < 120:
            offset += len(line)
            continue
        if s.startswith("#"):
            offset += len(line)
            continue
        letters = [c for c in s if c.isalpha()]
        if len(letters) < 40:
            offset += len(line)
            continue
        upper = sum(1 for c in letters if c.isupper())
        if upper / len(letters) > 0.75:
            offset += len(line)
            continue
        return search_from + offset
    return None


def replace_leading_table_of_contents_block(text: str) -> str:
    """
    Replace the PDF's front ``TABLE OF CONTENTS`` region with a short stub (before dot-leader
    promotion so TOC rows are not turned into fake ``###`` headings).
    """
    if _leading_toc_replacement_disabled():
        return text
    m = re.search(r"(?im)^TABLE OF CONTENTS\s*$", text)
    if not m:
        return text
    after_toc = text[m.end() :]
    welcome = _WELCOME_BODY_START.search(after_toc)
    if welcome is not None:
        start_body = m.end() + welcome.start()
    else:
        start_body = _fallback_first_long_prose_line_start(text, m.end())
    if start_body is None:
        return text
    stub = (
        "## Table of contents\n\n"
        "*The PDF table of contents (section titles and page numbers) is omitted; "
        "use the headings in the body below for navigation.*\n\n"
    )
    return text[: m.start()] + stub + text[start_body:]


_DOT_LEADER_PAGE = re.compile(r"^(.+?)\s*\.{2,}\s*(\d+)\s*$")


def strip_dot_leader_page_label(s: str) -> str:
    """
    Turn ``CHAPTER 4: SKILLS ........... 113`` into ``CHAPTER 4: SKILLS 113``.

    Keeps page reference as a trailing number (not dot leaders). No-op if no match.
    """
    m = _DOT_LEADER_PAGE.match(s.strip())
    if not m:
        return s
    return f"{m.group(1).strip()} {m.group(2)}"


def promote_dotted_leader_section_lines(text: str) -> str:
    """
    Promote ``Section title ........ page`` stubs to ``###`` headings **with page number**.

    Typical of PDF TOC and rulebook bodies where subsections use dot leaders to page
    numbers. Emits ``### Title 42`` so structure stays in headings—not a pipe table.
    Lines that look like ``CHAPTER n…``, ``APPENDIX …``, or ``PART …`` are
    left unchanged so ``promote_regex_section_headings`` can emit ``##`` / ``###``.
    """
    rx = re.compile(r"^([ \t]*)(.+?)\s*\.{2,}\s*(\d+)\s*$")
    part_start = re.compile(
        r"^PART\s+(?:ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|[IVXLC]+|\d+)\b",
        re.IGNORECASE,
    )
    out: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            out.append(line)
            continue
        m = rx.match(line.rstrip())
        if not m:
            out.append(line)
            continue
        indent, title = m.group(1), m.group(2).strip()
        if len(title) < 4 or len(title) > 200:
            out.append(line)
            continue
        if re.match(r"^CHAPTER\s+\d+", title, re.I):
            out.append(line)
            continue
        if re.match(r"^APPENDIX\s+\S", title, re.I):
            out.append(line)
            continue
        if part_start.match(title):
            out.append(line)
            continue
        page = m.group(3)
        out.append(f"{indent}### {title} {page}")
    joined = "\n".join(out)
    if text.endswith("\n") and not joined.endswith("\n"):
        joined += "\n"
    return joined


def _expand_pdf_duplicate_chapter_banners(stripped: str) -> list[str]:
    """
    Many PDFs glue the chapter title, a duplicate running-header echo, and body on one line::

        CHAPTER 3: ABILITIES CHAPTER 3: ABILITIES Everyone has.

    Only the **first** ``CHAPTER N: <title>`` is the chapter heading (e.g. ``CHAPTER 3: ABILITIES``).
    The second ``CHAPTER 3: ABILITIES`` is not a separate section—it is dropped and the text
    after it (``Everyone has.``) becomes normal prose on the next line.

    Split on repeated ``CHAPTER n:`` markers; when a segment repeats the same banner plus body,
    strip the repeated banner prefix. The first segment alone is promoted to ``##`` by the caller.
    """
    s = stripped.strip()
    if not re.match(r"^CHAPTER\s+\d+\s*:", s, re.I):
        return [stripped]
    parts = re.split(r"\s+(?=CHAPTER\s+\d+\s*:)", s)
    first = parts[0].strip()
    out: list[str] = [first]
    for seg in parts[1:]:
        seg = seg.strip()
        if seg.startswith(first + " "):
            out.append(seg[len(first) :].strip())
        else:
            out.append(seg)
    return [x for x in out if x]


def promote_regex_section_headings(text: str) -> str:
    """
    Promote plain lines that look like section labels (not already markdown headings).

    Conservative: ``CHAPTER n…``, ``APPENDIX …``, ``PART ONE|TWO|…|roman|digit`` on a
    single line, max length 160 (not applied to lines that start with ``CHAPTER`` /
    ``APPENDIX`` so PDF glue lines are not skipped). Skips lines that already start
    with ``#``.
    """
    out: list[str] = []
    part_re = re.compile(
        r"^PART\s+(?:ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN"
        r"|[IVXLC]+|\d+)\b",
        re.IGNORECASE,
    )
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            out.append(line)
            continue
        indent = line[: len(line) - len(line.lstrip())]

        if re.match(r"^CHAPTER\s+\d+", s, re.I):
            for piece in _expand_pdf_duplicate_chapter_banners(s):
                ps = piece.strip()
                if re.match(r"^CHAPTER\s+\d+", ps, re.I):
                    out.append(f"{indent}## {strip_dot_leader_page_label(ps)}")
                else:
                    out.append(f"{indent}{piece}")
            continue

        if len(s) > 160:
            out.append(line)
            continue
        if re.match(r"^APPENDIX\s+\S", s, re.IGNORECASE):
            out.append(f"{indent}## {strip_dot_leader_page_label(s)}")
            continue
        if part_re.match(s):
            out.append(f"{indent}### {strip_dot_leader_page_label(s)}")
            continue
        out.append(line)
    joined = "\n".join(out)
    if text.endswith("\n") and not joined.endswith("\n"):
        joined += "\n"
    return joined


_H2_CHAPTER_APPENDIX = re.compile(
    r"^(\s*)##\s+((?:CHAPTER|APPENDIX)\s+.+)$",
    re.IGNORECASE,
)


def _normalize_structure_h2_key(title: str) -> str:
    """Normalize for comparing duplicate running-header ``## CHAPTER …`` / ``## APPENDIX …``."""
    return re.sub(r"\s+", " ", title.strip()).upper()


def collapse_duplicate_structure_h2_lines(text: str) -> str:
    """
    Drop repeated identical ``## CHAPTER …`` / ``## APPENDIX …`` lines (PDF running headers).

    Skips a line when it matches the same normalized title as the last *kept* structural H2;
    when the title changes (e.g. Chapter 2), the new heading is emitted.
    """
    lines = text.splitlines()
    out: list[str] = []
    last_key: str | None = None
    for line in lines:
        m = _H2_CHAPTER_APPENDIX.match(line.rstrip())
        if m:
            key = _normalize_structure_h2_key(m.group(2))
            if last_key is not None and key == last_key:
                continue
            last_key = key
        out.append(line)
    joined = "\n".join(out)
    if text.endswith("\n") and not joined.endswith("\n"):
        joined += "\n"
    return joined


_ALL_CAPS_HEADING_DENY = frozenset(
    {
        "mutants & masterminds",
        "deluxe hero's handbook",
        "deluxe heros handbook",
        "third edition",
        "green ronin publishing",
        "printed in the usa",
        "interior art",
        "cover art",
        "writing and design",
        "editing and development",
        "adventure design",
        "publisher",
        "playtesters",
        "special thanks",
        "email",
        "web site",
        "web sites",
        "introduction",
        "table of contents",
    }
)


def _normalize_for_deny_compare(stripped: str) -> str:
    t = stripped.lower().strip()
    for u, a in ("\u2019", "'"), ("\u2018", "'"), ("\u2032", "'"):
        t = t.replace(u, a)
    return t


def _line_is_all_caps_label(stripped: str) -> bool:
    if len(stripped) < 4 or len(stripped) > 120:
        return False
    if stripped.startswith(("#", "-", "•", "*", "|", ">")):
        return False
    letters = [c for c in stripped if c.isalpha()]
    if len(letters) < 3:
        return False
    if not all(c.isupper() for c in letters):
        return False
    if len(stripped.split()) > 12:
        return False
    low = _normalize_for_deny_compare(stripped)
    if low in _ALL_CAPS_HEADING_DENY:
        return False
    if re.match(r"^(CHAPTER|APPENDIX|PART)\b", stripped, re.I):
        return False
    if "HTTP://" in stripped.upper() or "WWW." in stripped.upper():
        return False
    return True


def _all_caps_to_title_case(s: str) -> str:
    return " ".join(w[:1].upper() + w[1:].lower() if w else w for w in s.split())


def promote_all_caps_section_headings(text: str) -> str:
    """
    Promote short standalone ALL CAPS lines to ``##`` headings (title case).
    """
    out: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            out.append(line)
            continue
        if s.startswith("#"):
            out.append(line)
            continue
        if not _line_is_all_caps_label(s):
            out.append(line)
            continue
        indent = line[: len(line) - len(line.lstrip())]
        title = _all_caps_to_title_case(s)
        out.append(f"{indent}## {title}")
    joined = "\n".join(out)
    if text.endswith("\n") and not joined.endswith("\n"):
        joined += "\n"
    return joined


def _md_escape_table_cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ").strip()


# Book chapter/appendix titles must stay as ``##`` headings — never as pipe-table column headers.
_CHAPTER_OR_APPENDIX_HEADING_TITLE = re.compile(r"(?i)^(CHAPTER\s+\d+|APPENDIX)\b")


def _looks_like_chapter_or_appendix_heading_title(title: str) -> bool:
    """True if ``title`` is a real chapter/appendix line (must not merge into stacked tables)."""
    t = title.strip()
    if not t:
        return False
    return bool(_CHAPTER_OR_APPENDIX_HEADING_TITLE.match(t))


def _is_section_break_h2(line: str) -> bool:
    """Long ``##`` titles end a stacked table (body sections, not column labels)."""
    s = line.strip()
    if not s.startswith("## ") or s.startswith("###"):
        return False
    title = s[3:].strip()
    if not title:
        return False
    ws = title.split()
    return len(ws) > 2 or len(title) > 36


def _plain_stacked_column_title(line: str) -> str | None:
    """Single-line column labels often extracted without ``##`` (e.g. ``d20``, ``Archetype``)."""
    s = line.strip()
    if re.match(r"^d20\s*$", s, re.I):
        return "d20"
    if s.casefold() == "archetype":
        return "Archetype"
    return None


def _short_h2_stacked_column_title(line: str) -> str | None:
    """``## Foo`` / ``## Foo Bar`` as column headers; long ``##`` titles are section breaks."""
    s = line.strip()
    if not s.startswith("## ") or s.startswith("###"):
        return None
    title = s[3:].strip()
    if not title:
        return None
    ws = title.split()
    if len(ws) > 2 or len(title) > 36:
        return None
    if _looks_like_chapter_or_appendix_heading_title(title):
        return None
    return title


def _stacked_column_header_title(line: str) -> str | None:
    p = _plain_stacked_column_title(line)
    if p is not None:
        return p
    return _short_h2_stacked_column_title(line)


def remove_standalone_page_lines(text: str) -> str:
    """
    Remove lines that are only ``Page`` (case-insensitive).

    PDF table columns often insert a ``Page`` spacer line between roll/name and page numbers.
    """
    out: list[str] = []
    for line in text.splitlines():
        if line.strip().casefold() == "page":
            continue
        out.append(line)
    joined = "\n".join(out)
    if text.endswith("\n") and not joined.endswith("\n"):
        joined += "\n"
    return joined


def _try_parse_stacked_column_table(
    lines: list[str],
    start: int,
    *,
    min_rows: int,
    min_cols: int,
    max_header_len: int = 80,
) -> tuple[int, str] | None:
    """
    Vertical column stacks → pipe table: ``## Mass`` / plain ``d20`` / ``Archetype`` / short ``##``.

    Stops at long ``## Section Title`` (not a column label). Later columns cap at the first
    column's row count and skip prose until the next column or section heading.
    """
    if start >= len(lines):
        return None
    t0 = _stacked_column_header_title(lines[start])
    if not t0 or len(t0) > max_header_len:
        return None
    if _looks_like_chapter_or_appendix_heading_title(t0):
        return None
    pos = start + 1
    vals0: list[str] = []
    while pos < len(lines):
        line = lines[pos]
        if _is_section_break_h2(line):
            return None
        if _stacked_column_header_title(line) is not None:
            break
        s = line.strip()
        if s:
            vals0.append(s)
        pos += 1
    n0 = len(vals0)
    if n0 < min_rows:
        return None
    columns: list[tuple[str, list[str]]] = [(t0, vals0)]
    while pos < len(lines):
        if _is_section_break_h2(lines[pos]):
            break
        t = _stacked_column_header_title(lines[pos])
        if t is None:
            break
        if _looks_like_chapter_or_appendix_heading_title(t):
            return None
        if len(t) > max_header_len:
            break
        header_line_idx = pos
        pos += 1
        vals: list[str] = []
        while (
            pos < len(lines)
            and len(vals) < n0
            and not _is_section_break_h2(lines[pos])
            and _stacked_column_header_title(lines[pos]) is None
        ):
            s = lines[pos].strip()
            if s:
                vals.append(s)
            pos += 1
        while pos < len(lines) and not _is_section_break_h2(lines[pos]):
            if _stacked_column_header_title(lines[pos]) is not None:
                break
            pos += 1
        if len(vals) != n0:
            pos = header_line_idx
            break
        columns.append((t, vals))
    if len(columns) < min_cols:
        return None
    headers = [c[0] for c in columns]
    rows = list(zip(*(c[1] for c in columns)))
    out_lines: list[str] = []
    out_lines.append("| " + " | ".join(_md_escape_table_cell(h) for h in headers) + " |")
    out_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        out_lines.append("| " + " | ".join(_md_escape_table_cell(x) for x in row) + " |")
    return pos, "\n".join(out_lines)


def _try_parse_h2_header_block_row_major_table(
    lines: list[str],
    start: int,
    *,
    min_rows: int,
    min_cols: int,
    max_header_len: int = 80,
) -> tuple[int, str] | None:
    """
    All short column ``##`` titles stacked first, then cell text in **row-major** order
    (each row left-to-right).

    If the first title is multi-word (e.g. ``## Power Effects``) and the following titles
    are single-word column names, the first title is kept as a ``##`` caption above the table.
    """
    pos = start
    while pos < len(lines) and not lines[pos].strip():
        pos += 1
    if pos >= len(lines) or _stacked_column_header_title(lines[pos]) is None:
        return None
    headers: list[str] = []
    while pos < len(lines):
        t = _stacked_column_header_title(lines[pos])
        if t is None:
            break
        if len(t) > max_header_len:
            return None
        if _looks_like_chapter_or_appendix_heading_title(t):
            return None
        headers.append(t)
        pos += 1
        while pos < len(lines) and not lines[pos].strip():
            pos += 1
    if len(headers) < min_cols:
        return None
    caption: str | None = None
    if (
        len(headers) >= min_cols + 1
        and len(headers[0].split()) > 1
        and all(len(h.split()) == 1 for h in headers[1:])
    ):
        caption = headers[0]
        headers = headers[1:]
    if len(headers) < min_cols:
        return None
    k = len(headers)
    vals: list[str] = []
    while pos < len(lines):
        line = lines[pos]
        if _is_section_break_h2(line):
            break
        st = line.strip()
        if not st:
            pos += 1
            continue
        if _stacked_column_header_title(line) is not None:
            break
        vals.append(st)
        pos += 1
    if not vals or len(vals) % k != 0:
        return None
    n = len(vals) // k
    if n < min_rows:
        return None
    out_parts: list[str] = []
    if caption:
        out_parts.append(f"## {caption}")
        out_parts.append("")
    out_lines: list[str] = []
    out_lines.append("| " + " | ".join(_md_escape_table_cell(h) for h in headers) + " |")
    out_lines.append("| " + " | ".join(["---"] * k) + " |")
    for i in range(n):
        row = [vals[i * k + j] for j in range(k)]
        out_lines.append("| " + " | ".join(_md_escape_table_cell(x) for x in row) + " |")
    out_parts.append("\n".join(out_lines))
    return pos, "\n".join(out_parts)


def promote_stacked_h2_column_tables(text: str) -> str:
    """
    Merge stacked column blocks into pipe tables (vertical strips, then header-block column-major).
    """
    try:
        min_rows = max(2, int(os.environ.get("PDF_STACKED_TABLE_MIN_ROWS", "3")))
    except ValueError:
        min_rows = 3
    try:
        min_cols = max(2, int(os.environ.get("PDF_STACKED_TABLE_MIN_COLS", "2")))
    except ValueError:
        min_cols = 2
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        parsed = _try_parse_stacked_column_table(
            lines, i, min_rows=min_rows, min_cols=min_cols
        )
        if parsed is not None:
            end_i, table_md = parsed
            if out and out[-1].strip():
                out.append("")
            out.append(table_md)
            i = end_i
            continue
        parsed2 = _try_parse_h2_header_block_row_major_table(
            lines, i, min_rows=min_rows, min_cols=min_cols
        )
        if parsed2 is not None:
            end_i, table_md = parsed2
            if out and out[-1].strip():
                out.append("")
            out.append(table_md)
            i = end_i
            continue
        out.append(lines[i])
        i += 1
    joined = "\n".join(out)
    if text.endswith("\n") and not joined.endswith("\n"):
        joined += "\n"
    return joined


def postprocess_pdf_markdown(text: str, pdf_path: Path | None = None) -> str:
    """
    Apply generic PDF markdown normalizations.

    When ``pdf_path`` is set (the source ``.pdf``), runs optional outline alignment
    if PyMuPDF is installed (see ``pdf_outline_headings``). Outline injection runs early
    (after leading TOC replacement), before stacked-column table promotion.
    """
    t = collapse_consecutive_duplicate_banner_lines(text)
    if not _leading_toc_replacement_disabled():
        t = replace_leading_table_of_contents_block(t)
    if pdf_path is not None:
        from pdf_outline_headings import inject_pdf_outline_headings

        t = inject_pdf_outline_headings(pdf_path, t)
    if not _dotted_leader_promotion_disabled():
        t = promote_dotted_leader_section_lines(t)
    if not _regex_promotion_disabled():
        t = promote_regex_section_headings(t)
    if not _dedupe_chapter_h2_disabled():
        t = collapse_duplicate_structure_h2_lines(t)
    if not _all_caps_headings_disabled():
        t = promote_all_caps_section_headings(t)
    if not _remove_standalone_page_disabled():
        t = remove_standalone_page_lines(t)
    if not _stacked_h2_tables_disabled():
        t = promote_stacked_h2_column_tables(t)
    return t
