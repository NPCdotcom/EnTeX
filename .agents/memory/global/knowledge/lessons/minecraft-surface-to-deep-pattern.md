---
id: lesson-minecraft-surface-to-deep-pattern
kind: knowledge
topic: lesson
owner: learning
status: active
created: 2026-06-27
promoted_at: 2026-06-28
tags: [minecraft, java-edition, game-engine, learning, surface-to-deep, mod-loader]
sources:
  - learning/minecraft/notes/m0-roadmap.md
  - learning/minecraft/notes/d2-block-updates-overview.md
  - learning/minecraft/notes/evaluations/2026-06-27-minecraft-trace-critique.md
  - learning/minecraft/notes/x12-ml-mod-loaders.md
  - learning/minecraft/notes/x15-ml-spike-comparison.md
---

# 教訓 — Minecraft Java: 表面 → 深部学習パターン

## Principle

Minecraft Java の仕組み学習は **Phase S（datapack JSON · 個別 Block/Entity クラス）→ Phase D（ServerLevel · 更新 · チャンク · AI）→ Phase X（自作 datapack · Mod）** の順が効率的。各深部トピックは **必ず Phase S で触れた 26.2 具体例** を根拠にする。

## Facts

- ブロック「更新」は **4 系統**（scheduled · neighbor · random · block entity）+ block event — 用語 `tick` が衝突しやすい
- `/tick rate`（TickRateManager）と `randomTickSpeed`（gamerule）は **別レバー**
- 自然 spawn は **biome JSON · SpawnPlacements · NaturalSpawner · mob cap** の 4 層
- 26.1+ 難読化廃止 — `decompiled/` 参照が Phase D の第一ソースになりうる（EULA 範囲内ローカルのみ）
- Mod Loader: Fabric は **Event + Mixin** · NeoForge は **DeferredRegister + IEventBus** — 最終的にバニラ `Registry` に載る
- 26.2 Item 登録は `Properties.setId(ResourceKey)` 必須（Fabric / NeoForge 共通）

## Decisions

- ロードマップ hub: `d2-block-updates-overview.md`
- ケース固定: Potent Sulfur · Sulfur Cube · sulfur_pool · Copper Golem
- 検証: `experiments/` datapack · `sources/local/26.2/decompiled/` · `~/Projects/mc-fabric-spike` / `mc-neoforge-spike`
- Wiki は補助 — 実装名はコードで確認

## Anti-patterns

- Wiki のみで random tick 圏を断定（実装名と不一致がありうる）
- Phase D に入る前に具体 JSON/クラスを置かない（抽象だけでは復習不能）
- Mod 開発を datapack より先に始める（型追加の前にデータ駆動を読む方が早い）
- Fabric Event と NeoForge IEventBus を同一視する

## Recall

minecraft · 26.2 · Phase S/D/X · 4 update systems · Potent Sulfur · Fabric · NeoForge · surface-to-deep

## Related

- 正本索引: `learning/minecraft/notes/00-index.md`
- ML 概観: `learning/minecraft/notes/x12-ml-mod-loaders.md`
- 4 系統表: `learning/minecraft/notes/d2-block-updates-overview.md`
