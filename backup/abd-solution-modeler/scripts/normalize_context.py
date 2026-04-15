#!/usr/bin/env python3
"""Phase 1: Normalize context into context_chunks.json.

Accepts chunk_index.json (from abd-context-to-memory) or --context-path for raw markdown.
Applies default and optional workspace noise filters before writing.
Output: context_chunks.json with chunk_id, source, text per chunk.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent

# Default noise filters: TOC, pure headers, page numbers (for SHORT chunks only)
_DEFAULT_NOISE = [
    r"^table of contents\s*$",
    r"^contents\s*$",
    r"^appendix\s*[a-z]?\s*$",
    r"^index\s*$",
    r"^license\s*$",
    r"^\s*chapter\s+\d+[\s:][^.]*\.{10,}\s*\d+\s*$",  # "CHAPTER 8: TITLE ......... 235"
    r"^[\d\s\.]+$",  # page numbers only
    r"^[\d\s]+$",  # numbers only
]


def _stable_id(path: str, content: str) -> str:
    return hashlib.sha256(f"{path}:{content[:200]}".encode()).hexdigest()[:12]


def from_chunk_index(chunk_index_path: Path) -> list[dict]:
    """Read chunk_index.json, load each chunk file, produce rule_chunks."""
    data = json.loads(chunk_index_path.read_text(encoding="utf-8"))
    context_path = Path(data["context_path"]).resolve()
    chunks = data.get("chunks", [])

    rule_chunks = []
    for info in chunks:
        chunk_path = context_path / info["path"]
        if not chunk_path.exists():
            continue
        text = _clean_text(chunk_path.read_text(encoding="utf-8", errors="replace").strip())
        if not text:
            continue
        chunk_id = info.get("chunk_id", _stable_id(info["path"], text))
        rule_chunks.append({
            "chunk_id": chunk_id,
            "source": info["path"],
            "text": text,
        })
    return rule_chunks


_MIN_CHUNK_LINES = 5
_CHUNK_THRESHOLD_LINES = 200  # Files larger than this get split by headings/sections


def _chunk_by_headings(text: str) -> list[str]:
    """Split text at # or ## boundaries. Returns list of chunk texts."""
    lines = text.split("\n")
    chunks, current = [], []
    for line in lines:
        if re.match(r"^#{1,2}\s", line) and len(current) >= _MIN_CHUNK_LINES:
            chunks.append("\n".join(current))
            current = []
        current.append(line)
    if current:
        chunks.append("\n".join(current))
    return chunks


def _chunk_by_chapter_markers(text: str) -> list[str]:
    """Split on CHAPTER N markers (PDF/rpg book structure)."""
    lines = text.split("\n")
    chunks, current = [], []
    section_pat = re.compile(r"^CHAPTER\s+\d+\b", re.IGNORECASE)
    for line in lines:
        if section_pat.search(line) and len(current) >= _MIN_CHUNK_LINES:
            chunks.append("\n".join(current))
            current = []
        current.append(line)
    if current:
        chunks.append("\n".join(current))
    return chunks


def _split_large_md(rel: str, text: str) -> list[dict]:
    """Split a large markdown file into chunks. Returns list of {chunk_id, source, text}."""
    line_count = text.count("\n") + 1
    if line_count <= _CHUNK_THRESHOLD_LINES:
        return [{"chunk_id": _stable_id(rel, text), "source": rel, "text": text}]

    if re.search(r"^#{1,2}\s", text, re.MULTILINE):
        raw_chunks = _chunk_by_headings(text)
    else:
        raw_chunks = _chunk_by_chapter_markers(text)

    result = []
    for i, chunk_text in enumerate(raw_chunks):
        if not chunk_text.strip():
            continue
        source = f"{rel}__section_{i:03d}" if len(raw_chunks) > 1 else rel
        result.append({
            "chunk_id": _stable_id(source, chunk_text),
            "source": source,
            "text": chunk_text,
        })
    return result


def from_context_path(context_path: Path) -> list[dict]:
    """Scan folder for .md files, chunk large files by headings/sections, produce rule_chunks."""
    rule_chunks = []
    for md in sorted(context_path.rglob("*.md")):
        raw = md.read_text(encoding="utf-8", errors="replace").strip()
        if not raw:
            continue
        text = _clean_text(raw)
        if not text:
            continue
        rel = str(md.relative_to(context_path))
        for c in _split_large_md(rel, text):
            rule_chunks.append(c)
    return rule_chunks


# ---------------------------------------------------------------------------
# PDF running-header strip (applied per-chunk before any other processing)
# ---------------------------------------------------------------------------

# Doubled page numbers: "249249", "187187" — digit sequence repeated
_DOUBLED_PAGE_RE = re.compile(r"\b(\d{2,4})\1\b")

# All-caps lines that are pure PDF headers / book titles
# Matches lines that are ALL CAPS (or spaces/ampersands/apostrophes) with ≥10 chars
_ALLCAPS_HEADER_RE = re.compile(r"^[A-Z][A-Z\s&'''\u2019:]{9,}$")

# Mixed lines where an all-caps prefix is fused to a sentence:
# e.g. "COMBAT You have no penalty..." or "THE BASICS 99 a hero has..."
# Strips the leading all-caps block (plus optional page number) before prose.
_FUSED_HEADER_RE = re.compile(
    r"^(?:[A-Z][A-Z\s\-'&]{4,})(?:\s+\d{1,4})?\s+(?=[A-Za-z])"
)

# Source comment lines from abd-context-to-memory (<!-- Source: ... -->)
_SOURCE_COMMENT_RE = re.compile(r"<!--\s*Source:[^>]*-->", re.IGNORECASE)


