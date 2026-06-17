# ddd-building-blocks fidelity upgrade

When the domain model for a module advances in fidelity (e.g. ubiquitous language → CRC, CRC → object model) **and** a `*-ddd-building-blocks.md` file already exists for that module at the prior fidelity:

Ask the user: *"The domain model has advanced to [new level]. Would you like to update the DDD building blocks to match?"*

If yes, rewrite the building-blocks document at the new fidelity — carrying forward all stereotype decisions, identity rules, aggregate boundaries, and cross-aggregate consistency policies, now expressed in the richer notation.
