"""Assemble reference-based module partition from source chunk files.

Produces:
  abd-ooad/module-partitioning.md  — root index
  abd-ooad/modules/<name>.md       — per-module reference files
  abd-ooad/modules/rejected.md     — rejected files with reasons
"""
import re
from pathlib import Path

WORKSPACE = Path(r"C:\dev\mm3e-online-holistic")
CHUNKS_DIR = WORKSPACE / "context" / "rules"
OUTPUT_DIR = WORKSPACE / "abd-ooad" / "modules"
ROOT_INDEX = WORKSPACE / "abd-ooad" / "module-partitioning.md"

MODULES = [
    {
        "name": "Check Resolution",
        "filename": "check-resolution.md",
        "chunks": list(range(0, 22)),
        "scope": (
            "The d20 resolution mechanic (roll + modifier vs DC), "
            "checks (routine, opposed, resistance), degrees of success/failure, "
            "measurements and the Rank/Measure table, hero points, extra effort, "
            "power stunts, conditions (basic and combined), and reactions."
        ),
        "terms": [
            "d20", "check", "Difficulty Class (DC)", "opposed check",
            "resistance check", "routine check", "degree of success",
            "degree of failure", "modifier", "rank", "measure",
            "hero point", "extra effort", "power stunt",
            "condition", "combined condition", "dazed", "stunned",
            "staggered", "incapacitated", "dying",
            "vulnerable", "defenseless", "impaired", "disabled",
            "weakened", "exhausted", "fatigued",
            "reaction", "Gamemaster (GM)", "player character (PC)",
            "non-player character (NPC)",
        ],
    },
    {
        "name": "Character Construction",
        "filename": "character-construction.md",
        "chunks": list(range(22, 35)),
        "scope": (
            "Creating heroes from scratch: power level, power point budget, "
            "starting power points, PL-capped limits on trait combinations, "
            "trade-offs, hero archetypes, complications (motivation, enemy, "
            "secret, etc.), background details, and hero advancement/improvement."
        ),
        "terms": [
            "power level", "power points", "starting power points",
            "basic trait costs", "trade-off",
            "attack & effect limit", "Dodge & Toughness limit",
            "Parry & Toughness limit", "Fortitude & Will limit",
            "skill modifier limit",
            "hero archetype", "complication", "motivation",
            "enemy", "secret", "weakness", "power loss",
            "identity", "responsibility", "relationship",
            "hero advancement", "increasing power level",
            "reallocating power points", "origin", "costume",
        ],
    },
    {
        "name": "Ability",
        "filename": "ability.md",
        "chunks": list(range(35, 41)),
        "scope": (
            "The eight ability scores (Strength, Stamina, Agility, Dexterity, "
            "Fighting, Intellect, Awareness, Presence), absent abilities, "
            "debilitated abilities, and derived defense values."
        ),
        "terms": [
            "ability", "ability rank", "absent ability",
            "Strength (STR)", "Stamina (STA)", "Agility (AGL)",
            "Dexterity (DEX)", "Fighting (FGT)", "Intellect (INT)",
            "Awareness (AWE)", "Presence (PRE)",
            "Dodge", "Parry", "Fortitude", "Toughness", "Will",
            "defense", "debilitated",
        ],
    },
    {
        "name": "Skill",
        "filename": "skill.md",
        "chunks": list(range(41, 65)),
        "scope": (
            "Skill basics (ranks, checks, DCs, modifiers, interaction skills, "
            "manipulation skills, skill mastery), and all individual skills."
        ),
        "terms": [
            "skill rank", "skill check", "skill modifier",
            "trained only", "interaction skill", "manipulation skill",
            "Skill Mastery", "circumstance modifier",
            "Acrobatics", "Athletics", "Close Combat", "Deception",
            "Expertise", "Insight", "Intimidation", "Investigation",
            "Perception", "Persuasion", "Ranged Combat",
            "Sleight of Hand", "Stealth", "Technology", "Treatment",
            "Vehicles",
        ],
    },
    {
        "name": "Advantage",
        "filename": "advantage.md",
        "chunks": list(range(65, 82)),
        "scope": (
            "Advantage types: Combat, Fortune, General, and Skill advantages."
        ),
        "terms": [
            "advantage", "advantage rank", "combat advantage",
            "fortune advantage", "general advantage", "skill advantage",
            "Accurate Attack", "All-out Attack", "Defensive Attack",
            "Power Attack", "Improved Initiative", "Improved Critical",
            "Equipment", "Minion", "Sidekick", "Benefit",
            "Luck", "Inspire", "Leadership", "Beginner's Luck",
            "Skill Mastery", "Jack of all Trades",
            "Ranged Attack", "Close Attack",
            "Favored Environment", "Favored Foe",
        ],
    },
    {
        "name": "Power",
        "filename": "power.md",
        "chunks": list(range(82, 158)),
        "scope": (
            "Power effects (Affliction through Weaken), power types, "
            "action/range/duration defaults, Extras, Flaws, Descriptors, "
            "and modifier math."
        ),
        "terms": [
            "effect", "power", "power type", "base cost", "cost per rank",
            "flat modifier", "extra", "flaw",
            "Affliction", "Blast (Damage, Ranged)", "Burrowing",
            "Communication", "Comprehend", "Concealment", "Create",
            "Damage", "Deflect", "Elongation", "Enhanced Trait",
            "Environment", "Feature", "Flight", "Growth", "Healing",
            "Illusion", "Immortality", "Immunity", "Insubstantial",
            "Leaping", "Luck Control", "Mind Reading",
            "Move Object", "Movement", "Nullify", "Protection",
            "Quickness", "Regeneration", "Remote Sensing",
            "Senses", "Shrinking", "Speed", "Summon", "Swimming",
            "Teleport", "Transform", "Variable", "Weaken",
            "Accurate", "Area", "Multiattack", "Penetrating",
            "Activation", "Check Required", "Limited", "Removable",
            "descriptor", "origin descriptor", "source descriptor",
            "Array", "Alternate Effect", "Dynamic Alternate Effect",
        ],
    },
    {
        "name": "Equipment",
        "filename": "equipment.md",
        "chunks": list(range(158, 196)),
        "scope": (
            "Devices vs equipment distinction, the Equipment advantage, "
            "inventing/jury-rigging, general gear, weapons, armor, "
            "vehicles, headquarters, and constructs."
        ),
        "terms": [
            "device", "equipment", "Equipment advantage",
            "Removable", "Easily Removable", "Indestructible",
            "battlesuit", "costume", "enhanced equipment",
            "inventing", "jury-rigging", "ritual",
            "melee weapon", "ranged weapon", "grenade", "explosive",
            "armor", "shield", "Toughness bonus",
            "vehicle", "vehicle size", "vehicle feature",
            "headquarters", "headquarters size", "headquarters feature",
            "construct", "animated object", "robot",
        ],
    },
    {
        "name": "Combat",
        "filename": "combat.md",
        "chunks": list(range(196, 217)),
        "scope": (
            "Initiative and turn order, action types, the attack check sequence, "
            "resistance checks and degrees, combat maneuvers, concealment, "
            "cover, surprise, damage and resistance, recovery, hazards, "
            "minions, team attacks, and damaging objects."
        ),
        "terms": [
            "initiative", "action round", "turn",
            "standard action", "move action", "free action", "reaction",
            "attack check", "attack bonus", "defense class",
            "close attack", "ranged attack", "critical hit",
            "resistance check", "damage", "Toughness resistance",
            "concealment", "cover", "surprise",
            "aim", "charge", "defend", "delay", "disarm",
            "grab", "ready", "recover", "trip", "feint",
            "slam attack", "team attack", "combined attack",
            "minion", "hazard", "falling", "suffocation",
            "damaging objects", "Material Toughness",
            "dying", "incapacitated", "recovery check",
        ],
    },
]

