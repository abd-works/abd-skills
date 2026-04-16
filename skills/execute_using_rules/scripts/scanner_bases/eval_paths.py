from pathlib import Path
from typing import Optional, List


class EvalPaths:
    """Centralized path resolver for eval scanners.

    Resolves workspace root, behavior directory, guardrails,
    clarification/strategy files, instruction sources, and
    baseline paths from a single anchor (the rule file path).
    Change path logic here and every scanner picks it up.
    """

    def __init__(self, rule_file_path: Path):
        self._rule_path = Path(rule_file_path)
        self._behavior_dir: Optional[Path] = None
        self._workspace_root: Optional[Path] = None

    @property
    def behavior_dir(self) -> Optional[Path]:
        if self._behavior_dir is None:
            self._behavior_dir = self._resolve_behavior_dir()
        return self._behavior_dir

    @property
    def behavior_name(self) -> Optional[str]:
        bd = self.behavior_dir
        return bd.name if bd else None

    @property
    def workspace_root(self) -> Optional[Path]:
        if self._workspace_root is None:
            self._workspace_root = self._resolve_workspace_root()
        return self._workspace_root

    @property
    def guardrails_dir(self) -> Optional[Path]:
        bd = self.behavior_dir
        if not bd:
            return None
        p = bd / 'guardrails'
        return p if p.is_dir() else None

    @property
    def key_questions_path(self) -> Optional[Path]:
        gd = self.guardrails_dir
        if not gd:
            return None
        p = gd / 'required_context' / 'key_questions.json'
        return p if p.exists() else None

    @property
    def decision_criteria_dir(self) -> Optional[Path]:
        gd = self.guardrails_dir
        if not gd:
            return None
        p = gd / 'strategy' / 'decision_criteria'
        return p if p.is_dir() else None

    @property
    def clarification_path(self) -> Optional[Path]:
        ws = self.workspace_root
        if not ws:
            return None
        p = ws / 'docs' / 'story' / 'clarification.json'
        return p if p.exists() else None

    @property
    def strategy_path(self) -> Optional[Path]:
        ws = self.workspace_root
        if not ws:
            return None
        p = ws / 'docs' / 'story' / 'strategy.json'
        return p if p.exists() else None

    @property
    def baseline_path(self) -> Path:
        ws = self.workspace_root
        root = ws if ws else self._rule_path.parent
        return root / 'eval' / 'baseline_violations.json'

    @property
    def rules_dir(self) -> Optional[Path]:
        bd = self.behavior_dir
        if not bd:
            return None
        p = bd / 'rules'
        return p if p.is_dir() else None

    @property
    def behavior_json_path(self) -> Optional[Path]:
        bd = self.behavior_dir
        if not bd:
            return None
        p = bd / 'behavior.json'
        return p if p.exists() else None

    @property
    def bot_config_path(self) -> Optional[Path]:
        """bots/{bot}/bot_config.json -- two levels up from behavior dir."""
        bd = self.behavior_dir
        if not bd:
            return None
        bot_dir = bd.parent.parent
        p = bot_dir / 'bot_config.json'
        return p if p.exists() else None

    @property
    def bot_dir(self) -> Optional[Path]:
        bd = self.behavior_dir
        if not bd:
            return None
        return bd.parent.parent

    @property
    def base_actions_dir(self) -> Optional[Path]:
        ws = self.workspace_root
        if not ws:
            return None
        p = ws / 'base_actions'
        return p if p.is_dir() else None

    def action_config_path(self, action_name: str) -> Optional[Path]:
        ba = self.base_actions_dir
        if not ba:
            return None
        p = ba / action_name / 'action_config.json'
        return p if p.exists() else None

    def action_names_from_behavior(self) -> List[str]:
        """Read action names from behavior.json actions_workflow."""
        import json
        bp = self.behavior_json_path
        if not bp:
            return []
        try:
            with open(bp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            actions = data.get('actions_workflow', {}).get('actions', [])
            return [a.get('type', '') for a in actions if a.get('type')]
        except (json.JSONDecodeError, IOError):
            return []

    def _resolve_behavior_dir(self) -> Optional[Path]:
        """Rule lives at behaviors/<name>/rules/<file>.json -> parent.parent."""
        if not self._rule_path:
            return None
        candidate = self._rule_path.parent.parent
        if candidate.parent.name == 'behaviors':
            return candidate
        return candidate

    def _resolve_workspace_root(self) -> Optional[Path]:
        """Walk up from behavior dir looking for docs/story/."""
        start = self.behavior_dir or self._rule_path.parent
        current = start
        for _ in range(10):
            current = current.parent
            if (current / 'docs' / 'story').is_dir():
                return current
            if current == current.parent:
                break
        return None
