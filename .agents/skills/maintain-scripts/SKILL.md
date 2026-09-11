---
name: maintain-scripts
description: Inventory and review scripts under skills/*/scripts/. Use when auditing or refactoring kit helper scripts.
---

# Maintain Scripts

**Role**: `kit_maintainer` · **Read + report**（変更は `maintain-record`）

**When**: スクリプト追加後 · 定期メンテ · 共通化検討前

**Prerequisite**: `maintain-reference` · 正本: [`../_SCRIPT_POLICY.md`](../_SCRIPT_POLICY.md)

## Workflow

[`references/workflow.md`](references/workflow.md)

## Rubric

[`references/script-review-rubric.md`](references/script-review-rubric.md)

## Commands（agents-run）

| Stem | 用途 |
|------|------|
| `inventory` | 全 scripts 一覧 · SKILL.md 未記載検出 |
| `review` | ポリシー準拠チェック（`--skill NAME` 可） |
| `dedupe-report` | 重複 stem / 類似 body の抽出候補（dry-run） |

```powershell
python env/bin/agents-run.py maintain-scripts inventory skills
python env/bin/agents-run.py maintain-scripts review
python env/bin/agents-run.py maintain-scripts dedupe-report
```

## Output

[`assets/inventory-report-template.md`](assets/inventory-report-template.md)

## 分担

| Skill | 役割 |
|-------|------|
| `maintain-adhoc` | layout 監査（`audit-skill-layout`） |
| **maintain-scripts** | スクリプト資産の inventory / review / 共通化案 |
| `maintain-record` | リファクタ適用 · `env/python/lib/` 追加 |

## 禁止

- ターン中の ad-hoc スクリプト新規作成
- プロジェクト `.venv` への依存
- hook（`hooks/`）の env 化 — stdlib のみ維持
