# Modules

A **module** groups Key Abstractions that belong together — because they share a core concern and can be understood as a unit without constantly crossing into other modules. Modules emerge from the KAs, not the other way around.

## How to decide if KAs belong in the same module

Ask: *Can a reader reason about these KAs together as a coherent subject, or do they pull in different directions?*

- KAs that share vocabulary, rules, and invariants → same module.
- KAs that are only loosely related → separate modules.

## Kind-mixing

Ask of each module: *what kind of thing is this module about?* If the answer is more than one kind, split.

## Naming

Pick a single noun the source uses. If you reach for compounds or generic glue, the module likely covers two concerns — split.
