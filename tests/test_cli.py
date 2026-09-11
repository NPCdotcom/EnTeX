import shutil

import pytest
from typer.testing import CliRunner

from entex import __version__
from entex.cli import app

runner = CliRunner()


def test_version_prints_package_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


@pytest.mark.skipif(shutil.which("lualatex") is None, reason="TeX toolchain only inside Docker")
def test_doctor_passes_inside_tex_image() -> None:
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0, result.stdout
    assert "doctor: OK" in result.stdout
