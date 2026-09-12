from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGES_DIR = REPO_ROOT / "packages"
EXAMPLES_DIR = PACKAGES_DIR / "circle-monthly-report" / "examples"

requires_tex = pytest.mark.skipif(
    shutil.which("lualatex") is None or shutil.which("latexmk") is None,
    reason="TeX toolchain only inside Docker",
)


def load_example(relpath: str) -> Any:
    """`packages/circle-monthly-report/examples/<relpath>` を JSON として読む。"""
    return json.loads((EXAMPLES_DIR / relpath).read_text(encoding="utf-8"))


@pytest.fixture
def packages_dir() -> Path:
    return PACKAGES_DIR


@pytest.fixture
def examples_dir() -> Path:
    return EXAMPLES_DIR
