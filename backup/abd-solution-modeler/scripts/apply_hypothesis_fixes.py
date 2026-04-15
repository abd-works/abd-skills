#!/usr/bin/env python3
"""Apply hypothesis.json fixes from AI review / hypothesis_deep_scan_analysis.md.

Performs:
- Concept removals (false positives, amalgamations)
- concept_hierarchy updates (subtypes, parents)
- State additions
- Chunk cleanup (remove bad chunk_ids)

Run after AI classification or when applying analysis doc findings.
"""
import json
from pathlib import Path


# --- Fixes from hypothesis_deep_scan_analysis.md ---

# Concepts to remove entirely
REMOVE_CONCEPTS = [
    "Abilities Constructs",  # Amalgamation; chunk merged into Construct
    "Action Looking Glass",  # False positive; chunk doesn't support it
    # Batch 12
    "Either",  # False positive; common word in naming context
    "Element Control",  # False positive; chunk is Deflect/Material Toughness
    "Elemental",  # False positive; chunk is Equipment/High-tech
    # Batch 14
    "Equipment Equipment",  # Amalgamation; duplicate of Equipment
    "Etc.)",  # False positive; truncation
    "Etc.) To Gravity",  # False positive; truncation
    "Even",  # False positive; common word, not domain concept
    # Batch 15
    "Extras Illusion",  # Amalgamation; Extras + Illusion merged
    "Failure",  # False positive; common word
    "Far Worse",  # False positive; flavor text
    # Batch 16
    "Fighting Dis",  # False positive; truncation
    "Fighting Im",  # False positive; truncation
    "Favorable",  # False positive; common word
    "Finally",  # False positive; common word
    # Batch 17
    "Flat",  # False positive; common word
    "Following",  # False positive; common word
    "Four",  # False positive; number
    "Free",  # False positive; common word (Action: Free)
    # Batch 18
    "Freedom City",  # Instance; setting name
    "Freedom League",  # Instance; organization name
    "Frey",  # Instance; character name
    "Gad",  # False positive; truncation
    "Further",  # False positive; common word
    # Batch 19
    "He Grows Explo",  # False positive; truncation
    "Hearing Make",  # False positive; truncation
    "Hekawi",  # Instance; character/setting
    # Batch 20
    "Heroes Who",  # False positive; truncation
    "His",  # False positive; common word
    "However",  # False positive; common word
    "Hqs",  # False positive; truncation
    # Batch 21
    "Human Roll",  # False positive; truncation
    # Batch 23
    "Includ- Ing",  # False positive; truncation
    "Increasing",  # False positive; common word
    "Init",  # False positive; truncation
    # Batch 24
    "Instant Up",  # False positive; truncation
    "Instead",  # False positive; common word
    "Insub",  # False positive; truncation
    "Intel",  # False positive; truncation
    "Intimidation 8",  # Instance; rank value
    "Inventing If",  # False positive; truncation
    # Batch 25
    "Inves- Tigation",  # Amalgamation; merge into Investigation
    "Ited",  # False positive; truncation
    "Its Lead- Er",  # False positive; truncation
    "Jessica",  # Instance; character name
    "Jessica Prentiss",  # Instance; character name
    "Johnny",  # Instance; character name
    "Johnny Goff",  # Instance; character name
    "Johnny Rocket",  # Instance; character name
    "Just",  # False positive; common word
    # Batch 26
    "Key Concept Here",  # False positive; meta
    "Key Difference",  # False positive; meta
    "Kis",  # False positive; truncation
    "Lady Liberty",  # Instance; character name
    "Lamprey",  # Instance; character name
    # Batch 27
    "Life Attractive",  # False positive; truncation
    "Longhunter",  # Instance; character name
    # Batch 28
    "Looked",  # False positive; common word
    "Lookin",  # False positive; truncation
    "Lord Sanguine",  # Instance; character name
    "Luckily",  # False positive; common word
    "M Gamemaster",  # False positive; truncation
    "Mad Maple",  # Instance; character name
    # Batch 29
    "Make",  # False positive; common word
    "Man",  # False positive; common word
    "Maneuver Easy",  # False positive; truncation
    "Many",  # False positive; common word
    "Marguerite",  # Instance; character name
    "Marguerite Frey",  # Instance; character name
    "Marmo",  # False positive; truncation
    # Batch 30
    "Masterminds Game",  # Amalgamation; product name
    "Me",  # False positive; common word
    "Mea",  # False positive; truncation
    # Batches 31-54 (remaining)
    "Oth",  # False positive; truncation
    "Other",  # False positive; common word
    "One Hero",  # False positive; truncation
    "Only Objects",  # False positive; amalgamation
    "Others Immunity",  # Amalgamation
    "Others Variable",  # Amalgamation
    "Outcome In",  # False positive; truncation
    "Owl",  # Instance; archetype form
    "Selec",  # False positive; truncation
    "Sens",  # False positive; truncation
    "See Checks",  # False positive; truncation
    "See Team",  # False positive; truncation
    "Set",  # False positive; common word
    "Set Ii",  # False positive; truncation
    "Seven",  # False positive; number
    "World War Ii",  # Instance; setting
    "Zap",  # Instance; power name
    # Batches 13-52
    "Every",  # False positive; common word
    "Example",  # False positive; meta
    "Get",  # False positive; common word
    "Geography Freedom City",  # Amalgamation; setting + geography
    "Grabbing Or Tripping.",  # False positive; truncation
    "Grad",  # False positive; truncation
    "Grayscale America",  # Instance; setting
    "Hekawi Farmers",  # Instance; character/setting
    "Mind Eidetic Memory",  # Amalgamation
    "Most",  # False positive; common word
    "Most Con",  # False positive; truncation
    "Name",  # False positive; common word
    "Name What",  # False positive; meta
    "National Audu",  # False positive; truncation
    "Ness",  # False positive; truncation
    "New York City",  # Instance; setting
    "Non",  # False positive; common word
    "Note",  # False positive; common word
    "Now",  # False positive; common word
    "Now The Organization",  # Amalgamation
    "Npc",  # Instance; meta
    "Nul",  # False positive; truncation
    "Objects Only",  # False positive; amalgamation
    "Objects Weaken Toughness",  # Amalgamation
    "Odds",  # False positive; common word
    "Once",  # False positive; common word
    "One Example",  # False positive; meta
    "Options",  # False positive; common word
    "Pl10",  # Instance; power level value
    "Potential",  # False positive; common word
    "Professor Salinas",  # Instance; character
    "Professor Victor",  # Instance; character
    "Ranged Dam",  # False positive; truncation
    "Res",  # False positive; truncation
    "Rou",  # False positive; truncation
    "Since Damage",  # False positive; truncation
    "Since Hero Points",  # False positive; truncation
    "Since Rocky",  # False positive; truncation
    "Some",  # False positive; common word
    "Some Adventures",  # Amalgamation
    "Some Afflictions",  # Amalgamation
    "Some Battlesuits",  # Amalgamation
    "Some Gu",  # False positive; truncation
    "Some Immunity Effects",  # Amalgamation
    "So Space Travel",  # False positive; truncation
    "Sound Some",  # False positive; truncation
    "Such",  # False positive; common word
    "Such As Falling",  # False positive; truncation
    "Such.",  # False positive; truncation
    "Summoner Roll",  # Amalgamation
    "Summoner The Summoner",  # Amalgamation
    "Mystic The Mystic",  # Amalgamation
    "Tactics The Sons",  # Amalgamation
    "Take",  # False positive; common word
    "Tals",  # False positive; truncation
    "That Strength",  # Amalgamation
    "Their",  # False positive; common word
    "Theme Maybe",  # Amalgamation
    "Then It",  # False positive; truncation
    "There",  # False positive; common word
    "Therefore Unabl",  # False positive; truncation
    "These",  # False positive; common word
    "This Approach",  # False positive; meta
    "This Minion",  # Amalgamation
    "Though",  # False positive; common word
    "Three",  # False positive; number
    "Three Artifacts",  # Amalgamation
    "Three Ranks",  # Amalgamation
    "Tonight",  # False positive; common word
    "Too Low",  # False positive; truncation
    "Tools Some",  # False positive; truncation
    "Tools Technology",  # Amalgamation
    "Totals",  # False positive; common word
    "Touching",  # False positive; common word
    "Trawler",  # Instance; character/setting
    "Tricking",  # False positive; common word
    "Unless",  # False positive; common word
    "Unfortunately",  # False positive; common word
    "Victor",  # Instance; character
    "Visual Conceal",  # Amalgamation; merge into Visual Concealment
    "Vul- Nerable",  # False positive; truncation
    "Weap",  # False positive; truncation
    "Weather Mistress",  # Instance; character
    "Well",  # False positive; common word
    "West End",  # Instance; setting
    "White Knight",  # Instance; character
    "Windows",  # Instance; setting/product
    "Witchwings",  # Instance; character
    "With",  # False positive; common word
    "Wolfen",  # Instance; character/race
    "Yakuza",  # Instance; organization
]

