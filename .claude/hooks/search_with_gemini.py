#!/usr/bin/env python3
import sys
import os
from openai import OpenAI

if len(sys.argv) < 2:
    print('Usage: python3 ~/.claude/hooks/search_with_gemini.py "your query"')
    sys.exit(1)

query = sys.argv[1]

# Claude Code の settings.json "env" から取得（ANTHROPIC_変数をフォールバック）
api_key = os.getenv("API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")
base_url = os.getenv("BASE_URL") or os.getenv("ANTHROPIC_BASE_URL")
search_model = os.getenv("SEARCH_MODEL")

if not api_key or not base_url or not search_model:
    print(
        "エラー: ~/.claude/settings.json の \"env\" セクションに\n"
        "ANTHROPIC_AUTH_TOKEN / ANTHROPIC_BASE_URL / SEARCH_MODEL を設定してください。",
        file=sys.stderr,
    )
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url=base_url)

try:
    response = client.chat.completions.create(
        model=search_model,
        messages=[{"role": "user", "content": query}],
        extra_body={"tools": [{"google_search": {}}]},
    )

    content = response.choices[0].message.content or ""
    print("=== Gemini + Google Search Grounding 結果 ===\n")
    print(content)

except Exception as e:
    print(f"APIリクエストに失敗しました: {e}", file=sys.stderr)
    sys.exit(1)