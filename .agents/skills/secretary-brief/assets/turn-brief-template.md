# Turn Brief（Loop1 · 毎ターン）

**Prerequisite**: context-guard · memory-reference Phase 0 · memory-reason（mini/full）

**P/H/gate**: `nav.yaml` の `alignment.*` を **引用** — Loop1 では lifecycle 再推論 **禁止**（Loop2/nav-brief 済みを除く）。

## ユーザー発話（要約）
-

## nav 引用（正本）
| 項目 | 値（nav / project-state） |
|------|---------------------------|
| session_intent | |
| next_actions | |
| phase / H | |
| gate | |
| active_plan | |
| **Cursor mode** | `lifecycle_plan.recommended_cursor_mode`（G1 出力 · 空なら adaptive 提案） |

## トピック T1
| 区分 | 内容 |
|------|------|
| 今ターンの要求 | |
| gate（当ターン） | pass / block |
| 禁止 | Subagent, Hermes, … |

## Role 割当

| 順 | Role | スキル | ペイロード |
|----|------|--------|------------|
| | | | |

（Role 0 = read-only · evaluate **mini**）

## PM 実行
- [ ] role-execute（Role 行）
- [ ] evaluate: full | mini | skip
- [ ] flush → record（**nav.yaml 更新**）

`本ターン: turn-brief 完了 → PM role-execute → memory 書込`
