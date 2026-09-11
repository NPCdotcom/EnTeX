---
name: terminology-research
description: Look up requirement and design terms on the web before writing specs. Use when drafting P0-P4 docs to prevent terminology drift.
---

# Terminology Research

**Role**: Cursor 補助（PM）· **P0–P4** · Read + 外部調査

**目的**: 要求・要件・設計・計画の **用語食い違い** を防ぐ。

**探索型調査**は sibling skill **`landscape-research`** — `docs/LANDSCAPE_RESEARCH_POLICY.md`

## いつ実行

P1–P4 で `design-record` / `plan-record` の **前**。P0 charter でも product 用語は 1 回以上。  
トリガー詳細: [`references/search-queries.md`](references/search-queries.md)

## Workflow

1. `docs/project-state.yaml` の `lifecycle_plan.requirements_depth` を読む（空なら `standard`）
2. 用語 3–8 個を列挙（minimal: 2–4 · comprehensive: 6–10）
3. **WebSearch** — 用語ごと最低 1 クエリ、重要語は 2 ソース以上
4. **browser MCP** — 権威 1 ページ以上（`browser_navigate` → `browser_snapshot`）
5. `docs/glossary/` と照合
6. 出力: [`assets/alignment-template.md`](assets/alignment-template.md)
7. **memory-reason** — alignment へルーティング・glossary 昇格候補（G1–G5）

## Cursor ツール

WebSearch → browser MCP → Read glossary。**手動ブラウズ案内のみは禁止**。

## 順序

- spec_designer: **terminology-research** → design-*
- plan_slicer: **terminology-research** → plan-*

正本: `docs/TERMINOLOGY_RESEARCH_POLICY.md` · `cursor-tool-select`

## Do not

検索なし record、訓練データのみの「業界標準」断言、ソースなし引用、P1–P4 skip
