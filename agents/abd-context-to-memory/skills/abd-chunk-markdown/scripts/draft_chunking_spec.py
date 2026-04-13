"""
Structural scan of markdown sources → draft context_chunking_spec.yaml.

**Scope:** Observes existing Markdown to propose YAML and reports. **Making** structure easy to find
(headings, sections, GFM tables) is **converter / post-process** work—this script does not substitute
for fixing bad PDF→Markdown extraction.

Usage:
  python draft_chunking_spec.py [--path <source_folder>] [--force]
  (If --path is omitted, uses same default as _config: CONTENT_MEMORY_ROOT or cwd.)

Scans all .md files under <source_folder>/markdown/ (or <source_folder> if no
markdown/ subfolder), analyses heading structure, table density, slide markers,
section patterns, and noise indicators.

**Structural scan** (heading/table metrics) is an assessment of **converted** markdown — outputs go in
**`markdown/`** only: **`structural_scan_report.txt`** and **`structural_scan_report.md`**.

**Drafted chunking spec** (YAML for the chunker) is a **later** pipeline artifact — written to
**`memory/context_chunking_spec.yaml`** next to chunk output, not beside source `.md` files.
**Poor heading counts usually mean fixing PDF→Markdown conversion**
(`pdf_markdown_post`, PyMuPDF outline, or a corpus script) — not extending this scanner.

**Tables:** Valid GFM pipe tables (separator row, aligned columns) are a **conversion** concern—fix in
`pdf_markdown_post` / MarkItDown / bespoke post-processors. This script only counts `|` lines and longest
run for chunk-size hints, not table rendering QA.

If the YAML already exists it is NOT overwritten — use --force to replace it.

The output spec has four required sections:
  section_boundaries  - regexes that start new major structural units
  splitting           - min/max sizes, table handling, heading split level
  defaults            - fallback evidence_type / chunk_type (surface form vs role in source)
  taxonomy            - **not auto-filled**: `evidence_type` and `chunk_type` must be **[]** until an AI/human
  proposes enums from **reading this source**. The structural scanner only suggests boundaries/splits — it does
  not invent type vocabularies (those differ per corpus).

After the AI derives chunk types for this corpus, edit **`memory/context_chunking_spec.yaml`**
(`taxonomy` and usually `defaults`). The chunker loads **`memory/`** first, then legacy paths under
`markdown/` or topic root. Run `chunk_markdown.py --path <that_folder>`; no second config.
"""

import re
import statistics
import sys
from collections import Counter
from pathlib import Path

from _config import ROOT, ensure_root

ensure_root()

SPEC_FILENAME = "context_chunking_spec.yaml"
# Human-readable structural scan; always written when a new spec is drafted (--force or missing spec).
REPORT_FILENAME = "structural_scan_report.txt"
REPORT_MD_FILENAME = "structural_scan_report.md"
# Do not scan these — they are outputs of this script and would skew heading counts.
SKIP_MD_NAMES = frozenset({REPORT_MD_FILENAME.casefold()})


def _markdown_reports_dir(src: Path) -> Path:
    """Structural scan reports (assessment of converted markdown): <topic>/markdown/."""
    return src / "markdown"


def _memory_spec_path(src: Path) -> Path:
    """Drafted chunking spec for the chunker lives with memory artifacts: <topic>/memory/."""
    return src / "memory" / SPEC_FILENAME


HEADING_SAMPLE_LIMIT = 48
DUPLICATE_HEADING_TOP_N = 20

# Heading outline in structural_scan_report.*: omit ATX deeper than this (1=# … 6=######).
# Default 5 keeps ##### but drops ###### noise on large rulebooks. None = no cap.
STRUCTURAL_OUTLINE_MAX_LEVEL: int | None = 5

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _heading_sample_as_atx(level: int, title: str) -> str:
    """
    Format a heading sample the way it should read in source markdown (## / ### …).

    If the title already ends with a page number, keep it; otherwise append `` pg`` as a
    placeholder meaning “page ref belongs here in conversion”—not a pipe table cell.
    """
    hashes = "#" * min(max(level, 1), 6)
    t = " ".join(title.replace("\n", " ").split()).strip()
    if not t:
        return f"{hashes} "
    if re.search(r"\d{1,4}\s*$", t):
        return f"{hashes} {t}"
    if re.search(r"(?:^|\s)pg\s*$", t, re.IGNORECASE):
        return f"{hashes} {t}"
    return f"{hashes} {t} pg"


def _collect_md_files(src: Path) -> list[Path]:
    """Collect .md sources: prefer <src>/markdown/, fall back to <src> itself."""
    markdown_dir = src / "markdown"
    scan = markdown_dir if markdown_dir.is_dir() else src
    return sorted(
        f for f in scan.rglob("*.md")
        if "images" not in f.parts
        and f.name.casefold() not in SKIP_MD_NAMES
        and not re.search(r"__(?:slide|section|page)_\d+\.md$", f.name, re.IGNORECASE)
        and "memory" not in [p.casefold() for p in f.relative_to(scan).parts[:-1]]
    )


