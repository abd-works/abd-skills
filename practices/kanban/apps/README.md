# Kanban practice apps

Runnable applications that ship with the kanban practice package. Not deployed to engagement workspaces â€” run from this folder against an engagement's `docs/kanban/` tree.

| App | Purpose |
| --- | --- |
| [abd-delivery-agent-kanban](abd-delivery-agent-kanban/) | Live read-only board UI â€” polls `delivery-kanban-board/board.json` and related planning files |

## Quick start (board UI)

```powershell
cd practices/kanban/apps/abd-delivery-agent-kanban
npm install
npm run dev
```

Open http://localhost:3000/board. Default planning root: `config.default.json` â†’ engagement `docs/kanban/`.

Sync board state first (from engagement root):

```powershell
python .cursor/skills/abd-kanban/scripts/sync_kanban_board.py --workspace <engagement-root>
```
