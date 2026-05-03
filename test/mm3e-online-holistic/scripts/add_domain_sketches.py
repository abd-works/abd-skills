#!/usr/bin/env python3
"""Add domain sketch sections to character-construction.md for the domain-sketch step."""

import re
import sys

INPUT_PATH = r'c:\dev\mm3e-online-holistic\docs\character-construction\character-construction.md'
OUTPUT_PATH = r'c:\dev\mm3e-online-holistic\docs\character-construction\character-construction.md'

# Domain sketch content for each term (keyed by exact term name as it appears in ### heading)
DOMAIN_SKETCHES = {
    'power level': """\
#### Domain Sketch

Sets the series-wide PP budget by formula (PL × 15) before any design choices are made.
Governs hard caps on every paired trait combination: attack/effect, Dodge/Toughness, Parry/Toughness, Fortitude/Will, and skill modifier.
Applies uniformly to all player characters in the same series; the GM cannot vary PL per hero.
Does not constrain NPC traits — derives NPC effective PL retrospectively from the character's highest relevant offensive/defensive pair.
Frames the general scope of what heroes of this series can accomplish on a routine basis.
Invariant: no hero construction is valid without an established PL; the budget, all cap limits, and the skill modifier ceiling all derive from PL being set first.
""",
    'power points': """\
#### Domain Sketch

Serves as the construction currency spent to acquire every trait, tracking each allocation at the applicable Basic Trait Costs rate.
Locks spent PP to the chosen trait after allocation; redistribution requires GM permission or a specific power effect.
Accumulates through GM adventure awards and is spent between sessions to improve hero traits using the same cost formulas as initial construction.
Invariant: a completed hero's total spent PP must equal exactly the starting PP total; any discrepancy is a design error that must be corrected before GM approval.
""",
    'starting power points': """\
#### Domain Sketch

Derives from the GM's chosen PL via the fixed formula PL × 15, producing the exact budget that frames the entire hero design envelope.
Constrains the total resources available for trait allocation; the sum of all trait costs must equal this value exactly.
Permits GM adjustment up or down from the table value when series-specific balance requires it.
Invariant: a completed hero's PP expenditure must equal starting PP; over- or under-spending by even one PP signals an incomplete design.
""",
    'basic trait costs': """\
#### Domain Sketch

Converts design intentions into PP allocations via a fixed price schedule covering every trait category.
Applies fixed rates: abilities at 2 PP/rank, defenses at 1 PP/rank, skills at 1 PP per 2 ranks, advantages at 1 PP/rank or per ranked advantage rank.
Applies a formula-driven rate to powers: ((base effect cost + extras − flaws) × rank) + flat modifiers, with specific rates defined in the Powers chapter.
Provides the accounting reference against which the PP total balance check is validated.
Invariant: trait costs must be computed at the rates defined in the Basic Trait Costs table; no hero-specific pricing deviations are permitted outside power effects.
""",
    'trade-off': """\
#### Domain Sketch

Permits individual paired traits to differ from each other within the constraint that their sum must not exceed 2 × PL.
Enables design diversity: a hero can build a high-skill, lower-damage fighter, a raw-power brute with minimal attack finesse, or any balanced distribution between.
Flags extreme imbalances — a disparity of more than 50% between traits in a pair — as a design concern for close GM scrutiny at approval.
Does not change or relax the hard paired cap; trade-off operates entirely within the fixed ceiling.
""",
    'attack & effect limit': """\
#### Domain Sketch

Enforces that attack bonus + effect rank ≤ 2 × series PL for every attack that requires an attack roll.
Enforces that effect rank alone ≤ PL when an effect allows a resistance check without requiring an attack roll.
Validates each attack/effect pair independently: a hero with multiple attacks checks each combination against the cap separately.
Invariant: no single attack may exceed the 2 × PL ceiling on its combined bonus and effect rank, regardless of trade-off distribution.
""",
    'Dodge & Toughness limit': """\
#### Domain Sketch

Enforces that Dodge (purchased active defense) + Toughness (passive resistance) ≤ 2 × series PL.
Governs the hero's resilience against ranged attacks and area-effect threats.
Shares Toughness with the Parry & Toughness pair: any increase to Toughness simultaneously tightens both defense constraints.
Invariant: the sum of Dodge and Toughness cannot exceed 2 × PL at design time or after any advancement spending.
""",
    'Parry & Toughness limit': """\
#### Domain Sketch

Enforces that Parry (active close-combat defense) + Toughness ≤ 2 × series PL.
Governs close-combat resilience independently from the Dodge pair.
Shares Toughness with the Dodge & Toughness pair: improving Toughness tightens both limit pairs simultaneously.
Invariant: Parry + Toughness ≤ 2 × PL at all times, subject to the same trade-off flexibility as other limit pairs.
""",
    'Fortitude & Will limit': """\
#### Domain Sketch

Enforces that Fortitude + Will ≤ 2 × series PL.
Governs the hero's capacity to resist physical and mental threats that bypass active defense: afflictions, ailments, mental influence.
Operates independently from the combat defense pairs; Fortitude and Will are resistance defenses only, not active defenses.
Invariant: Fortitude + Will ≤ 2 × PL at all times; trade-off applies within this pair just as with defense limit pairs.
""",
    'skill modifier limit': """\
#### Domain Sketch

Enforces that total skill modifier (ability rank + skill rank + advantage modifiers) ≤ PL + 10 for any single skill.
Applies to untrained checks as well — since untrained use relies on ability rank alone, this effectively caps every ability rank as a side effect.
Validates each of the 24 skills independently against the per-skill limit.
Invariant: no constructed skill modifier may exceed PL + 10; this bound constrains all ability rank investments across the hero.
""",
    'complication': """\
#### Domain Sketch

Records a narrative liability that the GM can invoke during play to create genuine trouble for the hero and earn them a hero point.
Requires at minimum a motivation; two or more total complications are strongly recommended.
Can evolve over the course of the series as old conflicts resolve and new ones emerge; the GM may cap the number of active complications a hero holds simultaneously.
Invariant: every hero must have at least one motivation complication; without it, the hero has no hero-point-earning mechanism tied to character drive.
""",
    'motivation': """\
#### Domain Sketch

Defines the primary ethical or personal drive that shapes how the hero approaches their role and resolves moral conflicts in play.
Functions as a required complication that gives the hero a core character dimension the GM can invoke and the player must play through honestly.
Can serve as a power descriptor at GM option, enabling emotion-sensitive powers to detect or affect the hero based on motivation alignment.
Can be the triggering condition for a power loss complication when the motivation wavers or is actively undermined in play.
Invariant: every hero must have exactly one motivation; a hero without a stated motivation is mechanically incomplete and cannot earn hero points through character-drive complications.
""",
    'enemy': """\
#### Domain Sketch

Defines an adversarial figure who actively opposes the hero and whose interference in play generates hero points.
Specifies the adversary's identity and the nature of the enmity — one-sided (adversary targets hero) or mutual (genuine rivalry acknowledged on both sides).
Triggers a hero point only when the GM introduces the enemy in an adventure and the hero suffers specific harm or meaningful hardship as a result.
Can represent individuals, rival heroes, criminal organizations, or government agencies — any persistent adversarial relationship with defined identity and nature.
""",
    'secret': """\
#### Domain Sketch

Defines something potentially damaging or embarrassing that the hero actively conceals from the world.
Most commonly the hero's true identity, but can be a dark past, a hidden weakness, or a morally compromising fact the hero cannot afford to have exposed.
Triggers a hero point only when something or someone actively threatens to reveal the secret — not merely because the secret exists in the background.
Can intersect with the identity complication when the secret being kept IS the dual identity itself.
""",
    'weakness': """\
#### Domain Sketch

Specifies a material, condition, or circumstance that overcomes the hero's normally strong defenses or inflicts unusual harm.
Defines both the triggering substance/condition and the precise mechanical effect: increased damage degrees, affliction, specific power failure, or an alternate effect class.
Requires negotiation with the GM at construction time so both the trigger and its effect are agreed before play begins.
Triggers a hero point when the GM uses the weakness as an active complication during an adventure.
Invariant: both the triggering condition and the mechanical effect must be specified at construction time; a vague weakness without agreed trigger and effect is not a valid complication.
""",
    'power loss': """\
#### Domain Sketch

Defines specific circumstances under which the hero's powers fail entirely: a triggering substance, condition, location, or a direct undermining of the hero's motivation.
Triggers a hero point only when the powers actually fail due to the defined trigger in play — proximity to the trigger alone does not earn the point.
Can be linked to motivation: heroes who derive power from their convictions may suffer power loss when their motivation is genuinely undermined in play.
Requires the trigger to be specific and defined at construction time; overly broad triggers require GM negotiation to avoid making the complication too easily activated.
""",
    'identity': """\
#### Domain Sketch

Defines the hero's approach to their dual existence: maintaining a secret civilian identity separate from the hero persona, or operating fully as a publicly known hero.
Secret identity heroes actively manage two personas, must protect loved ones from knowing the truth, and risk exposure if the two worlds collide.
Public identity heroes face no dual-life management complexity but lose the safety of anonymity; enemies, media, and fans can track their civilian life.
Earns a hero point as a complication when the chosen identity approach creates genuine conflict, exposure risk, or personal cost during an adventure.
""",
    'responsibility': """\
#### Domain Sketch

Defines competing obligations — family duties, professional commitments, civic roles — that legitimately claim the hero's time in conflict with heroic duties.
Creates complication opportunities when the responsibility is visibly neglected, placed at risk, or in direct tension with what the hero must do as a hero.
Triggers a hero point only when the conflict is made manifest in play; the responsibility must actively interfere, not merely exist in the background.
""",
    'relationship': """\
#### Domain Sketch

Defines key people in the hero's life whose safety and knowledge create emotional stakes and potential vulnerability.
Generates different risk profiles depending on whether the person knows the hero's identity: an informed confidant becomes a danger target; an ignorant loved one requires the hero to maintain the deception.
Creates hero-point opportunities when the relationship is directly threatened, exploited, or placed in conflict with heroic duties during an adventure.
""",
    'hero advancement': """\
#### Domain Sketch

Awards PP at the end of adventures: typically 1 PP per completed single-session adventure, up to 2 PP for especially powerful or difficult challenges, and 1 PP per session for multi-session adventures with a possible end-of-arc bonus.
Requires PP to be spent between sessions — not during play — on new or improved traits, using the same cost formulas and PL limits as initial construction.
Allows unspent PP to accumulate so the hero can invest them after a PL increase on traits that were previously at the PL cap ceiling.
Enables the GM to withhold the PP award when the heroes handled an adventure especially poorly.
Invariant: all advancement spending obeys the current series PL limits; no earned PP can raise a trait above the current PL cap.
""",
    'increasing power level': """\
#### Domain Sketch

Triggers when heroes have accumulated approximately 15 additional PP since the series start or the last PL increase — mirroring the 15-PP interval used to set initial budgets.
Raises the series PL by +1, expanding cap headroom on every paired limit simultaneously and unlocking spending on previously-maxed traits.
Requires the GM to reevaluate NPC villain trait levels to maintain appropriate challenge; some adversaries are advanced, others intentionally left behind as the heroes outgrow them.
Enables the introduction of new villains and challenges calibrated to the new PL level.
""",
    'reallocating power points': """\
#### Domain Sketch

Permits already-spent PP to move from one trait to another, changing the hero's trait profile within current PL limits.
Normally prohibited after initial allocation; requires explicit GM permission as a deliberate narrative event, or activation of a specific power effect such as the transformed condition.
Can result in the hero losing traits entirely and gaining wholly new ones — the most radical form of hero transformation.
Should be rare unless the triggering power effect is designed to produce frequent or temporary transformations as part of the hero concept.
""",
    'hero archetype': """\
#### Domain Sketch

Provides a complete, tested PL 10 hero template that a player can adopt unchanged or use as a design starting point.
Offers Options sections where defined, allowing simple variant choices across skills, advantages, or power sets within the archetype's theme.
Can be freely modified beyond any Options section within PP budget, PL caps, and GM approval; the archetype is a starting point, not a constraint.
Marks advantages sourced from Enhanced Advantage power effects with italics to distinguish purchased advantages from power-granted ones.
""",
    'hero concept': """\
#### Domain Sketch

Establishes the creative foundation for the entire design: what type of hero, what powers, what origin, what theme — before any PP is spent.
Guides all subsequent construction steps: PP allocations, power selection, complication choices, and background details all flow from the concept.
Must be shared with the GM before design begins to validate series fit, and ideally with fellow players to ensure team composition makes sense.
Carries no PP cost and no mechanical rule; its role is to make the stat block coherent and the hero a deliberate creation rather than an arbitrary collection of traits.
""",
    'origin': """\
#### Domain Sketch

Establishes how the hero acquired powers and provides the narrative provenance that explains abilities, background, and potential complications.
Supported types: Accident, Alien, Endowment, Experiment, Mutant, and Training — each carrying different narrative implications for the hero's history and world relationships.
Functions as a power descriptor when the GM applies it: a mutant hero can be targeted by mutant-detection powers; a mystic's abilities may be countered by anti-magic effects.
Subject to GM restriction or mandate for the series setting; the GM may ban, require, or limit specific origins for story-consistency reasons.
""",
    'costume': """\
#### Domain Sketch

Provides the hero's distinctive visual identity in their superhero role — the primary external marker distinguishing the hero persona from the civilian persona.
Is immune by comic-book convention to wear from the hero's own powers (a fire controller does not incinerate their costume) — this immunity costs no PP.
Can be damaged or destroyed by external attacks and environmental circumstances, unlike the immunity to power-caused wear.
Serves as the key persona-transition marker for secret-identity heroes: donning or removing it signals the switch between civilian and hero roles.
Mechanical details of costumes treated as equipment (armor values, gadgets) are defined in the Gadgets & Gear module, not this module.
""",
    'background': """\
#### Domain Sketch

Encompasses the narrative details that make a hero a person with history rather than a stat block: name, appearance, age, personality, and goals.
Name selection follows creative conventions (origin-based, power-based, themed, titled, aesthetic, or real name) that signal the hero's style and persona.
Age shapes plausible trait choices: older heroes trend toward higher skill ranks and lower raw physical ability; younger heroes may have emerging raw capability with fewer trained skills.
Goals beyond generic heroism provide story hooks, roleplaying depth, and natural sources for complications and character arcs.
Background details directly inform which complications feel authentic and how the hero navigates the social world.
""",
}


