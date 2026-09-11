# Cursor 互換 — `.agents` と `.cursor` の関係

## 結論

| レイヤ | 正本（汎用） | Cursor が直接読むパス |
|--------|-------------|----------------------|
| Rules | `.agents/rules/` | `.cursor/rules/` |
| Skills | `.agents/skills/` | `.cursor/skills/` |
| Hooks 脚本 | `.agents/hooks/` | `.cursor/hooks/`（または `.agents/hooks/` を command で指定） |
| Hooks 定義 | `.agents/hooks.json` | **`.cursor/hooks.json`**（プロジェクト）または `~/.cursor/hooks.json`（ユーザー） |
| 記憶 | `.agents/memory/` | Cursor 非組込 — Skill 経由で読書 |

**Cursor 公式**（[Rules](https://cursor.com/docs/context/rules) · [Hooks](https://cursor.com/docs/hooks)）は **`.cursor/`** を前提とする。  
`.agents/` は [dotagentsprotocol](https://dotagentsprotocol.com/) 等の **ツール横断** 慣習。正本を `.agents/` に置き、**junction/symlink** で `.cursor/` を橋渡しするのが推奨。

## 配置パターン

### A. ユーザーキット（本リポジトリ）

```
%USERPROFILE%\.agents\          ← 正本（skills · rules · memory · docs）
%USERPROFILE%\.agents\.cursor\ ← link-cursor.ps1 が junction を作成
```

ワークスペースを `~/.agents` として開く場合、**link-cursor を一度実行**して Cursor が rules/skills を拾えるようにする。

### B. 利用先プロジェクト

```
project/
├── AGENTS.md
├── .agents/          ← maintain-bootstrap でコピー
└── .cursor/          ← link-cursor.ps1（rules/skills/hooks → .agents/*）
    └── hooks.json    ← .agents/hooks.json をコピー（command は .agents/hooks/*.py）
```

## セットアップ

```powershell
# プロジェクトルート、または ~/.agents キットルートで
.\.agents\scripts\link-cursor.ps1
```

```bash
./.agents/scripts/link-cursor.sh
```

## hooks.json の command パス

正本 `.agents/hooks.json` は **プロジェクトルート基準**で `.agents/hooks/*.py` を指す。  
Cursor は `.cursor/hooks.json` から実行するが、作業ディレクトリは **プロジェクトルート**のため command パスは `.agents/...` のままでよい（[公式 Hooks ドキュメント](https://cursor.com/docs/hooks)）。

## 他ツール

| ツール | 読むファイル |
|--------|-------------|
| Cursor Agent | `.cursor/rules` · `AGENTS.md` · `.cursor/hooks.json` |
| Claude Code | `CLAUDE.md` · `.claude/` |
| Copilot | `.github/copilot-instructions.md` |
| 汎用 | ルート `AGENTS.md` · `.agents/` |

`.agents/` を正本にすれば、`AGENTS.md` + symlink で複数 IDE に配布可能。

## 参照

- [Sharing configs with symlinks (Rushi's)](https://www.rushis.com/sharing-ai-agent-configs-between-cursor-and-claude-with-symlinks/)
- [.agents Protocol](https://dotagentsprotocol.com/)
- [agentsfolder/spec](https://github.com/agentsfolder/spec)
