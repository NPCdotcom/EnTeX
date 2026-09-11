# Compliance（規制 · エンタープライズ）

**用途**: 規制産業 · SOC2/ISO 向けの **利用先チェックリスト**。キット汎用正本には常時注入しない（p-06 · o-05）。

| ファイル | 内容 |
|----------|------|
| `regulated-checklist.md` | 工程 · 変更管理 · 監査 · AI 利用の確認項目 |

**関連**: `docs/ROLES_AND_GOVERNANCE.md` · `memory/audit/audit-log.md` · `a-07` security 例

**手順**:

1. プロジェクトで `regulated-checklist.md` をコピーし `docs/design/compliance/` に配置
2. `lifecycle_plan.profile: full` 推奨
3. 必要なら `docs/_example/.cursor/rules/security-conditional.mdc.example` を `.cursor/rules/` へ
