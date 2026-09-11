# Design（思案・基本設計）

スコープ階層 **H0–H5** に沿ったパス。詳細: [PROJECT_LIFECYCLE.md](../PROJECT_LIFECYCLE.md)

```
docs/design/
├── product/              # H0 プロダクト charter
├── reverse-engineering/  # brownfield 現状把握（P1 前 · brownfield-reference）
├── compliance/           # 規制チェックリスト（利用先 opt-in · o-05）
├── elements/             # H1 要素
├── systems/              # H2 システム（IaC は _template/infrastructure を systems/<slug>/ へ）
├── frameworks/           # H3 FW・ライブラリ選定
└── programs/             # H4/H5 プログラム・アルゴリズム設計（実装前）
```

テンプレ: `_template/reverse-engineering/` · `_template/infrastructure/` · `compliance/regulated-checklist.md`

- 思案: `*.deliberation.md`（`design-deliberate`）
- 仕様: `*.md`（`design-record`）
- 要求・要件: `docs/requirements/<slug>/`（P1–P2）

**PDCA Do** は `.agents/plans/programs/` または `algorithms/` の plan に紐づける。

記入例（中立）: [../_example/design/](../_example/README.md) — コピー後は置換すること。
