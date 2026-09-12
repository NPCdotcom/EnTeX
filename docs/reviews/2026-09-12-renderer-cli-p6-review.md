---
title: P6 レビュー — renderer / CLI 実装（PR #8）
kind: review
phase: P6
scope_level: H4
status: agreed
created: 2026-09-12
updated: 2026-09-12
reviewed_commit: 7955490   # Merge pull request #8 (main)
related_plans:
  - .agents/plans/algorithms/ir-validate-and-derive.md
  - .agents/plans/programs/render-and-cli.md
related_design: docs/design/programs/renderer.md
related_requirements: docs/requirements/circle-monthly-report/要件.md
verdict: pass
---

# P6 レビュー — renderer / CLI 実装

対象: [PR #8](https://github.com/NPCdotcom/EnTeX/pull/8)（`2936dc9..7955490`、36 ファイル +2940/−49）。
plan `ir-validate-and-derive`（H5）と `render-and-cli`（H4）の Do 完了に対する Check。
手順は skill `review-conduct`（V-model RTM）に従う。

## 判定

**pass**（Critical なし・Warning 2 件・Suggestion 4 件）。
AC はすべて根拠あり。Warning は AC 違反ではなく、次の Act（小パッチ）で直す提案として残す。

| 項目 | 結果 |
|------|------|
| ローカル検査（本レビュー時、`main@7955490`） | `ruff check` 通過 · `pytest` 126 件通過（ホストに TeX Live あり） |
| CI（merge commit） | run 34665860832: lint/test 3.12 · 3.13 · tex smoke（Docker、pytest 込み）すべて success |
| 設計前提（AGENTS.md Design invariants） | 4 項目とも違反なし（下記 ST） |

## RTM（要件 ↔ 設計 ↔ plan AC ↔ テスト）

検証層: UAT = 要件.md の検証方法 · ST = renderer.md · IT = plan scope / モジュール IF · UT = 単体テスト。

| 要件 | 検証層 | 設計リンク | plan AC | 変更ファイル | テスト / 根拠 | 結果 |
|------|--------|------------|---------|--------------|---------------|------|
| FR1 封筒を先に検証、中身は見ない | UT/IT/UAT | renderer.md §エラー分類 `EnvelopeError` | ir-validate AC1 | `src/entex/ir/loader.py:51-81` | `tests/test_ir_loader.py:26` `test_envelope_mismatch_stops_before_content`（`06-envelope-mismatch.json`）· CLI 境界 `tests/test_cli.py:46` | pass |
| FR2 11 型で検証、エラーはまとめて返す | UT/IT/UAT | 同 `ValidationError（複数件）` | ir-validate AC2 | `src/entex/ir/validate.py`, `errors.py:45-54` | `tests/test_ir_loader.py:105` `test_two_errors_come_back_in_one_call`（`03-…json`）· `:91` valid 6 件 · `:100` invalid 6 件 | pass |
| FR3 derived キーの入力を拒否 | UT/UAT | ir-type-vocabulary.md §6.1 | ir-validate AC3 | `src/entex/ir/validate.py:69-78` | `tests/test_ir_loader.py:217` `test_derived_key_in_input_is_rejected`（`01-derived-key-in-input.json`） | pass |
| FR4 `expr` を宣言順に評価、循環は拒否 | UT/UAT | ir-type-vocabulary.md §4 決定A | ir-validate AC4 | `src/entex/ir/derive.py`, `ir/schema.py:216-270` | `tests/test_ir_derive.py:51` README 期待値（01/02/03/04/05）· `tests/test_ir_schema.py:50,59` 前方参照・自己参照が `PackageError` | pass |
| FR5 `text` / `rich_text` を TeX エスケープ | UT/IT/UAT | renderer.md §責務・境界 `tex/escape.py` | render-and-cli AC1 | `src/entex/tex/escape.py`, `renderer.py:78-87`（`build_tex` 内で必ず通す） | `tests/test_tex_escape.py:17,26,40` · `tests/test_renderer.py:67` `test_built_tex_has_no_unescaped_specials`（`06-tex-special-chars.json`） | pass |
| FR6 `.tex` 組み立て → `latexmk -lualatex` で PDF | UT/IT/ST/UAT | renderer.md §公開 IF `render()` | render-and-cli AC2 | `src/entex/renderer.py:122-208` | `tests/test_renderer.py:217` `test_valid_examples_render_to_pdf`（6 件、`@requires_tex`）· CI tex job で実行 | pass |
| FR7 latexmk 失敗時に TeX ログを利用者へ出さない | UT/IT/ST/UAT | renderer.md §エラー分類 `RenderError` | render-and-cli AC3 | `src/entex/errors.py:61-82`, `renderer.py:160-207`, `cli.py:148-150` | 偽 latexmk: `tests/test_renderer.py:183` · `tests/test_cli.py:94`（stdout / stderr に `TEX_VOCABULARY` なし、`latexmk.log` に原文）· 壊れたテンプレ: `tests/test_renderer.py:225` | pass |
| FR8 `entex render <json>` で一連実行 | IT/UAT | renderer.md §公開 IF `entex.cli` | render-and-cli AC2 | `src/entex/cli.py:83-154` | `tests/test_cli.py:124` `test_render_typical_prints_pdf_path`（exit 0・PDF パス出力）· `:134` 既定の出力先 | pass |
| NFR1 生成 10 秒以内 | ST | charter §6 | render-and-cli AC5 | — | `tests/test_renderer.py:239` `test_typical_render_finishes_within_budget`（実測 1.5–4 秒、ホスト） | pass（目安計測） |
| NFR2 同じ入力 → 同じ `.tex` | ST | charter §4 | render-and-cli AC4 | `src/entex/renderer.py:122-137` | `tests/test_renderer.py:117` `test_build_tex_is_deterministic`（valid 6 件） | pass（PDF バイナリは plan Out of scope） |

### トレーサビリティ判定

- Forward: 10 要件すべてに 1 つ以上の自動テストがある。
- Backward: PR の `src/` 変更はすべて FR/NFR または renderer.md の Fact に辿れる。plan 外の変更は `src/entex/ir/schema.py` と `ir/validate.py` の分離（renderer.md は `ir/loader.py` 1 本を想定）だが、PDCA Do 行に「境界は変えていない」と記録済みで、モジュール境界の追加分割であり scope 逸脱ではない。
- Orphan 要件: なし（要件.md In scope の 7 項目は FR1–FR8 で覆われている）。
- Orphan テスト: `tests/test_ir_loader.py:57` `test_unsafe_doc_type_never_touches_the_filesystem` は AC に無いが、`packages.py:64-66` の `../` 対策を守るテストで有益。警告ではなく維持。

### 四層カバレッジ（G10）

| 層 | 確認 | 状態 |
|----|------|------|
| UT | 実装モジュールごとに単体テストあり（`tests/test_ir_schema.py` / `test_ir_loader.py` / `test_ir_derive.py` / `test_tex_escape.py` / `test_renderer.py`）。126 件 | ✓ |
| IT | `load_and_validate → apply_derived → build_tex/render` の結合を `tests/test_renderer.py:42` `_content()` と `tests/test_cli.py` が通す。`schemas/ir/envelope.schema.json` と pydantic モデルの同期テスト（`tests/test_ir_loader.py:257`） | ✓ |
| ST | renderer.md の 5 モジュール構成・エラー 4 分類・「体裁値は doc-package 側」に一致。NFR1/NFR2 テストあり | ✓（差分は下記 spec gap） |
| UAT | 要件.md の検証方法（各 examples）をそのままテスト化。**ただし仮レイアウトの見た目は実物の Word 版様式が未入手のため受入未了**（要件.md Out of scope として明記済み） | ✓（レイアウト UAT は保留） |

### 設計前提の確認（ST）

| 前提 | 確認箇所 | 結果 |
|------|----------|------|
| `renderer` は IR の出どころを知らない | `loader.py:51` は dict のみ受け取る。ファイル読みは `cli.py:125` だけ | ✓ |
| 文書種追加で `src/entex/` を変えない | `src/entex/` に `circle-monthly-report` 固有の識別子なし（`rg` で確認）。型語彙は `ir/schema.py:15-33` の定数のみ | ✓（判定自体は 2 文書種目で行う） |
| 利用者は TeX を見ない | `RenderError.user_message` は汎用文 1 種（`errors.py:68-71`）。`detail` / `log_path` は CLI で出力しない（`cli.py:148-150`） | ✓ |
| 体裁値は doc-package 側 | 余白・罫線・フォント指定は `packages/circle-monthly-report/style/circle-monthly-report.sty` のみ | ✓ |

## 指摘

### Critical

なし。

### Warning

| # | 内容 | 場所 | 起源工程 | 提案 |
|---|------|------|----------|------|
| W1 | **JSON のファイル名がそのまま latexmk のジョブ名になる。** `job_name = json_path.stem` を `<job>.tex` として latexmk に渡すため、`-` で始まる名前（オプションと解釈）や `%` `#` を含む名前（latexmk が "character not allowed" で停止）では PDF が出ず、利用者には「入力内容をご確認ください」の汎用文が返る。実機確認: `-dash.json` → exit 2、`pct%hash#.json` → exit 2、`報告 8月.json` → 成功 | `src/entex/cli.py:120,143` · `src/entex/renderer.py:166,181` | P5（実装） | ジョブ名を固定（`document`）または英数字とハイフンに正規化し、利用者由来の名前は出力ディレクトリ名にだけ使う。latexmk の引数は `./` を前置する。パッチ規模: 2 ファイル・10 行以内 + テスト 1 件 |
| W2 | **`template.tex.j2` 欠落が `RenderError`（exit 2、運用者向け）になる。** plan は「パッケージ不備は 3」と定めており、`packages.py` の docstring も「`template.tex.j2` / `style/` の存在を読む」と書くが、`load_package()` はテンプレートの存在を確認していない。現状は `test_missing_template_is_a_render_error` がこの挙動を固定している | `src/entex/renderer.py:128-131` · `src/entex/packages.py:1-5,63-92` | P5（実装） | `load_package()` でテンプレートの存在を検査して `PackageError` にし、テストの期待を `PackageError` に変える。パッチ規模: 2 ファイル + テスト 1 件 |

### Suggestion

| # | 内容 | 場所 | 提案 |
|---|------|------|------|
| S1 | renderer.md の公開 IF 表は設計時の仮シグネチャ（`render(ctx: EscapedContext, package_dir: Path, out_dir)`、`escape_context`）のまま。実装は `render(content, package: DocPackage, out_dir, *, job_name, timeout)`・`escape_content`・エスケープは `build_tex` 内部。設計文書側が「実装時に確定」と明記しているので違反ではないが、API 化（着手順 2）の設計が参照する前に揃えたい | `docs/design/programs/renderer.md:55-61` | Act で IF 表を実装に合わせて更新（`ir/schema.py` / `ir/validate.py` の追加も図に反映） |
| S2 | `pattern` は `re.search`（部分一致）で判定している。ir-type-vocabulary.md §3 は「追加の正規表現」とだけ書き、全体一致か部分一致かを決めていない。パッケージ作者がアンカーを忘れると素通りする | `src/entex/ir/validate.py:237` | `re.fullmatch` にするか、語彙文書に「部分一致。全体一致にはアンカーを書く」と明記する（どちらかに決めて 1 行足す） |
| S3 | `TEXINPUTS` の既存値に末尾区切りが無い場合、TeX の既定探索パスが落ちる（未設定時は末尾 `:` が残るので問題ない） | `src/entex/renderer.py:185-188` | 常に末尾に `os.pathsep` を付ける |
| S4 | 検証・生成の 3 段（`load_and_validate → apply_derived → render`）を CLI が直接並べている。API 化で同じ並びをもう一度書くことになる | `src/entex/cli.py:135-143` | API 設計（着手順 2）で共通パイプライン関数を導入し、CLI もそれを呼ぶ形に寄せる。本レビューの範囲では変更しない |

## Spec gap / Act への提案

- **S1**: renderer.md IF 表の追従（設計文書の更新。`status` は変えない）。
- **W1 / W2**: `patch-reference` の小パッチ範囲。API 設計より先に入れるのが安全（API 側はジョブ名を自前で決めるので W1 は API では再現しないが、CLI 利用者には残る）。
- Recycle 不要。工程の巻き戻し（P3 / P4）は要らない。
- Outcome check（任意）: 利用者が口頭説明なしで PDF を出せるか（charter §6）は、実物様式の入手後に UAT として実施。現時点では測れない。

## 次のアクション

1. plan 2 本の PDCA log に Check 行を追加（本レビューへのポインタ）。
2. `docs/project-state.yaml` を P6 に進め、Act 候補（W1 / W2 / S1）を `open_blockers` ではなく `gate_status.proposal` に載せる（ブロッカーではない）。
3. API 化（charter §11 着手順 2）の P3 設計に S4 を織り込む。
