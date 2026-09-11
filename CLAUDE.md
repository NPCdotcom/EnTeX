# CLAUDE.md

このリポジトリの前提情報は `AGENTS.md` にまとめてあります。作業を始める前に必ず読んでください。

Claude Code固有の追加ルールは現時点でありません。プロジェクト共通の注意点はすべて `AGENTS.md` に集約しています。Claude Codeだけに特有の設定が必要になった場合は、このファイルに追記してください。

Claude Code用のハーネス(スキル・権限)は `.claude/` 配下にあります。

| パス | 用途 |
|------|------|
| `.claude/skills/docs-sync-check/` | `docs/` ・`AGENTS.md` と実装のズレを点検する |
| `.claude/settings.local.json` | ローカルの権限許可(`gh pr` / `gh issue` など) |
