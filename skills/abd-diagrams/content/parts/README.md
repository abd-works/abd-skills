# Diagram library (`content/parts/`)

Four markdown files — **edit these**, not the assembled output:

| File | Role |
|------|------|
| `class-diagrams.md` | Class diagram: Draw.io + Markdown sync, Jeff’s collaborator style |
| `class-diagram-layout-rules.md` | Layout, edges, verify codes, XML-style rules for class diagrams |
| `sequence-diagrams.md` | Sequence / walkthrough: dual artifacts, lifelines, messages |
| `sequence-diagram-layout-rules.md` | Sequence layout and connection rules |

**Assemble** into one file for agents or docs:

```bash
python scripts/build_instructions.py
```

Output: **`AGENTS.md`** at the skill root (and `content/built/AGENTS.md`).

The root **`SKILL.md`** holds the full OOAD narrative (steps, ASCII notation, examples). Diagram-specific norms are maintained here so they stay short and reusable.

**Templates** (skill `templates/`): `domain model template.drawio` / `.md` for class structure; `domain realization template.drawio` and `domain walkthrough template.md` for sequence/walkthroughs — always use when creating or updating paired Draw.io + Markdown (see the class/sequence `.md` files above).
