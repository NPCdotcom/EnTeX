# Cursor tool selection table

| User intent (signals) | Primary | Secondary | Never as first answer |
|----------------------|---------|-----------|------------------------|
| **探索・方針・アーキテクチャ調査** | **landscape-research**（並列 WebSearch scan → drill） | browser MCP（drill 時） | 1 クエリで結論 / 訓練データのみ |
| **用語・定義・工程の確認**（要求/要件/設計/計画） | **WebSearch**（2+ queries） | **browser MCP**（権威 1 ページ） | 訓練データのみで定義 / 手動ブラウズ案内 |
| 要求定義・要件定義・受入条件・非機能 | **WebSearch** + terminology-research | browser MCP（日本 SI / PMI 等） | Read/Grep のみ |
| P0–P4 spec / plan 執筆前 | **WebSearch** 必須 | browser MCP 推奨 | design-record / plan-record 直行 |
| 画面確認・スクショ・UI テスト | cursor-ide-browser | Shell (start server) | OS ブラウザのみ案内 |
| localhost / デプロイ URL 検証 | browser_navigate(url) | Shell curl (structure only) | 手動ブラウズのみ |
| ビルド・テスト・git | Shell | Read output / Await | 「自分で実行して」 |
| ログ調査（実行済み） | Read terminals log | Shell tail | — |
| Linear issue / 状態更新 | CallMcpTool linear | — | 未確認で不可 |
| ファイルを IDE に見せる | open_resource | — | エージェントが Read で足りる |
| Cursor Automation 作成 | cursor-backend-control + open_automation | — | GitHub Actions と混同 |
| コード探索 | Grep / Glob / SemanticSearch | — | **Subagent** / Task explore |

## WebSearch + browser（用語 · P0–P4 必須）

```
WebSearch: "{用語} 定義 システム開発" (+ 英語 query if needed)
→ WebSearch: 2nd source (PMI / Atlassian / 日本 SI)
→ browser_navigate(authoritative URL)
→ browser_snapshot or browser_take_screenshot
→ Terminology alignment 表（terminology-research/assets/alignment-template.md）
```

## Landscape scan + drill（探索型）

```
Frame: 5–7 axes
→ WebSearch × N parallel (broad, shallow — 地図のみ)
→ Cluster: overlap / tension / gaps / 2–4 drill hooks
→ WebSearch × 2–4 (deep on hooks) [+ browser 1–2 pages]
→ landscape-research/assets/outputs/landscape-report-template.md
→ memory-reason (global/project lesson)
```

## Browser mini-flow（UI・スクショ）

```
browser_tabs → browser_navigate → browser_lock(lock)
→ browser_take_screenshot
→ browser_lock(unlock)
```

## Dev server + browser

```
Shell: start server (background if long)
→ Await or poll
→ browser_navigate(http://localhost:PORT)
→ browser_take_screenshot
```
