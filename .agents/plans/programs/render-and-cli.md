---
title: render-and-cli — エスケープ・テンプレ組み立て・latexmk・CLI
kind: plan
status: agreed   # Do 完了（2026-09-12）。P6 review 待ち
scope_level: program
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

# render-and-cli

## Goal

`renderer`（H4: [renderer.md](../../../docs/design/programs/renderer.md)）の後段、`tex/escape.py`・`renderer.py`・`cli.py` の `render` コマンドと、最初の doc-package の `template.tex.j2` を実装し、要件.md の FR5–FR8・NFR1–2 を満たす。charter §11 着手順 1「CLI で 1 本通す」の完了条件。

## Scope hierarchy（確定済み上位）

| Level | Path | Status |
|-------|------|--------|
| H0 product | docs/design/product/charter.md | draft（P0 ゲート Go 済み） |
| H1 element | docs/design/elements/ir-type-vocabulary.md | draft |
| H2 system | — | — |
| H3 framework | charter §7（Jinja2 / Typer / LuaLaTeX+luatexja / latexmk）で確定済み | agreed |
| H4 program | docs/design/programs/renderer.md → この plan | this plan |
| H5 algorithm | .agents/plans/algorithms/ir-validate-and-derive.md | 前提（先に完了） |

## Scope

### In scope

- `src/entex/tex/escape.py`: `escape_text()`（純粋関数）と、スキーマの型を見て `text` / `rich_text` の値だけをエスケープする `escape_content()`
- `src/entex/renderer.py`: Jinja2（TeX 向けの区切り `\VAR{}` / `\BLOCK{}` / 行頭 `%%`）で `template.tex.j2` から `.tex` を組み立て（`build_tex()`）、`latexmk -lualatex` で PDF にする（`render()`）。失敗は `RenderError`（汎用の日本語文）にし、latexmk の出力は `out/<job>/latexmk.log` にだけ残す
- 体裁に依存しない整形フィルタ（3 桁区切り・`YYYY年M月`・`YYYY年M月D日`）を `src/entex/` 側で提供し、どれを使うかはテンプレートが選ぶ（ir-type-vocabulary.md §5）
- `packages/circle-monthly-report/template.tex.j2` と `style/circle-monthly-report.sty`（仮レイアウト。renderer.md の方針: `ltjsarticle`、宣言順、可変長 `tabular`、装飾最小）
- `src/entex/cli.py`: `entex render <json> [--out DIR] [--packages-dir DIR]`。成功で PDF パスを標準出力・終了コード 0、入力エラーは 1、生成失敗は 2、パッケージ不備は 3
- テスト: エスケープ（FR5）、`.tex` の決定性（NFR2）、偽の `latexmk` を PATH に置いた失敗経路で TeX 語彙が漏れないこと（FR7、ホストで実行可）、Docker でのみ走る PDF 生成（FR6/FR8）と所要時間の目安（NFR1）

### Out of scope

- API 化（着手順 2）・2 文書種目・UI・CSV
- latexmk のエラーパターン別メッセージ（汎用 1 種で開始。renderer.md）
- PDF バイナリの完全一致（NFR2 は `.tex` の一致で判定。PDF のメタデータ時刻は対象外）
- 実物の様式に合わせたレイアウト調整（Word 版入手後、`packages/circle-monthly-report/` 内に閉じて行う）

## Acceptance criteria（S1: ≤5 推奨）

- [x] AC1 (FR5): `& % $ # _ { } ~ ^ \ < > '` を含む `examples/valid/06-tex-special-chars.json` から組み立てた `.tex` に、未エスケープの特殊文字が本文として残らない — `tests/test_tex_escape.py`、`tests/test_renderer.py::test_built_tex_has_no_unescaped_specials`
- [x] AC2 (FR6/FR8): `entex render packages/circle-monthly-report/examples/valid/01-typical.json` が終了コード 0 で PDF パスを出力し、そのパスに PDF がある。`examples/valid/` 6 件すべてで PDF が出る — `test_valid_examples_render_to_pdf`（6 件）/ `tests/test_cli.py::test_render_typical_prints_pdf_path`（TeX 環境で実行済み。Docker ではなくホストに同じ apt パッケージを入れて確認。CI の tex ジョブでも走る）
- [x] AC3 (FR7): latexmk が失敗したとき、CLI の標準出力・標準エラー・`RenderError.user_message` のいずれにも TeX 語彙が含まれず、原文は `out/.../latexmk.log` に残る — 偽 latexmk による `test_latexmk_failure_keeps_tex_log_server_side` / `test_render_failure_hides_tex_log_from_user`（ホストで実行）、壊れたテンプレートによる `test_broken_template_fails_without_leaking_tex`（TeX 環境）
- [x] AC4 (NFR2): 同じ IR から 2 回組み立てた `.tex` が一致する — `test_build_tex_is_deterministic`（6 件）
- [x] AC5 (NFR1): `01-typical` の生成（2 回目）が 10 秒以内 — `test_typical_render_finishes_within_budget`（実測 1.5–4 秒）。ruff / pytest（TeX あり 126 件・なし 115 件+11 skip）通過。`make docker-test` / `make tex-smoke` は Docker が無い環境のため未実行（CI の tex ジョブで代替）

