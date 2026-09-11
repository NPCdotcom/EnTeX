# Memory record — write scope

Resolve global root: [`../../memory-reference/references/global-paths.md`](../../memory-reference/references/global-paths.md)

Scope routing detail: [`scope-routing.md`](scope-routing.md)

## Allowed paths

| scope | Path | Allowed |
|-------|------|---------|
| project | `.agents/memory/index.yaml` | Yes — add/update `entries` |
| project | `.agents/memory/index/*` | Yes |
| project | `.agents/memory/state/*` | Yes — **nav.yaml every turn** |
| project | `.agents/memory/episodes/*` | Yes |
| project | `.agents/memory/traces/*` | **Append only** |
| project | `.agents/memory/audit/audit-log.md` | **Append only**（AI-DLC audit 相当） |
| project | `.agents/memory/evaluations/*` | Yes — turn eval + critique |
| project | `.agents/memory/rewards/rollup.yaml` | Yes — via memory-refine |
| project | `.agents/memory/knowledge/alignment/*` | Yes |
| project | `.agents/memory/knowledge/lessons/*` | Yes |
| project | `.agents/memory/history/*` | Append only |
| global | `{user_home}/.agents/memory/global/index.yaml` | Yes |
| global | `{user_home}/.agents/memory/global/knowledge/*` | Yes |
| global | `{user_home}/.agents/memory/global/index/*` | Yes |
| team | `docs/project-state.yaml` | Yes — gate/phase（PM 確認後） |
| team | `docs/glossary/` · `docs/adr/` · `docs/design/` | Via **doc-record** / design-record only |
| — | Chat-only memory | **No** — 必ずファイル化 |

## Forbidden

- project **episodes/threads** → global paths
- project **alignment** → global paths
- global **preferences/lessons** → project paths（unless duplicating summary link in project index `linked:`）
- secrets, tokens, credentials
- **traces/** 本文の上書き・削除
- **audit/audit-log.md** の過去エントリの上書き・削除
- critique/trace 無し L2 **lesson** 新規作成

## Index update rules

1. Every new file → index entry with **scope** + **granularity** + **recall**
2. `summary` ≤ 80 chars
3. Project: anchor ≤5, thread ≤3 active (archive old threads)
4. Global: anchor ≤2 active (archive to `granularity: archive`, `recall: on_demand`)
5. Append `project history/YYYY-MM-DD.md` on L2 (project scope only)

## Do not

- 推測を Fact として knowledge に書く（Assumptions と明記）
