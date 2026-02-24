#!/usr/bin/env python3
import json
import sys
import os
from openai import OpenAI

## 引数解析
debug = "--debug" in sys.argv
args = [a for a in sys.argv[1:] if a not in ("--debug", "--cite")]

if len(args) < 1:
    print('Usage: python3 search_with_gemini.py [--debug] "your query"')
    print('       （--cite はデフォルトで有効です）')
    sys.exit(1)

query = args[0]

## 環境変数取得（Claude Codeのsettings.json "env" から自動注入）
# あなたの既存のANTHROPIC_変数を優先的に使う（共通なので重複不要）
api_key = os.getenv("API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")
base_url = os.getenv("BASE_URL") or os.getenv("ANTHROPIC_BASE_URL")
search_model = os.getenv("SEARCH_MODEL")

if not api_key or not base_url or not search_model:
    print(
        "エラー: ~/.claude/settings.json の \"env\" に\n"
        "ANTHROPIC_AUTH_TOKEN / ANTHROPIC_BASE_URL / SEARCH_MODEL を設定してください。",
        file=sys.stderr,
    )
    sys.exit(1)

## クライアント初期化（LiteLLMプロキシ共通）
client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

## API処理（Google Search grounding付き）
try:
    response = client.chat.completions.create(
        model=search_model,
        messages=[{"role": "user", "content": query}],
        extra_body={"tools": [{"google_search": {}}]},
    )

    if debug:
        print("=== DEBUG: Raw Response ===")
        try:
            print(json.dumps(response.model_dump(), indent=2, ensure_ascii=False, default=str))
        except Exception:
            print(repr(response))
        print("=== END DEBUG ===\n")

    raw = response.model_dump()
    content = response.choices[0].message.content or ""

    # --- 引用処理（--cite デフォルト） ---
    annotations = (
        (raw.get("choices") or [{}])[0].get("message", {}).get("annotations") or []
    )

    domain_order = []
    domain_map = {}
    insertions = []

    for ann in annotations:
        if ann.get("type") != "url_citation":
            continue
        c = ann.get("url_citation") or {}
        title = c.get("title", "")
        url = c.get("url", "")
        end_idx = c.get("end_index")
        if not title or end_idx is None:
            continue
        if title not in domain_map:
            domain_order.append((title, url))
            domain_map[title] = len(domain_order)
        ref_num = domain_map[title]
        insertions.append((end_idx, ref_num))

    content_bytes = content.encode("utf-8")
    def byte_to_char(byte_idx: int) -> int:
        clamped = min(byte_idx, len(content_bytes))
        return len(content_bytes[:clamped].decode("utf-8", errors="replace"))

    char_insertions = [(byte_to_char(end_idx), ref_num) for end_idx, ref_num in insertions]
    char_insertions.sort(key=lambda x: x[0], reverse=True)

    seen_positions = set()
    modified = content
    for char_idx, ref_num in char_insertions:
        if char_idx in seen_positions:
            continue
        seen_positions.add(char_idx)
        marker = f"[{ref_num}]"
        modified = modified[:char_idx] + marker + modified[char_idx:]

    print("=== Gemini + Google Search Grounding 結果 ===\n")
    print(modified)

    if domain_order:
        print("\n=== Grounding Sources (引用元) ===")
        for i, (title, url) in enumerate(domain_order, 1):
            print(f"  [{i}] {title}: {url}")
    else:
        print("\n=== Grounding Sources (引用元) ===")
        print("（引用元情報なし）")

except Exception as e:
    print(f"APIリクエストに失敗しました: {e}", file=sys.stderr)
    sys.exit(1)