def process_file(content: str) -> str:
    """Add domain sketch sections and update state marker."""
    # Update state marker
    content = content.replace('state: key-abstractions', 'state: domain-sketch', 1)

    lines = content.split('\n')
    result = []
    in_source_block = False
    pending_sketch = None  # domain sketch text waiting to be inserted

    for line in lines:
        stripped = line.strip()

        # Track ```source ... ``` fenced blocks
        if stripped == '```source':
            in_source_block = True
            result.append(line)
            continue
        elif in_source_block and stripped == '```':
            in_source_block = False
            result.append(line)
            continue
        elif in_source_block:
            result.append(line)
            continue

        # Outside source blocks: track current term
        m = re.match(r'^### (.+)$', line)
        if m:
            term_name = m.group(1)
            if term_name in DOMAIN_SKETCHES:
                pending_sketch = DOMAIN_SKETCHES[term_name]

        # Handle top-level --- separator: insert pending domain sketch before it
        if stripped == '---' and pending_sketch is not None:
            result.append('')
            result.append(pending_sketch.rstrip())
            result.append('')
            result.append('---')
            pending_sketch = None
            continue

        result.append(line)

    # Handle edge case: file ends while pending_sketch is set (no trailing ---)
    if pending_sketch is not None:
        result.append('')
        result.append(pending_sketch.rstrip())

    return '\n'.join(result)