# Chunk to remove from ALL concepts (Emerald City gamemastering - doesn't support any)
BAD_CHUNK_ID = "d421725a8d2c"

# Concept -> add states
ADD_STATES = {
    "Construct": ["ability_config: no_stamina | no_intellect_presence | no_strength_agility"],
}

# concept_hierarchy: parent -> children to add (only if child concept exists)
HIERARCHY_ADDITIONS = {
    "Complication": [
        "Accident",
        "Addiction",
        "Disability",
        "Enemy",
        "Fame",
        "Hatred",
        "Honor",
        "Identity",
        "Obsession",
        "Phobia",
        "Power Loss",
        "Prejudice",
        "Quirk",
        "Relationship",
        "Reputation",
        "Responsibility",
        "Rivalry",
        "Secret",
        "Temper",
        "Weakness",
    ],
    "Advantage": [
        "Accurate Attack",
        "Power Attack",
        "Luck",
        "Evasion",
        "Favored Environment",
        "Favored Foe",
        "Fearless",
        "Finishing Attack",
        "Improved Critical",
        "Improved Defense",
        "Improved Disarm",
        "Improved Grab",
        "Improved Hold",
        "Improved Initiative",
        "Improved Smash",
        "Improved Trip",
        "Uncanny Dodge",
        "Safe Fall",
        "Quick Draw",
        "Without Defensive Roll",
    ],
    "Enhanced Trait": [
        "Enhanced Stamina",
        "Enhanced Strength",
    ],
    "Extended Sense": [
        "Extended",
        "Extended Vision",
    ],
    "Modifiers": [
        "Impervious",
        "Impervious Protection",
        "Impervious Toughness",
        "Limited",
        "Limited Degree",
        "Linked",
    ],
    "Alternate Effect": ["Dynamic Alternate Effects"],
    "Effect Parameters": ["Duration"],
    "Weaken": ["Weaken Stamina"],
}

