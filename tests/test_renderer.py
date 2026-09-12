"""FR5–FR7・NFR1–2: .tex の組み立て・latexmk 呼び出し・失敗時の利用者向けメッセージ。"""

from __future__ import annotations

import os
import re
import shutil
import stat
import time
from pathlib import Path

import pytest

from entex.errors import RenderError
from entex.ir.derive import apply_derived
from entex.ir.loader import load_and_validate
from entex.packages import DocPackage, load_package
from entex.renderer import (
    LATEXMK_LOG_FILENAME,
    build_tex,
    filter_group_digits,
    filter_ja_date,
    filter_ja_month,
    render,
)
from tests.conftest import EXAMPLES_DIR, load_example, requires_tex

# 利用者向けの経路に出てはいけない TeX の語彙（FR7）
TEX_VOCABULARY = (
    "! ",
    "LaTeX Error",
    "Undefined control sequence",
    "Emergency stop",
    "latexmk",
    "lualatex",
    ".tex",
    ".log",
    "Traceback",
)


def _content(name: str, packages_dir: Path) -> tuple[dict, DocPackage]:
    ir = load_and_validate(load_example(f"valid/{name}"), packages_dir)
    return apply_derived(ir.content, ir.package.schema), ir.package


def assert_no_tex_vocabulary(text: str) -> None:
    for word in TEX_VOCABULARY:
        assert word not in text, f"利用者向けの文に TeX の語彙 {word!r} が漏れている: {text!r}"


# --- フィルタ -----------------------------------------------------------------


def test_filters() -> None:
    assert filter_group_digits(138000) == "138,000"
    assert filter_group_digits(-4800) == "-4,800"
    assert filter_group_digits(0) == "0"
    assert filter_ja_month("2026-08") == "2026年8月"
    assert filter_ja_date("2026-08-03") == "2026年8月3日"
    assert filter_ja_date("2026-08-03", with_year=False) == "8月3日"


# --- FR5: 組み立てた .tex に生の特殊文字が残らない ---------------------------------


def test_built_tex_has_no_unescaped_specials(packages_dir: Path) -> None:
    content, package = _content("06-tex-special-chars.json", packages_dir)
    tex = build_tex(content, package)
    # 利用者の値が入る箇所を代表して確認
    assert r"R\&B研究会 \#2" in tex
    assert r"O\textquotesingle{}Brien" in tex
    assert r"\$10,000" in tex and r"85\%" in tex
    assert r"「A\_B」「C\textasciicircum{}D」「\{E\}」" in tex
    assert r"\textbackslash{} や \textasciitilde{}" in tex
    assert r"練習室 \textless{}B\textgreater{}" in tex
    # 特殊文字を含む利用者の値が、生のまま残っていない
    raw_values = (
        content["organization"],
        content["representative"]["name"],
        content["author"]["role"],
        content["summary"]["blocks"][0]["text"],
        *content["summary"]["blocks"][1]["items"],
        content["activities"][0]["title"],
        content["activities"][0]["place"],
        content["finance"][0]["item"],
        *content["next_month_plan"],
    )
    for raw in raw_values:
        assert any(ch in raw for ch in "&%$#_{}~^\\<>'"), raw
        assert raw not in tex, raw
    # テンプレートの制御構文が残っていない
    assert r"\VAR{" not in tex and r"\BLOCK{" not in tex and "%#" not in tex


def test_built_tex_uses_labels_and_derived_values(packages_dir: Path) -> None:
    content, package = _content("01-typical.json", packages_dir)
    tex = build_tex(content, package)
    assert "サークル月次活動報告書" in tex
    assert "138,000" in tex and "131,400" in tex and "19,400" in tex
    assert "2026年8月" in tex and "2026年9月5日" in tex
    assert "音楽練習室、会議室" in tex
    assert "\\documentclass" in tex and "\\end{document}" in tex


def test_optional_fields_can_be_absent(packages_dir: Path) -> None:
    content, package = _content("02-minimal.json", packages_dir)
    tex = build_tex(content, package)
    assert "当月の活動はありません" in tex
    assert "当月の収支はありません" in tex


# --- NFR2: 決定性 ---------------------------------------------------------------


@pytest.mark.parametrize("name", sorted(p.name for p in (EXAMPLES_DIR / "valid").glob("*.json")))
def test_build_tex_is_deterministic(packages_dir: Path, name: str) -> None:
    content, package = _content(name, packages_dir)
    first = build_tex(content, package)
    second = build_tex(content, package)
    assert first == second
    assert not re.search(r"20\d\d-\d\d-\d\dT\d\d:", first), "生成時刻らしき文字列が混ざっている"


# --- テンプレート側の誤り ----------------------------------------------------------


def _copy_package_with_template(tmp_path: Path, packages_dir: Path, template: str) -> DocPackage:
    dst = tmp_path / "circle-monthly-report"
    shutil.copytree(packages_dir / "circle-monthly-report", dst)
    (dst / "template.tex.j2").write_text(template, encoding="utf-8")
    return load_package(tmp_path, "circle-monthly-report")


