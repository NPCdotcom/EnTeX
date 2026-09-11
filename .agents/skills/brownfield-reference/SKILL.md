---
name: brownfield-reference
description: Inventory an existing repo and fill reverse-engineering templates before new requirements. Use on legacy codebases or when adaptive-lifecycle says brownfield first.
---

# Brownfield Reference

**Role**: `spec_designer` · `router`（入口判定）  
**参照**: `docs/design/_template/reverse-engineering/` · `adaptive-lifecycle-plan` · `landscape-research`（コード外の業界調査のみ）

## When

- `lifecycle_plan.brownfield: true`
- 既存 repo 初回 · 大規模リファクタ前 · P1 前に「現状把握」が必要
- `adaptive-lifecycle-plan` が Reverse Engineering を推奨

## Workflow

[`references/workflow.md`](references/workflow.md) · **monorepo**: [`references/monorepo-scoping.md`](references/monorepo-scoping.md)

## Output

利用先: `docs/design/reverse-engineering/`（テンプレコピー後に記入）

## Do not

- AI-DLC `aidlc-docs/inception/reverse-engineering/` 丸コピー
- RE なしで既存コードに大規模変更を開始
- Web 業界調査を本 skill で代用（→ `landscape-research`）
- ユーザー Go なしに P1 要求を確定
