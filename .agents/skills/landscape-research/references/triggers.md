# Landscape research — triggers

## 実行する

| シグナル | 例 |
|----------|-----|
| 探索・方針 | 「どう設計すべきか」「選択肢を調べて」 |
| ユーザー明示 | 「Webで検索」「広く調べてから絞って」 |
| アーキテクチャ | memory / agent / reward / evaluation 設計 |
| deliberate 前 | options が空 · 外部ベンチマークが必要 |
| キット整備 | skill 追加 · rule 変更 · 調査ベースの PDCA |
| 前回 scan から時間経過 | 同一 topic で sources > 6mo stale |

## terminology-research を使う（landscape 不可）

| シグナル | 例 |
|----------|-----|
| 用語定義 | 要求/要件/設計/計画の語 |
| record 前 gate | design-record / plan-record 前の alignment |
| 日英混在 PO/Epic/gate | TERMINOLOGY_RESEARCH_POLICY |

## 両方

| 順序 | ケース |
|------|--------|
| landscape → terminology | 方針調査後に残った専門用語を定義 |
| terminology → landscape | 用語は固まったが実装パターン未調査（稀） |

## skip 不可

- ユーザー「調査してから結論」と明示
- design-deliberate で **2+ options** を出すが外部根拠ゼロ

## skip 可

- 正本 `docs/` に十分な調査済み deliberate があり変更なし
- 純実装タスク（P5）で調査不要
