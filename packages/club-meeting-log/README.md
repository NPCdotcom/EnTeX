# club-meeting-log — 部会ログ

最初の文書種（charter §5 の MVP）。情報技術研究部が部会ごとに Notion で書いている記録を、同じ体裁の PDF にする。要求は [docs/requirements/club-meeting-log/要求.md](../../docs/requirements/club-meeting-log/要求.md)、経緯は [ADR-0001](../../docs/adr/0001-first-doc-type-pivot-to-meeting-log.md)。

> **状態: `schema.json` / `template.tex.j2` / `style/` / `examples/` は揃っているが、PDF はまだ出ない。**
> 本文を持つ `document` 型が `src/entex/` に実装されていないため、`schema.json` の読み込みそのものが落ちる（[issue #21](https://github.com/NPCdotcom/EnTeX/issues/21) で設計だけを決め、実装は残した）。足りないものは下の「`src/entex/` に足りないもの」にまとめた。

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

## `src/entex/` に足りないもの

このパッケージを置いた時点で `packages/` 側の作業は終わるが、PDF を出すには `src/entex/` に次が要る。[issue #22](https://github.com/NPCdotcom/EnTeX/issues/22) の完了条件が「触る必要が出たら直さずに報告する」としているので、ここに書き出すだけにしてある。

実際に出るエラーは次のとおり（`load_and_validate` に `examples/valid/01-typical.json` を渡したもの）。

```
文書パッケージ 'club-meeting-log' の schema.json が不正です:
  fields.meeting_date.source: Extra inputs are not permitted;
  fields.session_no_total.source: Extra inputs are not permitted;
  fields.fiscal_year.source: Extra inputs are not permitted;
  fields.body.type: Input should be 'text', 'rich_text', 'month', 'date', 'integer',
    'money', 'enum', 'boolean', 'object', 'row_list' or 'list';
  fields.body.sections: Extra inputs are not permitted;
  fields.body.extra_sections: Extra inputs are not permitted;
  fields.body.blocks: Extra inputs are not permitted;
  fields.body.max_heading_level: Extra inputs are not permitted
```

| 足りないもの | 置き場所 | 正本 |
|---|---|---|
| `source` 属性（`document` に限らず全フィールドに付く） | `FieldDef` | ir-type-vocabulary.md §3 |
| `document` を `FieldType` に足す | `FieldType` | 同 §1・§2.8 |
| `sections` / `extra_sections` / `blocks` / `max_heading_level` 属性 | `FieldDef` | 同 §3 |
| block の検証（宣言外の type の拒否・`max_heading_level`・`list` の入れ子3段） | `ir/validate.py` | 同 §2.8 |
| 節の並べ替え（宣言順の固定・宣言外の節の後置・見出しレベルの正規化） | `renderer.build_context` | 同 §5 |
| span のエスケープ（`code` の `text` は除く。`href` の扱いは下記） | `tex/escape.py` | 同 §5 |
| `ja_date` の曜日オプション | `renderer.py` のフィルタ | charter §5.2「曜日は `meeting_date` から `ja_date` フィルタで出す」 |

決めていない点が2つある。どちらも実装のときに決まる。

- **span の `href` をエスケープするか。** 文字列なので素直に読めばエスケープ対象だが、URL を TeX エスケープすると `\href` / `\url` に渡せなくなる。一方で素通しにもできない。`05-tex-special-chars.json` の URL（`https://example.com/sheet?a=1&b=2`）は `&` を含み、`\url` をマクロの引数越しに使うと `&` が表の区切りとして解釈されて壊れる。**エスケープではなくパーセントエンコードで TeX 特殊文字を消す**のが素直だと思うが、実装のときに決める
- **臨時の節の `heading` をエスケープするか。** これは利用者の入力なのでエスケープが要る。宣言節の `heading` はスキーマの値なので `schema_context` と同じ扱いでよい

なお、上の context を手で組み立ててテンプレートを素振りし、`examples/valid/` の6件すべてが `.tex` になるところまでは確かめてある（`src/entex/` は読み込んだだけで変更していない）。PDF になるかは LuaLaTeX を通していないので未確認である。

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
