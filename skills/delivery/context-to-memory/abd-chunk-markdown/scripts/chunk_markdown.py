"""
Chunk converted markdown into smaller pieces for agent memory.

**Role:** This step **splits** along headings, regex boundaries, and size limits from
``context_chunking_spec.yaml``. It does **not** compose or decompose the author's structure—
that belongs in **conversion and markdown post-process** (see skill docs: *Chunker vs converter*).
If the source ``.md`` is a flat blob, fix the markdown first; the chunker will not recover hierarchy.

Usage:
  python chunk_markdown.py --path <source_folder> [--memory <subfolder>]
  python chunk_markdown.py --path <source_folder> --output <output_dir>

Run from topic folder or set CONTENT_MEMORY_ROOT. Reads .md from source folder, writes chunked output to:
  --output <dir>   : exact directory (absolute or relative to cwd)
  (default)        : memory/ under topic root — chunks go here directly (no extra folder named after the project)
  --memory <name>  : optional nested folder memory/<name>/ (only when you want a sub-corpus under memory/)
Run convert_to_markdown.py first. Excludes chunked output (__slide_, __section_) from input.

**Sources:** For each logical document (same folder + stem), prefer ``<topic>/markdown/.../<stem>.md``
(parallel tree), then legacy ``.../markdown/<stem>.md`` beside originals, then sibling ``.../<stem>.md``.
Never duplicate chunks. **Output:** Chunks go under ``memory/`` mirroring the source tree **without**
a ``markdown`` path segment (e.g. ``markdown/notes/foo.md`` -> ``memory/notes/foo__slide_01.md``).

**Layout:** With ``--output <source>/memory``, markdown under ``<source>/memory/`` is never input
(output only).

**Folder named ``context``:** Pass ``--path`` as the **project root** (parent of ``context``) and
``--output`` to ``<project>/memory/context`` so converted markdown under ``<project>/markdown/`` is
found. (``index_memory`` does this automatically.)

**Chunking spec:** Loads ``<topic>/memory/context_chunking_spec.yaml`` if present, else legacy ``markdown/`` or topic root.
After the primary split (``split_on_heading_level``), any piece longer than ``splitting.max_chunk_chars`` is split again using **exact** ``####``, ``#####``, … headings for that slice only; if still too large, paragraph/line windows are used.
Structural rules: ``section_boundaries``, ``splitting``. Optional ``chunk_inputs``: a list of topic-relative
paths (e.g. ``["markdown/Book.md"]``); when set, only those files are chunked (skips backups under
``archive/``, notes, etc.). Types: after the AI decides ``evidence_type`` / ``chunk_type`` vocabulary
for the corpus, it writes them into **that same file** (``taxonomy`` plus ``defaults`` for usual chunk
labels). Chunks get YAML front matter from ``defaults``. If ``taxonomy`` lists are non-empty and
``defaults`` are not members, a warning is printed. Run ``draft_chunking_spec.py`` first for
boundaries/splits only; then have the agent fill types in the YAML.
"""

import re
import sys
from pathlib import Path
from typing import Any

from _config import ROOT, MEMORY, ASSETS, ensure_root

ensure_root()
MIN_CHUNK_LINES = 5
SPEC_FILENAME = "context_chunking_spec.yaml"


# ---------------------------------------------------------------------------
# Chunking spec loading
# ---------------------------------------------------------------------------

def _resolve_spec_path(src_root: Path) -> Path | None:
    """memory/ (canonical), then legacy markdown/, then topic root."""
    mem_spec = src_root / "memory" / SPEC_FILENAME
    md_spec = src_root / "markdown" / SPEC_FILENAME
    root_spec = src_root / SPEC_FILENAME
    if mem_spec.exists():
        return mem_spec
    if md_spec.exists():
        return md_spec
    if root_spec.exists():
        return root_spec
    return None


