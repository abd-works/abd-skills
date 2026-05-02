"""Markdown table parser shared by abd-cost-of-delay scanners."""
from __future__ import annotations

import re
from pathlib import Path


def find_markdown_files(workspace: Path, pattern: str) -> list[Path]:
    """Recursively find markdown files whose name matches *pattern* (glob)."""
    return sorted(workspace.rglob(pattern))


def parse_table(lines: list[str], header_pattern: re.Pattern) -> list[dict[str, str]]:
    """Parse a markdown table whose header row matches *header_pattern*.

    Returns a list of dicts keyed by lowercased, stripped header cell text.
    Stops at the first blank line or non-table line after the header.
    """
    rows: list[dict[str, str]] = []
    headers: list[str] = []
    in_table = False

    for line in lines:
        stripped = line.strip()
        if not in_table:
            if stripped.startswith("|") and header_pattern.search(stripped):
                headers = [h.strip().lower() for h in stripped.split("|")[1:-1]]
                in_table = True
            continue
        if re.match(r"^\|[\s\-:|]+\|$", stripped):
            continue
        if not stripped.startswith("|"):
            break
        cells = [c.strip() for c in stripped.split("|")[1:-1]]
        if cells and cells[0].startswith("**") and "total" in cells[0].lower():
            continue
        row = {}
        for i, h in enumerate(headers):
            row[h] = cells[i] if i < len(cells) else ""
        rows.append(row)

    return rows


def field_value(lines: list[str], field_name: str) -> str | None:
    """Find ``| **Field Name** | value |`` style rows and return the value cell."""
    pattern = re.compile(
        r"^\|\s*\*?\*?" + re.escape(field_name) + r"\*?\*?\s*\|\s*(.*?)\s*\|",
        re.IGNORECASE,
    )
    for line in lines:
        m = pattern.match(line.strip())
        if m:
            val = m.group(1).strip().strip("*").strip()
            return val if val else None
    return None
