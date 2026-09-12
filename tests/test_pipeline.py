"""plan `pipeline-and-cli`: CLI と API の共通入口 `entex.pipeline`。

AC1: render_ir / prepare / RenderResult があり、CLI は 3 段を直接呼ばない
AC2 (W1): ジョブ名の規則を pipeline が持つ
AC5: `.tex` の決定性を render_ir(tex_only=True) 経由でも確認
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from entex.errors import IRValidationError, RenderError
from entex.pipeline import (
    DEFAULT_JOB_NAME,
    JOB_NAME_RE,
    PreparedIR,
    RenderResult,
    normalize_job_name,
    prepare,
    render_ir,
)
from tests.conftest import EXAMPLES_DIR, REPO_ROOT, load_example

VALID = sorted(p.name for p in (EXAMPLES_DIR / "valid").glob("*.json"))


# --- AC1: 入口と構造 -------------------------------------------------------------


def test_prepare_returns_validated_and_derived_content(packages_dir: Path) -> None:
    prepared = prepare(load_example("valid/01-typical.json"), packages_dir)
    assert isinstance(prepared, PreparedIR)
    assert prepared.doc_type == "circle-monthly-report"
    assert prepared.schema_version == prepared.package.schema.schema_version
    # 導出値が埋まっている（FR4 の期待値。README 記載）
    assert prepared.content["activity_count"] == 5
    assert prepared.content["balance"] == 19_400


def test_prepare_raises_the_same_errors_as_the_loader(packages_dir: Path) -> None:
    with pytest.raises(IRValidationError):
        prepare(load_example("invalid/03-unknown-enum-and-negative-amount.json"), packages_dir)


def test_render_ir_tex_only_writes_tex_and_returns_result(
    tmp_path: Path, packages_dir: Path
) -> None:
    result = render_ir(
        load_example("valid/02-minimal.json"),
        packages_dir,
        tmp_path,
        job_name="minimal",
        tex_only=True,
    )
    assert isinstance(result, RenderResult)
    assert result.doc_type == "circle-monthly-report"
    assert result.job_name == "minimal"
    assert result.out_dir == tmp_path
    assert result.tex_path == tmp_path / "minimal.tex"
    assert result.pdf_path is None
    assert result.tex_path.is_file()
    assert "\\documentclass" in result.tex_path.read_text(encoding="utf-8")


def test_cli_goes_through_the_pipeline_only() -> None:
    """CLI が 3 段（検証・導出・組版）を直接 import していないこと（AC1）。"""
    src = (REPO_ROOT / "src" / "entex" / "cli.py").read_text(encoding="utf-8")
    for forbidden in (
        "from entex.ir.loader import",
        "from entex.ir.derive import",
        "from entex.renderer import",
    ):
        assert forbidden not in src, f"cli.py が pipeline を迂回している: {forbidden}"
    assert "from entex.pipeline import" in src


# --- AC2 (W1): ジョブ名の規則 -----------------------------------------------------------


@pytest.mark.parametrize("bad", ["-bad", "a b", "x%y", "", "日本語", "a" * 65, "_x", "a/b"])
def test_render_ir_rejects_unsafe_job_names(bad: str, tmp_path: Path, packages_dir: Path) -> None:
    with pytest.raises(ValueError):
        render_ir(
            load_example("valid/02-minimal.json"),
            packages_dir,
            tmp_path,
            job_name=bad,
            tex_only=True,
        )
    assert not any(tmp_path.iterdir()), "拒否したのに出力ディレクトリに何か書いている"


@pytest.mark.parametrize(
    ("stem", "expected"),
    [
        ("01-typical", "01-typical"),
        ("-dash", "dash"),
        ("pct%hash#", "pct-hash"),
        ("報告 8月", "8"),
        ("報告書", DEFAULT_JOB_NAME),
        ("", DEFAULT_JOB_NAME),
        ("a" * 80, "a" * 64),
        ("__init__", "init"),
    ],
)
def test_normalize_job_name(stem: str, expected: str) -> None:
    got = normalize_job_name(stem)
    assert got == expected
    assert JOB_NAME_RE.fullmatch(got)


def test_job_name_rule_matches_the_design() -> None:
    # api.md §3.1: ^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$
    assert JOB_NAME_RE.pattern == r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$"
    assert re.fullmatch(JOB_NAME_RE.pattern, DEFAULT_JOB_NAME)


# --- AC5: 決定性（render_ir 経由） --------------------------------------------------------


@pytest.mark.parametrize("name", VALID)
def test_render_ir_tex_is_deterministic(tmp_path: Path, packages_dir: Path, name: str) -> None:
    raw = load_example(f"valid/{name}")
    first = render_ir(raw, packages_dir, tmp_path / "a", tex_only=True).tex_path.read_text("utf-8")
    second = render_ir(raw, packages_dir, tmp_path / "b", tex_only=True).tex_path.read_text("utf-8")
    assert first == second


def test_render_ir_wraps_render_errors(
    tmp_path: Path, packages_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))  # latexmk が無い
    with pytest.raises(RenderError) as ei:
        render_ir(load_example("valid/02-minimal.json"), packages_dir, tmp_path / "out")
    assert ei.value.log_path is not None