def _load_spec(src_root: Path) -> dict[str, Any] | None:
    """Load context_chunking_spec.yaml from memory/ or legacy paths."""
    spec_path = _resolve_spec_path(src_root)
    if spec_path is None:
        return None
    try:
        return _parse_yaml(spec_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  Warning: could not parse {spec_path}: {e}")
        return None


def _parse_yaml(text: str) -> dict[str, Any]:
    """Minimal YAML parser for the spec structure (avoids PyYAML dependency)."""
    result: dict[str, Any] = {}
    current_section: str | None = None
    current_dict: dict[str, Any] = {}

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        # Top-level key (no leading space)
        if not raw_line.startswith(" ") and ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "" or val.startswith("#"):
                if current_section:
                    result[current_section] = current_dict
                current_section = key
                current_dict = {}
            else:
                if current_section:
                    result[current_section] = current_dict
                    current_section = None
                    current_dict = {}
                result[key] = _parse_scalar(val)
            continue

        # Indented key under current section
        if current_section and line.lstrip():
            stripped = line.lstrip()
            if ":" in stripped:
                k, _, v = stripped.partition(":")
                k = k.strip()
                v = v.strip()
                if v == "" or v.startswith("#"):
                    continue
                current_dict[k] = _parse_scalar(v)

    if current_section:
        result[current_section] = current_dict

    return result


def _parse_scalar(val: str) -> Any:
    """Parse a YAML scalar: bool, int, list, or string."""
    val = val.split("#")[0].strip()  # strip inline comments
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    try:
        return int(val)
    except ValueError:
        pass
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1]
        return [item.strip().strip('"').strip("'") for item in inner.split(",") if item.strip()]
    # Strip surrounding quotes
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    return val


def _spec_section_break_regex(spec: dict) -> re.Pattern | None:
    sb = spec.get("section_boundaries", {})
    chapter = sb.get("chapter_break_regex", "")
    section = sb.get("section_break_regex", "")
    patterns = [p for p in [chapter, section] if p]
    if not patterns:
        return None
    combined = "|".join(f"(?:{p})" for p in patterns)
    try:
        return re.compile(combined, re.IGNORECASE)
    except re.error:
        return None


