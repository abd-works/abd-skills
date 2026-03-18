"""Scanner: no nonsense concepts (character names, instruction phrases, typos)."""
import json

from .base import BaseScanner, Violation

# Instruction verbs, connectors, common non-concept phrases, known person/place names
_NONSENSE = frozenset({
    "Choose", "Choose One", "Although", "Because", "While", "Since",
    "Several", "This", "Select", "Select One", "Apply", "Apply One",
    "Smith", "McDonald", "Acme Corp", "Cline", "Jeremiah", "Jon", "Julia",
})


class ConceptSynthesisNoNonsenseScanner(BaseScanner):
    rule_id = "concept_synthesis-no-nonsense"

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return [Violation(rule_id=self.rule_id, message="Invalid JSON", location=str(source_path or ""))]
        concepts = data.get("concepts", {})
        for name in concepts:
            if name in _NONSENSE:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Nonsense concept '{name}' should be removed",
                    location=str(source_path or ""),
                    snippet=name,
                ))
        return violations
