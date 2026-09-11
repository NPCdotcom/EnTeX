---
id: lesson-continuous-discovery-delegation
kind: knowledge
topic: lesson
owner: kit
status: active
created: 2026-06-22
tags: [product-dev, discovery, continuous-discovery, ost, p-07, delegation]
sources:
  - learning/product-dev/notes/scans/p-07-report.md
  - learning/product-dev/notes/scans/p-01-report.md
  - learning/product-dev/notes/optimization/o-10-remaining-closure.md
  - docs/design/_template/product/continuous-discovery-cadence.md
promoted_at: 2026-06-22
---

# 教訓 — continuous discovery はプロジェクト委任

## Principle

Teresa Torres の **五要素**（outcome · OST · weekly touchpoints · assumption tests · product trio）のうち、キットが担うのは **outcome/OST/仮説検証の橋** に限定する。**週次顧客タッチポイント**は `docs/design/product/continuous-discovery-cadence.md` へ **プロジェクト任意配置** — secretary-route や rules への常時注入はしない。

## Facts

- p-07: landscape 7 軸 · drill 4 — Track P 拡張完了
- o-10 で OST 軽量テンプレ済（`opportunity-solution-tree.md`）
- t-04 outcome · G13 outcome-check と接続
- 1-user trio = ユーザー（顧客の声）+ PM エージェント（機会整理）+ P3/P5（実現性）

## Decisions

- 週次リズムは「目安」表記 — B2B 等で過剰ならプロジェクトが調整
- インタビューメモは `docs/design/product/interviews/`（任意）
- 新要求は P1 Gate 後に `要求.md` へ昇格
- 外部リクルーティング SaaS はキット正本化しない

## Anti-patterns

- 全プロジェクトへの週次インタビュー強制
- AI 要約だけで機会判断（HITL 必須）

## Recall

continuous discovery · weekly touchpoints · OST · P0–P2 · p-07 · プロジェクトテンプレ
