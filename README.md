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

### 2. 設定ファイルのシンボリックリンクを作成

既存の `~/.claude` ディレクトリには Claude Code が生成する履歴・キャッシュ・認証情報などが含まれるため、ディレクトリ全体を置き換えず、**リポジトリで管理するファイルだけを個別にリンク** します。

```bash
# 既存の settings.json をバックアップ（存在する場合）
[ -f ~/.claude/settings.json ] && mv ~/.claude/settings.json ~/.claude/settings.json.bak

# hooks ディレクトリを作成（存在しない場合）
mkdir -p ~/.claude/hooks

# 個別にシンボリックリンクを作成
ln -sf "$(pwd)/.claude/settings.json" ~/.claude/settings.json
ln -sf "$(pwd)/.claude/api-key-helper.sh" ~/.claude/api-key-helper.sh
ln -sf "$(pwd)/.claude/hooks/override_websearch.sh" ~/.claude/hooks/override_websearch.sh
ln -sf "$(pwd)/.claude/hooks/search_with_gemini.py" ~/.claude/hooks/search_with_gemini.py
```

### 3. スクリプトに実行権限を付与

```bash
chmod +x .claude/api-key-helper.sh
chmod +x .claude/hooks/override_websearch.sh
chmod +x .claude/hooks/search_with_gemini.py
```

### 4. Python 依存パッケージをインストール

Gemini + Google Search grounding フック用に `openai` パッケージが必要です。

```bash
pip install openai
```

### 5. 環境変数を設定

`~/.bashrc` または `~/.zshrc` に以下を追記してください。

```bash
# Anthropic API キー（LiteLLM Proxy 等のトークン）
export ANTHROPIC_AUTH_TOKEN="sk-XXXXXXXXXXXXXXXX"
```

設定を反映します。

```bash
source ~/.bashrc  # または source ~/.zshrc
```

### 6. 動作確認

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