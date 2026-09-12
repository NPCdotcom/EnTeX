---
title: ir-validate-and-derive — 封筒・型検証と導出値計算
kind: plan
status: agreed   # Do 完了（2026-09-12）。P6 review 後に superseded/closed を判断
scope_level: algorithm
pdca_class: S1
pdca_eligible: true
created: 2026-09-12
updated: 2026-09-12
related_design: docs/design/programs/renderer.md
related_requirements: docs/requirements/circle-monthly-report/要件.md
promoted_from: ""
parent_hierarchy:
  product: docs/design/product/charter.md
  element: docs/design/elements/ir-type-vocabulary.md
  system: ""
  framework: ""
---

# ir-validate-and-derive

## Goal

`renderer`（H4: [renderer.md](../../../docs/design/programs/renderer.md)）の前段、`ir/loader.py`・`ir/derive.py` を実装し、要件.md の FR1–FR4 を満たす。LaTeX 非依存なので `make test` だけで完了判定できる。

## Scope hierarchy（確定済み上位）

| Level | Path | Status |
|-------|------|--------|
| H0 product | docs/design/product/charter.md | draft（P0 ゲート Go 済み） |
| H1 element | docs/design/elements/ir-type-vocabulary.md | draft（決定A: 導出値は生成時計算） |
| H2 system | — | — |
| H3 framework | charter §7（pydantic）で確定済み | agreed |
| H4 program | docs/design/programs/renderer.md | draft（P3 完了） |
| H5 algorithm | この plan | this plan |

## Scope

### In scope

- `src/entex/ir/schema.py`: `packages/<slug>/schema.json`（案1 形式）を pydantic モデルで読む。11 型・フィールド属性・`expr` の形を検証し、`expr` の参照先が「自分より前に宣言された `integer` / `money` フィールド」であること（循環・前方参照の拒否）をここで検査する
- `src/entex/ir/loader.py`: 封筒（`doc_type` / `schema_version`）→ パッケージ解決 → `content` の型検証（FR1–FR3）。エラーはフィールドの `label` を使った日本語文で、見つかった分をまとめて返す
- `src/entex/ir/derive.py`: `sum` / `count` / `add` / `sub`（`where` 付き）を宣言順に評価し、導出値を埋める（FR4）
- `src/entex/errors.py`: `EnvelopeError` / `IRValidationError` / `DerivationError` / `PackageError` / `RenderError`（後者は plan `render-and-cli` が使う）。すべて `user_message` を持つ
- `src/entex/packages.py`: `packages/<slug>/` の場所の解決と読み込み（`schema.json` / `template.tex.j2` / `style/`）
- `schemas/ir/envelope.schema.json`: 封筒の JSON Schema を pydantic モデルから生成し、テストでズレを検知する
- テスト: `packages/circle-monthly-report/examples/` 全 12 件を素材にする

### Out of scope

- TeX エスケープ・テンプレート組み立て・latexmk・CLI（plan `render-and-cli`）
- `schema.json` の JSON Schema（案2）生成（2 つ目の文書種の前に判断。ir-type-vocabulary.md §8）
- 導出値の一致検証（決定B の後付け。API 化のとき）

## Acceptance criteria（S1: ≤5 推奨）