def _spec_min_lines(spec: dict) -> int:
    splitting = spec.get("splitting", {})
    min_chars = splitting.get("min_chunk_chars", 150)
    return max(3, min_chars // 80)  # rough chars-to-lines conversion


def _spec_max_lines(spec: dict) -> int:
    splitting = spec.get("splitting", {})
    max_chars = splitting.get("max_chunk_chars", 4000)
    return max_chars // 60


def _spec_split_heading_level(spec: dict) -> int:
    return spec.get("splitting", {}).get("split_on_heading_level", 2)


def _spec_keep_tables_intact(spec: dict | None) -> bool | None:
    """From YAML ``splitting.keep_markdown_tables_intact`` (drafter usually sets true).

    The chunker does **not** repair or reformat tables—that is a **conversion** concern.
    Splits happen only at headings, slide markers, or ``section_boundaries`` regexes; this
    flag is surfaced for transparency until optional future logic avoids splitting inside pipe blocks.
    """
    if not spec:
        return None
    v = spec.get("splitting", {}).get("keep_markdown_tables_intact")
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in ("true", "1", "yes")
    return bool(v)


def _spec_defaults(spec: dict) -> tuple[str, str]:
    """Default evidence_type (surface form) and chunk_type (role in source). Legacy: modeling_kind → chunk_type."""
    d = spec.get("defaults", {})
    et = d.get("evidence_type", "prose")
    ct = d.get("chunk_type") or d.get("modeling_kind", "prose_block")
    return et, ct


def _log_taxonomy_from_spec(spec: dict) -> None:
    """Show types the AI (or human) put in context_chunking_spec.yaml — chunker reads defaults from same file."""
    tax = spec.get("taxonomy") or {}
    et = tax.get("evidence_type") or []
    ct = tax.get("chunk_type") or []
    if not et and not ct:
        print(
            "  WARNING: taxonomy.evidence_type and taxonomy.chunk_type are still empty. "
            "Secondary pass: classify this corpus, fill both lists and defaults "
            "(see skill content/parts/library/chunking-spec.md), then re-run chunk_markdown."
        )
        return
    if et:
        preview = ", ".join(et[:14])
        more = f" (+{len(et) - 14} more)" if len(et) > 14 else ""
        print(f"  taxonomy.evidence_type ({len(et)}): {preview}{more}")
    if ct:
        preview = ", ".join(ct[:14])
        more = f" (+{len(ct) - 14} more)" if len(ct) > 14 else ""
        print(f"  taxonomy.chunk_type ({len(ct)}): {preview}{more}")


def _warn_defaults_vs_taxonomy(spec: dict) -> None:
    """If taxonomy lists are non-empty, defaults should be members (AI usually sets both together)."""
    tax = spec.get("taxonomy") or {}
    defs = spec.get("defaults") or {}
    et_allow = tax.get("evidence_type") or []
    ct_allow = tax.get("chunk_type") or []
    if not et_allow and not ct_allow:
        return
    et = defs.get("evidence_type")
    ct = defs.get("chunk_type") or defs.get("modeling_kind")
    if et_allow and et is not None and str(et) not in et_allow:
        print(f"  Warning: defaults.evidence_type {et!r} is not in taxonomy.evidence_type — fix YAML.")
    if ct_allow and ct is not None and str(ct) not in ct_allow:
        print(f"  Warning: defaults.chunk_type {ct!r} is not in taxonomy.chunk_type — fix YAML.")


def _warn_placeholder_defaults(spec: dict) -> None:
    """Remind to replace draft placeholders left by draft_chunking_spec or older edits."""
    defs = spec.get("defaults") or {}
    et = (defs.get("evidence_type") or "").strip().lower()
    ct = (defs.get("chunk_type") or defs.get("modeling_kind") or "").strip().lower()
    if et == "unspecified" or ct == "unspecified":
        print(
            "  WARNING: defaults still contain 'unspecified'. Set evidence_type / chunk_type "
            "to members of taxonomy (e.g. mixed + rules_chapter); see chunking-spec.md."
        )


def _find_image_refs(text: str) -> list[str]:
    return re.findall(r"!\[[^\]]*\]\(<?([^)>]+)>?\)", text)


def _copy_images(refs: list[str], src_base: Path, dst_base: Path):
    import shutil
    for ref in refs:
        src = src_base / ref
        if not src.exists():
            continue
        dst = dst_base / ref
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(str(src), str(dst))


def _chunk_by_slides(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"(<!-- Slide number: \d+ -->)", text)
    chunks, current_label, current_lines = [], "preamble", []

    for part in parts:
        m = re.match(r"<!-- Slide number: (\d+) -->", part)
        if m:
            if current_lines and "".join(current_lines).strip():
                chunks.append((current_label, "".join(current_lines)))
            current_label = f"slide_{int(m.group(1)):02d}"
            current_lines = [part]
        else:
            current_lines.append(part)

    if current_lines and "".join(current_lines).strip():
        chunks.append((current_label, "".join(current_lines)))
    return chunks


def _chunk_by_headings(text: str, heading_level: int = 2) -> list[tuple[str, str]]:
    pat = re.compile(r"^#{1," + str(heading_level) + r"}\s", re.MULTILINE)
    lines = text.split("\n")
    chunks, current_lines, chunk_idx = [], [], 0

    for line in lines:
        if pat.match(line) and len(current_lines) >= MIN_CHUNK_LINES:
            chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
            current_lines, chunk_idx = [], chunk_idx + 1
        current_lines.append(line)

    if current_lines:
        chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
    return chunks


def _chunk_by_exact_heading_level(text: str, level: int) -> list[str]:
    """Split at lines that are **exactly** ``level`` markdown headings (``#``…``######``).

    Used when a coarse chunk still exceeds ``max_chunk_chars``: split one level finer
    (``split_on_heading_level`` + 1, then +2, …) for that slice only.
    """
    if level < 1 or level > 6:
        return [text]
    pat = re.compile("^" + "#" * level + r"(?![#])\s", re.MULTILINE)
    lines = text.split("\n")
    chunks: list[str] = []
    current_lines: list[str] = []
    for line in lines:
        if pat.match(line) and len(current_lines) >= MIN_CHUNK_LINES:
            chunks.append("\n".join(current_lines))
            current_lines = []
        current_lines.append(line)
    if current_lines:
        chunks.append("\n".join(current_lines))
    return [c for c in chunks if c.strip()]


def _hard_split_oversized(text: str, max_chars: int) -> list[str]:
    """Last resort when no finer headings exist: pack paragraphs, then lines, then fixed windows."""
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    paras = [p for p in re.split(r"\n{2,}", text) if p.strip()]
    if not paras:
        paras = [text]
    out: list[str] = []
    buf: list[str] = []
    buf_len = 0
    for p in paras:
        plen = len(p) + (2 if buf else 0)
        if buf and buf_len + plen > max_chars:
            out.append("\n\n".join(buf))
            buf = [p]
            buf_len = len(p)
        elif not buf:
            buf = [p]
            buf_len = len(p)
        else:
            buf.append(p)
            buf_len += plen
    if buf:
        out.append("\n\n".join(buf))
    final: list[str] = []
    for piece in out:
        if len(piece) <= max_chars:
            final.append(piece)
            continue
        lines = piece.split("\n")
        buf2: list[str] = []
        bl = 0
        for ln in lines:
            add_len = len(ln) + (1 if buf2 else 0)
            if buf2 and bl + add_len > max_chars:
                final.append("\n".join(buf2))
                buf2 = [ln]
                bl = len(ln)
            elif not buf2:
                buf2 = [ln]
                bl = len(ln)
            else:
                buf2.append(ln)
                bl += add_len
        if buf2:
            final.append("\n".join(buf2))
    really: list[str] = []
    for piece in final:
        if len(piece) <= max_chars:
            really.append(piece)
        else:
            for i in range(0, len(piece), max_chars):
                really.append(piece[i : i + max_chars])
    return really if really else [text]


def _refine_oversized_chunk(
    base_label: str,
    content: str,
    next_exact_level: int,
    max_chars: int,
    *,
    max_heading_level: int = 6,
) -> list[tuple[str, str]]:
    """If ``content`` exceeds ``max_chars``, split using heading depth ``next_exact_level``, recurse."""
    if len(content) <= max_chars:
        return [(base_label, content)]
    if next_exact_level > max_heading_level:
        parts = _hard_split_oversized(content, max_chars)
        return [(f"{base_label}_p{i:02d}", p) for i, p in enumerate(parts)]

    sub_strings = _chunk_by_exact_heading_level(content, next_exact_level)
    if len(sub_strings) <= 1:
        return _refine_oversized_chunk(
            base_label, content, next_exact_level + 1, max_chars, max_heading_level=max_heading_level
        )

    out: list[tuple[str, str]] = []
    for i, part in enumerate(sub_strings):
        sub_label = f"{base_label}_{i:02d}"
        out.extend(
            _refine_oversized_chunk(
                sub_label, part, next_exact_level + 1, max_chars, max_heading_level=max_heading_level
            )
        )
    return out


def _refine_chunks_for_max_size(
    chunks: list[tuple[str, str]],
    split_on_heading_level: int,
    max_chars: int,
) -> list[tuple[str, str]]:
    """After primary heading/section splits, subdivide any piece larger than ``max_chunk_chars``."""
    refined: list[tuple[str, str]] = []
    start_level = split_on_heading_level + 1
    for label, content in chunks:
        refined.extend(_refine_oversized_chunk(label, content, start_level, max_chars))
    return refined


def _chunk_by_section_markers(text: str, section_pat: re.Pattern | None = None) -> list[tuple[str, str]]:
    """Split on lines matching ``section_pat`` (e.g. ``CHAPTER n``)—**output slices only**.

    Prefer fixing conversion so ``##``/``#`` exist (``pdf_markdown_post`` promotion, outline pass);
    then :func:`_chunk_by_headings` runs instead. This path does not edit the source ``.md`` file.
    """
    lines = text.split("\n")
    chunks, current_lines, chunk_idx = [], [], 0
    if section_pat is None:
        section_pat = re.compile(r"^CHAPTER\s+\d+\b", re.IGNORECASE)

    for line in lines:
        if section_pat.search(line) and len(current_lines) >= MIN_CHUNK_LINES:
            chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
            current_lines, chunk_idx = [], chunk_idx + 1
        current_lines.append(line)

    if current_lines:
        chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
    return chunks


def _has_markdown_headings(text: str) -> bool:
    return bool(re.search(r"^#{1,2}\s", text, re.MULTILINE))


def _is_slide_deck(text: str) -> bool:
    return bool(re.search(r"<!-- Slide number: \d+ -->", text))


def _is_chunked_output(path: Path) -> bool:
    """True if file is chunked output (__slide_NN, __section_NN)."""
    return bool(re.search(r"__(?:slide|section|page)_\d+\.md$", path.name, re.IGNORECASE))


def _is_under_source_memory_tree(md_path: Path, src_root: Path) -> bool:
    """True if md_path is inside <src_root>/memory/ (chunk output tree — not convert input)."""
    try:
        rel = md_path.relative_to(src_root.resolve())
    except ValueError:
        return False
    if not rel.parts:
        return False
    return rel.parts[0].casefold() == "memory"


def _is_under_assets_rag_tree(md_path: Path, src_root: Path) -> bool:
    """True if under <src_root>/assets/rag/ (vector index sidecar — not source content)."""
    try:
        rel = md_path.relative_to(src_root.resolve())
    except ValueError:
        return False
    parts = [p.casefold() for p in rel.parts]
    return len(parts) >= 2 and parts[0] == "assets" and parts[1] == "rag"


def _rel_has_markdown_dir(rel: Path) -> bool:
    """True if any directory segment (not the filename) is named markdown."""
    parts = rel.parts
    return len(parts) > 1 and any(p.casefold() == "markdown" for p in parts[:-1])


def _source_pick_priority(p: Path, src_root: Path) -> int:
    """Lower = preferred: parallel ``<root>/markdown/...`` first, then legacy nested ``.../markdown/``, then sibling."""
    rel = p.relative_to(src_root.resolve())
    parts = rel.parts
    if len(parts) >= 2 and parts[0].casefold() == "markdown":
        return 0
    if _rel_has_markdown_dir(rel):
        return 1
    return 2


def _logical_chunk_key(md_path: Path, src_root: Path) -> tuple[tuple[str, ...], str]:
    """(logical parent path under topic, stem) — same key for sibling .md and markdown/stem.md."""
    rel = md_path.relative_to(src_root.resolve())
    parts = list(rel.parts)
    stem = Path(parts[-1]).stem.casefold()
    dir_parts = parts[:-1]
    if dir_parts and dir_parts[0].casefold() == "markdown":
        dir_parts = dir_parts[1:]
    dir_parts = [p for p in dir_parts if p.casefold() != "markdown"]
    return (tuple(dir_parts), stem)


def _memory_output_parent(md_path: Path, src_root: Path) -> Path:
    """Parent path under chunk_base: mirror source but drop leading ``markdown`` and other ``markdown`` segments."""
    rel = md_path.relative_to(src_root.resolve())
    parts = list(rel.parts[:-1])
    if parts and parts[0].casefold() == "markdown":
        parts = parts[1:]
    parts = [p for p in parts if p.casefold() != "markdown"]
    return Path(*parts) if parts else Path(".")


def _spec_chunk_inputs(spec: dict | None) -> list[str] | None:
    """Optional allow-list of topic-relative POSIX paths (e.g. ``markdown/book.md``). If set, only these files are chunked."""
    if not spec:
        return None
    raw = spec.get("chunk_inputs")
    if raw is None:
        return None
    if isinstance(raw, str):
        return [raw.strip()] if raw.strip() else None
    if isinstance(raw, list):
        out = [str(x).strip() for x in raw if str(x).strip()]
        return out or None
    return None


def _select_chunk_sources(src_root: Path, spec: dict | None = None) -> list[Path]:
    """One .md per logical doc: prefer ``<root>/markdown/...``, then legacy ``.../markdown/``, else sibling."""
    src = src_root.resolve()
    allow = _spec_chunk_inputs(spec)
    if allow is not None:
        out: list[Path] = []
        for rel in allow:
            p = (src / rel.replace("\\", "/")).resolve()
            if p.is_file() and p.suffix.lower() == ".md":
                out.append(p)
            else:
                print(f"  Warning: chunk_inputs path missing or not .md: {rel}")
        return sorted(out, key=lambda p: str(p.as_posix().lower()))

    candidates = sorted(
        f
        for f in src.rglob("*.md")
        if "images" not in f.parts
        and not _is_chunked_output(f)
        and not _is_under_source_memory_tree(f, src)
        and not _is_under_assets_rag_tree(f, src)
    )
    by_key: dict[tuple[tuple[str, ...], str], Path] = {}
    for f in candidates:
        k = _logical_chunk_key(f, src)
        old = by_key.get(k)
        if old is None or _source_pick_priority(f, src) < _source_pick_priority(old, src):
            by_key[k] = f
    return sorted(by_key.values(), key=lambda p: str(p.as_posix().lower()))


def _extract_source_ref(text: str) -> tuple[str | None, str | None]:
    m = re.search(r"<!--\s*Source:\s*([^|]+)\s*\|\s*([^>]+)\s*-->", text)
    return (m.group(1).strip(), m.group(2).strip()) if m else (None, None)


def _add_chunk_source_ref(content: str, source_path: str | None, source_url: str | None, location: str) -> str:
    if not source_path:
        return content
    loc = f", {location}" if location else ""
    url = f" | {source_url}" if source_url else ""
    return f"<!-- Source: {source_path}{loc}{url} -->\n\n" + content


def _build_front_matter(
    chunk_id: str,
    source_path: str | None,
    evidence_type: str,
    chunk_type: str,
    section_path: list[str],
    *,
    slide_number: int | None = None,
    slide_title: str | None = None,
) -> str:
    """Produce YAML front matter block for a chunk when a spec is active."""
    lines = ["---"]
    lines.append(f"chunk_id: {chunk_id}")
    if source_path:
        lines.append("source:")
        lines.append(f"  canonical_path: {source_path}")
    lines.append(f"evidence_type: {evidence_type}")
    lines.append(f"chunk_type: {chunk_type}")
    if slide_number is not None:
        lines.append(f"slide_number: {slide_number}")
    if slide_title:
        st = " ".join(slide_title.split())
        st = st.replace('"', "'")
        if len(st) > 220:
            st = st[:217] + "..."
        lines.append(f'slide_title: "{st}"')
    if section_path:
        sections_yaml = ", ".join(f'"{s}"' for s in section_path)
        lines.append(f"section_path: [{sections_yaml}]")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def _extract_section_path(content: str) -> list[str]:
    """Extract heading breadcrumb from chunk content (first few headings)."""
    headings = re.findall(r"^#{1,6}\s+(.+)$", content, re.MULTILINE)
    return [h.strip() for h in headings[:3]]


def _strip_slide_chunk_for_title_probe(content: str) -> str:
    """Remove source/slide markers so we can tell if a chunk has real body text."""
    t = re.sub(r"<!--\s*Source:[^>]*-->\s*\n*", "", content).lstrip()
    t = re.sub(r"<!--\s*Slide number:\s*\d+\s*-->\s*", "", t).strip()
    return t


def _extract_slide_title(slide_body: str) -> str | None:
    """Primary H1 line plus optional short subtitle line (PPTX decks often split title across two lines)."""
    t = _strip_slide_chunk_for_title_probe(slide_body)
    if not t:
        return None
    m = re.search(r"^#\s+(.+)$", t, re.MULTILINE)
    if not m:
        return None
    first = m.group(1).strip()
    rest = t[m.end() :].lstrip()
    if not rest:
        return first
    line2 = rest.split("\n", 1)[0].strip()
    if not line2:
        return first
    if line2.startswith(("#", "!", "|", "<", "-", "*", "`", "‹")):
        return first
    if len(line2) > 160:
        return first
    low = line2.lower()
    if low.startswith("notes:") or low == "notes":
        return first
    return f"{first} {line2}".strip()


def _meaningful_chunk_body(content: str) -> bool:
    """False for preamble that is only Source comment, or empty slide shells."""
    return bool(_strip_slide_chunk_for_title_probe(content))


def chunk_file(
    md_path: Path,
    conv_root: Path,
    chunk_root: Path,
    spec: dict | None = None,
) -> int:
    text = md_path.read_text(encoding="utf-8")
    stem, source_path, source_url = md_path.stem, *_extract_source_ref(text)
    out_dir = chunk_root
    out_dir.mkdir(parents=True, exist_ok=True)

    use_spec = spec is not None
    if use_spec:
        section_pat = _spec_section_break_regex(spec)
        heading_level = _spec_split_heading_level(spec)
        default_et, default_ct = _spec_defaults(spec)
    else:
        section_pat = None
        heading_level = 2
        default_et = default_ct = ""

    if _is_slide_deck(text):
        chunks = _chunk_by_slides(text)
    elif text.count("\n") > 200:
        # Split only—never inject headings into the source. Order prefers markdown headings
        # (conversion should have promoted CHAPTER etc. via pdf_markdown_post where possible).
        if _has_markdown_headings(text):
            chunks = _chunk_by_headings(text, heading_level=heading_level)
        elif section_pat:
            chunks = _chunk_by_section_markers(text, section_pat=section_pat)
        else:
            chunks = _chunk_by_section_markers(text)
    else:
        chunks = [(stem, text)]

    if use_spec and not _is_slide_deck(text):
        splitting = spec.get("splitting", {}) if spec else {}
        raw_max = splitting.get("max_chunk_chars", 4000)
        try:
            max_chars_refine = int(raw_max)
        except (TypeError, ValueError):
            max_chars_refine = 4000
        if max_chars_refine > 0:
            # Reserve space for YAML front matter added when writing each chunk file.
            body_budget = max(400, max_chars_refine - 600)
            chunks = _refine_chunks_for_max_size(chunks, heading_level, body_budget)

    def _loc(label: str) -> str:
        if label.startswith("slide_"):
            return f"slide {int(label.split('_')[1])}"
        if label.startswith("section_"):
            m = re.match(r"^section_(\d+)", label)
            if m:
                return f"section {int(m.group(1)) + 1}"
        return ""

    written = 0
    is_deck = _is_slide_deck(text)
    for label, content in chunks:
        if not _meaningful_chunk_body(content):
            continue
        out_name = f"{stem}__{label}.md" if len(chunks) > 1 else f"{stem}.md"
        chunk_id = Path(out_name).stem  # filename stem without .md

        if use_spec:
            # Strip any existing source comment to avoid duplication
            content_body = re.sub(r"<!--\s*Source:[^>]*-->\s*\n*", "", content).lstrip()
            slide_number: int | None = None
            slide_title: str | None = None
            if is_deck and label.startswith("slide_"):
                sm = re.match(r"slide_(\d+)", label)
                slide_number = int(sm.group(1)) if sm else None
                slide_title = _extract_slide_title(content_body)
                # slide_title / slide_number are canonical for decks (avoid duplicating in section_path)
                section_path = []
            else:
                section_path = _extract_section_path(content_body)
            front = _build_front_matter(
                chunk_id,
                source_path,
                default_et,
                default_ct,
                section_path,
                slide_number=slide_number,
                slide_title=slide_title,
            )
            if is_deck and slide_number is not None:
                vis = f"### Slide {slide_number}"
                if slide_title:
                    vis += f" — {slide_title}"
                content_body = vis + "\n\n" + content_body
            final_content = front + content_body
        else:
            final_content = _add_chunk_source_ref(content, source_path, source_url, _loc(label))

        out = out_dir / out_name
        out.write_text(final_content, encoding="utf-8")
        for ref in _find_image_refs(final_content):
            _copy_images([ref], conv_root, chunk_root)
        written += 1
    return written


def _run_path_mode(source_path: str, memory_name_override: str | None = None, output_override: str | None = None) -> None:
    p = Path(source_path)
    if p.is_absolute():
        src_root = p
    else:
        under_assets = ASSETS / source_path
        under_root = ROOT / source_path
        if under_assets.exists():
            src_root = under_assets
        elif under_root.exists():
            src_root = under_root
        else:
            print(f"Path not found: {source_path}")
            return

    # When originals live in ``.../context/``, converted md is under ``../markdown/`` — scan project root.
    scan_root = src_root.parent if src_root.name.casefold() == "context" else src_root

    if output_override:
        chunk_base = Path(output_override)
        if not chunk_base.is_absolute():
            chunk_base = Path.cwd() / chunk_base
        dest = str(chunk_base)
    elif memory_name_override:
        chunk_base = MEMORY / memory_name_override
        dest = f"memory/{memory_name_override}/"
    else:
        chunk_base = MEMORY
        dest = "memory/"

    # Load chunking spec if present
    spec = _load_spec(src_root)
    if spec:
        sp = _resolve_spec_path(src_root)
        print(f"  Using chunking spec: {sp}")
        default_et, default_ct = _spec_defaults(spec)
        print(f"  Defaults (front matter): evidence_type={default_et}  chunk_type={default_ct}")
        kt = _spec_keep_tables_intact(spec)
        if kt is not None:
            print(
                "  splitting.keep_markdown_tables_intact: "
                f"{kt}  (splits follow headings/markers only; valid GFM pipes → fix in convert)"
            )
        _log_taxonomy_from_spec(spec)
        _warn_defaults_vs_taxonomy(spec)
        _warn_placeholder_defaults(spec)

    md_files = _select_chunk_sources(scan_root, spec)
    if not md_files:
        print(f"No markdown in {scan_root}")
        print("Run convert_to_markdown.py --memory <path> first.")
        return

    print(f"Source: {scan_root}  ({len(md_files)} logical docs) -> {dest}\n")
    total = 0
    for i, f in enumerate(md_files, 1):
        conv_root = f.parent
        mem_parent = _memory_output_parent(f, scan_root)
        chunk_root = chunk_base / mem_parent
        rel = f.relative_to(scan_root)
        label = str(rel) if rel != Path(".") else f.name
        print(f"  [{i}/{len(md_files)}] {label} ... ", end="", flush=True)
        try:
            n = chunk_file(f, conv_root, chunk_root, spec=spec)
            total += n
            print(f"OK  ({n} chunks)")
        except Exception as e:
            print(f"FAIL  {e}")
    print(f"\nDone: {total} chunks.")


def _get_arg(flag: str) -> str | None:
    if flag in sys.argv:
        idx = sys.argv.index(flag)
        if idx + 1 < len(sys.argv):
            return sys.argv[idx + 1]
    return None


def main():
    path_arg   = _get_arg("--path")
    memory_arg = _get_arg("--memory")
    output_arg = _get_arg("--output")
    if path_arg:
        _run_path_mode(path_arg, memory_name_override=memory_arg, output_override=output_arg)
        return
    if memory_arg:
        _run_path_mode(memory_arg)
        return
    print(
        "Usage: python chunk_markdown.py --path <source_folder> "
        "[--memory <nested_under_memory> | --output <dir>]"
    )


if __name__ == "__main__":
    main()
