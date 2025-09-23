# Repository Guidelines

## Project Structure & Module Organization
- `src/` – Core library
  - `anonymization/` (k-anonymity, l-diversity, t-closeness)
  - `privacy/` (differential privacy)
  - `encryption/` (homomorphic encryption simulation)
  - `access_control/` (RBAC)
  - `utils/` (data loading, logging)
  - `main.py` (end‑to‑end pipeline; generates processed data)
- `data/` – Local datasets (keep large files out of Git)
  - `data/raw/`, `data/processed/`, `data/example_output/`
- `streamlit_demo.py` – Interactive demo app
- `test_complete_framework.py` – High‑level validation script
- `run_demo.sh`, `Dockerfile`, `pyproject.toml`, `.pre-commit-config.yaml`

## Build, Test, and Development Commands
- Install (dev): `pip install -e .[dev]`
- Lint & format: `ruff check . --fix` and `ruff format .`
- Pre-commit: `pre-commit install` then `pre-commit run -a`
- Run pipeline: `python src/main.py` (or `python -m src.main`)
- Run tests (pytest): `pytest -q` (or `pytest -k framework`)
- Manual validation: `python test_complete_framework.py`
- Streamlit demo: `streamlit run streamlit_demo.py`

## Coding Style & Naming Conventions
- Python 3.8+; 4‑space indentation; line length 88.
- Formatting and linting via Ruff (formatter + linter). Use double quotes.
- Modules and files: `snake_case`; classes: `PascalCase`; functions/vars: `snake_case`.
- Keep I/O paths under `data/`; do not hard‑code user‑specific paths.

## Testing Guidelines
- Framework: `pytest`. Name files `test_*.py`.
- Prefer fast, deterministic tests; use small DataFrame fixtures.
- Write tests close to features (root or `tests/`).
- To regenerate processed inputs for tests, run `python src/main.py`.

## Commit & Pull Request Guidelines
- Use Conventional Commits (e.g., `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).
- PRs must include: concise description, rationale, screenshots for UI/demos if applicable, and linked issues.
- Before opening a PR: run `ruff` (fixes applied), all tests pass, docs updated (README or inline docstrings as needed).

## Security & Configuration Tips
- Do not commit PHI/PII or large datasets; keep data in `data/` and add new paths to `.gitignore` if needed.
- Homomorphic encryption is a simulation by default; real HE requires optional `Pyfhel` (see `pyproject.toml`).
- Avoid logging sensitive values; use `src/utils/logging_config.py` helpers.
