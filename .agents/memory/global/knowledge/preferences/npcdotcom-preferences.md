---
id: npcdotcom-preferences
kind: knowledge
topic: preferences
owner: NPCdotcom
status: active
promoted_from: learning/npcdotcom
promoted_at: 2026-06-18
updated: 2026-06-18
core_synced_at: 2026-06-18
tags: [npcdotcom, preferences, communication, research]
---

# NPCdotcom — 開発・調査プリファレンス

## 言語 · コミュニケーション

- 応答は **日本語**
- 説明は技術ブログ調 · 簡潔だが完全な文

## ドメイン

- **ゲームプログラミング**が中心。特に **シミュレーションゲーム**
- 動機: **現実世界への無限近似**（核心 E-15）
- 商用エンジン丸投げより **自前基盤**；**C++/CUDA/Vulkan 低レイヤー自前は許容**（核心に最も近い実装層）
- Project6A 等は **打ち切り済み・核心に最も近い一例** — デフォルト前提にしない

## 調査ワークフロー

1. **広く浅く** — 関連キーワードを限界まで網羅
2. **突飛なクエリ・多パターン** — 固定観念打破；**意外性**重視
3. **2–4 点だけ深掘り** — 権威ソース + browser/WebSearch
4. 結果は external memory に残す

Skills: `landscape-research` · `terminology-research`

## 思考・協働（E-13 確定）

| 項目 | 内容 |
|------|------|
| 駆動 | **イメージ** + 設計思想が基盤 |
| エージェント役 | イメージの発展、抜けの穴埋めアイデア |
| ユーザー役 | イメージ伝達、アイデアの **取捨選択** |
| 曖昧さ | エージェントが **理解させる** ことで回避 |
| ズレ | 思想違反 · 手順飛ばし · 用語/イメージ食い違い |
| 推敲 | **コメント（`>`）→ 対話** |
| 理解型 | **理屈・理論**（公式暗記型ではない） |
| 実装入り | アーキ **完璧に詰めてから** 最小単位積み上げ |
| 安心条件 | アーキ **全体像** の把握 |

詳細: `learning/npcdotcom/notes/thinking-process.md`

## エージェント設計判断

- レジストリ + OCP を優先して提案する
- 新機能は「どの登録種として足すか」から説明する
- 特定プロジェクト（Project6A 等）の手順を **デフォルト前提にしない**

## Related index ids

- npcdotcom-philosophy
