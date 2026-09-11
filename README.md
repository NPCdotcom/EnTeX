# EnTeX

GitHub 共同開発プロジェクト。

## Members

| Nickname | GitHub ID | Role |
|----------|-----------|------|
| NPC | [NPCdotcom](https://github.com/NPCdotcom) | Owner / collaborator |
| Aster | [astel_isk](https://github.com/astel_isk) | Collaborator |

## Repository

- HTTPS: https://github.com/NPCdotcom/EnTeX.git
- SSH: `git@github.com:NPCdotcom/EnTeX.git`
- Default branch: `main`

## Runtime

想定実行環境: **WSL (Ubuntu)**。

```bash
# 例: Ubuntu ディストリを起動してリポジトリへ
wsl -d Ubuntu
cd /mnt/c/Users/<you>/Documents/GitHub/EnTeX
```

## Layout

| Path | Shared? | Notes |
|------|:-------:|-------|
| `docs/` | yes | 要求・設計・ADR・用語 |
| `schemas/` | yes | 共有スキーマ |
| `design/` | yes | デザイン成果物 |
| `.agents/` | yes | AI キット（skills / rules / plans / memory 骨格） |
| `AGENTS.md` | yes | プロジェクト固有エージェント案内 |
| `.env` / venv / `.cursor` junctions | no | 生成物・秘密情報（`.gitignore`） |

`.gitignore` に **独自 AI アセットは載せません**。共同者がドキュメント・スキーマ・デザイン・エージェント資産を同じリポジトリで共有できるようにしています。

## First-time setup (collaborators)

```bash
git clone git@github.com:NPCdotcom/EnTeX.git
cd EnTeX

# Cursor 用 junction（Windows PowerShell）
.\.agents\scripts\link-cursor.ps1

# または WSL / Unix
./.agents/scripts/link-cursor.sh

# 任意: エージェント実行用 venv
# Windows: .\.agents\env\bin\setup.ps1
# Unix:    ./.agents/env/bin/setup.sh
```

## Docs entry

- [docs/README.md](docs/README.md)
- [docs/FIRST_PROJECT_START.md](docs/FIRST_PROJECT_START.md)
- [docs/PROJECT_LIFECYCLE.md](docs/PROJECT_LIFECYCLE.md)
- [docs/TEAM.md](docs/TEAM.md)
