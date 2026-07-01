"""Throwaway: strip acceptance_criteria + scenarios from every story.

Produces a story-map-only view of a story-graph.json:
- Keeps: epics, sub_epics, story_groups, stories (with their name + actor)
- Drops: acceptance_criteria[], scenarios[]
"""
import json
import sys


def strip(node: dict) -> None:
    for g in node.get("story_groups", []) or []:
        for s in g.get("stories", []) or []:
            s.pop("acceptance_criteria", None)
            s.pop("scenarios", None)
    for s in node.get("sub_epics", []) or []:
        strip(s)


src = json.load(open(sys.argv[1], encoding="utf-8"))
for e in src.get("epics", []):
    strip(e)

# Drop increments too (thin-slicing is a later stage; we're at story map)
src["increments"] = []

json.dump(src, open(sys.argv[2], "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"Wrote story-map-only JSON: {sys.argv[2]}")