def _median(nums: list[int]) -> float | None:
    if not nums:
        return None
    s = sorted(nums)
    n = len(s)
    mid = n // 2
    if n % 2:
        return float(s[mid])
    return (s[mid - 1] + s[mid]) / 2.0


def _heading_breakdown_h1_h6(heading_levels: dict) -> str:
    """Always show H1…H6 counts (0 if absent) for quick scanning."""
    parts = []
    for k in range(1, 7):
        parts.append(f"H{k}×{int(heading_levels.get(k, 0))}")
    return "  ".join(parts)


def _section_line_stats(
    heading_line_nums: list[tuple[int, int, str]],
    total_lines: int,
) -> dict | None:
    """
    Per ATX heading, measure line counts for:
    - **direct**: lines after the heading until the first deeper heading (child), else until peer.
      Excludes nested subsection bodies (only “intro” text before the first child heading).
    - **full**: lines after the heading until the next heading of same or higher outline level
      (next “peer” in the usual sense: same level or climbs toward root). Includes all nested content.
    """
    if not heading_line_nums:
        return None
    n = len(heading_line_nums)
    direct_list: list[int] = []
    full_list: list[int] = []
    for i in range(n):
        L, lv, _ = heading_line_nums[i]
        peer_line: int | None = None
        for j in range(i + 1, n):
            Lj, lvj, _ = heading_line_nums[j]
            if lvj <= lv:
                peer_line = Lj
                break
        first_child_line: int | None = None
        for j in range(i + 1, n):
            Lj, lvj, _ = heading_line_nums[j]
            if peer_line is not None and Lj >= peer_line:
                break
            if lvj > lv:
                first_child_line = Lj
                break
        if first_child_line is not None:
            direct_end = first_child_line - 1
        elif peer_line is not None:
            direct_end = peer_line - 1
        else:
            direct_end = total_lines
        direct_lines = max(0, direct_end - L)
        if peer_line is not None:
            full_end = peer_line - 1
        else:
            full_end = total_lines
        full_lines = max(0, full_end - L)
        direct_list.append(direct_lines)
        full_list.append(full_lines)

    def _triplet(xs: list[int]) -> tuple[int, float, float]:
        if not xs:
            return 0, 0.0, 0.0
        return (
            max(xs),
            float(statistics.mean(xs)),
            float(statistics.median(xs)),
        )

    md, me, mdn = _triplet(direct_list)
    mf, mfe, mfn = _triplet(full_list)
    return {
        "direct_lines_per_heading": direct_list,
        "full_lines_per_heading": full_list,
        "max_direct_lines": md,
        "mean_direct_lines": me,
        "median_direct_lines": mdn,
        "max_full_lines": mf,
        "mean_full_lines": mfe,
        "median_full_lines": mfn,
    }


