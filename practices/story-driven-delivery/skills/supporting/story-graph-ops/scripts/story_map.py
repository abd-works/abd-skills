from __future__ import annotations

import graph_path_bootstrap  # noqa: F401
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from graph_dict_utils import dict_object_list, int_field, optional_text, text_field
from graph_ops_common import read_json_text_file

EMPTY_STORY_GRAPH: Dict[str, Any] = {"epics": [], "increments": []}
_BEHAVIOR_HIERARCHY = ["code", "tests", "scenarios", "exploration"]


class StoryNode:
    def __init__(
        self,
        node_payload: Dict[str, Any],
        epic_idx: int,
        sub_epic_path: Optional[List[int]] = None,
        story_group_idx: Optional[int] = None,
        story_idx: Optional[int] = None,
    ):
        self._payload = node_payload
        self._epic_idx = epic_idx
        self._sub_epic_path = sub_epic_path or []
        self._story_group_idx = story_group_idx
        self._story_idx = story_idx
        self._new_node: Optional[Any] = None

    @property
    def epic_idx(self) -> int:
        return self._epic_idx

    @property
    def sub_epic_path(self) -> List[int]:
        return self._sub_epic_path

    @property
    def story_group_idx(self) -> Optional[int]:
        return self._story_group_idx

    @property
    def story_idx(self) -> Optional[int]:
        return self._story_idx

    @property
    def data(self) -> Dict[str, Any]:
        return self._payload

    @property
    def children(self) -> List["StoryNode"]:
        return []

    @property
    def name(self) -> str:
        return text_field(self._payload, "name")

    def map_location(self, field: str = "name") -> str:
        if isinstance(self, Epic):
            return f"epics[{self.epic_idx}].{field}"
        if isinstance(self, SubEpic):
            if self.sub_epic_path:
                path_str = "".join(f".sub_epics[{idx}]" for idx in self.sub_epic_path)
                return f"epics[{self.epic_idx}]{path_str}.{field}"
            return f"epics[{self.epic_idx}].{field}"
        if isinstance(self, Story):
            path_parts = [f"epics[{self.epic_idx}]"]
            for idx in self.sub_epic_path:
                path_parts.append(f"sub_epics[{idx}]")
            if self.story_group_idx is not None:
                path_parts.append(f"story_groups[{self.story_group_idx}]")
            path_parts.append(f"stories[{self.story_idx}]")
            path_parts.append(field)
            return ".".join(path_parts)
        return ""


class Epic(StoryNode):
    @property
    def children(self) -> List[StoryNode]:
        child_nodes: List[StoryNode] = []
        for sub_epic_idx, sub_epic_payload in enumerate(dict_object_list(self._payload, "sub_epics")):
            child_nodes.append(SubEpic(sub_epic_payload, self.epic_idx, [sub_epic_idx]))
        for story_group_idx, story_group_payload in enumerate(dict_object_list(self._payload, "story_groups")):
            child_nodes.append(StoryGroup(story_group_payload, self.epic_idx, None, story_group_idx))
        return child_nodes

    @property
    def all_stories(self) -> List["Story"]:
        stories: List[Story] = []

        def collect(node: StoryNode) -> None:
            if isinstance(node, Story):
                stories.append(node)
            for child in node.children:
                collect(child)

        collect(self)
        return stories


class SubEpic(StoryNode):
    @property
    def children(self) -> List[StoryNode]:
        child_nodes: List[StoryNode] = []
        for nested_idx, nested_payload in enumerate(dict_object_list(self._payload, "sub_epics")):
            nested_path = self.sub_epic_path + [nested_idx]
            child_nodes.append(SubEpic(nested_payload, self.epic_idx, nested_path))
        for story_group_idx, story_group_payload in enumerate(dict_object_list(self._payload, "story_groups")):
            child_nodes.append(StoryGroup(story_group_payload, self.epic_idx, self.sub_epic_path, story_group_idx))
        return child_nodes


