> **DEPRECATED** — Loop2 統合メンテ用。**通常運用は [`turn-brief-template.md`](turn-brief-template.md) + [`nav-brief-template.md`](nav-brief-template.md) のみ。** 本テンプレを Loop1 で使うと P/H 混線の原因になる。

# PM Handoff Brief（Legacy）

## ユーザー発話（原文の要約）
- （箇条書き。推測は「推定」と明記）

## 記憶 recall（memory-reference + reason 要約）
- flush 提案: L1 | L2
- 昇格提案: （glossary / adr / なし）

## トピック別整理

### T1: {短いラベル}
| 区分 | 内容 |
|------|------|
| 明示された要求 | |
| 推定ゴール | |
| 事実 | |
| 仮定 | |
| 未確定 | |
| 工程 P? | |
| スコープ H? | |
| PDCA 位置 | |
| ゲート | pass / block |
| ゲート提案 | Go / Conditional Go / Recycle / Hold / Kill（Gate Keeper = ユーザー） |
| 禁止（このトピック） | 例: plan-record, implement-conduct, Subagent, Hermes |
| エージェントおすすめ（1行） | |

## ライフサイクル（Loop2 · nav-brief へ移行）

**通常**: [`nav-brief-template.md`](nav-brief-template.md) を使用。以下は Legacy メンテ用。

| 項目 | 値 |
|------|-----|
| 現在工程 | P? |
| スコープ焦点 | H? + path |
| 巻き戻し | yes/no + 理由 |
| PM がユーザーに確認 | （ゲート判定） |

## PM 向け — 短期アクション案（優先順）
1. 
2. 
3. 

## Role・スキル割当（必須）

| 実行順 | トピック | Role | スキル（この順） | Cursor 補助 | ペイロード断片 |
|--------|----------|------|------------------|-------------|----------------|
| 1 | T1 | reviewer | review-reference → review-conduct | Shell / browser | （1–2文） |

## PM 実行（必須）

PM は各行を **`role-execute`** で Cursor 内処理。**Subagent / Hermes 禁止。**

## PM 実行チェックリスト

- [ ] memory-reference + memory-reason 済み
- [ ] 上表を実行順に role-execute
- [ ] P0–P4 用語 → terminology-research
- [ ] 探索型 → landscape-research（scan+drill）済み or n/a
- [ ] ターン終端 → action-evaluate → memory-critique → memory-flush (L1) → memory-record → memory-refine（条件付）
- [ ] 運用証跡付き

## ゲート確認（必須1行）

`本ターン: router 完了 → PM は role-execute（Subagent/Hermes なし）→ memory 書込`
