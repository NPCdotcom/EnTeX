---
title: Example cloud platform topology
kind: design
phase: P3
scope_level: system
status: example
related_requirements: docs/requirements/sample-capability/要件.md
---

# Cloud platform（記入例 · 中立）

> **サンプル**: コピー後は `{{...}}` を置換。正本テンプレは `docs/design/_template/infrastructure/`。

## 目的

サンプル能力 `sample-capability` をホストする最小 AWS 構成の設計例。

## コンポーネント（例）

| コンポーネント | 技術 | 責務 |
|----------------|------|------|
| API | Lambda + API Gateway | REST エンドポイント |
| データ | DynamoDB | エクスポートメタデータ |

## 次

- [ ] 本ファイルをベースに `topology.md` 等 6 テンプレを埋める
- [ ] P3 ゲート → plan criteria に IaC 検証行
