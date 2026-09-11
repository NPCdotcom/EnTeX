# Environments and promotion

**システム**: {{SYSTEM_NAME}}  
**記録日**: {{DATE}}

## 環境一覧

| 環境 | 目的 | データ | デプロイ頻度 |
|------|------|--------|--------------|
| dev | | 合成/匿名化 | |
| staging | | 本番類似 | |
| prod | | 本番 | |

## 昇格パス（変更管理）

```
dev → staging → prod
```

| 段階 | 承認者 | 証跡（p-06） |
|------|--------|--------------|
| PR merge | reviewer ≠ author | GitHub |
| staging deploy | | workflow log |
| prod deploy | Gate Keeper / CAB | ticket + deploy log |

## 設定差分

| 項目 | dev | staging | prod |
|------|-----|---------|------|
| インスタンスサイズ | | | |
| 冗長化 | | | |

## ロールバック

- 手順:
- RTO/RPO（要件リンク）:

## Open questions

- 
