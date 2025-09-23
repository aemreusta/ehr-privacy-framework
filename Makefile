# Makefile for EHR Privacy Framework (uv + pip-tools)

PYTHON ?= python
CONDA_ENV ?= ehrEnv

.PHONY: help conda-env deps-compile deps-sync install run demo test lint fmt precommit

help:
	@echo "Common targets:"
	@echo "  make conda-env     # Create conda env $(CONDA_ENV) with Python 3.10"
	@echo "  make deps-compile  # Compile requirements.in -> requirements.txt (pip-tools)"
	@echo "  make deps-sync     # Install deps with uv from compiled requirements"
	@echo "  make run           # Run pipeline (src.main) via uv"
	@echo "  make demo          # Run Streamlit demo via uv"
	@echo "  make test          # Run pytest via uv"
	@echo "  make lint / fmt    # Ruff lint / format via uv"
	@echo "  make precommit     # Run pre-commit on all files"

conda-env:
	conda create -n $(CONDA_ENV) python=3.10 -y

deps-compile:
	uv run --with pip-tools pip-compile requirements.in -o requirements.txt
	uv run --with pip-tools pip-compile requirements-dev.in -o requirements-dev.txt

deps-sync:
	uv pip sync requirements.txt requirements-dev.txt

install: deps-compile deps-sync

run:
	uv run $(PYTHON) -m src.main

demo:
	uv run streamlit run streamlit_demo.py

test:
	uv run pytest -q

lint:
	uv run ruff check . --fix

fmt:
	uv run ruff format .

precommit:
	uv run pre-commit run -a
