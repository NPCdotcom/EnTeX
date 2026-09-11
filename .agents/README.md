# Agent PDCA Asset Kit（汎用 · `.agents` 正本）

このキットは **プロジェクト非依存** のエージェント資産（スキル・ルール・記憶・Hooks）です。

| 配置 | 用途 |
|------|------|
| **`%USERPROFILE%\.agents\`** | ユーザーキット正本（本配置） |
| **`./.agents/`** | 利用先プロジェクトへ bootstrap コピー |

**Cursor 互換**: Cursor は `.cursor/rules` · `.cursor/skills` · `.cursor/hooks.json` を直接読む。正本 `.agents/` から [`scripts/link-cursor.ps1`](scripts/link-cursor.ps1) で junction を張る — [`docs/CURSOR_COMPAT.md`](docs/CURSOR_COMPAT.md)

**原則**: 利用先のドメイン仕様は **リポジトリルート `AGENTS.md`** と **`rules/local/`** のみ。キット本体には書かない。

## 新規プロジェクトへの導入

1. `%USERPROFILE%\.agents\`（または本キット）を `./.agents/` へコピー
2. `./.agents/scripts/link-cursor.ps1` で Cursor 用 junction 作成
3. `./.agents/env/bin/setup.ps1` でエージェント実行環境を作成
4. `kit_maintainer` + `maintain-bootstrap`（または手動）
5. [AGENTS.md.template](AGENTS.md.template) をルートの `AGENTS.md` としてコピーし、プレースホルダと **スタック文書** 表を埋める
6. `docs/` の骨格を作成（下記レイアウト）
7. 必要なら [rules/local/](rules/local/) にスタック用 `.mdc` を生成（テンプレ + `AGENTS.md` の文書参照）

## 長期記憶（IDE 正本）

> **Hermes Agent は使用しない。** チャット短期記憶を `.agents/memory/` へ掃き出す。

正本: [`docs/MEMORY_ARCHITECTURE.md`](docs/MEMORY_ARCHITECTURE.md) · [`docs/PM_ROUTING.md`](docs/PM_ROUTING.md)

| 優先 | パス |
|------|------|
| 0 | `.agents/memory/state/nav.yaml`（Control Plane） |
| 1 | `.agents/memory/index.yaml` |
| 2 | `.agents/memory/state/` ＝ `docs/project-state.yaml` |
| 3 | `.agents/memory/episodes/` · `traces/` · `evaluations/` |
| 4 | `.agents/memory/knowledge/` |

毎ターン: **pm-turn-start** → role-execute → **pm-turn-end**（正本 [`_chains/pm-turn.md`](skills/_chains/pm-turn.md)）  
学習ターン: **`learning/<topic>`** · Rule `learning-sandbox` · 詳細 [`docs/LEARNING_SANDBOX.md`](docs/LEARNING_SANDBOX.md)  
手順: [docs/PM_ROUTING.md](docs/PM_ROUTING.md) · [docs/MANDATORY_PROCEDURES.md](docs/MANDATORY_PROCEDURES.md)

## Cursor Hooks（summarize 先制）

| ファイル | 用途 |
|----------|------|
| [`hooks.json`](hooks.json) | `preCompact` + `stop`（Re-anchor · loop_limit 3） |
| [`hooks/pre-compact.py`](hooks/pre-compact.py) | nav `pressure=pre_compact` · history ログ |
| [`hooks/stop-reanchor.py`](hooks/stop-reanchor.py) | pre_compact 時 Re-anchor followup |

## Agent 実行環境（env）

**プロジェクトのデバッグ用 venv とは別** — キット作業専用。

| パス | 用途 |
|------|------|
| [`env/README.md`](env/README.md) | セットアップ · Python/Node 方針 |
| [`env/bin/setup.ps1`](env/bin/setup.ps1) | 初回 venv 作成 |
| [`env/bin/agents-run.py`](env/bin/agents-run.py) | スキル `scripts/` の推奨入口 |
| [`skills/_SCRIPT_POLICY.md`](skills/_SCRIPT_POLICY.md) | ad-hoc コード禁止 |

```powershell
.\env\bin\setup.ps1
python env\bin\agents-run.py maintain-adhoc audit-skill-layout skills
```

## Web 調査（2 系統）

| Skill | 用途 |
|-------|------|
| **`landscape-research`** | 広→狭 · 探索・方針 · [`LANDSCAPE_RESEARCH_POLICY.md`](docs/LANDSCAPE_RESEARCH_POLICY.md) |
| **`terminology-research`** | 用語 · P0–P4 gate · [`TERMINOLOGY_RESEARCH_POLICY.md`](docs/TERMINOLOGY_RESEARCH_POLICY.md) |

## レイアウト（汎用）

```
.agents/
├── env/                   # エージェント実行環境（python venv · node）
│   └── bin/agents-run.py  # スキル scripts 起動
├── hooks.json             # preCompact · stop Re-anchor
├── hooks/                 # pre-compact.py · stop-reanchor.py
├── memory/                # 長期記憶 + nav.yaml + traces/evaluations/rewards
├── skills/                # 手順書
├── rules/
├── plans/
├── handoffs/              # Legacy（2026-06-17 廃止 · 読取のみ）→ memory/episodes へ
├── learning/              # 学習・実験サンドボックス（検証前）→ docs/LEARNING_SANDBOX.md
├── mcp.json.template      # 空（Hermes 撤去）
└── docs/
```

## Cursor Roles

正本: [`docs/CURSOR_ROLES.md`](docs/CURSOR_ROLES.md) · 実行: **`role-execute`**（PM）

| Role | 責務 |
|------|------|
| `router` | 入口・brief |
| `spec_designer` | P0–P3 設計 |
| `plan_slicer` | P4 計画 |
| `builder` | P5 実装 |
| `hotfixer` | 手直し |
| `reviewer` | レビュー |
| `evaluator` | 評価 |
| `automator` | Automation |
| `kit_maintainer` | キット |

## スキル（抜粋）

| 領域 | Skills |
|------|--------|
| **記憶** | `memory-reference`, `memory-record`, `memory-flush` |
| 秘書 | `secretary-*` + `cursor-tool-select` |
| PM 実行 | `role-execute` |
| 横断 | `role-skill-catalog` |

## メンテナンスの二モード

| モード | スキル | 典型タイミング |
|--------|--------|----------------|
| **始動** | `maintain-bootstrap` | キットコピー直後、`AGENTS.md`・`docs/`・`rules/local/` |
| **臨時** | `maintain-adhoc` | role 追加、memory/skill 改訂 |
| **スクリプト** | `maintain-scripts` | `skills/*/scripts/` の inventory · review · 共通化案 |

Rule: `maintenance-stewardship` · Role: `kit_maintainer`

## ルール（rules）

| ファイル | 用途 |
|----------|------|
| `no-subagents.mdc` | **alwaysApply** — Subagent 使用禁止（誤爆防止） |
| `secretary-gate.mdc` | **alwaysApply** — 毎ターン PM HARD GATE · 標準/軽量ループ · 運用証跡 |
| `kit-context-routing.mdc` | **alwaysApply** — PM vs steward 正本 · 禁止事項 |
| `cursor-tooling-pm.mdc` | PM — ツール割当・委譲 |
| `cursor-tooling-stewards.mdc` | Cursor role — PM brief の browser/Shell |
| `maintenance-stewardship.mdc` | キット・始動／臨時メンテナンス |
| `secretary-stewardship.mdc` | `router` — brief・ルーティング |
| `design-stewardship.mdc` | 思案・設計の起動条件 |
| `documentation-adr-glossary.mdc` | ADR・用語 |
| `docs-content.mdc` | `docs/**` 形式 |
| `planning.mdc` | 実装計画 |
| `plans-content.mdc` | `.agents/plans/**` 形式 |
| `review-stewardship.mdc` | レビュー |
| `evaluation-stewardship.mdc` | 中間評価 |
| `implementation-stewardship.mdc` | 実装（Do） |
| `patch-stewardship.mdc` | 小手修正・バグ（PM / 大 Do のコンテキスト分散） |
| `automation-stewardship.mdc` | 承認済み plan サイクルの Automation 境界 |
| `local/*` | **利用先プロジェクト固有**（テンプレから生成） |
| `phase-index.mdc` | 工程 P0–P6 と rule/skill の対応 |
| `role-cross-skills.mdc` | Cursor role cross-skill usage |

（`project-leadership.mdc` は R-3 で削除 — `secretary-gate` + `PM_ROUTING` に統合）

## プロジェクト文脈

- **`AGENTS.md`**（リポジトリルート）: プロジェクト専用。リーダー方針・スタック文書表・設計原則。
- **コンテキスト分担**: Rules **`secretary-gate`** · **`kit-context-routing`** · **`no-subagents`**（alwaysApply）+ [CONTEXT_TIERS.md](docs/CONTEXT_TIERS.md) + [MANDATORY_PROCEDURES.md](docs/MANDATORY_PROCEDURES.md)
- **メインエージェント**: Rules `secretary-gate`（alwaysApply）, `cursor-tooling-pm`
- **Subagent**: 使用禁止（誤爆防止）
- **コンテキスト高負荷（目安 55%+）**: PM は高負荷モードに入り、`router` の割当表を短手順で実行。PM は統合と応答のみ。
- **本キット**: エンジン・ドメイン非依存。スタック固有レンズは `rules/local/`（利用先のみ）。
- **Automation**: `automations/AUTOMATION_INSTRUCTION.md` と `docs/LINEAR_AUTOMATION_POLICY.md` を参照。`agreed` plan 以外は実行しない。
- **Automation templates**: `automations/CURSOR_AUTOMATION_TEMPLATES.md` に trigger/instruction/approval の雛形を用意。
- **Agent tooling**: `docs/CURSOR_AGENT_TOOLING.md` — ブラウザ MCP・ターミナル・プラグイン MCP の使い分け。

## ライフサイクル（三層）

[docs/PROJECT_LIFECYCLE.md](docs/PROJECT_LIFECYCLE.md) — 工程 **P0–P6**、スコープ **H0–H5**、PDCA **S0–S1**（主に program/algorithm）。

| 成果物 | パス |
|--------|------|
| 状態 | `docs/project-state.yaml`（`gate_status` 含む） |
| 要求・要件 | `docs/requirements/<slug>/` |
| 設計 | `docs/design/{product,elements,systems,frameworks,programs}/` |
| 計画 | `.agents/plans/{programs,algorithms}/`（主 PDCA） |

Rule `project-lifecycle` · Skill `lifecycle-reference` · **役割・PM**: [docs/ROLES_AND_GOVERNANCE.md](docs/ROLES_AND_GOVERNANCE.md) · **カタログ**: [role-skill-catalog](skills/role-skill-catalog/references/full-catalog.md) · 起動: [docs/FIRST_PROJECT_START.md](docs/FIRST_PROJECT_START.md)

## PDCA フロー

0. `kit_maintainer` — キット導入（初回のみ）  
（毎回）`router` — 工程/スコープ/ゲート付き brief  
P0–P3 `spec_designer`（requirements + design、**H 高→低**）  
P4 `plan_slicer`（programs/algorithms、**ユーザー確認**）  
P5 **`builder`** — Do  
P6 `reviewer` — Check → Act（plan 分割・工程巻き戻し可）  
`evaluator` — 任意（at_risk 時は分割推奨）  
