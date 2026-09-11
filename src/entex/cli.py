"""Command-line entry point.

Step 1 of the roadmap (charter §11) is a CLI that turns JSON into a PDF.
For now this module only carries environment checks; `render` lands with
the first doc-package.
"""

from __future__ import annotations

import shutil
import subprocess
import sys

import typer

from entex import __version__

app = typer.Typer(help="EnTeX — form input to fixed-format PDF via LaTeX.", no_args_is_help=True)

# Binaries the renderer will shell out to. All must live inside the container.
REQUIRED_BINARIES = ("lualatex", "latexmk")


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
