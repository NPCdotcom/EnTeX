# Landscape research policy（広→狭 Web 調査）

**探索型の問い**（アーキテクチャ・方針・「何をすべきか」・キット設計）では、**広く浅く網羅 → 搾り込み → 結論** の2段調査を省略しない。

用語・定義の正本調査は **`terminology-research`**（狭く深い）。本ポリシーは **landscape-research**（広→狭）用。

**AI-DLC 対応**: 本 skill は AI-DLC **Inception 調査**（Workspace Detection · brownfield 探索 · Workflow Planning 入力）のキット翻訳。成果物は `docs/` 正本へ写像し、`aidlc-docs/` 丸コピーはしない（`s-01` · `a-06`）。

**question-driven 連携**: landscape 完了後、用語は **terminology-research** · 曖昧点は **verification-questions**（`TERMINOLOGY_RESEARCH_POLICY.md`）→ Gate → deliberate/record。

## 2 skill の使い分け

| | `terminology-research` | `landscape-research` |
|---|------------------------|----------------------|
| **目的** | 用語 alignment · 権威定義 | 調査地図 · 選択肢 · 設計根拠 |
| **深さ** | 用語ごとに深い · 権威1ページ以上 | 第1波は浅い · 第2波で2–4点だけ深掘り |
| **クエリ** | `{用語} 定義` 型 | 5–7軸 × 並列 broad query |
| **出力** | alignment 表 → glossary | scan map → drill → landscape report |
| **典型** | P0–P4 record 前 | design-deliberate 前 · ユーザー「調査して」 |
| **記憶** | project alignment · **learning `notes/`**（学習モード）· global `lessons/` + trace |

## 必須タイミング

| シグナル | Skill |
|----------|-------|
| アーキテクチャ / 方針 / 比較検討 | **landscape-research** |
| ユーザー明示「Webで調べて」「検索して」 | **landscape-research** |
| design-deliberate で options 前（探索型） | **landscape-research** → deliberate |
| kit_maintainer · キット設計 | **landscape-research** |
| brownfield 初回 · **既存コード**把握 | **`brownfield-reference`**（RE テンプレ · o-05） |
| brownfield · **業界/規制**の外部調査 | **landscape-research**（コード外のみ · a-06） |
| adaptive-lifecycle-plan 前の探索 | **landscape-research**（任意 · 複雑度高時） |
| 要求/要件/設計/計画の **用語** | **terminology-research**（従来通り） |

## 6 フェーズ（正本）

```
Frame  → 問いを 5–7 独立軸に分解
Scan   → 各軸 1 クエリ · 浅く · 並列 WebSearch（答えを書かず地図を書く）
Cluster→ 重複 · 対立 · 空白 · 「引っかかった 2–4 点」
Drill  → Cluster から選んだ点だけ第2波検索（深い）
Map    → キット写像（skill / memory / docs / 禁止事項）
Critique→ 反証 · リスク · 未検証 Assumption
```

## Gate

- 探索型 deliberate / 設計 record **前**に landscape report 無し → **Conditional Go**（調査不足）
- 第1波のみで結論 → **Recycle**
- ソース無し generalization → **Recycle**

## 記憶・評価

- Scan/Drill 中: brief + episode にフックのみ
- 完了: **memory-reason** → global `lessons/`（横断）または project `lessons/`（repo 固有）
- trace: `.agents/memory/traces/` または landscape report 内 `provenance`
- 運用証跡: `調査: landscape-research | scan:N drill:M | done/skipped`

## Cursor 料金（c-10 · 任意）

frontier モデルを手動選択した WebSearch/browser は **credit 消費**が大きい。可能なら **Auto mode** を優先し、drill は hooks 2–4 点に限定する。

## Skill / Rule / Doc

- Skill: **`landscape-research`**
- 連携: **`terminology-research`** · **`adaptive-lifecycle-plan`** · **`design-deliberate`** · **`memory-reason`**
- Rule: `cursor-tool-select` · `design-stewardship` · `secretary-gate`
- 正本: `docs/TERMINOLOGY_RESEARCH_POLICY.md` · `docs/AGENT_EVALUATION.md`
