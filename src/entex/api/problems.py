"""RFC 9457 Problem Details（api.md §3.3）。

`type` ごとに `status` と `title` を固定し、`detail` だけを出来事ごとに変える。`detail` に入れて
よいのは `EnTeXError.user_message` と、ここに書いた日本語の定型文だけ（charter §4）。
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from starlette.exceptions import HTTPException as StarletteHTTPException

from entex.errors import (
    DerivationError,
    EnTeXError,
    EnvelopeError,
    FieldIssue,
    IRValidationError,
    PackageError,
    RenderError,
    RenderTimeoutError,
)

logger = logging.getLogger("entex.api")

PROBLEM_MEDIA_TYPE = "application/problem+json"
# 実 URL に変えるのは配置先が決まってから（api.md §3.3）
PROBLEM_TYPE_BASE = "https://entex.example/problems/"
REQUEST_ID_HEADER = "X-Request-ID"


# --- 応答の形（`schemas/api/problem.schema.json` の正本） -----------------------------------


class ProblemIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(description="content 内の場所（例: finance[1].amount）")
    message: str = Field(description="利用者向けの完成文（フィールドの label を含む）")


class Problem(BaseModel):
    """RFC 9457 の 5 メンバー + 拡張 `issues`（`ir-invalid` のときだけ）。"""

    model_config = ConfigDict(
        extra="forbid",
        title="EnTeX Problem Details",
        json_schema_extra={
            "description": "EnTeX API の失敗応答（application/problem+json、RFC 9457）。"
            "detail は日本語の完成文で、TeX のログや Python のトレースバックは含まない。"
        },
    )

    type: str = Field(description=f"問題の種類の URI。{PROBLEM_TYPE_BASE}<slug>")
    title: str = Field(description="種類ごとに固定の短い日本語")
    status: int = Field(ge=400, le=599)
    detail: str = Field(description="この出来事の説明（日本語の完成文）")
    instance: str = Field(
        description="リクエスト ID。urn:uuid:<uuid>。サーバ側ログとの突き合わせ用"
    )
    issues: list[ProblemIssue] | None = Field(
        default=None, description="ir-invalid のときの件ごとの問題"
    )


# --- 種類の表 ----------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ProblemType:
    slug: str
    status: int
    title: str
    default_detail: str

    @property
    def uri(self) -> str:
        return f"{PROBLEM_TYPE_BASE}{self.slug}"


BAD_REQUEST = ProblemType(
    "bad-request", 400, "リクエストの本文を読めません", "入力を JSON として読めません。"
)
UNSUPPORTED_MEDIA_TYPE = ProblemType(
    "unsupported-media-type",
    415,
    "対応していない形式です",
    "本文は application/json で送ってください。",
)
CONTENT_TOO_LARGE = ProblemType(
    "content-too-large", 413, "本文が大きすぎます", "本文が上限を超えています。"
)
ENVELOPE_MISMATCH = ProblemType(
    "envelope-mismatch",
    422,
    "文書の種類または版が一致しません",
    "文書の種類（doc_type）または版（schema_version）が一致しません。",
)
IR_INVALID = ProblemType("ir-invalid", 422, "入力に問題があります", "入力に問題があります。")
PACKAGE_BROKEN = ProblemType(
    "package-broken",
    500,
    "文書種の定義に問題があります",
    "文書種の定義に問題があります。管理者へお問い合わせください。",
)
RENDER_FAILED = ProblemType(
    "render-failed", 500, "PDFの生成に失敗しました", RenderError.GENERIC_MESSAGE
)
RENDER_TIMEOUT = ProblemType(
    "render-timeout",
    500,
    "PDFの生成が時間内に終わりませんでした",
    RenderTimeoutError.GENERIC_MESSAGE,
)
BUSY = ProblemType(
    "busy", 503, "混み合っています", "混み合っています。しばらくしてからやり直してください。"
)
NOT_FOUND = ProblemType("not-found", 404, "見つかりません", "指定されたものは存在しません。")
METHOD_NOT_ALLOWED = ProblemType(
    "method-not-allowed", 405, "その操作はできません", "このパスではそのメソッドは使えません。"
)
HTTP_ERROR = ProblemType(
    "http-error", 400, "リクエストを処理できません", "リクエストを処理できません。"
)
INTERNAL_ERROR = ProblemType(
    "internal-error",
    500,
    "サーバ内部で問題が起きました",
    "サーバ内部で問題が起きました。管理者へお問い合わせください。",
)

ALL_TYPES: tuple[ProblemType, ...] = (
    BAD_REQUEST,
    UNSUPPORTED_MEDIA_TYPE,
    CONTENT_TOO_LARGE,
    ENVELOPE_MISMATCH,
    IR_INVALID,
    PACKAGE_BROKEN,
    RENDER_FAILED,
    RENDER_TIMEOUT,
    BUSY,
    NOT_FOUND,
    METHOD_NOT_ALLOWED,
    HTTP_ERROR,
    INTERNAL_ERROR,
)


class ProblemError(Exception):
    """ルートや依存から投げる「この Problem を返せ」。例外ハンドラが応答に変える。"""

    def __init__(
        self,
        problem_type: ProblemType,
        detail: str | None = None,
        *,
        issues: list[FieldIssue] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(problem_type.slug)
        self.problem_type = problem_type
        self.detail = detail or problem_type.default_detail
        self.issues = issues
        self.headers = headers or {}


# --- リクエスト ID ------------------------------------------------------------------------


def resolve_request_id(header_value: str | None) -> str:
    """`X-Request-ID` が UUID ならそれを使い、それ以外は生成する（任意文字列をログに流さない）。"""
    if header_value:
        try:
            return str(uuid.UUID(header_value.strip()))
        except ValueError:
            pass
    return str(uuid.uuid4())


def request_id_of(request: Request) -> str:
    rid = getattr(request.state, "request_id", None)
    if rid is None:
        rid = resolve_request_id(request.headers.get(REQUEST_ID_HEADER))
        request.state.request_id = rid
    return rid


# --- 応答の組み立て ------------------------------------------------------------------------


def problem_response(
    problem_type: ProblemType,
    request_id: str,
    detail: str | None = None,
    *,
    issues: list[FieldIssue] | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    problem = Problem(
        type=problem_type.uri,
        title=problem_type.title,
        status=problem_type.status,
        detail=detail or problem_type.default_detail,
        instance=f"urn:uuid:{request_id}",
        issues=[ProblemIssue(path=i.path, message=i.message) for i in issues] if issues else None,
    )
    out_headers = {REQUEST_ID_HEADER: request_id, **(headers or {})}
    return JSONResponse(
        content=problem.model_dump(exclude_none=True),
        status_code=problem_type.status,
        media_type=PROBLEM_MEDIA_TYPE,
        headers=out_headers,
    )


def problem_from_entex_error(exc: EnTeXError, request_id: str) -> JSONResponse:
    """`entex.errors` の階層を api.md §3.3 の表どおりに写す。作者向け・運用者向けの詳細はログへ。"""
    if isinstance(exc, IRValidationError):
        return problem_response(IR_INVALID, request_id, exc.user_message, issues=exc.issues)
    if isinstance(exc, EnvelopeError):
        return problem_response(ENVELOPE_MISMATCH, request_id, exc.user_message)
    if isinstance(exc, PackageError | DerivationError):
        logger.error("package-broken request_id=%s: %s", request_id, exc.user_message)
        return problem_response(PACKAGE_BROKEN, request_id)
    if isinstance(exc, RenderTimeoutError):
        logger.error("render-timeout request_id=%s: %s", request_id, exc.detail)
        return problem_response(RENDER_TIMEOUT, request_id, exc.user_message)
    if isinstance(exc, RenderError):
        logger.error("render-failed request_id=%s: %s", request_id, exc.detail)
        return problem_response(RENDER_FAILED, request_id, RenderError.GENERIC_MESSAGE)
    logger.error("unclassified EnTeXError request_id=%s: %s", request_id, exc.user_message)
    return problem_response(INTERNAL_ERROR, request_id)


def openapi_problem_responses(*types: ProblemType) -> dict[int | str, dict[str, Any]]:
    """ルートの `responses=` に渡す OpenAPI 断片。"""
    out: dict[int | str, dict[str, Any]] = {}
    for t in types:
        out[t.status] = {
            "description": t.title,
            "content": {PROBLEM_MEDIA_TYPE: {"schema": {"$ref": "#/components/schemas/Problem"}}},
        }
    return out


# --- FastAPI への登録 ------------------------------------------------------------------------


def install_exception_handlers(app: FastAPI) -> None:
    """FastAPI / Starlette 既定の `{"detail": ...}` を Problem Details に置き換える。"""

    @app.exception_handler(ProblemError)
    async def _problem(request: Request, exc: ProblemError) -> JSONResponse:
        return problem_response(
            exc.problem_type,
            request_id_of(request),
            exc.detail,
            issues=exc.issues,
            headers=exc.headers,
        )

    @app.exception_handler(EnTeXError)
    async def _entex(request: Request, exc: EnTeXError) -> JSONResponse:
        return problem_from_entex_error(exc, request_id_of(request))

    @app.exception_handler(RequestValidationError)
    async def _validation(request: Request, exc: RequestValidationError) -> JSONResponse:
        return problem_response(BAD_REQUEST, request_id_of(request))

    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        if exc.status_code == 404:
            problem_type = NOT_FOUND
        elif exc.status_code == 405:
            problem_type = METHOD_NOT_ALLOWED
        else:
            problem_type = ProblemType(
                HTTP_ERROR.slug, exc.status_code, HTTP_ERROR.title, HTTP_ERROR.default_detail
            )
        return problem_response(
            problem_type, request_id_of(request), headers=dict(exc.headers or {})
        )

    @app.exception_handler(Exception)
    async def _unexpected(request: Request, exc: Exception) -> JSONResponse:
        rid = request_id_of(request)
        logger.exception("unexpected error request_id=%s", rid)
        return problem_response(INTERNAL_ERROR, rid)
