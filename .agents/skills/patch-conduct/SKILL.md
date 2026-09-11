---
name: patch-conduct
description: Apply a small fix within file/line caps. Use for hotfixes after patch scope was approved.
---

# Patch Conduct

**Role**: `hotfixer` · **P5+** · Execute

**Prerequisite**: `patch-reference` verdict = **patch_ok**.

## Workflow

1. 症状から最小修正を特定
2. caps 内で編集（既存パターン優先）
3. **AGENTS.md** + **rules/local/** implement lens
4. 検証手順を 1 シナリオで記述

## Caps（hard stop）

| Limit | Value |
|-------|-------|
| Files | ≤ 5 |
| Net diff | ≤ ~80 lines |
| Scope | One symptom |

超過 → stop → **builder**

## Do not

新 API/機能、rename sweep、while-here refactor、full review、design/plan 編集

詳細: [`references/standards.md`](references/standards.md)
