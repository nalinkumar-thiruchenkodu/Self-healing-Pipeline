# Break it: 4 live failures (do ONE at a time)

Edit the file on github.com (pencil icon) and commit straight to `main`.
CI goes red, Self-Heal starts, and a fix PR appears in about 2 minutes.
Review the PR, merge it, then run the next scenario.

## 1. Messy code (fixed by tools, no AI)
In `app/main.py` add this line under the docstring and change the health route:

    import os

    return jsonify( status='ok' )

Expected: ruff removes the unused import, black fixes quotes and spaces.
PR notes say: "Layer 1 fixed it. No AI needed."
Teaching point: use cheap deterministic tools first.

## 2. Bad dependency version
In `requirements.txt` change `flask==3.0.3` to `flask==3.9.9`.

Expected: pip fails with "from versions: ...". The LLM picks a valid version
using the runbook `dependency-errors.md`.
Teaching point: the LLM reads the log like an engineer would.

## 3. Logic bug (the tests are the specification)
In `app/pricing.py` change `>=` to `>` in `if item["qty"] >= BULK_THRESHOLD:`.

Expected: `test_bulk_discount_applies_at_threshold` fails; the LLM fixes the code,
NOT the test.
Teaching point: without good tests, the bot cannot know what "correct" means.

## 4. Syntax error
In `app/main.py` delete the colon at the end of `def health():`.

Expected: ruff/pytest report a syntax error; the LLM restores the colon.

## Safety demo (optional, powerful)
Ask students: "What if the AI fix is wrong?" Answer: CI runs on the PR
(with HEAL_TOKEN), a human reviews, and nothing merges automatically.

## Reset between runs
If something gets stuck: close any open `heal/...` PR (the guard skips healing
while one is open) and delete the branch.
