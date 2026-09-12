"""ルート（api.md §3.2）。`POST /v1/render` / `GET /v1/health` / `GET /v1/doc-types*`。

latexmk を呼ぶ `render` は **同期 `def`** で書く（FastAPI がスレッドプールで動かす。api.md §3.4）。
本文の読み取り（415 / 413 / 400）は非同期の依存 `read_ir_body` が担う。
"""

from __future__ import annotations

import json
import logging
import math
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Annotated, Any
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse

from entex import __version__
from entex.api.problems import (
    BAD_REQUEST,
    BUSY,
    CONTENT_TOO_LARGE,
    IR_INVALID,
    NOT_FOUND,
    PACKAGE_BROKEN,
    RENDER_FAILED,
    REQUEST_ID_HEADER,
    UNSUPPORTED_MEDIA_TYPE,
    ProblemError,
    openapi_problem_responses,
    problem_from_entex_error,
    request_id_of,
)
from entex.api.settings import Settings
from entex.errors import EnTeXError, RenderError
from entex.packages import (
    SCHEMA_FILENAME,
    PackageNotFoundError,
    is_valid_slug,
    load_package,
)
from entex.pipeline import DEFAULT_JOB_NAME, render_ir
from entex.renderer import LATEXMK_LOG_FILENAME, RENDER_ERROR_LOG_FILENAME

logger = logging.getLogger("entex.api")

router = APIRouter(prefix="/v1")

REQUIRED_BINARIES = ("lualatex", "latexmk")
REQUIRED_TEX_FILES = ("luatexja.sty",)


def _settings(request: Request) -> Settings:
    return request.app.state.settings


# --- 本文の読み取り（415 / 413 / 400） --------------------------------------------------------


def _is_json_media_type(content_type: str) -> bool:
    media = content_type.split(";", 1)[0].strip().lower()
    return media == "application/json" or media.endswith("+json")


async def read_ir_body(request: Request) -> dict[str, Any]:
    """HTTP 本文を「JSON のオブジェクト」として読む。中身の検証はしない（pipeline の仕事）。"""
    settings = _settings(request)
    content_type = request.headers.get("content-type")
    if content_type and not _is_json_media_type(content_type):
        raise ProblemError(UNSUPPORTED_MEDIA_TYPE)

    too_large = ProblemError(
        CONTENT_TOO_LARGE,
        f"本文が上限（{settings.max_body_bytes:,} バイト）を超えています。",
    )
    declared = request.headers.get("content-length")
    if declared and declared.isdigit() and int(declared) > settings.max_body_bytes:
        raise too_large
    body = await request.body()
    if len(body) > settings.max_body_bytes:
        raise too_large

    try:
        raw = json.loads(body)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ProblemError(BAD_REQUEST) from exc
    if not isinstance(raw, dict):
        raise ProblemError(
            BAD_REQUEST,
            '入力はオブジェクト（{ "doc_type": ..., "schema_version": ..., "content": { ... } }）'
            "である必要があります。",
        )
    return raw


# --- POST /v1/render ---------------------------------------------------------------------


@router.post(
    "/render",
    summary="IR から PDF を生成する",
    response_class=Response,
    responses={
        200: {
            "description": "生成した PDF",
            "content": {"application/pdf": {"schema": {"type": "string", "format": "binary"}}},
            "headers": {
                "Content-Disposition": {
                    "description": 'attachment; filename="<doc_type>.pdf"; '
                    "filename*=UTF-8''<title>.pdf",
                    "schema": {"type": "string"},
                },
                REQUEST_ID_HEADER: {"schema": {"type": "string", "format": "uuid"}},
            },
        },
        **openapi_problem_responses(
            BAD_REQUEST,
            CONTENT_TOO_LARGE,
            UNSUPPORTED_MEDIA_TYPE,
            IR_INVALID,  # 422 は envelope-mismatch と ir-invalid の 2 種
            RENDER_FAILED,  # 500 は package-broken / render-failed / render-timeout の 3 種
            BUSY,
        ),
    },
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Envelope"},
                }
            },
        }
    },
)
def render(request: Request, raw: Annotated[dict[str, Any], Depends(read_ir_body)]) -> Response:
    settings = _settings(request)
    request_id = request_id_of(request)
    semaphore = request.app.state.render_semaphore

    if not semaphore.acquire(timeout=settings.queue_wait_seconds):
        retry_after = max(1, math.ceil(settings.queue_wait_seconds) or 1)
        raise ProblemError(BUSY, headers={"Retry-After": str(retry_after)})
    try:
        return _render_one(raw, settings, request_id)
    finally:
        semaphore.release()


