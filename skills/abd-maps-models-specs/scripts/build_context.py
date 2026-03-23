#!/usr/bin/env python3
"""
Phase 1 — emit ``chunks/*.md`` + ``context_index.json`` for the active skill workspace.

Chunk **segmentation** matches ``skills/abd-context-to-memory/scripts/chunk_markdown.py`` (slides,
``#``/``##`` splits for large docs, CHAPTER markers, or whole small files). Optional
``handbook_subsection_chunking: true`` in ``context_chunking_spec.yaml`` adds ALL CAPS subsection
splits for flat PDF handbooks (see ``context_chunk_from_memory.segment_markdown``). Shaping
(**front matter**, ``blocks[]``, ``manifest``) follows ``content/parts/library/context-spec.md``.

Usage::

    python scripts/build_context.py [--dry-run]

Optional (tests / alternate ``solution.conf``)::

    python scripts/build_context.py --config <path/to/solution.conf>

Configuration: ``<skill>/conf/abd-config.json`` → workspace root → ``solution.conf``
(``manifest_sources[]``, ``context_path``, ``context_chunking_spec``) via ``_config.py``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

__version__ = "0.1.0"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


def _parse_handbook_subsection_chunking(yaml_text: str) -> bool:
    """Optional: ``handbook_subsection_chunking: true`` in ``context_chunking_spec.yaml``."""
    for raw in yaml_text.splitlines():
        s = raw.split("#", 1)[0].strip()
        if re.match(r"handbook_subsection_chunking:\s*true\b", s, re.I):
            return True
    return False


def _parse_chunking_defaults(yaml_text: str) -> tuple[str, str]:
    """Read ``defaults.evidence_type`` / ``defaults.modeling_kind`` without PyYAML."""
    evidence_type, modeling_kind = "rule", "rule"
    in_defaults = False
    for raw in yaml_text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("defaults:"):
            in_defaults = True
            continue
        if in_defaults:
            if stripped and not raw[:1].isspace() and ":" in stripped and not stripped.startswith("#"):
                key = stripped.split(":", 1)[0].strip()
                if key not in ("evidence_type", "modeling_kind"):
                    in_defaults = False
            if in_defaults:
                m = re.match(r"evidence_type:\s*(.+)$", stripped)
                if m:
                    evidence_type = m.group(1).strip().strip("\"'")
                m = re.match(r"modeling_kind:\s*(.+)$", stripped)
                if m:
                    modeling_kind = m.group(1).strip().strip("\"'")
    return evidence_type, modeling_kind


def _chunk_id(canonical_rel: str, line_start: int, line_end: int, label: str) -> str:
    h = hashlib.sha256(
        f"{canonical_rel}\n{line_start}\n{line_end}\n{label}".encode()
    ).hexdigest()[:12]
    return f"blk_{h}"


def _fm_yaml_lines(
    *,
    chunk_id: str,
    canonical_path: str,
    line_start: int,
    line_end: int,
    evidence_type: str,
    modeling_kind: str,
) -> list[str]:
    """Nested ``source`` block; flat lines parse for ``chunk_id`` in contract scanner."""
    return [
        "---",
        f"chunk_id: {chunk_id}",
        "source:",
        f"  canonical_path: {canonical_path}",
        f"  line_start: {line_start}",
        f"  line_end: {line_end}",
        f"evidence_type: {evidence_type}",
        f"modeling_kind: {modeling_kind}",
        "---",
        "",
    ]


def _preview(body: str, n: int = 160) -> str:
    one = " ".join(body.split())
    return one[:n] + ("…" if len(one) > n else "")


def _preview_handbook_trim(body: str, n: int = 160) -> str:
    """Skip common page chrome so previews start near the subsection body."""
    parts: list[str] = []
    for line in body.split("\n"):
        s = line.strip()
        if not s:
            continue
        if s.startswith("<!--"):
            continue
        u = s.upper()
        if re.match(r"^CHAPTER\s+\d+\s*:", s, re.I):
            continue
        if "MUTANTS" in u and "MASTERMIND" in u:
            continue
        if u.startswith("DELUXE HERO"):
            continue
        if s.isdigit() and len(s) <= 4:
            continue
        if s.startswith("\f") or (s and ord(s[0]) == 12):
            continue
        parts.append(s)
        if len(parts) >= 2 and len(" ".join(parts)) >= min(n, 48):
            break
        if len(" ".join(parts)) >= n + 50:
            break
    one = " ".join(parts)
    if not one:
        return _preview(body, n=n)
    return one[:n] + ("…" if len(one) > n else "")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build Phase 1 context package (chunks + index).")
    ap.add_argument("--dry-run", action="store_true", help="Print plan only; no writes.")
    ap.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Use this solution.conf (must sit under the declared workspace root).",
    )
    ns = ap.parse_args()

    if ns.config is not None:
        import importlib

        import _config as cfg

        cfg.set_solution_conf_override(ns.config.resolve())
        importlib.reload(cfg)

    from context_chunk_from_memory import (
        decorate_segment_body,
        handbook_section_path_from_body,
        section_path_from_body,
        segment_markdown,
    )

    from _config import (
        CHUNKS_DIR,
        CONTEXT_INDEX,
        SKILL_ROOT,
        context_chunking_spec_path,
        resolved_manifest_sources,
        workspace_root,
    )

    spec_path = context_chunking_spec_path()
    if not spec_path.is_file():
        print(f"abd-maps-models-specs: missing context_chunking_spec: {spec_path}", file=sys.stderr)
        return 1

    yaml_text = spec_path.read_text(encoding="utf-8", errors="replace")
    evidence_type_d, modeling_kind_d = _parse_chunking_defaults(yaml_text)
    use_handbook_sub = _parse_handbook_subsection_chunking(yaml_text)

    sources = resolved_manifest_sources()
    if not sources:
        print(
            "abd-maps-models-specs: solution.conf has no manifest_sources[] entries",
            file=sys.stderr,
        )
        return 1

    root = workspace_root()
    manifest_rows: list[dict] = []
    blocks: list[dict] = []

    for abs_p, role, rel_posix in sources:
        if not abs_p.is_file():
            print(f"abd-maps-models-specs: manifest source missing: {abs_p}", file=sys.stderr)
            return 1
        if abs_p.suffix.lower() != ".md":
            print(f"abd-maps-models-specs: skip non-markdown manifest source: {rel_posix}", file=sys.stderr)
            continue
        raw = abs_p.read_bytes()
        manifest_rows.append(
            {
                "path": rel_posix,
                "role": role,
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        )

    if not manifest_rows:
        print("abd-maps-models-specs: no .md entries in manifest_sources[]", file=sys.stderr)
        return 1

    if ns.dry_run:
        print("build_context.py dry-run:")
        print(f"  workspace: {root}")
        print(f"  chunks_dir: {CHUNKS_DIR}")
        print(f"  index: {CONTEXT_INDEX}")
        print(f"  spec: {spec_path}")
        print(f"  defaults: evidence_type={evidence_type_d!r} modeling_kind={modeling_kind_d!r}")
        print(f"  handbook_subsection_chunking: {use_handbook_sub}")
        for abs_p, role, rel_posix in sources:
            if abs_p.suffix.lower() != ".md":
                continue
            text = abs_p.read_text(encoding="utf-8", errors="replace")
            segs = segment_markdown(
                text, stem=abs_p.stem, handbook_subsection_chunking=use_handbook_sub
            )
            print(f"  {rel_posix}: {len(segs)} segment(s)")
        return 0

    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    for old in CHUNKS_DIR.glob("*.md"):
        old.unlink()

    for abs_p, role, rel_posix in sources:
        if abs_p.suffix.lower() != ".md":
            continue
        text = abs_p.read_text(encoding="utf-8", errors="replace")
        segs = segment_markdown(
            text, stem=abs_p.stem, handbook_subsection_chunking=use_handbook_sub
        )
        for seg in segs:
            body = decorate_segment_body(seg, text)
            cid = _chunk_id(rel_posix, seg.line_start, seg.line_end, seg.label)
            if use_handbook_sub:
                section_path = handbook_section_path_from_body(
                    body, chapter_hint=seg.handbook_chapter_line
                )
                pv = _preview_handbook_trim(body)
            else:
                section_path = section_path_from_body(body)
                pv = _preview(body)
            et = seg.evidence_type if seg.evidence_type is not None else evidence_type_d
            mk = seg.modeling_kind if seg.modeling_kind is not None else modeling_kind_d
            fm = _fm_yaml_lines(
                chunk_id=cid,
                canonical_path=rel_posix,
                line_start=seg.line_start,
                line_end=seg.line_end,
                evidence_type=et,
                modeling_kind=mk,
            )
            chunk_path = CHUNKS_DIR / f"{cid}.md"
            chunk_path.write_text("\n".join(fm) + body + "\n", encoding="utf-8")
            blocks.append(
                {
                    "chunk_id": cid,
                    "section_path": section_path,
                    "evidence_type": et,
                    "modeling_kind": mk,
                    "source_anchor": {
                        "canonical_path": rel_posix,
                        "line_start": seg.line_start,
                        "line_end": seg.line_end,
                    },
                    "preview": pv,
                }
            )

    index = {
        "spec_version": "1",
        "manifest": {
            "sources": manifest_rows,
            "generator": {"name": "build_context.py", "version": __version__},
        },
        "blocks": blocks,
        "excluded": [],
    }
    CONTEXT_INDEX.parent.mkdir(parents=True, exist_ok=True)
    CONTEXT_INDEX.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(
        f"Wrote {len(blocks)} chunks under {CHUNKS_DIR.relative_to(SKILL_ROOT)}; "
        f"index {CONTEXT_INDEX.relative_to(SKILL_ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
