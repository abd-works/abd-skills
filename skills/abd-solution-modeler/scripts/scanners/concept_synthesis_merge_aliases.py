"""Scanner: alias concepts must be merged into canonical per concept_aliases."""
import json
from .base import BaseScanner, Violation


class ConceptSynthesisMergeAliasesScanner(BaseScanner):
    rule_id = "concept_synthesis-merge-aliases"

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return [Violation(rule_id=self.rule_id, message="Invalid JSON", location=str(source_path or ""))]
        concepts = data.get("concepts", {})
        aliases_map = data.get("concept_guidance", {}).get("concept_aliases", {})
        all_aliases = set()
        for canonical, aliases in aliases_map.items():
            for a in aliases:
                all_aliases.add(a)
        for name in concepts:
            if name in all_aliases:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Alias '{name}' should be merged into canonical; remove as separate concept",
                    location=str(source_path or ""),
                    snippet=name,
                ))
        return violations
