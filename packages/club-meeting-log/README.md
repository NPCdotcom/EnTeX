# club-meeting-log — 部会ログ

最初の文書種（charter §5 の MVP）。情報技術研究部が部会ごとに Notion で書いている記録を、同じ体裁の PDF にする。要求は [docs/requirements/club-meeting-log/要求.md](../../docs/requirements/club-meeting-log/要求.md)、経緯は [ADR-0001](../../docs/adr/0001-first-doc-type-pivot-to-meeting-log.md)。

> **状態: `schema.json` / `template.tex.j2` / `style/` / `examples/` は揃っており、`src/entex/` の `document` 型実装（[issue #30](https://github.com/NPCdotcom/EnTeX/issues/30)）で PDF が出る。**
> 画像ありの例（`06-with-images.json`）は `image` の `src` が何を指すかが未決のため、MVP では画像なしの過去ログを対象にする（charter §5・§11 Open）。

差し替え前の [`circle-monthly-report/`](../circle-monthly-report/README.md) は上書きせずに残してある。型語彙を一通り使う参考資料として価値があり、実物に基づかないので charter §6 の合否判定の材料にはならない。

## 中身

| パス | 内容 |
|---|---|
| `schema.json` | 入力の形。型の語彙は [ir-type-vocabulary.md](../../docs/design/elements/ir-type-vocabulary.md) §1・§2.8、書式は同 §8 の案1 |
| `template.tex.j2` | TeX 雛形（Jinja2）。区切りは `\VAR{…}`（値）・`\BLOCK{…}`（制御）・行頭 `%#`（コメント） |
| `style/club-meeting-log.sty` | 体裁（余白・見出し・箇条書き・引用・コード・画像・リンクの見せ方）。**団体名の定数もここ**（charter §5.2） |
| `examples/valid/` | 検証を通り、PDF が出るべき IR |
| `examples/invalid/` | 検証で **弾かれるべき** IR。`document` の検証を実装するときのテスト材料 |

## `schema.json` のフィールド

4つしかない。月次報告書と違って**本文が主体**で、メタ情報は3つだけである（実測。[issue #14](https://github.com/NPCdotcom/EnTeX/issues/14)）。

| フィールド | 型 | 必須 | 取り方 |
|---|---|---|---|
| `meeting_date` | `date` | ○ | Notion のプロパティ `開催日`（実物47本すべてにある） |
| `session_no_total` | `integer` | — | Notion の ID プロパティ（自動採番） |
| `fiscal_year` | `integer` | — | Notion の数式プロパティ `年度`（4月始まり） |
| `body` | `document` | ○ | 本文。節は3つを宣言し、宣言外の節も受ける |

**人間はどれも入力しない**（charter §5.2）。`source` 属性が取り出し元を持ち、インポータはプロパティ名そのものを知らない。

必須を `meeting_date` だけにしたのは、charter §5.2 の「検証も寛容にし、止めるのは `開催日` が無いときだけにする」に従ったためである。回次が付いていない過去ログも PDF になり、そのときテンプレートは表題を `第47回部会` ではなく `部会` にする。

節はすべて `required: false` にした。3節が揃う回は少数で（アナウンス44 / 活動報告34 / 次回予告4）、必須にすると過去ログの大半が通らない。空の節を PDF から落とすのはテンプレート側の判断である（ir-type-vocabulary.md §2.8）。

`extra_sections` は `"allow"`。臨時の節（部費回収・幹部自己紹介など）が実物に少数あり、禁止すると通らなくなる。

`blocks` は6種すべて（`heading` `paragraph` `list` `quote` `code` `image`）。**表は実測0件**なので block に持たない。

## テンプレートが前提にしている context

`document` の実装がテンプレートへ渡す形として、次を前提に書いてある。ir-type-vocabulary.md §5 の分担（節の順序の固定・宣言外の節の後置は `src/entex/` 側）をそのまま形にしたものである。

```jinja
\BLOCK{for sec in doc.body.sections}
\logSection{\VAR{sec.heading}}
\VAR{blocks(sec.blocks)}
\BLOCK{endfor}
```

- `doc.body.sections` は **並び済みの配列**。`schema.json` の `sections[]` の宣言順に並び、`extra_sections` はその後ろに入力の順序で付く。IR の側のキーの並びは見ない
- 各要素は `heading`（表示する見出し。宣言節はスキーマの値、臨時の節は入力の値）と `blocks` を持つ
- 空の節はキーごと落とすのではなく、`blocks` が空の要素として渡ってくる想定にしている。落とすかどうかは体裁の判断なのでテンプレートが `\BLOCK{if sec.blocks}` で決める
- 文字列はエスケープ済み。例外は `code` block の `text` と、span の `href`

IR そのものの形（`sections` は dict、`extra_sections` は別の配列）と context の形が違うのは、並べ替えを `src/entex/` が済ませてからテンプレートに渡すためである。

## `src/entex/` 側の実装（issue #30 で充足）

このパッケージを置いた時点で `packages/` 側の作業は終わっていた。PDF を出すために足りなかったものは [issue #30](https://github.com/NPCdotcom/EnTeX/issues/30) で `src/entex/` に足した。

| もの | 置き場所 |
|---|---|
| `source` 属性（全フィールド） | `FieldDef` |
| `document` を `FieldType` に足す | `FieldType` |
| `sections` / `extra_sections` / `blocks` / `max_heading_level` | `FieldDef` |
| block の検証（宣言外 type・`max_heading_level`・`list` の入れ子3段） | `ir/validate.py` |
| 節の並べ替え（宣言順の固定・宣言外の節の後置） | `renderer.shape_documents` |
| span のエスケープ（`code` の `text` は除く） | `tex/escape.py` |
| `href` は TeX エスケープせず、`%` `#` `&` は `\` 前置、他の特殊文字はパーセントエンコード | `tex/escape.escape_href` |
| 臨時の節の `heading` はエスケープする | `tex/escape.py` |
| `ja_date` の曜日オプション | `renderer.filter_ja_date(..., with_weekday=True)` |

## 正常系（`examples/valid/`）

| ファイル | 場面 | 確かめたいこと |
|---|---|---|
| `01-typical.json` | 3節が揃った回 | 見出し・段落・入れ子の箇条書き・インラインリンクが一通り出る。**画像なし**なので MVP（charter §5）の対象はこれ |
| `02-minimal.json` | 初回・アナウンスだけの回 | 任意フィールドがすべて無い状態。回次も年度も無く、表題が `部会` になる |
| `03-extra-sections.json` | 臨時の節がある回 | 宣言外の節が宣言節の**後ろ**に、入力の順序で並ぶ。活動報告が無いので節ごと出ない |
| `04-code-and-quote.json` | コードブロックと引用がある回 | `code` だけがエスケープされずに書いたとおり出る。引用の中にリンクがある |
| `05-tex-special-chars.json` | 特殊文字だらけの回 | `& % $ # _ { } ~ ^ \ < > ' " \` \|` が本文・見出し・URL に入っても壊れない |
| `06-with-images.json` | 直近の回（画像が主役） | `image` block が出る。MVP の次（`src` が何を指すかは未決。charter §11 Open） |

## 異常系（`examples/invalid/`）

| ファイル | 入れた誤り | 期待する挙動 |
|---|---|---|
| `01-unknown-section-key.json` | `sections` に宣言外のキー `free_talk` | 拒否する。宣言外の節は `extra_sections` に入れる |
| `02-unknown-block-type.json` | `blocks` に宣言していない `table` | 拒否する（実測0件なので語彙に無い） |
| `03-heading-too-deep.json` | `level: 3`（`max_heading_level: 2` 超過） | 拒否する |
| `04-missing-meeting-date.json` | `meeting_date` が無い | 拒否する。**寛容な検証が唯一止めるのがこれ**（charter §5.2） |
| `05-envelope-mismatch.json` | `schema_version: 2` | 中身を見る前に止める。版を上げたときはこの値を1つ大きくする（[packages/README.md](../README.md)） |
| `06-list-nested-too-deep.json` | 箇条書きの入れ子が4段 | 拒否する。LaTeX の `itemize` が4段までのため |

## examples の出どころ

実物47本（2024/5〜2026/7）の構造から起こした。節の構成・block の種類・見出しの入れ子・臨時の節の出方は実物のとおりである。

ただし**部員の呼称・作品名・具体的な金額など、個人が特定できる記述は一般的な語に置き換えてある**。このリポジトリは公開されており、第三者の情報を置かないためである。URL も `example.com` に差し替えた。パッケージの検証に要るのは構造であって中身ではないので、置き換えで失われるものは無い。
