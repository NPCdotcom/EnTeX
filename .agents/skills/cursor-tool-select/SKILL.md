---
name: cursor-tool-select
description: Pick the right Cursor tool for the job (WebSearch, browser, Shell). Use when researching terms, checking UI, or running commands.
---

# Cursor Tool Select

**Role**: `router` / PM · **毎ターン**

One intent → one primary tool path.

## Tables

- **選択表**: [`references/selection-table.md`](references/selection-table.md)
- **Role 別 Cursor 補助**: [`references/cursor-role-defaults.md`](references/cursor-role-defaults.md)

## P0–P4 用語（必須）

WebSearch（2+ queries）→ browser MCP（権威 1 ページ）→ `terminology-research` alignment 表

## 探索・方針調査（広→狭）

並列 WebSearch（5–7 軸）→ Cluster → Drill（2–4 hooks）→ **`landscape-research`** report  
正本: `docs/LANDSCAPE_RESEARCH_POLICY.md` · 用語定義は **terminology-research** のまま

## Stop

login/captcha/manual-only → `blocked`、ユーザー takeover。browser MCP 未使用のふりをしない。
