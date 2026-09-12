"""FastAPI アプリの組み立て（api.md §3.6 / §3.7）。

起動: `uvicorn entex.api.app:app --host 0.0.0.0 --port 8000`
スキーマ再生成: `python -m entex.api.app`（`schemas/api/problem.schema.json` と `openapi.json`）
"""

from __future__ import annotations

import json
import logging
import threading
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.openapi.utils import get_openapi

from entex import __version__
from entex.api.problems import (
    REQUEST_ID_HEADER,
    Problem,
    install_exception_handlers,
    resolve_request_id,
)
from entex.api.routes import router, toolchain_status
from entex.api.settings import Settings
from entex.ir.loader import Envelope

logger = logging.getLogger("entex.api")

API_TITLE = "EnTeX API"
API_DESCRIPTION = (
    "中間表現（IR）を POST すると固定様式の PDF が返る。"
    "失敗は application/problem+json（RFC 9457）。設計: docs/design/programs/api.md"
)


def create_app(settings: Settings | None = None) -> FastAPI:
    """`settings` を省くと起動時（lifespan）に環境変数から読む。"""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        resolved = settings if settings is not None else Settings.from_env()
        app.state.settings = resolved
        app.state.render_semaphore = threading.BoundedSemaphore(resolved.max_concurrent_renders)
        if resolved.work_dir is not None:
            resolved.work_dir.mkdir(parents=True, exist_ok=True)
        toolchain = toolchain_status()
        missing = sorted(name for name, found in toolchain.items() if not found)
        if missing:
            logger.warning("toolchain incomplete (health will report degraded): %s", missing)
        logger.info(
            "entex api %s: packages_dir=%s work_dir=%s max_concurrent=%d timeout=%ss",
            __version__,
            resolved.packages_dir,
            resolved.work_dir or "<system tmp>",
            resolved.max_concurrent_renders,
            resolved.render_timeout,
        )
        yield

    app = FastAPI(
        title=API_TITLE,
        version=__version__,
        description=API_DESCRIPTION,
        lifespan=lifespan,
        # 既定の 422 は Problem Details に置き換えるので、OpenAPI にも既定の形を出さない
        openapi_url="/openapi.json",
    )
    app.include_router(router)
    install_exception_handlers(app)

    @app.middleware("http")
    async def _request_id(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request.state.request_id = resolve_request_id(request.headers.get(REQUEST_ID_HEADER))
        response = await call_next(request)
        response.headers.setdefault(REQUEST_ID_HEADER, request.state.request_id)
        return response

    app.openapi = lambda: _openapi(app)  # type: ignore[method-assign]
    return app


def _openapi(app: FastAPI) -> dict[str, Any]:
    """OpenAPI を組み、Problem / Envelope のスキーマを components に入れ、既定の 422 の形を消す。"""
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    components = schema.setdefault("components", {}).setdefault("schemas", {})
    for model in (Problem, Envelope):
        model_schema = model.model_json_schema(ref_template="#/components/schemas/{model}")
        components.update(model_schema.pop("$defs", {}))
        components[model.__name__] = model_schema
    components.pop("HTTPValidationError", None)
    components.pop("ValidationError", None)
    for path_item in schema.get("paths", {}).values():
        for operation in path_item.values():
            responses = operation.get("responses", {})
            default_422 = responses.get("422", {}).get("content", {}).get("application/json")
            if default_422 and "HTTPValidationError" in json.dumps(default_422):
                responses["422"]["content"].pop("application/json")
                if not responses["422"]["content"]:
                    responses.pop("422")
    app.openapi_schema = schema
    return schema


app = create_app()


# --- schemas/api の再生成 --------------------------------------------------------------------


def problem_json_schema_text() -> str:
    return json.dumps(Problem.model_json_schema(), ensure_ascii=False, indent=2) + "\n"


def openapi_json_text() -> str:
    return json.dumps(create_app().openapi(), ensure_ascii=False, indent=2) + "\n"


if __name__ == "__main__":  # pragma: no cover - 手動再生成用
    target_dir = Path(__file__).resolve().parents[3] / "schemas" / "api"
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "problem.schema.json").write_text(problem_json_schema_text(), encoding="utf-8")
    (target_dir / "openapi.json").write_text(openapi_json_text(), encoding="utf-8")
    print(target_dir / "problem.schema.json")
    print(target_dir / "openapi.json")
