---
title: renderer — IR + doc-package から PDF を組み立てる
kind: design
phase: P3
scope_level: program
status: agreed
created: 2026-09-12
updated: 2026-09-12
parent_element: docs/design/elements/ir-type-vocabulary.md
parent_system: ""
related_requirements: docs/requirements/circle-monthly-report/要件.md
---

# renderer（H4）

親: [要件.md](../../requirements/circle-monthly-report/要件.md) / [ir-type-vocabulary.md](../elements/ir-type-vocabulary.md)

## 目的（どの H1/H2 のためか）

charter §8 の主要要素のうち `renderer` を対象にする。IR（検証済みの中間表現）と `doc-package`（`schema.json` + `template.tex.j2` + スタイル）から `.tex` を組み立て、`latexmk -lualatex` で PDF にする。要件.md の FR1–FR8・NFR1–2 を満たすことがゴール。

対象は着手順1（charter §11）: `entex render <json>` で1本通す。API化・2文書種目・UI・CSVはこの設計の範囲外（要件.md Out of scope）。

## 責務・境界

`renderer` が守る境界（charter §8）: **IR がどこから来たか（フォーム／CSV／DB）を知らない**。入力は「検証済みのenvelope + IR」のみを受け取る形にする。CLIが「JSONファイルを読む」役を持ち、`renderer` 本体は「パース済みのdict/pydanticモデル」を受け取る、という分離にする。

`renderer` は `packages/<slug>/` の中身（`schema.json` の型・属性、`template.tex.j2`）を読むが、**特定の文書種の知識をコードにハードコードしない**。文書種ごとの違いはすべて `packages/<slug>/` 側のファイルで表現される。

```
[ CLI: cli.py ]
      │ JSONファイルパスを受け取り、テキストとして読む
      ▼
[ ir/loader.py ]  envelope検証 → schema.json読み込み → pydanticモデルで型検証
      │ 検証済みモデル（またはエラーリスト）
      ▼
[ ir/derive.py ]  schema.jsonのexpr宣言を評価し、導出フィールドを埋める
      │ 導出値を含む完全なコンテキスト
      ▼
[ tex/escape.py ] text/rich_text の文字列値をTeX安全な形にエスケープ
      │ エスケープ済みコンテキスト
      ▼
[ renderer.py ]   template.tex.j2 に流し込み .tex を書き出し、latexmkを呼ぶ
      │ PDFパス（または RenderError）
      ▼
[ cli.py ]        結果（PDFパス／日本語エラー）を出力
```

`ir/loader.py` と `ir/derive.py` は **doc-packageの中身に依存するが、特定の文書種を知らない**（`schema.json` の内容だけを見る）。`tex/escape.py` は型にもdoc-packageにも依存しない純粋関数。`renderer.py` は `template.tex.j2` の存在とJinja2の呼び出し規約にのみ依存する。

## 公開インターフェース / API

段階1（CLI）でのモジュール間インターフェース（シグネチャは設計方針であり、実装時に確定させる）。

| モジュール | 主要関数 | 入力 | 出力 |
|---|---|---|---|
| `entex.ir.loader` | `load_and_validate(raw: dict, packages_dir: Path) -> ValidatedIR \| ValidationErrors` | envelope込みの生JSON（dict化済み） | 検証済みIR（pydanticモデル）、またはエラー一覧（FR1, FR2, FR3） |
| `entex.ir.derive` | `apply_derived(ir: ValidatedIR, schema: Schema) -> DerivedIR` | 検証済みIR、schema.jsonのexpr定義 | 導出フィールドを埋めた完全なコンテキスト（FR4） |
| `entex.tex.escape` | `escape_text(s: str) -> str` / `escape_context(ctx: DerivedIR) -> EscapedContext` | 生の文字列／コンテキスト全体 | TeX安全な文字列／コンテキスト（FR5） |
| `entex.renderer` | `render(ctx: EscapedContext, package_dir: Path, out_dir: Path) -> Path \| RenderError` | エスケープ済みコンテキスト、doc-packageのパス | 生成されたPDFのパス、または利用者向け日本語メッセージを持つ `RenderError`（FR6, FR7） |
| `entex.cli` | `render(json_path: Path)`（Typerコマンド） | JSONファイルパス | 標準出力にPDFパスまたは日本語エラー、終了コード（FR8） |

