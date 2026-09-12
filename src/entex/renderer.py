"""`template.tex.j2` に流し込んで `.tex` を作り、latexmk で PDF にする（FR6・FR7）。

知っていること: doc-package の `template.tex.j2` の場所、Jinja2 の呼び出し規約（変数名・区切り・
フィルタ）、latexmk の呼び方。知らないこと: 特定の文書種、IR の出どころ、体裁の値。

TeX の出力（latexmk のログ）は `out_dir` の中にだけ残し、利用者向けの `RenderError.user_message`
には一切含めない（charter §4）。
"""

from __future__ import annotations

import datetime as _dt
import os
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError

from entex.errors import RenderError, RenderTimeoutError
from entex.ir.schema import FieldDef, Schema
from entex.packages import TEMPLATE_FILENAME, DocPackage
from entex.tex.escape import escape_content, escape_text

LATEXMK_LOG_FILENAME = "latexmk.log"
RENDER_ERROR_LOG_FILENAME = "render-error.log"
DEFAULT_TIMEOUT_SECONDS = 180

# --- Jinja2 ----------------------------------------------------------------


def make_environment(package_dir: Path) -> Environment:
    """TeX として読める区切り（`\\VAR{}` / `\\BLOCK{}` / 行頭 `%%` / `%#`）の Jinja2 環境。"""
    env = Environment(
        loader=FileSystemLoader(str(package_dir)),
        block_start_string=r"\BLOCK{",
        block_end_string="}",
        variable_start_string=r"\VAR{",
        variable_end_string="}",
        comment_start_string=r"\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=False,  # HTML 用の autoescape は使わない。値は渡す前に escape_content で済ませる
        undefined=StrictUndefined,
    )
    env.filters["group_digits"] = filter_group_digits
    env.filters["ja_month"] = filter_ja_month
    env.filters["ja_date"] = filter_ja_date
    return env


def filter_group_digits(value: int) -> str:
    """3 桁区切り。`-4800` → `-4,800`。"""
    return f"{int(value):,}"


def filter_ja_month(value: str) -> str:
    """`2026-08` → `2026年8月`。"""
    year, month = value.split("-", 1)
    return f"{int(year)}年{int(month)}月"


JA_WEEKDAYS = "月火水木金土日"  # datetime.weekday() の 0 = 月曜


def filter_ja_date(value: str, with_year: bool = True, with_weekday: bool = False) -> str:
    """`2026-08-03` → `2026年8月3日`。`with_year=False` で `8月3日`、`with_weekday=True` で
    `8月3日(月)` のように曜日を付ける（charter §5.2: 曜日は入力せず開催日から導く）。"""
    d = _dt.date.fromisoformat(value)
    text = f"{d.year}年{d.month}月{d.day}日" if with_year else f"{d.month}月{d.day}日"
    if with_weekday:
        text += f"({JA_WEEKDAYS[d.weekday()]})"
    return text


# --- コンテキスト --------------------------------------------------------------


def build_context(content: dict[str, Any], schema: Schema) -> dict[str, Any]:
    """テンプレートに渡す変数。`doc` は利用者の値（エスケープ済み）、`schema` は label 等。

    dict のままだと Jinja2 の `x.items` が dict のメソッドに解決されてしまう（`rich_text` の
    `block.items` や `list` の `items` 定義で踏む）ので、属性アクセスできる名前空間に変換する。

    `document` は IR の形（`sections` は dict、`extra_sections` は別の配列）のままではなく、
    節を **並べ済みの配列** にしてから渡す（`shape_documents`）。
    """
    escaped = shape_documents(escape_content(content, schema), schema)
    return {
        "doc": _to_namespace(escaped),
        "schema": _to_namespace(schema_context(schema)),
    }


def shape_documents(content: dict[str, Any], schema: Schema) -> dict[str, Any]:
    """`document` 型のフィールドを、テンプレート向けの形に並べ替えた **新しい** dict を返す。

    ir-type-vocabulary.md §5 の分担のうち `src/entex/` 側（節の順序の固定・宣言外の節の後置）を
    ここで果たす。`doc.<field>.sections` は `{ key?, heading, blocks }` の配列で、

    - 宣言節がスキーマの `sections[]` の順に並ぶ。IR に無い節も `blocks` が空の要素として入る
      （落とすか「特になし」と書くかは体裁の判断なのでテンプレートが決める。§2.8）。
      `heading` はスキーマの値（エスケープ済み）、`key` は宣言のキー
    - その後ろに `extra_sections` が入力の順序で続く。`heading` は利用者の値（エスケープ済み）で、
      `key` は持たない
    """
    out = dict(content)
    for name, fdef in schema.fields.items():
        if fdef.type == "document" and isinstance(content.get(name), dict):
            out[name] = _shape_document(content[name], fdef)
    return out


def _shape_document(value: dict[str, Any], fdef: FieldDef) -> dict[str, Any]:
    by_key: dict[str, Any] = value.get("sections", {})
    sections: list[dict[str, Any]] = [
        {
            "key": sdef.key,
            "heading": escape_text(sdef.heading),
            "blocks": list(by_key.get(sdef.key, {}).get("blocks", [])),
        }
        for sdef in fdef.sections or []
    ]
    sections.extend(
        {"heading": extra.get("heading", ""), "blocks": list(extra.get("blocks", []))}
        for extra in value.get("extra_sections", [])
    )
    return {"sections": sections}


