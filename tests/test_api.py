"""plan `api-render`: `POST /v1/render` ほか（api.md §1 FR-A1〜A8 / NFR-A1〜A4）。

TeX 非依存分は偽 latexmk（PATH の先頭に置く）で、PDF が実際に出る分は `@requires_tex`。
"""

from __future__ import annotations

import json
import logging
import os
import stat
import time
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient
from typer.testing import CliRunner

from entex import __version__
from entex.api.app import create_app
from entex.api.problems import PROBLEM_TYPE_BASE, Problem
from entex.api.settings import Settings
from entex.cli import app as cli_app
from entex.errors import RenderError, RenderTimeoutError
from tests.conftest import EXAMPLES_DIR, PACKAGES_DIR, REPO_ROOT, load_example, requires_tex
from tests.test_renderer import TEX_VOCABULARY, assert_no_tex_vocabulary

VALID = sorted(p.name for p in (EXAMPLES_DIR / "valid").glob("*.json"))
INVALID = sorted(p.name for p in (EXAMPLES_DIR / "invalid").glob("*.json"))
PROBLEM_JSON = "application/problem+json"


# --- fixtures ----------------------------------------------------------------------


def _make_settings(tmp_path: Path, **overrides: Any) -> Settings:
    work_dir = tmp_path / "work"
    work_dir.mkdir(exist_ok=True)
    values: dict[str, Any] = {
        "packages_dir": PACKAGES_DIR,
        "work_dir": work_dir,
        "render_timeout": 30.0,
        "max_concurrent_renders": 2,
        "queue_wait_seconds": 0.0,
        "max_body_bytes": 1_048_576,
        "keep_failed_jobs": False,
    }
    values.update(overrides)
    return Settings(**values)


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return _make_settings(tmp_path)


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    with TestClient(create_app(settings=settings)) as c:
        yield c


def _write_fake_latexmk(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, body: str) -> Path:
    bin_dir = tmp_path / "fakebin"
    bin_dir.mkdir(exist_ok=True)
    script = bin_dir / "latexmk"
    script.write_text(f"#!/bin/sh\n{body}\n", encoding="utf-8")
    script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return script


