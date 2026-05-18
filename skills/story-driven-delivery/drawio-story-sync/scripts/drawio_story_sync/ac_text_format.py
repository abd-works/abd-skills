"""Acceptance criteria text shaping for exploration / acceptance-criteria diagrams.

Rendered cells use lightweight HTML (`html=1`) with WHEN / THEN / AND emphasis and
multi-line layouts. Companion helpers reconstruct plain strings for multiset sync
against graph JSON (canonical compare keys tolerate numbering and markup).
"""

from __future__ import annotations

import html as html_escape
import re
from collections import defaultdict
from typing import DefaultDict

_ORDINAL_PREFIX_RE = re.compile(r"^\s*\d+\.\s+")

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_HTML_ENTITY_MAP = {
    "&amp;": "&",
    "&lt;": "<",
    "&gt;": ">",
    "&quot;": '"',
    "&nbsp;": " ",
    "&#39;": "'",
}

# ``**WHEN**`` / WHEN / etc. strip / normalize prior to detecting structure
_KEYWORD_BOLD_MD_RE = re.compile(
    r"\*{2}\s*(WHEN|THEN|AND)\s*\*{2}", re.IGNORECASE
)

_WHENTHEN_RE = re.compile(
    r"(?is)\bWHEN\b\s*(.+?)\s*\bTHEN\b\s*(.+)$")


def strip_ordinal_prefix(s: str) -> str:
    return _ORDINAL_PREFIX_RE.sub("", (s or "").strip())


def plain_ac_from_cell_value(val: str) -> str:
    """Plain one-line-ish text recovered from drawn cell markup or raw JSON."""

    def _squish_spaces(t: str) -> str:
        return " ".join(t.split()).strip()

    if not val:
        return ""
    v = val.strip()
    if "<" not in v:
        v = strip_ordinal_prefix(v)
        v = _KEYWORD_BOLD_MD_RE.sub(lambda m: m.group(1).upper(), v)
        return _squish_spaces(v.replace("**", ""))

    t = v.replace("<div>", "").replace("</div>", " ")
    t = re.sub(r"(?is)<br\s*/?>", " ", t)
    t = _HTML_TAG_RE.sub("", t)
    for entity, ch in _HTML_ENTITY_MAP.items():
        t = t.replace(entity, ch)
    t = _squish_spaces(t)
    return strip_ordinal_prefix(t)


def canonical_ac_key(s: str) -> str:
    """Multiset identity for comparing diagram cells to graph acceptance strings."""
    base = plain_ac_from_cell_value(s)
    return " ".join(base.split()).strip()


def format_ac_diagram_html(raw: str) -> str:
    """Produce Draw.io html=1 markup: no ordinal; WHEN / THEN / AND bold; line breaks."""
    if not raw:
        return ""
    work = strip_ordinal_prefix((raw or "").strip())
    work = _KEYWORD_BOLD_MD_RE.sub(lambda m: m.group(1).upper(), work)

    m = _WHENTHEN_RE.search(work)
    if not m:
        return html_escape.escape(work)

    when_body = m.group(1).strip()
    then_rest = m.group(2).rstrip()
    then_rest = re.sub(r"\s*---+\s*$", "", then_rest)
    parts = [p.strip() for p in re.split(r"\s+AND\s+", then_rest) if p.strip()]

    out: list[str] = []
    out.append("<b>WHEN</b> ")
    out.append(html_escape.escape(when_body))
    out.append("<br/><b>THEN</b> ")
    if parts:
        out.append(html_escape.escape(parts[0]))
    for clause in parts[1:]:
        out.append("<br/><b>AND</b> ")
        out.append(html_escape.escape(clause))
    return "".join(out)


def ac_cell_height_px(formatted_html: str, *, min_px: float, line_px: float, pad_px: float) -> float:
    """Approximate stacked height when WHEN/THEN split or AND lines added."""
    n_breaks = len(re.findall(r"(?is)<br\s*/?>", formatted_html))
    lines = 1 + n_breaks
    return max(min_px, pad_px + line_px * float(lines))


def diagram_desired_buckets(desired_texts: list[str]) -> tuple[dict[str, int], DefaultDict[str, list[str]]]:
    """Canon-key counts plus ordered exemplar plaintext per key (diagram side)."""

    buckets: DefaultDict[str, list[str]] = defaultdict(list)
    for t in desired_texts:
        if not isinstance(t, str):
            t = str(t)
        t = t.strip()
        if not t:
            continue
        ck = canonical_ac_key(t)
        plain = plain_ac_from_cell_value(t)
        buckets[ck].append(plain)
    counts = {k: len(v) for k, v in buckets.items()}
    return counts, buckets