## Dependencies

- plan `ir-validate-and-derive`（検証済み・導出済みの content を受け取る）
- Docker イメージ `entex-dev`（`texlive-latex-recommended` に `geometry` / `booktabs` / `array` が含まれること — 実装時に `kpsewhich` で確認）

## Facts

- renderer.md: `RenderError` は汎用メッセージ 1 種、生ログはサーバ側のみ。体裁値は `src/entex/` に置かない
- AGENTS.md: 利用者の入力は必ずエスケープを通す。テンプレートに生の値を書き込まない

## Assumptions

- Debian の `texlive-latex-recommended` で `geometry` / `booktabs` / `tabularx` が使える
- 活動実績 10 行・会計明細 20 行は A4 1〜2 枚に収まる（`longtable` は使わず改ページを許容）

## Open questions

- 可変長 `tabular` で 1 ページを超えたときの見え方（`longtable` の要否）は実物入手後に判断
- PDF レベルの決定性（`SOURCE_DATE_EPOCH`）を入れるか。NFR2 を `.tex` で判定している間は保留

## Agent recommendations（計画時）

| 案 | 概要 | 推奨度 |
|----|------|--------|
| 1 | Jinja2 の既定区切り `{{ }}` / `{% %}` のまま TeX テンプレートを書く | △ — `}}` が TeX の閉じ括弧と衝突しやすく、テンプレート作者が読みづらい |
| 2 | TeX 向け区切り（`\VAR{…}` / `\BLOCK{…}` / 行頭 `%%` / `%#` コメント）+ `StrictUndefined` | ✓ — TeX として読める見た目。未定義変数はテンプレート作者のミスとして組み立て時点で落とす |

**推奨**: 案2。エスケープは Jinja2 の autoescape（HTML 用）ではなく、テンプレートへ渡す前に `escape_content()` で済ませる。

## User thinking（推敲）

> 2026-09-12: ユーザー指示「P3の設計に従って実装に入ってください」を PM 確認とみなし `status: agreed` とした。

## Progress assessments

| Date | Verdict | Summary |
|------|---------|---------|
| 2026-09-12 | on_track | plan 記録直後。`ir-validate-and-derive` 完了後に着手 |
| 2026-09-12 | on_track | Do 完了。AC1–AC5 テストで担保。残: Docker での `make docker-test` 実行（CI）、P6 レビュー、実物様式に合わせたレイアウト調整 |

## PDCA log

| Date | Phase | Note |
|------|-------|------|
| 2026-09-12 | Plan | renderer.md の分割案どおり起票。区切りは案2 |
| 2026-09-12 | Do | 実装: `src/entex/tex/escape.py`・`renderer.py`（`build_tex` / `render`、フィルタ 3 種、`\VAR{}` `\BLOCK{}` `%#` 区切り、`StrictUndefined`）・`cli.py render`（`--out` / `--packages-dir` / `--tex-only`、終了コード 0/1/2/3）、`packages/circle-monthly-report/template.tex.j2` と `style/circle-monthly-report.sty`。設計からの差分: エスケープは `renderer.build_tex` の内部で必ず通す（呼び出し側が忘れられない形）。テンプレートへ渡す dict は `SimpleNamespace` に変換（Jinja2 で `x.items` が dict のメソッドに解決される罠を避ける）。生成 PDF は目視確認（1〜2 ページ、特殊文字が正しく出る、負の残高は △ 表記） |
