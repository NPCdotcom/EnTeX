---
id: lesson-brownfield-reverse-engineering
kind: knowledge
topic: lesson
owner: kit
status: active
created: 2026-06-22
tags: [product-dev, aidlc, brownfield, reverse-engineering, g2]
sources:
  - learning/product-dev/notes/synthesis/gap-analysis.md
  - learning/product-dev/notes/optimization/o-05-brownfield-regulated.md
  - learning/product-dev/notes/scans/a-06-report.md
promoted_at: 2026-06-22
---

# 教訓 — brownfield reverse engineering パターン

## Principle

AI-DLC Reverse Engineering のキット翻訳は **専用 skill + 圧縮テンプレ 6 件** とする。`landscape-research`（コード外）と **役割分離**。P1 前にユーザー Go。

## Facts

- G2: RE 成果物セットなしが brownfield 最大リスク（a-06）
- 8–9 ファイル丸コピーは過剰 — workspace · architecture · deps · api · data · tech-debt に圧縮
- `adaptive-lifecycle-plan` の `brownfield: true` と連動

## Decisions

- skill 名: `brownfield-reference`（実行 skill ではなく参照・記録手順）
- 成果物: `docs/design/reverse-engineering/`（利用先コピー）
- hotfix profile は inventory のみで可

## Anti-patterns

- RE スキップで大規模変更
- aidlc-docs ディレクトリ名の直輸入

## Recall

brownfield 初回 · G2 · RE テンプレ · P1 前
