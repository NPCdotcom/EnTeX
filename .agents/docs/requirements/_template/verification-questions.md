---
title: Verification questions
kind: verification-questions
phase: P1
related_要求: 要求.md
related_要件: 要件.md
status: awaiting-answers
created: ""
gate_keeper: user
---

# 検証質問 — {topic}

**G12 · AI-DLC question-driven 準拠**

## ルール

1. **チャットで回答しない** — 本ファイルの `[Answer]:` にのみ記入
2. 各問は **A–E + Other**（該当なしは E）
3. 曖昧なまま `design-record` / `plan-record` → **block**
4. 全問回答後、Gate 節でユーザー **Approve and Continue**

正本フォーマット: skill `adaptive-lifecycle-plan` · `assets/question-file-template.md`

---

## Question 1: {title}

**Context**: （なぜこの問が必要か · 1 行）

A) …

B) …

C) …

D) …

E) Other — specify below

[Answer]:

---

## Question 2: {title}

**Context**:

A) …

B) …

C) …

D) …

E) Other — specify below

[Answer]:

---

## Gate

| 項目 | 状態 |
|------|------|
| 全 `[Answer]:` 記入 | [ ] |
| 矛盾・未解決が残る | [ ] なし / [ ] あり → Recycle |
| **Proposal** | Approve and Continue \| Request Changes |

**User decision**: _（署名 · 日付 · ISO-8601）_

**監査**: `memory-record` → `audit-log` に `verification_questions_approved`（refs: 本ファイル）
