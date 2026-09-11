---
title: Example program — normalize for export
kind: design
phase: P3
scope_level: program
status: draft
parent_element: docs/design/elements/example-export.md
related_requirements: docs/requirements/sample-capability/要件.md
---

# Program design（例: H4）

## 目的

エクスポート直前のテキストフィールドを正規化する（H1 `example-export` の一部）。

## 公開インターフェース（例）

- `normalizeField(value: string, rules: RuleId[]): string`

## 依存

- H5 algorithm: `.agents/plans/_example/algorithms/sample-transform.md`（実装計画例）

## エージェント提案

**推奨**: algorithm を先に S1 PDCA で完了し、program は薄いラッパに留める。

## ユーザー思考

> 

## 次

- [ ] PM ユーザー確認 → plan `algorithms/` へ（利用先パス）
