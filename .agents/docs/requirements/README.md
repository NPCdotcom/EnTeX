# Requirements（要求・要件）

**P1–P2** の正本。設計詳細は `docs/design/`、実装計画は `.agents/plans/`。

## フォルダ規則

1 要求トピック = 1 フォルダ（スラッグ名・わかりやすい英数字）。

```
docs/requirements/
├── README.md
├── _template/
│   ├── 要求.md
│   └── 要件.md
└── <slug>/          # 例: user-auth, inventory-core
    ├── 要求.md      # P1 要求定義
    └── 要件.md      # P2 要件定義（要求.md へリンク）
```

## 工程

| ファイル | 工程 | ゲート |
|----------|------|--------|
| `要求.md` | P1 | H0 プロダクト概要が存在 |
| `要件.md` | P2 | 要求.md がレビュー可能；検証可能な条件 |

## 推敲

`>` 行はユーザー・PM の思考メモ。エージェントは草案後、ユーザー入力を `>` に反映してから本文へ昇格。

## スキル

- 読取: `design-reference`, `lifecycle-reference`
- 記録: `design-record`（requirements パスも可）

詳細: [PROJECT_LIFECYCLE.md](../PROJECT_LIFECYCLE.md)

## 例

| 種類 | パス |
|------|------|
| 空テンプレ | `_template/要求.md`, `要件.md` |
| 記入済み中立サンプル | `../_example/requirements/sample-capability/`（**リネーム必須**） |

起動: [FIRST_PROJECT_START.md](../FIRST_PROJECT_START.md)
