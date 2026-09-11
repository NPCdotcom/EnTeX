# IaC verification

**システム**: {{SYSTEM_NAME}}  
**記録日**: {{DATE}}

## 静的解析（CI）

| ツール | 対象 | 失敗条件 | ワークフロー |
|--------|------|----------|--------------|
| Checkov | Terraform/CDK 等 | policy fail | `iac-checkov.example.yml` |
| tfsec / 代替 | | | |
| gitleaks | repo | secret | |

**例**: `docs/_example/.github/workflows/iac-checkov.example.yml` → 利用先 `.github/workflows/` にコピー

## Plan / Review

| 段階 | 実施者 | 証跡 |
|------|--------|------|
| `terraform plan` / `cdk diff` | builder + reviewer | PR コメント |
| 設計整合 | spec_designer | 本ディレクトリ ↔ plan criteria |

## P4 plan criteria 推奨行

```markdown
- [ ] IaC: Checkov（または同等）CI green
- [ ] prod 変更: チケット ID + Gate 承認記録
- [ ] シークレットが IaC / 状態ファイルに含まれない
```

## P6 接続

- `review-conduct`: criteria 上記を検証
- regulated: `regulated-checklist.md` §4.4

## Open questions

- 
