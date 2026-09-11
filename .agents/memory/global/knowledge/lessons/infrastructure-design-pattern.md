---
id: lesson-infrastructure-design
kind: knowledge
topic: lesson
owner: kit
status: active
created: 2026-06-22
tags: [product-dev, aidlc, infrastructure, iac, g9]
sources:
  - learning/product-dev/notes/synthesis/gap-analysis.md
  - learning/product-dev/notes/optimization/o-06-infrastructure-iac.md
  - learning/product-dev/notes/scans/a-07-report.md
promoted_at: 2026-06-22
---

# 教訓 — Infrastructure Design（G9）パターン

## Principle

AI-DLC Infrastructure Design のキット翻訳は **P3 `docs/design/systems/` + 圧縮テンプレ 6 件** とする。新 skill は作らず `design-deliberate` / `design-record` で記録。CI（Checkov）は **利用先 workflow 例** に委任。

## Facts

- G9: P3 IaC 明示弱い（gap-analysis · a-07）
- Checkov は a-07 CI 層 — キットは設計テンプレ + 例のみ
- G4 Operations: P3 observability-hooks → `docs/_template/operations/`（o-08）→ 利用先 `docs/operations/`

## Decisions

- テンプレ: topology · iac-structure · networking · environments · observability-hooks · iac-verification
- 例: `_example/.github/workflows/iac-checkov.example.yml`

## Anti-patterns

- IaC を programs テンプレのみで代替
- 汎用キットに Terraform モジュールを同梱

## Recall

G9 · IaC · P3 · Checkov · infrastructure template