class StoryGroup(StoryNode):
    @property
    def children(self) -> List[StoryNode]:
        return [
            Story(story_payload, self.epic_idx, self.sub_epic_path, self.story_group_idx, story_idx)
            for story_idx, story_payload in enumerate(dict_object_list(self._payload, "stories"))
        ]

    @property
    def behavior_needed(self) -> str:
        priorities: List[int] = []
        for child in self.children:
            behavior = getattr(child, "behavior_needed", None)
            if behavior and behavior in _BEHAVIOR_HIERARCHY:
                priorities.append(_BEHAVIOR_HIERARCHY.index(behavior))
        if not priorities:
            return "exploration"
        return _BEHAVIOR_HIERARCHY[min(priorities)]

    @property
    def behaviors_needed(self) -> List[str]:
        seen: List[str] = []
        for child in self.children:
            child_behaviors = getattr(child, "behaviors_needed", None)
            if child_behaviors is None:
                child_behavior = getattr(child, "behavior_needed", None)
                child_behaviors = [child_behavior] if child_behavior else []
            for behavior in child_behaviors:
                if behavior and behavior not in seen:
                    seen.append(behavior)
        seen.sort(
            key=lambda behavior: _BEHAVIOR_HIERARCHY.index(behavior)
            if behavior in _BEHAVIOR_HIERARCHY
            else len(_BEHAVIOR_HIERARCHY),
        )
        return seen


def _example_table_columns(table: Dict[str, Any]) -> Optional[List[str]]:
    if "columns" in table:
        return table["columns"]
    if "headers" in table:
        return table["headers"]
    return None


class ScenarioExamplesView:
    def __init__(self, scenario_payload: Dict[str, Any]):
        self._payload = scenario_payload

    @property
    def columns(self) -> List[str]:
        for table in self._normalized_tables():
            table_columns = _example_table_columns(table)
            if table_columns:
                return table_columns
        return []

    @property
    def rows(self) -> List[List[str]]:
        for table in self._normalized_tables():
            table_columns = _example_table_columns(table)
            table_rows = table["rows"] if "rows" in table else []
            if table_columns and table_rows:
                return table_rows
        return []

    @property
    def has_any(self) -> bool:
        for table in self._normalized_tables():
            if _example_table_columns(table):
                return True
        return False

    def _normalized_tables(self) -> List[Dict[str, Any]]:
        examples = self._payload["examples"] if "examples" in self._payload else None
        if not examples:
            return []
        if isinstance(examples, dict):
            return [examples]
        if isinstance(examples, list):
            return [table for table in examples if isinstance(table, dict)]
        return []


class ScenarioBase:
    _payload: Dict[str, Any]

    @property
    def steps(self) -> List[str]:
        steps_value = self._payload["steps"] if "steps" in self._payload else ""
        if isinstance(steps_value, str):
            return [step.strip() for step in steps_value.split("\n") if step.strip()]
        return steps_value if isinstance(steps_value, list) else []

    @property
    def all_steps(self) -> List[str]:
        background = self._payload["background"] if "background" in self._payload else []
        return list(background) + self.steps

    @property
    def default_test_method(self) -> str:
        scenario_name = self.name
        if not scenario_name:
            return ""
        words = scenario_name.split()
        method_name = "_".join(word.lower() for word in words)
        return f"test_{method_name}"


class Scenario(ScenarioBase):
    def __init__(self, node_payload: Dict[str, Any], story: "Story", scenario_idx: int):
        self._payload = node_payload
        self._story = story
        self._scenario_idx = scenario_idx

    @property
    def story(self) -> "Story":
        return self._story

    @property
    def scenario_idx(self) -> int:
        return self._scenario_idx

    @property
    def name(self) -> str:
        return text_field(self._payload, "name")

    @property
    def type(self) -> str:
        return text_field(self._payload, "type")

    @property
    def background(self) -> List[str]:
        background = self._payload["background"] if "background" in self._payload else []
        return background if isinstance(background, list) else []

    @property
    def examples(self) -> Optional[Any]:
        return self._payload["examples"] if "examples" in self._payload else None

    @property
    def example_tables(self) -> ScenarioExamplesView:
        return ScenarioExamplesView(self._payload)

    @property
    def test_method(self) -> Optional[str]:
        return optional_text(self._payload, "test_method")

    def map_location(self, field: str = "name") -> str:
        story_location = self.story.map_location("scenarios")
        return f"{story_location}[{self.scenario_idx}].{field}"


