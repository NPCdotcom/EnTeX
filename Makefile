.DEFAULT_GOAL := help
PY ?= python3
VENV ?= .venv
COMPOSE ?= docker compose

.PHONY: help setup hooks test lint fmt schemas docker-build docker-shell docker-doctor docker-test docker-serve tex-smoke clean

help: ## Show targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

# --- host (no TeX) ------------------------------------------------------------

setup: ## Create local venv and install package (lint/tests without TeX)
	$(PY) -m venv $(VENV)
	$(VENV)/bin/pip install -e ".[dev]"
	$(MAKE) hooks

hooks: ## Enable the repo git hooks (branch name / commit prefix / no main commits)
	git config core.hooksPath .githooks
	@echo "core.hooksPath -> .githooks"

test: ## Run pytest on host (TeX tests are skipped)
	$(VENV)/bin/pytest

lint: ## Ruff check
	$(VENV)/bin/ruff check .

fmt: ## Ruff format + fix
	$(VENV)/bin/ruff format . && $(VENV)/bin/ruff check --fix .

schemas: ## Regenerate schemas/ from the pydantic models / FastAPI app (tests check they are in sync)
	$(VENV)/bin/python -m entex.ir.loader
	$(VENV)/bin/python -m entex.api.app

# --- container (Python + LuaLaTeX) -------------------------------------------

docker-build: ## Build the dev image
	$(COMPOSE) build

docker-shell: ## Interactive shell inside the dev image
	$(COMPOSE) run --rm dev bash

docker-doctor: ## Verify TeX toolchain inside the image
	$(COMPOSE) run --rm dev entex doctor

docker-test: ## Run the full test suite inside the image (incl. TeX tests)
	$(COMPOSE) run --rm dev pytest

docker-serve: ## Serve the API on http://localhost:8000 (POST /v1/render, GET /v1/health)
	$(COMPOSE) run --rm --service-ports dev uvicorn entex.api.app:app --host 0.0.0.0 --port 8000

tex-smoke: ## Compile tests/fixtures/smoke.tex with LuaLaTeX inside the image
	$(COMPOSE) run --rm dev sh scripts/tex-smoke.sh

clean: ## Remove build artefacts
	rm -rf $(VENV) build dist *.egg-info .pytest_cache .ruff_cache out/
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