REJECTED_CHUNKS = list(range(217, 244))
REJECTED_EXTRA_FILES = [
    ("HeroesHandbook-statblocks.md", "Character archetype stat blocks — sample pre-built characters, not mechanical rules."),
]
REJECTED_REASONS = {
    range(217, 232): "Ch9 Gamemastering — GM-side adventure design, not mechanical rules needed for automation.",
    range(232, 238): "Supporting Characters — NPC archetype guidance; GM content, not player-facing mechanics.",
    range(238, 239): "Setting: Emerald City — campaign-specific setting material.",
    range(239, 244): "Reference — glossary and summary tables; derivative of rules in other modules.",
}


def read_chunk_metadata(n: int) -> dict | None:
    path = CHUNKS_DIR / f"HeroesHandbook-rules__chunk_{n:03d}.md"
    if not path.is_file():
        return None
    content = path.read_text(encoding="utf-8", errors="replace")
    topic_m = re.search(r'^topic:\s*"(.+?)"', content, re.MULTILINE)
    lr_m = re.search(r'^line_range:\s*"(.+?)"', content, re.MULTILINE)
    return {
        "path": f"context/rules/HeroesHandbook-rules__chunk_{n:03d}.md",
        "topic": topic_m.group(1) if topic_m else f"chunk_{n:03d}",
        "line_range": lr_m.group(1) if lr_m else "?",
    }