@pytest.fixture
def failing_latexmk(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    return _write_fake_latexmk(
        tmp_path,
        monkeypatch,
        "echo '! LaTeX Error: File `missing.sty` not found.'\n"
        "echo 'l.12 undefinedcommand'\n"
        "echo '! Emergency stop.' >&2\n"
        "exit 12",
    )


def _post(client: TestClient, raw: Any, headers: dict[str, str] | None = None):
    return client.post(
        "/v1/render", content=json.dumps(raw), headers=_json_headers(**(headers or {}))
    )


def _json_headers(**extra: str) -> dict[str, str]:
    return {"Content-Type": "application/json", **extra}


def _assert_problem(resp, status: int, slug: str | None) -> dict[str, Any]:
    assert resp.status_code == status, resp.text
    assert resp.headers["content-type"].startswith(PROBLEM_JSON)
    body = resp.json()
    assert body["type"].startswith(PROBLEM_TYPE_BASE)
    if slug is not None:
        assert body["type"] == f"{PROBLEM_TYPE_BASE}{slug}"
    assert body["status"] == status
    assert isinstance(body["title"], str) and body["title"]
    assert isinstance(body["detail"], str) and body["detail"]
    assert body["instance"].startswith("urn:uuid:")
    # FastAPI 既定の {"detail": [...]} の形が混ざっていない（AC2）
    assert not isinstance(body["detail"], list)
    Problem.model_validate(body)
    return body


# --- AC1: 成功応答（TeX 環境） -----------------------------------------------------------


@requires_tex
@pytest.mark.parametrize("name", VALID)
def test_render_valid_examples_return_pdf(client: TestClient, name: str) -> None:
    resp = _post(client, load_example(f"valid/{name}"))
    assert resp.status_code == 200, resp.text
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content.startswith(b"%PDF-")
    disposition = resp.headers["content-disposition"]
    assert 'filename="circle-monthly-report.pdf"' in disposition
    assert f"filename*=UTF-8''{quote('サークル月次活動報告書.pdf', safe='')}" in disposition
    assert disposition.isascii()
    assert resp.headers["x-request-id"]


@requires_tex
def test_render_typical_within_budget(client: TestClient) -> None:
    """NFR-A1 の目安。1 回目はフォントキャッシュで遅くなり得るので 2 回目を測る。"""
    budget = float(os.environ.get("ENTEX_NFR1_SECONDS", "10"))
    raw = load_example("valid/01-typical.json")
    assert _post(client, raw).status_code == 200
    started = time.perf_counter()
    assert _post(client, raw).status_code == 200
    assert time.perf_counter() - started < budget


def test_api_and_cli_write_the_same_tex(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, settings: Settings
) -> None:
    """FR-A8: 同じ IR から CLI と API が同じ .tex を作る（偽 latexmk で API 側の .tex を捕まえる）。

    ホストで実行できる（PDF は作らない）。
    """
    captured = tmp_path / "captured.tex"
    _write_fake_latexmk(
        tmp_path, monkeypatch, f'for a; do last="$a"; done\ncp "$last" "{captured}"\nexit 1'
    )
    src = EXAMPLES_DIR / "valid" / "06-tex-special-chars.json"
    with TestClient(create_app(settings=settings)) as client:
        resp = client.post("/v1/render", content=src.read_bytes(), headers=_json_headers())
    assert resp.status_code == 500
    assert captured.is_file()

    cli_out = tmp_path / "cli"
    result = CliRunner().invoke(cli_app, ["render", str(src), "--out", str(cli_out), "--tex-only"])
    assert result.exit_code == 0, result.stderr
    assert captured.read_text("utf-8") == (cli_out / "06-tex-special-chars.tex").read_text("utf-8")


# --- AC2: 422 / 400 -----------------------------------------------------------------------


@pytest.mark.parametrize("name", INVALID)
def test_invalid_examples_are_422_problems(client: TestClient, name: str) -> None:
    body = _assert_problem(_post(client, load_example(f"invalid/{name}")), 422, None)
    assert body["type"].rsplit("/", 1)[1] in {"envelope-mismatch", "ir-invalid"}


def test_envelope_mismatch_problem_has_no_issues(client: TestClient) -> None:
    body = _assert_problem(
        _post(client, load_example("invalid/06-envelope-mismatch.json")), 422, "envelope-mismatch"
    )
    assert "schema_version" in body["detail"]
    assert "issues" not in body


def test_ir_invalid_problem_lists_issues(client: TestClient) -> None:
    body = _assert_problem(
        _post(client, load_example("invalid/03-unknown-enum-and-negative-amount.json")),
        422,
        "ir-invalid",
    )
    assert "入力に2件の問題があります" in body["detail"]
    assert len(body["issues"]) == 2
    for issue in body["issues"]:
        assert set(issue) == {"path", "message"}
        assert issue["path"] and issue["message"]
    assert body["issues"][0]["path"].startswith("finance[")


@pytest.mark.parametrize(
    "content",
    [b"{not json", b"[]", b'"text"', b"123", b"null", b"", b"\xff\xfe"],
)
def test_non_object_bodies_are_400_problems(client: TestClient, content: bytes) -> None:
    resp = client.post("/v1/render", content=content, headers=_json_headers())
    _assert_problem(resp, 400, "bad-request")


def test_wrong_content_type_is_415_problem(client: TestClient) -> None:
    resp = client.post(
        "/v1/render",
        content=json.dumps(load_example("valid/02-minimal.json")),
        headers={"Content-Type": "text/plain"},
    )
    _assert_problem(resp, 415, "unsupported-media-type")


# --- AC3: 500 のとき TeX を漏らさない -----------------------------------------------------


def test_render_failure_is_500_without_tex_vocabulary(
    client: TestClient, failing_latexmk: Path, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.ERROR, logger="entex.api"):
        resp = _post(client, load_example("valid/01-typical.json"))
    body = _assert_problem(resp, 500, "render-failed")
    assert body["detail"] == RenderError.GENERIC_MESSAGE
    # 応答のヘッダと本文全体に TeX の語彙が無い（FR-A4）
    assert_no_tex_vocabulary(resp.text)
    for key, value in resp.headers.items():
        assert_no_tex_vocabulary(f"{key}: {value}")
    # サーバ側ログにだけ原文が残る（request_id と一緒に）
    assert "LaTeX Error" in caplog.text
    assert body["instance"].removeprefix("urn:uuid:") in caplog.text


def test_broken_package_is_500_package_broken(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    pkgs = tmp_path / "packages"
    (pkgs / "circle-monthly-report").mkdir(parents=True)
    (pkgs / "circle-monthly-report" / "schema.json").write_text("[]", encoding="utf-8")
    settings = _make_settings(tmp_path, packages_dir=pkgs)
    with TestClient(create_app(settings=settings)) as client:
        with caplog.at_level(logging.ERROR, logger="entex.api"):
            resp = _post(client, load_example("valid/01-typical.json"))
    body = _assert_problem(resp, 500, "package-broken")
    assert "schema.json" not in body["detail"]  # 作者向けの詳細は応答に出さない
    assert "schema.json" in caplog.text


def test_render_timeout_is_a_distinct_problem(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_fake_latexmk(tmp_path, monkeypatch, "sleep 5\nexit 0")
    settings = _make_settings(tmp_path, render_timeout=0.3)
    with TestClient(create_app(settings=settings)) as client:
        resp = _post(client, load_example("valid/02-minimal.json"))
    body = _assert_problem(resp, 500, "render-timeout")
    assert body["detail"] == RenderTimeoutError.GENERIC_MESSAGE
    assert_no_tex_vocabulary(resp.text)


# --- AC4: health / 503 / 413 / 一時ディレクトリ -------------------------------------------


@requires_tex
def test_health_ok_with_toolchain(client: TestClient) -> None:
    resp = client.get("/v1/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["version"] == __version__
    assert set(body["toolchain"]) == {"lualatex", "latexmk", "luatexja.sty"}
    assert all(body["toolchain"].values())


def test_health_degraded_without_toolchain(
    client: TestClient, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", str(tmp_path / "empty"))
    resp = client.get("/v1/health")
    assert resp.status_code == 503
    body = resp.json()
    assert body["status"] == "degraded"
    assert body["toolchain"]["latexmk"] is None


def test_busy_is_503_with_retry_after(tmp_path: Path) -> None:
    settings = _make_settings(tmp_path, max_concurrent_renders=1, queue_wait_seconds=0.0)
    app = create_app(settings=settings)
    with TestClient(app) as client:
        sem = app.state.render_semaphore
        assert sem.acquire(timeout=1)  # 1 件が latexmk 中、を模す
        try:
            resp = _post(client, load_example("valid/02-minimal.json"))
        finally:
            sem.release()
        _assert_problem(resp, 503, "busy")
        assert int(resp.headers["retry-after"]) >= 1
        # 解放後は通る（偽 latexmk 無し・TeX 無しなら 500、ありなら 200。503 でないこと）
        resp = _post(client, load_example("valid/02-minimal.json"))
        assert resp.status_code != 503


def test_too_large_body_is_413(tmp_path: Path) -> None:
    settings = _make_settings(tmp_path, max_body_bytes=100)
    with TestClient(create_app(settings=settings)) as client:
        resp = _post(client, load_example("valid/01-typical.json"))
    body = _assert_problem(resp, 413, "content-too-large")
    assert "100" in body["detail"]


def test_work_dir_is_clean_after_failure(
    client: TestClient, settings: Settings, failing_latexmk: Path
) -> None:
    assert _post(client, load_example("valid/01-typical.json")).status_code == 500
    assert settings.work_dir is not None
    assert list(settings.work_dir.iterdir()) == []


def test_work_dir_is_clean_after_validation_error(client: TestClient, settings: Settings) -> None:
    resp = _post(client, load_example("invalid/03-unknown-enum-and-negative-amount.json"))
    assert resp.status_code == 422
    assert settings.work_dir is not None
    assert list(settings.work_dir.iterdir()) == []


def test_failed_job_is_kept_when_configured(tmp_path: Path, failing_latexmk: Path) -> None:
    settings = _make_settings(tmp_path, keep_failed_jobs=True)
    with TestClient(create_app(settings=settings)) as client:
        assert _post(client, load_example("valid/01-typical.json")).status_code == 500
    assert settings.work_dir is not None
    kept = list(settings.work_dir.iterdir())
    assert len(kept) == 1 and (kept[0] / "latexmk.log").is_file()


@requires_tex
def test_work_dir_is_clean_after_success(client: TestClient, settings: Settings) -> None:
    assert _post(client, load_example("valid/02-minimal.json")).status_code == 200
    assert settings.work_dir is not None
    assert list(settings.work_dir.iterdir()) == []


def test_request_id_header_is_echoed_when_it_is_a_uuid(client: TestClient) -> None:
    rid = "123e4567-e89b-12d3-a456-426614174000"
    resp = _post(
        client, load_example("invalid/06-envelope-mismatch.json"), headers={"X-Request-ID": rid}
    )
    assert resp.headers["x-request-id"] == rid
    assert resp.json()["instance"] == f"urn:uuid:{rid}"


def test_request_id_header_is_replaced_when_not_a_uuid(client: TestClient) -> None:
    resp = _post(
        client,
        load_example("invalid/06-envelope-mismatch.json"),
        headers={"X-Request-ID": "<script>alert(1)</script>"},
    )
    assert "<" not in resp.headers["x-request-id"]
    assert "<" not in resp.text


# --- AC5: doc-types / schemas 同期 -------------------------------------------------------


def test_doc_types_lists_packages(client: TestClient) -> None:
    resp = client.get("/v1/doc-types")
    assert resp.status_code == 200
    assert resp.json() == [
        {
            "doc_type": "circle-monthly-report",
            "schema_version": 1,
            "title": "サークル月次活動報告書",
        },
        {
            "doc_type": "club-meeting-log",
            "schema_version": 1,
            "title": "部会ログ",
        },
    ]


def test_doc_type_detail_returns_schema_json(client: TestClient) -> None:
    resp = client.get("/v1/doc-types/circle-monthly-report")
    assert resp.status_code == 200
    on_disk = json.loads(
        (PACKAGES_DIR / "circle-monthly-report" / "schema.json").read_text(encoding="utf-8")
    )
    assert resp.json() == on_disk


@pytest.mark.parametrize("slug", ["nope", "Circle-Monthly-Report", "..", "a%2Fb"])
def test_unknown_doc_type_is_404_problem(client: TestClient, slug: str) -> None:
    _assert_problem(client.get(f"/v1/doc-types/{slug}"), 404, "not-found")


def test_unknown_route_is_404_problem(client: TestClient) -> None:
    _assert_problem(client.get("/v1/nope"), 404, "not-found")


def test_problem_schema_is_in_sync() -> None:
    path = REPO_ROOT / "schemas" / "api" / "problem.schema.json"
    assert json.loads(path.read_text(encoding="utf-8")) == Problem.model_json_schema(), (
        "schemas/api/problem.schema.json が entex.api.problems.Problem とずれている。"
        "`python -m entex.api.app` で再生成すること"
    )


def test_openapi_is_in_sync() -> None:
    path = REPO_ROOT / "schemas" / "api" / "openapi.json"
    assert json.loads(path.read_text(encoding="utf-8")) == create_app().openapi(), (
        "schemas/api/openapi.json がアプリの OpenAPI とずれている。"
        "`python -m entex.api.app` で再生成すること"
    )


def test_openapi_declares_problem_responses() -> None:
    spec = create_app().openapi()
    render_op = spec["paths"]["/v1/render"]["post"]
    assert "application/pdf" in render_op["responses"]["200"]["content"]
    for status in ("400", "413", "415", "422", "500", "503"):
        assert PROBLEM_JSON in render_op["responses"][status]["content"]
    # FastAPI 既定の 422 スキーマ（HTTPValidationError）が残っていない
    assert "HTTPValidationError" not in spec.get("components", {}).get("schemas", {})


def test_tex_vocabulary_constant_is_still_meaningful() -> None:
    """AC3 が空振りしないことの自衛（語彙表が消えたら気づく）。"""
    assert "LaTeX Error" in TEX_VOCABULARY
