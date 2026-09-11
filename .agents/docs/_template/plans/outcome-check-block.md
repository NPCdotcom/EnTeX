# Outcome check block（plan 用スニペット · G13）

P4 `plan-record` または P6 `review-conduct` で **任意** 使用。スパイク · 内部ツール · outcome 明示不要な plan では削除可。

```markdown
## Outcome 確認（任意 · P6）

| 項目 | 内容 |
|------|------|
| **Product outcome** | （P1 要求 / P2 要件 / charter から 1 行） |
| **Leading indicator** | （測定可能な行動指標 · 例: 週次利用回数 ≥ N） |
| **検証方法** | （ログ · アンケート · 手動観察 · 未測定なら「未設定」） |
| **結果** | pass / fail / deferred |
| **Act** | （未達時: 新 plan · Recycle · criterion 見直し） |

**完了定義**: Output（criteria pass）に加え、上記 outcome が **pass または deferred 理由記載** で P6 完了。
```

正本: `docs/PROJECT_LIFECYCLE.md` § P6 Outcome · skill `review-conduct` · 学習 `t-04-outcome-discovery.md`
