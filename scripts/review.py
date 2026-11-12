"""Demo 1: AI pull request reviewer that knows the team's standards.

Reads pr.diff (built by the workflow) and CONTRIBUTING.md, asks the LLM for a
review, and writes review.md. It never blocks the PR: on any error it posts a
short "unavailable" note instead.
"""

from pathlib import Path

from llm import ask

MAX_DIFF_CHARS = 14000

SYSTEM_PROMPT = """You are a senior engineer reviewing a pull request for the \
order-service team.

Review ONLY against real problems: bugs, security issues, missing input \
validation, broken team standards, missing tests. Skip pure style nitpicks \
(a formatter handles those).

TEAM STANDARDS (from CONTRIBUTING.md):
{standards}

Reply in Markdown:
1. One line summary.
2. At most 6 bullets in the form: **[High|Medium|Low]** file - issue - suggested fix.
   Mention which team standard is broken when one applies.
3. If the change looks fine, say so in one line.
"""


def read_text(path: str) -> str:
    file = Path(path)
    return file.read_text(encoding="utf-8", errors="replace") if file.exists() else ""


def main() -> None:
    diff = read_text("pr.diff")
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS] + "\n\n[diff truncated]"

    if not diff.strip():
        body = "No code changes to review."
    else:
        standards = read_text("CONTRIBUTING.md") or "(none provided)"
        try:
            body = ask(
                SYSTEM_PROMPT.format(standards=standards),
                f"Review this diff:\n\n{diff}",
            )
        except Exception as error:  # never block the PR
            print(f"[review] {type(error).__name__}: {error}")
            body = f"AI review unavailable ({type(error).__name__}). Review manually."

    footer = "\n\n---\n_Automated review by an LLM. Advisory only; a human decides._"
    Path("review.md").write_text("### AI Review\n\n" + body + footer, encoding="utf-8")
    print(body)


if __name__ == "__main__":
    main()
