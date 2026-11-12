"""Tiny LLM helper shared by review.py and heal.py (stdlib only).

Works with any OpenAI-compatible chat API. Defaults to Google Gemini's
OpenAI-compatible endpoint. Configure with environment variables:

  LLM_API_KEY  (required, store it as a GitHub Actions secret)
  LLM_API_URL  (optional, default: Gemini OpenAI-compatible endpoint)
  LLM_MODEL    (optional, default: gemini-3.8-flash)

To switch provider, change only these values. Example for Groq:
  LLM_API_URL=https://api.groq.com/openai/v1/chat/completions
  LLM_MODEL=llama-3.3-70b-versatile
"""

import json
import os
import time
import urllib.error
import urllib.request

API_URL = os.getenv(
    "LLM_API_URL",
    "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
)
MODEL = os.getenv("LLM_MODEL", "gemini-3.8-flash")


def ask(system: str, user: str, temperature: float = 0.2) -> str:
    """Send one prompt, return the model's text. Retries on rate limits."""
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise RuntimeError("LLM_API_KEY is not set (add it as a repository secret)")

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
        "Authorization": f"Bearer {api_key}",
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
    
