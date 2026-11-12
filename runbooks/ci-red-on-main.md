# Runbook: CI is red on main

1. Open the failed run and find the FIRST failing step (lint, format, tests, docker).
2. Lint or format failure: run `ruff check --fix app tests` and `black app tests`.
3. Test failure: read the assertion. The test is the specification; fix the code,
   not the test.
4. Install failure: see `dependency-errors.md`.
5. Never push a fix straight to main. Open a PR and get one human review.
