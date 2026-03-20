#!/usr/bin/env python3
"""Parse markdown into blocks, classify, split, write chunks/*.md and context_index.json.

Stage 1 Step 3 — Extract Context. Replaces chunk_markdown + build_context_chunks.

Usage:
  python parse_and_curate.py [--path <markdown_folder>] [--output <context_folder>]
  python parse_and_curate.py --add <file.md>

Source discovery (when --path omitted):
  1. Look in workspace for context/ — if context_index.json and chunks/ exist, skip (use --force to override)
  2. Use source_path from solution.conf if set
  3. Else search workspace: docs/, maps-models-specs/, then workspace root for .md files
  4. If nothing found: error — "Where is the source? Specify --path <folder> or add source_path to solution.conf."

Output schema:
  chunks/{chunk_id}.md — YAML front matter + markdown body (content)
  context_index.json — manifest, forward_index, concept_seeds, reverse_indexes, excluded (metadata only)

Planning: docs/plan-context-curation.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


# --- Section / chapter break detection (parameterized for config and AI rewrites) ---
# To change what counts as a section or chapter boundary: edit these two functions and/or
# the section_boundaries keys in solution.conf (section_break_regex, section_break_all_caps, etc.).


def is_section_break_line(line: str, config: dict | None) -> bool:
    """True if line is a section boundary (e.g. all-caps POWERS, or regex match).

    Config (context_curation.section_boundaries):
      - section_break_regex: if set, line must match this regex to be a section break.
      - all_caps_standalone: if true, also treat all-caps short lines as section breaks.
      - section_break_max_chars, section_break_max_words, section_break_caps_ratio:
        used when all_caps_standalone is true (defaults 80, 8, 0.85).
    """
    if not line or not line.strip():
        return False
    line = line.strip()
    section_cfg = (config or {}).get("context_curation", {}).get("section_boundaries", {})

    # Regex takes precedence when set
    regex = section_cfg.get("section_break_regex")
    if regex:
        try:
            if re.search(regex, line):
                return True
        except re.error:
            pass
        # If regex is set but didn't match, don't fall through to all-caps
        return False

    # All-caps standalone (current default behavior)
    if not section_cfg.get("all_caps_standalone", True):
        return False
    max_chars = int(section_cfg.get("section_break_max_chars", 80))
    max_words = int(section_cfg.get("section_break_max_words", 8))
    caps_ratio_min = float(section_cfg.get("section_break_caps_ratio", 0.85))
    if len(line) > max_chars:
        return False
    words = line.split()
    if len(words) > max_words:
        return False
    letters = [c for c in line if c.isalpha()]
    if not letters:
        return False
    caps_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    return caps_ratio >= caps_ratio_min


def is_chapter_break_line(line: str, config: dict | None) -> bool:
    """True if line is a chapter boundary (e.g. markdown # heading or regex).

    Config (context_curation.section_boundaries):
      - chapter_break_regex: if set, line must match to be a chapter break.
      - Otherwise, chapter = markdown heading: line starts with #.
    """
    if not line or not line.strip():
        return False
    stripped = line.strip()
    section_cfg = (config or {}).get("context_curation", {}).get("section_boundaries", {})

    regex = section_cfg.get("chapter_break_regex")
    if regex:
        try:
            return bool(re.search(regex, stripped))
        except re.error:
            pass
    # Default: markdown ATX heading
    return stripped.startswith("#")


def parse_markdown_to_blocks(source_path: Path, config: dict | None = None) -> list[dict]:
    """Parse markdown into candidate blocks. Returns list of block dicts.

    Section and chapter boundaries are determined by is_section_break_line and
    is_chapter_break_line (config-driven; see section_boundaries in solution.conf).
    """
    lines = source_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    blocks: list[dict] = []
    section_stack: list[str] = []
    current_lines: list[str] = []
    current_type = "paragraph"
    block_start = 1
    block_index = 0

    def flush(end_line: int) -> None:
        nonlocal current_lines, current_type, block_start, block_index
        text = _normalize_whitespace("\n".join(current_lines))
        if not text:
            current_lines = []
            return
        block_index += 1
        blocks.append({
            "block_id": f"blk_{block_index:05d}",
            "source_path": str(source_path),
            "source": source_path.stem,
            "section_path": section_stack.copy(),
            "text": text,
            "structural_type": current_type,
            "start_line": block_start,
            "end_line": end_line,
        })
        current_lines = []

    for i, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip()
        stripped = line.strip()

        # Chapter break (e.g. markdown # or chapter_break_regex)
        if is_chapter_break_line(line, config):
            if current_lines:
                flush(i - 1)
            heading = stripped.lstrip("#").strip() if stripped.startswith("#") else stripped
            depth = len(stripped) - len(stripped.lstrip("#")) if stripped.startswith("#") else 1
            section_stack[:] = section_stack[: max(depth - 1, 0)]
            section_stack.append(heading)
            current_type = "heading"
            current_lines = [heading]
            block_start = i
            flush(i)
            current_type = "paragraph"
            continue

        # Do not flush on blank lines: keep accumulating paragraphs into one block
        # until we hit a real boundary.
        if not stripped:
            continue

        # Section break (all-caps or section_break_regex)
        if is_section_break_line(line, config):
            if current_lines:
                flush(i - 1)
            current_type = "heading"
            current_lines = [stripped]
            block_start = i
            flush(i)
            current_type = "paragraph"
            continue

        # List: - * +, numbered, or Unicode bullets (• ·)
        if (
            re.match(r"^[-*+]\s+", stripped)
            or re.match(r"^\d+\.\s+", stripped)
            or re.match(r"^[•·]\s*", stripped)
        ):
            if current_lines and current_type != "list":
                flush(i - 1)
            if not current_lines:
                block_start = i
            current_type = "list"
            current_lines.append(stripped)
            continue

        if "|" in stripped and stripped.count("|") >= 2:
            if current_lines and current_type != "table":
                flush(i - 1)
            if not current_lines:
                block_start = i
            current_type = "table"
            current_lines.append(stripped)
            continue

        if current_lines and current_type not in {"paragraph"}:
            flush(i - 1)
            current_type = "paragraph"
            block_start = i
        if not current_lines:
            block_start = i
        current_lines.append(stripped)

    if current_lines:
        flush(len(lines))
    return blocks


def _is_truncated_header_fragment(text: str) -> bool:
    """True if block looks like a truncated header (e.g. 'DIFFICULTY CLASS' without 'ES')."""
    t = text.strip()
    if not t or len(t) > 40:
        return False
    # Common truncation patterns: ends with word that suggests cut-off
    truncation_endings = ("CLASS", "CLASSES", "CHECK", "CHECKS", "EXAMPLE", "EXAMPLES", "SKILL", "USING")
    words = t.split()
    last_upper = words[-1].upper() if words else ""
    return len(words) <= 3 and (last_upper in truncation_endings or last_upper.endswith("CLASS"))


def split_blocks_ending_with_fragment(blocks: list[dict], config: dict) -> list[dict]:
    """Split blocks that end with a truncated header fragment into two blocks.

    PDF conversion sometimes puts fragments (e.g. 'DIFFICULTY CLASS') on the same
    line as the preceding sentence. Split so the fragment becomes its own block,
    which merge_header_with_next can then merge with the following content.
    """
    result: list[dict] = []
    for block in blocks:
        if block["structural_type"] != "paragraph":
            result.append(block)
            continue
        text = block["text"].strip()
        if not text:
            result.append(block)
            continue
        # Look for fragment at end: sentence. FRAGMENT (space + all-caps fragment at end)
        parts = re.split(r"\s+([A-Z][A-Z\s]{4,30})$", text)
        if len(parts) != 3:
            result.append(block)
            continue
        before, fragment = parts[0].strip(), (parts[1] or "").strip()
        if not fragment or not _is_truncated_header_fragment(fragment):
            result.append(block)
            continue
        if not before:
            result.append(block)
            continue
        # Split: emit main content, then fragment as separate block
        result.append({
            **block,
            "text": before,
            "block_id": block["block_id"] + "_a",
        })
        result.append({
            **block,
            "block_id": block["block_id"] + "_b",
            "text": fragment,
        })
    return result


def merge_table_like_blocks(blocks: list[dict], config: dict) -> list[dict]:
    """Merge consecutive short paragraph blocks into table blocks.

    PDF conversion often produces tables as vertical stacks (one cell per line).
    Detect runs of such blocks and merge into one block with structural_type 'table'.
    Long example cells (e.g. 5-line DC examples) are kept in the table via max_cell_lines.
    """
    curation = config.get("context_curation", {})
    chunking = curation.get("chunking", {})
    merge_cfg = chunking.get("merge_table_like", {})
    if not merge_cfg.get("enabled", True):
        return blocks

    max_cell_chars = merge_cfg.get("max_cell_chars", 150)
    max_cell_lines = merge_cfg.get("max_cell_lines", 8)
    min_run_length = merge_cfg.get("min_run_length", 2)

    result: list[dict] = []
    run: list[dict] = []

    def flush_run() -> None:
        if len(run) < min_run_length:
            result.extend(run)
        else:
            merged = {
                "block_id": run[0]["block_id"],
                "source_path": run[0]["source_path"],
                "source": run[0]["source"],
                "section_path": run[0]["section_path"],
                "text": "\n".join(b["text"] for b in run),
                "structural_type": "table",
                "start_line": run[0]["start_line"],
                "end_line": run[-1]["end_line"],
            }
            result.append(merged)
        run.clear()

    for block in blocks:
        if block["structural_type"] != "paragraph":
            flush_run()
            result.append(block)
            continue

        # Skip truncated header fragments; they will be merged by merge_header_with_next
        if _is_truncated_header_fragment(block["text"]):
            flush_run()
            result.append(block)
            continue

        line_span = block["end_line"] - block["start_line"] + 1
        is_cell_like = line_span <= max_cell_lines and len(block["text"]) <= max_cell_chars
        if is_cell_like:
            run.append(block)
        else:
            flush_run()
            result.append(block)

    flush_run()
    return result


def _is_header_like_block(block: dict, config: dict) -> bool:
    """True if block looks like a standalone header (all-caps, short, no definition colon)."""
    text = block.get("text", "").strip()
    if not text or ":" in text:
        return False
    words = text.split()
    if len(words) > 5 or len(text) > 60:
        return False
    # Mostly uppercase (PDF headers often all-caps)
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    caps_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    return caps_ratio >= 0.7


def merge_header_with_next(blocks: list[dict], config: dict) -> list[dict]:
    """Merge short header-like blocks into the next content block instead of emitting separately.

    PDF conversion often produces section headers as standalone lines (e.g. TRADE-OFFS).
    Prepend them to the following block so context is preserved.
    """
    curation = config.get("context_curation", {})
    chunking = curation.get("chunking", {})
    merge_cfg = chunking.get("merge_header_with_next", {})
    if not merge_cfg.get("enabled", True):
        return blocks

    min_chars = merge_cfg.get("max_header_chars", 60)
    result: list[dict] = []
    i = 0
    while i < len(blocks):
        blk = blocks[i]
        text = blk.get("text", "").strip()
        if (
            text
            and len(text) <= min_chars
            and _is_header_like_block(blk, config)
            and i + 1 < len(blocks)
        ):
            next_blk = blocks[i + 1]
            next_text = next_blk.get("text", "").strip()
            if next_text:
                merged = next_blk.copy()
                merged["text"] = f"## {text}\n\n{next_text}"
                merged["start_line"] = blk["start_line"]
                merged["_is_section_header"] = False  # header+content is content, not a bare header
                result.append(merged)
                i += 2
                continue
        result.append(blk)
        i += 1
    return result


def _is_definition_block(block: dict) -> bool:
    """True if block has definition pattern (Label: definition)."""
    text = block.get("text", "")
    return ":" in text and len(text) > 20


def _is_trivial_separator(block: dict) -> bool:
    """True if block is trivial (single bullet, page noise) that can be skipped between definition runs."""
    text = block.get("text", "").strip()
    if not text or len(text) > 30:
        return False
    # Single bullet or bullet-like
    if text in ("•", "·", "-", "*") or re.match(r"^[•·\-*]\s*$", text):
        return True
    # Very short list item
    if block.get("structural_type") == "list" and len(text.split()) <= 2:
        return True
    return False


def assign_section_path_from_headers(blocks: list[dict], config: dict) -> list[dict]:
    """Set section_path on blocks from all-caps section headers. Runs before merge_header_with_next.

    When section_boundaries.all_caps_standalone is true, treat all-caps blocks as section boundaries
    and assign section_path to all following blocks until the next section header.

    section_path_max_depth (default 2): only keep the last N headers. PDFs stack many short all-caps
    lines; without a cap, path[0] never changes and merge/split logic breaks. Rolling window = current
    chapter + optional sub-heading (e.g. THE CORE MECHANIC + THE HEROES).
    """
    curation = config.get("context_curation", {})
    section_cfg = curation.get("section_boundaries", {})
    if not section_cfg.get("all_caps_standalone", False) and not section_cfg.get("section_break_regex"):
        return blocks

    max_depth = int(section_cfg.get("section_path_max_depth", 2))
    max_depth = max(1, min(max_depth, 8))

    section_stack: list[str] = []
    for block in blocks:
        text = block.get("text", "").strip()
        if is_section_break_line(text or "", config):
            section_stack.append(text)
            section_stack[:] = section_stack[-max_depth:]
            block["section_path"] = section_stack.copy()
            block["_is_section_header"] = True
        else:
            block["section_path"] = section_stack.copy()
            block["_is_section_header"] = False
    return blocks


def merge_blocks_in_section(blocks: list[dict], config: dict) -> list[dict]:
    """Merge consecutive blocks that share the same section_path, up to max_section_words.

    Groups by the full path (tuple), not path[0] alone — otherwise every block shares the first
    header forever and nothing sensible merges.
    """
    curation = config.get("context_curation", {})
    chunking = curation.get("chunking", {})
    merge_cfg = chunking.get("merge_section_blocks", {})
    if not merge_cfg.get("enabled", False):
        return blocks

    max_words = merge_cfg.get("max_section_words", 400)
    result: list[dict] = []
    run: list[dict] = []

    def section_key(blk: dict) -> tuple[str, ...]:
        p = blk.get("section_path", [])
        return tuple(p) if p else ()

    def flush_run() -> None:
        if not run:
            return
        if len(run) == 1:
            result.append(run[0])
        else:
            merged_text = "\n\n".join(b["text"] for b in run)
            total_words = len(merged_text.split())
            if total_words <= max_words:
                merged = run[0].copy()
                merged["text"] = merged_text
                merged["end_line"] = run[-1]["end_line"]
                merged["block_id"] = run[0]["block_id"] + "_merged"
                merged["_section_body_merged"] = True
                result.append(merged)
            else:
                result.extend(run)
        run.clear()

    for block in blocks:
        # Don't merge section headers into content
        if block.get("_is_section_header"):
            flush_run()
            result.append(block)
            continue
        key = section_key(block)
        if run and section_key(run[0]) == key:
            run.append(block)
        else:
            flush_run()
            if key:
                run.append(block)
            else:
                result.append(block)
    flush_run()
    return result


def merge_definition_runs(blocks: list[dict], config: dict) -> list[dict]:
    """Merge consecutive short definition blocks into single blocks.

    Reduces oversplitting when PDF produces many one-sentence definitions
    (e.g. Parry & Toughness, Fortitude & Will) that belong together.
    Skips trivial separators (single bullets) between definitions.
    """
    curation = config.get("context_curation", {})
    chunking = curation.get("chunking", {})
    merge_cfg = chunking.get("merge_definition_runs", {})
    if not merge_cfg.get("enabled", True):
        return blocks

    max_per_block = merge_cfg.get("max_words_per_block", 80)
    max_merged = merge_cfg.get("max_merged_words", 250)
    min_run = merge_cfg.get("min_run_length", 2)
    skip_trivial = merge_cfg.get("skip_trivial_separators", True)

    result: list[dict] = []
    run: list[dict] = []

    def same_section(a: dict, b: dict) -> bool:
        return a.get("section_path", []) == b.get("section_path", [])

    def flush_run() -> None:
        if len(run) < min_run:
            result.extend(run)
        else:
            merged_text = "\n\n".join(b["text"] for b in run)
            total_words = len(merged_text.split())
            if total_words <= max_merged:
                merged = run[0].copy()
                merged["text"] = merged_text
                merged["end_line"] = run[-1]["end_line"]
                result.append(merged)
            else:
                result.extend(run)
        run.clear()

    for block in blocks:
        text = block.get("text", "")
        words = len(text.split())
        is_def = _is_definition_block(block) and words <= max_per_block

        if is_def and run and same_section(run[0], block):
            run.append(block)
        elif skip_trivial and _is_trivial_separator(block) and run:
            # Skip trivial separator, keep building run
            continue
        else:
            flush_run()
            if is_def:
                run.append(block)
            else:
                result.append(block)

    flush_run()
    return result


# Map legacy evidence_type to richer taxonomy
_EVIDENCE_TYPE_MAP = {
    "rule": "domain-rule",
    "definition": "definition",
    "example": "example",
    "table": "table",
    "mention": "mention",
}


def assign_document_region(block: dict, config: dict) -> str:
    """Document-shape pre-pass: assign region from section_path + document_region_keywords."""
    headings = " / ".join(block["section_path"]).lower()
    curation = config.get("context_curation", {})
    region_keywords = curation.get("document_region_keywords", {})
    for region, keywords in region_keywords.items():
        if isinstance(keywords, list):
            for kw in keywords:
                if kw.lower() in headings:
                    return region
    return "rules"


def classify_block(block: dict, config: dict) -> tuple[str | None, str | None]:
    """Classify block. Returns (evidence_type, exclusion_reason).
    If exclusion_reason is not None, block is excluded.
    evidence_type: definition | domain-rule | mechanic | actor-action | state-change |
                  variation/exception | example | flavor | table | mention | metadata/noise
    """
    text = block["text"].lower()
    headings = " / ".join(block["section_path"]).lower()
    curation = config.get("context_curation", {})

    # Config-based exclusion
    noise_keywords = [k.lower() for k in curation.get("noise_heading_keywords", [])]
    if any(k in headings for k in noise_keywords):
        return None, "noise heading"

    # Config-based: out-of-scope sections (e.g. adventures, sample characters, flavor — not rules)
    out_of_scope = [k.lower() for k in curation.get("out_of_scope_section_keywords", [])]
    if any(k in headings for k in out_of_scope):
        return None, "out_of_scope"

    # Heuristic: heading-only blocks excluded
    if block["structural_type"] == "heading":
        return None, "structural heading only"

    # Heuristic: table → table
    if block["structural_type"] == "table":
        return "table", None

    # Config-based: definition cues
    definition_cues = [c.lower() for c in curation.get("definition_cues", ["refers to", "is a", "means", ":"])]
    if any(c in text for c in definition_cues):
        return "definition", None

    # Config-based: example cues
    example_cues = [c.lower() for c in curation.get("example_cues", ["for example", "for instance", "such as", "e.g."])]
    if any(c in text for c in example_cues):
        return "example", None

    # Config-based: decision cues → domain-rule
    decision_cues = [c.lower() for c in curation.get("decision_cues", [])]
    state_cues = [c.lower() for c in curation.get("state_cues", [])]
    if any(c in text for c in decision_cues):
        return "domain-rule", None
    if any(c in text for c in state_cues):
        return "state-change", None

    # Heuristic: list → actor-action
    if block["structural_type"] == "list":
        return "actor-action", None

    # Config-based: flavor → flavor
    flavor_cues = [c.lower() for c in curation.get("flavor_cues", [])]
    if any(c in text for c in flavor_cues):
        return "flavor", None

    # Config-based: mechanic cues (procedure, how to, step)
    mechanic_cues = [c.lower() for c in curation.get("mechanic_cues", ["procedure", "how to", "step 1", "first,", "then,"])]
    if any(c in text for c in mechanic_cues):
        return "mechanic", None

    # Config-based: variation/exception cues
    variation_cues = [c.lower() for c in curation.get("variation_cues", ["however", "exception", "unless", "alternatively", "instead", "otherwise"])]
    if any(c in text for c in variation_cues):
        return "variation/exception", None

    # Default: domain-rule
    return "domain-rule", None


def _block_to_unit(block: dict, chunk_id: str, text: str, evidence_type: str) -> dict:
    return {
        "chunk_id": chunk_id,
        "source": block["source"],
        "text": text,
        "section_path": block["section_path"],
        "structural_type": block["structural_type"],
        "evidence_type": evidence_type,
        "start_line": block["start_line"],
        "end_line": block["end_line"],
    }


# Trailing fragments that mean "don't split here" (first chunk would end mid-thought)
_INCOMPLETE_END_PATTERN = re.compile(
    r"\s+(?:vs\.?|such as|e\.g\.?|for example|for instance|like|i\.e\.?)\s*$",
    re.IGNORECASE,
)


def _split_multi_purpose(block: dict, evidence_type: str, config: dict) -> list[dict] | None:
    """Split block when it has multiple dominant purposes (e.g. definition + example).
    Never splits mid-sentence: the cut must be at a sentence boundary and both sides
    must read as complete (no trailing/leading fragment).
    """
    curation = config.get("context_curation", {})
    definition_cues = [c.lower() for c in curation.get("definition_cues", ["refers to", "is a", "means", ":"])]
    example_cues = [c.lower() for c in curation.get("example_cues", ["for example", "for instance", "such as", "e.g."])]
    text_lower = block["text"].lower()
    has_def = any(c in text_lower for c in definition_cues)
    has_ex = any(c in text_lower for c in example_cues)
    if not (has_def and has_ex):
        return None
    # Split on example cue boundaries (sentence boundaries only)
    sentences = re.split(r"(?<=[.!?])\s+", block["text"])
    before_ex: list[str] = []
    after_ex: list[str] = []
    found_ex = False
    for sent in sentences:
        sent_lower = sent.strip().lower()
        if any(c in sent_lower for c in example_cues) and not found_ex:
            found_ex = True
            after_ex.append(sent)
        elif found_ex:
            after_ex.append(sent)
        else:
            before_ex.append(sent)
    if not before_ex or not after_ex:
        return None
    before_text = " ".join(before_ex).strip()
    after_text = " ".join(after_ex).strip()
    # Never leave first chunk ending mid-sentence (e.g. "...vs." or "...such as")
    if _INCOMPLETE_END_PATTERN.search(before_text):
        return None
    # Never leave second chunk starting mid-sentence (e.g. "hand for talking..." or "the difficulty...")
    after_starts = after_text.lstrip()
    if after_starts and after_starts[0].islower() and not after_starts.startswith('"'):
        return None
    # Use the block's original evidence_type for both halves; don't over-specify as "definition" vs "example"
    base_id = block["block_id"].replace("blk_", "unit_")
    return [
        _block_to_unit(block, f"{base_id}_d1", before_text, evidence_type),
        _block_to_unit(block, f"{base_id}_e1", after_text, evidence_type),
    ]


def split_block(block: dict, evidence_type: str, config: dict) -> list[dict]:
    """Split long blocks on sentence boundaries. Returns list of unit dicts.
    Tables: row-aware when chunking.table.row_aware is true.
    Multi-purpose: split when block has multiple dominant purposes (config multi_purpose_split).

    Section-first: when all_caps_standalone + merge_section_blocks are on and the block has a
    section_path (or was merged as section body), use overflow_max_words so we do not carve a
    merged section back into tiny type-based chunks.
    """
    curation = config.get("context_curation", {})
    chunking = curation.get("chunking", {})
    section_cfg = curation.get("section_boundaries", {})
    merge_cfg = chunking.get("merge_section_blocks", {})
    type_config = chunking.get(evidence_type, chunking.get("rule", {}))
    max_words = type_config.get("max_words", curation.get("max_block_words", 300))
    min_words = type_config.get("min_words", curation.get("min_block_words", 20))

    if (
        section_cfg.get("all_caps_standalone")
        and merge_cfg.get("enabled", False)
        and (block.get("section_path") or block.get("_section_body_merged"))
    ):
        overflow = merge_cfg.get("overflow_max_words")
        if overflow is None:
            overflow = merge_cfg.get("max_section_words", 400)
        max_words = max(max_words, int(overflow))

    # Table row-aware: split by rows when row_aware is true and rows have pipes
    # Vertical tables (PDF conversion: one cell per line, no pipes) stay as one chunk
    if evidence_type == "table" and type_config.get("row_aware"):
        rows_with_pipes = [r.strip() for r in block["text"].split("\n") if r.strip() and "|" in r]
        if len(rows_with_pipes) <= 1:
            return [_block_to_unit(block, block["block_id"].replace("blk_", "unit_"), block["text"], evidence_type)]
        units = []
        for i, row in enumerate(rows_with_pipes):
            uid = f"{block['block_id'].replace('blk_', 'unit_')}_r{i + 1}"
            units.append(_block_to_unit(block, uid, row, evidence_type))
        return units

    # Multi-purpose split: detect purpose boundaries and split
    if curation.get("multi_purpose_split"):
        multi_units = _split_multi_purpose(block, evidence_type, config)
        if multi_units:
            return multi_units

    words = block["text"].split()
    if len(words) <= max_words:
        return [_block_to_unit(block, block["block_id"].replace("blk_", "unit_"), block["text"], evidence_type)]

    sentences = re.split(r"(?<=[.!?])\s+", block["text"])
    units: list[dict] = []
    chunk: list[str] = []
    chunk_idx = 0

    for sent in sentences:
        candidate = " ".join(chunk + [sent]).strip()
        if chunk and len(candidate.split()) > max_words:
            chunk_idx += 1
            text = " ".join(chunk).strip()
            if len(text.split()) >= min_words:
                uid = f"{block['block_id'].replace('blk_', 'unit_')}_s{chunk_idx}"
                units.append(_block_to_unit(block, uid, text, evidence_type))
            chunk = [sent]
        else:
            chunk.append(sent)

    if chunk:
        chunk_idx += 1
        text = " ".join(chunk).strip()
        uid = f"{block['block_id'].replace('blk_', 'unit_')}_s{chunk_idx}"
        units.append(_block_to_unit(block, uid, text, evidence_type))

    return units


def extract_concept_candidates(text: str) -> list[str]:
    """TitleCase words and uppercase acronyms. Blacklist common words."""
    matches = re.findall(r"\b(?:[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*|[A-Z]{2,})\b", text)
    blacklist = {"The", "And", "For", "You", "Your", "When", "With", "This"}
    return [m for m in matches if m not in blacklist]


def extract_actors(text: str, config: dict) -> list[str]:
    """Extract actor terms (e.g. hero, character, player, GM). Config-based cues optional."""
    curation = config.get("context_curation", {})
    actor_cues = curation.get("actor_cues", ["hero", "character", "player", "gm", "defender", "attacker"])
    text_lower = text.lower()
    found = []
    for cue in actor_cues:
        if cue.lower() in text_lower:
            found.append(cue)
    return list(dict.fromkeys(found))


def extract_actions(text: str) -> list[str]:
    """Simple verb extraction: common action verbs near start of sentences."""
    action_verbs = {"apply", "make", "roll", "spend", "gain", "use", "take", "perform", "choose", "modify", "add", "remove"}
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    return list(dict.fromkeys(w for w in words if w in action_verbs))[:5]


def extract_state_terms(text: str, config: dict) -> list[str]:
    """Extract state-related terms. Uses state_cues if present."""
    curation = config.get("context_curation", {})
    cues = [c.lower() for c in curation.get("state_cues", [])]
    if not cues:
        return []
    text_lower = text.lower()
    return [c for c in cues if c in text_lower]


def extract_decision_terms(text: str, config: dict) -> list[str]:
    """Extract decision-related terms. Uses decision_cues if present."""
    curation = config.get("context_curation", {})
    cues = [c.lower() for c in curation.get("decision_cues", [])]
    if not cues:
        return []
    text_lower = text.lower()
    return [c for c in cues if c in text_lower]


def _strip_trailing_header_fragment(text: str) -> str:
    """Remove trailing header fragments (e.g. ' DIFFICULTY CLASS', ' ROUTINE CHECKS')."""
    if not text:
        return text
    t = text.rstrip()
    # Literal known fragments (PDF truncation artifacts)
    for suffix in (" DIFFICULTY CLASS", " ROUTINE CHECKS", " DIFFICULTY CLASSES"):
        if t.endswith(suffix):
            return t[: -len(suffix)].rstrip()
    # Generic: trailing whitespace + short all-caps fragment
    m = re.search(r"\s+([A-Z][A-Z\s]{3,35})$", t)
    if m and _is_truncated_header_fragment(m.group(1).strip()):
        return t[: m.start()].rstrip()
    return t


def _is_below_min_chunk(unit: dict, config: dict) -> bool:
    """True if unit text is below min_chunk threshold (configurable)."""
    curation = config.get("context_curation", {})
    chunking = curation.get("chunking", {})
    min_cfg = chunking.get("min_chunk", {})
    min_words = min_cfg.get("min_words", 2)
    min_chars = min_cfg.get("min_chars", 15)
    text = unit.get("text", "")
    words = len(text.split())
    return words < min_words or len(text) < min_chars


def compute_noise_score(unit: dict) -> float:
    """Heuristic 0–1 noise score. Higher = more noise."""
    text = unit.get("text", "")
    score = 0.0
    if len(text) < 30:
        score += 0.3
    if unit.get("evidence_type") == "flavor":
        score += 0.4
    if unit.get("evidence_type") == "mention":
        score += 0.3
    return min(1.0, score)


def compute_modeling_priority(unit: dict) -> float:
    """Heuristic 0–1 modeling priority. Higher = more valuable for modeling."""
    ev = unit.get("evidence_type", "domain-rule")
    priority_map = {
        "definition": 0.9,
        "domain-rule": 0.85,
        "mechanic": 0.85,
        "actor-action": 0.8,
        "state-change": 0.8,
        "table": 0.75,
        "variation/exception": 0.7,
        "example": 0.5,
        "flavor": 0.2,
        "mention": 0.3,
    }
    return priority_map.get(ev, 0.5)


def _is_chunked_output(path: Path) -> bool:
    return bool(re.search(r"__(?:slide|section|page)_\d+\.md$", path.name, re.IGNORECASE))


def _find_markdown_in(roots: list[Path]) -> tuple[Path | None, list[Path]]:
    """Search roots for .md files. Returns (folder, list of md files) or (None, [])."""
    for root in roots:
        if not root.exists():
            continue
        files = [
            f for f in root.rglob("*.md")
            if "images" not in f.parts and not _is_chunked_output(f)
        ]
        if files:
            return root, sorted(files)
    return None, []


def _has_parsed_content(ctx_dir: Path) -> bool:
    """True if context dir has context_index.json and chunks with content."""
    idx = ctx_dir / "context_index.json"
    chunks = ctx_dir / "chunks"
    if not idx.exists() or not chunks.is_dir():
        return False
    return any(chunks.glob("*.md"))


def main():
    parser = argparse.ArgumentParser(
        description="Parse markdown → blocks; classify; split; write chunks/*.md and context_index.json."
    )
    parser.add_argument("--path", default=None, help="Folder with .md files (required if source not discoverable)")
    parser.add_argument("--output", default=None, help="Output folder for context artifacts (default: from solution.conf)")
    parser.add_argument("--config", default=None, help="Path to solution.conf (default: workspace/solution.conf)")
    parser.add_argument("--force", action="store_true", help="Re-parse even when context already has parsed content")
    parser.add_argument("--add", metavar="FILE", default=None, help="Add single markdown file (parse only this file)")
    args = parser.parse_args()

    # Load config
    config: dict = {}
    ws_root: Path | None = None
    try:
        from _config import workspace_config, workspace_root as _ws_root, context_path as _context_path
        ws_root = _ws_root()
        config = workspace_config() if ws_root else {}
        get_context_path = _context_path
    except ImportError:
        get_context_path = None

    if args.config:
        cfg_path = Path(args.config).resolve()
        if cfg_path.exists():
            try:
                config = json.loads(cfg_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                print(f"Warning: could not parse config: {e}", file=sys.stderr)
    elif args.path:
        # Load config from path so we get source_path for exclusive parsing
        cfg_path = Path(args.path).resolve() / "solution.conf"
        if cfg_path.exists():
            try:
                config = json.loads(cfg_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass

    # Resolve output dir early (for skip check)
    if args.output:
        out_dir = Path(args.output).resolve()
    elif get_context_path and ws_root:
        ctx = get_context_path()
        out_dir = ctx if ctx else None
    else:
        out_dir = None

    # Skip if already parsed (unless --force)
    if out_dir and out_dir.exists() and not args.force:
        if _has_parsed_content(out_dir):
            print(f"Context already has parsed content: {out_dir}")
            print("Skipping. Use --force to re-parse.")
            sys.exit(0)

    # Resolve source: --add, --path, or discover
    path: Path | None = None
    md_files: list[Path] = []

    if args.add:
        add_path = Path(args.add).resolve()
        if not add_path.exists():
            print(f"Error: file does not exist: {add_path}", file=sys.stderr)
            sys.exit(1)
        if add_path.suffix.lower() != ".md":
            print(f"Error: --add expects .md file: {add_path}", file=sys.stderr)
            sys.exit(1)
        path = add_path.parent
        md_files = [add_path]

    elif args.path:
        path = Path(args.path).resolve()
        if not path.exists():
            print(f"Error: path does not exist: {path}", file=sys.stderr)
            sys.exit(1)
        # Parse only the configured source (e.g. docs/) — exclusive, not the whole tree
        source_subdir = config.get("source_path", "docs")
        source_root = path / source_subdir
        if not source_root.exists():
            print(f"Error: source_path '{source_subdir}' does not exist under {path}", file=sys.stderr)
            sys.exit(1)
        md_files = [
            f for f in source_root.rglob("*.md")
            if "images" not in f.parts and not _is_chunked_output(f)
        ]
        md_files = sorted(md_files)
        path = source_root

    else:
        # Discover source from workspace
        if not ws_root:
            print("Error: No workspace. Specify --path <markdown_folder>.", file=sys.stderr)
            sys.exit(1)
        source_path = config.get("source_path")
        candidates: list[Path] = []
        if source_path:
            candidates.append(ws_root / source_path)
        candidates.extend([
            ws_root / "docs",
            ws_root / "maps-models-specs",
            ws_root,
        ])
        path, md_files = _find_markdown_in(candidates)
        if not path or not md_files:
            print("Error: No markdown source found.", file=sys.stderr)
            print("  Specify --path <folder> or add source_path to solution.conf.", file=sys.stderr)
            print("  Looked in:", [str(c) for c in candidates if c.exists()], file=sys.stderr)
            sys.exit(1)
        print(f"Source: {path} ({len(md_files)} .md files)")

    if not md_files:
        print(f"No markdown files in {path}", file=sys.stderr)
        sys.exit(1)

    # Output dir (may not have been set if we skipped earlier)
    if not out_dir:
        if args.output:
            out_dir = Path(args.output).resolve()
        elif get_context_path and ws_root:
            ctx = get_context_path()
            out_dir = ctx if ctx else path / "context"
        else:
            out_dir = path / "context"

    out_dir.mkdir(parents=True, exist_ok=True)
    chunks_dir = out_dir / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    all_units: list[dict] = []
    excluded: list[dict] = []
    concepts: Counter[str] = Counter()
    by_concept: dict[str, list[str]] = defaultdict(list)
    by_evidence_type: dict[str, list[str]] = defaultdict(list)
    section_counts: dict[str, int] = defaultdict(int)
    evidence_type_counts: Counter[str] = Counter()

    for md in md_files:
        blocks = parse_markdown_to_blocks(md, config)
        blocks = split_blocks_ending_with_fragment(blocks, config)
        blocks = merge_table_like_blocks(blocks, config)
        blocks = assign_section_path_from_headers(blocks, config)
        blocks = merge_header_with_next(blocks, config)
        blocks = merge_definition_runs(blocks, config)
        blocks = merge_blocks_in_section(blocks, config)
        for block in blocks:
            evidence_type, exclusion_reason = classify_block(block, config)
            if exclusion_reason:
                excluded.append({
                    "block_id": block["block_id"],
                    "section_path": block["section_path"],
                    "reason": exclusion_reason,
                    "evidence_type": "metadata/noise",
                    "text_preview": block["text"][:200],
                })
                continue

            doc_region = assign_document_region(block, config)
            for unit in split_block(block, evidence_type, config):
                unit["text"] = _strip_trailing_header_fragment(unit.get("text", "") or "")
                if _is_below_min_chunk(unit, config):
                    excluded.append({
                        "block_id": block["block_id"],
                        "section_path": block["section_path"],
                        "reason": "below_min_chunk",
                        "evidence_type": unit.get("evidence_type", "domain-rule"),
                        "text_preview": (unit.get("text", "") or "")[:200],
                    })
                    continue
                # Per-chunk metadata
                candidate_concepts = extract_concept_candidates(unit["text"])
                unit["candidate_concepts"] = list(dict.fromkeys(candidate_concepts))  # dedupe preserve order
                unit["noise_score"] = round(compute_noise_score(unit), 2)
                unit["modeling_priority"] = round(compute_modeling_priority(unit), 2)
                unit["retrieval_tags"] = [t for t in unit["section_path"][-1:]] if unit["section_path"] else []
                unit["document_region"] = doc_region
                unit["actors"] = extract_actors(unit["text"], config)
                unit["actions"] = extract_actions(unit["text"])
                unit["state_terms"] = extract_state_terms(unit["text"], config)
                unit["decision_terms"] = extract_decision_terms(unit["text"], config)

                concepts.update(candidate_concepts)
                for c in candidate_concepts:
                    by_concept[c].append(unit["chunk_id"])
                by_evidence_type[unit["evidence_type"]].append(unit["chunk_id"])
                for sec in unit["section_path"]:
                    section_counts[sec] += 1
                evidence_type_counts[unit["evidence_type"]] += 1

                all_units.append(unit)

    # Build context_index.json
    concept_seeds = [{"concept": c, "count": n} for c, n in concepts.most_common(100)]
    forward_index: dict[str, dict] = {}
    for u in all_units:
        cid = u["chunk_id"]
        forward_index[cid] = {
            "source": u["source"],
            "section_path": u["section_path"],
            "document_region": u.get("document_region", "rules"),
            "structural_type": u["structural_type"],
            "evidence_type": u["evidence_type"],
            "start_line": u["start_line"],
            "end_line": u["end_line"],
            "candidate_concepts": u["candidate_concepts"],
            "actors": u.get("actors", []),
            "actions": u.get("actions", []),
            "state_terms": u.get("state_terms", []),
            "decision_terms": u.get("decision_terms", []),
            "noise_score": u["noise_score"],
            "modeling_priority": u["modeling_priority"],
            "retrieval_tags": u["retrieval_tags"],
        }

    manifest = {
        "sources": sorted({u["source"] for u in all_units}),
        "section_counts": dict(section_counts),
        "evidence_type_counts": dict(evidence_type_counts),
        "total_chunks": len(all_units),
        "excluded_count": len(excluded),
    }

    context_index = {
        "manifest": manifest,
        "forward_index": forward_index,
        "concept_seeds": concept_seeds,
        "reverse_indexes": {
            "by_concept": dict(by_concept),
            "by_evidence_type": dict(by_evidence_type),
        },
        "excluded": excluded,
    }

    # Write chunks/*.md — clear existing so re-runs with stricter exclusion leave no stale files
    for f in chunks_dir.glob("*.md"):
        f.unlink()
    for u in all_units:
        cid = u["chunk_id"]
        front_matter = {
            "chunk_id": cid,
            "source": u["source"],
            "evidence_type": u["evidence_type"],
            "section_path": u["section_path"],
        }
        fm_lines = ["---"]
        for k, v in front_matter.items():
            if isinstance(v, list):
                fm_lines.append(f"{k}: {json.dumps(v)}")
            else:
                fm_lines.append(f"{k}: {v}")
        fm_lines.append("---")
        body = _strip_trailing_header_fragment(u.get("text", "") or "")
        content = "\n".join(fm_lines) + "\n\n" + body
        (chunks_dir / f"{cid}.md").write_text(content, encoding="utf-8")

    # Write context_index.json
    (out_dir / "context_index.json").write_text(
        json.dumps(context_index, indent=2), encoding="utf-8"
    )

    print(f"chunks/: {len(all_units)} files")
    print(f"context_index.json: {len(concept_seeds)} concept seeds, {len(forward_index)} forward index")
    print(f"excluded: {len(excluded)} blocks")
    print(f"Written to: {out_dir}")


if __name__ == "__main__":
    main()
