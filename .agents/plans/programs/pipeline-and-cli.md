---
title: pipeline-and-cli — 共通パイプライン関数の導入と CLI の乗せ替え（P6 レビュー W1 / W2 / S1 / S3 の解消）
kind: plan
status: agreed   # 2026-09-12 ユーザー Go（api.md の P4 分割案）
scope_level: program
pdca_class: S1
pdca_eligible: true
created: 2026-09-12
updated: 2026-09-12
related_design: docs/design/programs/api.md
related_requirements: docs/design/product/charter.md   # §11 着手順 2 の前段。API 固有要件は api.md §1
related_review: docs/reviews/2026-09-12-renderer-cli-p6-review.md
promoted_from: ""
parent_hierarchy:
  product: docs/design/product/charter.md
  element: docs/design/elements/ir-type-vocabulary.md
  system: ""
  framework: ""
---

# pipeline-and-cli

## Goal

[api.md](../../../docs/design/programs/api.md) §3.1 の `entex.pipeline`（`render_ir()` / `prepare()` / `RenderResult`）を実装し、CLI `entex render` をその上に乗せ替える。API（plan `api-render`）が HTTP の皮だけで済む状態を作る。あわせて P6 レビューの W1（ジョブ名）・W2（テンプレ欠落）・S1（renderer.md IF 表）・S3（`TEXINPUTS`）を Act として片付ける。TeX 非依存なので `make test` で完了判定できる。

## Scope hierarchy（確定済み上位）

| Level | Path | Status |
|-------|------|--------|
| H0 product | docs/design/product/charter.md | draft（P0 ゲート Go 済み） |
| H1 element | docs/design/elements/ir-type-vocabulary.md | draft |
| H2 system | — | — |
| H3 framework | charter §7（FastAPI / Typer / pydantic）で確定済み | agreed |
| H4 program | docs/design/programs/api.md → この plan · docs/design/programs/renderer.md（変更対象の既存設計） | this plan |
| H5 algorithm | — | — |

## Scope

### In scope

- `src/entex/pipeline.py`: `RenderResult`（`doc_type` / `schema_version` / `job_name` / `out_dir` / `tex_path` / `pdf_path`）、`prepare(raw, packages_dir) -> PreparedIR`（`load_and_validate` + `apply_derived`）、`render_ir(raw, packages_dir, out_dir, *, job_name="document", tex_only=False, timeout=None) -> RenderResult`
- ジョブ名の規則を `pipeline` が持つ（W1）: `^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$` に合わない `job_name` は `ValueError`（呼び出し側のプログラムミス）。CLI は JSON の stem を **正規化** して渡す（規則に合わない文字を `-` に置換し、それでも合わなければ `document`）。`renderer.render()` が latexmk に渡す引数は `./<job>.tex` と前置する
- `packages.load_package()` で `template.tex.j2` の存在を検査し、無ければ `PackageError`（W2）。`renderer.build_tex()` の同じ検査は残してよいが到達しなくなる。`packages.py` の docstring を実装に合わせる
- `renderer.render()` の `TEXINPUTS` を常に末尾 `os.pathsep` 付きにする（S3）
- `src/entex/cli.py`: `render` コマンドの 3 段直書きを `pipeline.render_ir()` 呼び出しに置き換える。終了コード 0/1/2/3・オプション・出力（PDF パス / `.tex` パス）は変えない
- `docs/design/programs/renderer.md`: 公開 IF 表と図を実装に追従（`ir/schema.py` / `ir/validate.py` / `pipeline.py` を反映、`escape_content`、`render(content, package, out_dir, *, job_name, timeout)`）。`status` は変えない（S1）
- テスト: `tests/test_pipeline.py`（新規）、`tests/test_cli.py`・`tests/test_renderer.py`・`tests/test_ir_loader.py` の期待値更新

### Out of scope

- FastAPI のルート・Problem Details・設定（plan `api-render`）
- `prepare()` を CLI から使う口（`entex validate` のようなコマンド）— 着手順 4 で UI が要るときに判断
- S2（`pattern` の部分一致 / 全体一致）— 語彙文書側の 1 行決定。別途 `doc-record` で扱う
- 出力ディレクトリ名の変更（`out/render/<stem>/` はそのまま。正規化はジョブ名だけ）

## Acceptance criteria（S1: ≤5 推奨）