# concept_hierarchy: add child to existing parent (e.g. Accurate under Modifiers)
HIERARCHY_ADD_TO_EXISTING = {
    "Modifiers": ["Accurate"],
}

# concept_hierarchy: parent -> children to remove
HIERARCHY_REMOVALS = {
    "Action": ["Action Looking Glass"],
    "Modifiers": ["Extras Illusion"],
}


def apply_fixes(hypothesis: dict) -> list[str]:
    """Apply all fixes. Returns list of change descriptions."""
    changes = []
    concepts = hypothesis.get("concepts", {})
    hierarchy = hypothesis.get("concept_hierarchy", {})

    # 0. Fix action/evidence references to removed concepts
    registries = hypothesis.get("registries") or {}
    actions = registries.get("actions") or {}
    for aid, adata in actions.items():
        if isinstance(adata, dict):
            if adata.get("subject") == "Abilities Constructs":
                adata["subject"] = "Construct"
                changes.append(f"Updated action {aid} subject: Abilities Constructs -> Construct")
            # Clear subject/object for removed concepts
            for name in REMOVE_CONCEPTS:
                if adata.get("subject") == name:
                    adata["subject"] = ""
                    changes.append(f"Cleared action {aid} subject (removed: {name})")
                if adata.get("object") == name:
                    adata["object"] = ""
                    changes.append(f"Cleared action {aid} object (removed: {name})")

    # 1. Remove concepts
    for name in REMOVE_CONCEPTS:
        if name in concepts:
            del concepts[name]
            changes.append(f"Removed concept: {name}")

    # 2. Remove bad chunk from all concepts
    for cname, cdata in list(concepts.items()):
        chunk_ids = cdata.get("chunk_ids") or []
        if BAD_CHUNK_ID in chunk_ids:
            chunk_ids = [cid for cid in chunk_ids if cid != BAD_CHUNK_ID]
            cdata["chunk_ids"] = chunk_ids
            changes.append(f"Removed bad chunk from: {cname}")

    # 3. Add states
    for cname, states in ADD_STATES.items():
        if cname in concepts:
            existing = concepts[cname].get("states") or []
            for s in states:
                if s not in existing:
                    existing.append(s)
            concepts[cname]["states"] = existing
            changes.append(f"Added states to {cname}: {states}")

    # 4. Hierarchy removals
    for parent, to_remove in HIERARCHY_REMOVALS.items():
        if parent in hierarchy:
            children = hierarchy[parent]
            for r in to_remove:
                if r in children:
                    children.remove(r)
                    changes.append(f"Removed {r} from hierarchy under {parent}")

    # 5. Hierarchy additions - new parent entries
    for parent, children in HIERARCHY_ADDITIONS.items():
        # Only add children that exist as concepts
        valid = [c for c in children if c in concepts]
        if not valid:
            continue
        if parent not in hierarchy:
            hierarchy[parent] = []
        existing = set(hierarchy[parent])
        for c in valid:
            if c not in existing:
                hierarchy[parent].append(c)
                existing.add(c)
                changes.append(f"Added {c} under {parent} in hierarchy")

    # 6. Hierarchy additions - add to existing parent
    for parent, to_add in HIERARCHY_ADD_TO_EXISTING.items():
        if parent not in hierarchy:
            hierarchy[parent] = []
        existing = set(hierarchy[parent])
        for c in to_add:
            if c in concepts and c not in existing:
                hierarchy[parent].append(c)
                existing.add(c)
                changes.append(f"Added {c} under {parent} in hierarchy")

    return changes


def main():
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    hypothesis_path = skill_dir / "test" / "mm3" / "solution" / "generated" / "hypothesis.json"

    if not hypothesis_path.exists():
        print(f"hypothesis.json not found: {hypothesis_path}")
        return 1

    hypothesis = json.loads(hypothesis_path.read_text(encoding="utf-8"))
    changes = apply_fixes(hypothesis)

    if not changes:
        print("No changes to apply.")
        return 0

    hypothesis_path.write_text(json.dumps(hypothesis, indent=2), encoding="utf-8")
    print(f"Applied {len(changes)} fixes to {hypothesis_path}:")
    for c in changes:
        print(f"  - {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
