# Infrastructure design templates（IaC · G9）

**用途**: AI-DLC Infrastructure Design 相当 · P3（H2 systems）でクラウド / IaC を設計する。

**コピー先**: `docs/design/systems/<slug>/`（例: `docs/design/systems/aws-platform/`）

| ファイル | 内容 |
|----------|------|
| `topology.md` | クラウド構成 · コンポーネント · データフロー |
| `iac-structure.md` | Terraform/CDK 等のモジュール構成 |
| `networking-and-security.md` | VPC · ファイアウォール · IAM 方針 |
| `environments-and-promotion.md` | dev/staging/prod · 昇格 |
| `observability-hooks.md` | ログ/メトリクス設計（G4 へのフック · 運用は `docs/_template/operations/`） |
| `iac-verification.md` | Checkov · plan review · P6 criteria |

**手順**: `design-deliberate` → `design-record` · `design-reference`  
**検証**: a-07 · `docs/_example/.github/workflows/iac-checkov.example.yml`  
**規制**: `docs/design/compliance/regulated-checklist.md` §4.4

**非採用**: `aidlc-docs` Infrastructure 丸コピー（o-06）
