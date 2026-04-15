"""Scanner: every concept must participate in at least one story.

Rule: domain-interaction-sync
Rule file: rules/domain-interaction-sync.md

Extracts **Concept** refs from epic statement, pre_condition, and story trigger/response.
Flags concepts in module that do not appear in any interaction text.

Usage (standalone):
    python scripts/scanners/domain_interaction_sync.py [--input <path>]

Default input: map-model-spec.json
Exit code 0 = no violations. Exit code 1 = violations found.
"""
import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

CONCEPT_REF = re.compile(r"\*\*([A-Za-z][A-Za-z0-9]*)\*\*")
# Actor names often use **X** — exclude from concept sync check
ACTOR_NAMES = {"Player", "GM", "System", "User", "Actor"}


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


RULE_ID = "domain-interaction-sync"


def _extract_concepts(text: str) -> set[str]:
    """Extract **Concept** names from text (exclude actor names)."""
    if not text:
        return set()
    return set(m.group(1) for m in CONCEPT_REF.finditer(text) if m.group(1) not in ACTOR_NAMES)


def _collect_interaction_texts(epic: dict) -> list[str]:
    """Collect all interaction text from epic (statement, pre_condition, story trigger/response)."""
    texts: list[str] = []
    if epic.get("statement"):
        texts.append(epic["statement"])
    if epic.get("pre_condition"):
        texts.append(epic["pre_condition"])
    for story in epic.get("stories", []):
        if isinstance(story, dict):
            if story.get("trigger"):
                texts.append(story["trigger"])
            if story.get("response"):
                texts.append(story["response"])
            if story.get("pre_condition"):
                texts.append(story["pre_condition"])
    for sub in epic.get("sub_epics", []):
        if isinstance(sub, dict):
            for story in sub.get("stories", []):
                if isinstance(story, dict):
                    if story.get("trigger"):
                        texts.append(story["trigger"])
                    if story.get("response"):
                        texts.append(story["response"])
                    if story.get("pre_condition"):
                        texts.append(story["pre_condition"])
    return texts


def scan(data: dict, source_path: str = "") -> list[Violation]:
    violations: list[Violation] = []

    for pair_idx, pair in enumerate(data.get("modules_and_epics", [])):
        module = pair.get("module", {})
        epic = pair.get("epic", {})
        module_name = module.get("name", f"<unnamed-{pair_idx}>")
        epic_name = epic.get("name", f"<unnamed-epic-{pair_idx}>")
        mloc = f"modules_and_epics[{pair_idx}].module['{module_name}']"

        # All concepts in this module
        concept_names = {c.get("name", "") for c in module.get("concepts", []) if c.get("name")}

        # All **Concept** refs in interaction texts
        interaction_texts = _collect_interaction_texts(epic)
        refd_concepts: set[str] = set()
        for t in interaction_texts:
            refd_concepts.update(_extract_concepts(t))

        # Case-insensitive match for comparison
        refd_lower = {c.lower() for c in refd_concepts}

        for cname in concept_names:
            if not cname:
                continue
            if cname.lower() in refd_lower:
                continue
            # Check if any ref is a partial match (e.g. "Check" vs "SkillCheck")
            if any(cname.lower() in r.lower() or r.lower() in cname.lower() for r in refd_concepts):
                continue
            violations.append(Violation(
                rule_id=RULE_ID,
                message=f"concept '{cname}' in module but not referenced in epic/interactions — synchronize or remove",
                location=f"{mloc}.concepts['{cname}']",
                snippet=cname,
            ))

    return violations


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    scripts_dir = script_dir.parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    try:
        from _config import default_map_model_spec_path

        default_input = str(default_map_model_spec_path())
    except ImportError as e:
        print(f"Error: could not import _config: {e}", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(
        description=f"Domain-story map sync scanner. Rule: {RULE_ID}"
    )
    parser.add_argument(
        "--input",
        default=default_input,
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        alt = Path(default_input)
        if alt.exists():
            input_path = alt
        else:
            print(f"ERROR: Input file not found: {args.input}")
            return 1

    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {input_path}: {e}")
        return 1

    violations = scan(data, source_path=str(input_path))

    if not violations:
        print(f"PASS [{RULE_ID}] — all concepts participate in interactions in {input_path.name}")
        return 0

    print(f"VIOLATIONS [{RULE_ID}] — {len(violations)} orphan concept(s) in {input_path.name}")
    print(f"  Rule: rules/domain-interaction-sync.md\n")
    for v in violations:
        print(f"  [{v.severity.upper()}] {v.location}")
        print(f"         {v.message}")
        if v.snippet:
            print(f"         snippet: {v.snippet!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
