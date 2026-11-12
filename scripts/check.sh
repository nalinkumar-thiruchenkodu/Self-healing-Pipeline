#!/usr/bin/env bash
# The same checks CI runs, in one place (used by the healer to verify a fix).
set -e
pip install -q -r requirements.txt -r requirements-dev.txt
ruff check app tests
black --check app tests
pytest -q
