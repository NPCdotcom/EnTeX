# 最初の実プロジェクトを始める（汎用）

> **キット利用先**向け。特定製品名・ドメインは書かない。`{{...}}` を置換して使う。

## 1. Bootstrap 後にコピーするもの

| キット内（`.agents/docs/`） | 利用先（リポジトリ `docs/`） |
|---------------------------|------------------------------|
| `PROJECT_LIFECYCLE.md` | `docs/PROJECT_LIFECYCLE.md` |
| `project-state.template.yaml` | `docs/project-state.yaml`（下記初期値） |
| `LINEAR_PHASE_MAP.md` | 任意 |
| `CONSUMER_DOCS_README.template.md` | `docs/README.md` |
| `_example/` 一式 | 参照 or コピー（**リネーム必須**） |

`maintain-bootstrap` が上記を自動化できる。手動でも可。

## 2. `project-state.yaml` と `nav.yaml` の初期値

### project-state.yaml

```yaml
current_phase: P0
phase_note: "New project — defining product charter"
scope_focus:
  level: H0
  path: docs/design/product/charter.md
active_pdca:
  plan_path: ""
  scope_level: ""
  pdca_class: ""
gate_status:
  current: pending
  proposal: ""
  last_decision: ""
  last_decided_at: ""
  conditions: []
  gate_keeper: user
last_gate_passed: ""
allowed_actions:
  - design-deliberate
  - design-record
open_blockers: []
```

### nav.yaml（Control Plane · 毎ターン）

```bash
cp .agents/memory/state/nav.yaml.example .agents/memory/state/nav.yaml
```

`session.intent` · `navigation.next_actions`（≤3）を毎ターン更新。正本: `docs/PM_ROUTING.md`

### hooks（summarize 先制 · 推奨）

キットの `hooks.json` + `hooks/*.py` をプロジェクト `.agents/` に配置（`maintain-bootstrap` 参照）。

## 3. 推奨作成順（H 高 → 低）

| 順 | 工程 | パス（例） | 備考 |
|----|------|------------|------|
| 1 | P0 | `docs/design/product/charter.md` | `_example` または `_charter-template` |
| 2 | P1 | `docs/requirements/<your-slug>/要求.md` | slug は英数字 kebab（**sample-capability は例**） |
| 3 | P2 | 同フォルダ `要件.md` | `>` に殴り書き → 推敲 |
| 4 | P3 | `docs/design/elements/`, `systems/`, … | 上位 H を先に |
| 5 | P4 | `.agents/plans/programs/` or `algorithms/` | **PM がユーザー確認**後 |
| 6 | P5–P6 | ソース + review | plan `agreed` のみ大規模 Do |

## 4. `_example/` の使い方

- **目的**: 空テンプレだけでは想像しづらい場合の**中立サンプル**（ゲーム・業界非依存）
- **必須ではない**。不要なら `_example/` ごと削除してよい
- コピー時は `sample-capability` → **自分の slug** にリネームし、本文の「例」「サンプル」を消す

## 5. PDCA を回す単位（再確認）

- **主**: `scope_level: program` または `algorithm` の plan 1 件 = 1 サイクル
- **前**: その program/algorithm が **何のため** か（H0–H3）を design / requirements でリンク

## 6. エージェントとの推敲

1. PM が `role-execute` で `spec_designer` スキル列を実行 — 草案 + **選択肢・おすすめ**  
2. ユーザーが `>` ブロックに思考を追記  
3. 確定部分を本文へ移動 → `status: agreed` は**ユーザー確認後**のみ  

## 参照

- [PROJECT_LIFECYCLE.md](./PROJECT_LIFECYCLE.md)
- [requirements/README.md](../.agents/docs/requirements/README.md)
- [requirements/_template/](../.agents/docs/requirements/_template/)
- [_example/README.md](../.agents/docs/_example/README.md)
