# Audit log（append-only）

**Tier**: `audit` · **scope**: project  
**AI-DLC 相当**: `aidlc-docs/audit.md`

単一正本: **`audit-log.md`** — **追記のみ**（上書き・削除禁止）。

## 形式

各エントリは skill `memory-record` · [`assets/audit/audit-entry-template.md`](../../skills/memory-record/assets/audit/audit-entry-template.md) に従う。

## 記録タイミング

| イベント | 発火 |
|----------|------|
| `lifecycle_plan` Go | adaptive-lifecycle-plan 後 |
| Gate 決定 | `project-state.yaml` gate_status 更新時 |
| 質問ファイル承認 | verification-questions Approval 時 |
| Phase 遷移 | `current_phase` 変更時 |
| L2 flush | trace id を参照して要約行（任意） |

## Bootstrap

```bash
cp .agents/memory/audit/audit-log.md.example .agents/memory/audit/audit-log.md
```

初回エントリ前でも空のヘッダのみで可。

## Git

`audit/` は **commit しない**（project memory と同様）。

正本: `docs/MEMORY_ARCHITECTURE.md` · skill `memory-record`
