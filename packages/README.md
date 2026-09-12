# packages/ — 文書種パッケージ（doc-package）

文書種 1 つ = ディレクトリ 1 つ。**本体コード（`src/entex`）を変えずに増やせる**ことが設計の合否判定（charter §4・§6）。

中身（最初の文書種で実際に使っている構成。2 つ目の文書種で妥当性を判定する）:

```
packages/<doc-type-slug>/
├── schema.json      # 入力の形（IR の検証に使う）。型の語彙: docs/design/elements/ir-type-vocabulary.md
├── template.tex.j2  # TeX 雛形（Jinja2）— 「テンプレート」はこのファイルだけを指す
├── style/           # .sty / 画像 など体裁側の資産
├── examples/        # IR の例。valid/（PDF が出るべき）と invalid/（検証で弾くべき）
└── README.md        # 文書種の説明・題材・examples の意図
```

用語は charter §10 に従う（パッケージ ≠ テンプレート）。

| パッケージ | 状態 |
|---|---|
| [`club-meeting-log/`](club-meeting-log/README.md) | 最初の文書種（charter §5 の MVP）。実物47本に基づくスキーマ・IR 例・テンプレートとスタイルが揃っている。`document` 型の実装（[issue #30](https://github.com/NPCdotcom/EnTeX/issues/30)）で画像なしの例は PDF が出る |
| [`circle-monthly-report/`](circle-monthly-report/README.md) | スキーマ・IR 例・仮レイアウトのテンプレートとスタイル。`entex render` で PDF が出る。**新規の文書種としては開発を継続しない**（[ADR-0001](../docs/adr/0001-first-doc-type-pivot-to-meeting-log.md)）。型語彙を一通り使う参考資料として残す |

`src/entex/` が読むのは `schema.json` の中身と `template.tex.j2` / `style/` の場所だけ（`src/entex/packages.py`）。`style/` は latexmk 実行時に `TEXINPUTS` へ加えられるので、`.sty` はファイル名だけで `\usepackage` できる。

## `schema.json` の書き方と版

書き方は **EnTeX 独自の簡潔な形式（案1）** が正本である（[型の語彙 §8](../docs/design/elements/ir-type-vocabulary.md#8-schemajson-の書き方決定-案1)）。JSON Schema では書かない。読み込む pydantic モデルは [`src/entex/ir/schema.py`](../src/entex/ir/schema.py) で、使える型は [§1 の語彙](../docs/design/elements/ir-type-vocabulary.md#1-語彙精査後)、フィールド属性は同 §3 の表に限る。

`schema_version` を上げるかどうかは、**「それまで通っていた IR が通らなくなるか」** の一軸で決める。

| よくある変更 | 版 |
|---|---|
| 任意フィールドの追加、`label` の変更、制約の緩和、`enum` の選択肢の追加 | 上げない |
| 必須フィールドの追加、フィールドの削除・改名、型の変更、`derived` の増減、制約の強化、`enum` の選択肢の削除 | **上げる** |

網羅した表と理由は [型の語彙 §6.1](../docs/design/elements/ir-type-vocabulary.md#schema_version-を上げる基準) にある。

上げるときの手順:

1. `schema.json` の `schema_version` を 1 つ増やす
2. `examples/` の IR の封筒の `schema_version` を新しい版に揃える。**古い版を受け付け続ける仕組みは無いので、揃えなかった例は中身を見られる前に落ちる**
   - 例外は**版の不一致そのものを試している例**（[`circle-monthly-report/examples/invalid/06-envelope-mismatch.json`](circle-monthly-report/examples/invalid/06-envelope-mismatch.json)）。これは「合わない版」であり続ける必要があるので、スキーマより 1 つ大きい値に付け替える
3. `make test` で `examples/` が期待どおりに通る・落ちることを確かめる

体裁だけの変更（`template.tex.j2` や `style/` の修正）では上げない。`schema_version` が版付けするのは入力の形であって、出力の見た目ではない。