def _render_one(raw: dict[str, Any], settings: Settings, request_id: str) -> Response:
    """1 リクエスト = 1 一時ディレクトリ。応答を作ったら消す（失敗時は設定で残せる）。"""
    if settings.work_dir is not None:
        settings.work_dir.mkdir(parents=True, exist_ok=True)
    job_dir = Path(tempfile.mkdtemp(prefix="entex-", dir=settings.work_dir))
    keep = False
    try:
        try:
            result = render_ir(
                raw,
                settings.packages_dir,
                job_dir,
                job_name=DEFAULT_JOB_NAME,
                timeout=settings.render_timeout,
            )
        except EnTeXError as exc:
            if isinstance(exc, RenderError):
                _log_render_failure(job_dir, request_id)
                keep = settings.keep_failed_jobs
            return problem_from_entex_error(exc, request_id)

        assert result.pdf_path is not None
        pdf = result.pdf_path.read_bytes()
        title = load_package(settings.packages_dir, result.doc_type).schema.title
        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": content_disposition(result.doc_type, title),
                REQUEST_ID_HEADER: request_id,
            },
        )
    finally:
        if keep:
            logger.error("kept failed job dir request_id=%s: %s", request_id, job_dir)
        else:
            shutil.rmtree(job_dir, ignore_errors=True)


def content_disposition(doc_type: str, title: str) -> str:
    """ASCII の `filename` と UTF-8 の `filename*`（RFC 6266 §4.3 / RFC 8187）。"""
    ascii_name = f"{doc_type}.pdf"
    utf8_name = quote(f"{title}.pdf", safe="")
    return f"attachment; filename=\"{ascii_name}\"; filename*=UTF-8''{utf8_name}"


def _log_render_failure(job_dir: Path, request_id: str) -> None:
    """latexmk / テンプレートの生ログをサーバ側ログにだけ流す（charter §4）。"""
    for name in (LATEXMK_LOG_FILENAME, RENDER_ERROR_LOG_FILENAME):
        path = job_dir / name
        if path.is_file():
            logger.error(
                "%s request_id=%s:\n%s",
                name,
                request_id,
                path.read_text(encoding="utf-8", errors="replace"),
            )


# --- GET /v1/health ----------------------------------------------------------------------


@router.get(
    "/health",
    summary="ツールチェーンの有無（readiness）",
    responses={
        200: {"description": "lualatex / latexmk / luatexja.sty がそろっている"},
        503: {"description": "いずれかが見つからない"},
    },
)
def health(request: Request) -> JSONResponse:
    toolchain = toolchain_status()
    ok = all(toolchain.values())
    return JSONResponse(
        content={
            "status": "ok" if ok else "degraded",
            "version": __version__,
            "toolchain": toolchain,
        },
        status_code=200 if ok else 503,
        headers={REQUEST_ID_HEADER: request_id_of(request)},
    )


def toolchain_status() -> dict[str, str | None]:
    """`entex doctor` と同じ確認。値は見つかった場所（無ければ None）。"""
    status: dict[str, str | None] = {name: shutil.which(name) for name in REQUIRED_BINARIES}
    kpsewhich = shutil.which("kpsewhich")
    for tex_file in REQUIRED_TEX_FILES:
        found: str | None = None
        if kpsewhich:
            proc = subprocess.run(
                [kpsewhich, tex_file], capture_output=True, text=True, check=False, timeout=30
            )
            found = proc.stdout.strip() or None
        status[tex_file] = found
    return status


# --- GET /v1/doc-types ---------------------------------------------------------------------


@router.get(
    "/doc-types",
    summary="使える文書種の一覧",
    responses={200: {"description": "packages/ 配下の doc-package（読み込めるものだけ）"}},
)
def list_doc_types(request: Request) -> JSONResponse:
    settings = _settings(request)
    items: list[dict[str, Any]] = []
    if settings.packages_dir.is_dir():
        for child in sorted(settings.packages_dir.iterdir()):
            if not child.is_dir() or not is_valid_slug(child.name):
                continue
            try:
                package = load_package(settings.packages_dir, child.name)
            except EnTeXError as exc:
                # 壊れたパッケージは一覧から外し、作者向けの理由はログにだけ出す
                logger.warning("doc-type %s skipped: %s", child.name, exc.user_message)
                continue
            items.append(
                {
                    "doc_type": package.slug,
                    "schema_version": package.schema.schema_version,
                    "title": package.schema.title,
                }
            )
    return JSONResponse(content=items, headers={REQUEST_ID_HEADER: request_id_of(request)})


@router.get(
    "/doc-types/{doc_type}",
    summary="文書種の schema.json",
    responses={
        200: {"description": "packages/<doc_type>/schema.json の内容"},
        **openapi_problem_responses(NOT_FOUND, PACKAGE_BROKEN),
    },
)
def get_doc_type(request: Request, doc_type: str) -> JSONResponse:
    settings = _settings(request)
    try:
        package = load_package(settings.packages_dir, doc_type)
    except PackageNotFoundError as exc:
        raise ProblemError(NOT_FOUND, f"文書の種類 '{doc_type}' には対応していません。") from exc
    # 検証は load_package で済ませ、返すのはファイルそのまま（UI がそのまま使う）
    content = json.loads((package.dir / SCHEMA_FILENAME).read_text(encoding="utf-8"))
    return JSONResponse(content=content, headers={REQUEST_ID_HEADER: request_id_of(request)})
