# godclaude

Claude Code の個人設定ファイルを管理するリポジトリです。

## 前提条件

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) がインストール済み
- Python 3 + `openai` パッケージ（Gemini 検索フック用）
- `jq` コマンド（フックスクリプト内で使用）
- 環境変数 `ANTHROPIC_AUTH_TOKEN` または `ANTHROPIC_API_KEY` が設定済み

## セットアップ手順

### 1. リポジトリをクローン

```bash
git clone https://github.com/oogamin-gu/godclaude.git
cd godclaude
```

### 2. 既存の `~/.claude` をバックアップ（存在する場合）

```bash
# 既存設定がある場合はバックアップ
[ -d ~/.claude ] && mv ~/.claude ~/.claude.bak
```

### 3. シンボリックリンクを作成

クローンした `.claude` ディレクトリを `~/.claude` としてリンクします。

```bash
ln -s "$(pwd)/.claude" ~/.claude
```

### 4. スクリプトに実行権限を付与

```bash
chmod +x ~/.claude/api-key-helper.sh
chmod +x ~/.claude/hooks/override_websearch.sh
chmod +x ~/.claude/hooks/search_with_gemini.py
```

### 5. Python 依存パッケージをインストール

Gemini + Google Search grounding フック用に `openai` パッケージが必要です。

```bash
pip install openai
```

### 6. 環境変数を設定

`~/.bashrc` または `~/.zshrc` に以下を追記してください。

```bash
# Anthropic API キー（LiteLLM Proxy 等のトークン）
export ANTHROPIC_AUTH_TOKEN="sk-XXXXXXXXXXXXXXXX"
```

設定を反映します。

```bash
source ~/.bashrc  # または source ~/.zshrc
```

### 7. 動作確認

```bash
claude
```

Claude Code が起動し、設定が反映されていれば完了です。

## ファイル構成

```
.claude/
├── settings.json                  # メイン設定ファイル
├── api-key-helper.sh              # API キー取得ヘルパースクリプト
└── hooks/
    ├── override_websearch.sh      # WebSearch を Gemini 検索に置き換えるフック
    └── search_with_gemini.py      # Gemini + Google Search grounding 実行スクリプト
```

### `settings.json`

Claude Code の中心となる設定ファイルです。

| 設定項目 | 説明 |
|---|---|
| `env.ANTHROPIC_BASE_URL` | API プロキシの URL |
| `env.ANTHROPIC_MODEL` | 使用するモデル |
| `env.SEARCH_MODEL` | Web 検索に使用する Gemini モデル |
| `apiKeyHelper` | API キー取得スクリプトのパス |
| `hooks.PreToolUse` | ツール実行前に呼ばれるフック（WebSearch の置き換え） |
| `permissions.allow` | 自動許可するツール・操作の一覧 |
| `permissions.deny` | 拒否するツール・操作の一覧（`.env` 読み取り、`rm -rf` 等） |

### `api-key-helper.sh`

環境変数から API キーを取得するヘルパースクリプトです。以下の優先順位で検索します。

1. `ANTHROPIC_API_KEY`
2. `ANTHROPIC_AUTH_TOKEN`
3. `LITELLM_ANTHROPIC_TOKEN`

### `hooks/override_websearch.sh`

Claude Code の `WebSearch` ツールを無効化し、代わりに Gemini 検索の実行コマンドを提示する PreToolUse フックです。

### `hooks/search_with_gemini.py`

Gemini + Google Search grounding を利用した Web 検索スクリプトです。OpenAI 互換 API 経由で Gemini モデルを呼び出します。

## カスタマイズ

`settings.json` の `env` セクションを編集して環境に合わせてください。

```jsonc
{
    "env": {
        "ANTHROPIC_BASE_URL": "https://your-proxy-url.example.com",  // API プロキシ URL
        "ANTHROPIC_MODEL": "claude-opus-4-6-adaptive-thinking",       // 使用モデル
        "SEARCH_MODEL": "gemini-3-flash-preview"                      // 検索用モデル
    }
}