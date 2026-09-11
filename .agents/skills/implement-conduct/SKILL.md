---
name: implement-conduct
description: Implement the agreed plan with TDD and minimal diffs. Use when coding features or fixes inside plan scope.
---

# Implement Conduct

**Role**: `builder` · **P5** · Execute

**Prerequisite**: `implement-reference` complete; ready for Do = yes.

## Workflow

1. Acceptance criteria 1 件ずつ → ファイル対応
2. **TDD**: follow [`../lib-tdd-cycle/SKILL.md`](../lib-tdd-cycle/SKILL.md)
3. **AGENTS.md** + **rules/local/** implement lens
4. 既存命名・型に合わせ、diff 最小

## Checklist

- 変更は plan Scope / criterion にトレース
- Design Facts 尊重；Assumptions を Fact 扱いしない
- secrets / debug 残しなし

## Gaps

- spec gap → stop → **spec_designer**
- plan gap → stop → **plan_slicer**

## After

**reviewer** 向け: files、criteria mapping、検証手順。

## Do not

ユーザー未依頼の full review、design/plan 直編（`implement-record` 経由のみ）

詳細: [`references/standards.md`](references/standards.md)
