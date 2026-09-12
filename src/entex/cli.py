"""Command-line entry point.

Step 1 of the roadmap (charter §11): `entex render <json>` turns an IR file into a PDF.
The CLI owns "read the JSON file" and "print the result"; validation, derivation,
escaping and typesetting live in `entex.ir` / `entex.tex` / `entex.renderer`, which never
learn where the IR came from (charter §8).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Annotated, NoReturn

import typer

from entex import __version__
from entex.errors import (
    DerivationError,
    EnTeXError,
    EnvelopeError,
    IRValidationError,
    PackageError,
    RenderError,
)
from entex.ir.derive import apply_derived
from entex.ir.loader import load_and_validate
from entex.packages import default_packages_dir
from entex.renderer import build_tex
from entex.renderer import render as render_pdf

app = typer.Typer(help="EnTeX — form input to fixed-format PDF via LaTeX.", no_args_is_help=True)

# Binaries the renderer will shell out to. All must live inside the container.
REQUIRED_BINARIES = ("lualatex", "latexmk")

# 終了コード。0 以外は「誰が直すべきか」で分ける
EXIT_OK = 0
EXIT_INPUT_ERROR = 1  # 利用者: 封筒・中身の誤り
EXIT_RENDER_ERROR = 2  # 運用者: 組版失敗（詳細は out/ 配下のログ）
EXIT_PACKAGE_ERROR = 3  # テンプレート作者: doc-package の不備

DEFAULT_OUT_ROOT = Path("out") / "render"


@app.command()
def version() -> None:
    """Print the EnTeX version."""
    typer.echo(__version__)


@app.command()
def doctor() -> None:
    """Check that the TeX toolchain and Python runtime are usable."""
    ok = True
    typer.echo(f"python  : {sys.version.split()[0]}")
    for name in REQUIRED_BINARIES:
        path = shutil.which(name)
        if path is None:
            ok = False
            typer.echo(f"{name:<8}: MISSING")
            continue
        typer.echo(f"{name:<8}: {path}")

    if shutil.which("kpsewhich"):
        for pkg in ("luatexja.sty", "ltjsarticle.cls"):
            found = subprocess.run(
                ["kpsewhich", pkg], capture_output=True, text=True, check=False
            ).stdout.strip()
            if not found:
                ok = False
            typer.echo(f"{pkg:<16}: {found or 'MISSING'}")

    if not ok:
        typer.echo("doctor: FAIL — run inside the Docker image (see Makefile)", err=True)
        raise typer.Exit(code=1)
    typer.echo("doctor: OK")


@app.command()
def render(
    json_path: Annotated[
        Path,
        typer.Argument(
            help="IR の JSON ファイル（封筒 doc_type / schema_version / content を含む）",
            exists=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    out: Annotated[
        Path | None,
        typer.Option(
            "--out",
            "-o",
            help="出力先ディレクトリ（既定: out/render/<JSON のファイル名>/）",
            file_okay=False,
        ),
    ] = None,
    packages_dir: Annotated[
        Path | None,
        typer.Option(
            "--packages-dir",
            help="doc-package の置き場（既定: $ENTEX_PACKAGES_DIR → ./packages → リポジトリ直下）",
            file_okay=False,
        ),
    ] = None,
    tex_only: Annotated[
        bool,
        typer.Option(
            "--tex-only",
            help="latexmk を呼ばず .tex を書き出すだけにする（TeX が無い環境の確認用）",
        ),
    ] = False,
) -> None:
    """IR の JSON から PDF を生成し、PDF のパスを標準出力に出す。"""
    job_name = json_path.stem
    out_dir = out if out is not None else DEFAULT_OUT_ROOT / job_name
    pkg_dir = packages_dir if packages_dir is not None else default_packages_dir()

    try:
        raw = json.loads(json_path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        _fail("入力ファイルを UTF-8 として読めません。", EXIT_INPUT_ERROR)
    except ValueError as exc:
        _fail(
            f"入力ファイルを JSON として読めません（{exc.args[0] if exc.args else ''}）。",
            EXIT_INPUT_ERROR,
        )

    try:
        ir = load_and_validate(raw, pkg_dir)
        content = apply_derived(ir.content, ir.package.schema)
        if tex_only:
            out_dir.mkdir(parents=True, exist_ok=True)
            tex_path = out_dir / f"{job_name}.tex"
            tex_path.write_text(build_tex(content, ir.package), encoding="utf-8", newline="\n")
            typer.echo(str(tex_path))
            return
        pdf_path = render_pdf(content, ir.package, out_dir, job_name=job_name)
    except (EnvelopeError, IRValidationError) as exc:
        _fail(exc.user_message, EXIT_INPUT_ERROR)
    except (PackageError, DerivationError) as exc:
        _fail(exc.user_message, EXIT_PACKAGE_ERROR)
    except RenderError as exc:
        # TeX のログは exc.log_path にだけある。利用者向けの経路（標準出力・標準エラー）には出さない
        _fail(exc.user_message, EXIT_RENDER_ERROR)
    except EnTeXError as exc:  # pragma: no cover - 将来の分類漏れの安全網
        _fail(exc.user_message, EXIT_RENDER_ERROR)

    typer.echo(str(pdf_path))


def _fail(message: str, code: int) -> NoReturn:
    typer.echo(message, err=True)
    raise typer.Exit(code=code)
