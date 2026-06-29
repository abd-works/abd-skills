# drawio-domain-sync — Rendered Diagram Example

This file shows a finished rendering of the **Resolution System** Key Abstraction from a fictional domain-specification source. Use it as a reference for the depth and structure a rendered page should reach.

---

## Example: Resolution System page

**Source:** `check-resolution-domain-specification.md`, Key Abstraction `## **Resolution System**`

**Diagram file:** `check-resolution-class-diagram.drawio`, page `Resolution System`

### Classes on this page

```
Rollable           (base abstract, y=40)
Check              (extends Rollable, y=220)
SuccessCheck       (extends Check, y=440)
FailureCheck       (extends Check, y=440)
Degree             (collaborator of Check, y=220, x=500)
DC                 (collaborator of Check, y=220, x=700)
```

### CLI commands used

```bash
# Init page
python scripts/drawio_class_cli.py init check-resolution-class-diagram.drawio \
  --page "Resolution System"

# Add Rollable (abstract base, top of page)
python scripts/drawio_class_cli.py add-class check-resolution-class-diagram.drawio \
  --page "Resolution System" \
  --name Rollable \
  --props "# modifier: Integer" \
  --ops "+ perform_check(roll: Integer, dc: DC): Check" \
  --invs "Invariant: modifier is applied before comparison to DC" \
  --x 200 --y 40

# Add Degree (value object, same row as Check)
python scripts/drawio_class_cli.py add-class check-resolution-class-diagram.drawio \
  --page "Resolution System" \
  --name Degree \
  --props "# label: String" \
  --x 500 --y 220

# Add DC (value object, same row as Check)
python scripts/drawio_class_cli.py add-class check-resolution-class-diagram.drawio \
  --page "Resolution System" \
  --name DC \
  --props "# value: Integer" \
  --x 700 --y 220

# Add Check (extends Rollable)
python scripts/drawio_class_cli.py add-class check-resolution-class-diagram.drawio \
  --page "Resolution System" \
  --name Check \
  --props "+ degree: Degree|+ dc: DC" \
  --ops "+ passed(): Boolean|+ failed(): Boolean" \
  --invs "Invariant: degree is derived from roll vs dc" \
  --x 200 --y 220

# Add SuccessCheck (extends Check, left child)
python scripts/drawio_class_cli.py add-class check-resolution-class-diagram.drawio \
  --page "Resolution System" \
  --name SuccessCheck \
  --ops "+ effectMagnitude(): Integer" \
  --x 60 --y 440

# Add FailureCheck (extends Check, right child)
python scripts/drawio_class_cli.py add-class check-resolution-class-diagram.drawio \
  --page "Resolution System" \
  --name FailureCheck \
  --ops "+ penaltyMagnitude(): Integer" \
  --x 340 --y 440

# Inheritance edges
python scripts/drawio_class_cli.py add-inheritance check-resolution-class-diagram.drawio \
  --page "Resolution System" --child Check --parent Rollable

# SuccessCheck → Check: distinct entry points on Check's bottom edge
python scripts/drawio_class_cli.py add-inheritance check-resolution-class-diagram.drawio \
  --page "Resolution System" --child SuccessCheck --parent Check \
  --entry-x 0.25 --entry-y 1

python scripts/drawio_class_cli.py add-inheritance check-resolution-class-diagram.drawio \
  --page "Resolution System" --child FailureCheck --parent Check \
  --entry-x 0.75 --entry-y 1

# Associations from Check to value collaborators
python scripts/drawio_class_cli.py add-association check-resolution-class-diagram.drawio \
  --page "Resolution System" --from Check --to Degree --exit-x 1 --exit-y 0.3

python scripts/drawio_class_cli.py add-association check-resolution-class-diagram.drawio \
  --page "Resolution System" --from Check --to DC --exit-x 1 --exit-y 0.7

# Inspect for overlaps
python scripts/drawio_class_cli.py inspect check-resolution-class-diagram.drawio \
  --page "Resolution System"

# Verify sync — should report "no changes"
python scripts/drawio_class_cli.py sync-to-model check-resolution-class-diagram.drawio \
  --page "Resolution System" \
  --model check-resolution-domain-specification.md
```

### What this example demonstrates

- `Rollable` at y=40 (base, abstract), `Check` at y=220 (one level below), children at y=440 (two levels down) — **base classes above derived**.
- Two inheritance arrows from `SuccessCheck` and `FailureCheck` both target `Check`'s bottom edge with explicit `entry-x` values (0.25 and 0.75) so the arrows are visually distinct — **distinct anchor points**.
- Two association edges leave `Check`'s right side: one exits at y=0.3, the other at y=0.7 — **distinct anchor points** on the same side.
- No cross-KA imports needed because all classes belong to the Resolution System KA. If `Check` were used on an Attack-and-Damage page, it would be rendered there with `--imported-from "Resolution System"`.
