# Project-local rules

このフォルダの `.mdc` は **各プロジェクト固有** の実装・レビュー用レンズです。  
汎用キットをコピーした直後は **空**（テンプレのみ）で問題ありません。

## いつ作るか

| タイミング | 担当 |
|------------|------|
| プロジェクト始動（キット導入直後） | **kit_maintainer** + `maintain-bootstrap` |
| スタック変更・role／スキル追加 | **kit_maintainer** + `maintain-adhoc` |

スタックの公式ドキュメント URL や社内規約のパスは **リポジトリルートの `AGENTS.md`** に記載し、必要ならそこから `rules/local/` 用の `.mdc` を生成します。キット本体にはエンジン名・ドメイン名・ゲーム名を書かない。

## テンプレ

| ファイル | 用途 |
|----------|------|
| [_lens-implement.mdc.template](_lens-implement.mdc.template) | 実装（Do）レンズの雛形 |
| [_lens-review.mdc.template](_lens-review.mdc.template) | レビュー（Check）レンズの雛形 |

コピーして `{{stack}}-implement.mdc` 等にリネームし、`globs` と本文を埋める。

## 参照

- 汎用ルール: `../` 直下
- メンテナンス手順: `maintain-bootstrap` / `maintain-adhoc` スキル
- Cursor role: `kit_maintainer` · 正本 [`docs/CURSOR_ROLES.md`](../docs/CURSOR_ROLES.md)
