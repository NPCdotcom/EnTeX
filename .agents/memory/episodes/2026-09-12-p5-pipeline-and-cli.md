---
id: 2026-09-12-p5-pipeline-and-cli
date: 2026-09-12
scope: project
tags: [implement, P5, H4, pipeline, cli, feature/npc, W1, W2, S1, S3]
---

# Episode: P5 Do of plan `pipeline-and-cli` (roadmap step 2, first half)

## Input

User:「pipeline-and-cli の P5 実装に進めてください。」 No branch given → continued on `feature/npc` (PR #10). Context was summarized once mid-turn; re-anchored from nav.yaml, the plan, and source.

## Done (TDD: Red → Green → Refactor)

- **Red** `tests/test_pipeline.py`: AC1 (prepare / render_ir / RenderResult; CLI import grep), AC2 (`ValueError` on 8 unsafe job names, `normalize_job_name` table, regex equals api.md §3.1), AC5 (determinism via `render_ir(tex_only=True)` for all valid examples; RenderError wrapping when latexmk missing).
- **Green**
  - `src/entex/pipeline.py` (new): `JOB_NAME_RE`, `DEFAULT_JOB_NAME="document"`, `normalize_job_name`, `PreparedIR`, `RenderResult`, `prepare`, `render_ir`. Validates `job_name` **before** touching `out_dir`; `timeout=None` → renderer default.
  - `src/entex/cli.py`: imports only `entex.pipeline` (+ errors/packages). `out_dir = out/render/<stem>/` unchanged; `job_name = normalize_job_name(stem)`. Exit codes / stdout / stderr unchanged.
  - `src/entex/packages.py`: `load_package()` raises `PackageError` when `template.tex.j2` is missing (W2); docstring corrected (`style/` optional).
  - `src/entex/renderer.py`: latexmk arg `./<job>.tex` (W1 belt-and-braces); `TEXINPUTS` always ends with `os.pathsep` even when inherited value lacks it (S3).
- **Tests updated/added**: `test_missing_template_is_a_package_error` (load_package) + `test_build_tex_still_guards_against_a_vanished_template` (safety net stays RenderError); `recording_latexmk` fixture → `test_texinputs_keeps_default_path`, `test_texinputs_without_inherited_value_ends_with_separator`, `test_tex_filename_is_passed_with_dot_slash`; CLI: `test_render_missing_template_is_a_package_error` (exit 3, no out dir created), `ODD_FILENAMES` (`-dash`→`dash`, `pct%hash#`→`pct-hash`, `報告 8月`→`8`, `報告書`→`document`) for `--tex-only` and `@requires_tex` PDF, `test_render_default_out_dir_keeps_original_stem`.
- **Docs (S1)**: renderer.md diagram (pipeline.py hub), IF table (real signatures incl. packages / ir.schema / ir.validate / pipeline), error table (5 classes + CLI exit codes). README CLI section: exit 3 examples, job-name normalization examples, flow includes pipeline.py. `status` of renderer.md untouched.
- **Verification**: `ruff format` / `make lint` pass; `make test` 168 passed, 0 skipped (TeX Live on host, so the 4 odd-filename PDF tests ran).
- **Record**: plan AC1–AC5 ticked with test names; Do row + Progress row; Open question (PDF name) resolved as recommended. `docs/project-state.yaml` → `current_phase: P5`, proposal P5→P6 Check. plans/README row.

## Decisions

- AC2 example `pct-hash-.tex` → implemented `pct-hash.tex` (trailing separators stripped; still within `JOB_NAME_RE`). Noted in plan Do row.
- `PackageError` for the missing template names `template.tex.j2` on purpose (author-facing, exit 3); the TeX-vocabulary check applies to user-facing `RenderError` messages only.
- Kept `build_tex`'s own missing-template check as a safety net for hand-built `DocPackage`.

## Commits (feature/npc)

`d5675ab fix:template.tex.j2の欠落…` · `9f596ff fix:latexmkへの.tex引数に./を前置…` · `8da1fd8 feat:検証・導出・組版の共通入口entex.pipeline…` · `4fd5944 test:pipelineのジョブ名規則…` · `644edb0 docs:renderer.mdのIF表・図とREADME…` · + record commit.

## Next

- User decides: P6 Check of pipeline-and-cli now, or go on to P5 `api-render` and review both together.
- Post `@coderabbitai review` on PR #10.
