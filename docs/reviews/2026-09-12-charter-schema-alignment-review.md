---
title: charter・IR型語彙・renderer設計と実装の整合レビュー（着手順1完了時点）
kind: review
phase: P6
status: done
created: 2026-09-12
reviewer: Cursor cloud agent
related_design:
  - docs/design/product/charter.md
  - docs/design/elements/ir-type-vocabulary.md
  - docs/design/programs/renderer.md
related_plans:
  - .agents/plans/algorithms/ir-validate-and-derive.md
  - .agents/plans/programs/render-and-cli.md
related_requirements: docs/requirements/circle-monthly-report/要件.md
---

# charter・IR型語彙・renderer設計と実装の整合レビュー

親: [renderer.md](../design/programs/renderer.md) の「次」— P6 review-conduct（本レビューで実施）

## 目的

着手順1（charter §11: `entex render <json>` で1本通す）が完了した時点の実装（`src/entex/`・`packages/circle-monthly-report/`）が、charter §4・§6 の設計不変条件、`ir-type-vocabulary.md` の型語彙、`renderer.md` の基本設計と食い違っていないかを確認する。ユーザー指示「既存の実装からチャーターやスキーマなどの設計に合わせて改変すべき場所を探す」に対応する。

## 検査方法

1. `make setup` → `make lint` → `make test` をホストで実行
2. charter §4・§6 の4つの設計不変条件をコード・git履歴で確認
3. `ir-type-vocabulary.md` §1（11型）・§3（フィールド属性）・§4（導出値）を `src/entex/ir/schema.py` / `ir/validate.py` / `ir/derive.py` と1項目ずつ突き合わせ
4. `schemas/ir/envelope.schema.json` を `python -m entex.ir.loader` で再生成し、コミット済みファイルとの差分を確認
5. `renderer.md`「公開インターフェース / API」表・エラー分類表と実装のシグネチャ・例外階層を比較
6. `packages/circle-monthly-report/` の中身（`schema.json` / `template.tex.j2` / `style/`）を `packages/README.md` の規約と比較
7. ドキュメント間の相互参照（`AGENTS.md` / `README.md` / `docs/README.md` / `docs/design/**`）のリンク先実在確認

## 結果サマリ

**設計不変条件・IR型語彙・doc-package構造は実装と一致（不一致なし）。ドキュメント側の更新漏れを2件検出。** 実装（`src/entex/`・`packages/circle-monthly-report/`）を変更する必要のある不一致は見つからなかった。

### 一致を確認した項目

| 項目 | 確認内容 |
|---|---|
| charter §4/§6 不変条件1: 文書種追加でsrc/entex/を変えない | `git log --oneline -- packages/ src/entex/` で `b44f10f`（月次報告書のIR例とスキーマ）は `src/entex/` を含まない |
| 不変条件2: rendererがIRの出どころを知らない | `renderer.py`・`ir/*.py` にform/CSV/DB/HTTP依存が無い。`load_and_validate(raw, packages_dir)` はパース済みdictのみを受け取る |
| 不変条件3: 利用者にTeXを見せない | `RenderError.user_message` は汎用文（`GENERIC_MESSAGE`）のみ、latexmk生ログは `out_dir` にのみ書く。`tests/test_cli.py::test_render_failure_hides_tex_log_from_user` 等で担保 |
| 不変条件4: 「テンプレート」は`.tex.j2`のみを指す | `AGENTS.md`/`README.md`/`docs/design/**`/`packages/**/README.md` 全箇所で用法が charter §10 と一致 |
| IR型語彙11型 | `ir/schema.py` の `FieldType` / `SCALAR_TYPES` / `NUMERIC_TYPES` / `LIST_ITEM_TYPES` が §1 の表と一致（`money`符号あり・`row_list`はスカラーのみ・`list`要素は text/enum/date/integer に限定 等） |
| フィールド属性 | `required`/`default`（静的値のみ）/`derived`+`expr`/`minimum`/`maximum`/`max_length`/`min_items`/`max_items`/`pattern` すべて §3 の制約どおりに `_check_shape` で検査 |
| 導出値（§4 決定A） | `sum`/`count`/`add`/`sub`（`where`付き）を宣言順評価、前方参照・循環はパッケージ読み込み時に拒否。`ir/derive.py` の `apply_derived` で生成時計算のみ、IRに含めたら `IRValidationError` |
| envelope | `schemas/ir/envelope.schema.json` は `entex.ir.loader.Envelope` から再生成して差分なし（`tests/test_ir_loader.py` でも同期を検知） |
| doc-package構造 | `packages/circle-monthly-report/` は `packages/README.md` の規約（`schema.json`/`template.tex.j2`/`style/`/`examples/`/`README.md`）どおり |
| ドキュメント相互参照 | `AGENTS.md`/`README.md`/`docs/README.md`/`docs/design/**` の相対リンクに壊れたリンクなし |
| lint/test | `make lint`（ruff）オールパス、`make test`: 115 passed / 11 skipped（TeX依存分はコンテナ外環境のためskip） |

