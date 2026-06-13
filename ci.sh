#! /bin/bash
uv run ruff check .
uv run mypy --ignore-missing-imports --strict ./*.py xtools
