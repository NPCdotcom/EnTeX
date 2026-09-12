---
id: 2026-09-12-charter-markdown-input-issue-14
date: 2026-09-12
scope: project
tags: [charter, P0, H0, doc-type, markdown, issue-14, club-meeting-log]
---

# Episode: charter revision for issue #14 (部会ログ実測 → front matter + Markdown 入力)

## Input

User: 「このプロジェクトの現状を把握したうえで、issue #14 を解決するために charter を改訂して。」

Context at turn start: local checkout was 21 commits behind `origin/main` (PR #10 pipeline, PR #13 pivot/ADR-0001). Fetched and reset to `origin/main@6813982` before editing. Issue #14 (by Aster) supplies the concrete 部会ログ format that ADR-0001 / nav `blockers` were waiting for: 47 real logs (2024/5–2026/7, Notion → Markdown), 3 meta props, sections converge to アナウンス44 / 活動報告34 / 次回予告4, 0 tables, images concentrated in recent sessions, session-number headings visibly inconsistent.

## Done

- `docs/design/product/charter.md` (single commit `f55091d`, `docs:` prefix):
  - §1 one-liner: Markdown added as an input means (kept フォーム; rationale in an Aster dialog note).
  - §3: user row rewritten from the 47-log census; long dialog note with the measured facts (meta / sections / blocks / heading drift / images).
  - §5: input = front matter + Markdown file for now (着手順3), フォーム stays at 着手順4; MVP = `club-meeting-log`, 画像なしの過去ログ first. New **§5.1** with the input example and the 3 rules (heading level not validated but order fixed; extra sections allowed after declared ones; sub-headings free) + Pandoc contrast + renderer sees only blocks.
  - §6: 「体裁上まったく同一」 replaced by explicit criteria (declared sections & order · meta formatting · heading hierarchy & block appearance · line/page count excluded). Judgment of the zero-change criterion only with **real** doc-types; `circle-monthly-report` doesn't count; `packages/` vs `src/entex/` owner split noted (canonical → TEAM.md, not yet written). Note that `document` type / importer / block expansion in `src/entex/` is a vocabulary change, not a doc-type addition.
  - §8: `data-import` loses 「後回し」; Markdown import is the first input path; separation from `renderer` unchanged (ir-type-vocabulary §2.2 applied).
  - §9: Pandoc row. §10: terms front matter / 本文(document) / 節 / block; note on Notion 雛形 sense of 「テンプレート」.
  - §11: 様式待ち and package question moved to 決着済み (new `club-meeting-log`, 1つ目の差し替え); new 決着済み entry for the input format with rejected alternatives; new Open items (image storage/reference, Markdown subset & Notion-specific syntax, whether to keep allowing extra sections). 着手順3 split into 3a (club-meeting-log: document type, importer, block TeX, then image) / 3b (real 2nd doc-type + §6 judgment). Step 1 marked done (PR #8).
  - Facts/Assumptions updated (census as Facts; heading drift is now a fact; "利用者は困っている" and "Markdown を書ける" stay assumptions; removed the 「様式待ち」 assumption).
- Memory: this episode, `nav.yaml`, `index.yaml`, `docs/project-state.yaml` `open_blockers` (様式待ち resolved).

## Decisions (as recorded in charter; agreement = PR review/merge by NPC & Aster)

- Input format: front matter + Markdown body with sections declared by the package (issue #14 §2 → charter §5.1).
- `club-meeting-log` is a **new** package and replaces the 1st doc-type; `circle-monthly-report` stays as reference and does not count for §6.
- Scope of this turn deliberately limited to the charter (user's request). `ir-type-vocabulary.md` (`document` type, `image` → 「次に入れる」), ADR-0001 open-question closure, `docs/TEAM.md` owner split, and follow-up implementation issues are **not** in this PR.

## Open / risks

- Branch `cursor/charter-issue-14-markdown-input-9732` follows the cloud-agent template, not AGENTS.md `<issue>/<owner>/<topic>` (same standing note as earlier turns).
- Charter now links to `ir-type-vocabulary.md` for the `document` type which that doc does not yet define — follow-up PR needed to avoid a dangling reference in meaning (link itself resolves).
- Dialog notes attributed to Aster paraphrase issue #14 text; Aster should confirm wording in review.

## Next

- Follow-up PR: `ir-type-vocabulary.md` — add `document` type (blocks heading/paragraph/list/quote/link/image; attrs sections/extra_sections/blocks/max_heading_level), move `image` from §7 「範囲外」 to 「次に入れる」, note `time`/小数/表 remain excluded (0 occurrences).
- Follow-up: ADR-0001 「Open questions」 → point to issue #14 answers (or ADR-0002 for the input-format decision). `docs/TEAM.md` owner split. Implementation issues for `packages/club-meeting-log/` (aster) and importer / `document` validation / block TeX (npc).
- Post `@coderabbitai review` on the PR.
