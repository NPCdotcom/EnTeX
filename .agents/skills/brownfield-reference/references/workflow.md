# Brownfield reference — workflow

## 1. Preconditions

| 確認 | 取得元 |
|------|--------|
| brownfield フラグ | `docs/project-state.yaml` · `lifecycle_plan` |
| スコープ | turn-brief · ユーザー意図 |
| テンプレ有無 | `docs/design/_template/reverse-engineering/` |

## 2. Bootstrap 成果物

```text
mkdir -p docs/design/reverse-engineering
cp docs/design/_template/reverse-engineering/*.md docs/design/reverse-engineering/
```

`README.md` はコピー不要 — テンプレ README を参照のみ。

## 3. 調査順（推奨）

| 順 | テンプレ | 調査手段 |
|----|----------|----------|
| 1 | `workspace-inventory.md` | Glob · ディレクトリ構造 · README · package manifests |
| 2 | `architecture-overview.md` | エントリポイント · 主要モジュール · レイヤ |
| 3 | `dependencies-and-integrations.md` | lockfiles · docker · 外部 API |
| 4 | `api-surface.md` | routes · OpenAPI · public exports |
| 5 | `data-model.md` | schema · migrations · ORM models |
| 6 | `tech-debt-risks.md` | TODO · テスト欠落 · 既知バグ · セキュリティ所見 |

**コード外の文脈**（競合 · 規制）が必要 → 別途 `landscape-research`。

## 4. Gate

1. 6 テンプレの **必須節** を埋める（不明は「未確認」と明記）
2. **Plan モード**でユーザーにサマリ提示
3. ユーザー **Go** → `audit-log` に `brownfield_re_complete`（`stage_complete` 相当 · refs: `docs/design/reverse-engineering/`）
4. `secretary-route` → **P1**（要求）

## 5. スコープ制限

| profile | RE の厚み |
|---------|-----------|
| hotfix | workspace-inventory のみで可 |
| spike | architecture + tech-debt |
| standard / full | 6 件すべて |

`adaptive-lifecycle-plan` の profile に従う。

## 6. AI-DLC 対応ラベル

| AI-DLC | キット |
|--------|--------|
| Reverse Engineering | 本 skill + `docs/design/reverse-engineering/` |
| Workspace Detection | adaptive-lifecycle-plan |

`lifecycle_plan.skipped_stages` に `Reverse Engineering` を **実行した場合は含めない**。
