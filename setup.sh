#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 既存の settings.json をバックアップ（存在する場合）
[ -f ~/.claude/settings.json ] && mv ~/.claude/settings.json ~/.claude/settings.json.bak

# hooks ディレクトリを作成（存在しない場合）
[ -d ~/.claude/hooks ] || mkdir -p ~/.claude/hooks

# 個別にシンボリックリンクを作成
ln -sf "$SCRIPT_DIR/.claude/settings.json" ~/.claude/settings.json
ln -sf "$SCRIPT_DIR/.claude/api-key-helper.sh" ~/.claude/api-key-helper.sh
ln -sf "$SCRIPT_DIR/.claude/hooks/override_websearch.sh" ~/.claude/hooks/override_websearch.sh
ln -sf "$SCRIPT_DIR/.claude/hooks/search_with_gemini.py" ~/.claude/hooks/search_with_gemini.py

# スクリプトに実行権限を付与
chmod +x "$SCRIPT_DIR/.claude/api-key-helper.sh"
chmod +x "$SCRIPT_DIR/.claude/hooks/override_websearch.sh"
chmod +x "$SCRIPT_DIR/.claude/hooks/search_with_gemini.py"

echo "セットアップ完了"