"""Regression tests: secure fixtures stay clean; insecure fixtures trigger rule scanners."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEST_ROOT = Path(__file__).resolve().parent
EXPECTATIONS = json.loads((TEST_ROOT / "scanner_expectations.json").read_text(encoding="utf-8"))
LANGUAGES = EXPECTATIONS["languages"]
SCANNER_GLOB = "no_*_scanner.py"


def _scanner_scripts(language: str) -> list[Path]:
    return sorted((SKILL_ROOT / "scanners" / language).glob(SCANNER_GLOB))


def _run_scanner(scanner: Path, workspace: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(scanner), "--workspace", str(workspace)],
        capture_output=True,
        text=True,
        cwd=str(SKILL_ROOT),
    )


def _stem(scanner: Path) -> str:
    return scanner.stem


@pytest.fixture(params=LANGUAGES, ids=LANGUAGES)
def language(request: pytest.FixtureRequest) -> str:
    return request.param


class TestSecureFixtures:
    def test_all_rule_scanners_pass_with_zero_violations(self, language: str) -> None:
        workspace = TEST_ROOT / "fixtures" / "secure-sample"
        failures: list[str] = []
        for scanner in _scanner_scripts(language):
            result = _run_scanner(scanner, workspace)
            if result.returncode != 0:
                failures.append(
                    f"{scanner.name} exit={result.returncode} stderr={result.stderr.strip()!r}"
                )
        assert not failures, "Secure sample must not trigger violations:\n" + "\n".join(failures)


class TestInsecureFixtures:
    def test_minimum_violation_count(self, language: str) -> None:
        workspace = TEST_ROOT / "fixtures" / "insecure-sample"
        minimum = EXPECTATIONS["fixtures"]["insecure-sample"]["minimum_violations"][language]
        violated = [
            _stem(s)
            for s in _scanner_scripts(language)
            if _run_scanner(s, workspace).returncode != 0
        ]
        assert len(violated) >= minimum, (
            f"Expected at least {minimum} scanners to flag insecure-sample for {language}; "
            f"got {len(violated)}: {violated}"
        )

    def test_must_violate_scanners(self, language: str) -> None:
        workspace = TEST_ROOT / "fixtures" / "insecure-sample"
        required = EXPECTATIONS["fixtures"]["insecure-sample"]["must_violate"][language]
        missing: list[str] = []
        for stem in required:
            scanner = SKILL_ROOT / "scanners" / language / f"{stem}.py"
            assert scanner.is_file(), f"Missing scanner script: {scanner}"
            result = _run_scanner(scanner, workspace)
            if result.returncode == 0:
                missing.append(stem)
        assert not missing, (
            f"Insecure sample must trigger violations for {language}:\n"
            + "\n".join(f"  - {name}" for name in missing)
        )
