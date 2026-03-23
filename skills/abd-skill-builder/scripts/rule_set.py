"""
RuleSet — loads markdown from rules/*.md and scanners.json.
Ported from abd-story-synthesizer (same shape).
"""
import json
from pathlib import Path


class RuleSet:
    """Unified rule set per skill: markdown + scanner config."""

    def __init__(self, skill_path: Path):
        self.skill_path = Path(skill_path).resolve()
        self.markdown_paths: list[Path] = []
        self.scanner_rules: dict = {}
        self.merged_content: str = ""

    def load(self) -> "RuleSet":
        """Load rules/*.md and rules/scanners.json."""
        rules_dir = self.skill_path / "rules"
        parts: list[str] = []

        scanners_path = rules_dir / "scanners.json"
        if scanners_path.exists():
            self.scanner_rules = json.loads(scanners_path.read_text(encoding="utf-8"))

        for md in sorted(rules_dir.glob("*.md")):
            self.markdown_paths.append(md)
            parts.append(md.read_text(encoding="utf-8").strip())
            parts.append("\n\n---\n\n")

        self.merged_content = "".join(parts).rstrip()
        return self
