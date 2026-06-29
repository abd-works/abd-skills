# Diagram workflow — abd-architecture-blueprint

Shared commands: [`../../../reference/diagram-workflow.md`](../../../reference/diagram-workflow.md)

**This skill:** four diagrams under `docs/architecture/` — `platform-architecture.drawio`, `module-overview.drawio`, `architecture-flow.drawio`, and `testing-flow.drawio`. All four must exist and verify PASS before the cell is marked done.

```powershell
# 1. Seed — creates all four drawio files
.\scripts\arch-drawio.ps1 init -ProjectRoot <target-project-root>

# 2. Fill platform-architecture.drawio, module-overview.drawio, and architecture-flow.drawio
#    from platform-architecture-elements.md and module subsections (edit seeded files)

# 3. Fill testing-flow.drawio from testing architecture tiers (edit seeded file)

# 4. Export PNGs
.\scripts\arch-drawio.ps1 export -ProjectRoot <target-project-root>

# 5. Verify — must print PASS
.\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
```

Fill seeded `.drawio` files from element-inventory markdown and blueprint module subsections before export.
