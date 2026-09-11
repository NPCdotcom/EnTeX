---
title: Example — normalize text transform
kind: plan
status: draft
scope_level: algorithm
pdca_class: S1
pdca_eligible: true
related_design: docs/design/programs/example-normalize.md
related_requirements: docs/requirements/sample-capability/要件.md
parent_hierarchy:
  product: docs/design/product/charter.md
  element: docs/design/elements/example-export.md
  system: ""
  framework: ""
---

# Example plan（algorithm）— 置換して使用

> **サンプル**: 文字列正規化アルゴリズム。実プロジェクトの algorithm に合わせて全文差し替え。

## Goal

選択されたテキストフィールドを、出力前に定義済みルールで正規化する（例: 改行統一、前後空白除去）。

## Scope hierarchy

| Level | Path | Status |
|-------|------|--------|
| H0 product | docs/design/product/charter.md | draft |
| H1 element | docs/design/elements/example-export.md | draft |
| H4 program | docs/design/programs/example-normalize.md | draft |
| H5 algorithm | （this plan） | draft |

## Scope

### In scope

- 単一文字列 in → 正規化 out の純関数
- ルールセット 2 種（trim, normalize-newlines）

### Out of scope

- ファイル IO、UI、並列処理

## Acceptance criteria（≤5）

- [ ] `trim` が前後空白を除去する
- [ ] `normalize-newlines` が `\r\n` を `\n` に統一する
- [ ] 空文字列はエラーにせず空のまま返す
- [ ] 既存テストコマンドが通る（利用先のスタックに合わせる）

## Agent recommendations

**推奨**: 先に program 設計で入出力型を固定してから本 algorithm を implement。

## User thinking

> 

## Open questions

- ルールの追加はデータ駆動かコード分岐か？

## PDCA log

| Date | Phase | Note |
|------|-------|------|
| | Plan | example only |
