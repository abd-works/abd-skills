"""Shared utilities for abd-secure-code language scanners."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable, Iterable

# Allow `from scan_utils import ...` from scanners/python|javascript|java/
_COMMON_DIR = Path(__file__).resolve().parent
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

_SKIP_LINE = re.compile(
    r"(?i)(example|placeholder|dummy|fake_|changeme|xxx|todo:|fixme:|nosec|pragma:\s*no cover)"
)

_SECURITY_CONTEXT = re.compile(
    r"(?i)(token|session|secret|password|csrf|nonce|salt|iv|key|auth|credential|otp|reset)"
)


def violation(
    rule: str,
    message: str,
    location: str,
    line: int,
    severity: str = "error",
) -> dict:
    return {
        "rule": rule,
        "message": message,
        "location": location,
        "line": line,
        "severity": severity,
    }


def should_skip_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or stripped.startswith("//"):
        return True
    if stripped.startswith("*") and not stripped.startswith("**"):
        return True
    return bool(_SKIP_LINE.search(line))


def read_lines(file_path: str | Path) -> list[str]:
    return Path(file_path).read_text(encoding="utf-8", errors="ignore").splitlines()


def line_has_security_context(lines: list[str], index: int, window: int = 4) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    block = "\n".join(lines[start:end])
    return bool(_SECURITY_CONTEXT.search(block))


def scan_lines_with_patterns(
    rule: str,
    file_path: str,
    lines: Iterable[str],
    patterns: list[tuple[re.Pattern[str], str]],
    *,
    require_security_context: bool = False,
    skip_fn: Callable[[str], bool] | None = None,
) -> list[dict]:
    """Run regex patterns line-by-line; optional security-context gate reduces noise."""
    skip = skip_fn or should_skip_line
    violations: list[dict] = []
    line_list = list(lines)

    for i, line in enumerate(line_list, start=1):
        if skip(line):
            continue
        if require_security_context and not line_has_security_context(line_list, i - 1):
            continue
        for pattern, message in patterns:
            if pattern.search(line):
                violations.append(violation(rule, message, file_path, i))
                break
    return violations


def scan_files_with_patterns(
    rule: str,
    file_paths: Iterable[str],
    patterns: list[tuple[re.Pattern[str], str]],
    *,
    require_security_context: bool = False,
) -> list[dict]:
    out: list[dict] = []
    for file_path in file_paths:
        try:
            lines = read_lines(file_path)
        except OSError:
            continue
        out.extend(
            scan_lines_with_patterns(
                rule,
                file_path,
                lines,
                patterns,
                require_security_context=require_security_context,
            )
        )
    return out
