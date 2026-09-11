# V-model traceability（RTM）

plan の各 Acceptance criterion について、左（開発）→ 右（検証）の対応を確認する。  
正本: `docs/ROLES_AND_GOVERNANCE.md` · `docs/PROJECT_LIFECYCLE.md` § P6

| 検証水準 | 対応する成果物（左） | レビューで確認すること |
|----------|----------------------|------------------------|
| **UAT（受入）** | P2 `要件.md` 受入条件・P1 要求 | criterion が要求/受入を満たすか；ユーザー視点 |
| **ST（総合）** | P3 `docs/design/` 基本設計 | システム全体・非機能・境界の整合 |
| **IT（結合）** | P4 plan scope・IF・モジュール間 | 結合点・契約・依存の破綻 |
| **UT（単体）** | P5 実装・TDD テスト | モジュール単位の正しさ・テスト存在 |

## RTM 行（criterion ごとに 1 行）

```markdown
| Criterion ID | 検証層 | 要件/設計リンク | 変更ファイル | テスト/検証 | 結果 |
|--------------|--------|-----------------|--------------|-------------|------|
| AC-1 | UT/IT/ST/UAT | docs/requirements/.../要件.md#... | src/... | pytest/手動 | pass/fail |

**四層カバレッジ（G10）**: 本 plan の AC セットが **UT · IT · ST · UAT のうち該当層をすべてカバー**しているか。該当なしの層は「N/A + 理由」を 1 行。

## P6 ゲート（層ごと）

- [ ] **UT**: 実装変更ごとに単体根拠あり
- [ ] **IT**: モジュール境界・契約を確認
- [ ] **ST**: `docs/design/` と矛盾なし
- [ ] **UAT**: P2 受入条件を満たす
```

## トレーサビリティ判定

- [ ] **Forward**: 各 criterion に少なくとも 1 つの検証がある
- [ ] **Backward**: 変更が criterion または設計 Fact にトレースできる
- [ ] **Orphan 要件**: P2 受入条件に対応する criterion が plan に無い → fail または spec gap
- [ ] **Orphan テスト**: criterion に無関係なテストのみ → 警告
- [ ] 欠陥の **起源工程** を推定 — Recycle 提案に使う

参照: [Jama RTM](https://www.jamasoftware.com/requirements-management-guide/requirements-traceability/how-to-create-and-use-a-requirements-traceability-matrix-rtm/)
