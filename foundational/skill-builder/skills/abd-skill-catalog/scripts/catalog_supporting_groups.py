"""Practice-plugin crosscut rows and foundational plugins below the delivery kanban."""

from __future__ import annotations

# (group_id, label, plugin id for link + family color, skill ids)
SUPPORTING_CROSSCUT_GROUPS: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    (
        "context-driven-delivery",
        "Context-driven delivery",
        "context-driven-delivery",
        (
            "context-driven-delivery",
        ),
    ),
    (
        "kanban",
        "Kanban",
        "kanban",
        (
            "abd-kanban-planning",
            "abd-kanban",
            "abd-kanban-repo",
            "kanban-estimation",
            "abd-kanban-handoff",
        ),
    ),
    (
        "domain-driven-design",
        "Domain-driven design",
        "domain-driven-design",
        (
            "abd-bounded-context-map",
            "abd-ddd-design-building-blocks",
            "abd-domain-walk",
            "drawio-domain-sync",
        ),
    ),
    (
        "story-driven-delivery",
        "Story-driven delivery",
        "story-driven-delivery",
        (
            "abd-thin-slicing",
            "story-graph-ops",
            "drawio-story-sync",
            "miro-story-sync",
        ),
    ),
)

FOUNDATIONAL_CROSSCUT_PLUGINS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (
        "context-to-memory",
        "Context to memory",
        (
            "abd-convert-to-markdown",
            "abd-chunk-markdown",
            "abd-embed-vectors",
            "abd-search-memory",
            "abd-semantic-context-chunker",
        ),
    ),
    (
        "skill-builder",
        "Skill builder",
        (
            "abd-query-practice-sources",
            "abd-author-practice-skill",
            "abd-build-practice-scanners",
            "abd-skill-catalog",
            "abd-practice-skill-manual",
        ),
    ),
    (
        "skill-helpers",
        "Helpers",
        (
            "commit-msg",
            "execute-skill-using-skills-rules",
            "track_task",
        ),
    ),
)

SUPPORTING_SKILL_GROUP_LABEL: dict[str, str] = {
    group_id: label for group_id, label, _plugin, _skills in SUPPORTING_CROSSCUT_GROUPS
}

SKILL_TO_SUPPORTING_GROUP: dict[str, str] = {}
for group_id, _label, _plugin, skill_ids in SUPPORTING_CROSSCUT_GROUPS:
    for skill_id in skill_ids:
        SKILL_TO_SUPPORTING_GROUP[skill_id] = group_id
