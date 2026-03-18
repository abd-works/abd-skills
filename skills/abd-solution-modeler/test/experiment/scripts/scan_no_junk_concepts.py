"""Scanner: concept names must be domain nouns, not labels, headers, or garbage.

Rule: no-junk-concepts
Rule file: test/experiment/rules/no-junk-concepts.md

Two-layer junk detection:

  Layer 1 — Universal pattern checks (in this file, domain-agnostic):
    - All-caps strings above a length threshold (section headers)
    - Truncations: ends with hyphen, or <=3 chars all-caps
    - Article+noun fragments: "A X", "An X", "The X"
    - Numeric patterns: "+2 bonus", "DC 10"
    - Single-word instruction verbs from junk_defaults.json

  Layer 2 — Domain config (loaded from junk_config.json next to the input file):
    - section_headers: ToC entries and chapter labels for this corpus
    - proper_nouns: character/setting/org names for this domain
    - additional_junk: anything else the AI flagged

Config loading:
  1. Loads junk_defaults.json from the scanner's own directory (universal)
  2. Looks for junk_config.json alongside the input file (solution-specific)
  Both are merged. If junk_config.json does not exist, runs with defaults only.

This scanner highlights candidates — it does NOT determine if a name is
definitely junk. Borderline names require AI judgment.

Usage (standalone):
    python test/experiment/scripts/scan_no_junk_concepts.py [--input <path>]

Default input: test/experiment/step1-output-v3.json
Exit code 0 = no violations. Exit code 1 = violations found.
"""
import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Violation:
    rule_id: str
    message: str
    location: str
    severity: str = "warning"
    snippet: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "message": self.message,
            "location": self.location,
            "severity": self.severity,
            "snippet": self.snippet,
        }


RULE_ID = "no-junk-concepts"


