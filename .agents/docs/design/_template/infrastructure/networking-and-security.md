# Networking and security

**システム**: {{SYSTEM_NAME}}  
**記録日**: {{DATE}}

## ネットワーク

| 要素 | 設計 |
|------|------|
| VPC / VNet CIDR | |
| サブネット（public/private） | |
| Ingress / Egress | |

## IAM · 認可

| 主体 | 権限スコープ | 原則 |
|------|--------------|------|
| 人間運用者 | | least privilege |
| CI/CD ロール | | |
| ワークロード ID | | |

## セキュリティコントロール

| 領域 | 方針 | 検証 |
|------|------|------|
| 保存時暗号化 | | |
| 転送時 TLS | | |
| シークレット | Secrets Manager 等 · repo 禁止 | gitleaks |
| WAF / 境界防御 | | |

## a-07 接続

- 利用先 conditional rule: `security-conditional.mdc.example`（opt-in）
- CI: Semgrep · Checkov（`iac-verification.md`）

## Open questions

- 
