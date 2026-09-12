"""doc-package（`packages/<slug>/`）の場所の解決と読み込み。

`src/entex/` は特定の文書種を知らない。ここが読むのは `schema.json` の中身と
`template.tex.j2` の **存在** だけである（`style/` は任意。無ければ TeX の既定探索に任せる）。
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError

from entex.errors import PackageError
from entex.ir.schema import SLUG_RE, Schema

PACKAGES_DIR_ENV = "ENTEX_PACKAGES_DIR"
SCHEMA_FILENAME = "schema.json"
TEMPLATE_FILENAME = "template.tex.j2"
STYLE_DIRNAME = "style"


class PackageNotFoundError(PackageError):
    """`packages/<slug>/` が存在しない。封筒の `doc_type` の誤りとして利用者に返してよい。"""


@dataclass(frozen=True, slots=True)
class DocPackage:
    slug: str
    dir: Path
    schema: Schema

    @property
    def template_path(self) -> Path:
        return self.dir / TEMPLATE_FILENAME

    @property
    def style_dir(self) -> Path:
        return self.dir / STYLE_DIRNAME


def default_packages_dir() -> Path:
    """`packages/` の既定の場所。環境変数 → カレント → リポジトリのルートの順に探す。"""
    env = os.environ.get(PACKAGES_DIR_ENV)
    if env:
        return Path(env)
    cwd_candidate = Path.cwd() / "packages"
    if cwd_candidate.is_dir():
        return cwd_candidate
    return Path(__file__).resolve().parents[2] / "packages"


def is_valid_slug(slug: str) -> bool:
    return bool(SLUG_RE.match(slug))


def package_exists(packages_dir: Path, slug: str) -> bool:
    return is_valid_slug(slug) and (packages_dir / slug).is_dir()


def load_package(packages_dir: Path, slug: str) -> DocPackage:
    if not is_valid_slug(slug):
        # パスに混ぜる前に弾く（`../` などを `packages_dir` の外へ向けさせない）
        raise PackageNotFoundError(f"文書の種類 '{slug}' には対応していません。")
    pkg_dir = packages_dir / slug
    if not pkg_dir.is_dir():
        raise PackageNotFoundError(f"文書の種類 '{slug}' には対応していません。")

    schema_path = pkg_dir / SCHEMA_FILENAME
    if not schema_path.is_file():
        raise PackageError(f"文書種パッケージ '{slug}' に {SCHEMA_FILENAME} がありません。")
    try:
        raw = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise PackageError(
            f"文書種パッケージ '{slug}' の {SCHEMA_FILENAME} を読めません（JSON として不正）。"
        ) from exc
    try:
        schema = Schema.model_validate(raw)
    except ValidationError as exc:
        detail = "; ".join(_format_schema_error(e) for e in exc.errors())
        raise PackageError(
            f"文書種パッケージ '{slug}' の {SCHEMA_FILENAME} が不正です: {detail}"
        ) from exc
    if schema.doc_type != slug:
        raise PackageError(
            f"文書種パッケージ '{slug}' の doc_type（{schema.doc_type}）が"
            "ディレクトリ名と一致しません。"
        )
    # テンプレートの欠落はパッケージの不備なので、組版（RenderError）ではなくここで弾く
    if not (pkg_dir / TEMPLATE_FILENAME).is_file():
        raise PackageError(f"文書種パッケージ '{slug}' に {TEMPLATE_FILENAME} がありません。")
    return DocPackage(slug=slug, dir=pkg_dir, schema=schema)


def _format_schema_error(err: dict) -> str:
    loc = ".".join(str(p) for p in err.get("loc", ()))
    msg = str(err.get("msg", ""))
    # pydantic の ValueError 由来メッセージは "Value error, <本文>" の形で来る
    msg = msg.removeprefix("Value error, ")
    return f"{loc}: {msg}" if loc else msg
