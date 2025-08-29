# Gemini Conversation Formatter

GeminiのHTML会話エクスポートからGeminiの会話データを抽出し、Markdownに変換するPythonツールです。

## 機能

- GeminiのHTMLエクスポートから `<user-query>` と `<model-response>` を抽出
- 会話データを構造化されたMarkdownフォーマットに変換
- 単一ファイルおよび一括処理をサポート
- 日本語とユニコード文字の完全対応

## システム要件

### 必要環境

- Python 3.12以上
- uvパッケージマネージャー（推奨）

### セットアップ

```bash
# リポジトリのクローン
git clone <repository-url>
cd gemini-conversation-formatter

# 仮想環境と依存関係のセットアップ
uv venv
uv sync
```

## 使用方法

### 単一ファイルの変換

```bash
# 基本的な使用法
source .venv/bin/activate
python main.py input.html

# 出力ファイルを指定
python main.py input.html output.md
```

### 一括処理

```bash
# HTMLファイルを一括変換
python main.py "*.html" --batch

# 出力ディレクトリを指定
python main.py "*.html" --batch --output-dir converted/
```

### コマンドライン引数

- `input`: 入力HTMLファイル、またはファイルパターン（一括処理時）
- `output`: 出力Markdownファイル（単一ファイル処理時）
- `--batch`: 一括処理モード
- `--output-dir`: 一括処理時の出力ディレクトリ

## 出力形式

変換されたMarkdownファイルは以下の形式になります：

```markdown
# 会話 1

## User
ユーザーの質問

## Gemini
Geminiの回答

---

# 会話 2

## User
次のユーザーの質問

## Gemini
次のGeminiの回答

---
```

## プロジェクト構造

```
gemini-conversation-formatter/
├── main.py                 # メインCLI
├── gemini_parser.py        # HTML解析
├── markdown_formatter.py   # Markdown生成
├── pyproject.toml         # プロジェクト設定
├── .venv/                 # 仮想環境
└── README.md              # このファイル
```

## アーキテクチャの詳細

### HTML解析器 (`gemini_parser.py`)

- BeautifulSoup4を使用してHTML解析
- `<user-query>`要素と`<model-response>`要素を抽出
- 複雑なHTMLマークアップと入れ子構造に対応
- エラーハンドリングと例外処理を実装

### Markdownフォーマッター (`markdown_formatter.py`)

- 質問と回答をMarkdownに構造化
- 質問番号の自動生成
- Unicode文字の適切な処理

## トラブルシューティング

### よくある問題

1. **質問が抽出されない場合**
   - HTMLファイルに`<user-query>`と`<model-response>`要素が含まれているか確認
   - ファイルのエンコーディングがUTF-8であることを確認

2. **文字化けが発生する場合**
   - 入力ファイルのエンコーディングを確認
   - 適切な文字コードで保存し直す

