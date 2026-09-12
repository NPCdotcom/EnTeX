"""環境変数から読む設定（api.md §3.5）。`pydantic-settings` は入れず `os.environ` を読む。"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from entex.packages import PACKAGES_DIR_ENV, default_packages_dir

ENV_WORK_DIR = "ENTEX_WORK_DIR"
ENV_RENDER_TIMEOUT = "ENTEX_RENDER_TIMEOUT"
ENV_MAX_CONCURRENT_RENDERS = "ENTEX_MAX_CONCURRENT_RENDERS"
ENV_QUEUE_WAIT_SECONDS = "ENTEX_QUEUE_WAIT_SECONDS"
ENV_MAX_BODY_BYTES = "ENTEX_MAX_BODY_BYTES"
ENV_KEEP_FAILED_JOBS = "ENTEX_KEEP_FAILED_JOBS"

DEFAULT_RENDER_TIMEOUT = 60.0  # renderer の既定 180 秒より短くする（api.md §3.4）
DEFAULT_QUEUE_WAIT_SECONDS = 5.0
DEFAULT_MAX_BODY_BYTES = 1_048_576  # 1 MiB。max_items 20 行の IR は数 KB


@dataclass(frozen=True, slots=True)
class Settings:
    packages_dir: Path
    work_dir: Path | None  # None ならシステムの tmp
    render_timeout: float
    max_concurrent_renders: int
    queue_wait_seconds: float
    max_body_bytes: int
    keep_failed_jobs: bool

    def __post_init__(self) -> None:
        if self.render_timeout <= 0:
            raise ValueError(f"{ENV_RENDER_TIMEOUT} は正の秒数")
        if self.max_concurrent_renders < 1:
            raise ValueError(f"{ENV_MAX_CONCURRENT_RENDERS} は 1 以上")
        if self.queue_wait_seconds < 0:
            raise ValueError(f"{ENV_QUEUE_WAIT_SECONDS} は 0 以上")
        if self.max_body_bytes < 1:
            raise ValueError(f"{ENV_MAX_BODY_BYTES} は 1 以上")

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Settings:
        e = os.environ if env is None else env
        packages_dir = Path(e[PACKAGES_DIR_ENV]) if e.get(PACKAGES_DIR_ENV) else None
        work_dir = Path(e[ENV_WORK_DIR]) if e.get(ENV_WORK_DIR) else None
        return cls(
            packages_dir=packages_dir if packages_dir is not None else default_packages_dir(),
            work_dir=work_dir,
            render_timeout=_float(e, ENV_RENDER_TIMEOUT, DEFAULT_RENDER_TIMEOUT),
            max_concurrent_renders=_int(e, ENV_MAX_CONCURRENT_RENDERS, os.cpu_count() or 1),
            queue_wait_seconds=_float(e, ENV_QUEUE_WAIT_SECONDS, DEFAULT_QUEUE_WAIT_SECONDS),
            max_body_bytes=_int(e, ENV_MAX_BODY_BYTES, DEFAULT_MAX_BODY_BYTES),
            keep_failed_jobs=_bool(e, ENV_KEEP_FAILED_JOBS, False),
        )


def _int(env: Mapping[str, str], name: str, default: int) -> int:
    value = env.get(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name}={value!r} は整数で指定する") from exc


def _float(env: Mapping[str, str], name: str, default: float) -> float:
    value = env.get(name)
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"{name}={value!r} は数値で指定する") from exc


def _bool(env: Mapping[str, str], name: str, default: bool) -> bool:
    value = env.get(name)
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}