`ValidationErrors` / `RenderError` は例外ではなく明示的な戻り値（または専用の例外クラスだが利用者向けメッセージを属性に持つ）とし、CLI層・将来のAPI層（着手順2）の両方が同じ形でハンドリングできるようにする。これにより「利用者向けエラーにTeXログを出さない」（AGENTS.md）という要件を、レイヤーをまたいでも壊れない形で満たす。

## エラー分類とFR7の写像方針

4種類に分類し、それぞれ日本語メッセージのテンプレートを持つ。

| 分類 | 発生源 | 利用者向けメッセージの方針 |
|---|---|---|
| `EnvelopeError` | `ir/loader.py`（封筒不一致） | 「文書の種類または版が一致しません」＋期待値・実際値（FR1） |
| `ValidationError`（複数件） | `ir/loader.py`（型・属性違反） | フィールドの `label`（日本語）を使い、`packages/circle-monthly-report/README.md` の異常系表にある文言パターンに準拠。**1件ずつ直させず、まとめて返す**（FR2） |
| `DerivationError` | `ir/derive.py`（循環参照など） | パッケージ作成者向け（利用者には通常出ない。テンプレート作者向けの内部エラーとして扱う） |
| `RenderError` | `renderer.py`（latexmk失敗） | 汎用メッセージ「PDFの生成に失敗しました。入力内容をご確認のうえ、解決しない場合は管理者へお問い合わせください」＋ latexmkの生ログは `out/<job>/latexmk.log` 相当のサーバ側ログにのみ書く。TeXのエラー文字列（`! `, `LaTeX Error` 等）を標準出力・戻り値に含めないことをテストで担保する（FR7） |

`ValidationError` と `EnvelopeError` はスキーマ検証の時点で原因が特定できるため日本語文言を機械的に組み立てられるが、`RenderError` はlatexmkの出力を解析して原因別メッセージに分岐させる価値が低い（TeXのエラーは組版の詳細に依存し尽くせない）ため、当面は汎用メッセージ1種に留める。原因別メッセージが必要になった時点で拡張する。

## 仮レイアウト方針（`template.tex.j2` が実物入手前でも書ける根拠）

要件.md Open questionsの1つ「仮レイアウトの方針」を解消する。

- 用紙: A4、`ltjsarticle`（luatexja-standard相当）をベースにする
- 構成順は `schema.json` の `fields` 宣言順に素直に対応させる: 団体情報（`organization`/`report_month`/`submitted_on`/`representative`/`author`/`advisor`）→ 会員数（`members`）→ 活動概要（`summary`）→ 活動実績（`activities`、`tabular`）→ 会計（`balance_carried`/`finance`/`income_total`/`expense_total`/`balance`）→ 次月予定（`next_month_plan`）→ 特記事項（`incident`/`remarks`/`audited`）
- 表（`row_list`）は `max_items` 行分の枠を確保する固定レイアウトにはせず、実際の行数だけ描画する可変長 `tabular`（罫線は最小限）とする。**行数が変わってもレイアウトが大きく崩れない**ことを優先し、装飾は最小限にする
- フォント・余白・罫線の具体値は `packages/circle-monthly-report/` 側のスタイルファイルに置く（AGENTS.md「体裁に関わる値は`src/entex/`ではなくdoc-package側に置く」）。`src/entex/renderer.py` はテンプレートパスとJinja2呼び出しの規約（変数名の受け渡し）のみを持つ
- 実物入手後の手戻りは `packages/circle-monthly-report/` 内（`schema.json`のフィールド名・`template.tex.j2`のレイアウト）に閉じる想定。`renderer` 本体のインターフェース（上表）は変えずに済む見込み

## 依存（H3 フレームワーク）

charter §7 で既に確定済みのため、この設計で新規のフレームワーク選定は発生しない。