def _clean_text(text: str) -> str:
    """Strip PDF running headers and metadata noise from chunk text.

    Removes:
    - Doubled page numbers (249249, 187187, ...)
    - All-caps-only lines that are book titles / chapter header repeats
    - Source comment metadata lines
    """
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Remove source comment lines
        if _SOURCE_COMMENT_RE.match(stripped):
            continue
        # Remove all-caps header lines (e.g. "MUTANTS & MASTERMINDS", "DELUXE HERO'S HANDBOOK")
        if _ALLCAPS_HEADER_RE.match(stripped):
            continue
        # Strip fused all-caps prefix from mixed lines (e.g. "COMBAT You have..." → "You have...")
        line = _FUSED_HEADER_RE.sub("", line)
        stripped = line.strip()
        # Strip doubled page numbers inline (e.g. "see page 249249" → "see page 249")
        line = _DOUBLED_PAGE_RE.sub(lambda m: m.group(1), line)
        cleaned.append(line)

    # Remove leading blank lines left by stripped header lines
    result = "\n".join(cleaned)
    return re.sub(r"\n{3,}", "\n\n", result).strip()


def _is_noise(text: str, patterns: list[str]) -> bool:
    """True if chunk is predominantly noise (TOC, headers, flavor only)."""
    lower = text.lower().strip()
    lines = [ln.strip() for ln in lower.split("\n") if ln.strip()]

    # Long chunks with substantial content are never noise
    if len(lower) > 800:
        return False

    # TOC: majority of lines match "chapter X: ... ..... page"
    toc_lines = sum(1 for ln in lines if re.search(r"chapter\s+\d+[\s:].*\.{5,}\s*\d+\s*$", ln, re.I))
    if len(lines) >= 4 and toc_lines >= max(3, len(lines) * 0.5):
        return True

    # Short chunks: check if they're purely noise
    if len(lower) < 150:
        for p in patterns:
            if re.search(p, lower, re.IGNORECASE | re.MULTILINE):
                return True
        if lower.count("\n") < 2 and re.match(r"^[\w\s:\.\-&'\u2019]+$", lower):
            if not any(w in lower for w in ("effect", "action", "damage", "rank", "check", "cost", "resistance")):
                return True

    # Chunk is mostly repeated header (e.g. "CHAPTER X" repeated 3+ times in first 6 lines)
    if len(lines) >= 3:
        top = lines[0][:40]
        repeats = sum(1 for ln in lines[:6] if top[:25] in ln or ln.startswith(top[:20]))
        if repeats >= 3 and len(lower) < 400:
            return True

    return False


def _load_workspace_filters() -> list[str]:
    """Load workspace-specific noise filters from concept_guidance.json if it exists.
    Used only when re-running Phase 1 after Phase 4 (Concept synthesis) has produced
    concept_guidance.json. On first run, returns [] since the file does not exist yet."""
    try:
        from _config import domain_dir
        guidance_path = domain_dir() / "concept_guidance.json"
        if guidance_path.exists():
            data = json.loads(guidance_path.read_text(encoding="utf-8"))
            filters = data.get("noise_filters", [])
            return [f if isinstance(f, str) else str(f) for f in filters]
    except Exception:
        pass
    return []


def filter_chunks(chunks: list[dict], workspace_filters: list[str] | None = None) -> tuple[list[dict], int]:
    """Apply default + workspace filters. Returns (filtered_chunks, dropped_count)."""
    patterns = _DEFAULT_NOISE.copy()
    if workspace_filters:
        for f in workspace_filters:
            if f and f.strip() and f.strip().lower() not in (p.lower() for p in patterns):
                patterns.append(re.escape(f.strip()))
    kept = []
    for c in chunks:
        if _is_noise(c.get("text", ""), patterns):
            continue
        kept.append(c)
    return kept, len(chunks) - len(kept)


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 1: Normalize context to rule_chunks.json")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--chunk-index", help="Path to chunk_index.json (from abd-context-to-memory)")
    group.add_argument("--context-path", help="Path to folder of markdown files")
    parser.add_argument("--output", "-o", help="Output path for rule_chunks.json")
    parser.add_argument("--no-filter", action="store_true", help="Skip noise filtering (for debugging)")
    args = parser.parse_args()

    if args.chunk_index:
        rule_chunks = from_chunk_index(Path(args.chunk_index).resolve())
    else:
        ctx = Path(args.context_path).resolve()
        if not ctx.exists():
            print(f"Context path does not exist: {ctx}", file=sys.stderr)
            sys.exit(1)
        rule_chunks = from_context_path(ctx)

    if not args.no_filter:
        workspace_filters = _load_workspace_filters()
        rule_chunks, dropped = filter_chunks(rule_chunks, workspace_filters or None)
        if dropped:
            print(f"Filtered {dropped} noise chunks (kept {len(rule_chunks)})", file=sys.stderr)

    from _config import context_dir
    context_out = Path(args.output).resolve() if args.output else context_dir()
    context_out.mkdir(parents=True, exist_ok=True)

    # Remove stale .md chunk files before writing fresh ones
    for old in context_out.glob("*.md"):
        old.unlink()

    # Write rule_chunks.json into <output_dir>/context/
    output_path = context_out / "context_chunks.json"
    output_path.write_text(json.dumps(rule_chunks, indent=2), encoding="utf-8")
    print(f"Normalized {len(rule_chunks)} chunks -> {output_path}")

    # Write individual chunk files into <output_dir>/context/
    for chunk in rule_chunks:
        (context_out / (chunk["chunk_id"] + ".md")).write_text(chunk["text"], encoding="utf-8")
    print(f"Wrote {len(rule_chunks)} chunk files -> {context_out}")


if __name__ == "__main__":
    main()
