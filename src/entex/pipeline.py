"""IR（raw dict）から PDF / `.tex` までの共通入口（api.md §3.1）。

CLI も API もここを呼ぶ。3 段（検証 → 導出 → 組版）の並びが 1 か所にしかないことで、
入口が違っても同じ IR から同じ `.tex` が出る（api.md FR-A8）。

ここが知っていること: 3 段の順序、ジョブ名の規則、出力ディレクトリの作り方。
知らないこと: IR の出どころ（ファイル / HTTP）、特定の文書種（charter §8）。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from entex import renderer
from entex.ir.derive import apply_derived
from entex.ir.loader import load_and_validate
from entex.packages import DocPackage

# latexmk の引数・ファイル名として安全な範囲（api.md §3.1）。先頭は英数字（`-` で始まると
# latexmk がオプションと誤認する）、64 文字まで
JOB_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
DEFAULT_JOB_NAME = "document"

_DISALLOWED_RUN = re.compile(r"[^A-Za-z0-9_-]+")
_REPEATED_SEPARATORS = re.compile(r"[-_]{2,}")


@dataclass(frozen=True, slots=True)
class PreparedIR:
    """検証済みで導出値も埋まった IR。組版に渡せる状態。"""

    doc_type: str
    schema_version: int
    package: DocPackage
    content: dict[str, Any]


@dataclass(frozen=True, slots=True)
class RenderResult:
    doc_type: str
    schema_version: int
    job_name: str
    out_dir: Path
    tex_path: Path
    pdf_path: Path | None  # tex_only のとき None


def normalize_job_name(stem: str) -> str:
    """任意の文字列（例: JSON のファイル名の stem）を `JOB_NAME_RE` に合う形へ寄せる。

    使えない文字の連なりは `-` 1 つに置き換え、先頭・末尾の `-` / `_` を落とし、64 文字に
    切り詰める。何も残らなければ `DEFAULT_JOB_NAME`。決定的（同じ入力には同じ出力）。
    """
    name = _DISALLOWED_RUN.sub("-", stem)
    name = _REPEATED_SEPARATORS.sub(lambda m: m.group(0)[0], name)
    name = name.strip("-_")
    name = name[:64].rstrip("-_")
    if not name:
        return DEFAULT_JOB_NAME
    assert JOB_NAME_RE.fullmatch(name), name
    return name


def prepare(raw: Any, packages_dir: Path) -> PreparedIR:
    """封筒 → パッケージ → 中身の検証に続けて導出値を埋める（FR1–FR5）。

    Raises:
        EnvelopeError / PackageError / IRValidationError / DerivationError:
            `load_and_validate` と `apply_derived` のものをそのまま上げる。
    """
    ir = load_and_validate(raw, packages_dir)
    content = apply_derived(ir.content, ir.package.schema)
    return PreparedIR(
        doc_type=ir.doc_type,
        schema_version=ir.schema_version,
        package=ir.package,
        content=content,
    )


def render_ir(
    raw: Any,
    packages_dir: Path,
    out_dir: Path,
    *,
    job_name: str = DEFAULT_JOB_NAME,
    tex_only: bool = False,
    timeout: float | None = None,
) -> RenderResult:
    """IR から `out_dir/<job_name>.tex`（と PDF）を作る。

    `job_name` が `JOB_NAME_RE` に合わなければ、何も書かずに `ValueError`（呼び出し側の
    プログラムミス。CLI は `normalize_job_name` を通してから渡す）。

    Raises:
        ValueError: `job_name` が規則外
        EnTeXError: 検証・導出・組版の失敗（`prepare` / `renderer` のものをそのまま上げる）
    """
    if not JOB_NAME_RE.fullmatch(job_name):
        raise ValueError(f"job_name {job_name!r} does not match {JOB_NAME_RE.pattern}")

    prepared = prepare(raw, packages_dir)
    tex_path = out_dir / f"{job_name}.tex"

    if tex_only:
        tex_source = renderer.build_tex(prepared.content, prepared.package)
        out_dir.mkdir(parents=True, exist_ok=True)
        tex_path.write_text(tex_source, encoding="utf-8", newline="\n")
        pdf_path: Path | None = None
    else:
        kwargs: dict[str, Any] = {"job_name": job_name}
        if timeout is not None:
            kwargs["timeout"] = timeout
        pdf_path = renderer.render(prepared.content, prepared.package, out_dir, **kwargs)

    return RenderResult(
        doc_type=prepared.doc_type,
        schema_version=prepared.schema_version,
        job_name=job_name,
        out_dir=out_dir,
        tex_path=tex_path,
        pdf_path=pdf_path,
    )