| 用途 | 選定 | 備考 |
|---|---|---|
| IRの型検証 | pydantic | `schema.json`（案1）からモデルを動的に構築、またはフィールド定義に対応する検証関数を書く（どちらにするかはP4実装計画で判断） |
| テンプレート | Jinja2（`.tex.j2`） | 変数はエスケープ済みの値のみを渡す（テンプレート内で生の値を書き込まない。AGENTS.md） |
| CLI | Typer | 既存の `src/entex/cli.py` に `render` コマンドを追加 |
| 組版 | LuaLaTeX + luatexja、`latexmk` 経由 | コンテナ内実行のみ（`make docker-*`） |

## エージェント提案

| 案 | 概要 | 推奨 |
|----|------|------|
| 1 | `renderer.py` に読み込み・検証・導出計算・エスケープ・テンプレ組み立て・latexmk呼び出しを1本で書く | — |
| 2 | 上記「責務・境界」の5モジュールに分割する | ✓ |

**推奨**: 案2。理由は要件.md に記載済み（charter §8 の境界をコード構造に反映し、2文書種目でのパッケージ構造妥当性判定に備える）。

### P4 planの分割案（要件.md Open questionsの解消）

1 plan = 1 PDCA サイクルの原則（PROJECT_LIFECYCLE.md）に従い、FR1–FR8 を2つのplanに分ける。

| Plan（仮称） | scope_level | 含むFR | 内容 |
|---|---|---|---|
| `ir-validate-and-derive` | H5（algorithm） | FR1, FR2, FR3, FR4 | `ir/loader.py`・`ir/derive.py`。envelope検証・型検証・導出値拒否・導出値計算。`packages/circle-monthly-report/examples/` 全12件で検証可能、LaTeX非依存なのでコンテナ無しでもテストできる |
| `render-and-cli` | H4（program） | FR5, FR6, FR7, FR8 | `tex/escape.py`・`renderer.py`・`cli.py`。エスケープ・テンプレ組み立て・latexmk呼び出し・CLIコマンド。`make docker-test` 相当が必要 |

先に `ir-validate-and-derive` を実装・完了させると、LaTeX環境が無くても（`make test`、TeX非依存）進捗を確認できる。`render-and-cli` はその後、Docker環境（`make docker-test`）で検証する。NFR1（10秒以内）・NFR2（決定性）は `render-and-cli` 側の受け入れ基準に含める。

## ユーザー思考

>

## Open questions

- ~~`schema.json` からpydanticモデルを動的生成する方式と、型ごとに検証関数を書く方式のどちらにするか~~ → **決定（P4, 2026-09-12）**: `schema.json` 自体・封筒・`expr` は pydantic の静的モデル（`ir/schema.py`）、`content` は型ごとの検証関数（`ir/validate.py`）。理由は plan `ir-validate-and-derive` の Agent recommendations
- ~~`template.tex.j2` の可変長 `tabular` を luatexja 環境でどう組むか~~ → **当面の実装（P5）**: `tabularx` + `booktabs`、`longtable` は使わず改ページを許容。上限行数（活動 10・会計 20）で A4 2 枚に収まることを確認済み。実物入手後に再判定
- `RenderError` の汎用メッセージ1種で当面足りるか、latexmkのエラーパターン別メッセージが必要になるかは、実物のテスト運用で判断する

## 次

- [x] P3 ゲート → [`.agents/plans/algorithms/ir-validate-and-derive.md`](../../../.agents/plans/algorithms/ir-validate-and-derive.md) と [`.agents/plans/programs/render-and-cli.md`](../../../.agents/plans/programs/render-and-cli.md)（2026-09-12、ユーザー指示「P3の設計に従って実装に入ってください」を PM 確認として記録）
- [x] P6 レビュー（`review-conduct`）→ [docs/reviews/2026-09-12-renderer-cli-p6-review.md](../../reviews/2026-09-12-renderer-cli-p6-review.md)（pass。Warning W1/W2 と本表の IF 追従 S1 は Act で扱う）
- [ ] 実物の Word 版報告書を入手して `packages/circle-monthly-report/` を直す
