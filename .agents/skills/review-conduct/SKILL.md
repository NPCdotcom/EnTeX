---
name: review-conduct
description: Review code against plan criteria, requirements, and design (V-model). Use at Check time after gathering review context.
---

# Review Conduct

**Role**: `reviewer` · **P6** · Execute

1. `review-reference`
2. **V-model**: [`../lib-review-vmodel/SKILL.md`](../lib-review-vmodel/SKILL.md) · detail [`references/v-model-rtm.md`](references/v-model-rtm.md)
3. **Outcome 確認（任意 · G13）** — plan に `outcome-check-block` がある場合: product outcome · leading indicator を Act に記録
4. Acceptance criteria — pass/fail with file:line
5. 一般チェック + **rules/local/** + **AGENTS.md**
6. Verdict: pass | conditional | fail

## Report

RTM 表、criterion ごとの結果、Critical/Warning/Suggestion、spec gaps、巻き戻し先 P?、next actions。

## Do not

drive-by refactor、plan/design status 変更、RTM 未カバーで pass

詳細パターン: [`references/standards.md`](references/standards.md)
