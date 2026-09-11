# Cursor Agent Tooling Reference（汎用）

Cursor role・PM が **見落としやすい Cursor 補助機能** の正本。キットはプロジェクト非依存。**Subagent 禁止** · **Hermes MCP 禁止**。

## 1. ツールの種類

| 層 | 例 | 用途 |
|----|-----|------|
| 組み込み | Shell, Read, Write, Grep, Glob, SemanticSearch, Task | コード・コマンド・検索 |
| MCP（Cursor） | cursor-ide-browser, cursor-app-control, cursor-backend-control | IDE 内ブラウザ・ワークスペース・Automations API |
| MCP（プラグイン） | Linear, Slack, Figma, Notion, Datadog 等 | 連携（有効化は環境依存） |

**発見方法**: エージェント環境の MCP descriptor ディレクトリ（`mcps/<server>/tools/*.json`）を列挙し、**CallMcpTool 前にスキーマを読む**。

## 2. WebSearch（用語・P0–P4 必須）

要求定義・要件定義・設計・計画では **用語の食い違い** を防ぐため、**WebSearch を先に** 使う。

| 目的 | ツール |
|------|--------|
| 用語・工程の定義 | **WebSearch**（2 クエリ以上推奨） |
| 権威ある解説ページ | **browser MCP**（§3） |
| プロジェクト内定義 | Read `docs/glossary/` |

Skill: **`terminology-research`** · Policy: `docs/TERMINOLOGY_RESEARCH_POLICY.md`

**禁止**: 検索なしで `要求.md` / `要件.md` / 設計正本を書く；「一般には…」だけで終える。

## 2b. WebSearch（探索型 · 広→狭）

方針・アーキテクチャ・「調査してから結論」では **landscape-research** を使う。

| 段 | 動作 |
|----|------|
| Frame | 5–7 軸に分解 |
| Scan | **並列 WebSearch** · 浅い · 地図のみ |
| Cluster | 重複/対立/空白 · drill hooks 2–4 |
| Drill | hooks のみ深掘り |
| Map+Critique | キット写像 · 反証 |

Skill: **`landscape-research`** · Policy: `docs/LANDSCAPE_RESEARCH_POLICY.md`

**禁止**: 1 クエリで結論；scan 無し drill；用語定義を landscape で代用。

## 3. Web 確認・スクリーンショット（browser MCP）

### 使う: cursor-ide-browser

| 目的 | ツール |
|------|--------|
| URL を開く | `browser_navigate` |
| 構造把握 | `browser_snapshot` |
| 画像証跡 | `browser_take_screenshot` |
| クリック・入力 | `browser_click`, `browser_fill`, … |
| 長い操作前 | `browser_lock` / unlock |

### 典型フロー

```
browser_tabs (list)
→ browser_navigate(url)
→ browser_lock(lock)
→ browser_snapshot または browser_take_screenshot
→ （必要なら操作）
→ browser_lock(unlock)
```

### 使わない（エージェント作業として）

- 「お使いのブラウザで URL を開いてください」だけ（スクショが必要なとき）
- OS 既定ブラウザをエージェントの代わりにする想定

### 例外

- ログイン・CAPTCHA・手動 MFA など **エージェントが触れない** と判明したら停止し、ユーザーに引き継ぎを明示

## 3. ターミナル・コマンド

| 目的 | 使うもの |
|------|----------|
| コマンド実行 | **Shell** |
| 長時間待ち | `block_until_ms`, **Await**, バックグラウンド |
| 既存ターミナル出力 | terminals フォルダのテキスト（Read） |
| dev サーバー起動後の確認 | Shell で起動 → **browser_navigate** で localhost |

## 4. IDE / ワークスペース（cursor-app-control）

| 目的 | ツール |
|------|--------|
| 別ルートで続行 | `move_agent_to_root` |
| 新規プロジェクト作成 | `create_project` |
| ファイル・ターミナル・URL を IDE に表示 | `open_resource` |
| Automations UI | `open_automation` |
| チャット名 | `rename_chat` |

`open_resource` は表示用。**エージェントがページを操作・撮影する**場合は browser MCP。

## 5. Cursor Automations API（cursor-backend-control）

- `list_automations` / `get_automation` / `create_automation` / `update_automation`
- GitHub Actions 等と混同しない（Cursor Automations 専用）
- 作成・更新はユーザー確認後

## 6. プラグイン MCP（例）

環境で有効なものだけ使う。代表例:

| 領域 | サーバー例 |
|------|------------|
| Issue / プロジェクト | plugin-linear-linear |
| デザイン | plugin-figma-figma |
| 通知 | plugin-slack-slack |

**断定禁止**: descriptor が無いときだけ「未接続」と報告。

## 7. よくある見落とし

| 症状 | 原因 | 対策 |
|------|------|------|
| スクショが取れない | OS ブラウザ案内のみ | browser MCP |
| テストを実行していない | 口頭依頼のみ | Shell |
| Linear を触れない | MCP 未確認 | descriptor 確認 → CallMcpTool |
| 同じ操作の失敗ループ | スナップショットなし | snapshot → 再試行は1回まで |

## 8. スキル

| Skill | 用途 |
|-------|------|
| **`terminology-research`** | P0–P4 用語・定義の WebSearch + browser |
| **`landscape-research`** | 探索型 · 広→狭 scan+drill · `LANDSCAPE_RESEARCH_POLICY` |
| `cursor-capabilities-reference` | 実行前の棚卸し・MCP 確認 |
| `cursor-tool-select` | 意図→ツールの短い対応表 |

Rules: `cursor-tooling-pm`（PM）, `cursor-tooling-stewards`（Cursor roles）, `no-subagents`, `kit-context-routing`

**Subagent 境界**: [CURSOR_SUBAGENT_POLICY.md](./CURSOR_SUBAGENT_POLICY.md)（Task/Explore 禁止 · Cloud はキット外）

## 9. Plan ファイルの二重化（c-08）

| パス | 役割 | 正本 |
|------|------|------|
| `.agents/plans/` | P4–P6 工程契約 · criteria · PDCA · unit 完走 | **キット** |
| `.cursor/plans/` | Cursor Plan Mode の作業メモ · 中断再開（任意） | **製品** |

**ルール**: agreed plan · Gate · review は **`.agents/plans/` のみ**。Cursor plan へ自動同期しない。

## 10. 併用ツール（c-09 · キット外）

キットの Execution 正本は **Cursor 同期セッション**（secretary · role-execute）。以下は **併用可** · 別 WF · `AGENTS.md` で宣言。

| ツール | 典型用途 | キットとの関係 |
|--------|----------|----------------|
| **Claude Code** | CLI · CI · 大規模 refactor | キット外 · hooks は利用先 |
| **GitHub Copilot** | 既存 IDE インライン | 非正本 · Enterprise 配布向け |
| **Windsurf 等** | 代替 AI IDE | キット非想定 |

## 11. 料金 · Enterprise（c-10）

| 項目 | ガイド |
|------|--------|
| 正本 | [cursor.com/pricing](https://cursor.com/pricing)（キットに料金表は載せない） |
| landscape / terminology | **Auto mode 優先**（frontier 手動選択は credit 消費） |
| Teams / Enterprise | SSO · org privacy · audit API — `regulated-checklist` §5.5 |
| 大 repo | `unit_scope` · scoped RE · monorepo-scoping（o-10） |
