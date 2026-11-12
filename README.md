# order-service: self-healing pipeline demo

A small Flask orders API with tests, Docker and a CI pipeline. Three workflows:

| Workflow | File | What it does |
|---|---|---|
| CI | `.github/workflows/ci.yml` | lint (ruff), format (black), tests (pytest), docker build |
| AI PR Review | `.github/workflows/pr-review.yml` | LLM reviews each PR against `CONTRIBUTING.md`, comments, labels `ai-reviewed`. Cannot merge. |
| Self-Heal | `.github/workflows/self-heal.yml` | When CI fails on `main`: fix with black/ruff first, then the LLM; open a PR labelled `ai-healed`. Cannot merge. |

## One-time setup (5 minutes)

1. Create a new GitHub repo (personal account) and upload everything here,
   keeping the folder structure (including the hidden `.github` folder).
2. **Settings > Actions > General > Workflow permissions:**
   choose **Read and write permissions** and tick
   **Allow GitHub Actions to create and approve pull requests**. Save.
3. Do NOT add a branch ruleset that blocks direct pushes to `main` on this demo
   repo (the demo breaks `main` on purpose). The bot's fix always arrives as a PR
   and is never merged by the bot.
4. Optional but recommended: create a fine-grained personal access token
   (repo: Contents, Pull requests, read and write) and save it as the secret
   `HEAL_TOKEN`. With it, CI and the AI review also run on the fix PR.
   Without it, the fix PR is still created, but no checks run on it.
5. Push once to `main` and confirm CI is green.

## Run locally

    pip install -r requirements.txt -r requirements-dev.txt
    bash scripts/check.sh

## How the healer is built

1. CI fails on `main`, so the Self-Heal workflow starts (`workflow_run`).
2. Guard: if a `heal/` PR is already open, stop (no loops).
3. Layer 1: `black` and `ruff --fix` (no AI).
4. Layer 2: if checks still fail, send the failure output, source files, tests
   (read-only), team standards and runbooks to the LLM. Max 2 attempts.
5. Only `app/*.py` and `requirements.txt` can change. Tests never change.
6. Re-run all checks. If green: push `heal/run-<id>` and open a PR. If not:
   open an issue for a human.

Models: uses GitHub Models with the built-in `GITHUB_TOKEN`. Override the model
with the `LLM_MODEL` environment variable if the default is unavailable.