def _to_namespace(value: Any) -> Any:
    if isinstance(value, dict):
        return SimpleNamespace(**{k: _to_namespace(v) for k, v in value.items()})
    if isinstance(value, list):
        return [_to_namespace(v) for v in value]
    return value


def schema_context(schema: Schema) -> dict[str, Any]:
    """テンプレートが使う `schema.json` の部分（title / label / enum 表示名）。エスケープ済み。"""

    def field(fdef: FieldDef) -> dict[str, Any]:
        d: dict[str, Any] = {"type": fdef.type, "label": escape_text(fdef.label or "")}
        if fdef.options:
            d["option_labels"] = {o.value: escape_text(o.label) for o in fdef.options}
        if fdef.fields:
            d["fields"] = {name: field(child) for name, child in fdef.fields.items()}
        if fdef.items is not None:
            d["items"] = field(fdef.items)
        if fdef.sections:
            d["sections"] = [
                {"key": s.key, "heading": escape_text(s.heading), "required": s.required}
                for s in fdef.sections
            ]
        return d

    return {
        "doc_type": schema.doc_type,
        "schema_version": schema.schema_version,
        "title": escape_text(schema.title),
        "fields": {name: field(fdef) for name, fdef in schema.fields.items()},
    }


# --- .tex の組み立て ------------------------------------------------------------


def build_tex(content: dict[str, Any], package: DocPackage) -> str:
    """`content`（検証済み・導出値込み）から `.tex` 文字列を作る。latexmk は呼ばない。

    テンプレートの誤り（未定義変数・構文）はパッケージ作者の問題なので、利用者には汎用文を、
    詳細は `RenderError.detail` に入れて呼び出し側がサーバ側ログへ書く。
    """
    if not package.template_path.is_file():
        raise RenderError(
            detail=f"{TEMPLATE_FILENAME} not found in {package.dir}",
        )
    env = make_environment(package.dir)
    try:
        template = env.get_template(TEMPLATE_FILENAME)
        return template.render(**build_context(content, package.schema))
    except TemplateError as exc:
        raise RenderError(detail=f"template error: {type(exc).__name__}: {exc}") from exc


# --- latexmk ----------------------------------------------------------------


def render(
    content: dict[str, Any],
    package: DocPackage,
    out_dir: Path,
    *,
    job_name: str = "document",
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> Path:
    """`.tex` を `out_dir/<job_name>.tex` に書き、latexmk で PDF にしてそのパスを返す。

    Raises:
        RenderError: 組み立てまたは組版に失敗。生ログは `out_dir` 内にだけ残る。
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    error_log = out_dir / RENDER_ERROR_LOG_FILENAME
    latexmk_log = out_dir / LATEXMK_LOG_FILENAME

    try:
        tex_source = build_tex(content, package)
    except RenderError as exc:
        _write_log(error_log, exc.detail or "")
        raise RenderError(log_path=error_log, detail=exc.detail) from exc

    tex_path = out_dir / f"{job_name}.tex"
    tex_path.write_text(tex_source, encoding="utf-8", newline="\n")

    latexmk = shutil.which("latexmk")
    if latexmk is None:
        _write_log(error_log, "latexmk not found on PATH")
        raise RenderError(log_path=error_log, detail="latexmk not found on PATH")

    cmd = [
        latexmk,
        "-lualatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-output-directory={out_dir.resolve()}",
        # `./` を前置し、ファイル名がオプションと誤認されないようにする（job_name の規則は
        # pipeline 側が守るが、ここでも二重に安全側へ寄せる）
        f"./{tex_path.name}",
    ]
    env = dict(os.environ)
    # style/ 配下の .sty を TeX に見つけさせる。TEXINPUTS は末尾が区切りで終わると既定の
    # 探索パスを続けて見る。既存の値が区切りで終わっていなくても、こちらで必ず終端する
    inherited = env.get("TEXINPUTS", "")
    if inherited and not inherited.endswith(os.pathsep):
        inherited += os.pathsep
    env["TEXINPUTS"] = (
        f"{package.style_dir.resolve()}{os.pathsep}{package.dir.resolve()}{os.pathsep}{inherited}"
    )
    try:
        proc = subprocess.run(
            cmd,
            cwd=out_dir,
            env=env,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout
        if isinstance(partial, bytes):  # text=True でも bytes で来る Python 版がある
            partial = partial.decode("utf-8", "replace")
        _write_log(latexmk_log, f"latexmk timed out after {timeout}s\n{partial or ''}")
        raise RenderTimeoutError(
            log_path=latexmk_log, detail=f"latexmk timed out after {timeout}s"
        ) from exc

    _write_log(latexmk_log, proc.stdout + ("\n" if proc.stderr else "") + proc.stderr)
    pdf_path = out_dir / f"{job_name}.pdf"
    if proc.returncode != 0 or not pdf_path.is_file():
        raise RenderError(log_path=latexmk_log, detail=f"latexmk exit {proc.returncode}")
    return pdf_path


def _write_log(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
