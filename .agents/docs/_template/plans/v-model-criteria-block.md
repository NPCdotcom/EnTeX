# V-model criteria block（plan 用スニペット · G10）

P4 `plan-record` の Acceptance criteria に **貼り付け** — 不要な行は削除。

```markdown
## V-model 検証（P6 review-conduct で確認）

| 層 | 本 plan での確認方法 | 状態 |
|----|----------------------|------|
| **UT** | 単体テスト / TDD（P5） | [ ] |
| **IT** | モジュール間・IF・結合テスト | [ ] |
| **ST** | 設計（P3）との整合 · 非機能 | [ ] |
| **UAT** | P2 受入条件 · 要求へのリンク | [ ] |

各 AC は `要件.md` または `docs/design/` へリンク（RTM）。

**Outcome（任意 · G13）**: `docs/_template/plans/outcome-check-block.md` を plan に含める場合、P6 で product outcome を確認。
```

正本: `docs/PROJECT_LIFECYCLE.md` § P6 · skill `review-conduct` · `references/v-model-rtm.md`
