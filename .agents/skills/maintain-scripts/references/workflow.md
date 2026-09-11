# Maintain scripts — workflow

## 1. Inventory

```powershell
python env/bin/agents-run.py maintain-scripts inventory skills
```

- `skills/*/scripts/*` を列挙
- 各 stem が当該 `SKILL.md` に記載されているか
- `agents-run` で解決できるか

## 2. Review

```powershell
python env/bin/agents-run.py maintain-scripts review
python env/bin/agents-run.py maintain-scripts review --skill maintain-adhoc
```

`_SCRIPT_POLICY.md` + [`script-review-rubric.md`](script-review-rubric.md) に照合。

## 3. Dedupe（共通化候補）

```powershell
python env/bin/agents-run.py maintain-scripts dedupe-report
```

- 同一 stem 名の重複
- 正規化ハッシュ一致 → `env/python/lib/` 抽出候補

**自動リファクタはしない** — レポート後 `maintain-record` で適用。

## 4. Encapsulate（手順）

1. 共有ロジックを `env/python/lib/<module>.py` へ
2. スキル script は薄い `argparse` ラッパーのみ
3. `inventory` + `review` を再実行 → ISSUES=0
4. `maintain-adhoc` の `audit-skill-layout` で skill 数・構造確認

## 5. Record

`maintain-record` · `role-skill-catalog` · 触った `SKILL.md` の stem 行を更新。
