"""
Parse rule markdown (YAML frontmatter + body) and decide if a rule applies to an operation.

When ``operations`` is omitted, defaults are inferred from the filename stem prefix
(see ``PREFIX_DEFAULT_OPERATIONS``). Set ``every_operation: true`` to include everywhere.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

# Operations that ever include ``story_synthesizer.validation.rules`` in skill-config.json
ALL_OPS_WITH_RULES: tuple[str, ...] = (
    "concept_scan",
    "extract_evidence",
    "model_discovery",
    "model_validation",
    "create_strategy",
    "validate_session",
    "run_slice",
    "generate_slice",
    "validate_run",
    "validate_slice",
)

# Default ``operations`` when frontmatter omits ``operations:`` — longest prefix wins (see ``default_operations_for_stem``).
PREFIX_DEFAULT_OPERATIONS: dict[str, tuple[str, ...]] = {
    "context-slice-": (
        "create_strategy",
        "validate_session",
        "run_slice",
        "generate_slice",
        "validate_run",
        "validate_slice",
    ),
    "context-": (
        "concept_scan",
        "model_discovery",
        "model_validation",
    ),
    "domain-": (
        "model_discovery",
        "model_validation",
        "create_strategy",
        "run_slice",
        "generate_slice",
        "validate_run",
        "validate_slice",
    ),
    "interaction-": (
        "model_discovery",
        "model_validation",
        "create_strategy",
        "run_slice",
        "generate_slice",
        "validate_run",
        "validate_slice",
    ),
    "session-": ("create_strategy", "validate_session", "run_slice", "generate_slice", "validate_slice"),
    "correction-": tuple(),  # not injected via validation.rules today; explicit ``operations`` if needed
    "verb-": ("run_slice", "generate_slice", "validate_run", "validate_slice", "model_discovery", "model_validation"),
    "scaffold-": ("model_discovery", "run_slice", "generate_slice", "validate_run", "validate_slice"),
}


def split_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    """Return (meta, body). Meta is {} if missing or unparseable."""
    if not raw.startswith("---"):
        return {}, raw
    m = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*", raw, re.DOTALL)
    if not m:
        return {}, raw
    block = m.group(1)
    body = raw[m.end() :]
    if yaml is None:
        return {}, body
    try:
        meta = yaml.safe_load(block)
        if not isinstance(meta, dict):
            meta = {}
    except yaml.YAMLError:
        meta = {}
    return meta, body


def default_operations_for_stem(stem: str) -> tuple[str, ...]:
    """Infer operations from filename prefix (stem uses hyphens). Longest prefix match wins."""
    for prefix, ops in sorted(
        PREFIX_DEFAULT_OPERATIONS.items(),
        key=lambda kv: -len(kv[0]),
    ):
        if stem.startswith(prefix):
            return ops
    return ALL_OPS_WITH_RULES


def rule_applies_to_operation(meta: dict[str, Any], stem: str, operation: str) -> bool:
    if meta.get("every_operation"):
        return True
    explicit = meta.get("operations")
    if isinstance(explicit, list) and explicit:
        return operation in explicit
    return operation in default_operations_for_stem(stem)


def merge_rules_markdown_for_operation(rules_dir: Path, operation: str) -> str:
    """Concatenate rule bodies (frontmatter stripped) that apply to *operation*."""
    if not rules_dir.is_dir():
        return ""
    parts: list[str] = []
    for md in sorted(rules_dir.glob("*.md")):
        if md.name.lower() == "readme.md":
            continue
        raw = md.read_text(encoding="utf-8")
        meta, body = split_frontmatter(raw)
        stem = md.stem.replace("_", "-")
        if not rule_applies_to_operation(meta, stem, operation):
            continue
        body = body.strip()
        if body:
            parts.append(body)
            parts.append("\n\n---\n\n")
    return "".join(parts).rstrip() if parts else ""