def deduplicate_refs_within_ka(content: str) -> str:
    """Within each ## KA block, deduplicate **Ref — title** entries.
    The first term in the KA that cites a ref keeps it; later terms in the same KA
    remove the duplicate Ref block (heading + Source + Locator + Extract + source block).
    """
    lines = content.split('\n')
    result = []
    in_source_block = False
    current_ka_refs = set()      # ref titles seen so far in this KA
    skip_mode = False            # True when we're skipping a duplicate ref block
    skip_depth = 0               # track nesting of skipped source block

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Track source blocks
        if stripped == '```source':
            in_source_block = True
            if skip_mode:
                skip_depth += 1
                i += 1
                continue
            result.append(line)
            i += 1
            continue
        elif in_source_block and stripped == '```':
            in_source_block = False
            if skip_mode:
                skip_depth -= 1
                if skip_depth == 0:
                    skip_mode = False
                i += 1
                continue
            result.append(line)
            i += 1
            continue
        elif in_source_block:
            if not skip_mode:
                result.append(line)
            i += 1
            continue

        # Outside source blocks
        # Reset KA ref tracking when we see a new ## KA heading
        if re.match(r'^## ', line) and not line.startswith('### '):
            current_ka_refs = set()

        # Detect **Ref — title** lines
        ref_match = re.match(r'^\*\*Ref — (.+)\*\*$', line)
        if ref_match:
            ref_title = ref_match.group(1)
            if ref_title in current_ka_refs:
                # This is a duplicate — skip this ref and its source block
                # We need to skip: the **Ref** line, Source:, Locator:, Extract:,
                # optional Part:, empty lines, and the ```source...``` block
                skip_mode = True
                skip_depth = 0
                i += 1
                continue
            else:
                current_ka_refs.add(ref_title)

        # When in skip_mode (but not in source block), skip metadata lines
        if skip_mode:
            # Skip Source:, Locator:, Extract:, Part:, and blank lines until we hit
            # the ```source block or a new non-metadata line
            if (stripped.startswith('Source:') or
                    stripped.startswith('Locator:') or
                    stripped.startswith('Extract:') or
                    stripped.startswith('Part:') or
                    stripped == ''):
                i += 1
                continue
            else:
                # Non-metadata line reached before ```source: stop skipping
                skip_mode = False

        result.append(line)
        i += 1

    return '\n'.join(result)


def main():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Input file: {len(content)} chars, {content.count(chr(10))} lines")

    # Step 1: Add domain sketches
    content = process_file(content)
    print(f"After domain sketches: {len(content)} chars")

    # Step 2: Deduplicate refs within KAs
    content = deduplicate_refs_within_ka(content)
    print(f"After dedup: {len(content)} chars")

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Written to {OUTPUT_PATH}")

    # Count domain sketch sections added
    ds_count = content.count('#### Domain Sketch')
    print(f"Domain Sketch sections: {ds_count}")


if __name__ == '__main__':
    main()
