#!/bin/bash
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""')
QUERY=$(echo "$INPUT" | jq -r '.tool_input.query // ""')

if [[ "$TOOL_NAME" == "WebSearch" && -n "$QUERY" ]]; then
    REASON="【WebSearch は無効化されています】

Gemini + Google Search grounding を使うには、以下のコマンドを実行してください：

python3 ~/.claude/hooks/search_with_gemini.py \"$QUERY\""
    
    jq -n --arg reason "$REASON" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: $reason
      }
    }'
else
    exit 0
fi