def _load_defaults(scanner_dir: Path) -> dict:
    defaults_path = scanner_dir / "junk_defaults.json"
    if defaults_path.exists():
        try:
            return json.loads(defaults_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _load_domain_config(input_path: Path) -> dict:
    """Look for junk_config.json in the same directory as the input file."""
    config_path = input_path.parent / "junk_config.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _build_junk_sets(defaults: dict, domain_config: dict) -> tuple[frozenset, frozenset, frozenset, list[re.Pattern]]:
    """Merge defaults and domain config into working sets."""
    section_headers = frozenset(
        s.strip().upper()
        for s in (domain_config.get("section_headers") or [])
        if isinstance(s, str) and s.strip()
    )
    proper_nouns = frozenset(
        s.strip()
        for s in (domain_config.get("proper_nouns") or [])
        if isinstance(s, str) and s.strip()
    )
    additional_junk = frozenset(
        s.strip()
        for s in (domain_config.get("additional_junk") or [])
        if isinstance(s, str) and s.strip()
    )
    instruction_verbs = frozenset(
        s.strip()
        for s in (defaults.get("instruction_verbs") or [])
        if isinstance(s, str) and s.strip()
    )

    # Compile fragment patterns from defaults
    patterns: list[re.Pattern] = []
    for p in (defaults.get("fragment_patterns") or []):
        try:
            patterns.append(re.compile(p))
        except re.error:
            pass

    # Combine all_junk = section_headers + proper_nouns + additional + instruction_verbs
    # (all_junk checked as exact match; proper_nouns and section_headers stored separately for better messages)
    return section_headers, proper_nouns, additional_junk | instruction_verbs, patterns


def _is_all_caps_header(name: str) -> bool:
    """Flag ALL CAPS multi-word names that look like section headers (universal pattern)."""
    stripped = name.strip()
    if stripped == stripped.upper() and len(stripped) > 4 and " " in stripped:
        return True
    return False


def _is_truncation(name: str) -> bool:
    """Flag truncated names (universal pattern)."""
    stripped = name.strip()
    if stripped.endswith("-") or stripped.endswith("—"):
        return True
    # <=3 chars, all-caps alpha — could be a legit abbreviation, flag as candidate
    if len(stripped) <= 3 and stripped.isalpha() and stripped == stripped.upper():
        return True
    return False


def scan(
    data: dict,
    source_path: str = "",
    scanner_dir: Optional[Path] = None,
    input_path: Optional[Path] = None,
) -> list[Violation]:
    violations: list[Violation] = []

    # Load config layers
    defaults = _load_defaults(scanner_dir or Path(__file__).resolve().parent)
    domain_config = _load_domain_config(input_path or Path(source_path)) if (input_path or source_path) else {}
    section_headers, proper_nouns, flat_junk, patterns = _build_junk_sets(defaults, domain_config)

    for pair_idx, pair in enumerate(data.get("modules_and_epics", [])):
        module = pair.get("module", {})
        module_name = module.get("name", f"<unnamed-{pair_idx}>")
        mloc = f"modules_and_epics[{pair_idx}].module['{module_name}']"

        for cidx, concept in enumerate(module.get("concepts", [])):
            cname = concept.get("name", "").strip()
            if not cname:
                continue

            cloc = f"{mloc}.concepts['{cname}']"

            # Layer 2: domain config — section headers
            if cname.upper() in section_headers:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message=f"'{cname}' matches a known section header or document label (junk_config.json)",
                    location=cloc,
                    snippet=cname,
                ))
                continue

            # Layer 2: domain config — proper nouns
            if cname in proper_nouns:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message=f"'{cname}' matches a known proper noun for this domain (junk_config.json)",
                    location=cloc,
                    snippet=cname,
                ))
                continue

            # Layer 2: flat junk (additional_junk + instruction_verbs)
            if cname in flat_junk:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message=f"'{cname}' matches a known junk term (junk_defaults.json or junk_config.json)",
                    location=cloc,
                    snippet=cname,
                ))
                continue

            # Layer 1: universal pattern — all-caps multi-word (not already in domain config)
            if _is_all_caps_header(cname):
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message=f"'{cname}' is all-caps multi-word — likely a section header",
                    location=cloc,
                    snippet=cname,
                ))
                continue

            # Layer 1: universal pattern — truncation
            if _is_truncation(cname):
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message=f"'{cname}' looks like a truncation or fragment",
                    location=cloc,
                    snippet=cname,
                ))
                continue

            # Layer 1: compiled fragment patterns from defaults
            for pattern in patterns:
                if pattern.match(cname):
                    violations.append(Violation(
                        rule_id=RULE_ID,
                        message=f"'{cname}' matches junk pattern '{pattern.pattern}'",
                        location=cloc,
                        snippet=cname,
                    ))
                    break

    return violations


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    experiment_dir = script_dir.parent

    parser = argparse.ArgumentParser(
        description=f"Junk concept name scanner. Rule: {RULE_ID}"
    )
    parser.add_argument(
        "--input",
        default=str(experiment_dir / "step1-output-v3.json"),
        help="Path to step output JSON",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return 1

    # Report which config files are active
    domain_config_path = input_path.parent / "junk_config.json"
    defaults_path = script_dir / "junk_defaults.json"
    print(f"  Config: {defaults_path.name} ({'found' if defaults_path.exists() else 'not found'})")
    print(f"  Config: junk_config.json ({'found at ' + str(domain_config_path) if domain_config_path.exists() else 'not found — running with defaults only'})")

    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {input_path}: {e}")
        return 1

    violations = scan(data, source_path=str(input_path), scanner_dir=script_dir, input_path=input_path)

    if not violations:
        print(f"PASS [{RULE_ID}] — no junk concept names found in {input_path.name}")
        return 0

    print(f"VIOLATIONS [{RULE_ID}] — {len(violations)} candidate(s) in {input_path.name}")
    print(f"  Rule: test/experiment/rules/no-junk-concepts.md")
    print(f"  AI must determine: genuine junk | false positive | rename\n")
    for v in violations:
        print(f"  [{v.severity.upper()}] {v.location}")
        print(f"         {v.message}")
        if v.snippet:
            print(f"         snippet: {v.snippet!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
