# War room work queue — role agents



Delivery **executor** and **reviewer** agents are **persistent by role**. The delivery lead instantiates each role agent **once** at engagement bootstrap; agents **claim** slots from the war room Kanban board.



**Kanban model:** [`../../content/kanban.md`](../../content/kanban.md) · **Board snapshot:** `<workspace>/docs/planning/delivery-war-room/board.json` (synced by delivery lead).



## Kanban columns (one ticket = one column)



| Column | Meaning |

| --- | --- |

| **`backlog`** | Run ticket not on the board yet — **only** place for not-started runs |

| **`in_progress`** | Active **executor** slot on the ticket |

| **`review`** | Active **reviewer** slot on the ticket |

| **`done`** | Stage exit passed — ticket **waits here** until next stage; then → **`in_progress`** (no Ready, no per-stage backlog) |

| **`blocked`** | Open `slot-NN-blocked.md` on the ticket |

| **`stalled`** | Claim open past `stall_timeout_minutes` without finish |



Each **stage** on a ticket cycles: **in_progress → review → done**.



## Role agents (Model B — role pools across all stages)



| Agent | Pulls |

| --- | --- |

| `product-owner` | `team-role: product-owner`, `slot_type: executor` → any stage |

| `product-owner-reviewer` | same role, `slot_type: reviewer` → any stage |

| `business-expert` | executor → any stage |

| `business-expert-reviewer` | reviewer → any stage |

| `ux-designer` | executor → any stage |

| `ux-designer-reviewer` | reviewer → any stage |

| `engineer` | executor → any stage |

| `engineer-reviewer` | reviewer → any stage |



Agents are **not stage-locked**. They claim eligible slots across all stages, prioritising downstream work first. The delivery lead scan loop controls how many concurrent agents of each role are live at any time (per `wip_policy` in `board.json`). Multiple agents of the same role can run simultaneously when `wip_policy` allows it.



Shared workflows: [executor-workflow.md](executor-workflow.md) · [reviewer-workflow.md](reviewer-workflow.md)



## Bootstrap (once per engagement)



Every role agent session receives **only** this bootstrap payload from the delivery lead (or operator):



- **`workspace`** — engagement root (required)

- **`team-role`** — fixed by which agent you are (do not switch)

- **`slot_type`** — `executor` or `reviewer` (fixed by which agent you are)



If `workspace` is missing, ask once and stop.



### Isolation from the delivery lead



You are an **isolated subagent**. Read from disk for every claimed slot:



- **`board.json`** — which run tickets are active and their column

- `slot-NN-start.md` — scope, stage, skills, `depends_on`, corrections

- `manifest.md` — engagement policy

- `docs/corrections-log.md` — when the start file references it



The **start file** is authoritative for slot scope. **`board.json`** is authoritative for ticket column state.



## Claim next slot (pull from board)



After finishing a slot — or on first turn:



1. Read **`board.json`** and `manifest.md`.

2. Find run **tickets** in the column matching your role:

   - **Executor** → tickets with `column: in_progress` (or claimable executor slot when board shows next pull)

   - **Reviewer** → tickets with `column: review`

3. For each candidate ticket, read `active_slot` or resolve the smallest eligible `slot-NN-start.md` matching your `team-role`, `slot_type`, and satisfied `depends_on`.

4. **Exclude** slots with `slot-NN-finished.md`.

5. **Exclude** slots claimed by another agent (`slot-NN-claim.md`).

6. **Pick by downstream-first priority** — work closest to shipping gets priority over work furthest from shipping:

   **Stage priority (highest → lowest):**

   | Priority | Stage |
   | --- | --- |
   | 1 (highest) | `engineering` |
   | 2 | `specification` |
   | 3 | `exploration` |
   | 4 | `discovery` |
   | 5 (lowest) | `shaping` |

   Within the same stage priority: **oldest active run first** (lowest run number), then **smallest slot id**.

   **Rationale:** downstream work unblocks shipping; stalling on engineering while picking up new shaping work wastes throughput. An agent finishing a spec slot should pull the next engineering-eligible slot before opening a new exploration slot.



If nothing qualifies, report **no pending work for this role**.



### Claim marker (avoid double work)



Before starting slot `NN`, write:



```yaml

# slot-NN-claim.md

claimed_by: product-owner

claimed_at: <ISO 8601>

```



Moving the ticket column is done by **work + sync** — executor claim → **`in_progress`**; reviewer claim → **`review`**; stage gate → **`done`**.



Remove `slot-NN-claim.md` when writing `slot-NN-finished.md`. Delivery lead re-runs **`sync_kanban_board.py`** after stage gates.



## Cross-run upstream parallelism



Separate **tickets** can be on the board at once — each in **one** column:



```text

Run 5 ticket:  in_progress  (engineering, slot 116)

Run 6 ticket:  in_progress  (exploration, slot 119)

```



Run N+1 pulls from **`backlog`** when Run N **specification exit** is done — not when Run N engineering finishes. See **`cross-run-upstream-parallelism.md`** and `depends_on` on first exploration slot (prior run spec reviewer, e.g. `"110"`).



## War room autostart



If `INSTRUCTIONS.md` exists:



1. Resolve `workspace`.

2. Read **`board.json`**, `manifest.md`.

3. **Claim** next slot per the algorithm above.

4. Read `slot-NN-start.md` → run executor or reviewer workflow.

5. On finish → `slot-NN-finished.md` → claim again until no eligible work.



## Blocked and stalled



| Signal | File | Ticket column |

| --- | --- | --- |

| **Blocked** | `slot-NN-blocked.md` | `blocked` |

| **Stalled** | claim age > `stall_timeout_minutes` (sync writes column) | `stalled` |



Stop claiming until cleared via `slot-NN-answer.md`. Delivery lead nudges or re-spawns on **stalled**.