### 検出した不一致（2件・いずれもドキュメント側の更新漏れ）

1. **`renderer.md`「公開インターフェース / API」表（59–62行目）が実装のシグネチャと不一致**
   - 設計: `entex.ir.derive.apply_derived(ir: ValidatedIR, schema: Schema) -> DerivedIR`
     実装: `apply_derived(content: dict[str, Any], schema: Schema) -> dict[str, Any]`（`ir/derive.py`）
   - 設計: `entex.tex.escape.escape_context(ctx: DerivedIR) -> EscapedContext`
     実装: `escape_content(content: dict[str, Any], schema: Schema) -> dict[str, Any]`（関数名・引数とも相違、`tex/escape.py`）
   - 設計: `entex.renderer.render(ctx: EscapedContext, package_dir: Path, out_dir: Path) -> Path | RenderError`
     実装: `render(content: dict[str, Any], package: DocPackage, out_dir: Path, *, job_name: str = "document", timeout: float = 180) -> Path`（`RenderError`は例外として投げる形。`package_dir: Path`ではなく`DocPackage`を受け取る。`job_name`/`timeout`が追加、`renderer.py`）
   - renderer.md自身が「シグネチャは設計方針であり、実装時に確定させる」と明記しているため設計違反ではないが、各planのPDCAログには一部の差分（`ir/loader.py`のモジュール分割等）のみ記録され、この表自体は実装後に更新されていない。次のパッケージ追加（着手順3・2文書種目）で `renderer.md` を参照する際に古いシグネチャで誤解を招く

2. **主要な設計決定がADRとして記録されていない**
   - `ir-type-vocabulary.md` 内に「決定」として書かれている重要判断（§2.1 `money`の符号あり化、§4 導出値計算タイミングの決定A、§8 `schema.json`形式=案1の暫定採用）が、`docs/adr/`（現状 `.gitkeep` のみで空）にADRとして記録されていない
   - `AGENTS.md` の索引は「設計判断の記録 | `docs/adr/`」としているため、索引と実態がずれている

### 参考情報（本レビューの対象外だが引き継ぎ済みの既知事項）

- ブランチ名がAGENTS.md規約（`issue番号/担当者/やること`）ではなくクラウドエージェント規約（`cursor/…`）になっている（`.agents/memory/state/nav.yaml` に引き継ぎ済み）。charter/schemaとの整合とは無関係の運用課題
- NFR1（10秒以内）のタイミングテストはフォントキャッシュの初回コールドスタートで揺れる可能性がある（`ENTEX_NFR1_SECONDS` で調整可能。同nav.yamlに引き継ぎ済み）
- 実物の学生課様式（Word版）入手待ちの `packages/circle-monthly-report/schema.json` 確定は既知のOpen question（`ir-type-vocabulary.md` / `packages/circle-monthly-report/README.md` に記載済み）

## 結論

**実装（`src/entex/`・`packages/circle-monthly-report/`）そのものをcharter/IR型語彙/renderer設計に合わせて変更する必要のある不一致は見つからなかった。** 検出した2件はいずれも「実装完了後にP3設計書・ADRへ反映されていない」というドキュメント側の同期漏れであり、GitHub Issueとして起票し次回のドキュメント更新タイミング（次の2文書種目着手前）で解消するのが妥当と判断する。

## 次

- [ ] GitHub Issueを起票（本レビュー結果を元に、`renderer.md`のインターフェース表更新とADR起票をタスク化）
- [ ] 2文書種目（charter §11 着手順3）着手前に上記2件を解消
