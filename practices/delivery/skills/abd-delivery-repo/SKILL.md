# delivery-repo

## Purpose

Manage git history for a delivery engagement. Commits, branches, and pushes are driven by the **delivery lead** as part of slot chaining.

---

## Branching strategy

| Scope | Branch name | When to use |
|-------|-------------|-------------|
| Run | `delivery/run-NN` | One branch per delivery run. Default. |
| Slot | `delivery/slot-NN` | When a slot touches a sensitive area needing isolated review. |
| Main | `main` | Only for hotfixes or when the engagement uses trunk-based delivery. |

The delivery lead chooses scope based on the engagement's autonomy setting:
- **tight** → branch per run, PR required before merging
- **delegated** → branch per run, auto-merge on reviewer pass
- **autonomous** → commit directly to main

---

## Tool: `scripts/git_ops.py`

The delivery lead invokes this script to commit and optionally push after a slot finishes.

### Usage

```bash
python scripts/git_ops.py commit --workspace <path> --message "<msg>"
python scripts/git_ops.py branch --workspace <path> --name delivery/run-01
python scripts/git_ops.py push   --workspace <path>
python scripts/git_ops.py status --workspace <path>
```

### When to call it

1. **After writing `slot-NN-finished.md`** — commit all war room and artifact changes.
2. **Before chaining to next slot** — so each slot's work is an atomic commit.
3. **After a reviewer PASS** — push the branch and (if autonomy allows) open a PR or merge.

### Commit message convention

```
slot-NN: <one-line summary from finished.md>

Run: run-NN
Slot type: executor | reviewer
Exit gate: PASS | CONDITIONAL
```

---

## Delivery lead instructions

When finishing a slot:

1. Write `slot-NN-finished.md` with exit gate result.
2. Run:
   ```bash
   python scripts/git_ops.py commit \
     --workspace <workspace-path> \
     --message "slot-NN: <summary>"
   ```
3. If this is the last slot in the run and autonomy ≠ tight:
   ```bash
   python scripts/git_ops.py push --workspace <workspace-path>
   ```
4. Chain to next slot.

---

## Branch lifecycle

```
main
 └─ delivery/run-01        ← created at run start
      ├─ commit: slot-01   ← executor work
      ├─ commit: slot-02   ← reviewer pass
      ├─ commit: slot-03
      └─ PR → main         ← at run checkpoint
```
