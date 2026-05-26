"""Run pattern-catalog scans for a rule + language."""
from __future__ import annotations

import re
import sys
from pathlib import Path

_COMMON = Path(__file__).resolve().parent
if str(_COMMON) not in sys.path:
    sys.path.insert(0, str(_COMMON))

from pattern_catalog import (  # noqa: E402
    CONTEXT_GATED_RULES,
    context_gated_patterns,
    patterns_for,
)
from scan_utils import (  # noqa: E402
    read_lines,
    scan_files_with_patterns,
    scan_lines_with_patterns,
    violation,
)

_HASH_NEARBY = re.compile(r"(?i)(hash|bcrypt|argon2|scrypt|pbkdf2|passlib|PasswordHasher|BCryptPasswordEncoder)")
_ENCRYPT_NEARBY = re.compile(
    r"(?i)(encrypt|cipher|kms|Fernet|Envelope|AES|vault|tokenize|tokenization|field_encrypt|piiCipher)"
)
_DTO_NEARBY = re.compile(
    r"(?i)(\btoDto\b|\btoDTO\b|\bmapToDTO\b|\bUserResponse\b|\bPatientDto\b|\bPatientSummary\b|\bfromEntity\b|\.from\(|select\(|pick\(|omit\()"
)
_SECURITY_LOG_NEARBY = re.compile(
    r"(?i)(login_failed|authentication_failed|auth_failure|failed_login|login_success|logout_event|securityEvent|audit\.(log|info|warn)|event\s*:\s*['\"]login|logger\.(warn|info|error)\(\s*['\"]?(login|auth|authentication))"
)


def _scan_plaintext_sensitive(rule: str, language: str, file_paths: list[str]) -> list[dict]:
    patterns = patterns_for("no-plaintext-sensitive-data-at-rest", language)  # type: ignore[arg-type]
    violations: list[dict] = []
    for file_path in file_paths:
        lines = read_lines(file_path)
        for i, line in enumerate(lines, start=1):
            matched = False
            for pattern, message in patterns:
                if pattern.search(line):
                    matched = True
                    msg = message
                    break
            if not matched:
                continue
            window = "\n".join(lines[max(0, i - 4) : min(len(lines), i + 4)])
            if _ENCRYPT_NEARBY.search(window):
                continue
            violations.append(violation(rule, msg, file_path, i))
    return violations


def _scan_excessive_response(rule: str, language: str, file_paths: list[str]) -> list[dict]:
    patterns = patterns_for("no-excessive-response-data", language)  # type: ignore[arg-type]
    violations: list[dict] = []
    for file_path in file_paths:
        lines = read_lines(file_path)
        for i, line in enumerate(lines, start=1):
            if _DTO_NEARBY.search(line):
                continue
            window = "\n".join(lines[max(0, i - 3) : min(len(lines), i + 3)])
            if _DTO_NEARBY.search(window):
                continue
            for pattern, message in patterns:
                if pattern.search(line):
                    violations.append(violation(rule, message, file_path, i))
                    break
    return violations


def _scan_security_event_logging(rule: str, language: str, file_paths: list[str]) -> list[dict]:
    patterns = patterns_for("no-missing-security-event-logging", language)  # type: ignore[arg-type]
    violations: list[dict] = []
    for file_path in file_paths:
        lines = read_lines(file_path)
        for i, line in enumerate(lines, start=1):
            window = "\n".join(lines[max(0, i - 3) : min(len(lines), i + 20)])
            if _SECURITY_LOG_NEARBY.search(window):
                continue
            for pattern, message in patterns:
                if pattern.search(line):
                    violations.append(violation(rule, message, file_path, i))
                    break
    return violations