class Story(StoryNode):
    @property
    def sizing(self) -> Any:
        return self._payload["sizing"] if "sizing" in self._payload else None

    @property
    def users(self) -> List[str]:
        users = self._payload["users"] if "users" in self._payload else []
        return users if isinstance(users, list) else []

    @property
    def story_type(self) -> str:
        return text_field(self._payload, "story_type")

    @property
    def connector(self) -> Optional[str]:
        return optional_text(self._payload, "connector")

    @property
    def sequential_order(self) -> int:
        return int_field(self._payload, "sequential_order")

    @property
    def scenarios(self) -> List[Scenario]:
        scenario_nodes = [
            Scenario(scenario_payload, self, scenario_idx)
            for scenario_idx, scenario_payload in enumerate(dict_object_list(self._payload, "scenarios"))
        ]
        outlines = dict_object_list(self._payload, "scenario_outlines")
        if outlines:
            offset = len(scenario_nodes)
            for outline_idx, outline_payload in enumerate(outlines):
                scenario_nodes.append(Scenario(outline_payload, self, offset + outline_idx))
        return scenario_nodes

    @property
    def test_class(self) -> Optional[str]:
        return optional_text(self._payload, "test_class")

    @property
    def default_test_class(self) -> str:
        story_name = self.name
        if not story_name:
            return ""
        words = story_name.split()
        class_name = "".join(word.capitalize() for word in words)
        return f"Test{class_name}"

    @property
    def behavior_needed(self) -> str:
        if not self.scenarios:
            return "scenarios"
        return "tests"

    @property
    def behaviors_needed(self) -> List[str]:
        return [self.behavior_needed]


def _story_graph_path_from_bot_paths(bot_paths: Any) -> Path:
    if hasattr(bot_paths, "story_graph_paths"):
        return Path(bot_paths.story_graph_paths.story_graph_path)
    workspace_dir = bot_paths.workspace_directory
    bot_name = bot_paths.bot_directory.name if hasattr(bot_paths, "bot_directory") else "story"
    try:
        from story_graph.story_graph_paths import StoryGraphPaths

        return Path(StoryGraphPaths(workspace_dir, bot_name).story_graph_path)
    except ImportError:
        return Path(workspace_dir) / bot_name / "docs" / "story" / "story-graph.json"


def _resolve_story_graph_path(bot: Any) -> Path:
    if hasattr(bot, "bot_paths"):
        return _story_graph_path_from_bot_paths(bot.bot_paths)
    if isinstance(bot, (str, Path)):
        bot_directory = Path(bot)
        return bot_directory / "docs" / "story" / "story-graph.json"
    raise TypeError(
        "Expected bot with bot_paths.story_graph_paths, bot_paths.workspace_directory, or Path/str, "
        f"got {type(bot)}",
    )


def _load_story_graph_dict_from_path(story_graph_path: Path) -> Dict[str, Any]:
    if not story_graph_path.is_file():
        return EMPTY_STORY_GRAPH.copy()
    parsed = read_json_text_file(story_graph_path)
    return parsed if isinstance(parsed, dict) else EMPTY_STORY_GRAPH.copy()


class StoryMap:
    def __init__(self, story_graph: Dict[str, Any]):
        self._story_graph = story_graph

    @property
    def story_graph(self) -> Dict[str, Any]:
        return self._story_graph

    @classmethod
    def from_json_file(cls, path: Path | str) -> "StoryMap":
        return cls(_load_story_graph_dict_from_path(Path(path)))

    @classmethod
    def from_bot(cls, bot: Any) -> "StoryMap":
        story_graph_path = _resolve_story_graph_path(bot)
        return cls(_load_story_graph_dict_from_path(story_graph_path))

    def epics(self) -> List[Epic]:
        return [
            Epic(epic_payload, epic_idx)
            for epic_idx, epic_payload in enumerate(dict_object_list(self._story_graph, "epics"))
        ]

    def find_epic_by_name(self, epic_name: str) -> Optional[Epic]:
        for epic in self.epics():
            if epic.name == epic_name:
                return epic
        return None

    def walk(self, node: StoryNode) -> Iterator[StoryNode]:
        yield node
        for child in node.children:
            yield from self.walk(child)