- [x] AC1: `entex.pipeline.render_ir()` / `prepare()` / `RenderResult` が api.md §3.1 のシグネチャで存在し、`cli.py` は `load_and_validate` / `apply_derived` / `renderer.render` を直接 import しない（`pipeline` 経由のみ）。既存テストは W1 / W2 に関わる期待値の更新以外は変更なしで通る — `tests/test_pipeline.py`、`rg` による import 検査をテスト化 → `tests/test_pipeline.py::test_cli_goes_through_the_pipeline_only`
- [x] AC2 (W1): `render_ir(job_name="-bad")` / `"a b"` / `"x%y"` は `ValueError`。CLI で `-dash.json` / `pct%hash#.json` / `報告 8月.json` を `--tex-only` で処理すると `.tex` が正規化された名前（`dash.tex` / `pct-hash-.tex` 相当、または `document.tex`）で出て終了コード 0。TeX 環境では同 3 件から PDF が出る — `tests/test_cli.py`（ホスト）・`@requires_tex` 1 件 → 実際の正規化結果は `dash.tex` / `pct-hash.tex` / `8.tex`（末尾の `-` は落とす）。`test_render_tex_only_normalizes_odd_filenames` / `test_render_odd_filenames_produce_pdf`（TeX あり環境で 4 件 pass）
- [x] AC3 (W2): `template.tex.j2` を欠いたパッケージは `load_package()` が `PackageError`、CLI は終了コード 3 と日本語文。`tests/test_renderer.py::test_missing_template_is_a_render_error` は `PackageError` 期待に書き換える → `test_missing_template_is_a_package_error`（renderer）・`test_render_missing_template_is_a_package_error`（cli、出力ディレクトリを作らないことも確認）
- [x] AC4 (S1 / S3): renderer.md の IF 表・図が実装と一致（表の関数名・引数を `src/entex/` の実シグネチャと突き合わせる）。`TEXINPUTS` が既に設定されている環境でも既定の探索パスが残る（`test_texinputs_keeps_default_path`）→ renderer.md の図・IF 表・エラー分類表を更新（`status` は据え置き）。`test_texinputs_keeps_default_path` + `test_tex_filename_is_passed_with_dot_slash`
- [x] AC5: `make lint` / `make test` 通過。CLI の利用者向け出力（成功時の PDF パス、失敗時の日本語文と終了コード）が変わっていないことを既存の `tests/test_cli.py` で確認。`.tex` の決定性テスト（`test_build_tex_is_deterministic`）を `render_ir(tex_only=True)` 経由でも通す → 168 passed（TeX ありホスト、skip 0）。`test_render_ir_tex_is_deterministic`

## Dependencies

- plan `render-and-cli`・`ir-validate-and-derive`（Check pass 済み）
- P6 レビュー `docs/reviews/2026-09-12-renderer-cli-p6-review.md`（W1 / W2 / S1 / S3 の根拠）

## Facts

- W1 の再現: `-dash.json` → latexmk がオプションと解釈、`pct%hash#.json` → "Filename contains character not allowed for TeX file"（レビュー時に実機確認）
- `renderer.render()` は `tex_path.name` を latexmk に渡している（`src/entex/renderer.py:181`）
- `load_package()` は `schema.json` の存在と内容だけを見る（`src/entex/packages.py:63-92`）

## Assumptions

- 出力ディレクトリ名に利用者由来の文字が残っても問題ない（ファイルシステムの制約は OS 側）
- `prepare()` の戻り値は `ValidatedIR` に `content`（導出値込み）を足した小さなデータクラスで足りる。pydantic 化はしない

## Open questions

- ~~CLI の PDF ファイル名を stem 正規化後の名前にするか、常に `document.pdf` にするか。**推奨**: 正規化後の名前（利用者が保存名を見てファイルを見分けられる）。合わなければ `document`~~ → **P5 で推奨どおり実装**（`normalize_job_name`: 不許可文字の連なりを `-` 1 つに、先頭末尾の `-`/`_` を落とし、64 文字で切り、空なら `document`）。README に例を記載

## Agent recommendations（計画時）

| 案 | 概要 | 推奨度 |
|----|------|--------|
| 1 | W1 / W2 を先に小パッチ PR で入れ、`pipeline` は別 PR | △ — ジョブ名の規則の所有者が 2 回動く |
| 2 | `pipeline` 導入と同じ PR で W1 / W2 / S1 / S3 を片付ける | ✓ — 規則の置き場が最初から `pipeline`。差分は 4 ファイル + テスト |

**推奨**: 案2（api.md §5 の 6 と同じ）。

## User thinking（推敲）

> 2026-09-12: 「2. Go」— api.md の P4 分割案（pipeline-and-cli → api-render）を承認。

## Progress assessments

| Date | Verdict | Summary |
|------|---------|---------|
| 2026-09-12 | on_track | plan 記録直後。P5 着手はユーザー指示待ち |
| 2026-09-12 | on_track | Do 完了。AC1–AC5 すべて検証済み（168 tests, lint pass）。Check（P6 レビュー）待ち |

## PDCA log

| Date | Phase | Note |
|------|-------|------|
| 2026-09-12 | Plan | api.md §5 の分割案どおり起票。W1 / W2 / S1 / S3 を Act としてここに吸収 |
| 2026-09-12 | Do | TDD（Red: `tests/test_pipeline.py` → Green → Refactor）。`src/entex/pipeline.py` 新規（`JOB_NAME_RE` / `DEFAULT_JOB_NAME` / `normalize_job_name` / `PreparedIR` / `RenderResult` / `prepare` / `render_ir`）。`cli.py` は `pipeline` 経由のみ（ジョブ名は `normalize_job_name(stem)`、出力ディレクトリは元の stem）。`packages.load_package()` に `template.tex.j2` 存在検査（W2）。`renderer.render()` は latexmk 引数を `./<job>.tex`、`TEXINPUTS` を必ず区切りで終端（W1 / S3）。`build_tex` の欠落検査は安全網として残す（`test_build_tex_still_guards_against_a_vanished_template`）。設計との差: AC2 の例示 `pct-hash-.tex` は末尾 `-` を落とし `pct-hash.tex` に（規則 `JOB_NAME_RE` は満たすので許容範囲と判断）。renderer.md の図・IF 表・エラー分類表と README の CLI 節を追従。— files: src/entex/pipeline.py, src/entex/cli.py, src/entex/packages.py, src/entex/renderer.py, tests/test_pipeline.py, tests/test_cli.py, tests/test_renderer.py, docs/design/programs/renderer.md, README.md（commits d5675ab / 9f596ff / 8da1fd8 / 4fd5944 / 644edb0） |
