# Diagram workflow — abd-architecture-outline

Shared commands: [`../../../reference/diagram-workflow.md`](../../../reference/diagram-workflow.md)

**This skill:** `docs/architecture/diagrams/system-context.drawio` — must exist and verify PASS before the cell is marked done.

```powershell
# 1. Seed — creates system-context.drawio under docs/architecture/diagrams/
.\scripts\arch-drawio.ps1 init -ProjectRoot <target-project-root>

# 2. Fill system-context.drawio with real names from system-context-elements.md (edit the seeded file)

# 3. Export PNG
.\scripts\arch-drawio.ps1 export -ProjectRoot <target-project-root>

# 4. Verify — must print PASS
.\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
```

Fill the seeded `.drawio` from `system-context-elements.md` (written first in generate step 2a) before export.
