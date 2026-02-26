#!/bin/bash
# =============================================
# Claude Code 用 API Key Helper（LiteLLM Proxy対応）
# 場所: ~/.claude/api-key-helper.sh
# =============================================

# 優先順位で環境変数をチェック（あなたの環境に合わせて調整可）
if [[ -n "${ANTHROPIC_API_KEY}" ]]; then
    echo "${ANTHROPIC_API_KEY}"
elif [[ -n "${ANTHROPIC_AUTH_TOKEN}" ]]; then
    echo "${ANTHROPIC_AUTH_TOKEN}"
elif [[ -n "${LITELLM_ANTHROPIC_TOKEN}" ]]; then
    echo "${LITELLM_ANTHROPIC_TOKEN}"
else
    echo "Error: No Anthropic API key found in environment variables." >&2
    echo "Please set one of the following in your ~/.zshrc or ~/.bashrc:" >&2
    echo "   export ANTHROPIC_AUTH_TOKEN=sk-XXXXXXXXXXXXXXXX" >&2
    echo "   # または" >&2
    echo "   export ANTHROPIC_API_KEY=sk-XXXXXXXXXXXXXXXX" >&2
    exit 1
fi