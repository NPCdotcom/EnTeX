from __future__ import annotations

import json
import os
import shutil
import stat
from pathlib import Path

import pytest
from typer.testing import CliRunner

from entex import __version__
from entex.cli import EXIT_INPUT_ERROR, EXIT_PACKAGE_ERROR, EXIT_RENDER_ERROR, app
from tests.conftest import EXAMPLES_DIR, load_example, requires_tex
from tests.test_renderer import assert_no_tex_vocabulary

runner = CliRunner()


def test_version_prints_package_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


@requires_tex
def test_doctor_passes_inside_tex_image() -> None:
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0, result.stdout
    assert "doctor: OK" in result.stdout


# --- render: 入力側の失敗（TeX 不要） -------------------------------------------------


def test_render_reports_validation_errors_in_japanese(tmp_path: Path) -> None:
    src = EXAMPLES_DIR / "invalid" / "03-unknown-enum-and-negative-amount.json"
    result = runner.invoke(app, ["render", str(src), "--out", str(tmp_path)])
    assert result.exit_code == EXIT_INPUT_ERROR
    assert result.stdout == ""
    assert "入力に2件の問題があります" in result.stderr
    assert "会計明細 1行目の区分は 収入 / 支出 のいずれかを選んでください" in result.stderr
    assert "会計明細 2行目の金額は0以上で入力してください" in result.stderr


def test_render_reports_envelope_error_only(tmp_path: Path) -> None:
    src = EXAMPLES_DIR / "invalid" / "06-envelope-mismatch.json"
    result = runner.invoke(app, ["render", str(src), "--out", str(tmp_path)])
    assert result.exit_code == EXIT_INPUT_ERROR
    assert "schema_version" in result.stderr
    assert "報告対象月" not in result.stderr


def test_render_rejects_non_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    result = runner.invoke(app, ["render", str(bad), "--out", str(tmp_path / "out")])
    assert result.exit_code == EXIT_INPUT_ERROR
    assert "JSON" in result.stderr


def test_render_missing_file_is_a_usage_error(tmp_path: Path) -> None:
    result = runner.invoke(app, ["render", str(tmp_path / "nope.json")])
    assert result.exit_code != 0


def test_render_broken_package_is_a_package_error(tmp_path: Path) -> None:
    pkgs = tmp_path / "packages"
    (pkgs / "circle-monthly-report").mkdir(parents=True)
    (pkgs / "circle-monthly-report" / "schema.json").write_text("[]", encoding="utf-8")
    src = EXAMPLES_DIR / "valid" / "01-typical.json"
    result = runner.invoke(
        app, ["render", str(src), "--out", str(tmp_path / "out"), "--packages-dir", str(pkgs)]
    )
    assert result.exit_code == EXIT_PACKAGE_ERROR
    assert "circle-monthly-report" in result.stderr


def test_render_tex_only_writes_tex_without_latexmk(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))  # latexmk が無くても動く
    src = EXAMPLES_DIR / "valid" / "01-typical.json"
    result = runner.invoke(app, ["render", str(src), "--out", str(tmp_path), "--tex-only"])
    assert result.exit_code == 0, result.stderr
    tex_path = Path(result.stdout.strip())
    assert tex_path == tmp_path / "01-typical.tex"
    assert "青葉大学 軽音楽サークル" in tex_path.read_text(encoding="utf-8")


# --- FR7 at the CLI boundary（偽の latexmk） -------------------------------------------


def test_render_failure_hides_tex_log_from_user(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    bin_dir = tmp_path / "fakebin"
    bin_dir.mkdir()
    fake = bin_dir / "latexmk"
    fake.write_text(
        "#!/bin/sh\n"
        "echo '! LaTeX Error: File `missing.sty` not found.'\n"
        "echo '! Emergency stop.'\n"
        "exit 12\n",
        encoding="utf-8",
    )
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")

    src = EXAMPLES_DIR / "valid" / "01-typical.json"
    out_dir = tmp_path / "out"
    result = runner.invoke(app, ["render", str(src), "--out", str(out_dir)])
    assert result.exit_code == EXIT_RENDER_ERROR
    assert_no_tex_vocabulary(result.stdout)
    assert_no_tex_vocabulary(result.stderr)
    assert "PDFの生成に失敗しました" in result.stderr
    assert "LaTeX Error" in (out_dir / "latexmk.log").read_text(encoding="utf-8")


# --- FR8: 一連で PDF が出る（TeX 環境のみ） ---------------------------------------------


@requires_tex
def test_render_typical_prints_pdf_path(tmp_path: Path) -> None:
    src = EXAMPLES_DIR / "valid" / "01-typical.json"
    result = runner.invoke(app, ["render", str(src), "--out", str(tmp_path)])
    assert result.exit_code == 0, result.stderr
    pdf = Path(result.stdout.strip())
    assert pdf == tmp_path / "01-typical.pdf"
    assert pdf.is_file() and pdf.read_bytes().startswith(b"%PDF-")


@requires_tex
def test_render_default_out_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    shutil.copytree(EXAMPLES_DIR.parent, tmp_path / "packages" / "circle-monthly-report")
    src = tmp_path / "02-minimal.json"
    src.write_text(json.dumps(load_example("valid/02-minimal.json")), encoding="utf-8")
    result = runner.invoke(app, ["render", str(src)])
    assert result.exit_code == 0, result.stderr
    assert Path(result.stdout.strip()) == Path("out/render/02-minimal/02-minimal.pdf")
    assert (tmp_path / "out/render/02-minimal/02-minimal.pdf").is_file()
