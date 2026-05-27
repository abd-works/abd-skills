"""Minimal stub for frontmatter tag helpers used by generate_abd_catalog.py."""
from __future__ import annotations
import re


def ordered_tags_from_frontmatter_block(block: str) -> list[str]:
    m = re.search(r"^tags\s*:\s*\[([^\]]*)\]", block, re.MULTILINE)
    if m:
        return [t.strip().strip('"\'') for t in m.group(1).split(",") if t.strip()]
    m = re.search(r"^tags\s*:\s*(.+)", block, re.MULTILINE)
    if m:
        return [t.strip().strip('"\'') for t in m.group(1).split(",") if t.strip()]
    return []


def normalize_tags_scalar(tags: object) -> list[str]:
    if isinstance(tags, list):
        return tags
    return [t.strip() for t in str(tags).split(",") if t.strip()]


def parse_tags_list(tags: object) -> list[str]:
    return normalize_tags_scalar(tags)
