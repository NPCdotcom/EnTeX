# PM Handoffs（Legacy · 廃止）

**廃止**: 2026-06-17 — **新規作成禁止**

| 代替 | Skill |
|------|-------|
| `.agents/memory/episodes/` | secretary-record, memory-record |
| `.agents/memory/state/nav.yaml` | memory-record（毎ターン） |
| turn-brief + nav-brief | secretary-brief |

既存ファイルは index 経由で読取のみ可。新規 brief は **episodes** へ。