def test_undefined_variable_in_template_is_a_render_error(
    tmp_path: Path, packages_dir: Path
) -> None:
    package = _copy_package_with_template(tmp_path, packages_dir, r"\VAR{doc.no_such_field}")
    content, _ = _content("02-minimal.json", packages_dir)
    with pytest.raises(RenderError) as ei:
        build_tex(content, package)
    assert_no_tex_vocabulary(ei.value.user_message)
    assert ei.value.detail and "no_such_field" in ei.value.detail


def test_missing_template_is_a_render_error(tmp_path: Path, packages_dir: Path) -> None:
    package = _copy_package_with_template(tmp_path, packages_dir, "")
    package.template_path.unlink()
    content, _ = _content("02-minimal.json", packages_dir)
    with pytest.raises(RenderError) as ei:
        render(content, package, tmp_path / "out")
    assert_no_tex_vocabulary(ei.value.user_message)
    assert ei.value.log_path is not None and ei.value.log_path.is_file()


# --- FR7: latexmk 失敗時に TeX ログが漏れない（偽の latexmk を PATH に置くのでホストでも走る） ---

FAKE_LATEXMK_OUTPUT = """Latexmk: This is Latexmk, John Collins, 7 Jan. 2023. Version 4.79.
./document.tex:12: Undefined control sequence.
l.12 undefinedcommand
! LaTeX Error: Something's wrong--perhaps a missing item.
! Emergency stop.
Latexmk: Errors, so I did not complete making targets
"""


@pytest.fixture
def fake_latexmk(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    bin_dir = tmp_path / "fakebin"
    bin_dir.mkdir()
    script = bin_dir / "latexmk"
    # 外部コマンドに頼らない（printf / echo はシェル組み込み）ので PATH が空でも動く
    lines = " ".join(f'"{line}"' for line in FAKE_LATEXMK_OUTPUT.splitlines())
    script.write_text(
        f"#!/bin/sh\nprintf '%s\\n' {lines}\necho 'stderr noise: ! LaTeX Error' >&2\nexit 12\n",
        encoding="utf-8",
    )
    script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return script


def test_latexmk_failure_keeps_tex_log_server_side(
    fake_latexmk: Path, tmp_path: Path, packages_dir: Path
) -> None:
    content, package = _content("01-typical.json", packages_dir)
    out_dir = tmp_path / "out"
    with pytest.raises(RenderError) as ei:
        render(content, package, out_dir, job_name="document")
    err = ei.value
    assert err.user_message == RenderError.GENERIC_MESSAGE
    assert_no_tex_vocabulary(err.user_message)
    assert_no_tex_vocabulary(str(err))
    # 原文はサーバ側ログにだけ残る
    assert err.log_path == out_dir / LATEXMK_LOG_FILENAME
    log = err.log_path.read_text(encoding="utf-8")
    assert "Undefined control sequence" in log and "stderr noise" in log
    # .tex 自体は書き出されている（運用者が再現できる）
    assert (out_dir / "document.tex").is_file()


def test_missing_latexmk_is_a_render_error(
    tmp_path: Path, packages_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))
    content, package = _content("02-minimal.json", packages_dir)
    with pytest.raises(RenderError) as ei:
        render(content, package, tmp_path / "out")
    assert_no_tex_vocabulary(ei.value.user_message)


# --- FR6 / NFR1: 実際に PDF を出す（TeX 環境のみ） -----------------------------------


@requires_tex
@pytest.mark.parametrize("name", sorted(p.name for p in (EXAMPLES_DIR / "valid").glob("*.json")))
def test_valid_examples_render_to_pdf(tmp_path: Path, packages_dir: Path, name: str) -> None:
    content, package = _content(name, packages_dir)
    pdf = render(content, package, tmp_path / "out", job_name=Path(name).stem)
    assert pdf.is_file() and pdf.stat().st_size > 1000
    assert pdf.read_bytes().startswith(b"%PDF-")


@requires_tex
def test_broken_template_fails_without_leaking_tex(tmp_path: Path, packages_dir: Path) -> None:
    template = (
        "\\documentclass{ltjsarticle}\n\\begin{document}\n\\undefinedcommand\n\\end{document}\n"
    )
    package = _copy_package_with_template(tmp_path, packages_dir, template)
    content, _ = _content("02-minimal.json", packages_dir)
    with pytest.raises(RenderError) as ei:
        render(content, package, tmp_path / "out")
    assert_no_tex_vocabulary(ei.value.user_message)
    assert ei.value.log_path is not None
    assert "Undefined control sequence" in ei.value.log_path.read_text(encoding="utf-8")


@requires_tex
def test_typical_render_finishes_within_budget(tmp_path: Path, packages_dir: Path) -> None:
    """NFR1 の目安計測。1 回目はフォントキャッシュ生成で遅くなり得るので 2 回目を測る。"""
    budget = float(os.environ.get("ENTEX_NFR1_SECONDS", "10"))
    content, package = _content("01-typical.json", packages_dir)
    render(content, package, tmp_path / "warm", job_name="warm")
    started = time.perf_counter()
    render(content, package, tmp_path / "timed", job_name="timed")
    elapsed = time.perf_counter() - started
    assert elapsed < budget, f"生成に {elapsed:.1f}s かかった（目安 {budget:.0f}s）"
