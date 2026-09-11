# Terminology research — 検索クエリとトリガー

## いつ必ず実行するか

| シグナル | 例 |
|----------|-----|
| 要求 / 要件 | 要求定義、要件定義、受入条件、非機能要件 |
| 設計 | 基本設計、詳細設計、外部設計、境界、コンテキスト |
| 計画 | Acceptance criteria、スコープ、DoD、MVP |
| 食い違い | ユーザーとエージェントで用語の意味がずれている |
| 新規 slug / ドメイン語 | 初めて `docs/requirements/` や glossary に載せる語 |
| 日英混在 | PO、Epic、Story、gate、charter 等 |

**skip 不可**: P1–P4 で `design-record` / `plan-record` の **前**。P0 でも product 用語は 1 回以上。

## 検索クエリの型

| 目的 | クエリ例 |
|------|----------|
| 日 SI 工程 | `{用語} システム開発 工程 定義` |
| 要求 vs 要件 | `要求定義 要件定義 違い` |
| 英語圏 | `{term} software engineering definition` |
| フレームワーク | `{term} scrum OR pmi OR ieee` |
| ドメイン | `{product domain} {term} 用語` |

## Cursor ツール優先順

1. **WebSearch** — 2 ソース以上推奨
2. **browser MCP** — 権威ページ 1 件以上（snapshot/screenshot）
3. Read `docs/glossary/` — プロジェクト内定義

OS ブラウザへの「手動で調べてください」だけは **禁止**。
