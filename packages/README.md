# packages/ — 文書種パッケージ（doc-package）

文書種 1 つ = ディレクトリ 1 つ。**本体コード（`src/entex`）を変えずに増やせる**ことが設計の合否判定（charter §4・§6）。

想定する中身（H1 で確定させる。現時点は仮）:

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
| [`circle-monthly-report/`](circle-monthly-report/README.md) | スキーマと IR 例のみ。テンプレートは着手順 1 で書く |
