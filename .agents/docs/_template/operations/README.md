# Operations templates（G4 · AI-DLC Operations 相当）

**用途**: P6 出荷後 · デプロイ · 監視 · インシデント。キットは **テンプレのみ** — 正本は利用先 `docs/operations/`。

| ファイル | 内容 |
|----------|------|
| `deploy-checklist.md` | リリース前後 · ロールバック |
| `runbook-skeleton.md` | 障害対応 · エスカレーション |
| `monitoring-slos.md` | SLO/SLI · アラート（observability-hooks から接続） |
| `feedback-to-inception.md` | 運用所見 → P0–P3 巻き戻し（a-08 · AI-DLC Operations ループ） |

**AI-DLC Operations 写像**（a-08 · キット翻訳）:

| AI-DLC | キット |
|--------|--------|
| Deploy / verify | `deploy-checklist.md` |
| Monitor / SLO | `monitoring-slos.md` |
| Incident / runbook | `runbook-skeleton.md` |
| Feedback → Inception | `feedback-to-inception.md` |

**接続**:

- P3 `infrastructure/observability-hooks.md` → 本テンプレへ
- P6 完了後 · unit ごとに 1 セット（任意）
- Cloud Agent / Automations → `CURSOR_SUBAGENT_POLICY.md`（キット外）

**手順**: コピー → `docs/operations/<unit-slug>/` · Gate Keeper 承認
