# Regulated / enterprise compliance checklist

**プロジェクト**: {{PROJECT_NAME}}  
**最終更新**: {{DATE}}  
**適用規格**（該当にチェック）: [ ] GxP/Part 11 [ ] SOC2 [ ] ISO 27001 [ ] その他:

> キットは **工程 Gate + audit-log** を提供。RTM · e-sign · デプロイ証跡は **ALM/GRC + git/CI** で満たす（p-06）。

---

## 1. 工程 · Gate

| # | 項目 | 状態 | 証跡パス |
|---|------|------|----------|
| 1.1 | `lifecycle_plan` ユーザー Go 済 | [ ] | `docs/project-state.yaml` |
| 1.2 | Gate Keeper = ユーザー（PM 独断なし） | [ ] | `ROLES_AND_GOVERNANCE` |
| 1.3 | ゲート決定が audit-log に記録 | [ ] | `.agents/memory/audit/audit-log.md` |
| 1.4 | P6 review 実施 · criteria リンク | [ ] | plan · review-record |

## 2. 変更管理（SOC2 CC8.1 / ISO A.8.32 相当）

| # | 項目 | 状態 | 証跡 |
|---|------|------|------|
| 2.1 | 変更はチケット/Issue で追跡 | [ ] | |
| 2.2 | PR にチケット ID リンク | [ ] | |
| 2.3 | PR レビュー ≠ 作者 | [ ] | branch protection |
| 2.4 | CI green 後にマージ | [ ] | workflow log |
| 2.5 | 本番デプロイログ保持 | [ ] | |
| 2.6 | 緊急変更の事後レビュー | [ ] | |

## 3. トレーサビリティ（RTM）

| # | 項目 | 状態 | 備考 |
|---|------|------|------|
| 3.1 | 要求 → 要件 → 設計リンク | [ ] | `docs/requirements/` · design |
| 3.2 | 要件 → plan criteria | [ ] | `.agents/plans/` |
| 3.3 | criteria → テスト証拠 | [ ] | CI / P6 |
| 3.4 | ALM/RTM ツール（任意） | [ ] | キット外 |

## 4. セキュリティ（a-07 翻訳）

| # | 項目 | 状態 | 備考 |
|---|------|------|------|
| 4.1 | シークレットを repo に含めない | [ ] | gitleaks 等 |
| 4.2 | CI: SAST/secret scan（利用先） | [ ] | |
| 4.3 | security conditional rule（opt-in） | [ ] | `.cursor/rules/` |
| 4.4 | IaC scan（該当時） | [ ] | Checkov 等 · [`_template/infrastructure/iac-verification.md`](../_template/infrastructure/iac-verification.md) |

## 5. AI / エージェント

| # | 項目 | 状態 | 備考 |
|---|------|------|------|
| 5.1 | Cloud Agent / Automations 未使用 or 明示承認 | [ ] | c-06 |
| 5.2 | Task subagent 禁止遵守 | [ ] | `no-subagents` |
| 5.3 | AI 生成コードは人間 review 必須 | [ ] | P6 |
| 5.4 | モデル/プロンプト版管理（該当時） | [ ] | キット外 registry |
| 5.5 | Cursor **Privacy Mode**（Teams: org 強制可 · Enterprise 推奨） | [ ] | [cursor.com/privacy](https://cursor.com/privacy-overview) · c-10 |
| 5.6 | Cursor Enterprise: MCP/repo 制御 · audit API と audit-log 二重記録方針 | [ ] | Enterprise admin |

## 6. 監査レビュー

| 日付 | レビュア | 範囲 | 結果 |
|------|----------|------|------|
| | | | |

---

**参照**: p-06 landscape · `docs/design/compliance/README.md`
