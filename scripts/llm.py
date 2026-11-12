"""Tiny LLM helper shared by review.py and heal.py (GitHub Models, stdlib only).

Authentication is the workflow's GITHUB_TOKEN (the job needs `models: read`).
"""

import json
import os
import time
import urllib.error
import urllib.request

API_URL = "https://models.github.ai/inference/chat/completions"
MODEL = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")


def ask(system: str, user: str, temperature: float = 0.2) -> str:
    """Send one prompt, return the model's text. Retries on rate limits."""
    payload = {
        "model": MODEL,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
    }
    last_error = None
    for attempt in range(3):
        request = urllib.request.Request(
            API_URL, data=json.dumps(payload).encode("utf-8"), headers=headers
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                raw = response.read().decode("utf-8", errors="replace")
                status = response.status
            print(f"[llm] model={MODEL} HTTP {status}, {len(raw)} bytes")
            try:
                return json.loads(raw)["choices"][0]["message"]["content"]
            except (json.JSONDecodeError, KeyError, IndexError):
                print(f"[llm] unexpected reply: {raw[:300]!r}")
                raise
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")[:300]
            print(f"[llm] HTTP {error.code}: {detail}")
            last_error = error
            if error.code not in (429, 500, 502, 503):
                raise
        time.sleep(5 * (attempt + 1))
    raise last_error