def rejected_reason(chunk_num: int) -> str:
    for r, reason in REJECTED_REASONS.items():
        if chunk_num in r:
            return reason
    return "Not required for application mechanics automation."


def write_module_file(mod: dict) -> None:
    lines = [
        f"## Module: [{mod['name']}]\n",
        f"Scope: {mod['scope']}\n",
        "**Core terms**:",
    ]
    for term in mod["terms"]:
        lines.append(f"- {term}")
    lines.append("\n---\n")

    for n in mod["chunks"]:
        meta = read_chunk_metadata(n)
        if meta is None:
            lines.append(f"**Ref — chunk_{n:03d} (FILE NOT FOUND)**\n")
            continue
        lines.append(f"**Ref — {meta['topic']}**")
        lines.append(f"Source: {meta['path']}")
        lines.append(f"Locator: lines {meta['line_range']}")
        lines.append("Extract: whole\n")

    (OUTPUT_DIR / mod["filename"]).write_text("\n".join(lines), encoding="utf-8")


def write_rejected_file() -> None:
    lines = [
        "## [Rejected]\n",
        "**Core terms**: *n/a — Rejected files are intentionally out of scope.*\n",
        "---\n",
    ]

    for n in REJECTED_CHUNKS:
        meta = read_chunk_metadata(n)
        if meta is None:
            lines.append(f"**Ref — chunk_{n:03d} (FILE NOT FOUND)**\n")
            continue
        reason = rejected_reason(n)
        lines.append(f"**Ref — {meta['topic']}**")
        lines.append(f"Source: {meta['path']}")
        lines.append(f"Locator: lines {meta['line_range']}")
        lines.append("Extract: whole")
        lines.append(f"Reason: {reason}\n")

    for filename, reason in REJECTED_EXTRA_FILES:
        lines.append(f"**Ref — {filename}**")
        lines.append(f"Source: context/{filename}")
        lines.append("Locator: whole file")
        lines.append("Extract: whole")
        lines.append(f"Reason: {reason}\n")

    (OUTPUT_DIR / "rejected.md").write_text("\n".join(lines), encoding="utf-8")


def write_root_index() -> None:
    lines = [
        "# Module Partitioning — MM3E Online Holistic\n",
        "Source: context/rules/",
        f"Modules: {len(MODULES)}  Unallocated: 0  Rejected: {len(REJECTED_CHUNKS) + len(REJECTED_EXTRA_FILES)}\n",
        "---\n",
    ]

    for mod in MODULES:
        chunk_min = min(mod["chunks"])
        chunk_max = max(mod["chunks"])
        lines.append(f"## Module: [{mod['name']}]")
        lines.append(f"File: modules/{mod['filename']}")
        lines.append(f"Chunks: {chunk_min:03d}-{chunk_max:03d} ({len(mod['chunks'])} files)")
        lines.append(f"Scope: {mod['scope']}\n")

    lines.append("---\n")
    lines.append("## [Unallocated]")
    lines.append("No unallocated source files.\n")
    lines.append("## [Rejected]")
    lines.append("File: modules/rejected.md")
    lines.append(f"Files: {len(REJECTED_CHUNKS) + len(REJECTED_EXTRA_FILES)}\n")

    ROOT_INDEX.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for mod in MODULES:
        write_module_file(mod)
        print(f"  Written modules/{mod['filename']}")

    write_rejected_file()
    print("  Written modules/rejected.md")

    write_root_index()
    print("  Written module-partitioning.md")

    total = sum(len(m["chunks"]) for m in MODULES) + len(REJECTED_CHUNKS) + len(REJECTED_EXTRA_FILES)
    print(f"\nTotal files allocated: {total}")
    print(f"Modules: {len(MODULES)}")
    print(f"Rejected: {len(REJECTED_CHUNKS) + len(REJECTED_EXTRA_FILES)}")
