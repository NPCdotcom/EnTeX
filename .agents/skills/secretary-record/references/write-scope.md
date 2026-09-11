# Secretary record — write scope

| Path | Allowed |
|------|---------|
| `.agents/memory/episodes/*.md` | **Yes（正本）** |
| `.agents/memory/index.yaml` | Via **memory-record** |
| `.agents/handoffs/*.md` | **読取のみ · 新規禁止**（2026-06-17 廃止 → episodes） |
| Other paths | **No** |

## Workflow

1. Copy PM Handoff Brief body
2. **memory-record** — index entry `tier: episodes`, `recall: next_turn`
3. Optional history append

Do not store secrets. Link docs/plans by path only.