def _analyse_file(path: Path) -> dict:
    """Return structural metrics for a single markdown file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}

    lines = text.splitlines()
    char_count = len(text)

    # Heading levels, samples, line indices for spacing / duplicates
    heading_levels: Counter = Counter()
    heading_samples: list[dict] = []
    title_norm_counts: Counter = Counter()
    heading_line_nums: list[tuple[int, int, str]] = []  # (line_no_1based, level, title)

    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if not m:
            continue
        level = len(m.group(1))
        raw_title = m.group(2).strip()
        title = raw_title[:200] + ("…" if len(raw_title) > 200 else "")
        heading_levels[level] += 1
        norm = re.sub(r"\s+", " ", raw_title).strip().casefold()
        if norm:
            title_norm_counts[norm] += 1
        heading_line_nums.append((i + 1, level, title))
        if len(heading_samples) < HEADING_SAMPLE_LIMIT:
            heading_samples.append({"level": level, "line": i + 1, "text": title})

    def _gaps_for_level(level_tgt: int) -> list[int]:
        nums = [ln for ln, lv, _ in heading_line_nums if lv == level_tgt]
        out: list[int] = []
        for a, b in zip(nums, nums[1:]):
            g = b - a - 1
            if g >= 0:
                out.append(g)
        return out

    median_gap_by_level: dict[int, float] = {}
    for lv in range(1, 7):
        if not any(l == lv for _, l, _ in heading_line_nums):
            continue
        m = _median(_gaps_for_level(lv))
        if m is not None:
            median_gap_by_level[lv] = m

    duplicate_titles = [(t, c) for t, c in title_norm_counts.items() if c > 1]
    duplicate_titles.sort(key=lambda x: -x[1])
    duplicate_titles = duplicate_titles[:DUPLICATE_HEADING_TOP_N]

    # Typical vertical gap between headings at the split level (heuristic for chunk size)
    split_gaps: list[int] = []
    if len(heading_line_nums) >= 2:
        for a, b in zip(heading_line_nums, heading_line_nums[1:]):
            gap = b[0] - a[0] - 1
            if gap >= 0:
                split_gaps.append(gap)

    # Pipe-style lines (density only — valid GFM tables are a converter concern, not QA here)
    table_line_count = sum(1 for l in lines if l.strip().startswith("|"))
    max_table_run = 0
    run = 0
    for ln in lines:
        if ln.strip().startswith("|"):
            run += 1
            max_table_run = max(max_table_run, run)
        else:
            run = 0

    # Slides
    is_slide_deck = bool(re.search(r"<!-- Slide number: \d+ -->", text))

    # Chapter / section markers (PDF exports). Tighten PART/SECTION so we do not match
    # prose like "part of a team" or "section of the city".
    def _chapter_line(s: str) -> bool:
        """True for lines that look like real chapter headings, not prose ('Chapter 5 and …')."""
        t = s.strip()
        if len(t) > 200:
            return False
        m = re.match(r"^CHAPTER\s+(\d+)\s*(.*)$", t, re.IGNORECASE)
        if not m:
            return False
        rest = (m.group(2) or "").strip()
        if not rest:
            return True
        if rest[0] in ":.":
            body = rest[1:].strip()
            # e.g. "Chapter 3.)" — not a real heading
            if len(body) < 3 or not re.search(r"[A-Za-z]{2,}", body):
                return False
            return True
        # Title-style remainder (TOC / heading), not a sentence starting with 'and', 'or', …
        if rest[0].isupper() and not re.match(
            r"^(and|or|but|if|when|where|as|is|are)\b", rest, re.IGNORECASE
        ):
            return len(t) < 160
        return False

    def _section_line(s: str) -> bool:
        t = s.strip()
        m = re.match(r"^(SECTION|PART|APPENDIX)\s+(\S+)", t, re.IGNORECASE)
        if not m:
            return False
        if len(t) > 200:
            return False
        first_word = m.group(2)
        if first_word and first_word[0].islower():
            return False
        low = t.casefold()
        if re.match(r"^part\s+(of|the|a|an|as|is|in|with)\b", low):
            return False
        if re.match(r"^section\s+(of|the|a|an|in|with)\b", low):
            return False
        return True

    chapter_markers = [l.strip() for l in lines if _chapter_line(l)]
    section_markers = [l.strip() for l in lines if _section_line(l)]

    # Noise indicators
    noise_patterns = sum(
        1 for l in lines
        if re.match(r"^\d+$", l.strip())          # bare page numbers
        or re.match(r"^page\s+\d+", l, re.IGNORECASE)
    )

    # Code fences
    code_fence_count = len(re.findall(r"^```", text, re.MULTILINE))

    # True when chapter/section cues appear as ATX headings (after PDF post-process), not only as bare lines
    has_chapter_in_atx = bool(re.search(r"(?m)^#{1,6}\s+CHAPTER\s+\d+\b", text, re.IGNORECASE))
    has_appendix_part_in_atx = bool(
        re.search(r"(?m)^#{1,6}\s+(?:APPENDIX|PART)\b", text, re.IGNORECASE)
    )

    total_headings = int(sum(heading_levels.values()))
    deepest_level = max(heading_levels, default=0)
    section_line_stats = _section_line_stats(heading_line_nums, len(lines))

    return {
        "line_count": len(lines),
        "char_count": char_count,
        "heading_levels": dict(heading_levels),
        "heading_total": total_headings,
        "heading_deepest_level": deepest_level,
        "section_line_stats": section_line_stats,
        "has_chapter_in_atx": has_chapter_in_atx,
        "has_appendix_part_in_atx": has_appendix_part_in_atx,
        "heading_samples": heading_samples,
        "all_headings": heading_line_nums,  # (line_1based, level, title) — full ATX list for outline report
        "duplicate_heading_counts": duplicate_titles,
        "median_lines_between_headings": _median(split_gaps),
        "median_gap_by_level": median_gap_by_level,
        "max_table_run_lines": max_table_run,
        "table_line_count": table_line_count,
        "is_slide_deck": is_slide_deck,
        "chapter_markers": chapter_markers[:12],
        "section_markers": section_markers[:12],
        "chapter_marker_count": len(chapter_markers),
        "section_marker_count": len(section_markers),
        "noise_lines": noise_patterns,
        "code_fence_count": code_fence_count,
    }


def _build_spec(analyses: list[dict], src: Path) -> dict:
    """Derive sensible defaults from aggregate structural metrics."""
    total_files = len(analyses)
    if total_files == 0:
        return _default_spec()

    any_chapter = any(a.get("chapter_markers") for a in analyses) or any(
        a.get("has_chapter_in_atx") for a in analyses
    )
    any_section_marker = any(a.get("section_markers") for a in analyses) or any(
        a.get("has_appendix_part_in_atx") for a in analyses
    )
    all_heading_levels: Counter = Counter()
    for a in analyses:
        all_heading_levels.update(a.get("heading_levels", {}))

    has_h1 = all_heading_levels.get(1, 0) > 0
    has_h2 = all_heading_levels.get(2, 0) > 0
    has_h3 = all_heading_levels.get(3, 0) > 0

    total_lines = sum(a.get("line_count", 0) for a in analyses)
    avg_lines = total_lines // max(total_files, 1)

    # --- section_boundaries ---
    chapter_break_regex = ""
    section_break_regex = ""

    if any_chapter:
        chapter_break_regex = r"^CHAPTER\s+\d+"
    elif has_h1:
        chapter_break_regex = r"^#\s+"

    if any_section_marker:
        section_break_regex = r"^(?:SECTION|PART|APPENDIX)\s+"
    elif has_h2:
        section_break_regex = r"^##\s+"
    elif has_h1 and not chapter_break_regex:
        section_break_regex = r"^#\s+"

    all_caps_standalone = any_chapter or any_section_marker

    # --- splitting ---
    # Larger files → allow bigger chunks to preserve coherence
    if avg_lines > 500:
        min_chars, max_chars = 400, 8000
    elif avg_lines > 100:
        min_chars, max_chars = 300, 4000
    else:
        min_chars, max_chars = 150, 2000

    split_on_heading_level = 2
    if has_h3 and all_heading_levels.get(3, 0) > all_heading_levels.get(2, 0):
        split_on_heading_level = 3

    any_tables = any(a.get("table_line_count", 0) > 0 for a in analyses)

    # --- defaults: placeholders until taxonomy is filled from this source ---
    default_evidence_type = "unspecified"
    default_chunk_type = "unspecified"

    return {
        "section_boundaries": {
            "chapter_break_regex": chapter_break_regex,
            "section_break_regex": section_break_regex,
            "all_caps_standalone": all_caps_standalone,
        },
        "splitting": {
            "min_chunk_chars": min_chars,
            "max_chunk_chars": max_chars,
            "keep_markdown_tables_intact": any_tables,
            "split_on_heading_level": split_on_heading_level,
        },
        "defaults": {
            "evidence_type": default_evidence_type,
            "chunk_type": default_chunk_type,
        },
        "taxonomy": _empty_taxonomy(),
    }


def _empty_taxonomy() -> dict:
    """No preset type lists — AI/human derives labels per source after reading the manuscript."""
    return {"evidence_type": [], "chunk_type": []}


def _default_spec() -> dict:
    return {
        "section_boundaries": {
            "chapter_break_regex": r"^#\s+",
            "section_break_regex": r"^##\s+",
            "all_caps_standalone": False,
        },
        "splitting": {
            "min_chunk_chars": 300,
            "max_chunk_chars": 4000,
            "keep_markdown_tables_intact": True,
            "split_on_heading_level": 2,
        },
        "defaults": {
            "evidence_type": "unspecified",
            "chunk_type": "unspecified",
        },
        "taxonomy": _empty_taxonomy(),
    }


# ---------------------------------------------------------------------------
# YAML serialiser (no dependency on PyYAML for portability)
# ---------------------------------------------------------------------------

def _to_yaml_str(value, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{k}:")
                lines.append(_to_yaml_str(v, indent + 1))
            else:
                lines.append(f"{pad}{k}: {_yaml_scalar(v)}")
        return "\n".join(lines)
    elif isinstance(value, list):
        items = ", ".join(_yaml_scalar(i) for i in value)
        return f"{pad}[{items}]"
    else:
        return f"{pad}{_yaml_scalar(value)}"


def _yaml_scalar(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if v == "":
        return '""'
    # Quote strings that look like regexes or contain special YAML chars
    if any(c in str(v) for c in r':{}[]|>&*!,#?-"'):
        escaped = str(v).replace('"', '\\"')
        return f'"{escaped}"'
    return str(v)


def _build_yaml_document(spec: dict, src: Path, files: list[Path]) -> str:
    lines = [
        "# context_chunking_spec.yaml — drafted by draft_chunking_spec.py",
        "# Review and edit before running chunk_markdown.py.",
        f"# Sources scanned: {len(files)} markdown file(s) under {src.name}/",
        "#",
        "# section_boundaries: regexes that start a new major structural unit.",
        "# splitting: size limits and table handling for the chunk emitter.",
        "# defaults: placeholders until you set real defaults after taxonomy is filled.",
        "# taxonomy: STARTS EMPTY — do not add a canned list here. Agent (or human) reads the source and",
        "#   proposes evidence_type + chunk_type enums for THIS corpus only. Types are not shared across sources.",
        "",
    ]

    section_b = spec["section_boundaries"]
    splitting = spec["splitting"]
    defaults = spec["defaults"]
    taxonomy = spec["taxonomy"]

    lines.append("section_boundaries:")
    lines.append(f'  chapter_break_regex: "{section_b["chapter_break_regex"]}"')
    lines.append(f'  section_break_regex: "{section_b["section_break_regex"]}"')
    lines.append(f"  all_caps_standalone: {_yaml_scalar(section_b['all_caps_standalone'])}")
    lines.append("")

    lines.append("splitting:")
    lines.append(f"  min_chunk_chars: {splitting['min_chunk_chars']}")
    lines.append(f"  max_chunk_chars: {splitting['max_chunk_chars']}")
    lines.append(f"  keep_markdown_tables_intact: {_yaml_scalar(splitting['keep_markdown_tables_intact'])}")
    lines.append(f"  split_on_heading_level: {splitting['split_on_heading_level']}")
    lines.append("")

    lines.append("defaults:")
    lines.append(f"  evidence_type: {defaults['evidence_type']}")
    lines.append(f"  chunk_type: {defaults['chunk_type']}")
    lines.append("")

    lines.append("taxonomy:")
    et = ", ".join(taxonomy["evidence_type"])
    ct = ", ".join(taxonomy["chunk_type"])
    lines.append(f"  evidence_type: [{et}]")
    lines.append(f"  chunk_type: [{ct}]")
    if not taxonomy.get("evidence_type") and not taxonomy.get("chunk_type"):
        lines.append("  # Fill lists above after analyzing this source (AI or human). No fixed vocabulary in tooling.")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Structural report (stdout + .txt + .md on disk)
# ---------------------------------------------------------------------------

def _atx_outline_lines(
    all_headings: list[tuple[int, int, str]],
    *,
    collapse_consecutive_duplicates: bool = True,
    max_level: int | None = None,
) -> list[str]:
    """Render headings as ATX lines (`#` … `######`). Optionally drop consecutive identical (level, title)."""
    cap = STRUCTURAL_OUTLINE_MAX_LEVEL if max_level is None else max_level
    out: list[str] = []
    last_key: tuple[int, str] | None = None
    for _line_no, level, title in all_headings:
        lv = min(max(int(level), 1), 6)
        if cap is not None and lv > cap:
            continue
        t = " ".join(title.replace("\n", " ").split()).strip()
        if not t:
            continue
        key = (lv, re.sub(r"\s+", " ", t).casefold())
        if collapse_consecutive_duplicates and key == last_key:
            continue
        last_key = key
        out.append(f"{'#' * lv} {t}")
    return out


def _format_structural_report(analyses: list[dict], spec: dict, files: list[Path]) -> str:
    """Detailed plain-text report for console and structural_scan_report.txt."""
    sp = spec["splitting"]
    split_lv = sp["split_on_heading_level"]
    lines: list[str] = []
    lines.append("")
    lines.append("=" * 72)
    lines.append("  STRUCTURAL SCAN REPORT (abd-context-to-memory / draft_chunking_spec)")
    lines.append("=" * 72)

    all_levels: Counter = Counter()
    for a in analyses:
        all_levels.update(a.get("heading_levels", {}))

    lines.append(f"  Files scanned: {len(files)}")
    if all_levels:
        hb = _heading_breakdown_h1_h6(dict(all_levels))
        tot_all = sum(all_levels.values())
        deepest_all = max(all_levels.keys(), default=0)
        lines.append(f"  Headings (all files): {hb}")
        lines.append(f"  ATX headings total: {tot_all}  |  deepest level used: H{deepest_all}")

    slide_files = [f for f, a in zip(files, analyses) if a.get("is_slide_deck")]
    if slide_files:
        lines.append(
            f"  Slide decks: {len(slide_files)} ({', '.join(f.name for f in slide_files[:4])}{'...' if len(slide_files) > 4 else ''})"
        )

    lines.append("")
    lines.append("-" * 72)
    lines.append("  PER-FILE SUMMARY")
    lines.append(
        "  (direct section = lines before first deeper # under same heading; full = through next peer #, nested included)"
    )
    lines.append("-" * 72)
    for f, a in zip(files, analyses):
        if not a:
            lines.append(f"  {f.name}: (read failed)")
            continue
        hl = a.get("heading_levels") or {}
        hb = _heading_breakdown_h1_h6(hl) if hl else "(no ATX headings)"
        htot = a.get("heading_total", 0)
        hdeep = a.get("heading_deepest_level", 0)
        chars = a.get("char_count", 0)
        tbl = a.get("table_line_count", 0)
        mrun = a.get("max_table_run_lines", 0)
        noise = a.get("noise_lines", 0)
        lines.append(f"  • {f.name}")
        lines.append(
            f"      lines {a.get('line_count', 0):,}  chars {chars:,}"
        )
        lines.append(
            f"      headings: {hb}"
        )
        lines.append(
            f"      ATX total: {htot}  |  deepest: H{hdeep}"
        )
        sls = a.get("section_line_stats")
        if sls:
            lines.append(
                "      section lines — direct (body before first child heading; excludes nested blocks): "
                f"max {sls['max_direct_lines']:,}  avg {sls['mean_direct_lines']:.1f}  med {sls['median_direct_lines']:.1f}"
            )
            lines.append(
                "      section lines — full (through next peer #; includes all nested content): "
                f"max {sls['max_full_lines']:,}  avg {sls['mean_full_lines']:.1f}  med {sls['median_full_lines']:.1f}"
            )
        lines.append(
            f"      table lines: {tbl:,}  longest table run: {mrun} lines  |  noise-ish lines: {noise}  |  code fences: {a.get('code_fence_count', 0)}"
        )
        mg = a.get("median_gap_by_level") or {}
        gap_bits = []
        for lv in (2, 3, 4):
            if lv in mg and mg[lv] is not None:
                gap_bits.append(f"H{lv} median gap {mg[lv]:.1f} lines")
        if gap_bits:
            lines.append(f"      spacing: {'; '.join(gap_bits)}")
        dup = a.get("duplicate_heading_counts") or []
        if dup:
            max_rep = max(c for _, c in dup)
            lines.append(f"      duplicate titles: {len(dup)} groups (max repeat ×{max_rep})")
        ch = a.get("chapter_marker_count", 0)
        se = a.get("section_marker_count", 0)
        if ch or se:
            lines.append(f"      CHAPTER/PART-style lines: CHAPTER×{ch}  SECTION/PART/APPENDIX×{se}")

    lines.append("")
    lines.append("-" * 72)
    _cap = STRUCTURAL_OUTLINE_MAX_LEVEL
    cap_note = f"max H{_cap}" if _cap is not None else "all levels"
    lines.append(
        f"  HEADING OUTLINE (# … {cap_note}; consecutive duplicate titles omitted)"
    )
    lines.append("-" * 72)
    for f, a in zip(files, analyses):
        heads = a.get("all_headings") or []
        if not heads:
            lines.append(f"  [{f.name}]")
            lines.append("    (no ATX headings)")
            lines.append("")
            continue
        lines.append(f"  [{f.name}]")
        for atx in _atx_outline_lines(heads):
            lines.append(f"  {atx}")
        lines.append("")

    lines.append("")
    lines.append("-" * 72)
    lines.append("  RAW CHAPTER / SECTION MARKER LINES (samples)")
    lines.append("-" * 72)
    for f, a in zip(files, analyses):
        cm = a.get("chapter_markers") or []
        sm = a.get("section_markers") or []
        if not cm and not sm:
            continue
        lines.append(f"  [{f.name}]")
        for x in cm[:8]:
            lines.append(f"    CHAPTER-line: {x[:100]}{'…' if len(x) > 100 else ''}")
        for x in sm[:8]:
            lines.append(f"    SECTION-line: {x[:100]}{'…' if len(x) > 100 else ''}")

    chapter_files = [f for f, a in zip(files, analyses) if a.get("chapter_markers")]
    if chapter_files:
        lines.append("")
        lines.append(f"  Chapter-style markers present in: {', '.join(f.name for f in chapter_files)}")

    table_files = [(f, a) for f, a in zip(files, analyses) if a.get("table_line_count", 0) > 0]
    if table_files:
        lines.append("")
        lines.append(f"  Tables: present in {len(table_files)} file(s). Longest single table run limits how small max_chunk_chars can be.")

    noise_files = [(f, a) for f, a in zip(files, analyses) if a.get("noise_lines", 0) > 5]
    if noise_files:
        lines.append("")
        lines.append(
            f"  Possible noise (bare page numbers, 'Page N'): {len(noise_files)} file(s) — review or strip in conversion."
        )

    lines.append("")
    lines.append("-" * 72)
    lines.append("  DRAFTED SPEC (context_chunking_spec.yaml)")
    lines.append("-" * 72)
    cb = spec["section_boundaries"]["chapter_break_regex"] or "(none)"
    sb = spec["section_boundaries"]["section_break_regex"] or "(none)"
    lines.append(f"  chapter_break_regex   : {cb}")
    lines.append(f"  section_break_regex   : {sb}")
    lines.append(f"  split_on_heading_level: {split_lv}  (H{split_lv})")
    mg_split = None
    for a in analyses:
        mgl = a.get("median_gap_by_level") or {}
        if split_lv in mgl:
            mg_split = mgl[split_lv]
            break
    if mg_split is not None:
        lines.append(
            f"  hint: median lines between consecutive H{split_lv} headings ≈ {mg_split:.1f} (spacing proxy; 0 often means stacked TOC-style lines)"
        )
    lines.append(f"  chunk_chars           : {sp['min_chunk_chars']} – {sp['max_chunk_chars']}")
    lines.append(
        f"  defaults              : evidence_type={spec['defaults']['evidence_type']}  chunk_type={spec['defaults']['chunk_type']}"
    )

    lines.append("")
    lines.append("-" * 72)
    lines.append("  WHAT TO DO NEXT")
    lines.append("-" * 72)
    lines.append("  1. Skim the heading outline above — structure should match how you want chunks to break.")
    lines.append("  2. If headings are wrong or sparse, fix PDF→Markdown (pdf_markdown_post / outline), not this scanner.")
    lines.append("  3. Edit context_chunking_spec.yaml: taxonomy (evidence_type, chunk_type), then tune min/max chunk chars.")
    lines.append("  4. Run chunk_markdown.py --path <this folder>.")
    lines.append("")
    lines.append("  ASSUMPTIONS / REVIEW")
    if not spec["section_boundaries"]["chapter_break_regex"]:
        lines.append("  ⚠  No chapter boundary regex — add one if the manuscript has clear chapter breaks.")
    if not spec["section_boundaries"]["section_break_regex"]:
        lines.append("  ⚠  No section boundary regex — add one if needed.")
    if not any(a.get("heading_levels") for a in analyses):
        lines.append("  ⚠  No ATX headings — chunking falls back to coarse splits; fix conversion if headings expected.")
    lines.append("  ✎  taxonomy starts empty; fill after reading the source. No global enum in tooling.")
    lines.append("  ✎  If max_table_run is large, keep max_chunk_chars above the largest table block or split tables in preprocessing.")

    lines.append("=" * 72)
    lines.append("")
    return "\n".join(lines)


def _format_structural_report_markdown(analyses: list[dict], spec: dict, files: list[Path]) -> str:
    """Same information as the .txt report, formatted for reading in an editor or LLM."""
    sp = spec["splitting"]
    split_lv = sp["split_on_heading_level"]
    out: list[str] = [
        "# Structural scan report",
        "",
        "Generated by `draft_chunking_spec.py`. Use this together with `context_chunking_spec.yaml`.",
        "",
        "## Aggregate",
        "",
    ]
    all_levels: Counter = Counter()
    for a in analyses:
        all_levels.update(a.get("heading_levels", {}))
    if all_levels:
        out.append("| Level | Count |")
        out.append("|-------|-------|")
        for k, v in sorted(all_levels.items()):
            out.append(f"| H{k} | {v} |")
        out.append("")
        tot_all = sum(all_levels.values())
        deepest_all = max(all_levels.keys(), default=0)
        out.append(f"- **ATX headings (all files):** {tot_all}")
        out.append(f"- **Deepest level (all files):** H{deepest_all}")
        out.append("")
        out.append("Full H1–H6 breakdown (all files): `" + _heading_breakdown_h1_h6(dict(all_levels)) + "`")
        out.append("")
    out.append(f"- **Files scanned:** {len(files)}")
    out.append("")

    out.append("## Per file")
    out.append("")
    out.append(
        "For each ATX heading, **direct** = lines from that heading through the line before the first "
        "deeper child heading (intro only; excludes nested subsection bodies). "
        "**Full** = lines until the next heading of the same or higher level (peer), including all nested content."
    )
    out.append("")
    for f, a in zip(files, analyses):
        out.append(f"### `{f.name}`")
        out.append("")
        if not a:
            out.append("*Read failed.*")
            out.append("")
            continue
        hl = a.get("heading_levels") or {}
        out.append("| Metric | Value |")
        out.append("|--------|------:|")
        out.append(f"| Lines | {a.get('line_count', 0):,} |")
        out.append(f"| Chars | {a.get('char_count', 0):,} |")
        out.append(f"| H1–H6 | {_heading_breakdown_h1_h6(hl) if hl else '—'} |")
        out.append(f"| ATX headings total | {a.get('heading_total', 0)} |")
        out.append(f"| Deepest level | H{a.get('heading_deepest_level', 0)} |")
        sls = a.get("section_line_stats")
        if sls:
            out.append(
                f"| Section lines — **direct** (max / avg / med) | {sls['max_direct_lines']:,} / "
                f"{sls['mean_direct_lines']:.1f} / {sls['median_direct_lines']:.1f} |"
            )
            out.append(
                f"| Section lines — **full** (max / avg / med) | {sls['max_full_lines']:,} / "
                f"{sls['mean_full_lines']:.1f} / {sls['median_full_lines']:.1f} |"
            )
        out.append(f"| Table lines | {a.get('table_line_count', 0):,} |")
        out.append(f"| Longest table run | {a.get('max_table_run_lines', 0)} |")
        out.append(f"| Noise-ish lines | {a.get('noise_lines', 0)} |")
        out.append(f"| Code fences | {a.get('code_fence_count', 0)} |")
        out.append("")

    out.append("### Median line gap between same-level headings")
    out.append("")
    out.append("Rough proxy for how many lines of prose sit under each heading tier (helps guess chunk size).")
    out.append("")
    for f, a in zip(files, analyses):
        mg = a.get("median_gap_by_level") or {}
        if not mg:
            continue
        bits = ", ".join(f"H{lv}: **{val:.1f}**" for lv, val in sorted(mg.items()) if val is not None)
        out.append(f"- `{f.name}`: {bits}")
    out.append("")

    out.append("## Heading outline")
    out.append("")
    _md_cap = STRUCTURAL_OUTLINE_MAX_LEVEL
    _cap_desc = (
        f"Headings deeper than **H{_md_cap}** are omitted here (set `STRUCTURAL_OUTLINE_MAX_LEVEL` in `draft_chunking_spec.py`; `None` = show all)."
        if _md_cap is not None
        else "All heading levels are included."
    )
    out.append(
        "ATX hierarchy as in the source (`#` … `######`). "
        "**Consecutive** duplicate titles (e.g. repeated running headers) are omitted once. "
        + _cap_desc
    )
    out.append("")
    for f, a in zip(files, analyses):
        heads = a.get("all_headings") or []
        out.append(f"### `{f.name}`")
        out.append("")
        if not heads:
            out.append("*No ATX headings.*")
            out.append("")
            continue
        out.append("```markdown")
        for atx in _atx_outline_lines(heads):
            out.append(atx)
        out.append("```")
        out.append("")

    out.append("## Draft spec summary")
    out.append("")
    out.append("| Key | Value |")
    out.append("|-----|-------|")
    cb = spec["section_boundaries"]["chapter_break_regex"] or "*(none)*"
    sb = spec["section_boundaries"]["section_break_regex"] or "*(none)*"
    out.append(f"| chapter_break_regex | `{cb}` |")
    out.append(f"| section_break_regex | `{sb}` |")
    out.append(f"| split_on_heading_level | **H{split_lv}** |")
    out.append(f"| chunk_chars | {sp['min_chunk_chars']} – {sp['max_chunk_chars']} |")
    out.append("")
    out.append("## Next steps")
    out.append("")
    out.append("1. Confirm heading samples match the structure you want for RAG chunks.")
    out.append("2. If not, improve **conversion** (e.g. `pdf_markdown_post.py`), not this scanner.")
    out.append("3. Fill **taxonomy** in `context_chunking_spec.yaml`, then run `chunk_markdown.py`.")
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _get_arg(flag: str) -> str | None:
    if flag in sys.argv:
        idx = sys.argv.index(flag)
        if idx + 1 < len(sys.argv):
            return sys.argv[idx + 1]
    return None


def draft_spec(src: Path, force: bool = False) -> Path | None:
    """
    Scan markdown, write structural reports under src/markdown/, draft chunking spec under src/memory/.
    Structural reports are always refreshed when a scan runs. The YAML in memory/ is skipped if it
    already exists unless --force (legacy: yaml under markdown/ or topic root counts as “have a spec”).
    """
    md_reports = _markdown_reports_dir(src)
    spec_path = _memory_spec_path(src)
    legacy_md_spec = md_reports / SPEC_FILENAME
    legacy_root_spec = src / SPEC_FILENAME

    files = _collect_md_files(src)
    if not files:
        print(f"No markdown files found under {src}.")
        print("Run convert_to_markdown.py first.")
        return None

    print(f"Scanning {len(files)} markdown file(s) in {src.name}/...")
    analyses = []
    for f in files:
        analyses.append(_analyse_file(f))

    spec = _build_spec(analyses, src)
    report_text = _format_structural_report(analyses, spec, files)
    print(report_text, end="")
    md_reports.mkdir(parents=True, exist_ok=True)
    report_path = md_reports / REPORT_FILENAME
    report_path.write_text(report_text, encoding="utf-8")
    print(f"Structural scan report written: {report_path}")
    report_md_path = md_reports / REPORT_MD_FILENAME
    report_md_path.write_text(
        _format_structural_report_markdown(analyses, spec, files), encoding="utf-8"
    )
    print(f"Structural scan report (Markdown): {report_md_path}")

    have_spec = (
        spec_path.exists()
        or legacy_md_spec.exists()
        or legacy_root_spec.exists()
    )
    if have_spec and not force:
        existing = (
            spec_path
            if spec_path.exists()
            else (legacy_md_spec if legacy_md_spec.exists() else legacy_root_spec)
        )
        print(
            f"Chunking spec already present ({existing}); not overwriting. "
            "Use --force to re-draft into memory/context_chunking_spec.yaml."
        )
        print("NEXT: Edit memory/context_chunking_spec.yaml if needed, then run chunk_markdown.py.")
        return existing

    mem_dir = spec_path.parent
    mem_dir.mkdir(parents=True, exist_ok=True)
    yaml_text = _build_yaml_document(spec, src, files)
    spec_path.write_text(yaml_text, encoding="utf-8")
    print(f"Chunking spec written: {spec_path}")
    print("NEXT: Fill taxonomy from source (AI or human), review boundaries/splits, then run chunk_markdown.py.")
    return spec_path


def main():
    path_arg = _get_arg("--path")
    force = "--force" in sys.argv

    if not path_arg:
        src = ROOT
    else:
        src = Path(path_arg)
        if not src.is_absolute():
            src = ROOT / src
    if not src.exists():
        print(f"ERROR: folder not found: {src}")
        sys.exit(1)

    result = draft_spec(src, force=force)
    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
