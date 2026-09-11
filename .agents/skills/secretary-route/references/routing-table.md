# Secretary route — ルーティング表



**毎ターン先頭**: `context-guard` → `memory-reference`（**nav.yaml Phase 0**）→ `turn-brief` → **[Loop2]** `nav-brief` → `secretary-route`



正本: `docs/PM_ROUTING.md` · **G6**: [`workspace-detection.md`](workspace-detection.md)



## G1 入口（Workflow Planning）



| 条件 | 必須アクション |

|------|----------------|

| `lifecycle_plan.profile` が空 | **`adaptive-lifecycle-plan`**（G1 · o-01）→ ユーザー Go |

| workspace-detection が **初回 / 再計画 / brownfield** | 上記 or `brownfield-reference` |

| `lifecycle_plan` あり · intent 整合 | 通常ルーティング（下表） |



判定手順: **workspace-detection** → 必要なら adaptive → **turn-brief** に `recommended_cursor_mode` 引用。



| シグナル | Role | スキル順 | **Cursor mode**（G11） | Cursor 補助 | PM禁止 |

|----------|------|----------|------------------------|-------------|--------|

| **入口 · 工程不明 · scope 大変更** | `router` / `spec_designer` | workspace-detection → memory-reference(nav) → **adaptive-lifecycle-plan** → 下表 | **Ask→Plan**（`lifecycle_plan` 優先） | WebSearch+browser | 独力で全 P 実行 |

| 要求・要件・設計 | `spec_designer` | memory-reference(nav) → **landscape-research**（探索）→ terminology-research → design-* | **Ask→Plan** | WebSearch scan+drill / browser | design-record 自前 |

| 実装計画 | `plan_slicer` | memory-reference(nav) → terminology-research → plan-* | **Plan** | WebSearch+browser | plan-record 自前 |

| 方針・キット調査 | `kit_maintainer` / PM | memory-reference(nav) → **landscape-research** | **Ask** | WebSearch scan+drill | — |

| 計画 Do | `builder` | memory-reference(nav) → implement-* | **Agent** | Shell / browser | implement-conduct 自前 |

| 小バグ | `hotfixer` | memory-reference(nav) → patch-* | **Agent** | Shell | patch 自前 |

| Automation | `automator` | memory-reference(nav) → automation-* | **Agent** | Shell | draft 実行 |

| レビュー | `reviewer` | memory-reference(nav) → review-* | **Agent**（失敗時 **Debug**） | Shell / browser | review-conduct 自前 |

| 評価 | `evaluator` | memory-reference(nav) → evaluate-* | **Ask** | Read / Shell | 評価独力 |

| キット | `kit_maintainer` | memory-reference(nav) → **landscape-research** → maintain-* | **Plan→Agent** | Read/Write `.agents/` | キット独力 |

| Operations（任意） | `router` / PM | P6 後 · deploy/runbook 記録 | **Agent** | Shell | キット外 Cloud は別 WF |

| 挨拶のみ | — | context-guard → nav 最小 → turn-brief → 短答（**軽量ループ** · evaluate skip） | — | — | Loop2 skip |



**mode 列の優先**: `lifecycle_plan.recommended_cursor_mode` > 上表デフォルト · turn-brief / nav-brief に引用。



## 判定・ゲート



hotfixer vs builder · spec_designer vs plan_slicer · lifecycle block → ユーザー確認 · **Loop2 不明 → nav-brief 実行**



実行: **role-execute** · 終端: evaluate (full/mini/skip) → **memory-flush** → **memory-record**（**nav.yaml 必更新**）