- [x] AC1 (FR1): `examples/invalid/06-envelope-mismatch.json` を渡すと `EnvelopeError` 1 件のみで止まり、中身のエラーは報告されない — `tests/test_ir_loader.py::test_envelope_mismatch_stops_before_content`
- [x] AC2 (FR2): `examples/invalid/03-unknown-enum-and-negative-amount.json` で、区分の不正と金額の負の **2 件が 1 回の呼び出しで** 返る。`examples/valid/` 6 件はすべて検証を通り、`examples/invalid/` 6 件はすべて弾かれる — `test_two_errors_come_back_in_one_call` / `test_all_valid_examples_pass` / `test_all_invalid_examples_fail`
- [x] AC3 (FR3): `examples/invalid/01-derived-key-in-input.json` で `income_total` / `balance` が「自動計算です」の文言で拒否される — `test_derived_key_in_input_is_rejected`
- [x] AC4 (FR4): `01-typical`（活動 5 回・延べ 77 人・収入 138,000・支出 131,400・残高 19,400）・`02-minimal`（残高 5,400）・`03-deficit`（残高 −4,800）・`04-max-rows`・`05-fiscal-year-start` の導出値が README の期待値と一致する。`expr` に前方参照・循環を仕込んだ schema は `PackageError` で読み込み時に落ちる — `tests/test_ir_derive.py` / `tests/test_ir_schema.py`
- [x] AC5: 利用者向けメッセージは日本語で、フィールド名ではなく `label` を使う。`make lint` / `make test` が通る — `test_messages_use_labels_not_field_names`、ruff / pytest 全通過（2026-09-12）

## Dependencies

- `packages/circle-monthly-report/schema.json` と `examples/`（既存）
- pydantic 2.x（既存依存）

## Facts

- 要件.md FR1–FR4 と検証方法（examples の対応）は確定済み
- ir-type-vocabulary.md §4: 導出値は生成時計算（決定A）、`expr` は JSON 構造、宣言順評価・循環拒否
- ir-type-vocabulary.md §6.1: 未知キー・導出キーは拒否、任意フィールドは `null` ではなくキー省略

## Assumptions

- `schema.json` は案1 形式のまま（案2 に転んでも `ir/schema.py` の読み込み部だけの差し替えで済む）
- 検証エラーの文言は `packages/circle-monthly-report/README.md` の異常系表を初期値とし、実運用で直す

## Open questions

- `text` の NFC 正規化は検証段で値を書き換える（正規化後の値をテンプレートに渡す）。入力を書き換えてよいかは API 化時に再確認
- 未知キーの「〜の間違い？」サジェストの閾値（difflib の cutoff）

## Agent recommendations（計画時）

| 案 | 概要 | 推奨度 |
|----|------|--------|
| 1 | `schema.json` から pydantic モデルを `create_model` で動的生成し、pydantic のエラー辞書を日本語へ写像する | △ — pydantic の `type` 文字列（版で変わる）に依存し、`label` 付き日本語文の組み立てが写像表任せになる |
| 2 | `schema.json` 自体と封筒・`expr` は pydantic の **静的モデル** で検証し、`content` は 11 型それぞれの検証関数（スキーマを辿る walker）で検証する | ✓ — 語彙が閉じていて小さい。日本語文・行番号付きの位置表示・NFC 正規化後の値の生成を自前で制御できる。renderer.md が許容した 2 方式のうちの後者 |

**推奨**: 案2。renderer.md Open questions「動的生成か検証関数か」はここで案2 に決定する。

## User thinking（推敲）

> 2026-09-12: ユーザー指示「P3の設計に従って実装に入ってください」を PM 確認とみなし `status: agreed` とした。

## Progress assessments

| Date | Verdict | Summary |
|------|---------|---------|
| 2026-09-12 | on_track | plan 記録直後。実装は同日中に着手 |
| 2026-09-12 | on_track | Do 完了。AC1–AC5 すべてテストで担保。P6 レビュー待ち |

## PDCA log

| Date | Phase | Note |
|------|-------|------|
| 2026-09-12 | Plan | renderer.md の分割案どおり起票。方式は案2（静的 pydantic + 型別検証関数）に決定 |
| 2026-09-12 | Do | 実装: `src/entex/errors.py`・`packages.py`・`ir/{schema,validate,loader,derive}.py`、`schemas/ir/envelope.schema.json`（pydantic から生成、同期テストあり）。テスト 74 件（`tests/test_ir_*.py`）。設計からの差分: `ir/loader.py` の型検証部を `ir/validate.py` に分離し、`schema.json` のモデルを `ir/schema.py` に置いた（境界は変えていない）。`expr` の参照先検査（前方参照・循環・任意項目の default 必須）はパッケージ読み込み時に行う |
