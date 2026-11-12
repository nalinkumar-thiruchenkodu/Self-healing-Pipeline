# Team standards for order-service

These rules are what reviewers (human and AI) check pull requests against.

1. **Validate all input.** Functions that receive external data raise
   `ValueError` for bad values. The API turns that into a 400, never a 500.
2. **Money is rounded to 2 decimals** at every step.
3. **No bare `except:`** and no `print()` in `app/`. Catch specific errors.
4. **Type hints** on every function in `app/pricing.py`.
5. **Every behavior change needs a test.** Never edit a test just to make it pass.
6. **Keep functions short** (about 30 lines). Split when they grow.
7. **Pin dependency versions** in `requirements.txt`.
