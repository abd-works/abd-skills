#!/usr/bin/env python3
"""AI discovery pass: analyze markdown and write context_curation to solution.conf.

Step 2 — runs after convert, before parse_and_curate.

Usage:
  python discover_context_structure.py [--path <markdown_folder>] [--config <solution.conf>]
  python discover_context_structure.py --no-reparse   # Skip deleting chunks and re-parsing

Samples markdown (stratified: beginning, middle, end), asks AI to identify:
- Heading patterns, table patterns
- Noise sections (TOC, index, legal, etc.)
- Definition/example cues for this corpus
- Chunking rules by evidence_type

By default, deletes all chunks and context_index.json, then re-runs parse_and_curate from scratch.

Requires: OPENAI_API_KEY, pip install openai
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Resolve script dir for _config
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

# What the parser actually supports. If AI outputs something else, we warn.
_PARSER_SUPPORTED_SECTION_BOUNDARIES = frozenset({"all_caps_standalone"})
# chapter_pattern, markdown_hash, etc. — add here when parser implements them


def _validate_parser_compatibility(curation: dict) -> list[tuple[str, str]]:
    """Check if section_boundaries and structure AI found are supported by the parser.
    Returns list of (config_key, warning_message) for unsupported config.
    """
    mismatches: list[tuple[str, str]] = []
    section_cfg = curation.get("section_boundaries") or {}
    for key, val in section_cfg.items():
        if val and key not in _PARSER_SUPPORTED_SECTION_BOUNDARIES:
            mismatches.append(
                (f"section_boundaries.{key}",
                 f"Parser does NOT support '{key}'. The sections/dividers found won't work. "
                 f"Update parse_and_curate.py to support it.")
            )
    return mismatches


def _clear_context_and_reparse(
    config_path: Path,
    workspace_root: Path,
    path: Path,
) -> bool:
    """Delete chunks/* and context_index.json, then run parse_and_curate --force. Returns True on success."""
    config: dict = {}
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    # Resolve context dir: context_path or output_dir/context
    ctx_path = config.get("context_path")
    out_dir = config.get("output_dir", "solution")
    if ctx_path:
        ctx_dir = workspace_root / ctx_path
    else:
        ctx_dir = workspace_root / out_dir / "context"

    if not ctx_dir.exists():
        print(f"Context dir not found: {ctx_dir}", file=sys.stderr)
        return False

    chunks_dir = ctx_dir / "chunks"
    idx_file = ctx_dir / "context_index.json"
    deleted = 0
    if chunks_dir.is_dir():
        for f in chunks_dir.glob("*.md"):
            f.unlink()
            deleted += 1
        print(f"Deleted {deleted} chunks from {chunks_dir}")
    if idx_file.exists():
        idx_file.unlink()
        print(f"Deleted {idx_file.name}")

    parse_script = _SCRIPT_DIR / "parse_and_curate.py"
    cmd = [
        sys.executable,
        str(parse_script),
        "--path", str(path),
        "--config", str(config_path),
        "--force",
    ]
    result = subprocess.run(cmd, cwd=str(workspace_root))
    return result.returncode == 0


def _sample_markdown(md_path: Path, pct: float = 0.15) -> str:
    """Sample ~pct of file, stratified: beginning, middle, end."""
    lines = md_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    n = len(lines)
    if n <= 500:
        return "\n".join(lines)
    chunk = max(1, int(n * pct / 3))
    parts = [
        "\n".join(lines[:chunk]),
        "\n".join(lines[n // 2 - chunk // 2 : n // 2 + chunk // 2]),
        "\n".join(lines[-chunk:]),
    ]
    return "\n\n--- [MIDDLE] ---\n\n".join(parts)


def _call_ai(sample: str, source_name: str) -> dict | None:
    try:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    except ImportError:
        print("Error: pip install openai", file=sys.stderr)
        return None
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: set OPENAI_API_KEY", file=sys.stderr)
        return None

    # Read parse_and_curate.py so AI knows what config the parser actually consumes
    parser_path = _SCRIPT_DIR / "parse_and_curate.py"
    parser_code = parser_path.read_text(encoding="utf-8", errors="ignore")[:6000] if parser_path.exists() else ""

    system = """You analyze markdown structure to produce a context_curation config for deterministic parsing.
Output ONLY valid JSON for the "context_curation" object. No markdown, no explanation.

CRITICAL: Read the parse_and_curate.py code in the user message. The parser only uses config keys it actually reads.
If the config you output won't work with the parser, the parser will be fixed to consume it — but your output must
describe section boundaries and other structure in a way that CAN be implemented. Be explicit."""

    user = f"""Analyze this markdown sample from "{source_name}". Identify how structure manifests in THIS document.

FIRST: Read the parse_and_curate.py snippet below. It shows what the parser does. The parser currently only recognizes
# markdown headings as section boundaries. If this document uses ALL CAPS standalone lines (e.g. "THE CORE MECHANIC",
"THE GAMEMASTER") or "CHAPTER X: Y" as section breaks, you MUST output section_boundaries so the parser can be
updated to treat them as section boundaries. If the config schema doesn't support what you need, say so — we fix the code.

Output a JSON object with these keys (use arrays of strings unless noted):
- table_pattern: regex or short description of how tables appear (e.g. "pipe syntax | col | col |", "HTML <table>")
- heading_pattern: regex or short description of how section headers are marked (e.g. "# Heading", "## Subheading", "ALL CAPS standalone line")
- section_boundaries: object — REQUIRED when document has obvious section breaks. Keys:
  - all_caps_standalone: true if standalone ALL CAPS lines (e.g. "THE CORE MECHANIC", "THE GAMEMASTER") mark section boundaries
  - chapter_pattern: true if "CHAPTER N: TITLE" or similar marks major sections
  - markdown_hash: true if # headings are used (default true if not specified)
- noise_heading_keywords: headings that indicate TOC, index, glossary, legal, credits — exclude from content
- definition_cues: phrases that signal a formal definition (e.g. "refers to", "is a", "means", ":")
- example_cues: phrases that signal an example (e.g. "for example", "for instance", "such as", "e.g.")
- flavor_cues: (optional) phrases for narrative/flavor text
- mechanic_cues: (optional) phrases for procedures (e.g. "procedure", "how to", "step 1")
- variation_cues: (optional) phrases for exceptions (e.g. "however", "exception", "unless")
- decision_cues: (optional) phrases for domain rules/decisions
- state_cues: (optional) phrases for state transitions
- actor_cues: (optional) actor terms (e.g. "hero", "character", "player")
- chunking: object with keys "definition", "rule", "table", "example" — each with max_words, min_words (numbers); table may have row_aware: true; add merge_section_blocks: {{"enabled": true, "max_section_words": 400}} to merge consecutive blocks in the same section
- document_region_keywords: (optional) object with keys "front_matter", "toc", "rules", "examples", "glossary", "appendix", "legal" — each an array of keyword strings
- multi_purpose_split: (optional) true if document has blocks mixing definition+example

Be specific to this document type. Identify domain-appropriate patterns. If you see ALL CAPS section headers that
group content (e.g. "THE CORE MECHANIC" ... "THE GAMEMASTER"), set section_boundaries.all_caps_standalone: true.

PARSER CODE (parse_and_curate.py) — what it currently does:
```python
{parser_code}
```

MARKDOWN SAMPLE:
{sample}
"""

    try:
        resp = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=2048,
            temperature=0,
        )
        text = resp.choices[0].message.content or ""
        # Extract JSON (handle markdown code blocks)
        if "```" in text:
            start = text.find("```")
            if "json" in text[:start + 10].lower():
                start = text.find("\n", start) + 1
            end = text.find("```", start)
            text = text[start:end] if end > start else text[start:]
        return json.loads(text.strip())
    except json.JSONDecodeError as e:
        print(f"Error: AI output not valid JSON: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI discovery: analyze markdown → context_curation in solution.conf")
    parser.add_argument("--path", default=None, help="Folder with .md files (default: discover from workspace)")
    parser.add_argument("--config", default=None, help="Path to solution.conf (default: workspace/solution.conf)")
    parser.add_argument("--no-reparse", action="store_true", help="Skip deleting chunks and re-running parse (default: delete and re-parse)")
    args = parser.parse_args()

    ws_root: Path | None = None
    try:
        from _config import workspace_root, workspace_config, context_path
        ws_root = workspace_root()
    except ImportError:
        pass

    config_path = Path(args.config).resolve() if args.config else None
    if not config_path and ws_root:
        config_path = ws_root / "solution.conf"
    if not config_path or not config_path.exists():
        print("Error: solution.conf not found. Specify --config or set solution_workspace.", file=sys.stderr)
        sys.exit(1)

    # Resolve markdown source
    path: Path | None = None
    md_files: list[Path] = []
    if args.path:
        path = Path(args.path).resolve()
        md_files = sorted(f for f in path.rglob("*.md") if "images" not in f.parts)
    elif ws_root:
        cfg = {}
        if config_path.exists():
            try:
                cfg = json.loads(config_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        for candidate in [ws_root / cfg.get("source_path", ""), ws_root / "docs", ws_root / "maps-models-specs", ws_root]:
            if candidate.exists():
                md_files = sorted(f for f in candidate.rglob("*.md") if "images" not in f.parts)
                if md_files:
                    path = candidate
                    break

    if not md_files:
        print("Error: No markdown files found. Specify --path.", file=sys.stderr)
        sys.exit(1)

    # Sample first (largest) file
    md_path = max(md_files, key=lambda p: p.stat().st_size)
    print(f"Sampling: {md_path.name} ({md_path.stat().st_size // 1024} KB)")
    sample = _sample_markdown(md_path)
    print(f"Sample size: {len(sample)} chars")

    curation = _call_ai(sample, md_path.stem)
    if not curation:
        sys.exit(1)

    # Validate: warn if AI found section boundaries the parser doesn't support
    mismatches = _validate_parser_compatibility(curation)
    if mismatches:
        print(file=sys.stderr)
        print("WARNING: The sections, dividers, or structure found in this document are NOT fully supported by the parser.", file=sys.stderr)
        print("The following config will NOT work until the parser is updated:", file=sys.stderr)
        for key, msg in mismatches:
            print(f"  - {key}: {msg}", file=sys.stderr)
        print(file=sys.stderr)
        print("Update parse_and_curate.py to support these, or chunking may not respect section boundaries.", file=sys.stderr)
        print(file=sys.stderr)

    # Merge into solution.conf
    config: dict = {}
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    config["context_curation"] = curation
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"Written context_curation to {config_path}")

    # Delete all chunks and re-parse from scratch (unless --no-reparse)
    if not args.no_reparse:
        workspace_root = config_path.parent
        # path is the folder containing the sampled md (e.g. docs/ or workspace root)
        parse_path = path
        if not args.path and ws_root:
            # Discovered path may be a subdir; parse expects workspace root
            parse_path = ws_root
        if _clear_context_and_reparse(config_path, workspace_root, parse_path):
            print("Re-parse complete.")
        else:
            print("Re-parse failed. Run parse_and_curate.py --force manually.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
