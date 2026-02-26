#!/bin/bash
# =============================================
# Claude Code 用 API Key Helper（LiteLLM対応・LITELLM_API_KEY優先版）
# 場所: ~/.claude/api-key-helper.sh
# =============================================

# 優先順位（あなたの希望通り LITELLM_API_KEY を最優先）
if [[ -n "${LITELLM_API_KEY}" ]]; then
    echo "${LITELLM_API_KEY}"
elif [[ -n "${LITELLM_ANTHROPIC_TOKEN}" ]]; then
    echo "${LITELLM_ANTHROPIC_TOKEN}"
elif [[ -n "${ANTHROPIC_API_KEY}" ]]; then
    echo "${ANTHROPIC_API_KEY}"
elif [[ -n "${ANTHROPIC_AUTH_TOKEN}" ]]; then
    echo "${ANTHROPIC_AUTH_TOKEN}"
else
    echo "Error: No Anthropic API key found in environment variables." >&2
    echo "Please set one of the following in your ~/.zshrc or ~/.bashrc:" >&2
    echo "   export LITELLM_API_KEY=sk-XXXXXXXXXXXXXXXX" >&2
    echo "   # または" >&2
    echo "   export ANTHROPIC_AUTH_TOKEN=sk-XXXXXXXXXXXXXXXX" >&2
    exit 1
fi