def _scan_plaintext_password(rule: str, language: str, file_paths: list[str]) -> list[dict]:
    patterns = patterns_for("no-plaintext-password-storage", language)  # type: ignore[arg-type]
    violations: list[dict] = []
    for file_path in file_paths:
        lines = read_lines(file_path)
        for i, line in enumerate(lines, start=1):
            matched = False
            for pattern, message in patterns:
                if pattern.search(line):
                    matched = True
                    msg = message
                    break
            if not matched:
                continue
            window = "\n".join(lines[max(0, i - 4) : min(len(lines), i + 4)])
            if _HASH_NEARBY.search(window):
                continue
            violations.append(violation(rule, msg, file_path, i))
    return violations


def _scan_unsafe_deser(rule: str, language: str, file_paths: list[str]) -> list[dict]:
    patterns = patterns_for("no-unsafe-deserialization", language)  # type: ignore[arg-type]
    violations: list[dict] = []
    for file_path in file_paths:
        lines = read_lines(file_path)
        for i, line in enumerate(lines, start=1):
            if "SafeLoader" in line or "yaml.safe_load" in line or "SafeConstructor" in line:
                continue
            for pattern, message in patterns:
                if pattern.search(line):
                    violations.append(violation(rule, message, file_path, i))
                    break
    return violations


_RATE_LIMIT_NEARBY = re.compile(
    r"(?i)(rateLimit|rate_limit|limiter|throttle|slowDown|captcha|@Limit|Bucket4j|express-rate-limit)"
)
_LOCK_NEARBY = re.compile(r"(?i)(lock\.|synchronized\s*\(|ReentrantLock|with\s+lock)")


def _scan_login_rate_limit(rule: str, language: str, file_paths: list[str]) -> list[dict]:
    patterns = patterns_for("no-insufficient-login-rate-limiting", language)  # type: ignore[arg-type]
    violations: list[dict] = []
    for file_path in file_paths:
        lines = read_lines(file_path)
        content = "\n".join(lines)
        if _RATE_LIMIT_NEARBY.search(content):
            continue
        for i, line in enumerate(lines, start=1):
            window = "\n".join(lines[max(0, i - 3) : i])
            if _RATE_LIMIT_NEARBY.search(window):
                continue
            for pattern, message in patterns:
                if pattern.search(line):
                    violations.append(violation(rule, message, file_path, i))
                    break
    return violations


def _scan_toctou(rule: str, language: str, file_paths: list[str]) -> list[dict]:
    patterns = patterns_for("no-toctou-outside-lock", language)  # type: ignore[arg-type]
    violations: list[dict] = []
    for file_path in file_paths:
        lines = read_lines(file_path)
        lock_line: int | None = None
        for i, line in enumerate(lines, start=1):
            if _LOCK_NEARBY.search(line) and "unlock" not in line.lower():
                lock_line = i
                break
        for i, line in enumerate(lines, start=1):
            for pattern, message in patterns:
                if not pattern.search(line):
                    continue
                if lock_line is None or i < lock_line:
                    violations.append(violation(rule, message, file_path, i))
                break
    return violations


_SPECIAL = {
    "no-plaintext-password-storage": _scan_plaintext_password,
    "no-plaintext-sensitive-data-at-rest": _scan_plaintext_sensitive,
    "no-excessive-response-data": _scan_excessive_response,
    "no-missing-security-event-logging": _scan_security_event_logging,
    "no-unsafe-deserialization": _scan_unsafe_deser,
    "no-insufficient-login-rate-limiting": _scan_login_rate_limit,
    "no-toctou-outside-lock": _scan_toctou,
}


def run_catalog_scan(
    rule_slug: str,
    language: str,
    rule_name: str,
    file_paths: list[str],
) -> list[dict]:
    handler = _SPECIAL.get(rule_slug)
    if handler:
        return handler(rule_name, language, file_paths)

    patterns = patterns_for(rule_slug, language)  # type: ignore[arg-type]
    violations = scan_files_with_patterns(rule_name, file_paths, patterns)

    if rule_slug in CONTEXT_GATED_RULES:
        gated = context_gated_patterns(rule_slug, language)  # type: ignore[arg-type]
        violations.extend(
            scan_files_with_patterns(
                rule_name, file_paths, gated, require_security_context=True
            )
        )
    return violations
