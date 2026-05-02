"""Parse ``tags:`` in YAML front matter without reordering (comma, flow, or block list)."""

from __future__ import annotations

import re


def normalize_tags_scalar(raw: str) -> str:
    """Normalize a single-line ``tags`` value to ``a, b, c`` (order preserved)."""
    s = raw.strip().strip('"').strip("'")
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return ""
        parts = [p.strip().strip('"').strip("'") for p in inner.split(",")]
        return ", ".join(p for p in parts if p)
    return s


def _parse_tags_at(lines: list[str], start: int) -> tuple[str, int]:
    """Parse ``tags:`` starting at ``lines[start]``. Returns ``(comma_joined, next_line_index)``."""
    m = re.match(r"^(\s*)tags:\s*(.*)$", lines[start].rstrip("\r"))
    if not m:
        return "", start
    inline = (m.group(2) or "").strip()
    base_indent = len(m.group(1))
    if inline.startswith("["):
        return normalize_tags_scalar(inline), start + 1
    if inline:
        return inline.strip().strip('"').strip("'"), start + 1

    items: list[str] = []
    j = start + 1
    while j < len(lines):
        t = lines[j].rstrip("\r")
        if not t.strip():
            j += 1
            continue
        ind = len(t) - len(t.lstrip())
        if ind <= base_indent:
            break
        item_m = re.match(r"^\s*-\s+(.+)$", t)
        if item_m:
            items.append(item_m.group(1).strip().strip('"').strip("'"))
            j += 1
            continue
        break
    return ", ".join(items), j


def ordered_tags_from_frontmatter_block(block: str) -> str:
    """First top-level ``tags:`` field (line starts with ``tags:``), order preserved."""
    lines = block.splitlines()
    for i, line in enumerate(lines):
        if not re.match(r"^tags:\s*", line):
            continue
        val, _ = _parse_tags_at(lines, i)
        if val:
            return val
    return ""


def parse_tags_list(tags_val: str) -> list[str]:
    """Split normalized or raw front matter ``tags`` into ordered tokens (lowercase not applied)."""
    if not tags_val or not str(tags_val).strip():
        return []
    s = normalize_tags_scalar(str(tags_val))
    if not s:
        return []
    return [p.strip() for p in s.split(",") if p.strip()]


def tags_contain(tags_val: str, tag: str) -> bool:
    """True if ``tag`` matches a list entry (case-insensitive)."""
    if not tag or not tags_val:
        return False
    want = tag.strip().lower()
    return any(t.strip().lower() == want for t in parse_tags_list(tags_val))
