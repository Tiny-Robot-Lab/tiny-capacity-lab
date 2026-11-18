# Agent Instructions: Tiny Capacity Lab

## Purpose and Scope

Tiny Capacity Lab experiments with observing capacity and quota behaviors of AI development tools on macOS.
All work in this repository must stay strictly bounded within the active experiment plan.

## Principles and Boundaries

- **Experiment and Privacy Boundaries**: Never commit, stage, quote, or copy live provider capacity data, account identifiers, prompts, or personal information. `data/` and `*.local.json` are strictly ignored.
- **Structured Provider CLI Output**: Always rely on structured machine-readable CLI output (e.g. `agy -p /usage --output-format json`). Never scrape human terminal text when structured data is available.
- **No Credential Handling**: Do not read, store, copy, pass, or refresh provider authentication tokens, secrets, or API keys. Let the provider CLI manage its own authentication.
- **No Invented Provider State**: Unknown values remain unknown. Never fabricate quota groups, buckets, reset times, percentages, or defaults. An error or missing observation must be reported honestly.
- **Evidence-First Behavior**: Back implementation choices and contract decisions with recorded, sanitized evidence files under `docs/evidence/`.
- **Deterministic Fixtures and Tests**: Committed test fixtures under `tests/fixtures/` must use obviously synthetic identifiers, percentages, and timestamps. Never derive committed fixtures by copying live provider state.
- **Testing & Tooling**: Run tests and linting explicitly using the local virtual environment:
  ```bash
  .venv/bin/python -m pytest
  .venv/bin/ruff check .
  ```
