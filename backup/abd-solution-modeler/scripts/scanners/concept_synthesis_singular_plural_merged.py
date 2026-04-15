"""Scanner: singular/plural variants should be merged."""
import json
from .base import BaseScanner, Violation


def _singular(s: str) -> str:
    if not s or len(s) < 2:
        return s
    if s.endswith("ies"):
        return s[:-3] + "y"
    if s.endswith("es") and s[-3] in "sxzch":
        return s[:-2]
    if s.endswith("s") and not s.endswith("ss"):
        return s[:-1]
    return s


class ConceptSynthesisSingularPluralMergedScanner(BaseScanner):
    rule_id = "concept_synthesis-singular-plural-merged"

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return [Violation(rule_id=self.rule_id, message="Invalid JSON", location=str(source_path or ""))]
        concepts = list(data.get("concepts", {}).keys())
        seen_singular: dict[str, str] = {}
        for name in concepts:
            sing = _singular(name)
            if sing != name:
                if sing in concepts:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Merge '{name}' and '{sing}' into one canonical",
                        location=str(source_path or ""),
                        snippet=f"{name} / {sing}",
                    ))
            else:
                plural_candidates = [c for c in concepts if _singular(c) == name and c != name]
                if plural_candidates:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Merge '{name}' and {plural_candidates} into one canonical",
                        location=str(source_path or ""),
                        snippet=f"{name} / {plural_candidates}",
                    ))
        return violations
