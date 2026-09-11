# IaC structure

**システム**: {{SYSTEM_NAME}}  
**記録日**: {{DATE}}  
**IaC ツール**: [ ] Terraform [ ] CDK [ ] Pulumi [ ] その他:

## リポジトリレイアウト

```text
infra/
├── modules/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── README.md
```

## モジュール境界

| モジュール | 責務 | 入力変数 | 出力 |
|------------|------|----------|------|
| | | | |

## 状態管理（State）

| 項目 | 方針 |
|------|------|
| Backend | （S3+lock 等） |
| 分離単位 | env / region / … |
| ドリフト検知 | |

## 依存関係

| 上流 | 下流 | 備考 |
|------|------|------|
| | | |

## Open questions

- 
