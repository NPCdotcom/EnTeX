# circle-monthly-report — サークル月次活動報告書

最初の文書種（charter §5 の MVP）。大学サークルが学生課へ毎月出す活動報告書を題材にしている。

**状態: スキーマ・IR 例・仮レイアウトのテンプレートとスタイルが揃い、`entex render` で PDF が出る（着手順 1）。**
実物の Word 版報告書はまだ確認していないので、項目構成もレイアウトも一般的なサークル報告書の形に沿った **仮定** である（[ir-type-vocabulary.md](../../docs/design/elements/ir-type-vocabulary.md) の Assumptions、[renderer.md](../../docs/design/programs/renderer.md) の仮レイアウト方針）。

## 中身

| パス | 内容 |
|---|---|
| `schema.json` | 入力の形。型の語彙は [ir-type-vocabulary.md](../../docs/design/elements/ir-type-vocabulary.md) §1、書式は同 §8 の案 1（仮） |
| `template.tex.j2` | TeX 雛形（Jinja2）。区切りは `\VAR{…}`（値）・`\BLOCK{…}`（制御）・行頭 `%#`（コメント）。渡される変数は `doc`（利用者の値。`text` / `rich_text` はエスケープ済み）と `schema`（`label`・enum の表示名） |
| `style/circle-monthly-report.sty` | 体裁（余白・罫線・表の列幅・見出し）。**体裁の値はここに置き、`src/entex/` には置かない** |
| `examples/valid/` | 検証を通り、PDF が出るべき IR。運用で起こる場面ごとに 1 件 |
| `examples/invalid/` | 検証で **弾かれるべき** IR。`tests/test_ir_loader.py` の素材 |

```bash
# コンテナ内で
entex render packages/circle-monthly-report/examples/valid/01-typical.json
# → out/render/01-typical/01-typical.pdf
```

テンプレートで使える整形フィルタ（`src/entex/renderer.py` が提供。どれを使うかはテンプレートが選ぶ）: `group_digits`（3 桁区切り）・`ja_month`（`2026年8月`）・`ja_date`（`2026年8月3日` / `with_year=false` で `8月3日`）。金額の負号（`△`）や「済 / 未」の表記はテンプレート内のマクロで決めている。

## スキーマが網羅している型と属性

`schema.json` は語彙の 11 型をすべて 1 回以上使い、フィールド属性も一通り含めている。語彙のどこが実際に使われるかを確かめるための構成で、実物に無い項目は後で削る。

| 型・属性 | 使っているフィールド |
|---|---|
| `text` + `max_length` | `organization` ほか |
| `text` + `pattern` | `representative.student_id` |
| `month` / `date` | `report_month` / `submitted_on`、各行の `date` |
| `integer`（既定 `minimum: 0`） | `members.*`、`activities[].participants` |
| `integer` + `default` | `members.joined` / `members.left`（省略時 0） |
| `money`（符号あり） | `balance_carried`（赤字で負） |
| `money` + `minimum: 0` | `finance[].amount` |
| `enum`（2 値） | `finance[].category` |
| `enum`（3 値。boolean の代わり） | `incident` |
| `boolean` | `audited` |
| `object` | `representative` / `author` / `members` |
| `row_list` + `min_items` / `max_items` | `activities`（0–10 行）/ `finance`（0–20 行） |
| `list<text>` | `next_month_plan`（1–8 件） |
| `list<enum>`（複数選択） | `facilities_used` |
| `rich_text`（必須） | `summary` |
| `rich_text`（任意） | `remarks` |
| `required: false` | `advisor` / `facilities_used` / `remarks` / `members.joined` / `members.left` |
| `derived` + `count` | `activity_count` |
| `derived` + `sum` | `participants_total` |
| `derived` + `sum` + `where` | `income_total` / `expense_total` |
| `derived` + `add` / `sub`（入れ子） | `balance` |

## 正常系（`examples/valid/`）

| ファイル | 場面 | 確かめたいこと |
|---|---|---|
| `01-typical.json` | 合宿のある通常月 | 全フィールドが埋まった標準形。導出値: 活動 5 回・延べ 77 人・収入 138,000・支出 131,400・残高 19,400 |
| `02-minimal.json` | 試験期間で活動休止 | 任意フィールドを **キーごと省略**。`activities` / `finance` が空配列。導出値はすべて 0 か繰越そのまま（残高 5,400） |
| `03-deficit.json` | 機材修理で赤字 | 残高が負（19,400 + 54,000 − 78,200 = −4,800）。`incident: minor` |
| `04-max-rows.json` | 学園祭月 | `activities` 10 行・`next_month_plan` 8 件が **上限ちょうど**。前月繰越が負（−4,800）からの回復 |
| `05-fiscal-year-start.json` | 年度初月 | 繰越 0 と引継金の扱い。`facilities_used: ["none"]`。`audited: true` |
| `06-tex-special-chars.json` | TeX の特殊文字 | `& % $ # _ { } ~ ^ \ < >` と `'` を含む文字列が **検証を通り**、エスケープされて PDF に出ること（AGENTS.md「利用者の入力は必ずエスケープ」） |

## 異常系（`examples/invalid/`）

利用者に見せるメッセージは日本語で、TeX の語は出さない（charter §4）。ここに書いた文言は仮。

| ファイル | 仕込んだ誤り | 期待する検証結果 |
|---|---|---|
| `01-derived-key-in-input.json` | `income_total` / `balance` を入力に含めた | 拒否。「収入合計・残高は自動計算です。入力から外してください」 |
| `02-newline-in-text.json` | `organization` に改行 | 拒否。「団体名は1行で入力してください」 |
| `03-unknown-enum-and-negative-amount.json` | `category: "refund"`、`amount: -500` | 2 件とも拒否。「区分は 収入 / 支出 のいずれか」「金額は0以上」。返金は収入として書く運用 |
| `04-too-many-rows.json` | `activities` 11 行 | 拒否。「活動実績は10行までです」 |
| `05-null-and-unknown-key.json` | 任意項目に `null`、`next_month_plans` という未知キー | 拒否。「顧問・特記事項は未入力ならキーを省く」「next_month_plans は使えない項目です（next_month_plan の間違い？）」 |
| `06-envelope-mismatch.json` | `schema_version: 2`、`"2026-8"`、`2026-09-31`、学籍番号に小文字と `-`、`rich_text` に `heading`、`audited` が文字列、`next_month_plan` が空 | 封筒の版で **先に** 拒否。版が合っていれば残り 6 件をまとめて報告 |

検証エラーは **見つかった分をまとめて返す**（1 件ずつ直させない）。ただし封筒（`doc_type` / `schema_version`）の不一致は中身を見る前に止める。

## 未確認・仮定

- 学生課の実際の様式（項目名・欄の順序・行数）。**実物を見て `schema.json` を直す**
- `activities` の上限 10 行・`finance` の 20 行は A4 1 枚に収まる見込みで置いた数。テンプレートを書いた時点で決め直す
- `student_id` の形式 `^[A-Z0-9]+$` は仮
